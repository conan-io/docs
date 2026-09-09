Changelog
=========

For a more detailed description of the major changes that Conan 2 brings, compared with Conan 1.X, please read :ref:`whatsnew`

2.0.17 (10-Jan-2024)
--------------------

- Fix: Automatically create folder if ``conan cache save --file=subfolder/file.tgz`` subfolder doesn't exist. `#15409 <https://github.com/conan-io/conan/pull/15409>`_
- Bugfix: Fix libcxx detection when using `CC/CXX` env vars. `#15418 <https://github.com/conan-io/conan/pull/15418>`_ . Docs `here <https://github.com/conan-io/docs/pull/3509>`__
- Bugfix: Solve ``winsdk_version`` bug in ``CMakeToolchain`` generator for ``cmake_minimum_required(3.27)``. `#15373 <https://github.com/conan-io/conan/pull/15373>`_
- Bugfix: Fix visible trait propagation with ``build=True`` trait. `#15357 <https://github.com/conan-io/conan/pull/15357>`_
- Bugfix: Fix `package_id` calculation when including conf values thru `tools.info.package_id:confs`. `#15356 <https://github.com/conan-io/conan/pull/15356>`_
- Bugfix: Order `conf` items when dumping them to allow reproducible `package_id` independent of the order the confs were declared. `#15356 <https://github.com/conan-io/conan/pull/15356>`_


2.0.16 (21-Dec-2023)
--------------------

- Bugfix: Revert the default of ``source_buildenv``, make it ``False`` by default. `#15319 <https://github.com/conan-io/conan/pull/15319>`_ . Docs `here <https://github.com/conan-io/docs/pull/3501>`__


2.0.15 (20-Dec-2023)
--------------------

- Feature: New ``conan lock remove`` command to remove requires from lockfiles. `#15284 <https://github.com/conan-io/conan/pull/15284>`_ . Docs `here <https://github.com/conan-io/docs/pull/3496>`__
- Feature: New ``CMake.ctest()`` helper method to launch directly ``ctest`` instead of via ``cmake --target=RUN_TEST``. `#15282 <https://github.com/conan-io/conan/pull/15282>`_
- Feature: Add tracking syntax in `<host_version>` for different references. `#15274 <https://github.com/conan-io/conan/pull/15274>`_ . Docs `here <https://github.com/conan-io/docs/pull/3480>`__
- Feature: Adding ``tools.microsoft:winsdk_version`` conf to make ``VCVars`` generator to use the given ``winsdk_version``. `#15272 <https://github.com/conan-io/conan/pull/15272>`_ . Docs `here <https://github.com/conan-io/docs/pull/3487>`__
- Feature: Add `pkglist` formatter for conan export command. `#15266 <https://github.com/conan-io/conan/pull/15266>`_ . Docs `here <https://github.com/conan-io/docs/pull/3483>`__
- Feature: Define ``CONAN_LOG_LEVEL`` env-var to be able to change verbosity at a global level. `#15263 <https://github.com/conan-io/conan/pull/15263>`_ . Docs `here <https://github.com/conan-io/docs/pull/3490>`__
- Feature: `conan cache path xxx --folder xxxx` raises an error if the folder requested does not exist. `#15257 <https://github.com/conan-io/conan/pull/15257>`_
- Feature: Add `in` operator support for ConanFile's `self.dependencies`. `#15221 <https://github.com/conan-io/conan/pull/15221>`_ . Docs `here <https://github.com/conan-io/docs/pull/3481>`__
- Feature: Make ``CMakeDeps`` generator create a ``conandeps.cmake`` that aggregates all direct dependencies in a ``cmake``-like generator style. `#15207 <https://github.com/conan-io/conan/pull/15207>`_ . Docs `here <https://github.com/conan-io/docs/pull/3492>`__
- Feature: Add build environment information to CMake configure preset and run environment information to CMake test presets. `#15192 <https://github.com/conan-io/conan/pull/15192>`_ . Docs `here <https://github.com/conan-io/docs/pull/3488>`__
- Feature: Removed a warning about a potential issue with conan migration that would print every time a build failed. `#15174 <https://github.com/conan-io/conan/pull/15174>`_
- Feature: New ``deploy()`` method in recipes for explicit per-recipe deployment. `#15172 <https://github.com/conan-io/conan/pull/15172>`_ . Docs `here <https://github.com/conan-io/docs/pull/3494>`__
- Feature: Allow ``tool-requires`` to be used in ``source()`` method injecting environment. `#15153 <https://github.com/conan-io/conan/pull/15153>`_ . Docs `here <https://github.com/conan-io/docs/pull/3493>`__
- Feature: Allow accessing the contents of `settings.yml` (and `settings_user`!) from `ConfigAPI`. `#15151 <https://github.com/conan-io/conan/pull/15151>`_
- Feature: Add builtin conf access from `ConfigAPI`. `#15151 <https://github.com/conan-io/conan/pull/15151>`_
- Feature: Add `redirect_stdout` to CMake integration methods. `#15150 <https://github.com/conan-io/conan/pull/15150>`_
- Feature: Add `core:warnings_as_errors` configuration option to make Conan raise on warnings and errors. `#15149 <https://github.com/conan-io/conan/pull/15149>`_ . Docs `here <https://github.com/conan-io/docs/pull/3484>`__
- Feature: Added `FTP_TLS` option using `secure` argument in `ftp_download` for secure communication. `#15137 <https://github.com/conan-io/conan/pull/15137>`_
- Feature: New ``[replace_requires]`` and ``[replace_tool_requires]`` in profile for redefining requires, useful for package replacements like ``zlibng/zlib``, to solve conflicts, and to replace some dependencies by system alternatives wrapped in another Conan package recipe. `#15136 <https://github.com/conan-io/conan/pull/15136>`_ . Docs `here <https://github.com/conan-io/docs/pull/3495>`__
- Feature: Add `stderr` capture argument to conanfile's `run()` method. `#15121 <https://github.com/conan-io/conan/pull/15121>`_ . Docs `here <https://github.com/conan-io/docs/pull/3482>`__
- Feature: New ``[platform_requires]`` profile definition to be able to replace Conan dependencies by platform-provided dependencies. `#14871 <https://github.com/conan-io/conan/pull/14871>`_ . Docs `here <https://github.com/conan-io/docs/pull/3495>`__
- Feature: New ``conan graph explain`` command to search, compare and explain missing binaries. `#14694 <https://github.com/conan-io/conan/pull/14694>`_ . Docs `here <https://github.com/conan-io/docs/pull/3486>`__
- Feature: Global ``cpp_info`` can be used to initialize components values. `#13994 <https://github.com/conan-io/conan/pull/13994>`_
- Fix: Make `core:warnings_as_errors` accept a list `#15297 <https://github.com/conan-io/conan/pull/15297>`_
- Fix: Fix `user` confs package scoping when no separator was given `#15296 <https://github.com/conan-io/conan/pull/15296>`_
- Fix: Fix range escaping in conflict reports involving ranges. `#15222 <https://github.com/conan-io/conan/pull/15222>`_
- Fix: Allow hard ``set_name()`` and ``set_version()`` to mutate name and version provided in command line. `#15211 <https://github.com/conan-io/conan/pull/15211>`_ . Docs `here <https://github.com/conan-io/docs/pull/3491>`__
- Fix: Make `conan graph info --format=text` print to stdout. `#15170 <https://github.com/conan-io/conan/pull/15170>`_
- Fix: Avoid warning in CMake output due to `CMAKE_POLICY_DEFAULT_CMP0091` unused variable. `#15127 <https://github.com/conan-io/conan/pull/15127>`_
- Fix: Deprecate ``[system_tools]`` in favor of ``[platform_tool_requires]`` to align with ``[platform_requires]`` for regular dependencies. Changed output from "System tool" to "Platform". `#14871 <https://github.com/conan-io/conan/pull/14871>`_ . Docs `here <https://github.com/conan-io/docs/pull/3495>`__
- Bugfix: Ensure `user` confs have at least 1 `:` separator `#15296 <https://github.com/conan-io/conan/pull/15296>`_
- Bugfix: ``Git.is_dirty()`` will use ``git status . -s`` to make sure it only process the current path, not the whole repo, similarly to other ``Git`` methods. `#15289 <https://github.com/conan-io/conan/pull/15289>`_
- Bugfix: Make ``self.info.clear()`` and header-only packages to remove ``python_requires`` and ``tool_requires``. `#15285 <https://github.com/conan-io/conan/pull/15285>`_ . Docs `here <https://github.com/conan-io/docs/pull/3485>`__
- Bugfix: Make ``conan cache save/restore`` portable across Windows and other OSs. `#15253 <https://github.com/conan-io/conan/pull/15253>`_
- Bugfix: Do not relativize absolute paths in ``deployers``. `#15244 <https://github.com/conan-io/conan/pull/15244>`_
- Bugfix: Add ``architecture`` to ``CMakePresets`` to avoid cmake ignoring toolchain definitions when using presets. `#15215 <https://github.com/conan-io/conan/pull/15215>`_
- Bugfix: Fix `conan graph info --format=html` reporting misleading conflicting nodes. `#15196 <https://github.com/conan-io/conan/pull/15196>`_
- Bugfix: Fix serialization of tool_requires in `conan profile show --format=json`. `#15185 <https://github.com/conan-io/conan/pull/15185>`_
- Bugfix: Fix NMakeDeps quoting issues. `#15140 <https://github.com/conan-io/conan/pull/15140>`_
- Bugfix: Fix the 2.0.14 migration to add LRU data to the cache when ``storage_path`` conf is defined. `#15135 <https://github.com/conan-io/conan/pull/15135>`_
- Bugfix: Fix definition of ``package_metadata_folder`` for :command:`conan export-pkg` command. `#15126 <https://github.com/conan-io/conan/pull/15126>`_
- Bugfix: `pyinstaller.py` was broken for Python 3.12 due to a useless `distutils` import. `#15116 <https://github.com/conan-io/conan/pull/15116>`_
- Bugfix: Fix backup sources error when no `core.sources:download_cache` is set. `#15109 <https://github.com/conan-io/conan/pull/15109>`_


2.0.14 (14-Nov-2023)
--------------------

