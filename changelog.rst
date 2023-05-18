Changelog
=========

For a more detailed description of the major changes that Conan 2.0 brings, compared with Conan 1.X, please read :ref:`whatsnew`

2.0.5 (18-May-2023)
-------------------

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
