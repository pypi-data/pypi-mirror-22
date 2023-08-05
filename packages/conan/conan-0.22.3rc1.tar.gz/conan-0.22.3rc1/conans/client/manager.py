import os
import time
import shutil
from collections import OrderedDict, Counter

from conans.client import packager
from conans.client.client_cache import ClientCache
from conans.client.deps_builder import DepsGraphBuilder
from conans.client.detect import detected_os
from conans.client.export import export_conanfile, load_export_conanfile
from conans.client.generators import write_generators
from conans.client.grapher import ConanGrapher, ConanHTMLGrapher
from conans.client.importer import run_imports, undo_imports
from conans.client.installer import ConanInstaller, BuildMode
from conans.client.loader import load_consumer_conanfile, ConanFileLoader
from conans.client.manifest_manager import ManifestManager
from conans.client.output import ScopedOutput, Color
from conans.client.package_copier import PackageCopier
from conans.client.printer import Printer
from conans.client.proxy import ConanProxy
from conans.client.remote_registry import RemoteRegistry
from conans.client.remover import ConanRemover
from conans.client.require_resolver import RequireResolver
from conans.client.source import config_source, config_source_local
from conans.client.uploader import ConanUploader
from conans.client.userio import UserIO
from conans.errors import NotFoundException, ConanException
from conans.model.ref import ConanFileReference, PackageReference
from conans.paths import CONANFILE, CONANINFO, CONANFILE_TXT, CONAN_MANIFEST
from conans.tools import environment_append
from conans.util.files import save,  rmdir, normalize, mkdir
from conans.util.log import logger
from conans.model.manifest import FileTreeManifest
from conans.client.loader_parse import load_conanfile_class
from conans.client.build_requires import BuildRequires
from conans.client.linter import conan_linter