- Feature: Added ``riscv64, riscv32`` architectures to default ``settings.yml`` and management of them in Meson and Autotools. `#15053 <https://github.com/conan-io/conan/pull/15053>`_
- Feature: Allow only one simultaneous database connection. `#15029 <https://github.com/conan-io/conan/pull/15029>`_
- Feature: Add `conan cache backup-upload` to upload all the backup sources in the cache, regardless of which references they are from `#15013 <https://github.com/conan-io/conan/pull/15013>`_ . Docs `here <https://github.com/conan-io/docs/pull/3438>`__
- Feature: New ``conan list --format=compact`` for better UX. `#15011 <https://github.com/conan-io/conan/pull/15011>`_ . Docs `here <https://github.com/conan-io/docs/pull/3446>`__
- Feature: Ignore metadata upload by passing --metadata="" `#15007 <https://github.com/conan-io/conan/pull/15007>`_ . Docs `here <https://github.com/conan-io/docs/pull/3436>`__
- Feature: Better output messages in :command:`conan upload` `#14984 <https://github.com/conan-io/conan/pull/14984>`_
- Feature: Add extra flags to CMakeToolchain. `#14966 <https://github.com/conan-io/conan/pull/14966>`_ . Docs `here <https://github.com/conan-io/docs/pull/3452>`__
- Feature: Implement package load/restore from the cache, for CI workflows and moving packages over air-gaps. `#14923 <https://github.com/conan-io/conan/pull/14923>`_ . Docs `here <https://github.com/conan-io/docs/pull/3453>`__
- Feature: Compute version-ranges intersection to avoid graph version conflicts for compatible ranges `#14912 <https://github.com/conan-io/conan/pull/14912>`_
- Feature: CMake helper can use multiple targets in target argument. `#14883 <https://github.com/conan-io/conan/pull/14883>`_
- Feature: Add Macos 13.6 to settings.yml. `#14858 <https://github.com/conan-io/conan/pull/14858>`_ . Docs `here <https://github.com/conan-io/docs/pull/3416>`__
- Feature: Add CMakeDeps and PkgConfigDeps generators listening to system_package_version property. `#14808 <https://github.com/conan-io/conan/pull/14808>`_ . Docs `here <https://github.com/conan-io/docs/pull/3399>`__
- Feature: Add shorthand syntax in cli to specify host and build in 1 argument `#14727 <https://github.com/conan-io/conan/pull/14727>`_ . Docs `here <https://github.com/conan-io/docs/pull/3439>`__
- Feature: Implement cache LRU control for cleaning of unused artifacts. `#14054 <https://github.com/conan-io/conan/pull/14054>`_ . Docs `here <https://github.com/conan-io/docs/pull/3455>`__
- Fix: Avoid ``CMakeToolchain`` overwriting user ``CMakePresets.json`` when no layout nor output-folder is defined `#15058 <https://github.com/conan-io/conan/pull/15058>`_
- Fix: Add ``astra``, ``elbrus`` and ``altlinux`` as distribution using ``apt`` in SystemPackageManager `#15051 <https://github.com/conan-io/conan/pull/15051>`_
- Fix: Default to apt-get package manager in Linux Mint `#15026 <https://github.com/conan-io/conan/pull/15026>`_ . Docs `here <https://github.com/conan-io/docs/pull/3441>`__
- Fix: Make ``Git()`` check commits in remote server even for shallow clones. `#15023 <https://github.com/conan-io/conan/pull/15023>`_
- Fix: Add new Apple OS versions to settings.yml `#15015 <https://github.com/conan-io/conan/pull/15015>`_
- Fix: Fix AutotoolsToolchain extraflags priority. `#15005 <https://github.com/conan-io/conan/pull/15005>`_ . Docs `here <https://github.com/conan-io/docs/pull/3451>`__
- Fix: Remove colors from ``conan --version`` output `#15002 <https://github.com/conan-io/conan/pull/15002>`_
- Fix: Add an error message if the sqlite3 version is unsupported (less than 3.7.11 from 2012) `#14950 <https://github.com/conan-io/conan/pull/14950>`_
- Fix: Make cache DB always use forward slash for paths, to be uniform across Windows and Linux `#14940 <https://github.com/conan-io/conan/pull/14940>`_
- Fix: Solve re-build of an existing package revision (like forcing rebuild of a an existing header-only package), while previous folder was still used by other projects. `#14938 <https://github.com/conan-io/conan/pull/14938>`_
- Fix: Avoid a recipe mutating a ``conf`` to affect other recipes. `#14932 <https://github.com/conan-io/conan/pull/14932>`_ . Docs `here <https://github.com/conan-io/docs/pull/3449>`__
- Fix: The output of system packages via ``Apt.install()`` or ``PkgConfig.fill_cpp_info``, like ``xorg/system`` was very noisy to the Conan output, making it more quiet `#14924 <https://github.com/conan-io/conan/pull/14924>`_
- Fix: Serialize the ``path`` information of ``python_requires``, necessary for computing buildinfo `#14886 <https://github.com/conan-io/conan/pull/14886>`_
- Fix: Define remotes in :command:`conan source` command in case recipe has ``python_requires`` that need to be downloaded from remotes. `#14852 <https://github.com/conan-io/conan/pull/14852>`_
- Fix: Fix min target flag for xros and xros-simulator. `#14776 <https://github.com/conan-io/conan/pull/14776>`_
- Bugfix: ``--build=missing`` was doing unnecessary builds of packages that were not needed and could be skipped, in the case of ``tool_requires`` having transitive dependencies. `#15082 <https://github.com/conan-io/conan/pull/15082>`_
- BugFix: Add package revision to format=json in 'conan export-pkg' command `#15042 <https://github.com/conan-io/conan/pull/15042>`_
- Bugfix: ``tools.build:download_source=True`` will not fail when there are editable packages. `#15004 <https://github.com/conan-io/conan/pull/15004>`_ . Docs `here <https://github.com/conan-io/docs/pull/3448>`__
- Bugfix: Transitive dependencies were incorrectly added to conandeps.xcconfig. `#14898 <https://github.com/conan-io/conan/pull/14898>`_
- Bugfix: Fix integrity-check (``upload --check`` or ``cache check-integrity``) when the ``export_source`` has not been downloaded `#14850 <https://github.com/conan-io/conan/pull/14850>`_
- Bugfix: Properly lock release candidates of python requires `#14846 <https://github.com/conan-io/conan/pull/14846>`_
- BugFix: Version ranges ending with ``-`` do not automatically activate pre-releases resolution in the full range. `#14814 <https://github.com/conan-io/conan/pull/14814>`_ . Docs `here <https://github.com/conan-io/docs/pull/3454>`__
- BugFix: Fix version ranges so pre-releases are correctly included in the lower bound and excluded in the upper bound. `#14814 <https://github.com/conan-io/conan/pull/14814>`_ . Docs `here <https://github.com/conan-io/docs/pull/3454>`__


2.0.13 (28-Sept-2023)
---------------------

- Bugfix: Fix wrong cppstd detection for newer apple-clang versions introduced in 2.0.11. `#14837 <https://github.com/conan-io/conan/pull/14837>`_

2.0.12 (26-Sept-2023)
---------------------

- Feature: Add support for Clang 17. `#14781 <https://github.com/conan-io/conan/pull/14781>`_ . Docs `here <https://github.com/conan-io/docs/pull/3398>`__
- Feature: Add `--dry-run` for :command:`conan remove`. `#14760 <https://github.com/conan-io/conan/pull/14760>`_ . Docs `here <https://github.com/conan-io/docs/pull/3404>`__
- Feature: Add `host_tool` to `install()` method in `package_manager` to indicate whether the package is a host tool or a library. `#14752 <https://github.com/conan-io/conan/pull/14752>`_ . Docs `here <https://github.com/conan-io/docs/pull/3401>`__
- Fix: Better error message when trying to ``export-pkg`` a ``python-require`` package, and avoid it being exported and then failing. `#14819 <https://github.com/conan-io/conan/pull/14819>`_
- Fix: ``CMakeDeps`` allows ``set_property()`` on all properties. `#14813 <https://github.com/conan-io/conan/pull/14813>`_
- Fix: Add minor version for Apple clang 15.0. `#14797 <https://github.com/conan-io/conan/pull/14797>`_ . Docs `here <https://github.com/conan-io/docs/pull/3402>`__
- Fix: :command:`conan build` command prettier error when <path> argument not provided. `#14787 <https://github.com/conan-io/conan/pull/14787>`_
- Bugfix: fix ``compatibility()`` over ``settings_target`` making it None `#14825 <https://github.com/conan-io/conan/pull/14825>`_
- Bugfix: ``compatible`` packages look first in the cache, and only if not found, the servers, to allow offline installs when there are compatible packages. `#14800 <https://github.com/conan-io/conan/pull/14800>`_
- BugFix: Reuse session in ConanRequester to speed up requests. `#14795 <https://github.com/conan-io/conan/pull/14795>`_
- Bugfix: Fix relative paths of ``editable`` packages when they have components partially defining directories. `#14782 <https://github.com/conan-io/conan/pull/14782>`_

2.0.11 (18-Sept-2023)
---------------------

- Feature: Add ``--format=json`` formatter to ``conan profile show`` command `#14743 <https://github.com/conan-io/conan/pull/14743>`_ . Docs `here <https://github.com/conan-io/docs/pull/3388>`__
- Feature: add new --deployer --generators args to 'conan build' cmd `#14737 <https://github.com/conan-io/conan/pull/14737>`_ . Docs `here <https://github.com/conan-io/docs/pull/3383>`__
- Feature: Better ``CMakeToolchain`` blocks interface. Added new ``.blocks.select()``, ``.blocks.keys()``. `#14731 <https://github.com/conan-io/conan/pull/14731>`_ . Docs `here <https://github.com/conan-io/docs/pull/3384>`__
- Feature: Add message when copying large files from download cache instead of downloading from server. `#14716 <https://github.com/conan-io/conan/pull/14716>`_
- Feature: MesonToolchain shows a warning message if any options are used directly. `#14692 <https://github.com/conan-io/conan/pull/14692>`_ . Docs `here <https://github.com/conan-io/docs/pull/3381>`__
- Feature: Support clang-cl in default profile plugin. `#14682 <https://github.com/conan-io/conan/pull/14682>`_ . Docs `here <https://github.com/conan-io/docs/pull/3387>`__
- Feature: Added mechanism to transform `c`, `cpp`, and/or `ld` binaries variables from Meson into lists if declared blank-separated strings. `#14676 <https://github.com/conan-io/conan/pull/14676>`_
- Feature: Add `nobara` distro to `dnf` package manager mapping. `#14668 <https://github.com/conan-io/conan/pull/14668>`_
- Feature: Ensure meson toolchain sets `b_vscrt` with clang-cl. `#14664 <https://github.com/conan-io/conan/pull/14664>`_
- Feature: Supporting regex pattern for conf `tools.info.package_id:confs` `#14621 <https://github.com/conan-io/conan/pull/14621>`_ . Docs `here <https://github.com/conan-io/docs/pull/3382>`__
- Feature: MakeDeps: Provide "require" information, and more styling tweaks. `#14605 <https://github.com/conan-io/conan/pull/14605>`_
- Feature: New ``detect_api`` to be used in profiles jinja templates. `#14578 <https://github.com/conan-io/conan/pull/14578>`_ . Docs `here <https://github.com/conan-io/docs/pull/3390>`__
- Feature: Allow access to `settings_target` in compatibility method. `#14532 <https://github.com/conan-io/conan/pull/14532>`_
- Fix: Add missing minor macos versions `#14740 <https://github.com/conan-io/conan/pull/14740>`_ . Docs `here <https://github.com/conan-io/docs/pull/3389>`__
- Fix: Improve error messages in `ConanApi` init failures, `#14735 <https://github.com/conan-io/conan/pull/14735>`_
- Fix: CMakeDeps: Remove "Target name ... already exists" warning about duplicating aliases. `#14644 <https://github.com/conan-io/conan/pull/14644>`_
- Bugfix: Fix regression in ``Git.run()`` when ``win_bash=True``. `#14756 <https://github.com/conan-io/conan/pull/14756>`_
- Bugfix: Change the default `check=False` in `conan.tools.system.package_manager.Apt`  to `True` as the other package manager tools. `#14728 <https://github.com/conan-io/conan/pull/14728>`_ . Docs `here <https://github.com/conan-io/docs/pull/3380>`__
- Bugfix: Solved propagation of transitive shared dependencies of ``test_requires`` with diamonds. `#14721 <https://github.com/conan-io/conan/pull/14721>`_
- Bugfix: Solve crash with :command:`conan export-pkg` with ``test_package`` doing calls to remotes. `#14712 <https://github.com/conan-io/conan/pull/14712>`_
- Bugfix: Do not binary-skip packages that have transitive dependencies that are not skipped, otherwise the build chain of build systems to those transitive dependencies like ``CMakeDeps`` generated files are broken. `#14673 <https://github.com/conan-io/conan/pull/14673>`_
- Bugfix: Fix detected CPU architecture when running ``conan profile detect`` on native ARM64 Windows. `#14667 <https://github.com/conan-io/conan/pull/14667>`_
- Bugfix: ``conan lock create --update`` now correctly updates references from servers if newer than cache ones. `#14643 <https://github.com/conan-io/conan/pull/14643>`_
- Bugfix: Fix unnecessarily decorating command stdout with escape sequences. `#14642 <https://github.com/conan-io/conan/pull/14642>`_
- Bugfix: ``tools.info.package_id:confs`` shouldn't affect header-only libraries. `#14622 <https://github.com/conan-io/conan/pull/14622>`_

2.0.10 (29-Aug-2023)
--------------------

- Feature: Allow ``patch_user`` in ``conandata.yml`` definition for user patches, not handled by ``apply_conandata_patches()``. `#14576 <https://github.com/conan-io/conan/pull/14576>`_ . Docs `here <https://github.com/conan-io/docs/pull/3332>`__
- Feature: Support for Xcode 15, iOS 17, tvOS 17, watchOS 10, macOS 14. `#14538 <https://github.com/conan-io/conan/pull/14538>`_
- Feature: Raise an error if users are adding incorrect ConanCenter web URL as remote. `#14531 <https://github.com/conan-io/conan/pull/14531>`_
- Feature: Serialization of graph with ``--format=json`` adds information to ``python_requires`` so ``conan list --graph`` can list ``python_requires`` too. `#14529 <https://github.com/conan-io/conan/pull/14529>`_
- Feature: Add ``rrev``, ``rrev_timestamp`` and ``prev_timestamp`` to the graph json serialization. `#14526 <https://github.com/conan-io/conan/pull/14526>`_
- Feature: Allow ``version-ranges`` to resolve to editable packages too. `#14510 <https://github.com/conan-io/conan/pull/14510>`_
- Feature: Add `tools.files.download:verify`. `#14508 <https://github.com/conan-io/conan/pull/14508>`_ . Docs `here <https://github.com/conan-io/docs/pull/3341>`__
- Feature: Add support for Apple visionOS. `#14504 <https://github.com/conan-io/conan/pull/14504>`_
- Feature: Warn of unknown version range options. `#14493 <https://github.com/conan-io/conan/pull/14493>`_
- Feature: Add `tools.graph:skip_binaries` to control binary skipping in the graph. `#14466 <https://github.com/conan-io/conan/pull/14466>`_ . Docs `here <https://github.com/conan-io/docs/pull/3342>`__
- Feature: New ``tools.deployer:symlinks`` configuration to disable symlinks copy in deployers. `#14461 <https://github.com/conan-io/conan/pull/14461>`_ . Docs `here <https://github.com/conan-io/docs/pull/3335>`__
- Feature: Allow remotes to automatically resolve missing ``python_requires`` in 'editable add'. `#14413 <https://github.com/conan-io/conan/pull/14413>`_ . Docs `here <https://github.com/conan-io/docs/pull/3345>`__
- Feature: Add ``cli_args`` argument for ``CMake.install()``. `#14397 <https://github.com/conan-io/conan/pull/14397>`_ . Docs `here <https://github.com/conan-io/docs/pull/3314>`__
- Feature: Allow ``test_requires(..., force=True)``. `#14394 <https://github.com/conan-io/conan/pull/14394>`_ . Docs `here <https://github.com/conan-io/docs/pull/3349>`__
- Feature: New ``credentials.json`` file to store credentials for Conan remotes. `#14392 <https://github.com/conan-io/conan/pull/14392>`_ . Docs `here <https://github.com/conan-io/docs/pull/3350>`__
- Feature: Added support for `apk` package manager and Alpine Linux `#14382 <https://github.com/conan-io/conan/pull/14382>`_ . Docs `here <https://github.com/conan-io/docs/pull/3312>`__
- Feature: `conan profile detect` can now detect the version of msvc when invoked within a Visual Studio prompt where `CC` or `CXX` are defined and pointing to the `cl` compiler executable `#14364 <https://github.com/conan-io/conan/pull/14364>`_
- Feature: Properly document ``--build=editable`` build mode. `#14358 <https://github.com/conan-io/conan/pull/14358>`_ . Docs `here <https://github.com/conan-io/docs/pull/3308>`__
- Feature: ``conan create --build-test=missing`` new argument to control what is being built as dependencies of the ``test_package`` folder. `#14347 <https://github.com/conan-io/conan/pull/14347>`_ . Docs `here <https://github.com/conan-io/docs/pull/3336>`__
- Feature: Provide new ``default_build_options`` attribute for defining options for ``tool_requires`` in recipes. `#14340 <https://github.com/conan-io/conan/pull/14340>`_ . Docs `here <https://github.com/conan-io/docs/pull/3338>`__
- Feature: Implement ``...@`` as a pattern for indicating matches with packages without user/channel. `#14338 <https://github.com/conan-io/conan/pull/14338>`_ . Docs `here <https://github.com/conan-io/docs/pull/3337>`__
- Feature: Add support to Makefile by the new MakeDeps generator `#14133 <https://github.com/conan-io/conan/pull/14133>`_ . Docs `here <https://github.com/conan-io/docs/pull/3348>`__
- Fix: Allow `--format=json` in :command:`conan create` for `python-requires` `#14594 <https://github.com/conan-io/conan/pull/14594>`_
- Fix: Remove conan v2 ready conan-center link. `#14593 <https://github.com/conan-io/conan/pull/14593>`_
- Fix: Make :command:`conan inspect` use all remotes by default. `#14572 <https://github.com/conan-io/conan/pull/14572>`_ . Docs `here <https://github.com/conan-io/docs/pull/3340>`__
- Fix: Allow extra hyphens in versions pre-releases. `#14561 <https://github.com/conan-io/conan/pull/14561>`_
- Fix: Allow confs for ``tools.cmake.cmaketoolchain`` to be used if defined even if ``tools.cmake.cmaketoolchain:user_toolchain`` is defined. `#14556 <https://github.com/conan-io/conan/pull/14556>`_ . Docs `here <https://github.com/conan-io/docs/pull/3333>`__
- Fix: Serialize booleans of ``dependencies`` in ``--format=json`` for graphs as booleans, not strings. `#14530 <https://github.com/conan-io/conan/pull/14530>`_ . Docs `here <https://github.com/conan-io/docs/pull/3334>`__
- Fix: Avoid errors in :command:`conan upload` when ``python_requires`` are not in the cache and need to be downloaded. `#14511 <https://github.com/conan-io/conan/pull/14511>`_
- Fix: Improve error check of ``lock add`` adding a full package reference instead of a recipe reference. `#14491 <https://github.com/conan-io/conan/pull/14491>`_
- Fix: Better error message when a built-in deployer failed to copy files. `#14461 <https://github.com/conan-io/conan/pull/14461>`_ . Docs `here <https://github.com/conan-io/docs/pull/3335>`__
- Fix: Do not print non-captured stacktraces to ``stdout`` but to ``stderr``. `#14444 <https://github.com/conan-io/conan/pull/14444>`_
- Fix: Serialize ``conf_info`` in ``--format=json`` output. `#14442 <https://github.com/conan-io/conan/pull/14442>`_
- Fix: `MSBuildToolchain`/`MSBuildDeps`: Avoid passing C/C++ compiler options as options for `ResourceCompile`. `#14378 <https://github.com/conan-io/conan/pull/14378>`_
- Fix: Removal of plugin files result in a better error message instead of stacktrace. `#14376 <https://github.com/conan-io/conan/pull/14376>`_
- Fix: Fix CMake system processor name on armv8/aarch64. `#14362 <https://github.com/conan-io/conan/pull/14362>`_
- Fix: Make backup sources ``core.sources`` conf not mandate the final slash. `#14342 <https://github.com/conan-io/conan/pull/14342>`_
- Fix: Correctly propagate options defined in recipe ``default_options`` to ``test_requires``. `#14340 <https://github.com/conan-io/conan/pull/14340>`_ . Docs `here <https://github.com/conan-io/docs/pull/3338>`__
- Fix: Invoke XCRun using conanfile.run() so that environment is injected. `#14326 <https://github.com/conan-io/conan/pull/14326>`_
- Fix: Use ``abspath`` for ``conan config install`` to avoid symlinks issues. `#14183 <https://github.com/conan-io/conan/pull/14183>`_
- Bugfix: Solve ``build_id()`` issues, when multiple different ``package_ids`` reusing same build-folder. `#14555 <https://github.com/conan-io/conan/pull/14555>`_
- Bugfix: Avoid DB errors when timestamp is not provided to :command:`conan download` when using package lists. `#14526 <https://github.com/conan-io/conan/pull/14526>`_
- Bugfix: Print exception stacktrace (when `-vtrace` is set) into stderr instead of stdout `#14522 <https://github.com/conan-io/conan/pull/14522>`_
- Bugfix: Print only packages confirmed interactively in :command:`conan upload`. `#14512 <https://github.com/conan-io/conan/pull/14512>`_
- Bugfix: 'conan remove' was outputting all entries in the cache matching the filter not just the once which where confirmed by the user. `#14478 <https://github.com/conan-io/conan/pull/14478>`_
- Bugfix: Better error when passing `--channel` without `--user`. `#14443 <https://github.com/conan-io/conan/pull/14443>`_
- Bugfix: Fix ``settings_target`` computation for ``tool_requires`` of packages already in the "build" context. `#14441 <https://github.com/conan-io/conan/pull/14441>`_
- Bugfix: Avoid ``DB is locked`` error when ``core.download:parallel`` is defined. `#14410 <https://github.com/conan-io/conan/pull/14410>`_
- Bugfix: Make generated powershell environment scripts relative when using deployers. `#14391 <https://github.com/conan-io/conan/pull/14391>`_
- Bugfix: fix profile [tool_requires] using revisions that were ignored. `#14337 <https://github.com/conan-io/conan/pull/14337>`_