class ConanManager(object):
    """ Manage all the commands logic  The main entry point for all the client
    business logic
    """
    def __init__(self, client_cache, user_io, runner, remote_manager, search_manager):
        assert isinstance(user_io, UserIO)
        assert isinstance(client_cache, ClientCache)
        self._client_cache = client_cache
        self._user_io = user_io
        self._runner = runner
        self._remote_manager = remote_manager
        self._current_scopes = None
        self._search_manager = search_manager

    def export(self, user, conan_file_path, keep_source=False, filename=None):
        """ Export the conans
        param conanfile_path: the original source directory of the user containing a
                           conanfile.py
        param user: user under this package will be exported
        param channel: string (stable, testing,...)
        """
        assert conan_file_path
        logger.debug("Exporting %s" % conan_file_path)
        try:
            user_name, channel = user.split("/")
        except:
            user_name, channel = user, "testing"

        src_folder = conan_file_path
        conan_file_path = os.path.join(conan_file_path, filename or CONANFILE)
        conan_linter(conan_file_path, self._user_io.out)
        conanfile = load_export_conanfile(conan_file_path, self._user_io.out)
        conan_ref = ConanFileReference(conanfile.name, conanfile.version, user_name, channel)
        conan_ref_str = str(conan_ref)
        # Maybe a platform check could be added, but depends on disk partition
        refs = self._search_manager.search(conan_ref_str, ignorecase=True)
        if refs and conan_ref not in refs:
            raise ConanException("Cannot export package with same name but different case\n"
                                 "You exported '%s' but already existing '%s'"
                                 % (conan_ref_str, " ".join(str(s) for s in refs)))
        output = ScopedOutput(str(conan_ref), self._user_io.out)
        export_conanfile(output, self._client_cache, conanfile, src_folder, conan_ref, keep_source,
                         filename)

    def package_files(self, reference, path, profile):
        """ Bundle pre-existing binaries
        @param reference: ConanFileReference
        """
        conan_file_path = self._client_cache.conanfile(reference)
        if not os.path.exists(conan_file_path):
            raise ConanException("Package recipe '%s' does not exist" % str(reference))

        current_path = path
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager,
                                  remote_name=None, update=False, check_updates=False,
                                  manifest_manager=None)
        loader = ConanFileLoader(self._runner, self._client_cache.settings, profile)
        conanfile = loader.load_virtual([reference], current_path)
        graph_builder = self._get_graph_builder(loader, False, remote_proxy)
        deps_graph = graph_builder.load(conanfile)

        # this is a bit tricky, but works. The loading of a cache package makes the referenced
        # one, the first of the first level, always existing
        nodes = deps_graph.direct_requires()
        _, conanfile = nodes[0]
        packages_folder = self._client_cache.packages(reference)
        package_folder = os.path.join(packages_folder, conanfile.info.package_id())
        shutil.copytree(path, package_folder)
        save(os.path.join(package_folder, CONANINFO), conanfile.info.dumps())
        # Create the digest for the package
        digest = FileTreeManifest.create(package_folder)
        save(os.path.join(package_folder, CONAN_MANIFEST), str(digest))

    def download(self, reference, package_ids, remote=None):
        """ Download conanfile and specified packages to local repository
        @param reference: ConanFileReference
        @param package_ids: Package ids or empty for download all
        @param remote: install only from that remote
        """
        assert(isinstance(reference, ConanFileReference))
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)

        package = remote_proxy.search(reference, None)
        if not package:  # Search the reference first, and raise if it doesn't exist
            raise ConanException("'%s' not found in remote" % str(reference))

        if package_ids:
            remote_proxy.download_packages(reference, package_ids)
        else:
            packages_props = remote_proxy.search_packages(reference, None)
            if not packages_props:
                output = ScopedOutput(str(reference), self._user_io.out)
                output.warn("No remote binary packages found in remote")
            else:
                remote_proxy.download_packages(reference, list(packages_props.keys()))

    def _get_conanfile_object(self, loader, reference_or_path, conanfile_filename, current_path):
        if isinstance(reference_or_path, ConanFileReference):
            conanfile = loader.load_virtual([reference_or_path], current_path)
        else:
            output = ScopedOutput("PROJECT", self._user_io.out)
            try:
                if conanfile_filename and conanfile_filename.endswith(".txt"):
                    raise NotFoundException("")
                conan_file_path = os.path.join(reference_or_path, conanfile_filename or CONANFILE)
                conanfile = loader.load_conan(conan_file_path, output, consumer=True)
            except NotFoundException:  # Load conanfile.txt
                conan_path = os.path.join(reference_or_path, conanfile_filename or CONANFILE_TXT)
                conanfile = loader.load_conan_txt(conan_path, output)

        return conanfile

    def _get_graph_builder(self, loader, update, remote_proxy):
        local_search = None if update else self._search_manager
        resolver = RequireResolver(self._user_io.out, local_search, remote_proxy)
        graph_builder = DepsGraphBuilder(remote_proxy, self._user_io.out, loader, resolver)
        return graph_builder

    def info(self, reference, current_path, profile, remote=None,
             info=None, filename=None, check_updates=False,
             build_order=None, build_modes=None, graph_filename=None, package_filter=None,
             show_paths=False):
        """ Fetch and build all dependencies for the given reference
        @param reference: ConanFileReference or path to user space conanfile
        @param current_path: where the output files will be saved
        @param remote: install only from that remote
        @param profile: Profile object with both the -s introduced options and profile readed values
        @param build_modes: List of build_modes specified
        @param filename: Optional filename of the conanfile

        """

        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote,
                                  update=False, check_updates=check_updates)

        loader = ConanFileLoader(self._runner, self._client_cache.settings, profile)
        conanfile = self._get_conanfile_object(loader, reference, filename, current_path)
        graph_builder = self._get_graph_builder(loader, False, remote_proxy)
        deps_graph = graph_builder.load(conanfile)

        if build_order:
            result = deps_graph.build_order(build_order)
            self._user_io.out.info(", ".join(str(s) for s in result))
            return

        if build_modes is not None:
            installer = ConanInstaller(self._client_cache, self._user_io.out, remote_proxy, None)
            build_mode = BuildMode(build_modes, self._user_io.out)
            nodes = installer.nodes_to_build(deps_graph, build_mode)
            counter = Counter(ref.conan.name for ref, _ in nodes)
            self._user_io.out.info(", ".join((str(ref)
                                              if counter[ref.conan.name] > 1 else str(ref.conan))
                                             for ref, _ in nodes))
            return

        if check_updates:
            graph_updates_info = graph_builder.get_graph_updates_info(deps_graph)
        else:
            graph_updates_info = {}

        def read_dates(deps_graph):
            ret = {}
            for ref, _ in sorted(deps_graph.nodes):
                if ref:
                    manifest = self._client_cache.load_manifest(ref)
                    ret[ref] = manifest.time_str
            return ret

        # Get project reference
        project_reference = None
        if isinstance(reference, ConanFileReference):
            project_reference = None
        else:
            if conanfile.name is not None and conanfile.version is not None:
                project_reference = "%s/%s@" % (conanfile.name, conanfile.version)
                project_reference += "PROJECT"
            else:
                project_reference = "PROJECT"

        # Print results
        if graph_filename:
            if graph_filename.endswith(".html"):
                grapher = ConanHTMLGrapher(project_reference, deps_graph)
            else:
                grapher = ConanGrapher(project_reference, deps_graph)
            grapher.graph_file(graph_filename)
        else:
            registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
            Printer(self._user_io.out).print_info(deps_graph, project_reference,
                                                  info, registry, graph_updates_info,
                                                  remote, read_dates(deps_graph),
                                                  self._client_cache, package_filter, show_paths)

    def install(self, reference, current_path, profile, remote=None,
                build_modes=None, filename=None, update=False,
                manifest_folder=None, manifest_verify=False, manifest_interactive=False,
                generators=None, no_imports=False):
        """ Fetch and build all dependencies for the given reference
        @param reference: ConanFileReference or path to user space conanfile
        @param current_path: where the output files will be saved
        @param remote: install only from that remote
        @param profile: Profile object with both the -s introduced options and profile readed values
        @param build_modes: List of build_modes specified
        @param filename: Optional filename of the conanfile
        @param update: Check for updated in the upstream remotes (and update)
        @param manifest_folder: Folder to install the manifests
        @param manifest_verify: Verify dependencies manifests against stored ones
        @param manifest_interactive: Install deps manifests in folder for later verify, asking user for confirmation
        @param generators: List of generators from command line
        @param no_imports: Install specified packages but avoid running imports
        """
        generators = generators or []
        manifest_manager = ManifestManager(manifest_folder, user_io=self._user_io,
                                           client_cache=self._client_cache,
                                           verify=manifest_verify,
                                           interactive=manifest_interactive) if manifest_folder else None
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote,
                                  update=update, check_updates=False, manifest_manager=manifest_manager)
        loader = ConanFileLoader(self._runner, self._client_cache.settings, profile)
        conanfile = self._get_conanfile_object(loader, reference, filename, current_path)
        graph_builder = self._get_graph_builder(loader, update, remote_proxy)
        deps_graph = graph_builder.load(conanfile)

        # This line is so the conaninfo stores the correct complete info
        conanfile.info.scope = profile.scopes

        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)

        Printer(self._user_io.out).print_graph(deps_graph, registry)

        try:
            if detected_os() != loader._settings.os:
                message = "Cross-platform from '%s' to '%s'" % (detected_os(), loader._settings.os)
                self._user_io.out.writeln(message, Color.BRIGHT_MAGENTA)
        except ConanException:  # Setting os doesn't exist
            pass

        build_mode = BuildMode(build_modes, self._user_io.out)
        build_requires = BuildRequires(loader, remote_proxy, self._user_io.out, self._client_cache,
                                       self._search_manager, profile.build_requires, current_path,
                                       build_mode)

        # Apply build_requires to consumer conanfile
        build_requires.install("", conanfile)
        installer = ConanInstaller(self._client_cache, self._user_io.out, remote_proxy,
                                   build_requires)

        installer.install(deps_graph, build_mode, current_path)
        build_mode.report_matches()

        prefix = "PROJECT" if not isinstance(reference, ConanFileReference) else str(reference)
        output = ScopedOutput(prefix, self._user_io.out)

        # Write generators
        tmp = list(conanfile.generators)  # Add the command line specified generators
        tmp.extend(generators)
        conanfile.generators = tmp
        write_generators(conanfile, current_path, output)

        if not isinstance(reference, ConanFileReference):
            content = normalize(conanfile.info.dumps())
            save(os.path.join(current_path, CONANINFO), content)
            output.info("Generated %s" % CONANINFO)
            if not no_imports:
                run_imports(conanfile, current_path, output)
            installer.call_system_requirements(conanfile, output)

        if manifest_manager:
            manifest_manager.print_log()

    def source(self, current_path, reference, force):
        if not isinstance(reference, ConanFileReference):
            output = ScopedOutput("PROJECT", self._user_io.out)
            conanfile_path = os.path.join(reference, CONANFILE)
            conanfile = load_consumer_conanfile(conanfile_path, current_path,
                                                self._client_cache.settings, self._runner,
                                                output)
            export_folder = reference
            config_source_local(export_folder, current_path, conanfile, output)
        else:
            output = ScopedOutput(str(reference), self._user_io.out)
            conanfile_path = self._client_cache.conanfile(reference)
            conanfile = load_consumer_conanfile(conanfile_path, current_path,
                                                self._client_cache.settings, self._runner,
                                                output, reference)
            src_folder = self._client_cache.source(reference, conanfile.short_paths)
            export_folder = self._client_cache.export(reference)
            config_source(export_folder, src_folder, conanfile, output, force)

    def imports_undo(self, current_path):
        undo_imports(current_path, self._user_io.out)

    def imports(self, current_path, reference, conan_file_path, dest_folder):
        if not isinstance(reference, ConanFileReference):
            output = ScopedOutput("PROJECT", self._user_io.out)
            if not conan_file_path:
                conan_file_path = os.path.join(reference, CONANFILE)
                if not os.path.exists(conan_file_path):
                    conan_file_path = os.path.join(reference, CONANFILE_TXT)
            reference = None
        else:
            output = ScopedOutput(str(reference), self._user_io.out)
            conan_file_path = self._client_cache.conanfile(reference)

        conanfile = load_consumer_conanfile(conan_file_path, current_path,
                                            self._client_cache.settings,
                                            self._runner, output, reference, error=True)

        if dest_folder:
            if not os.path.isabs(dest_folder):
                dest_folder = os.path.normpath(os.path.join(current_path, dest_folder))
            mkdir(dest_folder)
        else:
            dest_folder = current_path
        run_imports(conanfile, dest_folder, output)

    def local_package(self, current_path, build_folder):
        if current_path == build_folder:
            raise ConanException("Cannot 'conan package' to the build folder. "
                                 "Please move to another folder and try again")
        output = ScopedOutput("PROJECT", self._user_io.out)
        conan_file_path = os.path.join(build_folder, CONANFILE)
        conanfile = load_consumer_conanfile(conan_file_path, current_path,
                                            self._client_cache.settings,
                                            self._runner, output)
        packager.create_package(conanfile, build_folder, current_path, output, local=True)

    def package(self, reference, package_id):
        # Package paths
        conan_file_path = self._client_cache.conanfile(reference)
        if not os.path.exists(conan_file_path):
            raise ConanException("Package recipe '%s' does not exist" % str(reference))

        conanfile = load_conanfile_class(conan_file_path)
        if hasattr(conanfile, "build_id"):
            raise ConanException("package command does not support recipes with 'build_id'\n"
                                 "To repackage them use 'conan install'")

        if not package_id:
            packages = [PackageReference(reference, packid)
                        for packid in self._client_cache.conan_builds(reference)]
            if not packages:
                raise NotFoundException("%s: Package recipe has not been built locally\n"
                                        "Please read the 'conan package' command help\n"
                                        "Use 'conan install' or 'conan test_package' to build and "
                                        "create binaries" % str(reference))
        else:
            packages = [PackageReference(reference, package_id)]

        for package_reference in packages:
            build_folder = self._client_cache.build(package_reference, short_paths=None)
            if not os.path.exists(build_folder):
                raise NotFoundException("%s: Package binary '%s' folder doesn't exist\n"
                                        "Please read the 'conan package' command help\n"
                                        "Use 'conan install' or 'conan test_package' to build and "
                                        "create binaries"
                                        % (str(reference), package_reference.package_id))
            # The package already exist, we can use short_paths if they were defined
            package_folder = self._client_cache.package(package_reference, short_paths=None)
            # Will read current conaninfo with specified options and load conanfile with them
            output = ScopedOutput(str(reference), self._user_io.out)
            output.info("Re-packaging %s" % package_reference.package_id)
            conanfile = load_consumer_conanfile(conan_file_path, build_folder,
                                                self._client_cache.settings,
                                                self._runner, output, reference)
            rmdir(package_folder)
            with environment_append(conanfile.env):
                packager.create_package(conanfile, build_folder, package_folder, output)

    def build(self, conanfile_path, current_path, test=False, filename=None):
        """ Call to build() method saved on the conanfile.py
        param conanfile_path: the original source directory of the user containing a
                            conanfile.py
        """
        logger.debug("Building in %s" % current_path)
        logger.debug("Conanfile in %s" % conanfile_path)

        if filename and filename.endswith(".txt"):
            raise ConanException("A conanfile.py is needed to call 'conan build'")

        conan_file_path = os.path.join(conanfile_path, filename or CONANFILE)

        try:
            # Append env_vars to execution environment and clear when block code ends
            output = ScopedOutput("Project", self._user_io.out)
            conan_file = load_consumer_conanfile(conan_file_path, current_path,
                                                 self._client_cache.settings,
                                                 self._runner, output)
        except NotFoundException:
            # TODO: Auto generate conanfile from requirements file
            raise ConanException("'%s' file is needed for build.\n"
                                 "Create a '%s' and move manually the "
                                 "requirements and generators from '%s' file"
                                 % (CONANFILE, CONANFILE, CONANFILE_TXT))
        try:
            os.chdir(current_path)
            conan_file._conanfile_directory = conanfile_path
            with environment_append(conan_file.env):
                conan_file.build()

            if test:
                conan_file.test()
        except ConanException:
            raise  # Raise but not let to reach the Exception except (not print traceback)
        except Exception:
            import traceback
            trace = traceback.format_exc().split('\n')
            raise ConanException("Unable to build it successfully\n%s" % '\n'.join(trace[3:]))

    def upload(self, conan_reference_or_pattern, package_id=None, remote=None, all_packages=None,
               force=False, confirm=False, retry=0, retry_wait=0, skip_upload=False):
        """If package_id is provided, conan_reference_or_pattern is a ConanFileReference"""
        t1 = time.time()
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager,
                                  remote)
        uploader = ConanUploader(self._client_cache, self._user_io, remote_proxy,
                                 self._search_manager)

        if package_id:  # Upload package
            ref = ConanFileReference.loads(conan_reference_or_pattern)
            uploader.check_reference(ref)
            uploader.upload_package(PackageReference(ref, package_id), retry=retry,
                                    retry_wait=retry_wait, skip_upload=skip_upload)
        else:  # Upload conans
            uploader.upload(conan_reference_or_pattern, all_packages=all_packages,
                            force=force, confirm=confirm,
                            retry=retry, retry_wait=retry_wait, skip_upload=skip_upload)

        logger.debug("====> Time manager upload: %f" % (time.time() - t1))

    def search(self, pattern_or_reference=None, remote=None, ignorecase=True, packages_query=None):
        """ Print the single information saved in conan.vars about all the packages
            or the packages which match with a pattern

            Attributes:
                pattern = string to match packages
                remote = search on another origin to get packages info
                packages_pattern = String query with binary
                                   packages properties: "arch=x86 AND os=Windows"
        """
        printer = Printer(self._user_io.out)

        if remote:
            remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager,
                                      remote)
            adapter = remote_proxy
        else:
            adapter = self._search_manager
        if isinstance(pattern_or_reference, ConanFileReference):
            packages_props = adapter.search_packages(pattern_or_reference, packages_query)
            ordered_packages = OrderedDict(sorted(packages_props.items()))
            try:
                recipe_hash = self._client_cache.load_manifest(pattern_or_reference).summary_hash
            except IOError:  # It could not exist in local
                recipe_hash = None
            printer.print_search_packages(ordered_packages, pattern_or_reference,
                                          recipe_hash, packages_query)
        else:
            references = adapter.search(pattern_or_reference, ignorecase)
            printer.print_search_recipes(references, pattern_or_reference)

    def copy(self, reference, package_ids, username, channel, force=False):
        """ Copy or move conanfile (exported) and packages to another user and or channel
        @param reference: ConanFileReference containing the packages to be moved
        @param package_ids: list of ids or [] for all list
        @param username: Destination username
        @param channel: Destination channel
        @param remote: install only from that remote
        """
        # It is necessary to make sure the sources are complete before proceeding
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, None)
        remote_proxy.complete_recipe_sources(reference)

        # Now we can actually copy
        conan_file_path = self._client_cache.conanfile(reference)
        conanfile = load_conanfile_class(conan_file_path)
        copier = PackageCopier(self._client_cache, self._user_io, conanfile.short_paths)
        if not package_ids:
            packages = self._client_cache.packages(reference)
            if os.path.exists(packages):
                package_ids = os.listdir(packages)
            else:
                package_ids = []
        copier.copy(reference, package_ids, username, channel, force)

    def remove(self, pattern, src=False, build_ids=None, package_ids_filter=None, force=False,
               remote=None, packages_query=None):
        """ Remove conans and/or packages
        @param pattern: string to match packages
        @param src: Remove src folder
        @param package_ids_filter: list of ids or [] for all list
        @param build_ids: list of ids or [] for all list
        @param remote: search on another origin to get packages info
        @param force: if True, it will be deleted without requesting anything
        @param packages_query: Only if src is a reference. Query settings and options
        """
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)
        remover = ConanRemover(self._client_cache, self._search_manager, self._user_io,
                               remote_proxy)
        remover.remove(pattern, src, build_ids, package_ids_filter, force=force, packages_query=packages_query)

    def user(self, remote=None, name=None, password=None):
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)
        return remote_proxy.authenticate(name, password)