2.0.9 (19-Jul-2023)
-------------------

- Feature: Add `implements` attribute in ConanFile to provide automatic management of some options and settings. `#14320 <https://github.com/conan-io/conan/pull/14320>`_ . Docs `here <https://github.com/conan-io/docs/pull/3303>`__
- Feature: Add `apple-clang` 15. `#14302 <https://github.com/conan-io/conan/pull/14302>`_
- Fix: Allow repository being dirty outside of `conanfile.py` folder when using `revision_mode = "scm_folder"`. `#14330 <https://github.com/conan-io/conan/pull/14330>`_
- Fix: Improve the error messages and provide Conan traces for errors in `compatibility.py` and `profile.py` plugins. `#14322 <https://github.com/conan-io/conan/pull/14322>`_
- Fix: ``flush()`` output streams after every message write. `#14310 <https://github.com/conan-io/conan/pull/14310>`_
- Bugfix: Fix Package signing plugin not verifying the downloaded sources. `#14331 <https://github.com/conan-io/conan/pull/14331>`_ . Docs `here <https://github.com/conan-io/docs/pull/3304>`__
- Bugfix: Fix ``CMakeUserPresets`` inherits from conan generated presets due to typo. `#14325 <https://github.com/conan-io/conan/pull/14325>`_
- Bugfix: ConanPresets.json contains duplicate presets if multiple user presets inherit from the same conan presets. `#14296 <https://github.com/conan-io/conan/pull/14296>`_
- Bugfix: Meson `prefix` param is passed as UNIX path. `#14295 <https://github.com/conan-io/conan/pull/14295>`_
- Bugfix: Fix `CMake Error: Invalid level specified for --loglevel` when `tools.build:verbosity` is set to `quiet`. `#14289 <https://github.com/conan-io/conan/pull/14289>`_

2.0.8 (13-Jul-2023)
-------------------

- Feature: Add GCC 10.5 to default settings.yml. `#14252 <https://github.com/conan-io/conan/pull/14252>`_
- Feature: Let `pkg_config_custom_content` overwrite default `*.pc` variables created by `PkgConfigDeps`. `#14233 <https://github.com/conan-io/conan/pull/14233>`_ . Docs `here <https://github.com/conan-io/docs/pull/3293>`__
- Feature: Let `pkg_config_custom_content` be a dict-like object too. `#14233 <https://github.com/conan-io/conan/pull/14233>`_ . Docs `here <https://github.com/conan-io/docs/pull/3293>`__
- Feature: The `fix_apple_shared_install_name` tool now uses `xcrun` to resolve the `otool` and `install_name_tool` programs. `#14195 <https://github.com/conan-io/conan/pull/14195>`_
- Feature: Manage shared, fPIC, and header_only options automatically. `#14194 <https://github.com/conan-io/conan/pull/14194>`_ . Docs `here <https://github.com/conan-io/docs/pull/3296>`__
- Feature: Manage package ID for header-library package type automatically. `#14194 <https://github.com/conan-io/conan/pull/14194>`_ . Docs `here <https://github.com/conan-io/docs/pull/3296>`__
- Feature: New ``cpp_info.set_property("cmake_package_version_compat" , "AnyNewerVersion")`` for ``CMakeDeps`` generator. `#14176 <https://github.com/conan-io/conan/pull/14176>`_ . Docs `here <https://github.com/conan-io/docs/pull/3292>`__
- Feature: Metadata improvements. `#14152 <https://github.com/conan-io/conan/pull/14152>`_
- Fix: Improve error message when missing binaries with :command:`conan test` command. `#14272 <https://github.com/conan-io/conan/pull/14272>`_
- Fix: Make :command:`conan download` command no longer need to load conanfile, won't fail for 1.X recipes or missing ``python_requires``. `#14261 <https://github.com/conan-io/conan/pull/14261>`_
- Fix: Using `upload` with the `--list` argument now permits empty recipe lists. `#14254 <https://github.com/conan-io/conan/pull/14254>`_
- Fix: Guarantee that ``Options.rm_safe`` never raises. `#14238 <https://github.com/conan-io/conan/pull/14238>`_
- Fix: Allow `tools.gnu:make_program` to affect every CMake configuration. `#14223 <https://github.com/conan-io/conan/pull/14223>`_
- Fix: Add missing `package_type` to :command:`conan new` lib templates. `#14215 <https://github.com/conan-io/conan/pull/14215>`_
- Fix: Add clarification for the default folder shown when querying a package reference. `#14199 <https://github.com/conan-io/conan/pull/14199>`_ . Docs `here <https://github.com/conan-io/docs/pull/3290>`__
- Fix: Enable existing status-message code in the `patch()` function. `#14177 <https://github.com/conan-io/conan/pull/14177>`_
- Fix: Use ``configuration`` in ``XcodeDeps`` instead of always ``build_type``. `#14168 <https://github.com/conan-io/conan/pull/14168>`_
- Fix: Respect symlinked path for cache location. `#14164 <https://github.com/conan-io/conan/pull/14164>`_
- Fix: ``PkgConfig`` uses ``conanfile.run()`` instead of internal runner to get full Conan environment from profiles and dependencies. `#13985 <https://github.com/conan-io/conan/pull/13985>`_
- Bugfix: Fix leaking of ``CMakeDeps`` ``CMAKE_FIND_LIBRARY_SUFFIXES`` variable. `#14253 <https://github.com/conan-io/conan/pull/14253>`_
- Bugfix: Fix conan not finding generator by name when multiple custom global generators are detected. `#14227 <https://github.com/conan-io/conan/pull/14227>`_
- Bugfix: Improve display of graph conflicts in `conan graph info` in html format. `#14190 <https://github.com/conan-io/conan/pull/14190>`_
- Bugfix: Fix ``CMakeToolchain`` cross-building from Linux to OSX. `#14187 <https://github.com/conan-io/conan/pull/14187>`_
- Bugfix: Fix KeyError in backup sources when no package is selected. `#14185 <https://github.com/conan-io/conan/pull/14185>`_

2.0.7 (21-Jun-2023)
-------------------

- Feature: Add new ``arm64ec`` architecture, used to define CMAKE_GENERATOR_PLATFORM. `#14114 <https://github.com/conan-io/conan/pull/14114>`_ . Docs `here <https://github.com/conan-io/docs/pull/3266>`__
- Feature: Make ``CppInfo`` a public, documented, importable tool for generators that need to aggregate them. `#14101 <https://github.com/conan-io/conan/pull/14101>`_ . Docs `here <https://github.com/conan-io/docs/pull/3268>`__
- Feature: Allow ``conan remove --list=pkglist`` to remove package-lists. `#14082 <https://github.com/conan-io/conan/pull/14082>`_ . Docs `here <https://github.com/conan-io/docs/pull/3270>`__
- Feature: Output for ``conan remove --format`` both text (summary of deleted things) and json. `#14082 <https://github.com/conan-io/conan/pull/14082>`_ . Docs `here <https://github.com/conan-io/docs/pull/3270>`__
- Feature: Add `core.sources:excluded_urls` to backup sources. `#14020 <https://github.com/conan-io/conan/pull/14020>`_
- Feature: :command:`conan test` command learned the ``--format=json`` formatter. `#14011 <https://github.com/conan-io/conan/pull/14011>`_ . Docs `here <https://github.com/conan-io/docs/pull/3273>`__
- Feature: Allow ``pkg/[version-range]`` expressions in ``conan list`` (and download, upload, remove) patterns. `#14004 <https://github.com/conan-io/conan/pull/14004>`_ . Docs `here <https://github.com/conan-io/docs/pull/3244>`__
- Feature: Add ``conan upload --dry-run`` equivalent to 1.X ``conan upload --skip-upload``. `#14002 <https://github.com/conan-io/conan/pull/14002>`_ . Docs `here <https://github.com/conan-io/docs/pull/3274>`__
- Feature: Add new command `conan version` to format the output. `#13999 <https://github.com/conan-io/conan/pull/13999>`_ . Docs `here <https://github.com/conan-io/docs/pull/3243>`__
- Feature: Small UX improvement to print some info while downloading large files. `#13989 <https://github.com/conan-io/conan/pull/13989>`_
- Feature: Use ``PackagesList`` as input argument for ``conan upload --list=pkglist.json``. `#13928 <https://github.com/conan-io/conan/pull/13928>`_ . Docs `here <https://github.com/conan-io/docs/pull/3257>`__
- Feature: Use ``--graph`` input for ``conan list`` to create a ``PackagesList`` that can be used as input for :command:`conan upload`. `#13928 <https://github.com/conan-io/conan/pull/13928>`_ . Docs `here <https://github.com/conan-io/docs/pull/3257>`__
- Feature: New metadata files associated to recipes and packages that can be uploaded, downloaded and added after the package exists. `#13918 <https://github.com/conan-io/conan/pull/13918>`_
- Feature: Allow to specify a custom deployer output folder. `#13757 <https://github.com/conan-io/conan/pull/13757>`_ . Docs `here <https://github.com/conan-io/docs/pull/3275>`__
- Feature: Split build & compilation verbosity control to two confs. `#13729 <https://github.com/conan-io/conan/pull/13729>`_ . Docs `here <https://github.com/conan-io/docs/pull/3277>`__
- Feature: Added `bindir` to generated `.pc` file in `PkgConfigDeps`. `#13623 <https://github.com/conan-io/conan/pull/13623>`_ . Docs `here <https://github.com/conan-io/docs/pull/3269>`__
- Fix: Deprecate ``AutoPackage`` remnant from Conan 1.X. `#14083 <https://github.com/conan-io/conan/pull/14083>`_ . Docs `here <https://github.com/conan-io/docs/pull/3253>`__
- Fix: Fix description for the conf entry for default build profile used. `#14075 <https://github.com/conan-io/conan/pull/14075>`_ . Docs `here <https://github.com/conan-io/docs/pull/3252>`__
- Fix: Allow spaces in path in ``Git`` helper. `#14063 <https://github.com/conan-io/conan/pull/14063>`_ . Docs `here <https://github.com/conan-io/docs/pull/3271>`__
- Fix: Remove trailing ``.`` in ``conanfile.xxx_folder`` that is breaking subsystems like msys2. `#14061 <https://github.com/conan-io/conan/pull/14061>`_
- Fix: Avoid caching issues when some intermediate package in the graph calls ``aggregated_components()`` over some dependency and using ``--deployer``, generators still pointed to the Conan cache and not deployed copy. `#14060 <https://github.com/conan-io/conan/pull/14060>`_
- Fix: Allow internal ``Cli`` object to be called more than once. `#14053 <https://github.com/conan-io/conan/pull/14053>`_
- Fix: Force ``pyyaml>=6`` for Python 3.10, as previous versions broke. `#13990 <https://github.com/conan-io/conan/pull/13990>`_
- Fix: Improve graph conflict message when Conan can't show one of the conflicting recipes. `#13946 <https://github.com/conan-io/conan/pull/13946>`_
- Bugfix: Solve bug in timestamp of non-latest revision download from the server. `#14110 <https://github.com/conan-io/conan/pull/14110>`_
- Bugfix: Fix double base path setup in editable packages. `#14109 <https://github.com/conan-io/conan/pull/14109>`_
- Bugfix: Raise if ``conan graph build-order`` graph has any errors, instead of quietly doing nothing and outputting and empty json. `#14106 <https://github.com/conan-io/conan/pull/14106>`_
- Bugfix: Avoid incorrect path replacements for ``editable`` packages when folders have overlapping matching names. `#14095 <https://github.com/conan-io/conan/pull/14095>`_
- Bugfix: Set clang as the default FreeBSD detected compiler. `#14065 <https://github.com/conan-io/conan/pull/14065>`_
- Bugfix: Add prefix var and any custom content (through the `pkg_config_custom_content` property) to already generated pkg-config root .pc files by `PkgConfigDeps`. `#14051 <https://github.com/conan-io/conan/pull/14051>`_
- Bugfix: :command:`conan create` command returns always the same output for ``--format=json`` result graph, irrespective of test_package existence. `#14011 <https://github.com/conan-io/conan/pull/14011>`_ . Docs `here <https://github.com/conan-io/docs/pull/3273>`__
- Bugfix: Fix problem with ``editable`` packages when defining ``self.folders.root=".."`` parent directory. `#13983 <https://github.com/conan-io/conan/pull/13983>`_
- Bugfix: Removed `libdir1` and `includedir1` as the default index. Now, `PkgConfigDeps` creates the `libdir` and `includedir` variables by default in `.pc` files. `#13623 <https://github.com/conan-io/conan/pull/13623>`_ . Docs `here <https://github.com/conan-io/docs/pull/3269>`__

2.0.6 (26-May-2023)
-------------------

- Feature: Add a `tools.cmake:cmake_program` configuration item to allow specifying the location of the desired CMake executable. `#13940 <https://github.com/conan-io/conan/pull/13940>`_ . Docs `here <https://github.com/conan-io/docs/pull/3232>`__
- Fix: Output "id" property in graph json output as str instead of int. `#13964 <https://github.com/conan-io/conan/pull/13964>`_ . Docs `here <https://github.com/conan-io/docs/pull/3236>`__
- Fix: Fix custom commands in a layer not able to do a local import. `#13944 <https://github.com/conan-io/conan/pull/13944>`_
- Fix: Improve the output of download + unzip. `#13937 <https://github.com/conan-io/conan/pull/13937>`_
- Fix: Add missing values to `package_manager:mode` in `conan config install`. `#13929 <https://github.com/conan-io/conan/pull/13929>`_
- Bugfix: Ensuring the same graph-info JSON output for  `graph info`, `create`, `export-pkg`, and `install`. `#13967 <https://github.com/conan-io/conan/pull/13967>`_ . Docs `here <https://github.com/conan-io/docs/pull/3236>`__
- Bugfix: ``test_requires`` were affecting the ``package_id`` of consumers as regular ``requires``, but they shouldn't. `#13966 <https://github.com/conan-io/conan/pull/13966>`_
- Bugfix: Define ``source_folder`` correctly in the json output when ``-c tools.build:download_source=True``. `#13953 <https://github.com/conan-io/conan/pull/13953>`_
- Bugfix: Fixed and completed the `graph info xxxx --format json` output, to publicly document it. `#13934 <https://github.com/conan-io/conan/pull/13934>`_ . Docs `here <https://github.com/conan-io/docs/pull/3236>`__
- Bugfix: Fix "double" absolute paths in premakedeps. `#13926 <https://github.com/conan-io/conan/pull/13926>`_
- Bugfix: Fix regression from 2.0.5 https://github.com/conan-io/conan/pull/13898, in which overrides of packages and components specification was failing `#13923 <https://github.com/conan-io/conan/pull/13923>`_

2.0.5 (18-May-2023)
-------------------

- Feature: `-v` argument defaults to the `VERBOSE` level. `#13839 <https://github.com/conan-io/conan/pull/13839>`_
- Feature: Avoid showing unnecessary skipped dependencies. Now, it only shows a list of reference names if exists skipped binaries. They can be completely listed by adding `-v` (verbose mode) to the current command. `#13836 <https://github.com/conan-io/conan/pull/13836>`_
- Feature: Allow step-into dependencies debugging for packages built locally with ``--build`` `#13833 <https://github.com/conan-io/conan/pull/13833>`_ . Docs `here <https://github.com/conan-io/docs/pull/3210>`__
- Feature: Allow non relocatable, locally built packages with ``upload_policy="skip"`` and ``build_policy="missing"`` `#13833 <https://github.com/conan-io/conan/pull/13833>`_ . Docs `here <https://github.com/conan-io/docs/pull/3210>`__
- Feature: Do not move "build" folders in cache when ``package-revision`` is computed to allow locating sources for dependencies debuggability with step-into `#13810 <https://github.com/conan-io/conan/pull/13810>`_
- Feature: New ``settings.possible_values()`` method to query the range of possible values for a setting. `#13796 <https://github.com/conan-io/conan/pull/13796>`_ . Docs `here <https://github.com/conan-io/docs/pull/3212>`__
- Feature: Optimize and avoid hitting servers for binaries when ``upload_policy=skip`` `#13771 <https://github.com/conan-io/conan/pull/13771>`_
- Feature: Partially relativize generated environment .sh shell scripts `#13764 <https://github.com/conan-io/conan/pull/13764>`_
- Feature: Improve settings.yml error messages `#13748 <https://github.com/conan-io/conan/pull/13748>`_
- Feature: Auto create empty ``global.conf`` to improve UX looking for file in home. `#13746 <https://github.com/conan-io/conan/pull/13746>`_ . Docs `here <https://github.com/conan-io/docs/pull/3211>`__
- Feature: Render the profile file name as profile_name `#13721 <https://github.com/conan-io/conan/pull/13721>`_ . Docs `here <https://github.com/conan-io/docs/pull/3180>`__
- Feature: New global custom generators in cache "extensions/generators" that can be used by name. `#13718 <https://github.com/conan-io/conan/pull/13718>`_ . Docs `here <https://github.com/conan-io/docs/pull/3213>`__
- Feature: Improve :command:`conan inspect` output, it now understands `set_name`/`set_version`. `#13716 <https://github.com/conan-io/conan/pull/13716>`_ . Docs `here <https://github.com/conan-io/docs/pull/3204>`__
- Feature: Define new ``self.tool_requires("pkg/<host_version>")`` to allow some tool-requires to follow and use the same version as the "host" regular requires do. `#13712 <https://github.com/conan-io/conan/pull/13712>`_ . Docs `here <https://github.com/conan-io/docs/pull/3223>`__
- Feature: Introduce new ``core:skip_warns`` configuration to be able to silence some warnings in the output. `#13706 <https://github.com/conan-io/conan/pull/13706>`_ . Docs `here <https://github.com/conan-io/docs/pull/3215>`__
- Feature: Add info_invalid to graph node serialization `#13688 <https://github.com/conan-io/conan/pull/13688>`_
- Feature: Computing and reporting the ``overrides`` in the graph, and in the ``graph build-order`` `#13680 <https://github.com/conan-io/conan/pull/13680>`_
- Feature: New ``revision_mode = "scm_folder"`` for mono-repo projects that want to use ``scm`` revisions. `#13562 <https://github.com/conan-io/conan/pull/13562>`_ . Docs `here <https://github.com/conan-io/docs/pull/3218>`__
- Feature: Demonstrate that it is possible to ``tool_requires`` different versions of the same package. `#13529 <https://github.com/conan-io/conan/pull/13529>`_ . Docs `here <https://github.com/conan-io/docs/pull/3219>`__
- Fix: `build_scripts` now set the `run` trait to `True` by default `#13901 <https://github.com/conan-io/conan/pull/13901>`_ . Docs `here <https://github.com/conan-io/docs/pull/3206>`__
- Fix: Fix XcodeDeps includes skipped dependencies. `#13880 <https://github.com/conan-io/conan/pull/13880>`_
- Fix: Do not allow line feeds into ``pkg/version`` reference fields `#13870 <https://github.com/conan-io/conan/pull/13870>`_
- Fix: Fix ``AutotoolsToolchain`` definition of  ``tools.build:compiler_executable`` for Windows subsystems `#13867 <https://github.com/conan-io/conan/pull/13867>`_
- Fix: Speed up the CMakeDeps generation `#13857 <https://github.com/conan-io/conan/pull/13857>`_
- Fix: Fix imported library config suffix. `#13841 <https://github.com/conan-io/conan/pull/13841>`_
- Fix: Fail when defining an unkown conf `#13832 <https://github.com/conan-io/conan/pull/13832>`_
- Fix: Fix incorrect printing of "skipped" binaries in the ``conan install/create`` commands, when they are used by some other dependencies. `#13778 <https://github.com/conan-io/conan/pull/13778>`_
- Fix: Renaming the cache "deploy" folder to "deployers" and allow ``-d, --deployer`` cli arg. ("deploy" folder will not break but will warn as deprecated). `#13740 <https://github.com/conan-io/conan/pull/13740>`_ . Docs `here <https://github.com/conan-io/docs/pull/3209>`__
- Fix: Omit ``-L`` libpaths in ``CMakeDeps`` for header-only libraries. `#13704 <https://github.com/conan-io/conan/pull/13704>`_
- Bugfix: Fix when a ``test_requires`` is also a regular transitive "host" requires and consumer defines components. `#13898 <https://github.com/conan-io/conan/pull/13898>`_
- Bugfix: Fix propagation of options like ``*:shared=True`` defined in recipes `#13855 <https://github.com/conan-io/conan/pull/13855>`_
- Bugfix: Fix ``--lockfile-out`` paths for 'graph build-order' and 'test' commands `#13853 <https://github.com/conan-io/conan/pull/13853>`_
- Bugfix: Ensure backup sources are uploaded in more cases `#13846 <https://github.com/conan-io/conan/pull/13846>`_
- Bugfix: fix ``settings.yml`` definition of ``intel-cc`` ``cppstd=03`` `#13844 <https://github.com/conan-io/conan/pull/13844>`_
- Bugfix: Fix :command:`conan upload` with backup sources for exported-only recipes `#13779 <https://github.com/conan-io/conan/pull/13779>`_
- Bugfix: Fix ``conan lock merge`` of lockfiles containing alias `#13763 <https://github.com/conan-io/conan/pull/13763>`_
- Bugfix: Fix python_requires in transitive deps with version ranges `#13762 <https://github.com/conan-io/conan/pull/13762>`_
- Bugfix: fix CMakeToolchain CMAKE_SYSTEM_NAME=Generic for baremetal `#13739 <https://github.com/conan-io/conan/pull/13739>`_
- Bugfix: Fix incorrect environment scripts deactivation order `#13707 <https://github.com/conan-io/conan/pull/13707>`_
- Bugfix: Solve failing lockfiles when graph has requirements with ``override=True`` `#13597 <https://github.com/conan-io/conan/pull/13597>`_

2.0.4 (11-Apr-2023)
-------------------

- Feature: extend ``--build-require`` to more commands (``graph info``, ``lock create``, ``install``) and cases. `#13669 <https://github.com/conan-io/conan/pull/13669>`_ . Docs `here <https://github.com/conan-io/docs/pull/3166>`__
- Feature: Add `-d tool_requires` to :command:`conan new`. `#13608 <https://github.com/conan-io/conan/pull/13608>`_ . Docs `here <https://github.com/conan-io/docs/pull/3156>`__
- Feature: Make CMakeDeps, CMakeToolchain and Environment (.bat, Windows only) generated files have relative paths. `#13607 <https://github.com/conan-io/conan/pull/13607>`_
- Feature: Adding preliminary (non documented, dev-only) support for premake5 deps (PremakeDeps). `#13390 <https://github.com/conan-io/conan/pull/13390>`_
- Fix: Update old :command:`conan user` references to ``conan remote login``. `#13671 <https://github.com/conan-io/conan/pull/13671>`_
- Fix: Improve dependencies options changed in ``requirements()`` error msg. `#13668 <https://github.com/conan-io/conan/pull/13668>`_
- Fix: [system_tools] was not reporting the correct resolved version, but still the original range. `#13667 <https://github.com/conan-io/conan/pull/13667>`_
- Fix: Improve `provides` conflict message error. `#13661 <https://github.com/conan-io/conan/pull/13661>`_
- Fix: When server responds Forbidden to the download of 1 file in a recipe/package, make sure other files and DB are cleaned. `#13626 <https://github.com/conan-io/conan/pull/13626>`_
- Fix: Add error in :command:`conan remove` when using `--package-query` without providing a pattern that matches packages. `#13622 <https://github.com/conan-io/conan/pull/13622>`_
- Fix: Add ``direct_deploy`` subfolder for the ``direct_deploy`` deployer. `#13612 <https://github.com/conan-io/conan/pull/13612>`_ . Docs `here <https://github.com/conan-io/docs/pull/3155>`__
- Fix: Fix html output when pattern does not list package revisions, like: ``conan list "*#*:*"``. `#13605 <https://github.com/conan-io/conan/pull/13605>`_
- Bugfix: ``conan list -p <package-query>`` failed when a package had no settings or options. `#13662 <https://github.com/conan-io/conan/pull/13662>`_
- Bugfix: `python_requires` now properly loads remote requirements. `#13657 <https://github.com/conan-io/conan/pull/13657>`_
- Bugfix: Fix crash when ``override`` is used in a node of the graph that is also the closing node of a diamond. `#13631 <https://github.com/conan-io/conan/pull/13631>`_
- Bugfix: Fix the ``--package-query`` argument for ``options``. `#13618 <https://github.com/conan-io/conan/pull/13618>`_
- Bugfix: Add ``full_deploy`` subfolder for the ``full_deploy`` deployer to avoid collision with "build" folder. `#13612 <https://github.com/conan-io/conan/pull/13612>`_ . Docs `here <https://github.com/conan-io/docs/pull/3155>`__
- Bugfix: Make `STATUS` the default log level. `#13610 <https://github.com/conan-io/conan/pull/13610>`_
- Bugfix: Fix double delete error in `conan cache clean`. `#13601 <https://github.com/conan-io/conan/pull/13601>`_

2.0.3 (03-Apr-2023)
-------------------

- Feature: ``conan cache clean`` learned the ``--all`` and ``--temp`` to clean everything (sources, builds) and also the temporary folders. `#13581 <https://github.com/conan-io/conan/pull/13581>`_ . Docs `here <https://github.com/conan-io/docs/pull/3145>`__
- Feature: Introduce the ``conf`` dictionary update semantics with ``*=`` operator. `#13571 <https://github.com/conan-io/conan/pull/13571>`_ . Docs `here <https://github.com/conan-io/docs/pull/3141>`__
- Feature: Support MacOS SDK 13.1 (available in Xcode 14.2). `#13531 <https://github.com/conan-io/conan/pull/13531>`_
- Feature: The ``full_deploy`` deployer together with ``CMakeDeps`` generator learned to create relative paths deploys, so they are relocatable. `#13526 <https://github.com/conan-io/conan/pull/13526>`_
- Feature: Introduce the ``conan remove *#!latest`` (also for package-revisions), to remove all revisions except the latest one. `#13505 <https://github.com/conan-io/conan/pull/13505>`_ . Docs `here <https://github.com/conan-io/docs/pull/3144>`__
- Feature: New ``conan cache check-integrity`` command to replace 1.X legacy ``conan upload --skip-upload --check``. `#13502 <https://github.com/conan-io/conan/pull/13502>`_ . Docs `here <https://github.com/conan-io/docs/pull/3147>`__
- Feature: Add filtering for options and settings in conan list html output. `#13470 <https://github.com/conan-io/conan/pull/13470>`_
- Feature: Automatic server side source backups for third parties. `#13461 <https://github.com/conan-io/conan/pull/13461>`_
- Feature: Add `tools.android:cmake_legacy_toolchain` configuration useful when building CMake projects for Android. If defined, this will set the value of `ANDROID_USE_LEGACY_TOOLCHAIN_FILE`. It may be useful to set this to `False` if compiler flags are defined via `tools.build:cflags` or `tools.build:cxxflags` to prevent Android's legacy CMake toolchain from overriding the values. `#13459 <https://github.com/conan-io/conan/pull/13459>`_ . Docs `here <https://github.com/conan-io/docs/pull/3146>`__
- Feature: Default ``tools.files.download:download_cache`` to ``core.download:download_cache``, so it is only necessary to define one. `#13458 <https://github.com/conan-io/conan/pull/13458>`_
- Feature: Authentication for ``tools.files.download()``. `#13421 <https://github.com/conan-io/conan/pull/13421>`_ . Docs `here <https://github.com/conan-io/docs/pull/3149>`__
- Fix: Define a way to update ``default_options`` in ``python_requires_extend`` extension. `#13487 <https://github.com/conan-io/conan/pull/13487>`_ . Docs `here <https://github.com/conan-io/docs/pull/3120>`__
- Fix: Allow again to specify ``self.options["mydep"].someoption=value``, equivalent to ``"mydep/*"``. `#13467 <https://github.com/conan-io/conan/pull/13467>`_
- Fix: Generate `cpp_std=vc++20` for c++20 with meson with VS2019 and VS2022, rather than `vc++latest`. `#13450 <https://github.com/conan-io/conan/pull/13450>`_
- Bugfix: Fixed ``CMakeDeps`` not clearing ``CONAN_SHARED_FOUND_LIBRARY`` var in ``find_library()``. `#13596 <https://github.com/conan-io/conan/pull/13596>`_
- Bugfix: Do not allow adding more than 1 remote with the same remote name. `#13574 <https://github.com/conan-io/conan/pull/13574>`_
- Bugfix: ``cmd_wrapper`` added missing parameter ``conanfile``. `#13564 <https://github.com/conan-io/conan/pull/13564>`_ . Docs `here <https://github.com/conan-io/docs/pull/3137>`__
- Bugfix: Avoid generators errors because dependencies binaries of editable packages were "skip". `#13544 <https://github.com/conan-io/conan/pull/13544>`_
- Bugfix: Fix subcommands names when the parent command has underscores. `#13516 <https://github.com/conan-io/conan/pull/13516>`_
- Bugfix: Fix ``python-requires`` in remotes when running :command:`conan export-pkg`. `#13496 <https://github.com/conan-io/conan/pull/13496>`_
- Bugfix: Editable packages now also follow ``build_folder_vars`` configuration. `#13488 <https://github.com/conan-io/conan/pull/13488>`_
- Bugfix: Fix ``[system_tools]`` profile composition. `#13468 <https://github.com/conan-io/conan/pull/13468>`_

2.0.2 (15-Mar-2023)
-------------------

- Feature: Allow relative paths to the Conan home folder in the ``global.conf``. `#13415 <https://github.com/conan-io/conan/pull/13415>`_ . Docs `here <https://github.com/conan-io/docs/pull/3087>`__
- Feature: Some improvements for html formatter in :command:`conan list` command. `#13409 <https://github.com/conan-io/conan/pull/13409>`_ . Docs `here <https://github.com/conan-io/docs/pull/3093>`__
- Feature: Adds an optional "build_script_folder" argument to the `autoreconf` method of the `Autotools` class. It mirrors the same argument and behavior of the `configure` method of the same class. That is, it allows one to override where the tool is run (by default it runs in the `source_folder`. `#13403 <https://github.com/conan-io/conan/pull/13403>`_
- Feature: Create summary of cached content. `#13386 <https://github.com/conan-io/conan/pull/13386>`_
- Feature: Add `conan config show <conf>` command. `#13354 <https://github.com/conan-io/conan/pull/13354>`_ . Docs `here <https://github.com/conan-io/docs/pull/3091>`__
- Feature: Allow ``global.conf`` jinja2 inclusion of other files. `#13336 <https://github.com/conan-io/conan/pull/13336>`_
- Feature: Add ``conan export-pkg --skip-binaries`` to allow exporting without binaries of dependencies. `#13324 <https://github.com/conan-io/conan/pull/13324>`_ . Docs `here <https://github.com/conan-io/docs/pull/3106>`__
- Feature: Add `core.version_ranges:resolve_prereleases` conf to control whether version ranges can resolve to prerelease versions `#13321 <https://github.com/conan-io/conan/pull/13321>`_
- Fix: Allow automatic processing of ``package_type = "build-scripts"`` in :command:`conan create` as ``--build-require``. `#13433 <https://github.com/conan-io/conan/pull/13433>`_
- Fix: Improve the detection and messages of server side package corruption. `#13432 <https://github.com/conan-io/conan/pull/13432>`_
- Fix: Fix conan download help typo. `#13430 <https://github.com/conan-io/conan/pull/13430>`_
- Fix: Remove profile arguments from `conan profile path`. `#13423 <https://github.com/conan-io/conan/pull/13423>`_ . Docs `here <https://github.com/conan-io/docs/pull/3090>`__
- Fix: Fix typo in _detect_compiler_version. `#13396 <https://github.com/conan-io/conan/pull/13396>`_
- Fix: Fix ``conan profile detect`` detection of ``libc++`` for ``clang`` compiler on OSX. `#13359 <https://github.com/conan-io/conan/pull/13359>`_
- Fix: Allow internal ``vswhere`` calls to detect and use VS pre-releases too. `#13355 <https://github.com/conan-io/conan/pull/13355>`_
- Fix: Allow :command:`conan export-pkg` to use remotes to install missing dependencies not in the cache. `#13324 <https://github.com/conan-io/conan/pull/13324>`_ . Docs `here <https://github.com/conan-io/docs/pull/3106>`__
- Fix: Allow conversion to ``dict`` of ``settings.yml`` lists when ``settings_user.yml`` define a ``dict``. `#13323 <https://github.com/conan-io/conan/pull/13323>`_
- Fix: Fix flags passed by AutotoolsToolchain when cross compiling from macOS to a non-Apple OS. `#13230 <https://github.com/conan-io/conan/pull/13230>`_
- BugFix: Fix issues in ``MSBuild`` with custom configurations when custom configurations has spaces. `#13435 <https://github.com/conan-io/conan/pull/13435>`_
- Bugfix: Solve bug in ``conan profile path <nonexisting>`` that was crashing. `#13434 <https://github.com/conan-io/conan/pull/13434>`_
- Bugfix: Add global verbosity conf `tools.build:verbosity` instead of individual ones. `#13428 <https://github.com/conan-io/conan/pull/13428>`_ . Docs `here <https://github.com/conan-io/docs/pull/3107>`__
- Bugfix: Avoid raising fatal exceptions for malformed custom commands. `#13365 <https://github.com/conan-io/conan/pull/13365>`_
- Bugfix: Do not omit ``system_libs`` from dependencies even if they are header-only. `#13364 <https://github.com/conan-io/conan/pull/13364>`_
- Bugfix: Fix ``VirtualBuildEnv`` environment not being created when ``MesonToolchain`` is instantiated. `#13346 <https://github.com/conan-io/conan/pull/13346>`_
- Bugfix: Nicer error in the compatibility plugin with custom compilers. `#13328 <https://github.com/conan-io/conan/pull/13328>`_
- Bugfix: adds qcc cppstd compatibility info to allow dep graph to be calculated. `#13326 <https://github.com/conan-io/conan/pull/13326>`_

2.0.1 (03-Mar-2023)
-------------------

- Feature: Add `--insecure` alias to `--verify-ssl` in config install. `#13270 <https://github.com/conan-io/conan/pull/13270>`_ . Docs `here <https://github.com/conan-io/docs/pull/3035>`__
- Feature: Add `.conanignore` support to `conan config install`. `#13269 <https://github.com/conan-io/conan/pull/13269>`_ . Docs `here <https://github.com/conan-io/docs/pull/3036>`__
- Feature: Make verbose tracebacks on exception be shown for ``-vv`` and ``-vvv``, instead of custom env-var used in 1.X. `#13226 <https://github.com/conan-io/conan/pull/13226>`_
- Fix: Minor improvements to :command:`conan install` and 2.0-readiness error messages. `#13299 <https://github.com/conan-io/conan/pull/13299>`_
- Fix: Remove ``vcvars.bat`` VS telemetry env-var, to avoid Conan hanging. `#13293 <https://github.com/conan-io/conan/pull/13293>`_
- Fix: Remove legacy ``CMakeToolchain`` support for ``CMakePresets`` schema2 for ``CMakeUserPresets.json``. `#13288 <https://github.com/conan-io/conan/pull/13288>`_ . Docs `here <https://github.com/conan-io/docs/pull/3049>`__
- Fix: Remove ``--logger`` json logging and legacy traces. `#13287 <https://github.com/conan-io/conan/pull/13287>`_ . Docs `here <https://github.com/conan-io/docs/pull/3050>`__
- Fix: Fix typo in `conan remote auth` help. `#13285 <https://github.com/conan-io/conan/pull/13285>`_ . Docs `here <https://github.com/conan-io/docs/pull/3039>`__
- Fix: Raise arg error if ``conan config list unexpected-arg``. `#13282 <https://github.com/conan-io/conan/pull/13282>`_
- Fix: Do not auto-detect ``compiler.runtime_type`` for ``msvc``, rely on profile plugin. `#13277 <https://github.com/conan-io/conan/pull/13277>`_
- Fix: Fix conanfile.txt options parsing error message. `#13266 <https://github.com/conan-io/conan/pull/13266>`_
- Fix: Improve error message for unified patterns in options. `#13264 <https://github.com/conan-io/conan/pull/13264>`_
- Fix: Allow ``conan remote add --force`` to force re-definition of an existing remote name. `#13249 <https://github.com/conan-io/conan/pull/13249>`_
- Fix: Restore printing of profiles for build command. `#13214 <https://github.com/conan-io/conan/pull/13214>`_
- Fix: Change :command:`conan build` argument description for "path" to indicate it is only for conanfile.py and explicitly state that it does not work with conanfile.txt. `#13211 <https://github.com/conan-io/conan/pull/13211>`_ . Docs `here <https://github.com/conan-io/docs/pull/3046>`__
- Fix: Better error message when dependencies ``options`` are defined in ``requirements()`` method. `#13207 <https://github.com/conan-io/conan/pull/13207>`_
- Fix: Fix broken links to docs from error messages and readme. `#13186 <https://github.com/conan-io/conan/pull/13186>`_
- Bugfix: Ensure that `topics` are always serialized as lists. `#13298 <https://github.com/conan-io/conan/pull/13298>`_
- Bugfix: Ensure that `provides` are always serialized as lists. `#13298 <https://github.com/conan-io/conan/pull/13298>`_
- Bugfix: Fixed the detection of certain visual c++ installations. `#13284 <https://github.com/conan-io/conan/pull/13284>`_
- Bugfix: Fix supported ``cppstd`` values for ``msvc`` compiler. `#13278 <https://github.com/conan-io/conan/pull/13278>`_
- Bugfix: CMakeDeps generate files for ``tool_requires`` with the same ``build_type`` as the "host" context. `#13267 <https://github.com/conan-io/conan/pull/13267>`_
- Bugfix: Fix definition of patterns for dependencies options in configure(). `#13263 <https://github.com/conan-io/conan/pull/13263>`_
- Bugfix: Fix CMakeToolchain error when output folder in different Win drive. `#13248 <https://github.com/conan-io/conan/pull/13248>`_
- Bugfix: Do not raise errors if a ``test_requires`` is not used by components ``.requires``. `#13191 <https://github.com/conan-io/conan/pull/13191>`_

2.0.0 (22-Feb-2023)
-------------------

- Feature: Change default profile cppstd for apple-clang to gnu17. `#13185 <https://github.com/conan-io/conan/pull/13185>`_ 
- Feature: New ``conan remote auth`` command to force authentication in the remotes `#13180 <https://github.com/conan-io/conan/pull/13180>`_ 
- Fix: Allow defining options trait in ``test_requires(..., options={})`` `#13178 <https://github.com/conan-io/conan/pull/13178>`_ 
- Fix: Unifying Conan commands help messages. `#13176 <https://github.com/conan-io/conan/pull/13176>`_ 
- Bugfix: Fix MesonToolchain wrong cppstd in apple-clang `#13172 <https://github.com/conan-io/conan/pull/13172>`_ 
- Feature: Improved global Conan output messages (create, install, export, etc.) `#12746 <https://github.com/conan-io/conan/pull/12746>`_ 

2.0.0-beta10 (16-Feb-2023)
--------------------------

- Feature: Add basic html output to `conan list` command. `#13135 <https://github.com/conan-io/conan/pull/13135>`_
- Feature: Allow ``test_package`` to process ``--build`` arguments (computing --build=never for the main, non test_package graph). `#13117 <https://github.com/conan-io/conan/pull/13117>`_
- Feature: Add `--force` argument to remote add. `#13112 <https://github.com/conan-io/conan/pull/13112>`_
- Feature: Validate if the input configurations exist, to avoid typos. `#13110 <https://github.com/conan-io/conan/pull/13110>`_
- Feature: Allow defining ``self.folders.build_folder_vars`` in recipes ``layout()``. `#13109 <https://github.com/conan-io/conan/pull/13109>`_
- Feature: Block settings assignment. `#13099 <https://github.com/conan-io/conan/pull/13099>`_
- Feature: Improve `conan editable` ui. `#13093 <https://github.com/conan-io/conan/pull/13093>`_
- Feature: Provide the ability for users to extend Conan generated CMakePresets. `#13090 <https://github.com/conan-io/conan/pull/13090>`_
- Feature: Add error messages to help with the migration of recipes to 2.0, both from ConanCenter and from user repos. `#13074 <https://github.com/conan-io/conan/pull/13074>`_
- Feature: Remove option.fPIC for shared in :command:`conan new` templates. `#13066 <https://github.com/conan-io/conan/pull/13066>`_
- Feature: Add `conan cache clean` subcommand to clean build and source folders. `#13050 <https://github.com/conan-io/conan/pull/13050>`_
- Feature: Implement customizable ``CMakeToolchain.presets_prefix`` so presets name prepend this. `#13015 <https://github.com/conan-io/conan/pull/13015>`_
- Feature: Add `[system_tools]` section to profiles to use your own installed tools instead of the packages declared in the requires. `#10166 <https://github.com/conan-io/conan/pull/10166>`_
- Fix: Fixes in powershell escaping. `#13084 <https://github.com/conan-io/conan/pull/13084>`_
- Fix: Define ``CMakeToolchain.presets_prefix="conan"`` by default, to avoid conflict with other users presets. `#13015 <https://github.com/conan-io/conan/pull/13015>`_

2.0.0-beta9 (31-Jan-2023)
-------------------------

- Feature: Add package names in Conan cache hash paths. `#13011 <https://github.com/conan-io/conan/pull/13011>`_
- Feature: Implement ``tools.build:download_source`` conf to force the installation of sources in :command:`conan install` or ``conan graph info``. `#13003 <https://github.com/conan-io/conan/pull/13003>`_
- Feature: Users can define their own settings in `settings_user.yml` that will be merged with the Conan `settings.yml`. `#12980 <https://github.com/conan-io/conan/pull/12980>`_
- Feature: List disabled remotes too. `#12937 <https://github.com/conan-io/conan/pull/12937>`_
- Fix: PkgConfiDeps is using the wrong ``dependencies.host`` from dependencies instead of ``get_transitive_requires()`` computation. `#13013 <https://github.com/conan-io/conan/pull/13013>`_
- Fix: Fixing transitive shared linux libraries in CMakeDeps. `#13010 <https://github.com/conan-io/conan/pull/13010>`_
- Fix: Fixing issues with test_package output folder. `#12992 <https://github.com/conan-io/conan/pull/12992>`_
- Fix: Improve error messages for wrong methods. `#12962 <https://github.com/conan-io/conan/pull/12962>`_
- Fix: Fix fail in parallel packages download due to database concurrency issues. `#12930 <https://github.com/conan-io/conan/pull/12930>`_
- Fix: Enable authentication against disabled remotes. `#12913 <https://github.com/conan-io/conan/pull/12913>`_
- Fix: Improving system_requirements. `#12912 <https://github.com/conan-io/conan/pull/12912>`_
- Fix: Change tar format to PAX, which is the Python3.8 default. `#12899 <https://github.com/conan-io/conan/pull/12899>`_

2.0.0-beta8 (12-Jan-2023)
-------------------------

- Feature: Add `unix_path_package_info_legacy` function for those cases in which it is used in `package_info` in recipes that require compatibility with Conan 1.x. In Conan 2, path conversions should not be performed in the `package_info` method. `#12886 <https://github.com/conan-io/conan/pull/12886>`_
- Feature: New serialization json and printing for ``conan list``. `#12883 <https://github.com/conan-io/conan/pull/12883>`_
- Feature: Add requirements to `conan new cmake_{lib,exe}` `#12875 <https://github.com/conan-io/conan/pull/12875>`_
- Feature: Allow ``--no-remotes`` to force temporal disabling of remotes `#12808 <https://github.com/conan-io/conan/pull/12808>`_
- Feature: Add barebones template option to conan new. `#12802 <https://github.com/conan-io/conan/pull/12802>`_
- Feature: Avoid requesting package configuration if PkgID is passed. `#12801 <https://github.com/conan-io/conan/pull/12801>`_
- Feature: Implemented `conan list *#latest` and `conan list *:*#latest`. Basically, this command can show the latest RREVs and PREVs for all the matching references. `#12781 <https://github.com/conan-io/conan/pull/12781>`_
- Feature: Allow chaining of `self.output` write methods `#12780 <https://github.com/conan-io/conan/pull/12780>`_
- Fix: Make ``graph info`` filters to work on json output too `#12836 <https://github.com/conan-io/conan/pull/12836>`_
- Bugfix: Fix bug to pass a valid GNU triplet when using AutotoolsToolchain and cross-building on Windows. `#12881 <https://github.com/conan-io/conan/pull/12881>`_
- Bugfix: Ordering if same ref.name but different versions. `#12801 <https://github.com/conan-io/conan/pull/12801>`_

2.0.0-beta7 (22-Dec-2022)
-------------------------

- Feature: Raise an error when a generator is both defined in generators attribute and instantiated in generate() method `#12722 <https://github.com/conan-io/conan/pull/12722>`_
- Feature: `test_requires` improvements, including allowing it in conanfile.txt `#12699 <https://github.com/conan-io/conan/pull/12699>`_
- Feature: Improve errors for when required_conan_version has spaces between the operator and the version `#12695 <https://github.com/conan-io/conan/pull/12695>`_
- Feature: ConanAPI cleanup and organization `#12666 <https://github.com/conan-io/conan/pull/12666>`_

2.0.0-beta6 (02-Dec-2022)
-------------------------

- Feature: Use ``--confirm`` to not request confirmation when removing instead of ``--force`` `#12636 <https://github.com/conan-io/conan/pull/12636>`_
- Feature: Simplify loading conaninfo.txt for search results `#12616 <https://github.com/conan-io/conan/pull/12616>`_
- Feature: Renamed ConanAPIV2 to ConanAPI `#12615 <https://github.com/conan-io/conan/pull/12615>`_
- Feature: Refactor ConanAPI `#12615 <https://github.com/conan-io/conan/pull/12615>`_
- Feature: Improve conan cache path command `#12554 <https://github.com/conan-io/conan/pull/12554>`_
- Feature: Improve #latest and pattern selection from remove/upload/download `#12572 <https://github.com/conan-io/conan/pull/12572>`_
- Feature: Add build_modules to provided deprecated warning to allow migration from 1.x `#12578 <https://github.com/conan-io/conan/pull/12578>`_
- Feature: Lockfiles alias support `#12525 <https://github.com/conan-io/conan/pull/12525>`_

2.0.0-beta5 (11-Nov-2022)
-------------------------

- Feature: Improvements in the remotes management and API `#12468 <https://github.com/conan-io/conan/pull/12468>`_
- Feature: Implement env_info and user_info as fake attributes in Conan 2.0 `#12351 <https://github.com/conan-io/conan/pull/12351>`_
- Feature: Improve settings.rm_safe() `#12379 <https://github.com/conan-io/conan/pull/12379>`_
- Feature: New RecipeReference equality `#12506 <https://github.com/conan-io/conan/pull/12506>`_
- Feature: Simplifying compress and uncompress of .tgz files `#12378 <https://github.com/conan-io/conan/pull/12378>`_
- Feature: conan source command does not require a default profile `#12475 <https://github.com/conan-io/conan/pull/12475>`_
- Feature: Created a proper LockfileAPI, with detailed methods (update, save, etc), instead of several loose methods `#12502 <https://github.com/conan-io/conan/pull/12502>`_
- Feature: The conan export can also produce lockfiles, necessary for users doing a 2 step (export + install--build) process `#12502 <https://github.com/conan-io/conan/pull/12502>`_
- Feature: Drop compat_app `#12484 <https://github.com/conan-io/conan/pull/12484>`_
- Fix: Fix transitive propagation of transitive_headers=True `#12508 <https://github.com/conan-io/conan/pull/12508>`_
- Fix: Fix transitive propagation of transitive_libs=False for static libraries `#12508 <https://github.com/conan-io/conan/pull/12508>`_
- Fix: Fix test_package for python_requires `#12508 <https://github.com/conan-io/conan/pull/12508>`_

2.0.0-beta4 (11-Oct-2022)
-------------------------

- Feature: Do not allow doing conan create/export with uncommitted changes using revision_mode=scm `#12267 <https://github.com/conan-io/conan/pull/12267>`_
- Feature: Simplify conan inspect command, removing path subcommand `#12263 <https://github.com/conan-io/conan/pull/12263>`_
- Feature: Add --deploy argument to graph info command `#12243 <https://github.com/conan-io/conan/pull/12243>`_
- Feature: Pass graph object to deployers instead of ConanFile `#12243 <https://github.com/conan-io/conan/pull/12243>`_
- Feature: Add included_files method to conan.tools.scm.Git `#12246 <https://github.com/conan-io/conan/pull/12246>`_
- Feature: Improve detection of clang libcxx `#12251 <https://github.com/conan-io/conan/pull/12251>`_
- Feature: Remove old profile variables system in favor of Jinja2 syntax in profiles `#12152 <https://github.com/conan-io/conan/pull/12152>`_
- Fix: Update command to follow Conan 2.0 conventions about CLI output `#12235 <https://github.com/conan-io/conan/pull/12235>`_
- Fix: Fix aggregation of test trait in diamonds `#12080 <https://github.com/conan-io/conan/pull/12080>`_

2.0.0-beta3 (12-Sept-2022)
--------------------------

- Feature: Decouple test_package from create. `#12046 <https://github.com/conan-io/conan/pull/12046>`_
- Feature: Warn if special chars in exported refs. `#12053 <https://github.com/conan-io/conan/pull/12053>`_
- Feature: Improvements in MSBuildDeps traits. `#12032 <https://github.com/conan-io/conan/pull/12032>`_
- Feature: Added support for CLICOLOR_FORCE env var, that will activate the colors in the output if the value is declared and different to 0. `#12028 <https://github.com/conan-io/conan/pull/12028>`_
- Fix: Call source() just once for all configurations. `#12050 <https://github.com/conan-io/conan/pull/12050>`_
- Fix: Fix deployers not creating output_folder. `#11977 <https://github.com/conan-io/conan/pull/11977>`_
- Fix: Fix build_id() removal of require. `#12019 <https://github.com/conan-io/conan/pull/12019>`_
- Fix: If Conan fails to load a custom command now it fails with a useful error message. `#11720 <https://github.com/conan-io/conan/pull/11720>`_
- Bugfix: If the 'os' is not specified in the build profile and a recipe, in Windows, wanted to run a command. `#11728 <https://github.com/conan-io/conan/pull/11728>`_

2.0.0-beta2 (27-Jul-2022)
-------------------------

- Feature: Add traits support in MSBuildDeps. `#11680 <https://github.com/conan-io/conan/pull/11680>`_
- Feature: Add traits support in XcodeDeps. `#11615 <https://github.com/conan-io/conan/pull/11615>`_
- Feature: Let dependency define package_id modes. `# <https://github.com/conan-io/conan/pull/11441>`_
- Feature: Add ``conan.conanrc`` file to setup the conan user home. `#11675 <https://github.com/conan-io/conan/pull/11675>`_
- Feature: Add ``core.cache:storage_path`` to declare the absolute path where you want to store the Conan packages. `#11672 <https://github.com/conan-io/conan/pull/11672>`_ 
- Feature: Add tools for checking max cppstd version. `#11610 <https://github.com/conan-io/conan/pull/11610>`_ 
- Feature: Add a ``post_build_fail`` hook that is called when a build fails. `#11593 <https://github.com/conan-io/conan/pull/11593>`_ 
- Feature: Add ``pre_generate`` and ``post_generate`` hook, covering the generation of files around the ``generate()`` method call. `#11593 <https://github.com/conan-io/conan/pull/11593>`_ 
- Feature: Brought ``conan config list`` command back and other conf improvements. `#11575 <https://github.com/conan-io/conan/pull/11575>`_ 
- Feature: Added two new arguments for all commands -v for controlling the verbosity of the output and --logger to output the contents in a json log format for log processors. `#11522 <https://github.com/conan-io/conan/pull/11522>`_ 

2.0.0-beta1 (20-Jun-2022)
-------------------------

- Feature: New graph model to better support C and C++ binaries relationships, compilation, and linkage.
- Feature: New documented public Python API, for user automation
- Feature: New build system integrations, more flexible and powerful, and providing transparent integration when possible, like ``CMakeDeps`` and ``CMakeToolchain``
- Feature: New custom user commands, that can be built using the public PythonAPI and can be shared and installed with ``conan config install``
- Feature: New CLI interface, with cleaner commands and more structured output
- Feature: New deployers mechanism to copy artifacts from the cache to user folders, and consume those copies while building.
- Feature: Improved ``package_id`` computation, taking into account the new more detailed graph model.
- Feature: Added ``compatibility.py`` extension mechanism to allow users to define binary compatibility globally.
- Feature: Simpler and more powerful ``lockfiles`` to provide reproducibility over time.
- Feature: Better configuration with ``[conf]`` and better environment management with the new ``conan.tools.env`` tools.
- Feature: Conan cache now can store multiple revisions simultaneously.
- Feature: New extensions plugins to implement profile checking, package signing, and build commands wrapping.
- Feature: Used the package immutability for an improved update, install and upload flows.
