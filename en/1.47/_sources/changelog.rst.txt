.. spelling::

  dragly
  mathieu
  melmdk
  raulbocanegra
  rhel
  tivek
  tru
  yogeva

.. _changelog:

Changelog
=========

Check https://github.com/conan-io/conan for issues and more details about development, contributors, etc.

.. important::

    Conan 1.47 shouldn't break any existing 1.0 recipe or command line invocation. If it does, please submit 
    a report on GitHub. Read more about the :ref:`Conan stability commitment<stability>`.

1.47.0 (31-Mar-2022)
--------------------

- Feature: Renamed `tools.build:cppflags` to `tools.build:defines` and removed `tools.build:ldflags` (now it's the union between `tools.build:sharedlinkflags` and `tools.build:exelinkflags` in mostly all the cases). `#10928 <https://github.com/conan-io/conan/pull/10928>`_ . Docs `here <https://github.com/conan-io/docs/pull/2484>`__
- Feature: Adding cross-compilation for Android in MesonToolchain. `#10908 <https://github.com/conan-io/conan/pull/10908>`_ . Docs `here <https://github.com/conan-io/docs/pull/2480>`__
- Feature: Add extra flags via [conf] into XcodeToolchain. `#10906 <https://github.com/conan-io/conan/pull/10906>`_ . Docs `here <https://github.com/conan-io/docs/pull/2471>`__
- Feature: Preliminar support for CMakePresets.json. `#10903 <https://github.com/conan-io/conan/pull/10903>`_ . Docs `here <https://github.com/conan-io/docs/pull/2476>`__
- Feature: Added `wrap_mode=nofallback` project-option into `MesonToolchain` as default value. `#10884 <https://github.com/conan-io/conan/pull/10884>`_
- Feature: Added basic `rmdir` tool at `conan.tools.files`. `#10874 <https://github.com/conan-io/conan/pull/10874>`_ . Docs `here <https://github.com/conan-io/docs/pull/2470>`__
- Feature: Backport of 2.0 compatibility() recipe method. `#10868 <https://github.com/conan-io/conan/pull/10868>`_
- Feature: Add detection in meson toolchain for cross conditions and requirement of needs_exe_wrapper. Users may specify the exe wrapper in their meson.build now. `#10846 <https://github.com/conan-io/conan/pull/10846>`_
- Feature: Allow `tested_reference_str` to be `None`. `#10834 <https://github.com/conan-io/conan/pull/10834>`_
- Feature: New templates for the :command:`conan new` command with bazel examples: `bazel_exe` and `bazel_lib`. `#10812 <https://github.com/conan-io/conan/pull/10812>`_ . Docs `here <https://github.com/conan-io/docs/pull/2474>`__
- Feature: Add some support for ``msvc`` compiler older versions. `#10808 <https://github.com/conan-io/conan/pull/10808>`_
- Feature: Added mechanism to inject extra flags via `[conf]` into several toolchains like `AutotoolsToolchain`, `MesonToolchain` and `CMakeToolchain`. `#10800 <https://github.com/conan-io/conan/pull/10800>`_ . Docs `here <https://github.com/conan-io/docs/pull/2484>`__
- Feature: Support selecting the target to build for XcodeBuild helper. `#10799 <https://github.com/conan-io/conan/pull/10799>`_ . Docs `here <https://github.com/conan-io/docs/pull/2473>`__
- Feature:  Support for Xcode 13.3, iOS 15.4, watchOS 8.5 and tvOS 15.4. `#10797 <https://github.com/conan-io/conan/pull/10797>`_
- Feature: New modern "conan new --template=msbuild_lib|exe" for modern MSBuild VS integration. `#10760 <https://github.com/conan-io/conan/pull/10760>`_ . Docs `here <https://github.com/conan-io/docs/pull/2483>`__
- Feature: Added a checker for Conan 2.x deprecated `from conans` imports in `pylint_plugin`. `#10746 <https://github.com/conan-io/conan/pull/10746>`_ . Docs `here <https://github.com/conan-io/docs/pull/2475>`__
- Feature: New `conan.tool.microsoft.unix_path` to convert paths to any subsystem when using `conanfile.win_bash`. `#10743 <https://github.com/conan-io/conan/pull/10743>`_ . Docs `here <https://github.com/conan-io/docs/pull/2479>`__
- Feature: New ``from conan.errors import XXX`` new namespace to be ready for 2.0. `#10734 <https://github.com/conan-io/conan/pull/10734>`_ . Docs `here <https://github.com/conan-io/docs/pull/2482>`__
- Feature: Allow specifying `default_options = {"pkg/*:option": "value"}` or `default_options = {"pkg*:option": "value"}`   instead of `default_options = {"pkg:option": "value"}` to make compatible recipes with 2.0. `#10731 <https://github.com/conan-io/conan/pull/10731>`_ . Docs `here <https://github.com/conan-io/docs/pull/2468>`__
- Feature: Add Clang 15 to default settings. `#10558 <https://github.com/conan-io/conan/pull/10558>`_
- Feature: When the layout is declared, the cwd() in the source() method will follow the declared `self.folders.source` but the `exports_sources` will still be copied to the base source folder. `#10091 <https://github.com/conan-io/conan/pull/10091>`_ . Docs `here <https://github.com/conan-io/docs/pull/2486>`__
- Fix: Add support for ``clang`` to ``msvc_runtime_flag()``. It requires defining ``compiler.runtime = static/dynamic`` definition, same as modern ``msvc`` compiler setting. `#10898 <https://github.com/conan-io/conan/pull/10898>`_ . Docs `here <https://github.com/conan-io/docs/pull/2485>`__
- Fix: Generate the correct `--target` triple when building for Apple catalyst. `#10880 <https://github.com/conan-io/conan/pull/10880>`_
- Fix: The "conan.tools.files.patch" will (by default) look for the patch files in the `self.base_source_folder` instead of `self.source_folder` but will apply them with `self.source_folder` as the base folder. `#10875 <https://github.com/conan-io/conan/pull/10875>`_ . Docs `here <https://github.com/conan-io/docs/pull/2477>`__
- Fix: Setting `CMAKE_SYSTEM_PROCESSOR` for Apple cross-compiling including M1. `#10856 <https://github.com/conan-io/conan/pull/10856>`_ . Docs `here <https://github.com/conan-io/docs/pull/2472>`__
- Fix: Do not overwrite values for `CMAKE_SYSTEM_NAME`, `CMAKE_SYSTEM_VERSION` and `CMAKE_SYSTEM_PROCESSOR` set from the [conf] or the user_toolchain. `#10856 <https://github.com/conan-io/conan/pull/10856>`_ . Docs `here <https://github.com/conan-io/docs/pull/2472>`__
- Fix: Fix architecture translation from Conan syntax to build system in CMakeToolchain. `#10856 <https://github.com/conan-io/conan/pull/10856>`_ . Docs `here <https://github.com/conan-io/docs/pull/2472>`__
- Fix: Several improvements of the Bazel integration (`Bazel`, `BazelToolchain`, `BazelDeps`), new functional tests in all platforms. `#10812 <https://github.com/conan-io/conan/pull/10812>`_ . Docs `here <https://github.com/conan-io/docs/pull/2474>`__
- Fix: `Conf.get()` always returns `default` value if internal `conf_value.value` is `None`, i.e., it was unset. `#10800 <https://github.com/conan-io/conan/pull/10800>`_ . Docs `here <https://github.com/conan-io/docs/pull/2484>`__
- Fix: Set `-DCMAKE_MAKE_PROGRAM` when the generator is for MinGW and the conf `tools.gnu:make_program` is set. `#10770 <https://github.com/conan-io/conan/pull/10770>`_
- Fix: Remove unused ``clion_layout``. `#10760 <https://github.com/conan-io/conan/pull/10760>`_ . Docs `here <https://github.com/conan-io/docs/pull/2483>`__
- Fix: AutotoolsToolchain adjust the runtime flag of `msvc` (`MTd`, `MT`, `MDd` or `MD`) to `CFLAGS` and `CXXFLAGS` when using the `msvc` as `settings.compiler`. `#10755 <https://github.com/conan-io/conan/pull/10755>`_ . Docs `here <https://github.com/conan-io/docs/pull/2478>`__
- Fix: Removed `subsystem_path` from the `conan.tool.microsoft` namespace, superseded by `unix_path`. `#10743 <https://github.com/conan-io/conan/pull/10743>`_ . Docs `here <https://github.com/conan-io/docs/pull/2479>`__
- Fix: Show an error message at :command:`conan install` if the ``validate()`` method raises ``ConanInvalidConfiguration``. `#10725 <https://github.com/conan-io/conan/pull/10725>`_
- BugFix: The `find_dependency` called internally in `CMakeDeps` generator to locate transitive dependencies now use the `MODULE/NO_MODULE` following the `cmake_find_mode` property when declared in the dependency. `#10917 <https://github.com/conan-io/conan/pull/10917>`_
- Bugfix: Fix virtualrunenv wrong ``build`` scope. `#10904 <https://github.com/conan-io/conan/pull/10904>`_
- BugFix: Make ``self.folders.root`` apply at package ``conan install .`` too. `#10842 <https://github.com/conan-io/conan/pull/10842>`_
- Bugfix: Fix call to undefined function for markdown generator when components add `system_libs`. `#10783 <https://github.com/conan-io/conan/pull/10783>`_
- Bugfix: solve ``build_policy=never`` bug when ``conan export-pkg --force`` and there already exists a package in the cache. `#10738 <https://github.com/conan-io/conan/pull/10738>`_
- Bugfix: Add transitive dependencies to generated Bazel BUILD files. `#10686 <https://github.com/conan-io/conan/pull/10686>`_

1.46.2 (18-Mar-2022)
--------------------

- Bugfix: Fix deprecated imports checker line number. `#10822 <https://github.com/conan-io/conan/pull/10822>`_
- Bugfix: Specifying compiler.version=13 for apple-clang raised a CMake error when using the old cmake generator. `#10820 <https://github.com/conan-io/conan/pull/10820>`_

1.46.1 (17-Mar-2022)
--------------------

- Feature: Added a checker for Conan 2.x deprecated from conans imports in pylint_plugin. `#10811 <https://github.com/conan-io/conan/pull/10811>`_
- Feature: Add apple-clang 13 major version to settings. `#10807 <https://github.com/conan-io/conan/pull/10807>`_
- Feature: Make apple-clang 13 version package-id compatible with 13.0. `#10807 <https://github.com/conan-io/conan/pull/10807>`_
- Feature: Autodetect only major version for apple-clang profile starting in version 13. `#10807 <https://github.com/conan-io/conan/pull/10807>`_
- Feature: Add clang 15 version to settings. `#10807 <https://github.com/conan-io/conan/pull/10807>`_
- Bugfix: Fix call to undefined function for markdown generator when components add system_libs. `#10810 <https://github.com/conan-io/conan/pull/10810>`_

1.46.0 (07-Mar-2022)
--------------------

- Feature: Configuration field `tools.cmake.cmaketoolchain:user_toolchain` defined as list-like object `#10729 <https://github.com/conan-io/conan/pull/10729>`_ . Docs `here <https://github.com/conan-io/docs/pull/2427>`__
- Feature: Prepare Conan for search remote repos with mix of 1.X and 2.0 binaries. Conan 1.X will not list binaries (``conan search <ref>``) stored in remote repos that were created with Conan 2.0. `#10692 <https://github.com/conan-io/conan/pull/10692>`_
- Feature: Adding jinja rendering of global.conf config file. `#10687 <https://github.com/conan-io/conan/pull/10687>`_ . Docs `here <https://github.com/conan-io/docs/pull/2427>`__
- Feature: Improve markdown generator instructions. `#10673 <https://github.com/conan-io/conan/pull/10673>`_ . Docs `here <https://github.com/conan-io/docs/pull/2423>`__
- Feature: The `CMakeToolchain` and `AutotoolsToolchain` take into account the `cpp.package` info to set the output directories for libraries, executables, and so on when running `cmake.install` or `make install`. `#10672 <https://github.com/conan-io/conan/pull/10672>`_ . Docs `here <https://github.com/conan-io/docs/pull/2425>`__
- Feature: Added `basic_layout`, removed `meson_layout` and added argument `src_folder` to `cmake_layout`as a shortcut for adjusting `conanfile.folders.source`. `#10659 <https://github.com/conan-io/conan/pull/10659>`_ . Docs `here <https://github.com/conan-io/docs/pull/2426>`__
- Feature: Adding ``self.base_source_folder`` for ``exports_sources`` explicit layouts. `#10654 <https://github.com/conan-io/conan/pull/10654>`_ . Docs `here <https://github.com/conan-io/docs/pull/2418>`__
- Feature: Adding ``root`` to layout model to allow conanfile.py in subfolders. `#10654 <https://github.com/conan-io/conan/pull/10654>`_ . Docs `here <https://github.com/conan-io/docs/pull/2418>`__
- Feature: Added new property `component_version` for `PkgConfigDeps` and legacy `PkgConfig`. `#10633 <https://github.com/conan-io/conan/pull/10633>`_ . Docs `here <https://github.com/conan-io/docs/pull/2433>`__
- Feature: Changed `.pc` file description field for components in `PkgConfigDeps`. `#10633 <https://github.com/conan-io/conan/pull/10633>`_ . Docs `here <https://github.com/conan-io/docs/pull/2433>`__
- Feature: Add `sdk_version` setting for `Macos`, `iOS`, `watchOS` and `tvOS`. `#10608 <https://github.com/conan-io/conan/pull/10608>`_ . Docs `here <https://github.com/conan-io/docs/pull/2431>`__
- Feature: Add new `XcodeBuild` build helper. `#10608 <https://github.com/conan-io/conan/pull/10608>`_ . Docs `here <https://github.com/conan-io/docs/pull/2431>`__
- Feature: Add new `XcodeToolchain` helper. `#10608 <https://github.com/conan-io/conan/pull/10608>`_ . Docs `here <https://github.com/conan-io/docs/pull/2431>`__
- Feature: Add ``compiler.version`` 12 for GCC in settings. `#10595 <https://github.com/conan-io/conan/pull/10595>`_
- Feature: Introduce new ``conan.tools.scm.Git`` helper, for direct use in ``export()`` method to capture git url and commit, and to be used in ``source()`` method to clone and checkout a git repo. `#10594 <https://github.com/conan-io/conan/pull/10594>`_ . Docs `here <https://github.com/conan-io/docs/pull/2419>`__
- Feature: New ``from conan.tools.files import update_conandata()`` helper to add data to ``conandata.yml`` in the ``export()`` method. `#10586 <https://github.com/conan-io/conan/pull/10586>`_ . Docs `here <https://github.com/conan-io/docs/pull/2422>`__
- Feature: Add CMake variables, cli arguments and native build system arguments to new ``conan.tools.cmake.CMake`` helper. `#10573 <https://github.com/conan-io/conan/pull/10573>`_ . Docs `here <https://github.com/conan-io/docs/pull/2424>`__
- Feature: Adding more functionality to `ConfDefinition` and `Conf`, something similar to `ProfileEnvironment` and `Environment` ones. `#10537 <https://github.com/conan-io/conan/pull/10537>`_ . Docs `here <https://github.com/conan-io/docs/pull/2427>`__
- Feature: Port `conan.tools.Version` to Conan 1.X. `#10536 <https://github.com/conan-io/conan/pull/10536>`_ . Docs `here <https://github.com/conan-io/docs/pull/2434>`__
- Feature: Port `conan.tools.build.cross_building` to Conan 1.X. `#10536 <https://github.com/conan-io/conan/pull/10536>`_ . Docs `here <https://github.com/conan-io/docs/pull/2434>`__
- Feature: New `copy` tool at `conan.tools.files` namespace that will replace the `self.copy` in Conan 2.0. `#10530 <https://github.com/conan-io/conan/pull/10530>`_ . Docs `here <https://github.com/conan-io/docs/pull/2428>`__
- Feature: Add ``recipe_folder`` to pylint plugin. `#10527 <https://github.com/conan-io/conan/pull/10527>`_
- Fix: Pin Markupsafe==2.0.1 for py27 and upgrade Jinja2>3 for py3, after Markupsafe latest 2.1 release broke Jinja2 2.11. `#10710 <https://github.com/conan-io/conan/pull/10710>`_
- Fix: Fixed templates for :command:`conan new` with `--template cmake_lib` and `--template cmake_exe` to include Conan 2.0 compatible syntax. `#10706 <https://github.com/conan-io/conan/pull/10706>`_
- Fix: Moved new tool `cross_building` from `conan.tool.cross_building` to `conan.tool.build` to match the location in develop2. `#10706 <https://github.com/conan-io/conan/pull/10706>`_
- Fix: Don't compose folders in Xcode generator using `dep.package_folder`, now `cpp_info.bindirs`, `cpp_info.includedirs`, etc. are absolute. `#10694 <https://github.com/conan-io/conan/pull/10694>`_
- Fix: When the `layout()` method is declared, the `self.package_folder` in the recipe is now available even when doing a `conan install . `, pointing to the specified output folder (`-of` ) or the path of the conanfile if not specified. `#10655 <https://github.com/conan-io/conan/pull/10655>`_
- Fix: Fix creation path of deactivate scripts. `#10653 <https://github.com/conan-io/conan/pull/10653>`_
- Fix: Add support for `[tool_requires]` section in conanfile.txt. `#10642 <https://github.com/conan-io/conan/pull/10642>`_
- Fix: When ``layout()`` is defined, the ``exports`` will not be considered sources anymore, but only the ``exports_sources``. The ``exports`` are used exclusively by the recipe, but not as package source. `#10625 <https://github.com/conan-io/conan/pull/10625>`_
- Fix: Make the ``source()`` method run inside the ``self.source_folder``, in the same way ``build()`` runs in ``self.build_folder``. But only for recipes that define the ``layout()`` method, to not break unless using ``layout()``. `#10612 <https://github.com/conan-io/conan/pull/10612>`_ . Docs `here <https://github.com/conan-io/docs/pull/2418>`__
- Fix: Remove the ``--source-folder`` new argument to ``install`` and ``editable``, not necessary at the moment. `#10590 <https://github.com/conan-io/conan/pull/10590>`_ . Docs `here <https://github.com/conan-io/docs/pull/2420>`__
- Fix: Fix conf `True` and `False` handling in `tools.system.package_manage` helpers. `#10583 <https://github.com/conan-io/conan/pull/10583>`_
- Fix: Change the ``CMakeToolchain`` message to use ``CMAKE_CURRENT_LIST_FILE``. `#10552 <https://github.com/conan-io/conan/pull/10552>`_
- Fix: BazelDeps was generating invalid bazel files cause the static_library paths were absolute and not relative. `#10484 <https://github.com/conan-io/conan/pull/10484>`_
- Fix: BazelDeps was crashing when generating packages without libs cause the context was not checking the array size. `#10484 <https://github.com/conan-io/conan/pull/10484>`_
- Fix: Fix Premake test failing on Linux because the Premake executable isn't found. `#10250 <https://github.com/conan-io/conan/pull/10250>`_
- Bugfix: Fix ``MesonToolchain`` extra quotes in ``cpp_std`` `#10707 <https://github.com/conan-io/conan/pull/10707>`_
- Bugfix: Add missing ``system_libs`` management in ``AutotoolsDeps``. `#10681 <https://github.com/conan-io/conan/pull/10681>`_
- Bugfix: `GnuDepsFlags` attributes like `frameworks` and `frameworkdirs` are only available for Apple OS. `#10675 <https://github.com/conan-io/conan/pull/10675>`_
- Bugfix: Remove tmp folders created in Conan while checking the output of a command and detecting the compiler. `#10663 <https://github.com/conan-io/conan/pull/10663>`_
- Bugfix: Fix ``conan_server`` circular import do to ``conan.tools`` namespace. `#10635 <https://github.com/conan-io/conan/pull/10635>`_
- bugfix: Fix ``meson_layout()`` issue with shared folders. `#10600 <https://github.com/conan-io/conan/pull/10600>`_
- Bugfix: Fix ``SystemPackageTool`` when ``mode=verify``, it was still installing packages. `#10596 <https://github.com/conan-io/conan/pull/10596>`_
- Bugfix: ``self.build_folder`` not being computed even if ``layout()`` method is defined in local :command:`conan install`. Close https://github.com/conan-io/conan/issues/10566 `#10567 <https://github.com/conan-io/conan/pull/10567>`_
- Bugfix: Fix conan_manifest.txt parse error when the filename has ":" in it. `#10492 <https://github.com/conan-io/conan/pull/10492>`_
- Bugfix: Use meson toolchain file from install folder. `#8965 <https://github.com/conan-io/conan/pull/8965>`_

1.45.0 (02-Feb-2022)
--------------------

- Feature: Add system.package_manager tools to `conan config list`. `#10469 <https://github.com/conan-io/conan/pull/10469>`_ . Docs `here <https://github.com/conan-io/docs/pull/2379>`__
- Feature: Use system package manager helpers `from conan.tools.system.package_manager`. `#10467 <https://github.com/conan-io/conan/pull/10467>`_ . Docs `here <https://github.com/conan-io/docs/pull/2379>`__
- Feature: Add ``[tool_requires]`` section to profiles. `#10462 <https://github.com/conan-io/conan/pull/10462>`_
- Feature: Add ``meson_lib`` and ``meson_exe``, :command:`conan new` templates. `#10460 <https://github.com/conan-io/conan/pull/10460>`_ . Docs `here <https://github.com/conan-io/docs/pull/2364>`__
- Feature: Add `is_msvc_static_runtime` method to `conan.tools.microsoft.visual` to identify when using `msvc` with static runtime. `#10437 <https://github.com/conan-io/conan/pull/10437>`_ . Docs `here <https://github.com/conan-io/docs/pull/2372>`__
- Feature: Improve support for Visual Studio in ``AutotoolsToolchain``. `#10429 <https://github.com/conan-io/conan/pull/10429>`_
- Feature: Make `pkg-config` tooling accessible under `conan.tools.gnu.PkgConfig` and `conan.tools.gnu.PkgConfigDeps`. `#10415 <https://github.com/conan-io/conan/pull/10415>`_
- Feature: Use `.bazel` suffix for generated Bazel files. `#10391 <https://github.com/conan-io/conan/pull/10391>`_ . Docs `here <https://github.com/conan-io/docs/pull/2381>`__
- Feature: New tools in `conan.tools.system` for invoking system package managers in recipes. `#10380 <https://github.com/conan-io/conan/pull/10380>`_ . Docs `here <https://github.com/conan-io/docs/pull/2379>`__
- Feature: Testing the expected PC files created when the component name matches with the root package one using either `pkg_config` or `PkgConfigDeps` generators. `#10344 <https://github.com/conan-io/conan/pull/10344>`_ . Docs `here <https://github.com/conan-io/docs/pull/2378>`__
- Feature: Better definition of clang compiler in Windows in `CMakeToolchain`. `#10333 <https://github.com/conan-io/conan/pull/10333>`_
- Feature: Add VxWorks to OSs in default settings.yml. `#10315 <https://github.com/conan-io/conan/pull/10315>`_ . Docs `here <https://github.com/conan-io/docs/pull/2355>`__
- Feature: Add `is_msvc` to validate if `settings.compiler` is `Visual Studio` and `msvc` compilers. `#10310 <https://github.com/conan-io/conan/pull/10310>`_ . Docs `here <https://github.com/conan-io/docs/pull/2353>`__
- Feature: `os.sdk` field is mandatory for CMakeToolchain and OS in `('Macos', 'iOS', 'watchOS', 'tvOS')`. `#10300 <https://github.com/conan-io/conan/pull/10300>`_
- Feature: Adding ``--source-folder`` and ``--output-folder`` to ``conan editable`` and :command:`conan install` to work with ``layout()``. `#10274 <https://github.com/conan-io/conan/pull/10274>`_ . Docs `here <https://github.com/conan-io/docs/pull/2377>`__
- Feature: Adding clang 14 to ``settings.yml``. Needed for emsdk package in Conan Center Index. `#10269 <https://github.com/conan-io/conan/pull/10269>`_
- Feature: `PkgConfigDeps` shows `WARN` messages if there are duplicated `pkg_config_name` and/or `pkg_config_aliases`. `#10263 <https://github.com/conan-io/conan/pull/10263>`_ . Docs `here <https://github.com/conan-io/docs/pull/2378>`__
- Feature: Improvements in ``MesonToolchain``, including some cross-building functionality. `#10174 <https://github.com/conan-io/conan/pull/10174>`_
- Feature: Update content created by the markdown generator. `#9758 <https://github.com/conan-io/conan/pull/9758>`_ . Docs `here <https://github.com/conan-io/docs/pull/2380>`__
- Fix: Remove auto-detection of VS 2022 as ``msvc`` compiler, detect it as ``Visual Studio`` version ``17``. `#10457 <https://github.com/conan-io/conan/pull/10457>`_ . Docs `here <https://github.com/conan-io/docs/pull/2376>`__
- Fix: Do not report warning for duplicated component names in CMakeDeps. `#10456 <https://github.com/conan-io/conan/pull/10456>`_
- Fix: Let legacy `Meson` build helper use other backends apart from `ninja`. `#10447 <https://github.com/conan-io/conan/pull/10447>`_
- Fix: `msvc_runtime_flag` returns empty string instead of `None`. `#10424 <https://github.com/conan-io/conan/pull/10424>`_ . Docs `here <https://github.com/conan-io/docs/pull/2363>`__
- Fix: Parsing a url with query args in ``conan config install`` results in a bad filename that could fail. `#10423 <https://github.com/conan-io/conan/pull/10423>`_
- Fix: The argument `patch_file` from `tools.files.patch` is now relative to `conanfile.source_folder`by default, unless an absolute path to another location is provided, for example, to a path in the `conanfile.build_folder`. `#10408 <https://github.com/conan-io/conan/pull/10408>`_ . Docs `here <https://github.com/conan-io/docs/pull/2382>`__
- Fix: Use install folder for Bazel dependency paths. `#10391 <https://github.com/conan-io/conan/pull/10391>`_ . Docs `here <https://github.com/conan-io/docs/pull/2381>`__
- Fix: Enforce `CMP0091` policy to NEW in `CMakeToolchain`. `#10390 <https://github.com/conan-io/conan/pull/10390>`_
- Fix: Add quotes around `conan_message` output variable so it is not modified. `#10388 <https://github.com/conan-io/conan/pull/10388>`_
- Fix: Add ``pathlib`` as hidden-import to pyinstaller.py, so it is bundled with the installer. `#10386 <https://github.com/conan-io/conan/pull/10386>`_
- Fix: Move imports of pre-defined layouts to their build-system domain. `#10385 <https://github.com/conan-io/conan/pull/10385>`_ . Docs `here <https://github.com/conan-io/docs/pull/2364>`__
- Fix: Allow ``cmake`` generator checks for Visual Studio 2022. `#10361 <https://github.com/conan-io/conan/pull/10361>`_
- Fix: Do not generate transitive `.props` for `MSbuildDeps` tool-requires. `#10350 <https://github.com/conan-io/conan/pull/10350>`_
- Fix: Manage spaces in ``[buildenv]`` profile definition. `#10343 <https://github.com/conan-io/conan/pull/10343>`_
- Fix: Add ``-debug`` to `LDFLAGS` in ``AutotoolsToolchain`` when necessary. `#10339 <https://github.com/conan-io/conan/pull/10339>`_
- Fix: Fix extra `}` characters in cppstd info message. `#10337 <https://github.com/conan-io/conan/pull/10337>`_
- Fix: Fix quotes in generated environment deactivation scripts. `#10325 <https://github.com/conan-io/conan/pull/10325>`_
- Fix: Fix the ``CMakeToolchain`` generated code, so it doesnt fail for ``-Werror --warn-unitilized``. `#10292 <https://github.com/conan-io/conan/pull/10292>`_
- Fix: Fix spaces in settings.yml to prevent the YAML linter from complaining. `#10230 <https://github.com/conan-io/conan/pull/10230>`_
- Fix: Convert `NewCppInfo` folders to absolute. `#10207 <https://github.com/conan-io/conan/pull/10207>`_
- Fix: Improved CMakeToolchain robustness regarding ``find_file``, ``find_path`` and ``find_program`` commands allowing better cross-build scenarios and better differentiation of the right context where to get, for example,  executables (build vs host). `#10186 <https://github.com/conan-io/conan/pull/10186>`_ . Docs `here <https://github.com/conan-io/docs/pull/2383>`__
- Bugfix: Fix ``BazelDeps`` using absolute ``glob`` paths instead of relative. `#10478 <https://github.com/conan-io/conan/pull/10478>`_
- BugFix: Avoid BazelDeps exception when depending on a package without libs. Close https://github.com/conan-io/conan/issues/10471 `#10472 <https://github.com/conan-io/conan/pull/10472>`_
- Bugfix: Fix ``AttributeError: 'PackageEditableLayout' object has no attribute 'package_lock'`` that happened when sing ``package_revision_mode`` with ``editable`` packages (and lockfiles). `#10416 <https://github.com/conan-io/conan/pull/10416>`_
- Bugfix: Visual Studio 2022 auto-detected profile was incomplete. `#10322 <https://github.com/conan-io/conan/pull/10322>`_
- Bugfix: Fix the caching of `ConanFile.dependencies` at `validate()` time. `#10307 <https://github.com/conan-io/conan/pull/10307>`_
- Bugfix: Avoid ``package_id`` errors when using ``compatible_packages`` of repeated references (which can happen if using ``private`` dependencies). `#10266 <https://github.com/conan-io/conan/pull/10266>`_

1.44.1 (13-Jan-2022)
--------------------

- Bugfix: The `CMakeDeps` generator now uses the property `cmake_build_modules` declared in components of the required packages not only in the root cpp_info. `#10326 <https://github.com/conan-io/conan/pull/10326>`_
- Bugfix: Adding missing hidden-imports to pyinstaller. Close https://github.com/conan-io/conan/issues/10318 `#10320 <https://github.com/conan-io/conan/pull/10320>`_
- Bugfix: Make `pkg_config` generator listen to root `cpp_info` properties. `#10312 <https://github.com/conan-io/conan/pull/10312>`_

1.44.0 (29-Dec-2021)
--------------------

- Feature: Add `<PackageName>_LIBRARIES`, `<PackageName>_INCLUDE_DIRS`, `<PackageName>_INCLUDE_DIR`, `<PackageName>_DEFINITIONS` and `<PackageName>_VERSION_STRING` variables in CMakeDeps. `#10227 <https://github.com/conan-io/conan/pull/10227>`_
- Feature: Adding a new Block to the CMakeToolchain now doesn't require inheriting `CMakeToolchainBlock`. `#10213 <https://github.com/conan-io/conan/pull/10213>`_ . Docs `here <https://github.com/conan-io/docs/pull/2337>`__
- Feature: Add build_modules and build_modules_paths to JsonGenerator. `#10203 <https://github.com/conan-io/conan/pull/10203>`_ . Docs `here <https://github.com/conan-io/docs/pull/2329>`__
- Feature: The `CMakeToolchain` is now prepared to apply several user toolchains. `#10178 <https://github.com/conan-io/conan/pull/10178>`_ . Docs `here <https://github.com/conan-io/docs/pull/2340>`__
- Feature: In the conanfile.py of the test_package, the reference being tested is always available at `self.tested_reference_str`. `#10171 <https://github.com/conan-io/conan/pull/10171>`_ . Docs `here <https://github.com/conan-io/docs/pull/2341>`__
- Feature: Introduced a new `test_type` value `explicit` so a user can declare explicitly the `requires` or `build_requires` manually (using `self.tested_reference_str`), it won't be automatically injected as a require. In Conan 2.0 the `test_type` attribute will be ignored, the behavior will be always explicit, so declaring `test_type="explicit"` will make the test recipe compatible with Conan 2.0. `#10171 <https://github.com/conan-io/conan/pull/10171>`_ . Docs `here <https://github.com/conan-io/docs/pull/2341>`__
- Feature: Introduced `tool_requires` attribute to provide a compatible way to migrate to Conan 2.0, where the current concept of `build_requires` has been renamed to `tool_requires`. `#10168 <https://github.com/conan-io/conan/pull/10168>`_ . Docs `here <https://github.com/conan-io/docs/pull/2342>`__
- Feature: Upgrade Conan python jinja requirement to v3.x. `#10159 <https://github.com/conan-io/conan/pull/10159>`_
- Feature: Provided several `conan.tools.files` functions to manage symlinks: Transform absolute to relative symlinks, remove broken symlinks, remove external symlinks and get the symlinks in a folder. These tools will help migrate to Conan 2.0 where the package files won't be automatically cleaned from broken absolute symlinks or external symlinks. `#10154 <https://github.com/conan-io/conan/pull/10154>`_ . Docs `here <https://github.com/conan-io/docs/pull/2343>`__
- Feature: Remove legacy folder setters in ``conanfile.xxxx_folder = yyy`` only used for testing. `#10153 <https://github.com/conan-io/conan/pull/10153>`_
- Feature: Add ``Git.version`` property to check the current git version, aligned with ``SVN.version``. `#10114 <https://github.com/conan-io/conan/pull/10114>`_ . Docs `here <https://github.com/conan-io/docs/pull/2338>`__
- Feature: Add build_requires support in BazelDeps generators. `#9876 <https://github.com/conan-io/conan/pull/9876>`_
- Fix: Fix variable names set by `CMakeDeps` modules. `#10227 <https://github.com/conan-io/conan/pull/10227>`_
- Fix: Call to `find_dependency` in module mode to find transitive dependencies. `#10227 <https://github.com/conan-io/conan/pull/10227>`_
- Fix: remove rpath from .pc files generated by `pkg_config` & `PkgConfigDeps` generators. `#10192 <https://github.com/conan-io/conan/pull/10192>`_ . Docs `here <https://github.com/conan-io/docs/pull/2339>`__
- Fix: Deleted CMake warning for already existing targets. `#10150 <https://github.com/conan-io/conan/pull/10150>`_
- Bugfix: Fix passing component's linkflags in CMakeDepes generator `#10205 <https://github.com/conan-io/conan/pull/10205>`_
- Bugfix: `AutotoolsToolchain` was not passing the `compiler` to `get_gnu_triplet` function. `#10141 <https://github.com/conan-io/conan/pull/10141>`_

1.43.4 (18-Feb-2022)
--------------------

- Fix: Limit markupsafe python dependency to <2.1. `#10616 <https://github.com/conan-io/conan/pull/10616>`_

1.43.3 (13-Jan-2022)
--------------------

- Bugfix: The CMakeDeps generator now uses the property cmake_build_modules declared in components of the required packages not only in the root cpp_info. `#10331 <https://github.com/conan-io/conan/pull/10331>`_
- Bugfix: Make pkg_config generator listen to root cpp_info properties. `#10323 <https://github.com/conan-io/conan/pull/10323>`_

1.43.2 (21-Dec-2021)
--------------------

- Fix: Remove ``generator`` argument from ``cpp_info.set_property()`` method. `#10214 <https://github.com/conan-io/conan/pull/10214>`_ . Docs `here <https://github.com/conan-io/docs/pull/2331>`__
- Fix: Do not convert to ``cmake_build_modules`` property the legacy ``cpp_info.build_modules``. `#10208 <https://github.com/conan-io/conan/pull/10208>`_
- Bugfix: Compiler `msvc` was not working for CMake legacy generators. `#10195 <https://github.com/conan-io/conan/pull/10195>`_

1.43.1 (17-Dec-2021)
--------------------

- Bugfix: Making aggregate_components non-destructive, which was causing errors in generators with components. `#10183 <https://github.com/conan-io/conan/pull/10183>`_
- Bugfix: Fix the definition of D_GLIBCXX_USE_CXX11_ABI in gcc-like compilers for ``CMakeToolchain`` and ``AutotoolsToolchain``. Define it only to ``D_GLIBCXX_USE_CXX11_ABI=0`` for new compilers, assuming that the default is alread 1. `#10165 <https://github.com/conan-io/conan/pull/10165>`_

1.43.0 (03-Dec-2021)
--------------------

- Feature: Remove `cmake_target_namespace` and `cmake_module_target_namespace` properties. `#10099 <https://github.com/conan-io/conan/pull/10099>`_ . Docs `here <https://github.com/conan-io/docs/pull/2316>`__
- Feature: Allow `CMakeDeps` to set `cmake_target_name` property as an absolute target. `#10099 <https://github.com/conan-io/conan/pull/10099>`_ . Docs `here <https://github.com/conan-io/docs/pull/2316>`__
- Feature: Add warning in `CMakeDeps` generated CMake files when target names collide. `#10099 <https://github.com/conan-io/conan/pull/10099>`_ . Docs `here <https://github.com/conan-io/docs/pull/2316>`__
- Feature: Legacy cmake generators (`cmake_find_package`, `cmake_find_package_multi`) don't listen to new `set_properties` model anymore. `#10098 <https://github.com/conan-io/conan/pull/10098>`_ . Docs `here <https://github.com/conan-io/docs/pull/2316>`__
- Feature: `pkg_config_name` is used as the main name for a package/component and it will be used as the name for the `*.pc` file. `#10084 <https://github.com/conan-io/conan/pull/10084>`_ . Docs `here <https://github.com/conan-io/docs/pull/2315>`__
- Feature: Added new property`pkg_config_aliases` which admits a  list of strings to define different aliases for any package/component. `#10084 <https://github.com/conan-io/conan/pull/10084>`_ . Docs `here <https://github.com/conan-io/docs/pull/2315>`__
- Feature: Define ``os=baremetal`` in ``settings.yml`` to represent platforms without OS "bare metal". `#10067 <https://github.com/conan-io/conan/pull/10067>`_ . Docs `here <https://github.com/conan-io/docs/pull/2309>`__
- Feature: Modern ``tools.gnu.PkgConfig`` to supersede legacy ``tools.PkgConfig``. Includes management of `PKG_CONFIG_PATH` and mapping to a ``cpp_info`` structure `#10065 <https://github.com/conan-io/conan/pull/10065>`_ . Docs `here <https://github.com/conan-io/docs/pull/2310>`__
- Feature: Add ``test_requires()`` for 2.0 migration of force_host_context. `#10027 <https://github.com/conan-io/conan/pull/10027>`_ . Docs `here <https://github.com/conan-io/docs/pull/2313>`__
- Feature: Added C++23 support for Visual Studio and GCC 11.2 one. `#10021 <https://github.com/conan-io/conan/pull/10021>`_
- Feature: Enable ``from conan import ConanFile`` to prepare for future namespace. `#10016 <https://github.com/conan-io/conan/pull/10016>`_ . Docs `here <https://github.com/conan-io/docs/pull/2318>`__
- Feature: Add backend support to MesonToolchain. `#9990 <https://github.com/conan-io/conan/pull/9990>`_ . Docs `here <https://github.com/conan-io/docs/pull/2295>`__
- Fix: Fix `<PackageName>_FIND_COMPONENTS` CMake generated variable to the correct value associated with the filename, not the package name. `#10098 <https://github.com/conan-io/conan/pull/10098>`_ . Docs `here <https://github.com/conan-io/docs/pull/2316>`__
- Fix: Updated the ConanException in installer.py to improve the error message handling. `#10089 <https://github.com/conan-io/conan/pull/10089>`_ . Docs `here <https://github.com/conan-io/docs/pull/2305>`__
- Fix: Simplify ``parallel`` definition in new ``conf``, leaving only ``tools.build:jobs``. Use max number of CPUs by default to build in parallel. `#10068 <https://github.com/conan-io/conan/pull/10068>`_ . Docs `here <https://github.com/conan-io/docs/pull/2308>`__
- Fix: Fix the ``msvc`` version model, which is comparison broken with the "main" 19.3 version < 19.22. `#10057 <https://github.com/conan-io/conan/pull/10057>`_ . Docs `here <https://github.com/conan-io/docs/pull/2314>`__
- Fix: Fix the `EnvVar.save_ps1()` method. `#10049 <https://github.com/conan-io/conan/pull/10049>`_
- Fix: CMakeToolchain will not crash if build_type not defined. `#9984 <https://github.com/conan-io/conan/pull/9984>`_
- Fix: Avoid raising an exception for ``conan info --paths`` when there are editables in the graph. `#9944 <https://github.com/conan-io/conan/pull/9944>`_
- Fix: Fix wrong parameter name in CMakeDeps find_library function. `#9932 <https://github.com/conan-io/conan/pull/9932>`_
- Fix: Improve error message when unzipping Conan `.tgz` artifacts. `#9925 <https://github.com/conan-io/conan/pull/9925>`_
- Fix: Respect error code 6 in some situations. `#9905 <https://github.com/conan-io/conan/pull/9905>`_
- Bugfix: Fix parallel package downloading. While downloading conan locks incorrect package ref. `#10038 <https://github.com/conan-io/conan/pull/10038>`_
- Bugfix: Add import for ``CMakeToolchainBlock`` custom Blocks in ``CMakeToolchain``. `#10026 <https://github.com/conan-io/conan/pull/10026>`_ . Docs `here <https://github.com/conan-io/docs/pull/2312>`__
- Bugfix: Option `--require-override` is not working for `conanfile.txt`. `#10013 <https://github.com/conan-io/conan/pull/10013>`_
- Bugfix: Fix unescaped double-quotes for defines in ``Premake`` generator. `#10008 <https://github.com/conan-io/conan/pull/10008>`_
- Bugfix: Use new `tools.cross_building` in MesonToolchain . `#9992 <https://github.com/conan-io/conan/pull/9992>`_
- Bugfix: CMakeDeps generated `*-data.cmake` was not including properly the set of link flags. `#9980 <https://github.com/conan-io/conan/pull/9980>`_
- Bugfix: CMakeDeps was not populating `INTERFACE_LINK_OPTIONS` to each target. `#9980 <https://github.com/conan-io/conan/pull/9980>`_
- Bugfix: `PkgConfigDeps` was not adding correctly the `Requires` for all the package dependencies. `#9945 <https://github.com/conan-io/conan/pull/9945>`_
- Bugfix: ``user_toolchain`` properly included and path quoted in ``CMakeToolchain``. `#9916 <https://github.com/conan-io/conan/pull/9916>`_
- Bugfix: Solved an issue with the `conan config install` whereby a cryptic error was raised when a user tried to install a directory that previously was a file and vice-versa. `#9908 <https://github.com/conan-io/conan/pull/9908>`_
- Bugfix: Missing framework for Xcode generator with no compiler setting. `#9896 <https://github.com/conan-io/conan/pull/9896>`_

1.42.2 (22-Nov-2021)
--------------------

- Bugfix: Legacy `cmake_multi` generator is not affected by `set_property`. `#10062 <https://github.com/conan-io/conan/pull/10062>`_

1.42.1 (08-Nov-2021)
--------------------

- Fix: Fix XcodeDeps architecture name translation from Conan to Apple identifiers. `#9955 <https://github.com/conan-io/conan/pull/9955>`_
- Bugfix: Fix XcodeDeps bad xcconfig generation when using dash-case-named packages `#9955 <https://github.com/conan-io/conan/pull/9955>`_
- Bugfix: Avoid exception if ``msvc`` compiler not defined in settings.yml file. `#9954 <https://github.com/conan-io/conan/pull/9954>`_
- Bugfix: legacy `cmake` generator is not affected by `set_property`. `#9952 <https://github.com/conan-io/conan/pull/9952>`_

1.42.0 (29-Oct-2021)
--------------------

- Feature: Remove `sdk` condition in _.xcconfig_ files generated by _XcodeDeps_. `#9887 <https://github.com/conan-io/conan/pull/9887>`_
- Feature: Add new Macos version 12.0 (Monterey). `#9886 <https://github.com/conan-io/conan/pull/9886>`_
- Feature: Add `CMAKE_POSITION_INDEPENDENT_CODE` in `CMakeToolchain` if it's set in the conanfile independently from the value of the shared option. `#9868 <https://github.com/conan-io/conan/pull/9868>`_
- Feature: Generate aggregated deactivation file for aggregated environments. `#9862 <https://github.com/conan-io/conan/pull/9862>`_ . Docs `here <https://github.com/conan-io/docs/pull/2279>`__
- Feature: adding preprocessor definitions to ``MSBuildTolchain`` ResourceCompile. `#9843 <https://github.com/conan-io/conan/pull/9843>`_
- Feature: Support `cmake_module_target_name` and `cmake_module_file_name` properties in _cmake_find_package_ generator. `#9832 <https://github.com/conan-io/conan/pull/9832>`_ . Docs `here <https://github.com/conan-io/docs/pull/2271>`__
- Feature: Define new ``conf["tools.microsoft.msbuild:install_path"]`` for the MSBuild toolchain and remove generation of intel_vars files by ``VCVars``. `#9827 <https://github.com/conan-io/conan/pull/9827>`_ . Docs `here <https://github.com/conan-io/docs/pull/2281>`__
- Feature: New Conan _XcodeDeps_ multi-config generator for _Xcode_. `#9807 <https://github.com/conan-io/conan/pull/9807>`_ . Docs `here <https://github.com/conan-io/docs/pull/2274>`__
- Feature: Refactor `conan.tools.gnu.pkgconfigdeps` module. `#9806 <https://github.com/conan-io/conan/pull/9806>`_
- Feature: Decoupled ``Environment`` as an abstract environment representation (do not depend on conanfile), and ``EnvVars``, as the specialization for a given conanfile, settings/settings_build, and ``win_bash``. `#9755 <https://github.com/conan-io/conan/pull/9755>`_ . Docs `here <https://github.com/conan-io/docs/pull/2279>`__
- Feature: Enabled `patch_string` when using `apply_conandata_patches`. `#9740 <https://github.com/conan-io/conan/pull/9740>`_ . Docs `here <https://github.com/conan-io/docs/pull/2246>`__
- Feature: Add property "cmake_target_aliases" to create some CMake alias targets using CMakeDeps. `#8533 <https://github.com/conan-io/conan/pull/8533>`_
- Fix: Do not fall back for the property "filename" to target properties, only to legacy "names" definition. `#9894 <https://github.com/conan-io/conan/pull/9894>`_
- Fix: Fix build settings conditional logic to work correctly with Xcode IDE. `#9892 <https://github.com/conan-io/conan/pull/9892>`_
- Fix: Show a more specific error message on 'conan search' when a package version is not valid `#9891 <https://github.com/conan-io/conan/pull/9891>`_
- Fix: Removed the new layout `folders.package` property as it was not clear the value/usage. `#9884 <https://github.com/conan-io/conan/pull/9884>`_ . Docs `here <https://github.com/conan-io/docs/pull/2278>`__
- Fix: The "conan package" method now raises an exception when declaring the layout() method. This is part of the migration to Conan 2.0 where the local method "conan package" is removed. `#9884 <https://github.com/conan-io/conan/pull/9884>`_ . Docs `here <https://github.com/conan-io/docs/pull/2278>`__
- Fix: Moved experimental LayoutPackager to a `conan.tools.files.AutoPackager` with a new interface. Removed also the `conanfile.patterns` attribute that now is configured directly in the AutoPackager. `#9882 <https://github.com/conan-io/conan/pull/9882>`_ . Docs `here <https://github.com/conan-io/docs/pull/2278>`__
- Fix: When the `layout()` method is declared inside the conanfile.py of a `test-package`, Conan won't generate temporary folders at build/_HASH_ anymore. The build folder will follow the structure declared at the layout() method. `#9882 <https://github.com/conan-io/conan/pull/9882>`_ . Docs `here <https://github.com/conan-io/docs/pull/2278>`__
- Fix: Fix frameworks aggregation in XcodeDeps. `#9881 <https://github.com/conan-io/conan/pull/9881>`_
- Fix: Remove python ``requests`` version from ``User-Agent`` header, it can be problematic sometimes and adds no value. `#9861 <https://github.com/conan-io/conan/pull/9861>`_
- Fix: Change ``MesonToolchain`` to define ``preprocessor_definitions`` as ``[constant]``, because Meson 0.60 now raises errors on it defined in ``[built-in options]``. `#9858 <https://github.com/conan-io/conan/pull/9858>`_
- Fix: Rename ``ConanFileInterface.new_cpp_info`` to ``ConanFileInterface.cpp_info`` (being it a ``NewCppInfo`` object). The `ConanFileInterface` object is only used when accessing `self.dependencies` in a conanfile, so we can make sure that the new develop generators use the final `cpp_info` name. `#9800 <https://github.com/conan-io/conan/pull/9800>`_ . Docs `here <https://github.com/conan-io/docs/pull/2280>`__
- Fix: Renamed ``group`` argument in ``Environment`` classes to ``scope``, that can get "build" and "run" values. `#9755 <https://github.com/conan-io/conan/pull/9755>`_ . Docs `here <https://github.com/conan-io/docs/pull/2279>`__
- Fix: New ``win_bash`` behavior failed for dual profile, the new computation of subsystem paths completely depend now on defined settings, but not on ``platform.system()`` or auto-detection. `#9755 <https://github.com/conan-io/conan/pull/9755>`_ . Docs `here <https://github.com/conan-io/docs/pull/2279>`__
- Bugfix: Avoid lockfile raising because of incorrect options when using ``compatible_packages``. Close https://github.com/conan-io/conan/issues/9591 `#9890 <https://github.com/conan-io/conan/pull/9890>`_
- Bugfix: Avoid VCVars defining ``-vcvars`` argument for VS<=2015. Close https://github.com/conan-io/conan/issues/9888 `#9889 <https://github.com/conan-io/conan/pull/9889>`_
- Bugfix: Respect the previous value of ``sys.dont_write_bytecode``. `#9865 <https://github.com/conan-io/conan/pull/9865>`_
- Bugfix: :command:`conan export-pkg` now raises an error (ConanInvalidConfiguration exception) if the ``validate()`` method raise that error and results in an invalid `package_id`. `#9818 <https://github.com/conan-io/conan/pull/9818>`_
- Bugfix: Respect the ``build_policy="never"`` even for ``--build=missing`` cli argument. `#9817 <https://github.com/conan-io/conan/pull/9817>`_
- Bugfix: Avoid crash in ``CMakeToolchain`` for custom generator when compiler is not defined. `#9801 <https://github.com/conan-io/conan/pull/9801>`_
- Bugfix: Do not force new authentication when a token is expired, it might not be needed. `#9781 <https://github.com/conan-io/conan/pull/9781>`_
- Bugfix: The CMakeToolchain generator always sets fPIC enabled due to a typo where the actual parameter is not templated but instead hard-coded as `ON`. `#9752 <https://github.com/conan-io/conan/pull/9752>`_
- Bugfix: The path to a patch file in a `conandata.yml` is also relative to the base source folder when the patches are not associated with a version (list of patches). `#9740 <https://github.com/conan-io/conan/pull/9740>`_ . Docs `here <https://github.com/conan-io/docs/pull/2246>`__

1.41.0 (06-Oct-2021)
--------------------

- Feature: Added `IntelCC` as public generator. `#9747 <https://github.com/conan-io/conan/pull/9747>`_ . Docs `here <https://github.com/conan-io/docs/pull/2233>`__
- feature: Prepare ``conan.tools.files download, get, ftp_download`` for adoption. `#9715 <https://github.com/conan-io/conan/pull/9715>`_ . Docs `here <https://github.com/conan-io/docs/pull/2249>`__
- Feature: Support multiple toolchains in one recipe. `#9688 <https://github.com/conan-io/conan/pull/9688>`_ . Docs `here <https://github.com/conan-io/docs/pull/2238>`__
- Feature: ``MSBuildDeps`` generator learned how to handle ``build_requires`` to use executables from them. `#9686 <https://github.com/conan-io/conan/pull/9686>`_ . Docs `here <https://github.com/conan-io/docs/pull/2248>`__
- Feature: ``PkgConfig`` helper now honors `PKG_CONFIG` environment variable. `#9627 <https://github.com/conan-io/conan/pull/9627>`_
- Feature: Make new environment generators multi-config (Release/Debug and arch). `#9543 <https://github.com/conan-io/conan/pull/9543>`_ . Docs `here <https://github.com/conan-io/docs/pull/2247>`__
- Feature: Environment ``activate`` scripts will generate ``deactivate`` scripts by default. `#9539 <https://github.com/conan-io/conan/pull/9539>`_
- Feature: Support remote archives other than zip in ``conan config install``. `#9530 <https://github.com/conan-io/conan/pull/9530>`_
- Feature: New "compiler" `intel-cc` with different modes (icx, dpcpp, classic) for Intel oneAPI. `#9522 <https://github.com/conan-io/conan/pull/9522>`_ . Docs `here <https://github.com/conan-io/docs/pull/2233>`__
- Feature: Add Intel oneAPI support for `CMakeToolChain`, `MSBuildToolchain` and `VCVars`. `#9522 <https://github.com/conan-io/conan/pull/9522>`_ . Docs `here <https://github.com/conan-io/docs/pull/2233>`__
- Feature: Add objects attribute to the cpp_info so that we can add object files to the linker without having to add those mixed with linker flags. `#9520 <https://github.com/conan-io/conan/pull/9520>`_ . Docs `here <https://github.com/conan-io/docs/pull/2243>`__
- Feature: New setttings: _xtensalx6_ and _xtensalx106_ for ESP32/ESP8266 platforms. `#7977 <https://github.com/conan-io/conan/pull/7977>`_
- Fix: New environment deactivate scripts fail in Windows because env-var different casing. `#9741 <https://github.com/conan-io/conan/pull/9741>`_
- Fix: Avoid "overcrowding" Windows environment variables with `LD_LIBRARY_PATH` and `DYLD_LIBRARY_PATH`, not used in Windows. `#9678 <https://github.com/conan-io/conan/pull/9678>`_
- Fix: Command :command:`conan package` now works for new ``layout()`` with generators folder. `#9674 <https://github.com/conan-io/conan/pull/9674>`_
- Fix:  Don't just print  "ERROR: True" on unresolvable conflict. `#9624 <https://github.com/conan-io/conan/pull/9624>`_
- Fix: Fix migrations settings comparison. `#9615 <https://github.com/conan-io/conan/pull/9615>`_
- Fix: Removed unused ``future`` dependency from Python ``requirements.txt``. `#9563 <https://github.com/conan-io/conan/pull/9563>`_
- Fix: Make automatic call of ``VirtualBuildEnv`` and ``VirtualRunEnv`` independent. `#9543 <https://github.com/conan-io/conan/pull/9543>`_ . Docs `here <https://github.com/conan-io/docs/pull/2247>`__
- Bugfix: ``generator_folder`` was using the ``cwd`` instead of a relative folder to the conanfile, producing layout errors. `#9668 <https://github.com/conan-io/conan/pull/9668>`_
- Bugfix: Support components with symbolic imports. `#9667 <https://github.com/conan-io/conan/pull/9667>`_
- Bugfix: Fix ``conan.tools.files.patch`` bug with ``strip`` argument. `#9653 <https://github.com/conan-io/conan/pull/9653>`_
- Bugfix: Add support for Xcode 13/Apple clang 13.0 `#9642 <https://github.com/conan-io/conan/pull/9642>`_
- Bugfix: Fixed bad `Requires` declaration in `*.pc` files. `#9635 <https://github.com/conan-io/conan/pull/9635>`_
- Bugfix: Fixed bug whereby when a conflict of requirements happens, in some special situations, just a message `ERROR: True` was printed in the terminal, making it hard to guess what was going on. `#9633 <https://github.com/conan-io/conan/pull/9633>`_
- BugFix: Fixed a bug where using the new `layout()` the `exports` went to the `conanfile.source_folder` instead of the base source folder in the cache and only the `exports_sources` should go there. `#9536 <https://github.com/conan-io/conan/pull/9536>`_

1.40.4 (05-Oct-2021)
--------------------

- Fix: Check current _cacert.pem_ file when updating Conan and only migrate if the user has not modified the file. If  the local file is modified then create a new cacert file but don't overwrite current. `#9734 <https://github.com/conan-io/conan/pull/9734>`_
- Fix: Update Conan debian package to fix ssl certificates problem. `#9723 <https://github.com/conan-io/conan/pull/9723>`_

1.40.3 (30-Sept-2021)
---------------------

- Bugfix: Added root certificate for Let's encrypt. `#9697 <https://github.com/conan-io/conan/pull/9697>`_

1.40.2 (21-Sept-2021)
---------------------

- Bugfix: Add support for Xcode 13/Apple clang 13.0 `#9643 <https://github.com/conan-io/conan/pull/9643>`_

1.40.1 (14-Sept-2021)
---------------------

- Feature: Change default `cmake_layout()` source folder from 'src' to '.' `#9596 <https://github.com/conan-io/conan/pull/9596>`_ . Docs `here <https://github.com/conan-io/docs/pull/2225>`__
- Feature: Recovered `base_path` argument for `conan.tools.files.patch` and `conan.tools.files.apply_conandata_patches` to be able to specify a relative folder from the `conanfile.source_folder` directory (that follows the layout() method). `#9593 <https://github.com/conan-io/conan/pull/9593>`_ . Docs `here <https://github.com/conan-io/docs/pull/2222>`__
- Fix: Allow user definition of `CMAKE_XXX_INIT` variables in user toolchains when using `CMakeToolchain`. `#9576 <https://github.com/conan-io/conan/pull/9576>`_
- Fix: Upgrade minimum ``requests>=2.25`` in requirements.txt to make it compatible with latest upgrade of ``urllib3`` to 1.26.6 `#9562 <https://github.com/conan-io/conan/pull/9562>`_
- Bugfix: Aggregate `[conf]` from `build_requires` earlier so it is available for generators declared as `generators`. attribute. Close https://github.com/conan-io/conan/issues/9571 `#9573 <https://github.com/conan-io/conan/pull/9573>`_
- Bugfix: The qmake generator now assigns `QMAKE_LFLAGS_SHLIB` and `QMAKE_LFLAGS_APP` variables instead of the incorrect `QMAKE_LFLAGS` following the official docs. `#9568 <https://github.com/conan-io/conan/pull/9568>`_ . Docs `here <https://github.com/conan-io/docs/pull/2224>`__

1.40.0 (06-Sept-2021)
---------------------

- Feature: Update :command:`conan new` modern templates ``--template=cmake_lib`` and ``--template=cmake_exe``. `#9516 <https://github.com/conan-io/conan/pull/9516>`_ . Docs `here <https://github.com/conan-io/docs/pull/2211>`__
- Feature: Introduced a new cpp_info property `cmake_target_namespace` to declare the target namespace for the `CMakeDeps` generator. This feature allows declaring a global target with a different namespace like `Foo::Bar`. `#9513 <https://github.com/conan-io/conan/pull/9513>`_ . Docs `here <https://github.com/conan-io/docs/pull/2209>`__
- Feature: Detect Visual Studio 2022 as `msvc`. `#9504 <https://github.com/conan-io/conan/pull/9504>`_
- Feature: Add Clang 13 support. `#9502 <https://github.com/conan-io/conan/pull/9502>`_ . Docs `here <https://github.com/conan-io/docs/pull/2204>`__
- Feature: Testing support for Windows CMake + Clang (independent LLVM, not VS) + Ninja/MinGW builds, and CMake + Clang (Visual Studio 16 internal LLVM 11 via ClangCL toolset). `#9477 <https://github.com/conan-io/conan/pull/9477>`_
- Feature: Provide new ``[conf]`` ``core:default_build_profile`` to enable the usage of the build profile as default, and to allow definition of the host profile default in new ``[conf]`` ``core:default_profile``. `#9468 <https://github.com/conan-io/conan/pull/9468>`_ . Docs `here <https://github.com/conan-io/docs/pull/2213>`__
- Feature: **CMakeToolchain** new member `find_builddirs` defaulted to `True` to add the `cpp_info.builddirs` from the requirements to the `CMAKE_PREFIX_PATH/CMAKE_MODULE_PATH`. That would allow finding the config files packaged and to be able to `include()` them from the consumer `CMakeLists.txt`. `#9455 <https://github.com/conan-io/conan/pull/9455>`_ . Docs `here <https://github.com/conan-io/docs/pull/2209>`__
- Feature: **CMakeDeps**. Added a new property `cmake_find_mode` with possible values to `config`(default), `module`, `both` or `none` to control the files to be generated from a package itself. The `none` replaces the current `skip_deps_file` property. `#9455 <https://github.com/conan-io/conan/pull/9455>`_ . Docs `here <https://github.com/conan-io/docs/pull/2209>`__
- Feature: **CMakeDeps**: Added two new properties `cmake_module_file_name` and `cmake_module_target_name`, analog to `cmake_file_name` and `cmake_target_name`, but to configure the name of `FindXXX.cmake` file and the target declared inside. `#9455 <https://github.com/conan-io/conan/pull/9455>`_ . Docs `here <https://github.com/conan-io/docs/pull/2209>`__
- Feature: Remove `conan-center` (https://conan.bintray.com) default remote. `#9401 <https://github.com/conan-io/conan/pull/9401>`_ . Docs `here <https://github.com/conan-io/docs/pull/2212>`__
- Feature: Implement round trip new profile ``[buildenv]`` section, necessary for lockfiles, and specially stdout printing. `#9320 <https://github.com/conan-io/conan/pull/9320>`_
- Feature: Allow ``-o &:option=value`` wildcard for consumer, too, same it was done for settings in 1.39 `#9316 <https://github.com/conan-io/conan/pull/9316>`_ . Docs `here <https://github.com/conan-io/docs/pull/2214>`__
- Fix: Adding management of private dependencies, via new ``visible`` trait compatible with 2.0 for new ``CMakeDeps`` and ``MSBuildDeps``. `#9517 <https://github.com/conan-io/conan/pull/9517>`_
- Fix: Remove unused ``deprecation`` pip dependency `#9478 <https://github.com/conan-io/conan/pull/9478>`_
- Fix: Upgrade ``distro`` dependency to allow 1.6.0 `#9462 <https://github.com/conan-io/conan/pull/9462>`_
- Fix: Make :command:`conan remove` accept package reference syntax. `#9459 <https://github.com/conan-io/conan/pull/9459>`_ . Docs `here <https://github.com/conan-io/docs/pull/2198>`__
- Fix: Fixed old CMake build helper to cross-build to iOS when two profiles are specified. `#9437 <https://github.com/conan-io/conan/pull/9437>`_
- Fix: Fix :command:`conan export` typo in help message. `#9408 <https://github.com/conan-io/conan/pull/9408>`_ . Docs `here <https://github.com/conan-io/docs/pull/2187>`__
- Fix:  Relax python six dependency to allow 1.16 `#9407 <https://github.com/conan-io/conan/pull/9407>`_
- Fix: Bump urllib3 version to 1.26.6 `#9405 <https://github.com/conan-io/conan/pull/9405>`_
- Fix: The new `Autotools` build helper accepts a `build_script_folder ` argument in the `configure()` method to specify are subfolder where the configure script is. `#9393 <https://github.com/conan-io/conan/pull/9393>`_ . Docs `here <https://github.com/conan-io/docs/pull/2208>`__
- Fix: Use `frameworks` in Premake generator. `#9371 <https://github.com/conan-io/conan/pull/9371>`_ . Docs `here <https://github.com/conan-io/docs/pull/2210>`__
- Fix: The tool `conan.tools.files.apply_conandata_patches` will use the root source folder to find the patch file and the tool `conan.tools.files.patch` will take the current source folder declared in the `layout()` method to know where is the source to apply the patches. `#9361 <https://github.com/conan-io/conan/pull/9361>`_ . Docs `here <https://github.com/conan-io/docs/pull/2207>`__
- Fix: Avoid checking other remotes when ``-r=remote`` is defined and revisions are activated and binary is not found in the defined remote. `#9355 <https://github.com/conan-io/conan/pull/9355>`_
- Bugfix: Setting the `CMAKE_OSX_DEPLOYMENT_TARGET` variable as a cache entry. `#9498 <https://github.com/conan-io/conan/pull/9498>`_
- BugFix: Use topological ordering to define `VirtualBuildEnv` composition and precedence of appending variables. `#9491 <https://github.com/conan-io/conan/pull/9491>`_
- Bugfix: Bazel build files have an extra `]` if there are no dependencies. `#9480 <https://github.com/conan-io/conan/pull/9480>`_
- Bugfix: Add AlmaLinux to `with_yum`. `#9463 <https://github.com/conan-io/conan/pull/9463>`_
- Bugfix: **CMakeToolchain**. Fixed a bugfix whereby a variable declared at the `.variables` containing a boolean ended at CMake with a quoted `"True"` or `"False"` values, instead of `ON` / `OFF` `#9455 <https://github.com/conan-io/conan/pull/9455>`_ . Docs `here <https://github.com/conan-io/docs/pull/2209>`__
- Bugfix: Fixed bug whereby Conan failed when using `compiler=gcc` with `compiler.version=5` (without specifying a minor version) and `compiler.cppstd=17`. `#9431 <https://github.com/conan-io/conan/pull/9431>`_
- Bugfix: No verbose traceback was been printed for `conanfile.layout()` method. `#9384 <https://github.com/conan-io/conan/pull/9384>`_
- Bugfix: Fix Bazel `cc_library`: `deps` and `linkopts`. `#9381 <https://github.com/conan-io/conan/pull/9381>`_
- Bugfix: Fixed bug whereby using new `layout()` method together with `cppinfo.components` in the `package_info` method caused an exception. `#9360 <https://github.com/conan-io/conan/pull/9360>`_
- Bugfix: Fix `PkgConfigDeps` that was failing in the case of components with requirements. `#9341 <https://github.com/conan-io/conan/pull/9341>`_

1.39.0 (27-Jul-2021)
--------------------

- Feature: Use `CMAKE_OSX_DEPLOYMENT_TARGET` to get `-version-min` set in _CMakeToolchain_. `#9301 <https://github.com/conan-io/conan/pull/9301>`_
- Feature: Display ``python_requires`` information in the :command:`conan info` output. `#9290 <https://github.com/conan-io/conan/pull/9290>`_
- Feature: Now it is possible to define settings for a downstream consumer using `-s &:setting=value` or the same syntax in the profile even if the consumer is a `conanfile.txt` or a `conanfile.py` not declaring a name. e.g: Building a Debug application with Release dependencies: `-s build_type=Release -s &:build_type=Debug` `#9267 <https://github.com/conan-io/conan/pull/9267>`_ . Docs `here <https://github.com/conan-io/docs/pull/2160>`__
- Feature: The `AutotoolsDeps` allows to alter the generated environment corresponding to the information read from the dependencies before calling the `generate()` method. `#9256 <https://github.com/conan-io/conan/pull/9256>`_ . Docs `here <https://github.com/conan-io/docs/pull/2155>`__
- Feature: new `remove` and `items` methods for the `Environment` objects. `#9256 <https://github.com/conan-io/conan/pull/9256>`_ . Docs `here <https://github.com/conan-io/docs/pull/2155>`__
- Feature: New `VCVars` generator that generates a `conanvcvars.bat` that activates the Visual Studio Developer Command Prompt. `#9230 <https://github.com/conan-io/conan/pull/9230>`_ . Docs `here <https://github.com/conan-io/docs/pull/2153>`__
- Feature: Skip build helper test and using [conf]. `#9218 <https://github.com/conan-io/conan/pull/9218>`_ . Docs `here <https://github.com/conan-io/docs/pull/2154>`__
- Feature: Implement a new ``requires = "pkg/(alias)"`` syntax to be able to dissambiguate alias requirements and resolve them earlier in the flow, solving some limitations of the previous alias definition. This approach is intended to be the one in Conan 2.0 (issue backported from https://github.com/conan-io/tribe/pull/25). `#9217 <https://github.com/conan-io/conan/pull/9217>`_ . Docs `here <https://github.com/conan-io/docs/pull/2169>`__
- Feature: Introduce the ``-require-override`` argument to define dependency overrides directly on command line. `#9195 <https://github.com/conan-io/conan/pull/9195>`_ . Docs `here <https://github.com/conan-io/docs/pull/2170>`__
- Feature: New `self.win_bash` mechanism to enable running commands in a bash shell in Windows. It works only with the new environment definition from the dependencies (`env_buildinfo` and `run_buildinfo`) as long as the new `AutotoolsToolchain`, `AutotoolsDeps` and `Autotools` build helper. It supports automatic conversion of the environment variables values declared as "path" according to the declared subsystem in the conf `tools.win.bash:subsystem`, that is not being auto-detected anymore. `#9194 <https://github.com/conan-io/conan/pull/9194>`_ . Docs `here <https://github.com/conan-io/docs/pull/2152>`__
- Feature: A unique environment launcher (`conanenv.bat/sh`) is generated to aggregate all the environment generators (`VirtualRunEnv`, `VirtualBuildEnv`, `AutotoolsToolchain` and `AutotoolsDeps`) that had been generated so the user can easily activate all of them with one command. `#9161 <https://github.com/conan-io/conan/pull/9161>`_ . Docs `here <https://github.com/conan-io/docs/pull/2151>`__
- Feature: Use _CMake_ File API. `#9005 <https://github.com/conan-io/conan/pull/9005>`_
- Fix: Add ``bindirs`` definition to ``cmake_layout()``. `#9276 <https://github.com/conan-io/conan/pull/9276>`_
- Fix: Improve error message when ``conan search <ref>`` a package in editable mode. `#9262 <https://github.com/conan-io/conan/pull/9262>`_
- Fix: Add ``options`` to ``conanfile.dependencies`` model. `#9258 <https://github.com/conan-io/conan/pull/9258>`_
- Fix: Fix _CMake_ rejecting library name with special characters. `#9245 <https://github.com/conan-io/conan/pull/9245>`_
- Fix: Use filename `[PKG-NAME]-[COMP-NAME]` for `PkgConfigDeps`. `#9228 <https://github.com/conan-io/conan/pull/9228>`_ . Docs `here <https://github.com/conan-io/docs/pull/2148>`__
- Fix: Saving all the toolchain args information into `conanbuild.conf` instead of json file. `#9225 <https://github.com/conan-io/conan/pull/9225>`_ . Docs `here <https://github.com/conan-io/docs/pull/2156>`__
- Fix: Added warning in the new toolchains (the used in the generate() method) if no build profile is being used. `#9206 <https://github.com/conan-io/conan/pull/9206>`_ . Docs `here <https://github.com/conan-io/docs/pull/2173>`__
- Fix: Implemented check that will raise an error in the `CMakeDeps` generator when using the `build_context_activated`, `build_context_suffix` or `build_context_build_modules` attributes if no build profile is being used. `#9206 <https://github.com/conan-io/conan/pull/9206>`_ . Docs `here <https://github.com/conan-io/docs/pull/2173>`__
- Fix: The`CMakeDeps` generator will check if the targets specified in the `find_package(foo components x y z)` exist instead of checking against an internal variable. Also, this check will be done at the end of the `xxx-config.cmake` so any included `build_module` can declare the needed targets. `#9206 <https://github.com/conan-io/conan/pull/9206>`_ . Docs `here <https://github.com/conan-io/docs/pull/2173>`__
- Fix: Consistent help message for conan profile (sub-command part). `#9204 <https://github.com/conan-io/conan/pull/9204>`_ . Docs `here <https://github.com/conan-io/docs/pull/2171>`__
- Fix: Consistently put short arguments (-a) before long ones (--args). `#9199 <https://github.com/conan-io/conan/pull/9199>`_
- Fix: `CC=clang` `--gcc-toolchain` is now identified as _clang_. `#9198 <https://github.com/conan-io/conan/pull/9198>`_
- Fix: The new `VirtualEnv` generator has been split into `VirtualRunEnv` and `VirtualBuildEnv`. Both are automatically generated as before but only `VirtualBuildEnv` will be activated by default. `#9161 <https://github.com/conan-io/conan/pull/9161>`_ . Docs `here <https://github.com/conan-io/docs/pull/2151>`__
- Bugfix: Fixing ``workspace install`` when conanfile has ``imports()``. `#9281 <https://github.com/conan-io/conan/pull/9281>`_
- Bugfix: Fix QbsProfile toolchain ``qbs.architecture`` KeyError. `#9192 <https://github.com/conan-io/conan/pull/9192>`_
- Bugfix: Do not define CMAKE_GENERATOR_TOOLSET  in CMakeToolchain for Ninja generator, and define it in ``vcvars_ver`` instead. `#9187 <https://github.com/conan-io/conan/pull/9187>`_
- BugFix: ``build_requires`` in host context, like gtest, are being propagated downstream by generators in the ``dependencies`` model. `#9171 <https://github.com/conan-io/conan/pull/9171>`_ . Docs `here <https://github.com/conan-io/docs/pull/2172>`__
- Bugfix: Fix that overridden requirements _"cannot be found in lockfile"_. `#8907 <https://github.com/conan-io/conan/pull/8907>`_

1.38.0 (30-Jun-2021)
--------------------

- Feature: New ``PkgConfigDeps`` generator. `#9152 <https://github.com/conan-io/conan/pull/9152>`_ . Docs `here <https://github.com/conan-io/docs/pull/2133>`__
- Feature: Proposal of jinja2 templates for profiles. `#9147 <https://github.com/conan-io/conan/pull/9147>`_ . Docs `here <https://github.com/conan-io/docs/pull/2138>`__
- Feature: Add support for `CMAKE_CXX_STANDARD_REQUIRED` in _CMakeToolchain_. `#9144 <https://github.com/conan-io/conan/pull/9144>`_
- Feature: Add ``context`` information to :command:`conan info` output both to stdout and json outputs. `#9137 <https://github.com/conan-io/conan/pull/9137>`_ . Docs `here <https://github.com/conan-io/docs/pull/2142>`__
- Feature: Improved the new `AutotoolsToolchain`, `AutotoolsDeps` and `Autotools` build helper. `#9131 <https://github.com/conan-io/conan/pull/9131>`_ . Docs `here <https://github.com/conan-io/docs/pull/2135>`__
- Feature: Initial cross-build support in ``CMakeToolchain`` with definition of ``CMAKE_SYSTEM_NAME``, ``CMAKE_SYSTEM_PROCESSOR`` and ``CMAKE_SYSTEM_VERSION``, deduced from ``self.settings_build`` (only using the 2 profiles) and from new ``[conf]`` items. `#9115 <https://github.com/conan-io/conan/pull/9115>`_ . Docs `here <https://github.com/conan-io/docs/pull/2140>`__
- Feature: Easier access to modify or update context values in ``CMakeToolchain`` blocks. `#9109 <https://github.com/conan-io/conan/pull/9109>`_ . Docs `here <https://github.com/conan-io/docs/pull/2140>`__
- Feature: Provide `[conf]` command line support. `#9103 <https://github.com/conan-io/conan/pull/9103>`_ . Docs `here <https://github.com/conan-io/docs/pull/2124>`__
- Feature: Added support for using server config from a custom location, setting `CONAN_SERVER_HOME` env variable or using `-d` or `--server_dir` flag when launching the server with `conan_server` command. `#9099 <https://github.com/conan-io/conan/pull/9099>`_ . Docs `here <https://github.com/conan-io/docs/pull/2125>`__
- Feature: Support for `CMakeDeps` generator of a new property `"skip_deps_file"` to be declared in the `cpp_info` of a package to skip creating `xxx-config.cmake` files for it, allowing to create "system wrapper" recipes easily. `#9087 <https://github.com/conan-io/conan/pull/9087>`_ . Docs `here <https://github.com/conan-io/docs/pull/2121>`__
- Feature: New ``conanfile.dependencies`` model, using a dict {requirement: ConanFileInterface} to prepare for Conan 2.0. `#9062 <https://github.com/conan-io/conan/pull/9062>`_ . Docs `here <https://github.com/conan-io/docs/pull/2134>`__
- Feature: Allow a explicit ``requires = "pkg..#recipe_revision"`` to update cache revision without ``--update``. `#9058 <https://github.com/conan-io/conan/pull/9058>`_ . Docs `here <https://github.com/conan-io/docs/pull/2143>`__
- Feature: New ``cmake_layout()`` layout helper to define a multi-platform CMake layout that will work for different generators (ninja, xcode, visual, unix), and is multi-config. `#9057 <https://github.com/conan-io/conan/pull/9057>`_ . Docs `here <https://github.com/conan-io/docs/pull/2141>`__
- Feature: The `conan_toolchain.cmake` now includes `xxx_DIR` variables for the dependencies to ease the `find_package` mechanism to locate them. The declaration of these directories is a must when cross-building in OSX where CMake ignores `CMAKE_PREFIX_PATH` and `CMAKE_MODULE_PATH` to look only at the system framework directories. `#9032 <https://github.com/conan-io/conan/pull/9032>`_ . Docs `here <https://github.com/conan-io/docs/pull/2108>`__
- Feature: Provide access in the recipes to the environment declared with the [new environment system](https://docs.conan.io/en/latest/reference/conanfile/tools/env.html). `#9030 <https://github.com/conan-io/conan/pull/9030>`_ . Docs `here <https://github.com/conan-io/docs/pull/2136>`__
- Fix: Fix Bazel build string defines. `#9139 <https://github.com/conan-io/conan/pull/9139>`_
- Fix: Fixed behavior in the `self.folders` feature whereby the sources saved or downloaded inside the `source(self)` were saved at the `self.folders.source` folder. But `self.folders.source` is intended to describe where the sources are instead of forcing where the sources are saved. `#9124 <https://github.com/conan-io/conan/pull/9124>`_ . Docs `here <https://github.com/conan-io/docs/pull/2127>`__
- Fix: Properly generate qbs profile for msvc. `#9122 <https://github.com/conan-io/conan/pull/9122>`_
- Fix: Configuration general.user_home_short works with "None" value. `#9118 <https://github.com/conan-io/conan/pull/9118>`_
- Fix: Avoid ``CMakeToolchain`` to generate OSX and Apple config for non Apple builds. `#9107 <https://github.com/conan-io/conan/pull/9107>`_
- Fix: The new `MesonToolchain` now takes the declared environment variables (`CC`, `CXX`...) from build-requires and profiles to set the variables `c`, `cpp`, `c_ld`, `cpp_ld` etc, into the `conan_meson_native.ini` `#8353 <https://github.com/conan-io/conan/pull/8353>`_ . Docs `here <https://github.com/conan-io/docs/pull/2139>`__
- Fix: Added new `preprocessor_definitions` to new Meson build helper. `#8353 <https://github.com/conan-io/conan/pull/8353>`_ . Docs `here <https://github.com/conan-io/docs/pull/2139>`__
- Fix: The new `MesonToolchain` now allows adjusting any variable before generating the `conan_meson_native.ini` file. `#8353 <https://github.com/conan-io/conan/pull/8353>`_ . Docs `here <https://github.com/conan-io/docs/pull/2139>`__
- Bugfix: Disabled remotes shouldn't fail if not used at all `#9184 <https://github.com/conan-io/conan/pull/9184>`_
- BugFix: ``ConanFileDependencies.build["dep"]`` was retrieving the ``host`` dependency if existing, or failing otherwise, because the default requires was hardcoded to fetch the host (build=False) dependency. `#9148 <https://github.com/conan-io/conan/pull/9148>`_ . Docs `here <https://github.com/conan-io/docs/pull/2134>`__
- Bugfix: Now, `conan profile {show, update, get, remove}` is working fine with new experimental `[conf]` section. `#9114 <https://github.com/conan-io/conan/pull/9114>`_

1.37.2 (14-Jun-2021)
--------------------

- Bugfix: Avoid crash when using ``--lockfile`` with the :command:`conan test` command. `#9089 <https://github.com/conan-io/conan/pull/9089>`_
- Bugfix: The `CMakeDeps` generator variables were named wrongly when a component had the same name as the package. `#9073 <https://github.com/conan-io/conan/pull/9073>`_

1.37.1 (08-Jun-2021)
--------------------

- Fix: Update the experimental ``conan new ... -m=v2_cmake`` template to start using the new ``layout()`` basic info. `#9053 <https://github.com/conan-io/conan/pull/9053>`_
- Fix: Do not fail in ``CMakeDeps`` when there are ``build_requires`` with same name as host requires, unless ``build_context_activated`` is enabled for those and a different suffix has not been defined. `#9046 <https://github.com/conan-io/conan/pull/9046>`_
- Fix: When using the new `self.folders.source` (at `layout(self)` method) the sources (from `export`, `export_sources` and `scm`) are copied to the base source folder and not to the `self.folders.source` that is intended to describe where the sources are after fetching them. `#9043 <https://github.com/conan-io/conan/pull/9043>`_ . Docs `here <https://github.com/conan-io/docs/pull/2117>`__
- BugFix: Do not quote all values and allow integer and macro referencing in ``MSBuildToolchain.preprocessor_definitions`` `#9056 <https://github.com/conan-io/conan/pull/9056>`_
- Bugfix: The new generators like `CMakeDeps` and `CMakeToolchain`write the generated files defaulting to the `install folder` if no `self.folders.generators` is specified in the `layout()` method. `#9050 <https://github.com/conan-io/conan/pull/9050>`_
- Bugfix: The `CMakeToolchain` generator now manages correctly a recipe without `arch` declared in an Apple system. `#9045 <https://github.com/conan-io/conan/pull/9045>`_

1.37.0 (31-May-2021)
--------------------

- Feature: Remove ``CMAKE_SKIP_RPATHS`` by default to True in ``CMakeToolchain``, it is not necessary by default, users can opt-in, and new test validates shared libs will work with ``VirtualEnv`` generator ``conanrunenv``. `#9024 <https://github.com/conan-io/conan/pull/9024>`_ . Docs `here <https://github.com/conan-io/docs/pull/2105>`__
- Feature: simplified ``CMakeToolchain`` with only 1 category of blocks, made ``try-compile`` template code as another block, and reordered blocks so relevant flags for try-compile are taken into account. `#9009 <https://github.com/conan-io/conan/pull/9009>`_ . Docs `here <https://github.com/conan-io/docs/pull/2105>`__
- Feature: Add new default `conancenter` remote for `https://center.conan.io` as first in the list. `#8999 <https://github.com/conan-io/conan/pull/8999>`_ . Docs `here <https://github.com/conan-io/docs/pull/2112>`__
- Feature: Implements a new experimental ``conan.tools.google`` Bazel integration with ``BazelDeps``, ``BazelToolchain`` and ``Bazel``. `#8991 <https://github.com/conan-io/conan/pull/8991>`_ . Docs `here <https://github.com/conan-io/docs/pull/2109>`__
- Feature: Introduced new options for the `CMakeDeps` generator allowing to manage `build_requires` even declaring the same package as a `require` and `build_require` avoiding the collision of the `config` cmake files and enabling to specify which `build_modules` should be included (e.g protobuf issue) `#8985 <https://github.com/conan-io/conan/pull/8985>`_ . Docs `here <https://github.com/conan-io/docs/pull/2104>`__
- Feature: Expand user-agent string to include OS info. `#8947 <https://github.com/conan-io/conan/pull/8947>`_
- Feature: Implement ``build_policy=never`` for :command:`conan export-pkg` packages that cannot be rebuilt with ``--build=xxx``. `#8946 <https://github.com/conan-io/conan/pull/8946>`_ . Docs `here <https://github.com/conan-io/docs/pull/2106>`__
- Feature: Define ``[conf]`` for defining the user toolchain for ``CMakeToolchain``, both for injecting a user toolchain in the ``CMakeToolchain`` generated ``conan_toolchain.cmake`` and for completely replacing ``conan_toolchain.cmake``. `#8945 <https://github.com/conan-io/conan/pull/8945>`_ . Docs `here <https://github.com/conan-io/docs/pull/2105>`__
- Feature: add GCC 11 to _settings.yml_. `#8924 <https://github.com/conan-io/conan/pull/8924>`_
- Feature: Add new `tools.rename()` interface. `#8915 <https://github.com/conan-io/conan/pull/8915>`_ . Docs `here <https://github.com/conan-io/docs/pull/2099>`__
- Feature: Update urlib3 Conan dependency setting version `>=1.25.8` to avoid CVE-2020-7212. `#8914 <https://github.com/conan-io/conan/pull/8914>`_
- Feature: Build-requires can define [conf] for its consumers. `#8895 <https://github.com/conan-io/conan/pull/8895>`_ . Docs `here <https://github.com/conan-io/docs/pull/2107>`__
- Feature: support M1 Catalyst. `#8818 <https://github.com/conan-io/conan/pull/8818>`_
- Feature: New ``conan install <ref> --build-require`` and ``conan create <path> --build-require``  (when not using ``test_package``) arguments to explicitly define that the installed or created package has to be a ``build-require``, receiving the build profile instead of the host one. `#8627 <https://github.com/conan-io/conan/pull/8627>`_ . Docs `here <https://github.com/conan-io/docs/pull/2113>`__
- Feature: Introduced the `layout()` method to the recipe to be able to declare the folder structure both for the local development methods (conan source, conan build...) and in the cache. Also, associated to the folders, cppinfo objects to be used in editable packages and file pattern descriptions to enable "auto packaging". `#8554 <https://github.com/conan-io/conan/pull/8554>`_ . Docs `here <https://github.com/conan-io/docs/pull/2092>`__
- Fix: **CMakeDeps** generator: The transitive requirements for a build_require are not included in the `xxx-config.cmake` files generated. `#9015 <https://github.com/conan-io/conan/pull/9015>`_
- Fix: The `CMakeToolchain` now supports Apple M1 cross-building with a profile without environment declared pointing to the system toolchain. `#9011 <https://github.com/conan-io/conan/pull/9011>`_
- Fix: Set `env_info.DYLD_FRAMEWORK_PATH` correctly. `#8984 <https://github.com/conan-io/conan/pull/8984>`_
- Fix: Fix some typos in the code. `#8977 <https://github.com/conan-io/conan/pull/8977>`_
- Fix: Improve error message when a directory doesn't contain a valid repository. `#8956 <https://github.com/conan-io/conan/pull/8956>`_
- Fix: The `build_modules` defined per generator in `cpp_info` now are rendered properly using the `markdown` generator. `#8942 <https://github.com/conan-io/conan/pull/8942>`_
- Fix: Simplify code access to [conf] variables removing attribute based access. `#8901 <https://github.com/conan-io/conan/pull/8901>`_
- Bugfix: Prevent unintended evil insertions into metadata.json resulted in corrupted package and inability to install. `#9022 <https://github.com/conan-io/conan/pull/9022>`_
- Bugfix: Allow ``MSBuildDeps`` to correctly process packages with dots in the package name. `#9012 <https://github.com/conan-io/conan/pull/9012>`_
- Bugfix: Avoid errors because of ``package_id`` mismatch in lockfiles when using ``compatible_packages`` feature. `#9008 <https://github.com/conan-io/conan/pull/9008>`_
- BugFix: Respect order of declared directories when using components. `#8927 <https://github.com/conan-io/conan/pull/8927>`_
- Bugfix: Raise an exception when response header `Content-type` is different than `application/json` or `application/json; charset=utf-8`. `#8912 <https://github.com/conan-io/conan/pull/8912>`_
- Bugfix: Fix exception in CMakeToolchain when settings remove known compilers. `#8900 <https://github.com/conan-io/conan/pull/8900>`_
- Bugfix: Fix current directory definition in ``vcvars`` commands in new toolchains. `#8899 <https://github.com/conan-io/conan/pull/8899>`_
- Bugfix: AptTool: add repo key before running apt-add-repository. `#8861 <https://github.com/conan-io/conan/pull/8861>`_
- BugFix: Prevent evil insertions into metadata.json resulted in corrupted package and inability to install. `#8532 <https://github.com/conan-io/conan/pull/8532>`_

1.36.0 (28-Apr-2021)
--------------------

- Feature: Add support to ``tools.cmake.CMake`` for Ninja toolchain defined with ``CMakeToolchain``. `#8887 <https://github.com/conan-io/conan/pull/8887>`_
- Feature: The `CMakeDeps` generator will print CMake traces with the declared targets. e.g: `Target declared: 'OpenSSL::Crypto'`. `#8843 <https://github.com/conan-io/conan/pull/8843>`_
- Feature: Add clang 12 support. `#8828 <https://github.com/conan-io/conan/pull/8828>`_
- Feature: List tools and core from profile and _global.conf_. `#8821 <https://github.com/conan-io/conan/pull/8821>`_ . Docs `here <https://github.com/conan-io/docs/pull/2077>`__
- Feature: Add cross-building tests for new AutoTools build helper. `#8819 <https://github.com/conan-io/conan/pull/8819>`_
- Feature: ``CMakeToolchain`` generates a ``conanbuild.json`` file with the generator to be used in the ``CMake`` command line later, so it is not necessary to duplicate logic, and is explicit what generator should be used. `#8815 <https://github.com/conan-io/conan/pull/8815>`_ . Docs `here <https://github.com/conan-io/docs/pull/2079>`__
- Feature: ``CMakeToolchain`` learned to build with different toolsets, down to the minor compiler version, for the ``msvc`` compiler. `#8815 <https://github.com/conan-io/conan/pull/8815>`_ . Docs `here <https://github.com/conan-io/docs/pull/2079>`__
- Feature: Validate checksum and retry download for corrupted downloaded cache files. `#8806 <https://github.com/conan-io/conan/pull/8806>`_
- Feature: ``CMakeToolchain`` defining `CMAKE_GENERATOR_TOOLSET` for msvc version different than the default. `#8800 <https://github.com/conan-io/conan/pull/8800>`_
- Feature: Implement ``test_build_require`` in ``test_package/conanfile.py`` recipes, so build_requires can be tested as such. `#8787 <https://github.com/conan-io/conan/pull/8787>`_ . Docs `here <https://github.com/conan-io/docs/pull/2081>`__
- Feature: Make available the full recipe and package reference to consumers via ``.dependencies``. `#8765 <https://github.com/conan-io/conan/pull/8765>`_
- Feature: New ``CMakeToolchain`` customization and extensibility mechanism with blocks of components instead of inheritance. `#8749 <https://github.com/conan-io/conan/pull/8749>`_ . Docs `here <https://github.com/conan-io/docs/pull/2085>`__
- Feature: Add `set_property` and `get_property` to set properties and access them in generators. Can be set only for a specific generator or as a default value for all of them. `#8727 <https://github.com/conan-io/conan/pull/8727>`_ . Docs `here <https://github.com/conan-io/docs/pull/2082>`__
- Feature: Use `set_property` and `get_property` to support custom defined content in `pkg_config` generator. `#8727 <https://github.com/conan-io/conan/pull/8727>`_ . Docs `here <https://github.com/conan-io/docs/pull/2082>`__
- Feature: Add new property names: `cmake_target_name`, `cmake_file_name`, `pkg_config_name` and `cmake_build_modules` that can be used for multiple generators of the same type allowing also an easier migration of `names`, `filenames` and `build_modules` properties to this model. `#8727 <https://github.com/conan-io/conan/pull/8727>`_ . Docs `here <https://github.com/conan-io/docs/pull/2082>`__
- Feature: Skip package when building all package from sources at once using `--build=!<package>` syntax. `#8483 <https://github.com/conan-io/conan/pull/8483>`_ . Docs `here <https://github.com/conan-io/docs/pull/2023>`__
- Feature: ``CMakeToolchain`` will generate ``conanvcvars.bat`` for Ninja builds for ``msvc``. `#8005 <https://github.com/conan-io/conan/pull/8005>`_
- Fix: Remove ``tools.gnu.MakeToolchain``, superseded by ``tools.gnu.AutotoolsToolchain``. `#8880 <https://github.com/conan-io/conan/pull/8880>`_ . Docs `here <https://github.com/conan-io/docs/pull/2084>`__
- Fix: Allow spaces in the path for new environment files and ``conancvvars.bat`` Visual toolchain file. `#8847 <https://github.com/conan-io/conan/pull/8847>`_
- Fix: Return `deprecated` attribute in :command:`conan inspect` command. `#8832 <https://github.com/conan-io/conan/pull/8832>`_
- Fix: Check if Artifactory url for publishing the build_info has `artifactory` string as the service context and remove from the API url if it doesn't. `#8826 <https://github.com/conan-io/conan/pull/8826>`_
- Fix: Recognize ``Ninja Multi-Config`` as a  CMake multi-configuration generator. `#8814 <https://github.com/conan-io/conan/pull/8814>`_
- Fix: using `CMAKE_CURRENT_LIST_DIR` in `CMakeToolchain` to locate `CMakeDeps` config files. `#8810 <https://github.com/conan-io/conan/pull/8810>`_
- Fix: `config_install_interval` no longer enter in loop when invalid. `#8769 <https://github.com/conan-io/conan/pull/8769>`_ . Docs `here <https://github.com/conan-io/docs/pull/2067>`__
- Fix: Remove multi-config support for ``CMakeDeps`` generator. `#8767 <https://github.com/conan-io/conan/pull/8767>`_ . Docs `here <https://github.com/conan-io/docs/pull/2083>`__
- Fix: Accept relative profile path when folder is on same tree level. `#8685 <https://github.com/conan-io/conan/pull/8685>`_ . Docs `here <https://github.com/conan-io/docs/pull/2049>`__
- Bugfix: Fixed test_package/conanfile.py using ``build_requires`` for a package belonging to a lockfile. `#8793 <https://github.com/conan-io/conan/pull/8793>`_

1.35.2 (19-Apr-2021)
--------------------

- Bugfix: Revert regression that replaces first ``/`` by ``-`` in ``cpp_info.xxxxlinkflags`` in _CMake_ generators because it can break passing objects and other paths that start with ``/``. `#8812 <https://github.com/conan-io/conan/pull/8812>`_

1.35.1 (13-Apr-2021)
--------------------

- Fix: Avoid breaking users calling forbidden private api ``conanfile.__init__``. `#8746 <https://github.com/conan-io/conan/pull/8746>`_
- Bugfix: Fix opensuse SystemPackageTools incorrectly using apt-get when zypper-aptitude. `#8747 <https://github.com/conan-io/conan/pull/8747>`_
- Bugfix: Fix linker flags in cmake (find_package based) generators. `#8740 <https://github.com/conan-io/conan/pull/8740>`_
- Bugfix: Fixed bug in transitive build_requires of MSBuildDeps. `#8734 <https://github.com/conan-io/conan/pull/8734>`_

1.35.0 (30-Mar-2021)
--------------------

- Feature: ``MSBuildDeps`` generator uses new visitor model and handles conditional requirements correctly. `#8733 <https://github.com/conan-io/conan/pull/8733>`_ . Docs `here <https://github.com/conan-io/docs/pull/2052>`__
- Feature: CMake toolchain supports include_guard() feature `#8728 <https://github.com/conan-io/conan/pull/8728>`_
- Feature: New ``conan lock bundle clean-modified`` command. `#8726 <https://github.com/conan-io/conan/pull/8726>`_ . Docs `here <https://github.com/conan-io/docs/pull/2053>`__
- Feature: Use ``conancvvars.bat`` file for Meson toolchain `#8719 <https://github.com/conan-io/conan/pull/8719>`_
- Feature: Allow arbitrary defines in :command:`conan new` templates. `#8718 <https://github.com/conan-io/conan/pull/8718>`_ . Docs `here <https://github.com/conan-io/docs/pull/2051>`__
- Feature: Automatically handle `CONAN_RUN_TESTS` to avoid extra boilerplate. `#8687 <https://github.com/conan-io/conan/pull/8687>`_ . Docs `here <https://github.com/conan-io/docs/pull/2056>`__
- Feature: More fine-grained control (using [conf]) for build parallelization. `#8665 <https://github.com/conan-io/conan/pull/8665>`_ . Docs `here <https://github.com/conan-io/docs/pull/2061>`__
- Feature: Add support for testing with different tools versions. `#8656 <https://github.com/conan-io/conan/pull/8656>`_
- Feature: Add different CMake versions for testing. `#8656 <https://github.com/conan-io/conan/pull/8656>`_
- Feature: Move the definition of CMakeDeps variables to its own file `#8655 <https://github.com/conan-io/conan/pull/8655>`_ . Docs `here <https://github.com/conan-io/docs/pull/2055>`__
- Feature: Added `conan.tools.files.patch` to apply a single patch (new interface for legacy `conans.tools.patch` function. `#8650 <https://github.com/conan-io/conan/pull/8650>`_ . Docs `here <https://github.com/conan-io/docs/pull/2062>`__
- Feature: Added `conan.tools.files.apply_conandata_patches` to apply patches defined in `conandata.yml`. `#8650 <https://github.com/conan-io/conan/pull/8650>`_ . Docs `here <https://github.com/conan-io/docs/pull/2062>`__
- Feature: Allow integers as ``preprocessor_definitions`` in ``CMakeToolchain``. `#8645 <https://github.com/conan-io/conan/pull/8645>`_
- Feature: New ``Environment`` model for recipes and profiles `#8630 <https://github.com/conan-io/conan/pull/8630>`_ . Docs `here <https://github.com/conan-io/docs/pull/2060>`__
- Feature: Do not remove sh from the path in the new CMake helper. `#8625 <https://github.com/conan-io/conan/pull/8625>`_ . Docs `here <https://github.com/conan-io/docs/pull/2055>`__
- Feature: Allow definition of custom Visual Studio version for msvc compiler in MSBuild helpers. `#8603 <https://github.com/conan-io/conan/pull/8603>`_ . Docs `here <https://github.com/conan-io/docs/pull/2054>`__
- Feature: MSBuildToolchain creates conanvcvars.bat containing vcvars command for command line building. `#8603 <https://github.com/conan-io/conan/pull/8603>`_ . Docs `here <https://github.com/conan-io/docs/pull/2054>`__
- Feature: Set `CMAKE_FIND_PACKAGE_PREFER_CONFIG=ON`. `#8599 <https://github.com/conan-io/conan/pull/8599>`_
- Feature: Include the recipe name when constrained settings prevent install. `#8559 <https://github.com/conan-io/conan/pull/8559>`_ . Docs `here <https://github.com/conan-io/docs/pull/2032>`__
- Feature: Create new conan.tools.files for 2.0. `#8550 <https://github.com/conan-io/conan/pull/8550>`_
- Feature: New AutotoolsDeps, AutotoolsToolchain helpers in conan.tools.gnu `#8457 <https://github.com/conan-io/conan/pull/8457>`_ . Docs `here <https://github.com/conan-io/docs/pull/2057>`__
- Feature: Experimental ``conan lock install`` that can install a lockfile in the cache, all the binaries or only the recipes with ``--recipes``, intended for CI flows. `#8021 <https://github.com/conan-io/conan/pull/8021>`_ . Docs `here <https://github.com/conan-io/docs/pull/2053>`__
- Fix: Fix incorrect output of ``default_user`` and ``default_channel`` in ``export``. `#8732 <https://github.com/conan-io/conan/pull/8732>`_
- Fix: remotes not being loaded for the :command:`conan alias` command, which was preventing :command:`conan alias` from working if python_requires is used. `#8704 <https://github.com/conan-io/conan/pull/8704>`_
- Fix: Improve error message for ``lock create`` providing a path instead of full path with filename. `#8695 <https://github.com/conan-io/conan/pull/8695>`_
- Fix: Rename `tools.microsoft:msbuild_verbosity` to `tools.microsoft.msbuild:verbosity` `#8692 <https://github.com/conan-io/conan/pull/8692>`_ . Docs `here <https://github.com/conan-io/docs/pull/2059>`__
- Fix: Simplifications to ``CMakeDeps`` generator to remove legacy code. `#8666 <https://github.com/conan-io/conan/pull/8666>`_
- Fix: Add dirty management in download cache, so interrupted downloads doesn't need a manual cleaning of such download cache. `#8664 <https://github.com/conan-io/conan/pull/8664>`_
- Fix: Build helper qbs install now installs directly into package_folder. `#8660 <https://github.com/conan-io/conan/pull/8660>`_
- Fix: Allow arbitrary template structure. `#8641 <https://github.com/conan-io/conan/pull/8641>`_
- Fix: Restoring the behavior that `exports` and `exports_sources` were case sensitive by default. `#8585 <https://github.com/conan-io/conan/pull/8585>`_
- Fix: Remove default dummy value for iOS XCode signature. `#8576 <https://github.com/conan-io/conan/pull/8576>`_
- Fix: Do not order Settings lists, so error messages are in declared order. `#8573 <https://github.com/conan-io/conan/pull/8573>`_
- BugFix: Command :command:`conan new` accepts short reference with address sign. `#8721 <https://github.com/conan-io/conan/pull/8721>`_
- Bugfix: Fix profile definitions of env-vars per-package using patterns, not only the package name. `#8688 <https://github.com/conan-io/conan/pull/8688>`_
- Bugfix: Preserve the explicit value `None` for SCM attributes if the default is a different value. `#8622 <https://github.com/conan-io/conan/pull/8622>`_
- Bugfix: Properly detect Amazon Linux 2 distro. `#8612 <https://github.com/conan-io/conan/pull/8612>`_
- Bugfix: Fix config install not working when .git* folder is in the path. `#8605 <https://github.com/conan-io/conan/pull/8605>`_
- Bugfix: Fix: Transitive python requires not working with the new syntax. `#8604 <https://github.com/conan-io/conan/pull/8604>`_

1.34.1 (10-Mar-2021)
--------------------

- Fix: Allow ``cmake_find_package_multi`` and ``CMakeDeps`` to be aliases for ``cpp_info.names`` and ``cpp_info.filenames`` to allow easy migration. `#8568 <https://github.com/conan-io/conan/pull/8568>`_
- Bugfix: Restoring the behavior that `exports` and `exports_sources` were case sensitive by default. `#8621 <https://github.com/conan-io/conan/pull/8621>`_
- BugFix: Solved issues with already existing packages appearing in ``conan lock bundle build-order``. `#8579 <https://github.com/conan-io/conan/pull/8579>`_

1.34.0 (26-Feb-2021)
--------------------

- Feature: Add `path` and `repository` properties to conan_build_info v2. `#8436 <https://github.com/conan-io/conan/pull/8436>`_
- Feature: Setting _conan_ as name for `buildAgent` in `conan_build_info`. `#8433 <https://github.com/conan-io/conan/pull/8433>`_
- Feature: Using actual conan version in version for `buildAgent` in `conan_build_info` instead of 1.X. `#8433 <https://github.com/conan-io/conan/pull/8433>`_
- Feature: Add `type` _conan_ to Conan build info modules. `#8433 <https://github.com/conan-io/conan/pull/8433>`_
- Feature: Add ``scm`` output in :command:`conan info` command. `#8380 <https://github.com/conan-io/conan/pull/8380>`_
- Feature: Forked ``cmake_find_package_multi`` into ``CMakeDeps``, to allow evolution without breaking. `#8371 <https://github.com/conan-io/conan/pull/8371>`_
- Feature: Use built-in retries in requests lib to retry http requests with _5xx_ response code. `#8352 <https://github.com/conan-io/conan/pull/8352>`_
- Feature: New lockfile "bundle" feature that can integrate different lockfiles for different configurations and different graphs into a single lockfile bundle that can be used to vastly optimize CI (specially for multiple products), implementing bundle build-order and bundle update operations. `#8344 <https://github.com/conan-io/conan/pull/8344>`_ . Docs `here <https://github.com/conan-io/docs/pull/2030>`__
- Fix: Renamed generator `QbsToolchain` to `QbsProfile`. `#8537 <https://github.com/conan-io/conan/pull/8537>`_ . Docs `here <https://github.com/conan-io/docs/pull/2027>`__
- Fix: Renamed default filename of _QbsProfile_ generated file to _conan_toolchain_profile_.qbs. `#8537 <https://github.com/conan-io/conan/pull/8537>`_ . Docs `here <https://github.com/conan-io/docs/pull/2027>`__
- Fix: Renamed Qbs attribute `use_toolchain_profile` to `profile`. `#8537 <https://github.com/conan-io/conan/pull/8537>`_ . Docs `here <https://github.com/conan-io/docs/pull/2027>`__
- Fix: Remove extra spaces in flags and colons in path variables. `#8496 <https://github.com/conan-io/conan/pull/8496>`_
- Fix: `conan_v2_error` if `scm_to_conandata` is not enabled. `#8447 <https://github.com/conan-io/conan/pull/8447>`_
- Fix: `CONAN_V2_MODE` env-var does not longer alter behavior, only raises errors for Conan 2.0 incompatibilities `#8399 <https://github.com/conan-io/conan/pull/8399>`_ . Docs `here <https://github.com/conan-io/docs/pull/2031>`__
- Fix: meson : Add target and jobs arguments. `#8384 <https://github.com/conan-io/conan/pull/8384>`_ . Docs `here <https://github.com/conan-io/docs/pull/2011>`__
- Fix: Set `qbs.targetPlatform` with qbs toolchain. `#8372 <https://github.com/conan-io/conan/pull/8372>`_
- Fix: Remove warnings for old toolchains imports and ``generate_toolchain_files()`` calls (use new imports and ``generate()`` calls. `#8361 <https://github.com/conan-io/conan/pull/8361>`_
- BugFix: Improve `tools.unix_path` for Cygwin. `#8509 <https://github.com/conan-io/conan/pull/8509>`_
- BugFix: Allow `run_in_windows_bash` in MSYS/Cygwin. `#8506 <https://github.com/conan-io/conan/pull/8506>`_
- BugFix: Add some sanity check to avoid a vague error for custom architectures. `#8502 <https://github.com/conan-io/conan/pull/8502>`_
- BugFix: Fix Apple M1 detection. `#8501 <https://github.com/conan-io/conan/pull/8501>`_
- Bugfix: Fix repeated ``build_requires``, including conflicting versions in profile composition or inclusion that repeats ``[build_requires]`` values. `#8463 <https://github.com/conan-io/conan/pull/8463>`_
- Bugfix: Fixing a `CMakeDeps` bug with components, not finding the _conan_macros.cmake_ file. `#8445 <https://github.com/conan-io/conan/pull/8445>`_
- Bugfix: Fix exit code for `conan_build_info`. `#8408 <https://github.com/conan-io/conan/pull/8408>`_

1.33.1 (02-Feb-2021)
--------------------

- Fix: Rename _conan.cfg_ to _global.conf_. `#8422 <https://github.com/conan-io/conan/pull/8422>`_ . Docs `here <https://github.com/conan-io/docs/pull/2008>`__
- Fix: Make CMakeDeps generator available in declarative mode ``generators = "CMakeDeps"`` `#8416 <https://github.com/conan-io/conan/pull/8416>`_
- Fix: Make the new Macos subsystem Catalyst lowercase to be consistent with existing subsystems. `#8389 <https://github.com/conan-io/conan/pull/8389>`_ . Docs `here <https://github.com/conan-io/docs/pull/2009>`__
- BugFix: Fix Apple Catalyst flags. `#8389 <https://github.com/conan-io/conan/pull/8389>`_ . Docs `here <https://github.com/conan-io/docs/pull/2009>`__

1.33.0 (20-Jan-2021)
--------------------

- Feature: Introducing a new ``[conf]`` section in profiles that allows a more systematic configuration management for recipes and helpers (build helpers, toolchains). Introducing a new ``conan_conf.txt`` cache configuration file that contains configuration definition with the same syntax as in profiles. `#8266 <https://github.com/conan-io/conan/pull/8266>`_ . Docs `here <https://github.com/conan-io/docs/pull/1993>`__
- Feature: Add Apple Catalyst support (as new os.subsystem) `#8264 <https://github.com/conan-io/conan/pull/8264>`_ . Docs `here <https://github.com/conan-io/docs/pull/1983>`__
- Feature: Add os.sdk sub-settings for Apple `#8263 <https://github.com/conan-io/conan/pull/8263>`_ . Docs `here <https://github.com/conan-io/docs/pull/1981>`__
- Feature: Provide support for ``msvc`` compiler in ``MSBuild`` tools `#8238 <https://github.com/conan-io/conan/pull/8238>`_ . Docs `here <https://github.com/conan-io/docs/pull/1991>`__
- Feature: Specify build modules by the generator in `cpp_info`. Added backwards compatibility for `*.cmake` build modules added at global scope, but not for other file extensions. `#8232 <https://github.com/conan-io/conan/pull/8232>`_ . Docs `here <https://github.com/conan-io/docs/pull/1986>`__
- Feature: The `tools.get`, `tools.unzip` and `tools.untargz` now accept a new argument `strip_root=True` to unzip moving all the files to the parent folder when all of them belongs to a single folder. `#8208 <https://github.com/conan-io/conan/pull/8208>`_ . Docs `here <https://github.com/conan-io/docs/pull/1967>`__
- Feature: Add new ``msvc`` compiler setting and preliminary support in ``conan.tools.cmake`` generator and toolchain. `#8201 <https://github.com/conan-io/conan/pull/8201>`_ . Docs `here <https://github.com/conan-io/docs/pull/1991>`__
- Feature: ``CMakeDeps`` now takes values for configurations from ``settings.yml``. `#8194 <https://github.com/conan-io/conan/pull/8194>`_ . Docs `here <https://github.com/conan-io/docs/pull/1992>`__
- Feature: Implement ``ConanXXXRootFolder`` in ``MSBuildDeps`` generator. `#8177 <https://github.com/conan-io/conan/pull/8177>`_
- Feature: Add _Meson_ build helper. `#8147 <https://github.com/conan-io/conan/pull/8147>`_ . Docs `here <https://github.com/conan-io/docs/pull/1980>`__
- Feature: Add `QbsToolchain` and a Qbs build helper class (currently working for Mcus, not for Android or iOS). `#8125 <https://github.com/conan-io/conan/pull/8125>`_ . Docs `here <https://github.com/conan-io/docs/pull/1978>`__
- Feature: Add e2k (elbrus) architectures and mcst-lcc compiler `#8032 <https://github.com/conan-io/conan/pull/8032>`_ . Docs `here <https://github.com/conan-io/docs/pull/1982>`__
- Feature: New ``CMakeDeps`` generator (at the moment is the ``cmake_find_package_multi``, that allows custom configurations, like ``ReleaseShared``. `#8024 <https://github.com/conan-io/conan/pull/8024>`_ . Docs `here <https://github.com/conan-io/docs/pull/1992>`__
- Feature: Allow ``MSBuildToolchain`` custom configurations in ``generate()`` method. `#7754 <https://github.com/conan-io/conan/pull/7754>`_ . Docs `here <https://github.com/conan-io/docs/pull/1957>`__
- Fix: Fixed help message in command `conan remove --outdated` with reference or pattern `#8350 <https://github.com/conan-io/conan/pull/8350>`_ . Docs `here <https://github.com/conan-io/docs/pull/1988>`__
- Fix: Do not define CMAKE_GENERATOR_PLATFORM and CMAKE_GENERATOR_TOOLSET in the ``CMakeToolchain`` file unless the CMake generator is "Visual Studio". Fix https://github.com/conan-io/conan/issues/7485 `#8333 <https://github.com/conan-io/conan/pull/8333>`_
- Fix: Remove spurious '-find' argument to XCodes xcrun tool. `#8329 <https://github.com/conan-io/conan/pull/8329>`_
- Fix: Update pylint plugin, some fields are now available in the base `ConanFile`. `#8320 <https://github.com/conan-io/conan/pull/8320>`_
- Fix: Remove PyJWT deprecation warning by adding explicitly ``algorithms`` argument. `#8267 <https://github.com/conan-io/conan/pull/8267>`_
- Fix: CMake's generator name for Visual Studio compiler uses only the major version. `#8257 <https://github.com/conan-io/conan/pull/8257>`_
- Fix: Remove nosetests support, now using pytest for the test suite. `#8253 <https://github.com/conan-io/conan/pull/8253>`_
- Fix: Remove `CMAKE_PROJECT_INCLUDE` in `CMakeToolchain`, no longer necessary as the MSVC runtime can be defined with a generator expression in the toolchain. `#8251 <https://github.com/conan-io/conan/pull/8251>`_
- Fix: Temporarily allow ``cmake_paths`` generator for ``CMakeToolchain``, to allow start using the toolchain for users that depend on that generator. `#8230 <https://github.com/conan-io/conan/pull/8230>`_
- Fix: Let CMake generator generate code for checking against "ClangCL" msvc toolset. `#8218 <https://github.com/conan-io/conan/pull/8218>`_
- Fix: Include ``build_requires`` in the global ``conandeps.props`` file generated by MSBuildDeps. `#8186 <https://github.com/conan-io/conan/pull/8186>`_
- Fix: Change `MSBuildDeps` file ``conan_deps.props`` to ``conandeps.props`` to avoid collision with a package named "deps". `#8186 <https://github.com/conan-io/conan/pull/8186>`_
- Fix: Throw error when the recipe description is not a string. `#8143 <https://github.com/conan-io/conan/pull/8143>`_
- Fix: Inject build modules after CMake targets are created `#8130 <https://github.com/conan-io/conan/pull/8130>`_ . Docs `here <https://github.com/conan-io/docs/pull/1944>`__
- Fix: Define ``package_folder`` in the ``test_package`` folder (defaulting to "package"), so the test recipe can execute ``cmake.install()`` in its ``build()`` method. `#8117 <https://github.com/conan-io/conan/pull/8117>`_
- Fix: Remove the downloaded file if it doesn't satisfy provided checksums (modifies `tools.download`). `#8116 <https://github.com/conan-io/conan/pull/8116>`_ . Docs `here <https://github.com/conan-io/docs/pull/1979>`__
- Bugfix: Solved ``assert node.package_id != PACKAGE_ID_UNKNOWN`` assertion that happened when using ``build_requires`` that also exist in ``requires``, and using ``package_revision_mode`` and ``full_transitive_package_id=1`` `#8358 <https://github.com/conan-io/conan/pull/8358>`_
- BugFix: Fix SCM user and password by making them url-encoded `#8355 <https://github.com/conan-io/conan/pull/8355>`_
- Bugfix: Fix bug in definition of ``ROOT`` variables in ``MakeGenerator``. `#8301 <https://github.com/conan-io/conan/pull/8301>`_
- BugFix: fix `-j` being passed to _NMake_ in `AutotoolsBuildEnvironment`. `#8285 <https://github.com/conan-io/conan/pull/8285>`_
- BugFix: Fix per-package settings exact match for packages without user/channel. `#8281 <https://github.com/conan-io/conan/pull/8281>`_
- BugFix: Fix detected_architecture() for Apple M1, mapping to ``armv8`` (from returned ``arm64``). `#8262 <https://github.com/conan-io/conan/pull/8262>`_
- Bugfix: Make prompt names unique when using multiple virtualenv scripts in Powershell. `#8228 <https://github.com/conan-io/conan/pull/8228>`_
- Bugfix: Fix when _conandata.yml_ is empty and `scm_to_conandata` is enabled `#8215 <https://github.com/conan-io/conan/pull/8215>`_
- Bugfix: Removed a reference to deprecated `FlagsForFile` function in place of current `Settings` function. `#8167 <https://github.com/conan-io/conan/pull/8167>`_
- Bugfix: Add test for AutoToolsBuildEnvironment on Apple platforms `#8118 <https://github.com/conan-io/conan/pull/8118>`_
- Bugfix: Change the `rpath_flags` flag to always use the comma separator instead of "=", because the current behaviour causes linker error messages when attempting to cross-compile to Mac OS, and the comma separator is accepted everywhere. `#7716 <https://github.com/conan-io/conan/pull/7716>`_

1.32.1 (15-Dec-2020)
--------------------

- Bugfix: Avoid conflict of user custom generators names with new generators. `#8183 <https://github.com/conan-io/conan/pull/8183>`_
- Bugfix: Fix errors when using ``conan info --paths`` and ``short_paths=True`` in Windows, due to creation of empty folders in the short-paths storage. `#8181 <https://github.com/conan-io/conan/pull/8181>`_
- Bugfix: ``conan new <pkg-name>/version -t`` wrong include when not using ``-s`` (using the hardcoded git repo). `#8175 <https://github.com/conan-io/conan/pull/8175>`_
- Bugfix: Fix ``excludes`` pattern case-insensitive in non Windows platforms. `#8155 <https://github.com/conan-io/conan/pull/8155>`_
- Bugfix: Enabling set_name, set_version for lockfile roo not location. `#8151 <https://github.com/conan-io/conan/pull/8151>`_

1.32.0 (03-Dec-2020)
--------------------

- Feature: Generate `<pkgname>-config.cmake` files for lowercase packages to improve case compatibility. `#8129 <https://github.com/conan-io/conan/pull/8129>`_ . Docs `here <https://github.com/conan-io/docs/pull/1945>`__
- Feature: Add meson cross-build toolchain. `#8111 <https://github.com/conan-io/conan/pull/8111>`_
- Feature: Temporary acquire write permissions in `replace_in_file`. `#8107 <https://github.com/conan-io/conan/pull/8107>`_
- Feature: Update :command:`conan new` to latest guidelines. `#8106 <https://github.com/conan-io/conan/pull/8106>`_
- Feature: Deprecate experimental ``toolchain()`` in favor of more generic ``generate()`` method. Deprecate toolchains ``write_toolchain_files()`` to new ``generate()`` method. `#8101 <https://github.com/conan-io/conan/pull/8101>`_ . Docs `here <https://github.com/conan-io/docs/pull/1940>`__
- Feature: Move the ``CMakeToolchain`` and new ``CMake`` experimental helpers to the new ``from conan.tools.cmake`` import. `#8096 <https://github.com/conan-io/conan/pull/8096>`_ . Docs `here <https://github.com/conan-io/docs/pull/1940>`__
- Feature: Move the ``MSBuildToolchain`` and new ``MSBuild`` experimental helpers to the new ``from conan.tools.microsoft`` import. `#8096 <https://github.com/conan-io/conan/pull/8096>`_ . Docs `here <https://github.com/conan-io/docs/pull/1940>`__
- Feature: Move the ``MakeToolchain`` experimental helper to the new ``from conan.tools.gnu`` import. `#8096 <https://github.com/conan-io/conan/pull/8096>`_ . Docs `here <https://github.com/conan-io/docs/pull/1940>`__
- Feature: Add ``conan remote list_ref --no-remote`` to list recipes without a remote defined. `#8094 <https://github.com/conan-io/conan/pull/8094>`_ . Docs `here <https://github.com/conan-io/docs/pull/1936>`__
- Feature: Add ``conan remote list_pref --no-remote`` to list packages without a remote defined. `#8094 <https://github.com/conan-io/conan/pull/8094>`_ . Docs `here <https://github.com/conan-io/docs/pull/1936>`__
- Feature: Add ``--lockfile-node-id`` argument to ``conan install --lockfile`` so it can target different packages with same reference (different binary, this can happen with private requirements). `#8077 <https://github.com/conan-io/conan/pull/8077>`_ . Docs `here <https://github.com/conan-io/docs/pull/1938>`__
- Feature: Proof that ``python_requires`` can be used (as a workaround) to affect the ``package_id`` of consumers of ``build_requires`` that otherwise will not be rebuilt based on changes. `#8076 <https://github.com/conan-io/conan/pull/8076>`_ . Docs `here <https://github.com/conan-io/docs/pull/1925>`__
- Feature: Introduce configuration ``general.keep_python_files`` to allow packaging of Python .pyc files. `#8070 <https://github.com/conan-io/conan/pull/8070>`_ . Docs `here <https://github.com/conan-io/docs/pull/1942>`__
- Feature: Tests for toolchains and Intel compiler. `#8062 <https://github.com/conan-io/conan/pull/8062>`_
- Feature: Add recipe and package revision to show a complete Conan reference when generating the `build_info --v2` id fields. `#8055 <https://github.com/conan-io/conan/pull/8055>`_
- Feature: Introduce a new `BINARY_INVALID` mode for more flexible definition and management of invalid configurations. `#8053 <https://github.com/conan-io/conan/pull/8053>`_ . Docs `here <https://github.com/conan-io/docs/pull/1947>`__
- Feature: Add headers with settings and options to HTTP GET requests when searching for packages. `#8046 <https://github.com/conan-io/conan/pull/8046>`_
- Feature: Preliminary experimental support for toolchains with CMake + Visual + Ninja. `#8034 <https://github.com/conan-io/conan/pull/8034>`_
- Feature: Allow (experimental) custom configuration of the ``msbuild`` generator. `#8014 <https://github.com/conan-io/conan/pull/8014>`_
- Feature: Rename ``msbuild`` generator to ``MSBuildDeps`` and use the new ``generate()`` method. `#8014 <https://github.com/conan-io/conan/pull/8014>`_
- Feature: Make the ``conan new bye/0.1 -s -t`` to provide variable filenames and messages that include the package name and version, instead of a hardcoded "hello" one. `#7989 <https://github.com/conan-io/conan/pull/7989>`_
- Feature: Tagged tests and created a `conftest.py` to run the tests with `pytest` skipping the tests using not available tools (cmake, visual studio...). `#7975 <https://github.com/conan-io/conan/pull/7975>`_
- Feature: Provide correct `--pure_c` implementation to :command:`conan new`. `#7947 <https://github.com/conan-io/conan/pull/7947>`_
- Feature: System package tools can install a list of different packages. `#7779 <https://github.com/conan-io/conan/pull/7779>`_ . Docs `here <https://github.com/conan-io/docs/pull/1937>`__
- Feature: meson toolchain `#7662 <https://github.com/conan-io/conan/pull/7662>`_ . Docs `here <https://github.com/conan-io/docs/pull/1943>`__
- Feature: Add Conan package name and version to Visual Studio generator properties file. `#7645 <https://github.com/conan-io/conan/pull/7645>`_
- Fix: Remove ``__init__.py`` in the root of the repo, which was useless, without a purpose, but caused issues with other projects importing Conan Python code. `#8132 <https://github.com/conan-io/conan/pull/8132>`_
- Fix: Make variables defined in ``CMakeToolchain`` cache variables, so they can define directly values defined in ``CMakeLists.txt``. `#8124 <https://github.com/conan-io/conan/pull/8124>`_
- Fix: Remove cryptography, pyopenssl and idna from OSX requirements in Python. `#8075 <https://github.com/conan-io/conan/pull/8075>`_
- Fix: Rename the generated file of ``MSBuildToolchain`` to ``conantoolchain.props`` so it doesn't collide with a potential ``toolchain`` package name and the ``msbuild`` generator. `#8073 <https://github.com/conan-io/conan/pull/8073>`_ . Docs `here <https://github.com/conan-io/docs/pull/1941>`__
- Fix: Avoid warning in ``msbuild`` generator importing multiple times the same .props file due to transitive dependencies. `#8072 <https://github.com/conan-io/conan/pull/8072>`_
- Fix: Set username or password individually in git SCM with ssh. `#8016 <https://github.com/conan-io/conan/pull/8016>`_
- Fix: When using lockfiles, allow ``config_options`` and ``configure`` to compute different options as long as the final evaluated values match the locked ones. `#7993 <https://github.com/conan-io/conan/pull/7993>`_
- Fix: Make the ``conan new --pure_c`` pure C template to remove both ``compiler.libcxx`` and ``compiler.cppstd`` settings, as described in the docs. `#7989 <https://github.com/conan-io/conan/pull/7989>`_
- BugFix: Fix linkage to a same global target of different package components in `cmake_find_package/_multi` generators. `#8114 <https://github.com/conan-io/conan/pull/8114>`_ . Docs `here <https://github.com/conan-io/docs/pull/1946>`__
- Bugfix: Solve ``os.rename`` crash when using ``short_paths`` with a short path storage located in another Windows drive unit. `#8103 <https://github.com/conan-io/conan/pull/8103>`_
- BugFix: Allow lockfiles to be relaxed with the `--build` argument. `#8054 <https://github.com/conan-io/conan/pull/8054>`_ . Docs `here <https://github.com/conan-io/docs/pull/1939>`__
- Bugfix: Append existing ``LocalDebuggerEnvironment`` in ``msbuild`` generator. `#8040 <https://github.com/conan-io/conan/pull/8040>`_
- Bugfix: Remove correctly short-paths folders in Windows. `#7986 <https://github.com/conan-io/conan/pull/7986>`_

1.31.4 (25-Nov-2020)
--------------------

- Feature: Add new `CONAN_CMAKE_SYSROOT` environment variable to enable the definition of sysroot from environment, without abusing `CONAN_CMAKE_FIND_ROOT_PATH`. `#8097 <https://github.com/conan-io/conan/pull/8097>`_ . Docs `here <https://github.com/conan-io/docs/pull/1926>`__
- Bugfix: remove definition of sysroot from `CONAN_CMAKE_FIND_ROOT_PATH`. `#8097 <https://github.com/conan-io/conan/pull/8097>`_ . Docs `here <https://github.com/conan-io/docs/pull/1926>`__
- Bugfix: Bugfix: Solve os.rename crash when using short_paths with a short path storage located in another Windows drive unit. Ported from: `#8103 <https://github.com/conan-io/conan/pull/8103>`_

1.31.3 (17-Nov-2020)
--------------------

- Bugfix: Fix addition of CMAKE_SYSTEM_NAME for SunOS and AIX 64->32 bits builds `#8059 <https://github.com/conan-io/conan/pull/8059>`_

1.31.2 (11-Nov-2020)
--------------------

- Bugfix: Recent ``liburl3`` 1.26 library updates is breaking the constraints in Conan ``requirements.txt``  as ``requests`` 2.24 has a limitation for ``liburl3``. This PR constrains ``liburl3`` version to be less than 1.26, so it does not break with requests 2.24. `#8042 <https://github.com/conan-io/conan/pull/8042>`_

1.31.1 (10-Nov-2020)
--------------------

- Fix: Bump _cryptography_ dependency in MacOS to equal or later than 3.2. `#7962 <https://github.com/conan-io/conan/pull/7962>`_
- Bugfix: Fix a problem with the ``init()`` function not being called when the recipe loader uses some cached data, which can happen when using lockfiles and with ``python_requires``. `#8018 <https://github.com/conan-io/conan/pull/8018>`_
- Bugfix: Fixed ``self.copy()`` incorrectly handling ``ignore_case``. `#8009 <https://github.com/conan-io/conan/pull/8009>`_
- Bugfix: Fixed wrong ``ignore_case`` default in ``[imports]`` section of *conanfile.txt*. `#8009 <https://github.com/conan-io/conan/pull/8009>`_
- Bugfix: Do not try to encrypt a `None` value when using `CONAN_LOGIN_ENCRYPTION_KEY` environment variable. `#8004 <https://github.com/conan-io/conan/pull/8004>`_

1.31.0 (30-Oct-2020)
--------------------

- Feature: Add argument `conanfile` to `pre_download_package` and `post_download_package` hook functions. `#7968 <https://github.com/conan-io/conan/pull/7968>`_ . Docs `here <https://github.com/conan-io/docs/pull/1905>`__
- Feature: Add `CONAN_LOGIN_ENCRYPTION_KEY` environment variable to obfuscate stored auth token. `#7958 <https://github.com/conan-io/conan/pull/7958>`_ . Docs `here <https://github.com/conan-io/docs/pull/1903>`__
- Feature: Use profile to filter results in the :command:`conan search` HTML output. `#7956 <https://github.com/conan-io/conan/pull/7956>`_
- Feature: Changed recommended way to launch test suite, with pytest over nosetests. `#7952 <https://github.com/conan-io/conan/pull/7952>`_
- Feature: Provide a ``MSBuildCmd`` helper class that encapsulates calling MSBuild. `#7941 <https://github.com/conan-io/conan/pull/7941>`_ . Docs `here <https://github.com/conan-io/docs/pull/1907>`__
- Feature: Download and keep the ``conan_export.tgz`` and ``conan_source.tgz`` in the cache, so they are not affected by different Operating Systems compression and de-compression and uploading is way more efficient. `#7938 <https://github.com/conan-io/conan/pull/7938>`_
- Feature: Add `provides` and `deprecated` fields to :command:`conan info` output `#7916 <https://github.com/conan-io/conan/pull/7916>`_
- Feature: Including package revision information in output from :command:`conan info` (when revisions are enabled). `#7890 <https://github.com/conan-io/conan/pull/7890>`_
- Feature: Download and keep the conan_package.tgz in the cache, so they are not affected by different Operating Systems compression and de-compression and uploading is way more efficient. `#7886 <https://github.com/conan-io/conan/pull/7886>`_
- Feature: Add POC on a toolchain for iOS (using CMake XCode generator). `#7855 <https://github.com/conan-io/conan/pull/7855>`_ . Docs `here <https://github.com/conan-io/docs/pull/1906>`__
- Feature: Add POC on a toolchain for Android (using CMake provided modules). `#7843 <https://github.com/conan-io/conan/pull/7843>`_ . Docs `here <https://github.com/conan-io/docs/pull/1902>`__
- Feature: Allow ``conan config install`` of a single file `#7840 <https://github.com/conan-io/conan/pull/7840>`_ . Docs `here <https://github.com/conan-io/docs/pull/1908>`__
- Feature: Use Python loggers for Conan output in cli 2.0. `#7502 <https://github.com/conan-io/conan/pull/7502>`_
- Fix: Improve permission error message when migrating cache folder. `#7966 <https://github.com/conan-io/conan/pull/7966>`_
- Fix: Make per-package settings definition complete the existing settings values, not requiring a complete redefinition. `#7953 <https://github.com/conan-io/conan/pull/7953>`_
- Fix: Avoid unnecessary extra loading of *conan.conf* file in the version migrations check. `#7949 <https://github.com/conan-io/conan/pull/7949>`_
- Fix: Simplified MakeToolchain to remove things that were not checked by tests or unused. `#7942 <https://github.com/conan-io/conan/pull/7942>`_
- Fix: displayed message when settings of the recipe are constrained. `#7930 <https://github.com/conan-io/conan/pull/7930>`_ . Docs `here <https://github.com/conan-io/docs/pull/1890>`__
- Fix: Set `CMAKE_SYSTEM_NAME` set to `iOS`, `tvOS` or `watchOS` or `Darwin` depending on the CMake version. `#7924 <https://github.com/conan-io/conan/pull/7924>`_
- Fix: Remove duplicate entries while modifying PATH-like environment variables internally. Especially important for Windows where system PATH size is limited by 8192 charachers (when using cmd.exe). `#7891 <https://github.com/conan-io/conan/pull/7891>`_
- Fix: Make default behaviour explicit in search help output. `#7877 <https://github.com/conan-io/conan/pull/7877>`_ . Docs `here <https://github.com/conan-io/docs/pull/1884>`__
- Fix: Automatically add OSX deployment flags in ``AutootoolsBuildEnvironment`` with the value of ``os_version``, unless the values are already defined in environment variables `CFLAGS` or `CXXFLAGS`. `#7862 <https://github.com/conan-io/conan/pull/7862>`_
- Fix: Remove toolset variability from the ``msbuild`` generator and ``MSBuildToolchain``. `#7825 <https://github.com/conan-io/conan/pull/7825>`_
- Fix: Component requirement checking now properly handles private and override requirements. `#7585 <https://github.com/conan-io/conan/pull/7585>`_
- Bugfix: Set default storage_folder to .conan/data in case if storage_path entry fails to be defined by conan.conf. `#7910 <https://github.com/conan-io/conan/pull/7910>`_
- Bugfix: Fix regression in self.run(output=xxxx) that have a write() method but do not wrap a stream. `#7905 <https://github.com/conan-io/conan/pull/7905>`_
- Bugfix: Fix local flow (conan install + build) support for ``cpp_info.names`` and ``cpp_info.filenames``. `#7867 <https://github.com/conan-io/conan/pull/7867>`_
- Bugfix: Fix ``inspect --remote`` forcing to retrieve the remote for evaluation, overwriting what is in the local cache. `#7749 <https://github.com/conan-io/conan/pull/7749>`_
- Bugfix: Copy symbolic links to directory with deploy generator. `#7655 <https://github.com/conan-io/conan/pull/7655>`_ . Docs `here <https://github.com/conan-io/docs/pull/1830>`__

1.30.2 (15-Oct-2020)
--------------------

- Feature: Supports Clang 11. `#7871 <https://github.com/conan-io/conan/pull/7871>`_ . Docs `here <https://github.com/conan-io/docs/pull/1883>`__
- Bugfix: Fix regression https://github.com/conan-io/conan/issues/7856, ``imports`` failing to match subfolders in Windows due to backslash differences. `#7861 <https://github.com/conan-io/conan/pull/7861>`_
- Bugfix: Allow defining new options values when creating a new lockfile from an existing base lockfile. `#7859 <https://github.com/conan-io/conan/pull/7859>`_

1.30.1 (09-Oct-2020)
--------------------

- Fix: Use quotes around the install path, it can contain spaces. `#7842 <https://github.com/conan-io/conan/pull/7842>`_
- Fix: prefix intel functions with ``intel_`` because they are now exposed via tools. Fixes https://github.com/conan-io/conan/issues/7820. `#7821 <https://github.com/conan-io/conan/pull/7821>`_ . Docs `here <https://github.com/conan-io/docs/pull/1875>`__
- Bugfix: Fix regression introduced in 1.30 (https://github.com/conan-io/conan/pull/7673), with incorrect matches of user/channel for version ranges. `#7847 <https://github.com/conan-io/conan/pull/7847>`_
- Bugfix: Fix ``CMakeToolchain`` with multiple variables definitions. `#7833 <https://github.com/conan-io/conan/pull/7833>`_
- Bugfix: Check comparing the host and the build architecture to decide if cross building and set `CMAKE_SYSTEM_NAME` in the ``CMake`` build helper. `#7827 <https://github.com/conan-io/conan/pull/7827>`_

1.30.0 (05-Oct-2020)
--------------------

- Feature: Implement real detection of ``compiler.libcxx`` value for ``gcc`` compiler. Only enabled in `CONAN_V2_MODE`, otherwise it would be breaking. `#7776 <https://github.com/conan-io/conan/pull/7776>`_
- Feature: Added [Depends](https://doc.qt.io/qbs/qml-qbslanguageitems-depends.html) items for every public dependency of conanfiles requires/dependencies. `#7729 <https://github.com/conan-io/conan/pull/7729>`_ . Docs `here <https://github.com/conan-io/docs/pull/1847>`__
- Feature: Instructions on how to run conan tests against a real Artifactory server. `#7697 <https://github.com/conan-io/conan/pull/7697>`_
- Feature: List `cpp_info.names` and `cpp_info.filenames` in JSON and Markdown generator. `#7690 <https://github.com/conan-io/conan/pull/7690>`_ . Docs `here <https://github.com/conan-io/docs/pull/1844>`__
- Feature: Add information about components to `markdown` generator. `#7677 <https://github.com/conan-io/conan/pull/7677>`_
- Feature: New experimental ``MSBuildToolchain`` to generate ``conan_toolchain.props`` files (it is multi-config, will generate one specific toolchain file per configuration) for more transparent integration and better developer experience with Visual Studio. `#7674 <https://github.com/conan-io/conan/pull/7674>`_ . Docs `here <https://github.com/conan-io/docs/pull/1865>`__
- Feature: Allow packages that do not declare components to depend on other packages components and manage transitivity correctly, with the new ``self.cpp_info.requires`` attribute. `#7644 <https://github.com/conan-io/conan/pull/7644>`_ . Docs `here <https://github.com/conan-io/docs/pull/1864>`__
- Feature: Add MacOS 11 ("Big Sur") support. `#7601 <https://github.com/conan-io/conan/pull/7601>`_ . Docs `here <https://github.com/conan-io/docs/pull/1819>`__
- Feature: Expose intel_installation_path, compilervars, compilervars_dict, and compilervars_command under tools module in order to support usage of the intel compiler. `#7572 <https://github.com/conan-io/conan/pull/7572>`_ . Docs `here <https://github.com/conan-io/docs/pull/1815>`__
- Feature: Allow user-defined generators to be installed and used from the Conan cache. `#7527 <https://github.com/conan-io/conan/pull/7527>`_ . Docs `here <https://github.com/conan-io/docs/pull/1811>`__
- Feature: Add :command:`conan remote` proposal for cli 2.0. `#7401 <https://github.com/conan-io/conan/pull/7401>`_
- Fix: Allow usage of MD5 checksums in FIPS systems that would raise error otherwise. `#7807 <https://github.com/conan-io/conan/pull/7807>`_
- Fix: Fix capture output when running tests that call the ConanRunner in the conanfile. `#7799 <https://github.com/conan-io/conan/pull/7799>`_
- Fix: Consider absolute paths when parsing `conanbuildinfo.txt` `#7797 <https://github.com/conan-io/conan/pull/7797>`_
- Fix: Update parallel uploads help message. `#7785 <https://github.com/conan-io/conan/pull/7785>`_ . Docs `here <https://github.com/conan-io/docs/pull/1863>`__
- Fix: Removed check in lockfiles computed from other lockfile that it should be part of it. Users can check the resulting lockfile themselves if they want to. `#7763 <https://github.com/conan-io/conan/pull/7763>`_ . Docs `here <https://github.com/conan-io/docs/pull/1868>`__
- Fix: Extend help message indicating how to run :command:`conan export` without `user/channel`. `#7757 <https://github.com/conan-io/conan/pull/7757>`_ . Docs `here <https://github.com/conan-io/docs/pull/1859>`__
- Fix: Conan copy shows better description when using full reference for destination. `#7741 <https://github.com/conan-io/conan/pull/7741>`_
- Fix: Do not capture output for normal conan run (no logging or testing) when launching processes via `ConanRunner` so that color from build tools output is not lost. `#7740 <https://github.com/conan-io/conan/pull/7740>`_
- Fix: `self.copy()` follows `igore_case` correctly on Windows. `#7704 <https://github.com/conan-io/conan/pull/7704>`_ . Docs `here <https://github.com/conan-io/docs/pull/1862>`__
- Fix: Use patterns in server query when resolving version ranges. `#7673 <https://github.com/conan-io/conan/pull/7673>`_
- Fix: Raising conflict errors when options doesn't match in the evaluation of graphs with lockfiles. `#7513 <https://github.com/conan-io/conan/pull/7513>`_
- Bugfix: Fixed bug where uploading to multiple remotes in a single conan upload command would fail. `#7781 <https://github.com/conan-io/conan/pull/7781>`_
- BugFix: Add ``armv5hf`` and ``armv5el`` to the Android ABI architectures. `#7730 <https://github.com/conan-io/conan/pull/7730>`_
- Bugfix: Correctly inherit and use ``system_requirements`` when using ``python_requires``. `#7721 <https://github.com/conan-io/conan/pull/7721>`_
- Bugfix: Translate `settings.os` value `Macos` to `Darwin` for `CMAKE_SYSTEM_NAME` to allow compiling CMake-based packages for MacOS. `#7695 <https://github.com/conan-io/conan/pull/7695>`_

1.29.2 (21-Sept-2020)
---------------------

- Feature: Add support for apple-clang 12.0. `#7722 <https://github.com/conan-io/conan/pull/7722>`_ . Docs `here <https://github.com/conan-io/docs/pull/1843>`__

1.29.1 (17-Sept-2020)
---------------------

- Bugfix: Fix ``pkg_config`` generator adding to .pc files empty include and lib dirs. `#7703 <https://github.com/conan-io/conan/pull/7703>`_
- Bugfix: Fix non existing (failed import) ``tools.remove_files_by_mask``. `#7700 <https://github.com/conan-io/conan/pull/7700>`_
- BugFix: Removed lockfile checking build_requires when they come from 2 different origins: profiles and recipes. `#7698 <https://github.com/conan-io/conan/pull/7698>`_
- Bugfix: CMake build helper: Use actual CMake generator version to append platform generator, instead of the Conan setting `compiler.version`. `#7684 <https://github.com/conan-io/conan/pull/7684>`_

1.29.0 (02-Sept-2020)
---------------------

- Feature: Add QNX Neutrino version 7.1 to settings. `#7627 <https://github.com/conan-io/conan/pull/7627>`_
- Feature: Added support for `cpp_info.system_libs`, `cpp_info.framework_paths` and `cpp_info.frameworks` for ``qbs`` generator. `#7619 <https://github.com/conan-io/conan/pull/7619>`_
- Feature: Provide useful information trying to compute the build order using a `--base` lockfile. `#7551 <https://github.com/conan-io/conan/pull/7551>`_
- Feature: Add `user_info_build` field to JSON generator. `#7550 <https://github.com/conan-io/conan/pull/7550>`_
- Feature: `PkgConfig` tools now exposes the packages's version as property. `#7534 <https://github.com/conan-io/conan/pull/7534>`_ . Docs `here <https://github.com/conan-io/docs/pull/1820>`__
- Feature: Support from iOS 13.2 to 13.6. `#7507 <https://github.com/conan-io/conan/pull/7507>`_ . Docs `here <https://github.com/conan-io/docs/pull/1800>`__
- Feature: Add an experimental toolchain for gnu make. `#7430 <https://github.com/conan-io/conan/pull/7430>`_ . Docs `here <https://github.com/conan-io/docs/pull/1808>`__
- Feature: New ``tools.rename`` function to rename a file or folder to avoid 'Access is denied' on Windows. `#6774 <https://github.com/conan-io/conan/pull/6774>`_ . Docs `here <https://github.com/conan-io/docs/pull/1646>`__
- Fix: Fix `conan info --build-order` deprecation message. `#7632 <https://github.com/conan-io/conan/pull/7632>`_
- Fix: Set CMake targets compile options based on language `#7600 <https://github.com/conan-io/conan/pull/7600>`_
- Fix: Support installing configs from non-regular files. `#7583 <https://github.com/conan-io/conan/pull/7583>`_ . Docs `here <https://github.com/conan-io/docs/pull/1818>`__
- Fix: Update docs in `conan info -bo` command. `#7570 <https://github.com/conan-io/conan/pull/7570>`_
- Fix: Relax python six dependency to allow 1.15. `#7538 <https://github.com/conan-io/conan/pull/7538>`_
- Fix: Add pre-release versions when resolving `required_conan_version`. `#7535 <https://github.com/conan-io/conan/pull/7535>`_
- Fix: Adds support of URL-like git ssh syntax. `#7509 <https://github.com/conan-io/conan/pull/7509>`_
- Fix: Improve message of missing dependencies for components. `#7483 <https://github.com/conan-io/conan/pull/7483>`_
- Fix: Changed _requirements.txt_ to include distro package version 1.5.0. `#7461 <https://github.com/conan-io/conan/pull/7461>`_
- Fix: Avoid requiring the existence of all ``conanbuildinfo_xxx.cmake`` files in ``cmake_multi`` generator. `#7376 <https://github.com/conan-io/conan/pull/7376>`_
- Bugfix: Fix `cpp_info` filename in FindPackageHandleStandardArgs for cmake_find_package generator. `#7610 <https://github.com/conan-io/conan/pull/7610>`_
- Bugfix: Avoid marking as "modified" packages in a lockfile computed from a base lockfile. `#7592 <https://github.com/conan-io/conan/pull/7592>`_
- Bugfix: Update correctly "Package_ID_Unknown" nodes when using ``conan lock update`` and ``package_revision_mode``. `#7592 <https://github.com/conan-io/conan/pull/7592>`_
- Bugfix: Respect `winsdk_version` for WindowsStore. `#7584 <https://github.com/conan-io/conan/pull/7584>`_
- Bugfix: Fix frameworks usage with components for `cmake_find_package_multi` generator. `#7580 <https://github.com/conan-io/conan/pull/7580>`_
- Bugfix: Support `frameworks` and `framework_paths` in _qmake_ generator. `#7579 <https://github.com/conan-io/conan/pull/7579>`_
- Bugfix: Provide a more descriptive error when an unknown statement is added to a profile `#7577 <https://github.com/conan-io/conan/pull/7577>`_
- Bugfix: Add support for `cpp_info.system_libs` to _QMake_ generator. `#7563 <https://github.com/conan-io/conan/pull/7563>`_
- Bugfix: Make frogarian show up as a whole (not sliced) on linux terminal. `#7553 <https://github.com/conan-io/conan/pull/7553>`_
- Bugfix: Fix import of `collections.Iterable` compatible with Python2. `#7545 <https://github.com/conan-io/conan/pull/7545>`_
- Bugfix: Propagate the global version of the recipe for components. `#7524 <https://github.com/conan-io/conan/pull/7524>`_
- Bugfix: Use `CMAKE_FIND_ROOT_PATH_BOTH` to locate frameworks. `#7515 <https://github.com/conan-io/conan/pull/7515>`_

1.28.2 (31-Aug-2020)
--------------------

- Fix: Fix import of ``six.moves.collections_abc`` non existing for some six versions. `#7622 <https://github.com/conan-io/conan/pull/7622>`_
- Fix: Add system libs and frameworks to components targets in `cmake_find_package` and `cmake_find_package_multi` generators. `#7611 <https://github.com/conan-io/conan/pull/7611>`_
- Bugfix: Fix `cpp_info` filename in FindPackageHandleStandardArgs for cmake_find_package generator. `#7625 <https://github.com/conan-io/conan/pull/7625>`_
- Bugfix: Fix regression in ``deps_cpp_info`` incorrectly adding directories when reading from ``conanbuildinfo.txt`` file. `#7599 <https://github.com/conan-io/conan/pull/7599>`_

1.28.1 (06-Aug-2020)
--------------------

- Feature: Add `user_info_build` attribute to `txt` generator. `#7488 <https://github.com/conan-io/conan/pull/7488>`_
- Fix: Attribute `user_info_build` is available for commands in the local development workflow. `#7488 <https://github.com/conan-io/conan/pull/7488>`_
- Fix: Do not override value of `public_deps` in `pkg_config` generator. `#7482 <https://github.com/conan-io/conan/pull/7482>`_
- Bugfix: correctly set `CMAKE_OSX_SYSROOT` and `CMAKE_OSX_ARCHITECTURES`. `#7512 <https://github.com/conan-io/conan/pull/7512>`_
- Bugfix: When using ``build_requires`` defined in a profile that is passed as ``profile_host``, it was not being applied to ``build_requires`` that live in the host context (with ``force_host_context=True``). `#7500 <https://github.com/conan-io/conan/pull/7500>`_
- Bugfix: Fix broken ``cmake_find_package_multi`` when using components, as different configurations were being resolved to the same name, overwriting each other. `#7492 <https://github.com/conan-io/conan/pull/7492>`_
- Bugfix: Powershell files generated by `virtualenv` generators use proper path separators. `#7472 <https://github.com/conan-io/conan/pull/7472>`_

1.28.0 (31-Jul-2020)
--------------------

- Feature: Show Conan version on HTML output. `#7443 <https://github.com/conan-io/conan/pull/7443>`_ . Docs `here <https://github.com/conan-io/docs/pull/1782>`__
- Feature: Support for `cpp_info.components` in `pkg_config` generator. `#7413 <https://github.com/conan-io/conan/pull/7413>`_ . Docs `here <https://github.com/conan-io/docs/pull/1781>`__
- Feature: Adds ps1 virtualenv to other OS for use with powershell 7. #7407 `#7408 <https://github.com/conan-io/conan/pull/7408>`_ . Docs `here <https://github.com/conan-io/docs/pull/1776>`__
- Feature: Propose ``init()`` method to unconditionally initialize class attributes like ``license`` or ``description``. `#7404 <https://github.com/conan-io/conan/pull/7404>`_ . Docs `here <https://github.com/conan-io/docs/pull/1791>`__
- Feature: add deprecated attribute `#7399 <https://github.com/conan-io/conan/pull/7399>`_ . Docs `here <https://github.com/conan-io/docs/pull/1775>`__
- Feature: Allow ``conan.conf`` user configuration of paths to client certificate and key, outside of the Conan cache. `#7398 <https://github.com/conan-io/conan/pull/7398>`_ . Docs `here <https://github.com/conan-io/docs/pull/1791>`__
- Feature: Document return value of `self.copy()` in the `package()` method. `#7389 <https://github.com/conan-io/conan/pull/7389>`_ . Docs `here <https://github.com/conan-io/docs/pull/1773>`__
- Feature: Complete cli2.0 framework to handle sub-commands and add :command:`conan user` command for cli 2.0 `#7372 <https://github.com/conan-io/conan/pull/7372>`_
- Feature: Implement ``required_conan_version`` in ``conanfile.py``, will raise if the current Conan version does not match the defined version range. `#7360 <https://github.com/conan-io/conan/pull/7360>`_ . Docs `here <https://github.com/conan-io/docs/pull/1788>`__
- Feature: Add `provides` attribute to `ConanFile`: recipes can declare what they provide and Conan will fail if several recipes provide the same functionality (ODR violation). `#7337 <https://github.com/conan-io/conan/pull/7337>`_ . Docs `here <https://github.com/conan-io/docs/pull/1786>`__
- Feature: When using `CONAN_V2_MODE` if build_type or compiler are not defined Conan will raise an error. `#7327 <https://github.com/conan-io/conan/pull/7327>`_ . Docs `here <https://github.com/conan-io/docs/pull/1783>`__
- Feature: Adds "filenames" to cppinfo attribute, and changes `cmake_find_package` and `cmake_find_package_multi` generators so that they support it. `#7320 <https://github.com/conan-io/conan/pull/7320>`_ . Docs `here <https://github.com/conan-io/docs/pull/1768>`__
- Feature: Define ``recipe_folder`` attribute pointing to the folder containing ``conanfile.py`` `#7314 <https://github.com/conan-io/conan/pull/7314>`_ . Docs `here <https://github.com/conan-io/docs/pull/1785>`__
- Feature: Checking if a Linux distro uses `apt` is now based on the existence of `apt` in the system, instead of checking if the distro currently being used is in a hard-coded list of distros known to use `apt`. `#7309 <https://github.com/conan-io/conan/pull/7309>`_
- Feature: Add commands management for cli 2.0. `#7278 <https://github.com/conan-io/conan/pull/7278>`_
- Feature: Complete revamp of the **lockfiles** feature. Including version-only lockfiles, partial lockfiles, new command line syntax, improved management of build-order and many pending fixes. `#7243 <https://github.com/conan-io/conan/pull/7243>`_ . Docs `here <https://github.com/conan-io/docs/pull/1790>`__
- Feature: More detailed description for `--update` argument. `#7167 <https://github.com/conan-io/conan/pull/7167>`_ . Docs `here <https://github.com/conan-io/docs/pull/1778>`__
- Feature: improve compiler detection for `CONAN_V2_MODE`. `#5740 <https://github.com/conan-io/conan/pull/5740>`_ . Docs `here <https://github.com/conan-io/docs/pull/1789>`__
- Feature: Add settings for clang-cl (clang on Windows). `#5705 <https://github.com/conan-io/conan/pull/5705>`_ . Docs `here <https://github.com/conan-io/docs/pull/1784>`__
- Fix: Relax ``pluginbase`` requirement to ``pluginbase>=0.5``, including latest 1.0.0 . `#7441 <https://github.com/conan-io/conan/pull/7441>`_
- Fix: Make explicit the file writing of ``toolchain()`` helpers, so the method can be used to save custom files. `#7435 <https://github.com/conan-io/conan/pull/7435>`_ . Docs `here <https://github.com/conan-io/docs/pull/1793>`__
- Fix: Fixing `--help` for commands in proposal for command line v2.0. `#7394 <https://github.com/conan-io/conan/pull/7394>`_
- Fix: Show outdated packages when running `search --table`. `#7364 <https://github.com/conan-io/conan/pull/7364>`_ . Docs `here <https://github.com/conan-io/docs/pull/1771>`__
- Fix: Relax ``msbuild`` generator to not raise in Linux. `#7361 <https://github.com/conan-io/conan/pull/7361>`_
- Fix: Conan config install does not trigger scheduled config command. `#7311 <https://github.com/conan-io/conan/pull/7311>`_
- Fix: Implement missing ``__contains__`` method, so checking ``if "myoption" in self.info.options`` is possible in ``package_id()``. `#7303 <https://github.com/conan-io/conan/pull/7303>`_
- Fix: Build first ocurrence of a node in a lockfile when it is repeated (build requires) `#7144 <https://github.com/conan-io/conan/pull/7144>`_
- BugFix: Only add User-Agent to headers dict if it was not provided by the user. `#7390 <https://github.com/conan-io/conan/pull/7390>`_
- Bugfix: `cppstd` was missing in `settings.yml` for the qcc compiler and updates to 8.3. `#7384 <https://github.com/conan-io/conan/pull/7384>`_
- BugFix: Fix missing download of ``conan_sources.tgz`` created using ``export_sources()`` method. `#7380 <https://github.com/conan-io/conan/pull/7380>`_
- Bugfix: Intel Compiler install location detection on Windows. `#7370 <https://github.com/conan-io/conan/pull/7370>`_
- Bugfix: Avoid crash while computing ``package_id`` when using ``package_revision_mode``, and also incorrectly using installed binaries and reporting them installed after the re-computation of ``package_id`` resolved to a different binary. `#7353 <https://github.com/conan-io/conan/pull/7353>`_
- Bugfix: cmake_multi generator used with Xcode CMake generator. `#7341 <https://github.com/conan-io/conan/pull/7341>`_
- Bugfix: Do not fail for `conan remove -r remote -p` when there are no packages in the remote. `#7338 <https://github.com/conan-io/conan/pull/7338>`_
- Bugfix: Add ``system_libs`` to ``scons`` generator. `#7302 <https://github.com/conan-io/conan/pull/7302>`_

1.27.1 (10-Jul-2020)
--------------------

- Bugfix: Recover quotes around linker flags in CMake generators, fix failure with Macos frameworks `#7322 <https://github.com/conan-io/conan/pull/7322>`_

1.27.0 (01-Jul-2020)
--------------------

- Feature: (Only if using two profiles) Information from the `self.user_info` field is provided to consumers: information from the _host_ context is accessible via `deps_user_info` attribute,  and information from the _build_ context via `user_info_build` attribute. `#7266 <https://github.com/conan-io/conan/pull/7266>`_ . Docs `here <https://github.com/conan-io/docs/pull/1753>`__
- Feature: New ``conan config install --list`` and ``conan config install --remove=index`` arguments to display and remove conan config install origins. `#7263 <https://github.com/conan-io/conan/pull/7263>`_ . Docs `here <https://github.com/conan-io/docs/pull/1757>`__
- Feature: Support components for `cmake_find_package_multi` generator. `#7259 <https://github.com/conan-io/conan/pull/7259>`_ . Docs `here <https://github.com/conan-io/docs/pull/1755>`__
- Feature: Add Pop!_OS to the list of APT based distributions. `#7237 <https://github.com/conan-io/conan/pull/7237>`_
- Feature: Use Bootstrap in search table template style. `#7224 <https://github.com/conan-io/conan/pull/7224>`_
- Feature: Added support for template dir in :command:`conan new`. `#7215 <https://github.com/conan-io/conan/pull/7215>`_ . Docs `here <https://github.com/conan-io/docs/pull/1752>`__
- Feature: Configuration for checking the required Conan client version. `#7183 <https://github.com/conan-io/conan/pull/7183>`_ . Docs `here <https://github.com/conan-io/docs/pull/1740>`__
- Feature: Adds tool to fix symlinks in the `package_folder`. `#7178 <https://github.com/conan-io/conan/pull/7178>`_ . Docs `here <https://github.com/conan-io/docs/pull/1751>`__
- Feature: Templates for `conan search --table` and `conan info --graph` can be overridden by the user. `#7176 <https://github.com/conan-io/conan/pull/7176>`_ . Docs `here <https://github.com/conan-io/docs/pull/1739>`__
- Feature: Add support for the `CLICOLOR`/`CLICOLOR_FORCE`/`NO_COLOR` output colorization control variables. `#7154 <https://github.com/conan-io/conan/pull/7154>`_ . Docs `here <https://github.com/conan-io/docs/pull/1728>`__
- Fix: Remove message from the qmake generator. `#7228 <https://github.com/conan-io/conan/pull/7228>`_
- Fix: Allow ``--build=Pkg/0.1@`` to match the ``Pkg/0.1`` package, so the ``conan install Pkg/0.1@ --build=Pkg/0.1@`` also works. `#7219 <https://github.com/conan-io/conan/pull/7219>`_
- Fix: Improve error message when svn or git are not in the installed or in the path. `#7194 <https://github.com/conan-io/conan/pull/7194>`_
- Fix: Graph created for the `test_package/conanfile.py` recipe takes the `profile:build` if given. `#7182 <https://github.com/conan-io/conan/pull/7182>`_
- Fix: Define user variables in the ``conan_toolchain.cmake`` file, not in the project-include file. `#7160 <https://github.com/conan-io/conan/pull/7160>`_
- Fix: Set toolset for MSBuild in case of Intel C++. `#6809 <https://github.com/conan-io/conan/pull/6809>`_
- Bugfix: Allow to extend classes with ``python_requires_extend`` from packages that contain "." dots in the package name. `#7262 <https://github.com/conan-io/conan/pull/7262>`_
- Bugfix: Correctly inherit ``scm`` definitions from ``python_requires`` base classes. `#7238 <https://github.com/conan-io/conan/pull/7238>`_
- Bugfix: Change GNU triplet for iOS, watchOS, tvOS to allow simulator builds. `#6748 <https://github.com/conan-io/conan/pull/6748>`_
- SCM mode with ``scm_to_conandata`` and revisions marked as stable. Docs `here <https://github.com/conan-io/docs/pull/1759>`__

1.26.1 (23-Jun-2020)
--------------------

- Fix: Add missing migrations. `#7213 <https://github.com/conan-io/conan/pull/7213>`_
- Fix: Packages listed as `build_requires` in recipes that belong to the _host_ context don't add as `build_requires` those listed in the _host_ profile. `#7169 <https://github.com/conan-io/conan/pull/7169>`_

1.26.0 (10-Jun-2020)
--------------------

- Feature: Expose `msvs_toolset` tool. `#7134 <https://github.com/conan-io/conan/pull/7134>`_ . Docs `here <https://github.com/conan-io/docs/pull/1715>`__
- Feature: Add components to `cmake_find_package` generator. `#7108 <https://github.com/conan-io/conan/pull/7108>`_ . Docs `here <https://github.com/conan-io/docs/pull/1722>`__
- Feature: Add `stdcpp_library` tool. `#7082 <https://github.com/conan-io/conan/pull/7082>`_ . Docs `here <https://github.com/conan-io/docs/pull/1714>`__
- Feature: Add remove_files_by_mask helper `#7080 <https://github.com/conan-io/conan/pull/7080>`_ . Docs `here <https://github.com/conan-io/docs/pull/1713>`__
- Feature: New ``toolchain()`` recipe method, as a new paradigm for integrating build systems, and simplifying developer flows. `#7076 <https://github.com/conan-io/conan/pull/7076>`_ . Docs `here <https://github.com/conan-io/docs/pull/1729>`__
- Feature: New experimental ``msvc`` generator that generates a .props file per dependency and is also multi-configuration. `#7035 <https://github.com/conan-io/conan/pull/7035>`_ . Docs `here <https://github.com/conan-io/docs/pull/1732>`__
- Feature: Add `conan config init` command. `#6959 <https://github.com/conan-io/conan/pull/6959>`_ . Docs `here <https://github.com/conan-io/docs/pull/1704>`__
- Feature: Add ``export()`` and ``export_sources()`` methods, that provide the ``self.copy()`` helper to add files to recipe or sources in the same way as the corresponding attributes. `#6945 <https://github.com/conan-io/conan/pull/6945>`_ . Docs `here <https://github.com/conan-io/docs/pull/1733>`__
- Feature: Allow access to ``self.name`` and ``self.version`` in ``set_name()`` and ``set_version()`` methods. `#6940 <https://github.com/conan-io/conan/pull/6940>`_ . Docs `here <https://github.com/conan-io/docs/pull/1710>`__
- Feature: Use a template approach for the `html` and `dot` output of the Conan graph. `#6833 <https://github.com/conan-io/conan/pull/6833>`_
- Feature: Handle C++ standard flag for Intel C++ compiler. `#6766 <https://github.com/conan-io/conan/pull/6766>`_
- Feature: Call compilervars.sh within CMake helper (Intel C++). `#6735 <https://github.com/conan-io/conan/pull/6735>`_ . Docs `here <https://github.com/conan-io/docs/pull/1716>`__
- Feature: Pass command to Runner as a sequence instead of string. `#5583 <https://github.com/conan-io/conan/pull/5583>`_ . Docs `here <https://github.com/conan-io/docs/pull/1385>`__
- Fix: JSON-serialize sets as a list when using `conan inspect --json`. `#7151 <https://github.com/conan-io/conan/pull/7151>`_
- Fix: Update the lockfile passed as an argument to the install command instead of the default `conan.lock`. `#7127 <https://github.com/conan-io/conan/pull/7127>`_
- Fix: Adding a package as editable stores full path to `conanfile.py`. `#7079 <https://github.com/conan-io/conan/pull/7079>`_
- Fix: Fix broken test `PkgGeneratorTest`. `#7065 <https://github.com/conan-io/conan/pull/7065>`_
- Fix: Fix wrong naming of variables in the ``pkg_config`` generator. `#7059 <https://github.com/conan-io/conan/pull/7059>`_
- Fix: Do not modify `scm` attribute when the `origin` remote cannot be deduced. `#7048 <https://github.com/conan-io/conan/pull/7048>`_
- Fix: `vcvars_dict` should accept a conanfile too. `#7010 <https://github.com/conan-io/conan/pull/7010>`_ . Docs `here <https://github.com/conan-io/docs/pull/1696>`__
- Fix: ``conan config install`` can overwrite read-only files and won't copy permissions. `#7004 <https://github.com/conan-io/conan/pull/7004>`_
- Fix: Better error message for missing binaries, including multiple "--build=xxx" outputs. `#7003 <https://github.com/conan-io/conan/pull/7003>`_
- Fix: Add quotes to folders to accept paths with spaces when calling pyinstaller. `#6955 <https://github.com/conan-io/conan/pull/6955>`_
- Fix: Previously `conan` always set `cpp_std` option in `meson` project, even if `cppstd` option was not set in `conan` profile. Now it sets the option only if `cppstd` profile option has a concrete value. `#6895 <https://github.com/conan-io/conan/pull/6895>`_
- Fix: Handle compiler flags for Intel C++ (AutoToolsBuildEnvironment, Meson). `#6819 <https://github.com/conan-io/conan/pull/6819>`_
- Fix: Set the default CMake generator and toolset for Intel C++. `#6804 <https://github.com/conan-io/conan/pull/6804>`_
- Bugfix: Fix iOS CMake architecture. `#7164 <https://github.com/conan-io/conan/pull/7164>`_
- Bugfix: Getting attribute of ``self.deps_user_info["dep"]`` now raise ``AttributeError`` instead of a (wrong) ``KeyError``, enabling ``hasattr()`` and correct ``getattr()`` behaviors. `#7131 <https://github.com/conan-io/conan/pull/7131>`_
- Bugfix: Fix crash while computing the ``package_id`` of a package when different ``package_id_mode`` are mixed and include ``package_revision_mode``. `#7051 <https://github.com/conan-io/conan/pull/7051>`_
- Bugfix: Do not allow uploading packages with missing information in the `scm` attribute. `#7048 <https://github.com/conan-io/conan/pull/7048>`_
- Bugfix: Fixes an issue where Apple Framework lookup wasn't working on `RelWithDebInfo` CMake build types. `#7024 <https://github.com/conan-io/conan/pull/7024>`_
- Bugfix: Do not check patch compiler version in the ``cmake`` generators. `#6976 <https://github.com/conan-io/conan/pull/6976>`_

1.25.2 (19-May-2020)
--------------------

- Bugfix: Previously conan always set ``cpp_std`` option in meson project, even if ``cppstd`` option was not set in conan profile. Now it sets the option only if ``cppstd`` profile option has a concrete value. `#7047 <https://github.com/conan-io/conan/pull/7047>`_
- Bugfix: Fix deploy generator management of relative symlinks. `#7044 <https://github.com/conan-io/conan/pull/7044>`_
- Bugfix: Fixes an issue where Apple Framework lookup wasn't working on RelWithDebInfo. `#7041 <https://github.com/conan-io/conan/pull/7041>`_
- Bugfix: Fix broken ``AutoToolsBuildEnvironment`` when a profile:build is defined. `#7032 <https://github.com/conan-io/conan/pull/7032>`_

1.25.1 (13-May-2020)
--------------------

- Feature: Add missing gcc versions: 6.5, 7.5, 8.4, 10.1. `#6993 <https://github.com/conan-io/conan/pull/6993>`_ . Docs `here <https://github.com/conan-io/docs/pull/1689>`__
- Bugfix: Resumable download introduced a bug when there is a fronted (like Apache) to Artifactory or other server that gzips the returned files, returning an incorrect ``Content-Length`` header that doesn't match the real content length. `#6996 <https://github.com/conan-io/conan/pull/6996>`_
- Bugfix: Set ``shared_linker_flags`` to CMake ``MODULE`` targets too in ``cmake`` generators, not only to ``SHARED_LIBRARIES``. `#6983 <https://github.com/conan-io/conan/pull/6983>`_
- Bugfix: Fix `conan_get_policy` return value. `#6982 <https://github.com/conan-io/conan/pull/6982>`_
- Bugfix: Fix json output serialization for ``cpp_info.components``. `#6966 <https://github.com/conan-io/conan/pull/6966>`_

1.25.0 (06-May-2020)
--------------------

- Feature: Consume ``settings_build`` to get the value of the OS and arch from the ``build`` machine (only when ``--profile:build`` is provided). `#6916 <https://github.com/conan-io/conan/pull/6916>`_ . Docs `here <https://github.com/conan-io/docs/pull/1678>`__
- Feature: Implements ``cpp_info.components`` dependencies. `#6871 <https://github.com/conan-io/conan/pull/6871>`_ . Docs `here <https://github.com/conan-io/docs/pull/1682>`__
- Feature: Change HTML output for `conan search --table` command. `#6832 <https://github.com/conan-io/conan/pull/6832>`_ . Docs `here <https://github.com/conan-io/docs/pull/1676>`__
- Feature: Execute periodic config install command. `#6824 <https://github.com/conan-io/conan/pull/6824>`_ . Docs `here <https://github.com/conan-io/docs/pull/1679>`__
- Feature: Add `build_modules` to markdown generator output. `#6800 <https://github.com/conan-io/conan/pull/6800>`_
- Feature: Resume interrupted file downloads if server supports it. `#6791 <https://github.com/conan-io/conan/pull/6791>`_
- Feature: Using `CONAN_V2_MODE` the `version` attribute in a `ConanFile` is always a string (already documented). `#6782 <https://github.com/conan-io/conan/pull/6782>`_ . Docs `here <https://github.com/conan-io/docs/pull/1660>`__
- Feature: Support GCC 9.3. `#6772 <https://github.com/conan-io/conan/pull/6772>`_ . Docs `here <https://github.com/conan-io/docs/pull/1644>`__
- Feature: Populate `settings_build` and `settings_target` in conanfile (only if provided ``--profile:build``). `#6769 <https://github.com/conan-io/conan/pull/6769>`_ . Docs `here <https://github.com/conan-io/docs/pull/1678>`__
- Feature: handle C++ standard for Intel C++ compiler `#6766 <https://github.com/conan-io/conan/pull/6766>`_
- Feature: add Intel 19.1 (2020). `#6733 <https://github.com/conan-io/conan/pull/6733>`_
- Fix: `tools.unix_path` is noop in all platforms but Windows (already documented behavior). `#6935 <https://github.com/conan-io/conan/pull/6935>`_
- Fix: Preserve symbolic links for deploy generator. `#6922 <https://github.com/conan-io/conan/pull/6922>`_ . Docs `here <https://github.com/conan-io/docs/pull/1681>`__
- Fix: Adds missing version GCC 10 to default settings. `#6911 <https://github.com/conan-io/conan/pull/6911>`_ . Docs `here <https://github.com/conan-io/docs/pull/1675>`__
- Fix: Populate `requires` returned by the servers from the search endpoint using `requires` (Artifactory) or `full_requires` (conan_server) fields. `#6861 <https://github.com/conan-io/conan/pull/6861>`_
- Fix: Avoid failures that happen when Conan runs in a non-existing folder. `#6825 <https://github.com/conan-io/conan/pull/6825>`_
- Fix: Use pep508 environment markers for defining Conan pip requirements. `#6798 <https://github.com/conan-io/conan/pull/6798>`_
- Fix: Improve error message when ``[options]`` are not specified correctly in conanfile.txt. `#6794 <https://github.com/conan-io/conan/pull/6794>`_
- Fix: add missing compiler version check for Intel. `#6734 <https://github.com/conan-io/conan/pull/6734>`_
- Bugfix: Prevent crash when mixing package_id modes for the same dependency. `#6947 <https://github.com/conan-io/conan/pull/6947>`_
- BugFix: Propagate arch parameter to ``tools.vcvars_command()`` in `MSBuild()` build helper. `#6928 <https://github.com/conan-io/conan/pull/6928>`_
- Bugfix: Fix the output of :command:`conan info` package folder when using ``build_id()`` method. `#6917 <https://github.com/conan-io/conan/pull/6917>`_
- Bugfix: Generate correct PACKAGE_VERSION in ``cmake_find_package_multi`` generator for multi-config packages. `#6914 <https://github.com/conan-io/conan/pull/6914>`_
- Bugfix: enable C++20 on Apple Clang. `#6858 <https://github.com/conan-io/conan/pull/6858>`_
- Bugfix: Variable `package_name` in `conan new -t <template>` command contains a _CamelCase_ version of the name of the package. `#6821 <https://github.com/conan-io/conan/pull/6821>`_ . Docs `here <https://github.com/conan-io/docs/pull/1663>`__
- Bugfix: Changed the CMake generator template to properly handle exelinkflags and sharedlinkflags using generator expressions. `#6780 <https://github.com/conan-io/conan/pull/6780>`_

1.24.1 (21-Apr-2020)
--------------------

- Bugfix: correct the `cmake` generator target name in the `markdown` generator output. `#6788 <https://github.com/conan-io/conan/pull/6788>`_
- Bugfix: Avoid `FileNotFoundError` as it is not compatible with Python 2. `#6786 <https://github.com/conan-io/conan/pull/6786>`_

1.24.0 (31-Mar-2020)
--------------------

- Feature: Add the needed command-line arguments to existing commands to provide information about host and build profiles. `#5594 <https://github.com/conan-io/conan/pull/5594>`_ . Docs: `here <https://github.com/conan-io/docs/pull/1629>`__
- Feature: Add `markdown` generator, it exposes useful information to consume the installed packages. `#6758 <https://github.com/conan-io/conan/pull/6758>`_ . Docs `here <https://github.com/conan-io/docs/pull/1638>`__
- Feature: Add new tool `cppstd_flag` to retrieve the compiler flag for the given settings. `#6744 <https://github.com/conan-io/conan/pull/6744>`_ . Docs `here <https://github.com/conan-io/docs/pull/1639>`__
- Feature: Short paths feature is available for Cygwin. `#6741 <https://github.com/conan-io/conan/pull/6741>`_ . Docs `here <https://github.com/conan-io/docs/pull/1641>`__
- Feature: Add Apple Clang as a base compiler for Intel C++. `#6740 <https://github.com/conan-io/conan/pull/6740>`_ . Docs `here <https://github.com/conan-io/docs/pull/1637>`__
- Feature: Make `settings.get_safe` and `options.get_safe` accept a default value. `#6739 <https://github.com/conan-io/conan/pull/6739>`_ . Docs `here <https://github.com/conan-io/docs/pull/1631>`__
- Feature: `CONAN_V2_MODE` deprecates two legacy ways of reusing python code: the `<cache>/python` path and the automatic `PYTHONPATH` environment variable. `#6737 <https://github.com/conan-io/conan/pull/6737>`_ . Docs `here <https://github.com/conan-io/docs/pull/1630>`__
- Feature: Add the _description_ field to the output of the :command:`conan info` command. `#6724 <https://github.com/conan-io/conan/pull/6724>`_ . Docs `here <https://github.com/conan-io/docs/pull/1627>`__
- Feature: Add more detailed information when there are `missing` packages. `#6700 <https://github.com/conan-io/conan/pull/6700>`_ . Docs `here <https://github.com/conan-io/docs/pull/1616>`__
- Feature: Support mirrors for `tools.download` and `tools.get`. `#6679 <https://github.com/conan-io/conan/pull/6679>`_ . Docs `here <https://github.com/conan-io/docs/pull/1623>`__
- Feature: Modify the default behaviour in `SystemPackageTool` to be able to create a recipe that does not install system requirements by default if the `CONAN_SYSREQUIRES_MODE` is not set. `#6677 <https://github.com/conan-io/conan/pull/6677>`_ . Docs `here <https://github.com/conan-io/docs/pull/1613>`__
- Feature: Add `cpp_info.components` package creator interface to model internal dependencies inside a recipe. `#6653 <https://github.com/conan-io/conan/pull/6653>`_ . Docs `here <https://github.com/conan-io/docs/pull/1363>`__
- Feature: Add a new ``init()`` method to ``conanfile.py`` recipes that can be used to add extra logic when inheriting from ``python_requires`` classes. `#6614 <https://github.com/conan-io/conan/pull/6614>`_ . Docs `here <https://github.com/conan-io/docs/pull/1622>`__
- Fix: Add Sun C compiler version 5.15 into default settings.yml. `#6767 <https://github.com/conan-io/conan/pull/6767>`_
- Fix: Raises `ConanException` when package folder is invalid for `export-pkg`. `#6720 <https://github.com/conan-io/conan/pull/6720>`_ . Docs `here <https://github.com/conan-io/docs/pull/1624>`__
- Fix: Added print to stderr and exit into pyinstaller script when it detects python usage of python 3.8 or higher as currently pyinstaller does not support python 3.8. `#6686 <https://github.com/conan-io/conan/pull/6686>`_
- Fix: Improve the command line help for the `conan install --build` option. `#6681 <https://github.com/conan-io/conan/pull/6681>`_ . Docs `here <https://github.com/conan-io/docs/pull/1595>`__
- Fix: Add build policy help for `--build` argument when used in `conan graph build-order` command. `#6650 <https://github.com/conan-io/conan/pull/6650>`_
- Fix: Remove file before copying in ``conan config install`` to avoid permission issues. `#6601 <https://github.com/conan-io/conan/pull/6601>`_
- Fix: check_min_cppstd raises an exception for an unknown compiler. `#6548 <https://github.com/conan-io/conan/pull/6548>`_ . Docs `here <https://github.com/conan-io/docs/pull/1559>`__
- Fix: cmake_find_package no longer seeks to find packages which are already found. `#6389 <https://github.com/conan-io/conan/pull/6389>`_
- Bugfix: Fixes the auto-detection of ``sun-cc`` compiler when it outputs ``Studio 12.5 Sun C``. `#6757 <https://github.com/conan-io/conan/pull/6757>`_
- Bugfix: Add values to ``definitions`` passed to ``MSBuild`` build helper which values are not None (0, False...). `#6730 <https://github.com/conan-io/conan/pull/6730>`_
- Bugfix: Include name and version in the data from ``conanbuildinfo.txt``, so it is available in ``self.deps_cpp_info["dep"].version`` and ``self.deps_cpp_info["dep"].name``, so it can be used in :command:`conan build` and in ``test_package/conanfile.py``. `#6723 <https://github.com/conan-io/conan/pull/6723>`_ . Docs `here <https://github.com/conan-io/docs/pull/1626>`__
- Bugfix: Fix `check_output_runner()` to handle dirs with whitespaces. `#6703 <https://github.com/conan-io/conan/pull/6703>`_
- Bugfix: Fix vcvars_arch usage before assignment, that can cause a crash in ``tools.vcvars_command()`` that is also used internally by ``MSBuild`` helper. `#6675 <https://github.com/conan-io/conan/pull/6675>`_
- Bugfix: Silent output from cmake_find_package generator with `CONAN_CMAKE_SILENT_OUTPUT`. `#6672 <https://github.com/conan-io/conan/pull/6672>`_
- Bugfix: Use always LF line separator for .sh scripts generated by ``virtualenv`` generators. `#6670 <https://github.com/conan-io/conan/pull/6670>`_
- Bugfix: Use the real settings value to check the compiler and compiler version in the ``cmake`` generator local flow when the ``package_id()`` method changes values. `#6659 <https://github.com/conan-io/conan/pull/6659>`_

1.23.0 (10-Mar-2020)
--------------------

- Feature: New ``general.parallel_download=<num threads>`` configuration, for parallel installation of binaries, to speed up populating packages in a cache. `#6632 <https://github.com/conan-io/conan/pull/6632>`_ . Docs `here <https://github.com/conan-io/docs/pull/1583>`__
- Feature: Fixed inability to run execute `test` and `install` separately, that is, without `build` step. Added `meson_test()` method, which executes `meson test` (compared to `ninja test` in `test()`). Added `meson_install()` method, which executes `meson install` (compared to `ninja install` in `install()`). `#6574 <https://github.com/conan-io/conan/pull/6574>`_ . Docs `here <https://github.com/conan-io/docs/pull/1568>`__
- Feature: Update python six dependency to 1.14.0. `#6507 <https://github.com/conan-io/conan/pull/6507>`_
- Feature: Add environment variable 'CONAN_V2_MODE' to enable Conan v2 behavior. `#6490 <https://github.com/conan-io/conan/pull/6490>`_ . Docs `here <https://github.com/conan-io/docs/pull/1578>`__
- Feature: Implement `conan graph clean-modified` subcommand to be able to clean the modified state of a lockfile and re-use it later for more operations. `#6465 <https://github.com/conan-io/conan/pull/6465>`_ . Docs `here <https://github.com/conan-io/docs/pull/1542>`__
- Feature: Allow building dependency graphs when using lockfiles even if some requirements are not in the lockfiles. This can happen for example when ``test_package/conanfile.py`` has other requirements, as they will not be part of the lockfile. `#6457 <https://github.com/conan-io/conan/pull/6457>`_ . Docs `here <https://github.com/conan-io/docs/pull/1585>`__
- Feature: Implement a new package-ID computation that includes transitive dependencies even when the direct dependencies have remove them, for example when depending on a header-only library that depends on a static library. `#6451 <https://github.com/conan-io/conan/pull/6451>`_ . Docs `here <https://github.com/conan-io/docs/pull/1575>`__
- Fix: inspect command can be executed without remote.json (#6558) `#6559 <https://github.com/conan-io/conan/pull/6559>`_
- Fix: Raise an error if ``MSBuild`` argument ``targets`` is not a list, instead of splitting a string passed as argument instead of a list. `#6555 <https://github.com/conan-io/conan/pull/6555>`_
- Bugfix: Check the `CMP0091` policy and set `CMAKE_MSVC_RUNTIME_LIBRARY` accordingly to `CONAN_LINK_RUNTIME` if it's set to `NEW`. `#6626 <https://github.com/conan-io/conan/pull/6626>`_
- Bugfix: Fix error parsing `system_libs` from `conanbuildinfo.txt` file. `#6616 <https://github.com/conan-io/conan/pull/6616>`_
- Bugfix: Environment variables from the profiles are not set in the _conaninfo.txt_ file of the packages exported with the `export-pkg` command. `#6607 <https://github.com/conan-io/conan/pull/6607>`_
- BugFix: Set the ``self.develop=True`` attribute for recipes when they are used with :command:`conan export-pkg`, in all methods, it was previously only setting it for the ``package()`` method. `#6585 <https://github.com/conan-io/conan/pull/6585>`_
- Bugfix: set CMAKE_OSX_DEPLOYMENT_TARGET for iOS, watchOS and tvOS. `#6566 <https://github.com/conan-io/conan/pull/6566>`_
- Bugfix: Parse function of GCC version from command line now works with versions `>=10`. `#6551 <https://github.com/conan-io/conan/pull/6551>`_
- Bugfix: improve Apple frameworks lookups with CMake integration `#6533 <https://github.com/conan-io/conan/pull/6533>`_

1.22.3 (05-Mar-2020)
--------------------

- Bugfix: Fixed crashing of recipes using both ``python_requires`` and ``build_id()``. `#6618 <https://github.com/conan-io/conan/pull/6618>`_
- Bugfix: Conan should not append generator_platform to the Visual Studio generator if it is already specified by the user. `#6549 <https://github.com/conan-io/conan/pull/6549>`_

1.22.2 (13-Feb-2020)
--------------------

- Bugfix: Do not re-evaluate lockfiles nodes, only update the package reference, otherwise the build-requires are broken. `#6529 <https://github.com/conan-io/conan/pull/6529>`_
- Bugfix: Fixing locking system for metadata file so it can be accessed concurrently. `#6524 <https://github.com/conan-io/conan/pull/6524>`_

1.22.1 (11-Feb-2020)
--------------------

- Fix: Increase ``six`` version to allow more modern releases. `#6509 <https://github.com/conan-io/conan/pull/6509>`_
- Fix: remove `GLOBAL` from targets to avoid conflicts when using `add_subdirectory`. `#6488 <https://github.com/conan-io/conan/pull/6488>`_ . Docs `here <https://github.com/conan-io/docs/pull/1551>`__
- Fix: Avoid caching revision "0" under api V2 (revisions enabled) in the download cache. `#6475 <https://github.com/conan-io/conan/pull/6475>`_ . Docs `here <https://github.com/conan-io/docs/pull/1552>`__
- Bugfix: Manage the ``dirty`` state of the cache package folder with :command:`conan export-pkg`. `#6498 <https://github.com/conan-io/conan/pull/6498>`_
- BugFix: Add ``system_libs`` to ``premake`` generator. `#6495 <https://github.com/conan-io/conan/pull/6495>`_
- Bugfix: Upload was silently skipping exceptions that could leave the packages dirty. Long uploads or large compressing times in non-terminals (piped output, like in CI systems) crashed, leaving packages dirty too, but not reporting any error. `#6486 <https://github.com/conan-io/conan/pull/6486>`_
- BugFix: Add quotes to ``virtualenv`` scripts, so they don't crash in pure sh shells. `#6265 <https://github.com/conan-io/conan/pull/6265>`_

1.22.0 (05-Feb-2020)
--------------------

- Feature: Set conan generated CMake targets as `GLOBAL` so that they can be used with an `ALIAS` for consumers. `#6438 <https://github.com/conan-io/conan/pull/6438>`_ . Docs `here <https://github.com/conan-io/docs/pull/1534>`__
- Feature: Deduce `compiler.base.runtime` for Intel compiler settings when using Visual Studio as the base compiler. `#6424 <https://github.com/conan-io/conan/pull/6424>`_
- Feature: Allow defining an extra user-defined properties .props file in ``MSBuild`` build helper. `#6374 <https://github.com/conan-io/conan/pull/6374>`_ . Docs `here <https://github.com/conan-io/docs/pull/1533>`__
- Feature: Force the user to read that Python 2 has been deprecated. `#6336 <https://github.com/conan-io/conan/pull/6336>`_ . Docs `here <https://github.com/conan-io/docs/pull/1523>`__
- Feature: Add opt-in `scm_to_conandata` for the SCM feature: Conan will store the data from the SCM attribute in the `conandata.yml` file (except the fields `username` and `password`). `#6334 <https://github.com/conan-io/conan/pull/6334>`_ . Docs `here <https://github.com/conan-io/docs/pull/1522>`__
- Feature: Implement a download cache, which can be shared and concurrently used among different conan user homes, selectable configuring ``storage.download_cache`` in ``conan.conf``. `#6287 <https://github.com/conan-io/conan/pull/6287>`_ . Docs `here <https://github.com/conan-io/docs/pull/1544>`__
- Feature: Some improvements in the internal of lockfiles. Better ordering of nodes indexes. Separation of ``requires`` and ``build-requires``. Better ``status`` field, with explicit ``exported``, ``built`` values. `#6237 <https://github.com/conan-io/conan/pull/6237>`_
- Feature: ``imports`` functionality can import from "symbolic" names, preceded with @, like @bindirs, @libdirs, etc. This allows importing files from variable package layouts, including custom ``package_info()`` layouts (like ``cpp_info.bindirs = ["mybin"]`` can be used with ``src="@bindirs"``), and editable package layouts `#6208 <https://github.com/conan-io/conan/pull/6208>`_ . Docs `here <https://github.com/conan-io/docs/pull/1547>`__
- Feature: Improve output messages for parallel uploads: the text of the uploaded files contains to which packages they belong and the output for CI is clearer. `#6184 <https://github.com/conan-io/conan/pull/6184>`_
- Feature: Adds ``vcvars_append`` variable (defaulting to ``False``) to ``CMake`` and ``Meson`` build helpers constructors, so when they need to activate the Visual Studio environment via ``vcvars`` (for Ninja and NMake generators), the ``vcvars`` environment is appended at the end, giving precedence to the environment previously defined. `#6000 <https://github.com/conan-io/conan/pull/6000>`_ . Docs `here <https://github.com/conan-io/docs/pull/1543>`__
- Fix: Use CCI package reference for example command. `#6463 <https://github.com/conan-io/conan/pull/6463>`_
- Fix: Generators `cmake` and `cmake_multi` use the name defined in `cpp_info.name` (reverts change from 1.21.1 as stated). `#6429 <https://github.com/conan-io/conan/pull/6429>`_
- Fix: Cleaning ``LD_LIBRARY_PATH`` environment in ``SCM`` commands for "pyinstaller" installations, as SSL can fail due to using old SSL stuff from Conan instead from git/svn. `#6380 <https://github.com/conan-io/conan/pull/6380>`_
- Fix: Recipe substitution for `scm` (old behavior) fixed for multiline comments in Python 3.8. `#6355 <https://github.com/conan-io/conan/pull/6355>`_ . Docs `here <https://github.com/conan-io/docs/pull/1526>`__
- Fix: Avoid warning in "detect" process with Python 3.8, due to Popen with ``bufsize=1`` `#6333 <https://github.com/conan-io/conan/pull/6333>`_
- Fix: Propagate server error (500) in `checksum_deploy`. `#6324 <https://github.com/conan-io/conan/pull/6324>`_
- Fix: Fixed wrong CMake command line with ``-G Visual Studio 15 ARM`` for ``armv8`` architectures. `#6312 <https://github.com/conan-io/conan/pull/6312>`_
- Fix: Add all the system_libs and requirements to the CMake targets constructed by the generators. It will impact header-only libraries that are consumed using targets (previously they were missing some information). `#6298 <https://github.com/conan-io/conan/pull/6298>`_
- Fix: Avoid WindowsStore ``tools.vcvars()`` management when the environment is already set. `#6296 <https://github.com/conan-io/conan/pull/6296>`_
- Fix: When the token is empty, and ``conan user myuser -p=mypass -r=remote`` is used, the user-password are send in HttpBasic so it can be used for completely protected servers that do not expose the ping endpoint. `#6254 <https://github.com/conan-io/conan/pull/6254>`_
- Fix: Add `cpp_info.<config>` information to `cmake_find_package_multi` and `cmake_find_package` generators. `#6230 <https://github.com/conan-io/conan/pull/6230>`_ . Docs `here <https://github.com/conan-io/docs/pull/1508>`__
- Fix: Multi-generators cannot be used without `build_type` setting. A failure is forced to `cmake_find_package_multi` and `visual_studio_multi` as it was in `cmake_multi`. `#6228 <https://github.com/conan-io/conan/pull/6228>`_
- Fix: Fix typo in error message from ``tools.get()``. `#6204 <https://github.com/conan-io/conan/pull/6204>`_
- Fix: Raise error for symlinks in Windows that point to a different unit. `#6201 <https://github.com/conan-io/conan/pull/6201>`_
- BugFix: Avoid included profiles overwriting variables in the current profile. `#6398 <https://github.com/conan-io/conan/pull/6398>`_
- Bugfix: Lockfiles were not correctly applying locked ``options`` to packages, which produced incorrect evaluation of ``requirements()`` method. `#6395 <https://github.com/conan-io/conan/pull/6395>`_
- Bugfix: Fix broken compression of .tgz files due to Python 3.8 changing tar default schema. `#6355 <https://github.com/conan-io/conan/pull/6355>`_ . Docs `here <https://github.com/conan-io/docs/pull/1526>`__
- Bugfix: Include MacOS frameworks definitions in autotools LDFLAGS (also Meson). `#6309 <https://github.com/conan-io/conan/pull/6309>`_
- Bugfix: Apply ``system_libs`` information in autotools build helper. `#6309 <https://github.com/conan-io/conan/pull/6309>`_
- Bugfix: The ``environment_append()`` helper does not modify the argument anymore, which caused problems if the argument was reused. `#6285 <https://github.com/conan-io/conan/pull/6285>`_
- Bugfix: Include "Package ID Unknown" nodes in ``conan graph build-order``, as they need to be processed in that order. `#6251 <https://github.com/conan-io/conan/pull/6251>`_
- Bugfix: `--raw` argument is ignored when searching for a specific reference. `#6241 <https://github.com/conan-io/conan/pull/6241>`_
- Bugfix: Avoid raising a version conflict error when aliases have not been resolved yet, typically for aliased ``build-requires`` that are also in the ``requires``. `#6236 <https://github.com/conan-io/conan/pull/6236>`_
- Bugfix: :command:`conan inspect` now is able to properly show name and version coming from ``set_name()`` and ``set_version()`` methods. `#6214 <https://github.com/conan-io/conan/pull/6214>`_


1.21.3 (03-Mar-2020)
--------------------

- Bugfix: Fixing locking system for metadata file so it can be accessed concurrently. `#6543 <https://github.com/conan-io/conan/pull/6543>`_
- Bugfix: Manage the dirty state of the cache package folder with conan export-pkg. `#6517 <https://github.com/conan-io/conan/pull/6517>`_
- Bugfix: BugFix: Add quotes to virtualenv scripts, so they don't crash in pure sh shells. `#6516 <https://github.com/conan-io/conan/pull/6516>`_
- Bugfix: Upload was silently skipping exceptions, which could result in packages not uploaded, but user not realizing about the error. `#6515 <https://github.com/conan-io/conan/pull/6515>`_
- BugFix: Add ``system_libs`` to ``premake`` generator. `#6496 <https://github.com/conan-io/conan/pull/6496>`_


1.21.2 (31-Jan-2020)
--------------------

- Fix: Recipe substitution for scm (old behavior) fixed for multiline comments in Python 3.8 `#6439 <https://github.com/conan-io/conan/pull/6439>`_
- Bugfix: Fix broken compression of .tgz files due to Python 3.8 changing tar default schema. `#6439 <https://github.com/conan-io/conan/pull/6439>`_
- Bugfix: Append `CONAN_LIBS` in `cmake` generator to avoid overwriting user-defined libs. `#6433 <https://github.com/conan-io/conan/pull/6433>`_


1.21.1 (14-Jan-2020)
--------------------

- Fix: Fix options type detection using `six.string_types`. `#6322 <https://github.com/conan-io/conan/pull/6322>`_
- Fix: Fix minor issues in `cmake` and `cmake_multi` generators: wrong variable used in `conan_find_apple_frameworks` macro. `#6295 <https://github.com/conan-io/conan/pull/6295>`_
- Fix: Generators `cmake` and `cmake_multi` use the name of the package instead of `cpp_info.name` (this change is to be reverted in 1.22) `#6288 <https://github.com/conan-io/conan/pull/6288>`_
- Bugfix: Fixing readout of backslashes for virtualenv generator files so they are not interpreted as escape characters. `#6320 <https://github.com/conan-io/conan/pull/6320>`_
- Bugfix: Fix uninformative crash when ``tools.download()`` gets a 403 and it is not providing an ``auth`` field. `#6317 <https://github.com/conan-io/conan/pull/6317>`_
- Bugfix: Enhance validation of the `short_paths_home` property to correctly handle the scenarios where it is set to a path that contains the value of the Conan cache path, but is not a subdirectory of it. `#6304 <https://github.com/conan-io/conan/pull/6304>`_
- Bugfix: Fixes `cpp_info.name` vs. `cpp_info.names` issue in `pkg_config` generator `#6223 <https://github.com/conan-io/conan/pull/6223>`_


1.21.0 (10-Dec-2019)
--------------------

- Feature: The generator `cmake_find_package_multi` generates a `PackageConfigVersion.cmake` file that allows using `find_package` with the `VERSION` argument. `#6063 <https://github.com/conan-io/conan/pull/6063>`_ . Docs `here <https://github.com/conan-io/docs/pull/1484>`__
- Feature: Settings support for Intel compiler. `#6052 <https://github.com/conan-io/conan/pull/6052>`_ . Docs `here <https://github.com/conan-io/docs/pull/1479>`__
- Feature: Allow setting different cpp_info name for each generator that supports that property using the new cpp_info.names["generator_name"] property. `#6033 <https://github.com/conan-io/conan/pull/6033>`_ . Docs `here <https://github.com/conan-io/docs/pull/1489>`__
- Feature: Provide `_INCLUDE_DIR` variables in the `cmake_find_package` generator `#6017 <https://github.com/conan-io/conan/pull/6017>`_
- Feature: Information in the `artifacts.properties` file is sent using matrix-params too when a package is uploaded to a server (if it has the capability). This will be the recommended way to send these properties to Artifactory (release TBD) to bypass Nginx blocking properties with periods. `#6014 <https://github.com/conan-io/conan/pull/6014>`_ . Docs `here <https://github.com/conan-io/docs/pull/1487>`__
- Feature: New `tools.check_min_cppstd` and `tools.valid_min_cppstd` to check if the cppstd version is valid for a specific package. `#5997 <https://github.com/conan-io/conan/pull/5997>`_ . Docs `here <https://github.com/conan-io/docs/pull/1467>`__
- Feature: New parameter for `tools.patch` to opt-in applying fuzzy patches. `#5996 <https://github.com/conan-io/conan/pull/5996>`_ . Docs `here <https://github.com/conan-io/docs/pull/1466>`__
- Feature: Environment variables for virtual environments are stored in `.env` files containing just the key-value pairs. It will help other processes that need to read these variables to run their own commands. `#5989 <https://github.com/conan-io/conan/pull/5989>`_
- Feature: New argument of :command:`conan upload` command `--parallel` to upload packages using multithreading. `#5856 <https://github.com/conan-io/conan/pull/5856>`_ . Docs `here <https://github.com/conan-io/docs/pull/1250>`__
- Feature: New ``python_requires`` declared as Conanfile class attributes. Includes extension of base class, they affect the binary packageID with ``minor_mode`` default mode. They are also locked in lockfiles. `#5804 <https://github.com/conan-io/conan/pull/5804>`_ . Docs `here <https://github.com/conan-io/docs/pull/1495>`__
- Feature: Accept logging level as logging names `#5772 <https://github.com/conan-io/conan/pull/5772>`_ . Docs `here <https://github.com/conan-io/docs/pull/1419>`__
- Fix: Add the RES_DIRS as variable to the variables when using the ``cmake_find_package`` generator. `#6166 <https://github.com/conan-io/conan/pull/6166>`_
- Fix: Fix SyntaxWarning when comparing a literal with for identity in Python 3.8 `#6165 <https://github.com/conan-io/conan/pull/6165>`_
- Fix: Remove recipe linter from codebase, it is no longer a built-in feature. It has been moved to hooks. Install the hook and update your "conan.conf" to activate it. `#6152 <https://github.com/conan-io/conan/pull/6152>`_ . Docs `here <https://github.com/conan-io/docs/pull/1488>`__
- Fix: Make lockfiles invariant when the graph doesn't change. Now 2 different lockfiles captured with the same resulting graph in 2 different instants will be identical. `#6139 <https://github.com/conan-io/conan/pull/6139>`_
- Fix: Make the ``compatible_packages`` feature to follow the ``--build=missing`` build policy. Packages that find a compatible binary will not fire a binary build with the "missing" build policy. `#6134 <https://github.com/conan-io/conan/pull/6134>`_ . Docs `here <https://github.com/conan-io/docs/pull/1491>`__
- Fix: Fix create command build policy help message to reflect correct behavior. `#6131 <https://github.com/conan-io/conan/pull/6131>`_ . Docs `here <https://github.com/conan-io/docs/pull/1483>`__
- Fix: Improved error message when sources can't be retrieved from remote `#6085 <https://github.com/conan-io/conan/pull/6085>`_
- Fix: Raise a meaningful error when the `settings.yml` file is invalid `#6059 <https://github.com/conan-io/conan/pull/6059>`_
- Fix: Move the warning about mixing 'os' and 'os_build' to just before the pre_export stage `#6021 <https://github.com/conan-io/conan/pull/6021>`_
- Bugfix: Implement ``SystemPackageTool.installed(package_name)`` as described in the documentation. `#6198 <https://github.com/conan-io/conan/pull/6198>`_
- Bugfix: Remove carriage returns from build info `.json` file to avoid Artifactory errors in some cases when publishing the build info to the remote. `#6180 <https://github.com/conan-io/conan/pull/6180>`_
- Bugfix: Upload correct packages when specifying revisions and fail with incorrect ones. `#6143 <https://github.com/conan-io/conan/pull/6143>`_
- Bugfix: Fix different problems when using :command:`conan download` with revisions. `#6138 <https://github.com/conan-io/conan/pull/6138>`_
- Bugfix: Make sure ``set_version()`` runs in the ``conanfile.py`` folder, not in the current folder, so relative paths are not broken if executing from a different location. `#6130 <https://github.com/conan-io/conan/pull/6130>`_ . Docs `here <https://github.com/conan-io/docs/pull/1490>`__
- Bugfix: Fix the help message for :command:`conan export-pkg` command for the --options parameter. `#6092 <https://github.com/conan-io/conan/pull/6092>`_
- Bugfix: Use a context manager to change the folder during `build_package` to avoid propagating the directory change to other tasks. `#6060 <https://github.com/conan-io/conan/pull/6060>`_
- Bugfix: The `AutoToolsBuildEnvironment` build helper now uses the `win_bash` parameter of the constructor when calling to `configure()`. `#6026 <https://github.com/conan-io/conan/pull/6026>`_
- Bugfix: Conan's virtualenvironments restore the environment to the state it was before activating them (previously it was restored to the state it was when the :command:`conan install` was run). `#5989 <https://github.com/conan-io/conan/pull/5989>`_


1.20.5 (3-Dec-2019)
-------------------

- Bugfix: Removing `--skip-env`  and `--multi-module` arguments  for `conan_build_info --v2`. Now the environment is not captured (will be handled by the Artifactory plugin) and recipes and packages are saved as different modules in build info. `#6169 <https://github.com/conan-io/conan/pull/6169>`_ . Docs `here <https://github.com/conan-io/docs/pull/1486>`__


1.20.4 (19-Nov-2019)
--------------------

- Feature: Added traces to `check_output` internal call to log the called command and the output as INFO traces (can be adjusted with `export CONAN_LOGGING_LEVEL=20`) `#6091 <https://github.com/conan-io/conan/pull/6091>`_
- Bugfix: Using `scm` with `auto` values with a `conanfile.py` not being in the root scm folder it failed to export the right source code directory if not using `--ignore-dirty` and the repo was not pristine. `#6098 <https://github.com/conan-io/conan/pull/6098>`_
- Bugfix: Fix `conan_build_info` command when conan_sources.tgz not present in remote. `#6088 <https://github.com/conan-io/conan/pull/6088>`_


1.20.3 (11-Nov-2019)
--------------------

- Bugfix: Using the `scm` feature with `auto` fields was not using correctly the freeze sources from the local user directory from the second call to :command:`conan create`. `#6048 <https://github.com/conan-io/conan/pull/6048>`_
- Bugfix: Each Apple framework found using CMake `find_library` is stored in a different `CONAN_FRAMEWORK_<name>_FOUND` variable `#6042 <https://github.com/conan-io/conan/pull/6042>`_


1.20.2 (6-Nov-2019)
-------------------

- Bugfix: Fix Six package version to be compatible with Astroid `#6031 <https://github.com/conan-io/conan/pull/6031>`_


1.20.1 (5-Nov-2019)
-------------------

- Bugfix: Fixed authentication with an Artifactory repository without anonymous access enabled. `#6022 <https://github.com/conan-io/conan/pull/6022>`_


1.20.0 (4-Nov-2019)
-------------------

- Feature: Provide `CONAN_FRAMEWORKS` and `CONAN_FRAMEWORKS_FOUND` for Apple frameworks in CMake generators and `conan_find_apple_frameworks()` macro helper in CMake generators. `#6003 <https://github.com/conan-io/conan/pull/6003>`_ . Docs `here <https://github.com/conan-io/docs/pull/1472>`__
- Feature: Saving profile list as a json file `#5954 <https://github.com/conan-io/conan/pull/5954>`_ . Docs `here <https://github.com/conan-io/docs/pull/1449>`__
- Feature: Improve `conan_build_info` command maintaining old functionality. `#5950 <https://github.com/conan-io/conan/pull/5950>`_ . Docs `here <https://github.com/conan-io/docs/pull/1456>`__
- Feature: Add `--json `argument  to the `config home` subcommand to output the result to a JSON file. `#5946 <https://github.com/conan-io/conan/pull/5946>`_ . Docs `here <https://github.com/conan-io/docs/pull/1464>`__
- Feature: Add `cpp_info.build_modules` to manage build system modules like additional CMake functions in packages `#5940 <https://github.com/conan-io/conan/pull/5940>`_ . Docs `here <https://github.com/conan-io/docs/pull/1465>`__
- Feature: Add support for Clang 10. `#5936 <https://github.com/conan-io/conan/pull/5936>`_
- Feature: Store `md5` and `sha1` checksums of downloaded and uploaded packages in `metadata.json`. `#5910 <https://github.com/conan-io/conan/pull/5910>`_
- Feature: Allow the possibility to avoid `x86_64` to `x86` building when cross-building. `#5904 <https://github.com/conan-io/conan/pull/5904>`_ . Docs `here <https://github.com/conan-io/docs/pull/1445>`__
- Feature: Allow to specify encoding for `tools.load`, `tools.save` and `tools.replace_in_files`. `#5902 <https://github.com/conan-io/conan/pull/5902>`_ . Docs `here <https://github.com/conan-io/docs/pull/1446>`__
- Feature: Add support for gcc 7.4. `#5898 <https://github.com/conan-io/conan/pull/5898>`_ . Docs `here <https://github.com/conan-io/docs/pull/1438>`__
- Feature: New ``set_name()`` and ``set_version()`` member methods to dynamically obtain the name and version (at export time). `#5881 <https://github.com/conan-io/conan/pull/5881>`_ . Docs `here <https://github.com/conan-io/docs/pull/1444>`__
- Feature: New binary compatibility mode. Recipes can define in their ``package_id()`` an ordered list of binary package variants that would be binary compatible with the default one. These variants will be checked in order if the main package ID is not found (missing), and the first one will be installed and used. `#5837 <https://github.com/conan-io/conan/pull/5837>`_ . Docs `here <https://github.com/conan-io/docs/pull/1468>`__
- Feature: Support for DNF system package manager (Fedora 31+ and others) when present. `#5791 <https://github.com/conan-io/conan/pull/5791>`_ . Docs `here <https://github.com/conan-io/docs/pull/1462>`__
- Feature: Refactor Conan Upload, Download and Compress progress bars. `#5763 <https://github.com/conan-io/conan/pull/5763>`_
- Feature: Add `system_deps` attribute for cpp_info and deps_cpp_info. `#5582 <https://github.com/conan-io/conan/pull/5582>`_ . Docs `here <https://github.com/conan-io/docs/pull/1395>`__
- Feature: The `scm` feature does not replace the `scm.revision="auto"` field with the commit when uncommitted changes unless ``--scm-dirty`` argument is specified. The recipe in the local cache will be kept with `revision=auto`. `#5543 <https://github.com/conan-io/conan/pull/5543>`_ . Docs `here <https://github.com/conan-io/docs/pull/1471>`__
- Feature: The :command:`conan upload` command forbids to upload a recipe that uses the `scm` feature containing `revision=auto` or `url=auto`, unless `--force` is used. `#5543 <https://github.com/conan-io/conan/pull/5543>`_ . Docs `here <https://github.com/conan-io/docs/pull/1471>`__
- Feature: The `scm` feature captures the local sources in the local cache during the export, avoiding later issues of modified local sources. `#5543 <https://github.com/conan-io/conan/pull/5543>`_ . Docs `here <https://github.com/conan-io/docs/pull/1471>`__
- Fix: Deprecate argument `--build-order` in :command:`conan info` command. `#5965 <https://github.com/conan-io/conan/pull/5965>`_ . Docs `here <https://github.com/conan-io/docs/pull/1451>`__
- Fix: Avoid doing complex ``conan search --query`` in the server, do them always in the client. `#5960 <https://github.com/conan-io/conan/pull/5960>`_
- Fix: Improved ``conan remove --help`` message for ``--packages`` `#5899 <https://github.com/conan-io/conan/pull/5899>`_
- Fix: Improved cmake compiler check message to explain the problem with different compiler versions when installing dependencies `#5858 <https://github.com/conan-io/conan/pull/5858>`_
- Fix: Adds support for transitive dependencies to b2 generator. `#5812 <https://github.com/conan-io/conan/pull/5812>`_
- Fix: Add support for recipes without `settings.compiler` in b2 generator. `#5810 <https://github.com/conan-io/conan/pull/5810>`_
- Fix: Add and remove out-of-tree git patches (#5320) `#5761 <https://github.com/conan-io/conan/pull/5761>`_
- Fix: Add quiet output for `inspect --raw`. `#5702 <https://github.com/conan-io/conan/pull/5702>`_
- Bugfix: Allow :command:`conan download` for packages without user/channel `#6010 <https://github.com/conan-io/conan/pull/6010>`_
- Bugfix: Avoid erroneous case-sensitive conflict for packages without user/channel. `#5981 <https://github.com/conan-io/conan/pull/5981>`_
- Bugfix: Fix crashing when using lockfiles with a ``conanfile.txt`` instead of ``conanfile.py``. `#5894 <https://github.com/conan-io/conan/pull/5894>`_
- Bugfix: Fix incorrect propagation of build-requires to downstream consumers, resulting in missing dependencies in ``deps_cpp_info``. `#5886 <https://github.com/conan-io/conan/pull/5886>`_
- Bugfix: Adds the `short_paths_home` property to `ConanClientConfigParser` to validate that it is not a subdirectory of the conan cache. `#5864 <https://github.com/conan-io/conan/pull/5864>`_ . Docs `here <https://github.com/conan-io/docs/pull/1436>`__
- Bugfix: Use imported python requires' `short_path` value instead of the defined in the `conanfile` that imports it. `#5841 <https://github.com/conan-io/conan/pull/5841>`_
- Bugfix: Avoid repeated copies of absolute paths when using `self.copy()`. `#5792 <https://github.com/conan-io/conan/pull/5792>`_
- Bugfix: Downstream overrides to exact dependencies versions are always used, even if the upstream has a version range that does not satisfy the override. `#5713 <https://github.com/conan-io/conan/pull/5713>`_


1.19.3 (29-Oct-2019)
--------------------

- Fix: Fixed range of pylint and astroid requirements to keep compatibility with python 2 `#5987 <https://github.com/conan-io/conan/pull/5987>`_
- Fix: Force ``conan search --query`` queries to be resolved always in the client to avoid servers failures due to unsupported syntax `#5970 <https://github.com/conan-io/conan/pull/5970>`_
- Bugfix: Use cpp_info.name lower case in pkg-config generator when defined `#5988 <https://github.com/conan-io/conan/pull/5988>`_
- Bugfix: Fix ``cpp_info.name`` not used in cmake find generators for dependencies `#5973 <https://github.com/conan-io/conan/pull/5973>`_
- Bugfix: Fixed bug when overriden dependencies that don't exist and make the CMake generated code crash `#5971 <https://github.com/conan-io/conan/pull/5971>`_
- Bugfix: Fixed bug when overriden dependencies that don't exist and make the CMake generated code crash `#5945 <https://github.com/conan-io/conan/pull/5945>`_


1.19.2 (16-Oct-2019)
--------------------

- Feature: Implement ``self.info.shared_library_package_id()`` to better manage shared libraries package-ID, specially when they depend on static libraries `#5893 <https://github.com/conan-io/conan/pull/5893>`_ . Docs `here <https://github.com/conan-io/docs/pull/1442>`__
- Bugfix: Allow ``conan install pkg/[*]@user/channel`` resolving to a reference, not a path. `#5908 <https://github.com/conan-io/conan/pull/5908>`_
- Bugfix: The dependency overriding mechanism was not working properly when using the same version with different build metadata (`1.2.0+xyz` vs `1.2.0+abc`). `#5903 <https://github.com/conan-io/conan/pull/5903>`_
- Bugfix: Artifactory was returning an error on the first login attempt because the server capabilities were not assigned correctly. `#5880 <https://github.com/conan-io/conan/pull/5880>`_
- Bugfix: conan export failed if there is no user/channel and a lockfile is applied `#5875 <https://github.com/conan-io/conan/pull/5875>`_
- Bugfix: SCM component failed for url pointing to local path in Windows with backslash. `#5875 <https://github.com/conan-io/conan/pull/5875>`_
- Bugfix: Fix `conan graph build-order` output so it uses references including its recipe revision `#5863 <https://github.com/conan-io/conan/pull/5863>`_


1.19.1 (3-Oct-2019)
-------------------

- Bugfix: Use imported python requires' `short_path` value instead of the defined in the `conanfile` that imports it. `#5849 <https://github.com/conan-io/conan/pull/5849>`_
- Bugfix: Fix regression in ``visual_studio`` generator adding a ``<Lib>`` task. `#5846 <https://github.com/conan-io/conan/pull/5846>`_ . Docs `here <https://github.com/conan-io/docs/pull/1430>`__


1.19.0 (30-Sept-2019)
---------------------

- Feature: Update settings.yml file with macOS, watchOS, tvOS, iOS version numbers `#5823 <https://github.com/conan-io/conan/pull/5823>`_
- Feature: Add clang 9 to the settings.yml file `#5786 <https://github.com/conan-io/conan/pull/5786>`_ . Docs `here <https://github.com/conan-io/docs/pull/1420>`__
- Feature: Show suggestions when typing an incorrect command conan command. `#5725 <https://github.com/conan-io/conan/pull/5725>`_
- Feature: Client support for using refresh tokens in the auth process with Artifactory. `#5662 <https://github.com/conan-io/conan/pull/5662>`_
- Feature: Add GCC  9.2 to default settings.yml file `#5650 <https://github.com/conan-io/conan/pull/5650>`_ . Docs `here <https://github.com/conan-io/docs/pull/1394>`__
- Feature: Add subcommand for enabling and disabling remotes `#5623 <https://github.com/conan-io/conan/pull/5623>`_ . Docs `here <https://github.com/conan-io/docs/pull/1392>`__
- Feature: New `conan config home` command for getting Conan home directory `#5613 <https://github.com/conan-io/conan/pull/5613>`_ . Docs `here <https://github.com/conan-io/docs/pull/1387>`__
- Feature: Adds `name` attribute to `CppInfo` and use `cpp_info.name` in all CMake and pkg-config generators as the find scripts files names, target names, etc. `#5598 <https://github.com/conan-io/conan/pull/5598>`_ . Docs `here <https://github.com/conan-io/docs/pull/1393>`__
- Feature: Enhanced vs-generator by providing more properties that can be referenced by other projects; added library paths also to <Lib> so it's possible to compile static libraries that reference other libs `#5564 <https://github.com/conan-io/conan/pull/5564>`_
- Feature: Better support OSX frameworks by declaring `cppinfo.frameworks`. `#5552 <https://github.com/conan-io/conan/pull/5552>`_ . Docs `here <https://github.com/conan-io/docs/pull/1414>`__
- Feature: Virtual environment generator for gathering only the PYTHONPATH. `#5511 <https://github.com/conan-io/conan/pull/5511>`_ . Docs `here <https://github.com/conan-io/docs/pull/1369>`__
- Fix: :command:`conan upload` with a reference without user and channel and package id ``name/version:package_id`` should work `#5824 <https://github.com/conan-io/conan/pull/5824>`_
- Fix: Dropped support for python 3.4.  That version is widely being dropped by the python community. Since Conan 1.19, the tests won't be run with python 3.4 and we won't be aware if something is not working correctly. `#5820 <https://github.com/conan-io/conan/pull/5820>`_ . Docs `here <https://github.com/conan-io/docs/pull/1424>`__
- Fix: Apply lockfile to the node before updating with downstream requirements `#5771 <https://github.com/conan-io/conan/pull/5771>`_
- Fix: Make :command:`conan new` generate default options as a dictionary `#5767 <https://github.com/conan-io/conan/pull/5767>`_
- Fix: Output  search result for remotes in order by version, as local search `#5723 <https://github.com/conan-io/conan/pull/5723>`_
- Fix: Excluded also `ftp_proxy` and `all_proxy` variables from the environment when proxy configuration is specified in the `conan.conf` file. `#5697 <https://github.com/conan-io/conan/pull/5697>`_
- Fix: Relax restriction on the future python dependency `#5692 <https://github.com/conan-io/conan/pull/5692>`_
- Fix: Call `post_package` hook before computing the manifest `#5647 <https://github.com/conan-io/conan/pull/5647>`_
- Fix: Show friendly message when can't get remote path `#5638 <https://github.com/conan-io/conan/pull/5638>`_
- Fix: Detect the number of CPUs used by Docker (#5464) `#5466 <https://github.com/conan-io/conan/pull/5466>`_ . Docs `here <https://github.com/conan-io/docs/pull/1359>`__
- Bugfix: Set Ninja to use `cpu_count` value when building with `parallel` option with CMake `#5832 <https://github.com/conan-io/conan/pull/5832>`_
- Bugfix: output of references without user/channel is done with _/_, like in lockfiles. `#5817 <https://github.com/conan-io/conan/pull/5817>`_
- Bugfix: A lockfile generated from a consumer should be able to generate a build-order too. `#5800 <https://github.com/conan-io/conan/pull/5800>`_
- Bugfix: Fix system detection on Solaris. `#5630 <https://github.com/conan-io/conan/pull/5630>`_
- Bugfix: `SVN` uses `username` and `password` if provided `#5601 <https://github.com/conan-io/conan/pull/5601>`_
- Bugfix: Use the final package folder as the `conanfile.package_folder` attribute for the `pre_package` hook. `#5600 <https://github.com/conan-io/conan/pull/5600>`_
- BugFix: Fix crash with custom generators using ``install_folder`` `#5569 <https://github.com/conan-io/conan/pull/5569>`_


1.18.5 (24-Sept-2019)
---------------------

- Bugfix: A `bug <https://github.com/urllib3/urllib3/issues/1683>`_ in `urllib3` caused bad encoded URLs causing failures when using any repository from Bintray, like `conan-center`. `#5801 <https://github.com/conan-io/conan/pull/5801>`_


1.18.4 (12-Sept-2019)
---------------------

- Fix: ``package_id`` should be used for ``recipe_revision_mode`` `#5729 <https://github.com/conan-io/conan/pull/5729>`_ . Docs `here <https://github.com/conan-io/docs/pull/1410>`__


1.18.3 (10-Sept-2019)
---------------------

- Fix: Version ranges resolution using references without user/channel `#5707 <https://github.com/conan-io/conan/pull/5707>`_


1.18.2 (30-Aug-2019)
--------------------

- Feature: Add opt-out for Git shallow clone in `SCM` feature `#5677 <https://github.com/conan-io/conan/pull/5677>`_ . Docs `here <https://github.com/conan-io/docs/pull/1400>`__
- Fix: Use the value of argument `useEnv` provided by the user to the `MSBuild` helper also to adjust `/p:UseEnv=false` when the arg is `False`. `#5609 <https://github.com/conan-io/conan/pull/5609>`_
- Bugfix: Fixed assertion when using nested build_requires that depend on packages that are also used in the main dependency graph `#5689 <https://github.com/conan-io/conan/pull/5689>`_
- Bugfix: When Artifactory doesn't have the anonymous access activated, the conan client wasn't able to capture the server capabilities and therefore never used the `revisions` mechanism. `#5688 <https://github.com/conan-io/conan/pull/5688>`_
- Bugfix: When no `user/channel` is specified creating a package, upload it to a remote using  `None` as the "folder" in the storage, instead of `_`. `#5671 <https://github.com/conan-io/conan/pull/5671>`_
- Bugfix: Using the version ranges mechanism Conan wasn't able to resolve the correct reference if a library with the same name but different user/channel was found in an earlier remote. `#5657 <https://github.com/conan-io/conan/pull/5657>`_
- Bugfix: Broken cache package collection for packages without user/channel `#5607 <https://github.com/conan-io/conan/pull/5607>`_


1.18.1 (8-Aug-2019)
-------------------

- Bugfix: The `scm` feature was trying to run a checkout after a shallow clone. `#5571 <https://github.com/conan-io/conan/pull/5571>`_


1.18.0 (30-Jul-2019)
--------------------

- Feature: The "user/channel" fields are now optional. e.g: `conan create .` is valid if the `name` and `version` are declared in the recipe. e.g: `conan create . lib/1.0@` to omit user and channel. The same for other commands. The `user` and `channel` can also be omitted while specifying requirements in the conanfiles. `#5381 <https://github.com/conan-io/conan/pull/5381>`_ . Docs `here <https://github.com/conan-io/docs/pull/1375>`__
- Feature: Output current revision from references in local cache when using a pattern `#5537 <https://github.com/conan-io/conan/pull/5537>`_ . Docs `here <https://github.com/conan-io/docs/pull/1381>`__
- Feature: New parameter ``--skip-auth`` for the :command:`conan user` command to avoid trying to authenticate when the client already has credentials stored. `#5532 <https://github.com/conan-io/conan/pull/5532>`_ . Docs `here <https://github.com/conan-io/docs/pull/1377>`__
- Feature: Allow patterns in per-package settings definitions, not only the package name `#5523 <https://github.com/conan-io/conan/pull/5523>`_ . Docs `here <https://github.com/conan-io/docs/pull/1372>`__
- Feature: Search custom settings (#5378) `#5521 <https://github.com/conan-io/conan/pull/5521>`_ . Docs `here <https://github.com/conan-io/docs/pull/1371>`__
- Feature: shallow git clone `#5514 <https://github.com/conan-io/conan/pull/5514>`_ . Docs `here <https://github.com/conan-io/docs/pull/1380>`__
- Fix: Remove ``conan graph clean-modified`` command, it is automatic and no longer necessary. `#5533 <https://github.com/conan-io/conan/pull/5533>`_ . Docs `here <https://github.com/conan-io/docs/pull/1378>`__
- Fix: Incomplete references (for local conanfile.py files) are not printed with `@None/None` anymore. `#5509 <https://github.com/conan-io/conan/pull/5509>`_
- Fix: Discard empty string values in SCM including `subfolder` `#5459 <https://github.com/conan-io/conan/pull/5459>`_
- Bugfix: The `stderr` was not printed when a command failed running the `tools.check_output` function. `#5548 <https://github.com/conan-io/conan/pull/5548>`_
- Bugfix: Avoid dependency (mainly build-requires) being marked as skipped when another node exists in the graph that is being skipped because of being private `#5547 <https://github.com/conan-io/conan/pull/5547>`_
- Bugfix: fix processing of UTF-8 files with BOM `#5506 <https://github.com/conan-io/conan/pull/5506>`_
- Bugfix: apply http.sslVerify to the current Git command only `#5470 <https://github.com/conan-io/conan/pull/5470>`_
- Bugfix: Do not raise when accessing the metadata of editable packages `#5461 <https://github.com/conan-io/conan/pull/5461>`_
- Bugfix: Use cxxFlags instead of cppFlags in ``qbs`` generator. `#5452 <https://github.com/conan-io/conan/pull/5452>`_ . Docs `here <https://github.com/conan-io/docs/pull/1354>`__


1.17.2 (25-Jul-2019)
--------------------

- Bugfix: Lock transitive python-requires in lockfiles, not only direct ones. `#5531 <https://github.com/conan-io/conan/pull/5531>`_


1.17.1 (22-Jul-2019)
--------------------

- Feature: support 7.1 clang version `#5492 <https://github.com/conan-io/conan/pull/5492>`_
- Bugfix: When a profile was detected, for GCC 5.X the warning message about the default `libcxx` was not shown. `#5524 <https://github.com/conan-io/conan/pull/5524>`_
- Bugfix: Update python-dateutil dependency to ensure availability of `dateutil.parser.isoparse` `#5485 <https://github.com/conan-io/conan/pull/5485>`_
- Bugfix: Solve regression in ``conan info <ref>`` command, incorrectly reading the graph_info.json and lockfiles `#5481 <https://github.com/conan-io/conan/pull/5481>`_
- Bugfix: Trailing files left when packages are not found in conan info and install, restricted further installs with different case in Windows, without ``rm -rf ~/.conan/data/pkg_name`` `#5480 <https://github.com/conan-io/conan/pull/5480>`_
- Bugfix: The lock files mechanism now allows to update a node providing new information, like a retrieved package revision, if the "base" reference was the same. `#5467 <https://github.com/conan-io/conan/pull/5467>`_
- Bugfix: search command table output has invalid HTML code syntax `#5460 <https://github.com/conan-io/conan/pull/5460>`_


1.17.0 (9-Jul-2019)
-------------------

- Feature: Better UX for no_proxy (#3943) `#5438 <https://github.com/conan-io/conan/pull/5438>`_ . Docs `here <https://github.com/conan-io/docs/pull/1347>`__
- Feature: Show warning when URLs for remotes is invalid (missing schema, host, etc). `#5418 <https://github.com/conan-io/conan/pull/5418>`_
- Feature: Implementation of lockfiles. Lockfiles store in a file all the configuration, exact versions (including revisions), necessary to achieve reproducible builds, even when using version-ranges or package revisions. `#5412 <https://github.com/conan-io/conan/pull/5412>`_ . Docs `here <https://github.com/conan-io/docs/pull/1350>`__
- Feature: Change progress bar output to tqdm to make it look better `#5407 <https://github.com/conan-io/conan/pull/5407>`_
- Feature: Define 2 new modes and helpers for the package binary ID: ``recipe_revision_mode`` and ``package_revision_mode``, that take into account the revisions. The second one will use all the information from dependencies, resulting in fully deterministic and complete package IDs: if some dependency change, it will be necessary to build a new binary of consumers `#5363 <https://github.com/conan-io/conan/pull/5363>`_ . Docs `here <https://github.com/conan-io/docs/pull/1345>`__
- Feature: Add apple-clang 11.0 to settings.yml (#5328) `#5357 <https://github.com/conan-io/conan/pull/5357>`_ . Docs `here <https://github.com/conan-io/docs/pull/1327>`__
- Feature: SystemPackageTool platform detection (#5026) `#5215 <https://github.com/conan-io/conan/pull/5215>`_ . Docs `here <https://github.com/conan-io/docs/pull/1291>`__
- Fix: Enable the definition of revisions in conanfile.txt `#5435 <https://github.com/conan-io/conan/pull/5435>`_
- Fix: Improve resolution of version ranges for remotes `#5433 <https://github.com/conan-io/conan/pull/5433>`_
- Fix: The conan process returns `6` when a `ConanInvalidConfiguration` is thrown during :command:`conan info`. `#5421 <https://github.com/conan-io/conan/pull/5421>`_
- Fix: Inspect missing attribute is not an error (#3953) `#5419 <https://github.com/conan-io/conan/pull/5419>`_
- Fix: Allow --build-order and --graph together for conan info (#3447) `#5417 <https://github.com/conan-io/conan/pull/5417>`_
- Fix: Handling error when reference not found using conan download `#5399 <https://github.com/conan-io/conan/pull/5399>`_
- Fix: Update Yum cache (#5370) `#5387 <https://github.com/conan-io/conan/pull/5387>`_
- Fix: Remove old folder for conan install (#5376) `#5384 <https://github.com/conan-io/conan/pull/5384>`_
- Fix: Add missing call to super constructor to `VirtualEnvGenerator`. `#5375 <https://github.com/conan-io/conan/pull/5375>`_
- Fix: Force forward slashes in the variable `$PROFILE_DIR` `#5373 <https://github.com/conan-io/conan/pull/5373>`_ . Docs `here <https://github.com/conan-io/docs/pull/1333>`__
- Fix: Accept a list for the requires attribute `#5371 <https://github.com/conan-io/conan/pull/5371>`_ . Docs `here <https://github.com/conan-io/docs/pull/1332>`__
- Fix: Remove packages when version is asterisk (#5297) `#5346 <https://github.com/conan-io/conan/pull/5346>`_
- Fix: Make conan_data visible to pylint (#5327) `#5337 <https://github.com/conan-io/conan/pull/5337>`_
- Fix: Improve the output to show the remote (or cache) that a version range is resolved to. `#5336 <https://github.com/conan-io/conan/pull/5336>`_
- Fix: Deprecated ``conan copy|download|upload <ref> -p=ID``, use ``conan .... <pref>`` instead `#5293 <https://github.com/conan-io/conan/pull/5293>`_ . Docs `here <https://github.com/conan-io/docs/pull/1317>`__
- Fix: `AutoToolsBuildEnvironment` is now aware of `os_target` and `arch_target` to calculate the gnu triplet when declared. `#5283 <https://github.com/conan-io/conan/pull/5283>`_
- Fix: Better message for gcc warning of libstdc++ at default profile detection `#5275 <https://github.com/conan-io/conan/pull/5275>`_
- Bugfix: `verify_ssl` field in SCM being discarded when used with `False` value. `#5441 <https://github.com/conan-io/conan/pull/5441>`_
- Bugfix: enable retry for requests `#5400 <https://github.com/conan-io/conan/pull/5400>`_
- Bugfix: Allow creation and deletion of files in ``tools.patch`` with ``strip>0`` `#5334 <https://github.com/conan-io/conan/pull/5334>`_
- Bugfix: Use case insensitive comparison for SHA256 checksums `#5306 <https://github.com/conan-io/conan/pull/5306>`_



1.16.1 (14-Jun-2019)
--------------------

- Feature: Print nicer error messages when receive an error from Artifactory. `#5326 <https://github.com/conan-io/conan/pull/5326>`_
- Fix: Make ``conan config get storage.path`` return an absolute, resolved path `#5350 <https://github.com/conan-io/conan/pull/5350>`_
- Fix: Skipped the compiler version check in the cmake generator when a `-s compiler.toolset` is specified (Visual Studio). `#5348 <https://github.com/conan-io/conan/pull/5348>`_
- Fix: Constraint transitive dependency ``typed-ast`` (required by astroid) in python3.4, as they stopped releasing wheels, and it fails to build in some Windows platforms with older SDKs. `#5324 <https://github.com/conan-io/conan/pull/5324>`_
- Fix: Accept v140 and VS 15.0 for CMake generator (#5318) `#5321 <https://github.com/conan-io/conan/pull/5321>`_
- Fix: Accept only .lib and .dll as Visual extensions (#5316) `#5319 <https://github.com/conan-io/conan/pull/5319>`_
- Bugfix: Do not copy directories inside a symlinked one `#5342 <https://github.com/conan-io/conan/pull/5342>`_
- Bugfix: Conan was retrying the upload when failed with error 400 (request error). `#5326 <https://github.com/conan-io/conan/pull/5326>`_


1.16.0 (4-Jun-2019)
-------------------

- Feature: The :command:`conan upload` command can receive now the full package reference to upload a binary package. The `-p` argument is now deprecated. `#5224 <https://github.com/conan-io/conan/pull/5224>`_ . Docs `here <https://github.com/conan-io/docs/pull/1300>`__
- Feature: Add hooks `pre_package_info` and `post_package_info` `#5223 <https://github.com/conan-io/conan/pull/5223>`_ . Docs `here <https://github.com/conan-io/docs/pull/1293>`__
- Feature: New build mode `--build cascade` that forces building from sources any node with dependencies also built from sources. `#5218 <https://github.com/conan-io/conan/pull/5218>`_ . Docs `here <https://github.com/conan-io/docs/pull/1296>`__
- Feature: Print errors and warnings to `stderr` `#5206 <https://github.com/conan-io/conan/pull/5206>`_
- Feature: New ``conan new --template=mytemplate`` to initialize recipes with your own templates `#5189 <https://github.com/conan-io/conan/pull/5189>`_ . Docs `here <https://github.com/conan-io/docs/pull/1286>`__
- Feature: Allow using wildcards to remove system requirements sentinel from cache. `#5176 <https://github.com/conan-io/conan/pull/5176>`_ . Docs `here <https://github.com/conan-io/docs/pull/1294>`__
- Feature: Implement conan.conf ``retry`` and ``retry-wait`` and ``CONAN_RETRY`` and ``CONAN_RETRY_WAIT`` to configure all retries for all transfers, including upload, download, and ``tools.download()``. `#5174 <https://github.com/conan-io/conan/pull/5174>`_ . Docs `here <https://github.com/conan-io/docs/pull/1295>`__
- Feature: Support yaml lists in workspace ``root`` field. `#5156 <https://github.com/conan-io/conan/pull/5156>`_ . Docs `here <https://github.com/conan-io/docs/pull/1288>`__
- Feature: Add gcc 8.3 and 9.1 new versions to default *settings.yml* `#5112 <https://github.com/conan-io/conan/pull/5112>`_
- Feature: Retry upload or download for error in response message (e.g. status is '500') `#4984 <https://github.com/conan-io/conan/pull/4984>`_
- Fix: Do not retry file transfer operations for 401 and 403 auth and permissions errors. `#5278 <https://github.com/conan-io/conan/pull/5278>`_
- Fix: Copy symlinked folder when using `merge_directories` function `#5237 <https://github.com/conan-io/conan/pull/5237>`_
- Fix: Add the ability to avoid the `/verbosity` argument in CMake command line for MSBuild `#5220 <https://github.com/conan-io/conan/pull/5220>`_ . Docs `here <https://github.com/conan-io/docs/pull/1292>`__
- Fix: self.copy with symlinks=True does not copy symlink if the .conan directory is a symlink #5114 `#5125 <https://github.com/conan-io/conan/pull/5125>`_
- Fix: Export detected_os from tools.oss (#5101) `#5102 <https://github.com/conan-io/conan/pull/5102>`_ . Docs `here <https://github.com/conan-io/docs/pull/1276>`__
- Fix: Use `revision` as the SVN's `peg_revision` (broken for an edge case) `#5029 <https://github.com/conan-io/conan/pull/5029>`_
- Bugfix: ``--update`` was not updating ``python_requires`` using version ranges. `#5265 <https://github.com/conan-io/conan/pull/5265>`_
- Bugfix: ``visual_studio`` generator only adds ".lib" extension for lib names without extension, otherwise (like ".a") respect it. `#5254 <https://github.com/conan-io/conan/pull/5254>`_
- Bugfix: Fix :command:`conan search` command showing revisions timestamps in a different time offset than UTC. `#5232 <https://github.com/conan-io/conan/pull/5232>`_
- Bugfix: Meson build-helper gets correct compiler flags, AutoTools build environment adds compiler.runtime flags `#5222 <https://github.com/conan-io/conan/pull/5222>`_
- Bugfix: The `cmake_multi` generator was not managing correctly the `RelWithDebInfo` and `MinSizeRel` build types. `#5221 <https://github.com/conan-io/conan/pull/5221>`_
- Bugfix: Check that registry file exists before removing it `#5219 <https://github.com/conan-io/conan/pull/5219>`_
- Bugfix: do not append "-T " if generator doesn't support it `#5201 <https://github.com/conan-io/conan/pull/5201>`_
- Bugfix: :command:`conan download` always retrieve the sources, also with ``--recipe`` argument, which should only skip download binaries, not the sources. `#5194 <https://github.com/conan-io/conan/pull/5194>`_
- Bugfix: Using `scm` declared in a superclass failed exporting the recipe with the error `ERROR: The conanfile.py defines more than one class level 'scm' attribute`. `#5185 <https://github.com/conan-io/conan/pull/5185>`_
- Bugfix: Conan command returns 6 (Invalid configuration) also when the settings are restricted in the recipe `#5178 <https://github.com/conan-io/conan/pull/5178>`_
- Bugfix: Make sure that proxy "http_proxy", "https_proxy", "no_proxy" vars are correctly removed if custom ones are defined in the conan.conf. Also, avoid using ``urllib.request.getproxies()``, they are broken. `#5162 <https://github.com/conan-io/conan/pull/5162>`_
- Bugfix: Use `copy()` for deploy generator so that permissions of files are preserved. Required if you want to use the deploy generator to deploy executables. `#5136 <https://github.com/conan-io/conan/pull/5136>`_


1.15.4
------

- Fix: Accept v140 and VS 15.0 for CMake generator (#5318) `#5331 <https://github.com/conan-io/conan/pull/5331>`_
- Fix: Constraint transitive dependency typed-ast (required by astroid) in python3.4, as they stopped releasing wheels, and it fails to build in some Windows platforms with older SDKs. `#5331 <https://github.com/conan-io/conan/pull/5331>`_


1.15.3
------

- Please, do not use this version, there was a critical error in the release process and changes from the 1.16 branch were merged.


1.15.2 (31-May-2019)
--------------------

- Bugfix: Fix bug with python-requires not being updated with ``--update`` if using version-ranges. `#5266 <https://github.com/conan-io/conan/pull/5266>`_
- Bugfix: Fix computation of ancestors performance regression `#5260 <https://github.com/conan-io/conan/pull/5260>`_


1.15.1 (16-May-2019)
---------------------

- Fix: Fix regression of ``conan remote update --insert`` using the same URL it had before `#5110 <https://github.com/conan-io/conan/pull/5110>`_
- Fix: Fix migration of *registry.json|txt* file including reference to non existing remotes. `#5103 <https://github.com/conan-io/conan/pull/5103>`_
- Bugfix: Avoid crash of commands copy, imports, editable-add for packages using python_requires `#5150 <https://github.com/conan-io/conan/pull/5150>`_


1.15.0 (6-May-2019)
--------------------

- Feature: Updated the generated *conanfile.py* in :command:`conan new` to the new `conan-io/hello <https://github.com/conan-io/hello>`_ repository `#5069 <https://github.com/conan-io/conan/pull/5069>`_ . Docs `here <https://github.com/conan-io/docs/pull/1269>`__
- Feature: The `MSBuild` build helper allows the parameter `toolset` with `False` value to skip the toolset adjustment. `#5052 <https://github.com/conan-io/conan/pull/5052>`_ . Docs `here <https://github.com/conan-io/docs/pull/1260>`__
- Feature: Add GCC 9 to default settings.yml `#5046 <https://github.com/conan-io/conan/pull/5046>`_ . Docs `here <https://github.com/conan-io/docs/pull/1257>`__
- Feature: You can disable broken symlinks checks when packaging using `CONAN_SKIP_BROKEN_SYMLINKS_CHECK` env var or `config.skip_broken_symlinks_check=1` `#4991 <https://github.com/conan-io/conan/pull/4991>`_ . Docs `here <https://github.com/conan-io/docs/pull/1272>`__
- Feature: New ``deploy`` generator to export files from a dependency graph to an installation folder `#4972 <https://github.com/conan-io/conan/pull/4972>`_ . Docs `here <https://github.com/conan-io/docs/pull/1262>`__
- Feature: Create `tools.Version` with _limited_ capabilities `#4963 <https://github.com/conan-io/conan/pull/4963>`_ . Docs `here <https://github.com/conan-io/docs/pull/1253>`__
- Feature: Default filename for workspaces: `conanws.yml` (used in install command) `#4941 <https://github.com/conan-io/conan/pull/4941>`_ . Docs `here <https://github.com/conan-io/docs/pull/1243>`__
- Feature: Add install folder to command 'conan workspace install' `#4940 <https://github.com/conan-io/conan/pull/4940>`_ . Docs `here <https://github.com/conan-io/docs/pull/1261>`__
- Feature: Add `compiler.cppstd` setting (mark `cppstd` as deprecated) `#4917 <https://github.com/conan-io/conan/pull/4917>`_ . Docs `here <https://github.com/conan-io/docs/pull/1266>`__
- Feature: Add a `--raw` argument to :command:`conan inspect` command to get an output only with the value of the requested attributes `#4903 <https://github.com/conan-io/conan/pull/4903>`_ . Docs `here <https://github.com/conan-io/docs/pull/1240>`__
- Feature: ``tools.get()`` and ``tools.unzip()`` now handle also ``.gz`` compressed files `#4883 <https://github.com/conan-io/conan/pull/4883>`_ . Docs `here <https://github.com/conan-io/docs/pull/1230>`__
- Feature: Add argument `--force` to command `profile new` to overwrite existing one `#4880 <https://github.com/conan-io/conan/pull/4880>`_ . Docs `here <https://github.com/conan-io/docs/pull/1176>`__
- Feature: Get commit message `#4877 <https://github.com/conan-io/conan/pull/4877>`_ . Docs `here <https://github.com/conan-io/docs/pull/1175>`__
- Fix: Remove sudo from Travis CI template `#5073 <https://github.com/conan-io/conan/pull/5073>`_ . Docs `here <https://github.com/conan-io/docs/pull/1270>`__
- Fix: Handle quoted path and libraries in the premake generator `#5051 <https://github.com/conan-io/conan/pull/5051>`_
- Fix: A simple addition to ensure right compiler version is found on windows. `#5041 <https://github.com/conan-io/conan/pull/5041>`_
- Fix: Include CMAKE_MODULE_PATH for CMake find_dependency (#4956) `#5021 <https://github.com/conan-io/conan/pull/5021>`_
- Fix: Add default_package_id_mode in the default conan.conf (#4947) `#5005 <https://github.com/conan-io/conan/pull/5005>`_ . Docs `here <https://github.com/conan-io/docs/pull/1248>`__
- Fix: Use back slashes for ``visual_studio`` generator instead of forward slashes `#5003 <https://github.com/conan-io/conan/pull/5003>`_
- Fix: Adding `subparsers.required = True` makes both Py2 and Py3 print an error when no arguments are entered in commands that have subarguments `#4902 <https://github.com/conan-io/conan/pull/4902>`_
- Fix: Example bare package recipe excludes `conanfile.py` from copy `#4892 <https://github.com/conan-io/conan/pull/4892>`_
- Fix: More meaningful error message when a remote communication fails to try to download a binary package. `#4888 <https://github.com/conan-io/conan/pull/4888>`_
- Bugfix: ``conan upload --force`` force also the upload of package binaries, not only recipes `#5088 <https://github.com/conan-io/conan/pull/5088>`_
- BugFix: MSYS 3.x detection `#5078 <https://github.com/conan-io/conan/pull/5078>`_
- Bugfix: Don't crash when an editable declare a ``build_folder`` in the layout, but not used in a workspace `#5070 <https://github.com/conan-io/conan/pull/5070>`_
- Bugfix: Made compatible the `cmake_find_package_multi` generator with `CMake < 3.9` `#5042 <https://github.com/conan-io/conan/pull/5042>`_
- Bugfix: Fix broken local development flow (:command:`conan source`, :command:`conan build`, :command:`conan package`, :command:`conan export-pkg`) with recipes with ``python-requires`` `#4979 <https://github.com/conan-io/conan/pull/4979>`_
- Bugfix: 'tar_extract' function was failing if there was a linked folder in the working dir that matches one inside the tar file. Now we use the `destination_dir` as base directory to check this condition. `#4965 <https://github.com/conan-io/conan/pull/4965>`_
- Bugfix: Remove package folder in :command:`conan create` even when using ``--keep-build`` `#4918 <https://github.com/conan-io/conan/pull/4918>`_


1.14.5 (30-Apr-2019)
--------------------

- Bugfix: Uncompressing a `tgz` package with a broken symlink failed while touching the destination file. `#5065 <https://github.com/conan-io/conan/pull/5065>`_
- Bugfix: The symlinks compressed in a `tgz` had invalid nonzero size. `#5064 <https://github.com/conan-io/conan/pull/5064>`_
- Bugfix: Fixing exception of transitive build-requires mixed with normal requires `#5056 <https://github.com/conan-io/conan/pull/5056>`_


1.14.4 (25-Apr-2019)
--------------------

- Bugfix: Fixed error while using Visual Studio 2019 with Ninja generator. `#5028 <https://github.com/conan-io/conan/pull/5028>`_
- Bugfix: Fixed error while using Visual Studio 2019 with Ninja generator. `#5025 <https://github.com/conan-io/conan/pull/5025>`_
- Bugfix: Solved errors in concurrent uploads of same recipe `#5014 <https://github.com/conan-io/conan/pull/5014>`_
- Bugfix: Fixed a bug that intermittently raised  `ERROR: 'NoneType' object has no attribute 'file_sums'` when uploading a recipe. `#5012 <https://github.com/conan-io/conan/pull/5012>`_
- Bugfix: Bug in `cmake_find_package_multi` caused `CMake` to find incorrect modules in `CMake` modules paths when only `Config` files should be taken into account. `#4995 <https://github.com/conan-io/conan/pull/4995>`_
- Bugfix: Fix skipping binaries because of transitive ``private`` requirements `#4987 <https://github.com/conan-io/conan/pull/4987>`_
- Bugfix: Fix broken local development flow (conan source, conan build, conan package, conan export-pkg) with recipes with python-requires `#4983 <https://github.com/conan-io/conan/pull/4983>`_


1.14.3 (11-Apr-2019)
--------------------

- Bugfix: ``build-requires`` and ``private`` requirements that resolve to a dependency that is already in the graph won't span a new node, nor will be ``build-requires`` or ``private``. They can conflict too. `#4937 <https://github.com/conan-io/conan/pull/4937>`_


1.14.2 (11-Apr-2019)
--------------------

- Bugfix: Run a full metadata migration in the cache to avoid old ``null`` revisions in package metadata `#4934 <https://github.com/conan-io/conan/pull/4934>`_


1.14.1 (1-Apr-2019)
-------------------

- Fix: Print a message for unhandled Conan errors building the API and collaborators `#4869 <https://github.com/conan-io/conan/pull/4869>`_
- Bugfix: Client does not require credentials for anonymous downloads from remotes. `#4872 <https://github.com/conan-io/conan/pull/4872>`_
- Bugfix: Fix a migration problem of ``conan config install`` for Conan versions 1.9 and older `#4870 <https://github.com/conan-io/conan/pull/4870>`_
- Feature: Now Conan will crush your enemies, see them driven before you, and to hear the lamentation of their women! (April's fools)


1.14.0 (28-Mar-2019)
--------------------

- Feature: support new architectures s390 and s390x `#4810 <https://github.com/conan-io/conan/pull/4810>`_ . Docs `here <https://github.com/conan-io/docs/pull/1140>`__
- Feature: `--build` parameter now applies fnmatching onto the whole reference, allowing to control rebuilding in a much broader way. `#4787 <https://github.com/conan-io/conan/pull/4787>`_ . Docs `here <https://github.com/conan-io/docs/pull/1141>`__
- Feature: Add config variable `general.error_on_override` and environment variable `CONAN_ERROR_ON_OVERRIDE` (defaulting to `False`) to configure if an overridden requirement should raise an error when overridden from downstream consumers. `#4771 <https://github.com/conan-io/conan/pull/4771>`_ . Docs `here <https://github.com/conan-io/docs/pull/1128>`__
- Feature: Allow to specify `revision_mode` for each recipe, values accepted are `scm` or `hash` (default) `#4767 <https://github.com/conan-io/conan/pull/4767>`_ . Docs `here <https://github.com/conan-io/docs/pull/1126>`__
- Feature: Sort library list name when calling tools.collect_libs `#4761 <https://github.com/conan-io/conan/pull/4761>`_ . Docs `here <https://github.com/conan-io/docs/pull/1124>`__
- Feature: Add `cmake_find_package_multi` generator. `#4714 <https://github.com/conan-io/conan/pull/4714>`_ . Docs `here <https://github.com/conan-io/docs/pull/1114>`__
- Feature: Implement ``--source-folder`` and ``--target-folder`` to ``conan config install`` command to select  subfolder to install from the source origin, and also the destination folder within the cache. `#4709 <https://github.com/conan-io/conan/pull/4709>`_ . Docs `here <https://github.com/conan-io/docs/pull/1131>`__
- Feature: Implement ``--update`` argument for ``python-requires`` too. `#4660 <https://github.com/conan-io/conan/pull/4660>`_
- Fix: Apply environment variables from profile and from requirements to :command:`conan export-pkg` `#4852 <https://github.com/conan-io/conan/pull/4852>`_
- Fix: Do not run `export_sources` automatically for python_requires `#4838 <https://github.com/conan-io/conan/pull/4838>`_
- Fix: Show the correct profile name when detect a new one (#4818) `#4824 <https://github.com/conan-io/conan/pull/4824>`_
- Fix: Allow using ``reference`` object in workspaces in templates for out of source builds `#4812 <https://github.com/conan-io/conan/pull/4812>`_ . Docs `here <https://github.com/conan-io/docs/pull/1135>`__
- Fix: Look for ``vswhere`` in ``PATH`` when using ``tools.vswhere()`` `#4805 <https://github.com/conan-io/conan/pull/4805>`_
- Fix: SystemPackageTools doesn't run sudo when it's not found (#4470) `#4774 <https://github.com/conan-io/conan/pull/4774>`_ . Docs `here <https://github.com/conan-io/docs/pull/1127>`__
- Fix: Show warning if repo is not pristine and using SCM mode to set the revisions `#4764 <https://github.com/conan-io/conan/pull/4764>`_
- Fix: avoid double call to ``package()`` method `#4748 <https://github.com/conan-io/conan/pull/4748>`_ . Docs `here <https://github.com/conan-io/docs/pull/1133>`__
- Fix: The `cmake_paths` generator now declares the `CONAN_XXX_ROOT` variables in case some exported cmake module file like `XXXConfig.cmake` has been patched with the `cmake.patch_config_paths()` to replace absolute paths to the local cache. `#4719 <https://github.com/conan-io/conan/pull/4719>`_ . Docs `here <https://github.com/conan-io/docs/pull/1115>`__
- Fix: Do not distribute the tests in the python package nor in the installers. `#4713 <https://github.com/conan-io/conan/pull/4713>`_
- Fix: add support for CMake generator platform `#4708 <https://github.com/conan-io/conan/pull/4708>`_ . Docs `here <https://github.com/conan-io/docs/pull/1125>`__
- Fix: Fix corrupted packages with missing conanmanifest.txt files `#4662 <https://github.com/conan-io/conan/pull/4662>`_
- Fix: Include information about all the configurations in the JSON generator `#4657 <https://github.com/conan-io/conan/pull/4657>`_ . Docs `here <https://github.com/conan-io/docs/pull/1129>`__
- Bugfix: Fixed authentication management when a server returns 401 uploading a file. `#4857 <https://github.com/conan-io/conan/pull/4857>`_
- Bugfix: Fixed recipe revision detection when some error output or unexpected output was printed to the stdout running the `git` command. `#4854 <https://github.com/conan-io/conan/pull/4854>`_
- Bugfix: The error output was piped to stdout causing issues while running git commands, especially during the detection of the scm revision `#4853 <https://github.com/conan-io/conan/pull/4853>`_
- Bugfix: :command:`conan export-pkg` should never resolve build-requires `#4851 <https://github.com/conan-io/conan/pull/4851>`_
- bugfix: The `--build` pattern was case sensitive depending on the os file system, now it is always case sensitive, following the :command:`conan search` behavior. `#4842 <https://github.com/conan-io/conan/pull/4842>`_
- Bugfix:  Fix metadata not being updated for :command:`conan export-pkg` when using  ``--package-folder`` `#4834 <https://github.com/conan-io/conan/pull/4834>`_
- Bugfix: `--build` parameter now is always case-sensitive, previously it depended to the file system type. `#4787 <https://github.com/conan-io/conan/pull/4787>`_ . Docs `here <https://github.com/conan-io/docs/pull/1141>`__
- Bugfix: Raise an error if source files cannot be correctly copied to build folder because of long paths in Windows. `#4766 <https://github.com/conan-io/conan/pull/4766>`_
- Bugfix: Use the same interface in ``conan_basic_setup()`` for the ``cmake_multi`` generator `#4721 <https://github.com/conan-io/conan/pull/4721>`_ . Docs `here <https://github.com/conan-io/docs/pull/1121>`__


1.13.3 (27-Mar-2019)
--------------------

- Bugfix: Revision computation failed when a git repo was present but without commits `#4830 <https://github.com/conan-io/conan/pull/4830>`_


1.13.2 (21-Mar-2019)
--------------------

- Bugfix: Installing a reference with "update" and "build outdated" options raised an exception. `#4790 <https://github.com/conan-io/conan/pull/4790>`_
- Bugfix: Solved bug with build-requires transitive build-requires `#4783 <https://github.com/conan-io/conan/pull/4783>`_
- Bugfix: Fixed workspace crash when no layout was specified `#4783 <https://github.com/conan-io/conan/pull/4783>`_
- Bugfix: Do not generate multiple ``add_subdirectories()`` for workspaces build-requires `#4783 <https://github.com/conan-io/conan/pull/4783>`_


1.13.1 (15-Mar-2019)
--------------------

- Bugfix: Fix computation of graph when transitive diamonds are processed. `#4737 <https://github.com/conan-io/conan/pull/4737>`_


1.13.0 (07-Mar-2019)
--------------------

- Feature: Added with_login parameter to tools.run_in_windows_bash() `#4673 <https://github.com/conan-io/conan/pull/4673>`_ . Docs `here <https://github.com/conan-io/docs/pull/1103>`__
- Feature: The `deb` and `windows` Conan installers now use Python 3. `#4663 <https://github.com/conan-io/conan/pull/4663>`_
- Feature: Allow configuring in *conan.conf* a different default ``package_id`` mode. `#4644 <https://github.com/conan-io/conan/pull/4644>`_ . Docs `here <https://github.com/conan-io/docs/pull/1106>`__
- Feature: Apply Jinja2 to layout files before parsing them `#4596 <https://github.com/conan-io/conan/pull/4596>`_ . Docs `here <https://github.com/conan-io/docs/pull/1093>`__
- Feature: Accept a PackageReference for the command  :command:`conan get` (argument `-p` is accepted, but hidden) `#4494 <https://github.com/conan-io/conan/pull/4494>`_ . Docs `here <https://github.com/conan-io/docs/pull/1070>`__
- Feature: Re-implement Workspaces based on Editable packages. `#4481 <https://github.com/conan-io/conan/pull/4481>`_ . Docs `here <https://github.com/conan-io/docs/pull/1086>`__
- Feature: Removed old "compatibility" mode of revisions. `#4462 <https://github.com/conan-io/conan/pull/4462>`_ . Docs `here <https://github.com/conan-io/docs/pull/1105>`__
- Fix: When revisions enabled, add the revision to the json output of the info/install commands. `#4667 <https://github.com/conan-io/conan/pull/4667>`_
- Fix: JSON output for `multi_config` now works in `install` and `create` commands `#4656 <https://github.com/conan-io/conan/pull/4656>`_
- Fix: Deprecate 'cppflags' in favor of 'cxxflags' in class CppInfo `#4611 <https://github.com/conan-io/conan/pull/4611>`_ . Docs `here <https://github.com/conan-io/docs/pull/1091>`__
- Fix: Return empty list if env variable is an empty string `#4594 <https://github.com/conan-io/conan/pull/4594>`_
- Fix: `conan profile list` will now recursively list profiles. `#4591 <https://github.com/conan-io/conan/pull/4591>`_
- Fix: `Instance of 'TestConan' has no 'install_folder' member` when exporting recipe `#4585 <https://github.com/conan-io/conan/pull/4585>`_
- Fix: SCM replacement with comments below it `#4580 <https://github.com/conan-io/conan/pull/4580>`_
- Fix: Remove package references associated to a remote in *registry.json* when that remote is deleted `#4568 <https://github.com/conan-io/conan/pull/4568>`_
- Fix:  Fixed issue with Artifactory when the anonymous user is enabled, causing the uploads to fail without requesting the user and password. `#4526 <https://github.com/conan-io/conan/pull/4526>`_
- Fix: Do not allow an alias to override an existing package `#4495 <https://github.com/conan-io/conan/pull/4495>`_
- Fix: Do not display the warning when there are files in the package folder (#4438). `#4464 <https://github.com/conan-io/conan/pull/4464>`_
- Fix: Renamed the :command:`conan link` command to :command:`conan editable` to put packages into editable mode. `#4481 <https://github.com/conan-io/conan/pull/4481>`_ . Docs `here <https://github.com/conan-io/docs/pull/1086>`__
- Bugfix: Solve problem with loading recipe python files in Python 3.7 because of ``module.__file__ = None`` `#4669 <https://github.com/conan-io/conan/pull/4669>`_
- Bugfix: Do not attempt to upload non-existing packages, due to empty short_paths folders, or to explicit ``upload -p=id`` command. `#4615 <https://github.com/conan-io/conan/pull/4615>`_
- Bugfix: Fix LIB overwrite in ``virtualbuildenv`` generator `#4583 <https://github.com/conan-io/conan/pull/4583>`_
- Bugfix: Avoid ``str(self.settings.xxx)`` crash when the value is None. `#4571 <https://github.com/conan-io/conan/pull/4571>`_ . Docs `here <https://github.com/conan-io/docs/pull/1089>`__
- Bugfix: Build-requires expand over the closure of the package they apply to, so they can create conflicts too. Previously, those conflicts were silently skipped, and builds would use an undetermined version and configuration of dependencies. `#4514 <https://github.com/conan-io/conan/pull/4514>`_
- Bugfix: meson build type actually reflects recipe shared option `#4489 <https://github.com/conan-io/conan/pull/4489>`_
- Bugfix: Fixed several bugs related to revisions. `#4462 <https://github.com/conan-io/conan/pull/4462>`_ . Docs `here <https://github.com/conan-io/docs/pull/1105>`__
- Bugfix: Fixed several bugs related to the package `metadata.json` `#4462 <https://github.com/conan-io/conan/pull/4462>`_ . Docs `here <https://github.com/conan-io/docs/pull/1105>`__


1.12.3 (18-Feb-2019)
--------------------

- Fix: Fix potential downgrade from future 1.13 to 1.12 `#4547 <https://github.com/conan-io/conan/pull/4547>`_
- Fix: Remove output warnings in MSBuild helper. `#4518 <https://github.com/conan-io/conan/pull/4518>`_
- Fix: Revert default cmake generator on Windows (#4265) `#4509 <https://github.com/conan-io/conan/pull/4509>`_ . Docs `here <https://github.com/conan-io/docs/pull/1072>`__
- Bugfix: Fixed problem with conanfile.txt [imports] sections using the '@' character. `#4539 <https://github.com/conan-io/conan/pull/4539>`_ . Docs `here <https://github.com/conan-io/docs/pull/1078>`__
- Bugfix: Fix search packages function when remote is called `all` `#4502 <https://github.com/conan-io/conan/pull/4502>`_


1.12.2 (8-Feb-2019)
-------------------

- Bugfix: Regression in ``MSBuild`` helper, incorrectly ignoring the ``conan_build.props`` file because of using a relative path instead of absolute one. `#4488 <https://github.com/conan-io/conan/pull/4488>`_


1.12.1 (5-Feb-2019)
-------------------

- Bugfix: GraphInfo parsing of existing ``graph_info.json`` files raises KeyError over "root". `#4458 <https://github.com/conan-io/conan/pull/4458>`_
- Bugfix: Transitive Editable packages fail to install `#4448 <https://github.com/conan-io/conan/pull/4448>`_


1.12.0 (30-Jan-2019)
--------------------

- Feature: Add JSON output to 'info' command `#4359 <https://github.com/conan-io/conan/pull/4359>`_ . Docs `here <https://github.com/conan-io/docs/pull/1050>`__
- Feature: Remove system requirements conan folders (not installed binaries) from cache `#4354 <https://github.com/conan-io/conan/pull/4354>`_ . Docs `here <https://github.com/conan-io/docs/pull/1038>`__
- Feature: Updated *CONTRIBUTING.md* with code style `#4348 <https://github.com/conan-io/conan/pull/4348>`_
- Feature: Updated OS versions for apple products `#4345 <https://github.com/conan-io/conan/pull/4345>`_
- Feature: add environment variable CONAN_CACHE_NO_LOCKS to simplify debugging `#4309 <https://github.com/conan-io/conan/pull/4309>`_ . Docs `here <https://github.com/conan-io/docs/pull/1019>`__
- Feature: The commands :command:`conan install`, :command:`conan info`, :command:`conan create` and :command:`conan export-pkg` now can receive multiple profile arguments. The applied profile will be the composition of them, prioritizing the latest applied. `#4308 <https://github.com/conan-io/conan/pull/4308>`_ . Docs `here <https://github.com/conan-io/docs/pull/1036>`__
- Feature: Added ``get_tag()`` methods to ``tools.Git()`` and ``tools.SVN()`` helpers. `#4306 <https://github.com/conan-io/conan/pull/4306>`_ . Docs `here <https://github.com/conan-io/docs/pull/1020>`__
- Feature: Package reference is now accepted as an argument in ``conan install --build`` `#4305 <https://github.com/conan-io/conan/pull/4305>`_ . Docs `here <https://github.com/conan-io/docs/pull/1017>`__
- Feature: define environment variables for CTest `#4299 <https://github.com/conan-io/conan/pull/4299>`_ . Docs `here <https://github.com/conan-io/docs/pull/1018>`__
- Feature: Added a configuration entry at the `conan.conf` file to be able to specify a custom `CMake` executable. `#4298 <https://github.com/conan-io/conan/pull/4298>`_ . Docs `here <https://github.com/conan-io/docs/pull/1025>`__
- Feature: Skip "README.md" and "LICENSE.txt" during the installation of a custom config via `conan config install`. `#4259 <https://github.com/conan-io/conan/pull/4259>`_ . Docs `here <https://github.com/conan-io/docs/pull/1016>`__
- Feature: allow to specify MSBuild verbosity level `#4251 <https://github.com/conan-io/conan/pull/4251>`_ . Docs `here <https://github.com/conan-io/docs/pull/1012>`__
- Feature: add definitions to MSBuild build helper (and ``tools.build_sln_command()``) `#4239 <https://github.com/conan-io/conan/pull/4239>`_ . Docs `here <https://github.com/conan-io/docs/pull/1024>`__
- Feature: Generate deterministic short paths on Windows `#4238 <https://github.com/conan-io/conan/pull/4238>`_
- Feature: The `tools.environment_append()` now accepts unsetting variables by means of appending such variable with a value equal to None. `#4224 <https://github.com/conan-io/conan/pull/4224>`_ . Docs `here <https://github.com/conan-io/docs/pull/1003>`__
- Feature: Enable a new ``reference`` argument in ``conan install <path> <reference>``, where ``reference`` can be a partial reference too (identical to what is passed to :command:`conan create` or :command:`conan export`. This allows defining all pkg,version,user,channel fields of the recipe for the local flow. `#4197 <https://github.com/conan-io/conan/pull/4197>`_ . Docs `here <https://github.com/conan-io/docs/pull/1045>`__
- Feature: Added support for new architecture ``ppc32`` `#4195 <https://github.com/conan-io/conan/pull/4195>`_ . Docs `here <https://github.com/conan-io/docs/pull/1001>`__
- Feature: Added support for new architecture ``armv8.3`` `#4195 <https://github.com/conan-io/conan/pull/4195>`_ . Docs `here <https://github.com/conan-io/docs/pull/1001>`__
- Feature: Added support for new architecture ``armv8_32`` `#4195 <https://github.com/conan-io/conan/pull/4195>`_ . Docs `here <https://github.com/conan-io/docs/pull/1001>`__
- Feature: Add experimental support for packages in editable mode `#4181 <https://github.com/conan-io/conan/pull/4181>`_ . Docs `here <https://github.com/conan-io/docs/pull/1009>`__
- Fix: Conditionally expand list-like environment variables in ``virtualenv`` generator `#4396 <https://github.com/conan-io/conan/pull/4396>`_
- Fix: get_cross_building_settings for MSYS `#4390 <https://github.com/conan-io/conan/pull/4390>`_
- Fix: Implemented retrial of output to stdout stream when the OS (Windows) is holding it and producing IOError for output `#4375 <https://github.com/conan-io/conan/pull/4375>`_
- Fix: Validate CONAN_CPU_COUNT and output user-friendly message for invalid values `#4372 <https://github.com/conan-io/conan/pull/4372>`_
- Fix: Map ``cpp_info.cppflags`` to ``CONAN_CXXFLAGS`` in ``make`` generator. `#4349 <https://github.com/conan-io/conan/pull/4349>`_ . Docs `here <https://github.com/conan-io/docs/pull/1037>`__
- Fix: Use ``*_DIRS`` instead of ``*_PATHS`` ending for varaibles generated by the ``make`` generator: ``INCLUDE_DIRS``, ``LIB_DIRS``, ``BIN_DIRS``, ``BUILD_DIRS`` and ``RES_DIRS`` `#4349 <https://github.com/conan-io/conan/pull/4349>`_ . Docs `here <https://github.com/conan-io/docs/pull/1037>`__
- Fix: Bumped requirement of pyOpenSSL on OSX to `>=16.0.0, <19.0.0` `#4333 <https://github.com/conan-io/conan/pull/4333>`_
- Fix: Fixed a bug in the migration of the server storage to the revisions layout. `#4325 <https://github.com/conan-io/conan/pull/4325>`_
- Fix: ensure tools.environment_append doesn't raise trying to unset variables `#4324 <https://github.com/conan-io/conan/pull/4324>`_ . Docs `here <https://github.com/conan-io/docs/pull/1023>`__
- Fix: Improve error message when a server (like a proxy), returns 200-OK for a conan api call, but with an unexpected message. `#4317 <https://github.com/conan-io/conan/pull/4317>`_
- Fix: ensure is_windows, detect_windows_subsystem, uname work under MSYS/Cygwin `#4313 <https://github.com/conan-io/conan/pull/4313>`_
- Fix: uname shouldn't use -o flag, which is GNU extention `#4311 <https://github.com/conan-io/conan/pull/4311>`_
- Fix: ``get_branch()`` method of ``tools.SVN()`` helper now returns only the branch name, not the tag when present. `#4306 <https://github.com/conan-io/conan/pull/4306>`_ . Docs `here <https://github.com/conan-io/docs/pull/1020>`__
- Fix: Conan client now always include the `X-Checksum-Sha1` header in the file uploads, not only when checking if the file is already there with a remote supporting checksum deploy (Artifactory) `#4303 <https://github.com/conan-io/conan/pull/4303>`_
- Fix: SCM optimization related to `scm_folder.txt` is taken into account only for packages under development. `#4301 <https://github.com/conan-io/conan/pull/4301>`_
- Fix: Update premake generator, rename conanbuildinfo.premake -> conanbuildinfo.premake.lua, conan_cppdefines -> conan_defines `#4296 <https://github.com/conan-io/conan/pull/4296>`_ . Docs `here <https://github.com/conan-io/docs/pull/1032>`__
- Fix: Using ``yaml.safe_load`` instead of ``load`` `#4285 <https://github.com/conan-io/conan/pull/4285>`_
- Fix: Fixes default CMake generator on Windows to use MinGW Makefiles. `#4281 <https://github.com/conan-io/conan/pull/4281>`_ . Docs `here <https://github.com/conan-io/docs/pull/1026>`__
- Fix: Visual Studio toolset is passed from settings to the MSBuild helper `#4250 <https://github.com/conan-io/conan/pull/4250>`_ . Docs `here <https://github.com/conan-io/docs/pull/1052>`__
- Fix: Handle corner cases related to SCM with local sources optimization `#4249 <https://github.com/conan-io/conan/pull/4249>`_
- Fix: Allow referring to projects created by b2 generator for dependencies with absolute paths. `#4211 <https://github.com/conan-io/conan/pull/4211>`_
- Fix: Credentials are removed from SCM `url` attribute if Conan is automatically resolving it. `#4207 <https://github.com/conan-io/conan/pull/4207>`_ . Docs `here <https://github.com/conan-io/docs/pull/996>`__
- Fix: Remove client/server versions check on every request. Return server capabilities only in `ping` endpoint. `#4205 <https://github.com/conan-io/conan/pull/4205>`_
- Fix: Updated contributing guidelines to the new workflow `#4173 <https://github.com/conan-io/conan/pull/4173>`_
- Bugfix: Fixes config install when copying hooks `#4412 <https://github.com/conan-io/conan/pull/4412>`_
- BugFix: Meson generator was failing in case of package_folder == None (test_package using Meson) `#4391 <https://github.com/conan-io/conan/pull/4391>`_
- BugFix: Prepend environment variables are applied twice in conanfile `#4380 <https://github.com/conan-io/conan/pull/4380>`_
- Bugfix: Caching of several internal loaders broke the conan_api usage `#4362 <https://github.com/conan-io/conan/pull/4362>`_
- Bugfix: Removing usage of FileNotFoundError which is Py3 only `#4361 <https://github.com/conan-io/conan/pull/4361>`_
- Bugfix: Custom generator allow to use imports `#4358 <https://github.com/conan-io/conan/pull/4358>`_ . Docs `here <https://github.com/conan-io/docs/pull/1043>`__
- Bugfix: conanbuildinfo.cmake won't fail if ``project()`` LANGUAGE is None, but the user defines ``CONAN_DISABLE_CHECK_COMPILER``. `#4276 <https://github.com/conan-io/conan/pull/4276>`_
- Bugfix: Fix version ranges containing spaces and not separated by commas. `#4273 <https://github.com/conan-io/conan/pull/4273>`_
- Bugfix: When running consecutively Conan python API calls to `create` the default profile object became modified and cached between calls. `#4256 <https://github.com/conan-io/conan/pull/4256>`_
- Bugfix: Fixes a bug in the CMake build helper about how flags are appended `#4227 <https://github.com/conan-io/conan/pull/4227>`_
- Bugfix: Apply the environment to the local conan package command `#4204 <https://github.com/conan-io/conan/pull/4204>`_
- Bugfix: b2 generator was failing when package recipe didn't use compiler setting `#4202 <https://github.com/conan-io/conan/pull/4202>`_



1.11.2 (8-Jan-2019)
--------------------

- Bugfix: The migrated data in the server from a version previous to Conan `1.10.0` was not migrated creating the needed indexes.
  This fixes the migration and creates the index on the fly for fixing broken migrations.
  Also the server doesn't try to migrate while running but warns the user to run `conan server --migrate` after
  doing a backup of the data, avoiding issues when running the production servers like gunicorn where the process
  doesn't accept input from the user. `#4229 <https://github.com/conan-io/conan/pull/4229>`_



1.11.1 (20-Dec-2018)
--------------------

- BugFix: Fix `conan config install` requester for zip file download `#4172 <https://github.com/conan-io/conan/pull/4172>`_


1.11.0 (19-Dec-2018)
--------------------

- Feature: Store ``verify_ssl`` argument in :command:`conan config install` `#4158 <https://github.com/conan-io/conan/pull/4158>`_ . Docs `here <https://github.com/conan-io/docs/pull/976>`__
- Feature: Tox launcher to run the test suite. `#4151 <https://github.com/conan-io/conan/pull/4151>`_
- Feature: Allow ``--graph=file.html`` html output using local *vis.min.js* and *vis.min.css* resources if they are found in the local cache (can be deployed via :command:`conan config install`) `#4133 <https://github.com/conan-io/conan/pull/4133>`_ . Docs `here <https://github.com/conan-io/docs/pull/972>`__
- Feature: Improve client DEBUG traces with better and more complete messages. `#4128 <https://github.com/conan-io/conan/pull/4128>`_
- Feature: Server prints the configuration used at startup to help debugging issues. `#4128 <https://github.com/conan-io/conan/pull/4128>`_
- Feature: Allow hooks to be stored in folders `#4106 <https://github.com/conan-io/conan/pull/4106>`_ . Docs `here <https://github.com/conan-io/docs/pull/979>`__
- Feature: Remove files containing Macos meta-data (files beginning by `._`) `#4103 <https://github.com/conan-io/conan/pull/4103>`_ . Docs `here <https://github.com/conan-io/docs/pull/978>`__
- Feature: Allow arguments in :command:`git clone` for :command:`conan config install` `#4083 <https://github.com/conan-io/conan/pull/4083>`_ . Docs `here <https://github.com/conan-io/docs/pull/975>`__
- Feature: Display the version-ranges resolutions in a cleaner way. `#4065 <https://github.com/conan-io/conan/pull/4065>`_
- Feature: allow ``conan export . version@user/channel`` and ``conan create . version@user/channel`` `#4062 <https://github.com/conan-io/conan/pull/4062>`_ . Docs `here <https://github.com/conan-io/docs/pull/982>`__
- Fix: `cmake_find_package` generator not forwarding all dependency properties `#4125 <https://github.com/conan-io/conan/pull/4125>`_
- Fix: Recent updates in python break ``ConfigParser`` with ``%`` in values, like in path names containing % (jenkins) `#4122 <https://github.com/conan-io/conan/pull/4122>`_
- Fix: The property file that the ``MSBuild()`` is now generated in the `build_folder` instead of a temporary folder to allow more reproducible builds. `#4113 <https://github.com/conan-io/conan/pull/4113>`_ . Docs `here <https://github.com/conan-io/docs/pull/980>`__
- Fix: Fixed the check of the return code from Artifactory when using the checksum deploy feature. `#4100 <https://github.com/conan-io/conan/pull/4100>`_
- Fix: Evaluate always SCM attribute before exporting the recipe `#4088 <https://github.com/conan-io/conan/pull/4088>`_ . Docs `here <https://github.com/conan-io/docs/pull/981>`__
- Fix: Reordered Python imports `#4064 <https://github.com/conan-io/conan/pull/4064>`_
- Bugfix: In ftp_download function there is extra call to ``ftp.login()`` with empty args. This causes ftp lib to login again with empty credentials and throwing exception because authentication is required by server. `#4092 <https://github.com/conan-io/conan/pull/4092>`_
- Bugfix: Take into account ``os_build`` and ``arch_build`` for search queries. `#4061 <https://github.com/conan-io/conan/pull/4061>`_


1.10.2 (17-Dec-2018)
--------------------

- Bugfix: Fixed bad URL schema in ApiV2 that could cause URLs collisions `#4138 <https://github.com/conan-io/conan/pull/4138>`_


1.10.1 (11-Dec-2018)
--------------------

- Fix: Handle some corner cases of python_requires `#4099 <https://github.com/conan-io/conan/pull/4099>`_
- Bugfix: Add v1_only argument in Conan server class `#4096 <https://github.com/conan-io/conan/pull/4096>`_
- Bugfix: Handle invalid use of `python_requires` when imported like `conans.python_requires` `#4090 <https://github.com/conan-io/conan/pull/4090>`_


1.10.0 (4-Dec-2018)
-------------------

- Feature: Add `include_prerelease` and `loose` option to version range expression  `#3898 <https://github.com/conan-io/conan/pull/3898>`_
- Feature: Merged "revisions" feature code in develop branch, still disabled by default until it gets stabilized.  `#3055 <https://github.com/conan-io/conan/pull/3055>`_
- Feature: CMake global variable to disable Conan output ``CONAN_CMAKE_SILENT_OUTPUT`` `#4042 <https://github.com/conan-io/conan/pull/4042>`_
- Feature: Added new ``make`` generator. `#4003 <https://github.com/conan-io/conan/pull/4003>`_
- Feature: Deploy a conan snapshot package to `test.pypi.org <https://test.pypi.org/project/conan/>`_ for every develop commit. `#4000 <https://github.com/conan-io/conan/pull/4000>`_
- Fix: Using the `scm` feature when Conan is not able to read the gitignored files (local optimization mechanism) print a warning to improve the debug information but not crash. `#4045 <https://github.com/conan-io/conan/pull/4045>`_
- Fix: The `tools.get` tool (download + unzip) now supports all the arguments of the `download` tool. e.g: `verify`, `retry`,  `retry_wait` etc. `#4041 <https://github.com/conan-io/conan/pull/4041>`_
- Fix: Improve ``make`` generator test `#4018 <https://github.com/conan-io/conan/pull/4018>`_
- Fix: Add space and dot in ``conan new --help`` `#3999 <https://github.com/conan-io/conan/pull/3999>`_
- Fix: Resolve aliased packages in python_requires `#3957 <https://github.com/conan-io/conan/pull/3957>`_
- Bugfix: Better checks of package reference ``pkg/version@user/channel``, avoids bugs for conanfile in 4 nested folders and ``conan install path/to/the/file`` `#4044 <https://github.com/conan-io/conan/pull/4044>`_
- Bugfix: Running Windows subsystem scripts crashed when the PATH environment variable passed as a list. `#4039 <https://github.com/conan-io/conan/pull/4039>`_
- Bugfix: Fix removal of conanfile.py with :command:`conan source` command and the removal of source folder in the local cache when something fails `#4033 <https://github.com/conan-io/conan/pull/4033>`_
- Bugfix: A :command:`conan install` with a reference failed when running in the operating system root folder because python tried to create the directory even when nothing is going to be written. `#4012 <https://github.com/conan-io/conan/pull/4012>`_
- Bugfix: Fix qbs generator mixing sharedlinkflags and exelinkflags `#3980 <https://github.com/conan-io/conan/pull/3980>`_
- Bugfix: ``compiler_args`` generated "mytool.lib.lib" for Visual Studio libraries that were defined with the ``.lib`` extension in the ``self.cpp_info.libs`` field of ``package_info()``. `#3976 <https://github.com/conan-io/conan/pull/3976>`_


1.9.2 (20-Nov-2018)
-------------------

- Bugfix: SVN API changes are relevant since version 1.9 `#3954 <https://github.com/conan-io/conan/pull/3954>`_
- Bugfix: Fixed bug in `vcvars_dict` tool when using `filter_known_paths` argument. `#3941 <https://github.com/conan-io/conan/pull/3941>`_


1.9.1 (08-Nov-2018)
-------------------

- Fix: Fix regression introduced in 1.7, setting ``amd64_x86`` when no ``arch_build`` is defined. `#3918 <https://github.com/conan-io/conan/pull/3918>`_
- Fix: Do not look for binaries in other remotes than the recipe, if it is defined. `#3890 <https://github.com/conan-io/conan/pull/3890>`_
- Bugfix: ``sudo --askpass`` breaks CentOS 6 package installation. The sudo version on CentOS 6 is 1.8.6. The option of ``askpass`` for sudo version 1.8.7 or older is `sudo -A`. `#3885 <https://github.com/conan-io/conan/pull/3885>`_


1.9.0 (30-October-2018)
-----------------------

- Feature: Support for ``srcdirs`` in ``package_info()``. Packages can package sources, and specify their location, which will be propagated to consumers. Includes support for CMake generator. `#3857 <https://github.com/conan-io/conan/pull/3857>`_
- Feature: Added `remote_name` and `remote_url` to upload json output. `#3850 <https://github.com/conan-io/conan/pull/3850>`_
- Feature: Add environment variable `CONAN_USE_ALWAYS_SHORT_PATHS` to let the consumer override short_paths behavior from recipes `#3846 <https://github.com/conan-io/conan/pull/3846>`_
- Feature: Added ``--json`` output to ``conan export_pkg`` command `#3809 <https://github.com/conan-io/conan/pull/3809>`_
- Feature: Add `conan remote clean` subcommand `#3767 <https://github.com/conan-io/conan/pull/3767>`_
- Feature: New `premake` generator incorporated to the Conan code base from the external generator at https://github.com/memsharded/conan-premake. `#3751 <https://github.com/conan-io/conan/pull/3751>`_
- Feature: New `conan remote list_pref/add_pref/remove_pref/update_pref` commands added to manage the new Registry entries for binary packages. `#3726 <https://github.com/conan-io/conan/pull/3726>`_
- Feature: Add cpp_info data to json output of ``install`` and ``create`` commands at package level. `#3717 <https://github.com/conan-io/conan/pull/3717>`_
- Feature: Now the default templates of the :command:`conan new` command use the docker images from the `conanio` organization: https://hub.docker.com/u/conanio `#3710 <https://github.com/conan-io/conan/pull/3710>`_
- Feature: Added ``topics`` attribute to the `ConanFile` to specify topics (a.k.a tags, a.k.a keywords) to the recipe. `#3702 <https://github.com/conan-io/conan/pull/3702>`_
- Feature: Internal refactor to the remote registry to manage a json file. Also improved internal interface. `#3676 <https://github.com/conan-io/conan/pull/3676>`_
- Feature: Implement reuse of sources (``exports_sources``) in recipes used as ``python_requires()``. `#3661 <https://github.com/conan-io/conan/pull/3661>`_
- Feature: Added support for Clang >=8 and the new versioning schema, where only the major and the patch is used. `#3643 <https://github.com/conan-io/conan/pull/3643>`_
- Fix: Renamed Plugins as Hooks `#3867 <https://github.com/conan-io/conan/pull/3867>`_
- Fix: Adds GCC 8.2 to default settings.yml `#3865 <https://github.com/conan-io/conan/pull/3865>`_
- Fix: Hidden confusing messages `download conaninfo.txt` when requesting the server to check package manifests. `#3861 <https://github.com/conan-io/conan/pull/3861>`_
- Fix: The ``MSBuild()`` build helper doesn't adjust the compiler flags for the build_type anymore because they are adjusted by the project itself. `#3860 <https://github.com/conan-io/conan/pull/3860>`_
- Fix: Add ``neon`` as linux distro for SystemPackageTools `#3845 <https://github.com/conan-io/conan/pull/3845>`_
- Fix: remove error that was raised for custom compiler & compiler version, while checking ``cppstd`` setting. `#3844 <https://github.com/conan-io/conan/pull/3844>`_
- Fix: do not allow wildcards in command ``conan download <ref-without-wildcards>`` `#3843 <https://github.com/conan-io/conan/pull/3843>`_
- Fix: do not populate ``arch`` nor ``arch_build`` in autodetected profile if ``platform.machine`` returns an empty string. `#3841 <https://github.com/conan-io/conan/pull/3841>`_
- Fix: The registry won't remove a reference to a remote removed recipe or package. `#3838 <https://github.com/conan-io/conan/pull/3838>`_
- Fix: Internal improvements of the ConanFile loader `#3837 <https://github.com/conan-io/conan/pull/3837>`_
- Fix: environment variables are passed verbatim to generators. `#3836 <https://github.com/conan-io/conan/pull/3836>`_
- Fix: Implement dirty checks in the cache build folder, so failed builds are not packaged when there is a ``build_id()`` method. `#3834 <https://github.com/conan-io/conan/pull/3834>`_
- Fix: ``vcvars`` is also called in the ``CMake()`` build helper when `clang` compiler is used, not only with `Visual Studio`compiler. `#3832 <https://github.com/conan-io/conan/pull/3832>`_
- Fix: Ignore empty line when parsing output inside ``SVN::excluded_files`` function. `#3830 <https://github.com/conan-io/conan/pull/3830>`_
- Fix: Bump version of ``tqdm`` requirement to ``>=4.28.0`` `#3823 <https://github.com/conan-io/conan/pull/3823>`_
- Fix: Handling corrupted lock files in cache `#3816 <https://github.com/conan-io/conan/pull/3816>`_
- Fix: Implement download concurrency checks, to allow simultaneous download of the same package (as header-only) while installing different configurations that depend on that package. `#3806 <https://github.com/conan-io/conan/pull/3806>`_
- Fix: ``vcvars`` is also called in the `CMake()` build helper when using `Ninja` or `NMake` generators. `#3803 <https://github.com/conan-io/conan/pull/3803>`_
- Fix: Fixed ``link_flags`` management in ``MSBuild`` build helper `#3791 <https://github.com/conan-io/conan/pull/3791>`_
- Fix: Allow providing ``--profile`` argument (and settings, options, env, too) to :command:`conan export-pkg`, so it is able to correctly compute the binary package_id in case the information captured in the installed conaninfo.txt in previous :command:`conan install` does not contain all information to reconstruct the graph. `#3768 <https://github.com/conan-io/conan/pull/3768>`_
- Fix: Upgrade dependency of ``tqdm`` to >=4.27: solves issue with weakref assertion. `#3763 <https://github.com/conan-io/conan/pull/3763>`_
- Fix: Use XML output to retrieve information from SVN command line if its client version is less than 1.8 (command ``--show-item`` is not available). `#3757 <https://github.com/conan-io/conan/pull/3757>`_
- Fix: SVN v1.7 does not have ``-r`` argument in ``svn status``, so functionality ``SVN::is_pristine`` won't be available. `#3757 <https://github.com/conan-io/conan/pull/3757>`_
- Fix: Add ``--askpass`` argument to ``sudo`` if it is not an interactive terminal `#3727 <https://github.com/conan-io/conan/pull/3727>`_
- Fix: The remote used to download a binary package is now stored, so any update for the specific binary will come from the right remote. `#3726 <https://github.com/conan-io/conan/pull/3726>`_
- Fix: Use XML output from SVN command line interface to compute if the repository is pristine. `#3653 <https://github.com/conan-io/conan/pull/3653>`_
- Fix: Updated templates of the :command:`conan new` command with the latest conan package tools changes. `#3651 <https://github.com/conan-io/conan/pull/3651>`_
- Fix: Improve error messages if conanfile was not found `#3554 <https://github.com/conan-io/conan/pull/3554>`_
- BugFix: Fix conflicting multiple local imports for python_requires `#3876 <https://github.com/conan-io/conan/pull/3876>`_
- Bugfix: do not ask for the username if it is already given when login into a remote. `#3839 <https://github.com/conan-io/conan/pull/3839>`_
- Bugfix: ``yum update`` needs user's confirmation, which breaks system update in CentOS non-interactive terminal. `#3747 <https://github.com/conan-io/conan/pull/3747>`_


1.8.4 (19-October-2018)
-----------------------

- Feature: Increase debugging information when an error uploading a recipe with different timestamp occurs. `#3801 <https://github.com/conan-io/conan/pull/3801>`_
- Fix: Changed ``tqdm`` dependency to a temporarily forked removing the "man" directory write permissions issue installing the `pip` package. `#3802 <https://github.com/conan-io/conan/pull/3802>`_
- Fix: Removed `ndg-httpsclient` and `pyasn` dependencies from OSX requirements file because they shouldn't be necessary. `#3802 <https://github.com/conan-io/conan/pull/3802>`_


1.8.3 (17-October-2018)
-----------------------

- Feature: New attributes ``default_user`` and ``default_channel`` that can be declared in a conanfile to specify the `user` and `channel` for conan local methods when neither `CONAN_USERNAME` and `CONAN_CHANNEL` environment variables exist. `#3758 <https://github.com/conan-io/conan/pull/3758>`_
- Bugfix: AST parsing of ``conanfile.py`` with shebang and encoding header lines was failing in python 2. This fix also allows non-ascii chars in ``conanfile.py`` if proper encoding is declared. `#3750 <https://github.com/conan-io/conan/pull/3750>`_


1.8.2 (10-October-2018)
-----------------------

- Fix: Fix misleading warning message in ``tools.collect_libs()`` `#3718 <https://github.com/conan-io/conan/pull/3718>`_
- BugFix: Fixed wrong naming of ``--sbindir`` and ``--libexecdir`` in AutoTools build helper. `#3715 <https://github.com/conan-io/conan/pull/3715>`_


1.8.1 (10-October-2018)
-----------------------

- Fix: Remove warnings related to ``python_requires()``, both in linter and due to Python2. `#3706 <https://github.com/conan-io/conan/pull/3706>`_
- Fix: Use *share* folder for ``DATAROOTDIR`` in CMake and AutoTools build helpers. `#3705 <https://github.com/conan-io/conan/pull/3705>`_
- Fix: Disabled `apiv2` until the new protocol becomes stable. `#3703 <https://github.com/conan-io/conan/pull/3703>`_


1.8.0 (9-October-2018)
----------------------

- Feature: Allow `conan config install` to install configuration from a folder and not only from compressed files. `#3680 <https://github.com/conan-io/conan/pull/3680>`_
- Feature: The environment variable CONAN_DEFAULT_PROFILE_PATH allows the user to define the path (existing) to the default profile that will be used by Conan. `#3675 <https://github.com/conan-io/conan/pull/3675>`_
- Feature: New :command:`conan inspect` command that provides individual attributes of a recipe, like name, version, or options. Work with ``-r=remote`` repos too, and is able to produce ``--json`` output. `#3634 <https://github.com/conan-io/conan/pull/3634>`_
- Feature: Validate parameter for ConanFileReference objects to avoid unnecessary checks `#3623 <https://github.com/conan-io/conan/pull/3623>`_
- Feature: The environment variable `CONAN_DEFAULT_PROFILE_PATH` allows the user to define the path (absolute and existing) to the default profile that will be used by Conan. `#3615 <https://github.com/conan-io/conan/pull/3615>`_
- Feature: Warning message printed if Conan cannot deduce an architecture of a GNU triplet. `#3603 <https://github.com/conan-io/conan/pull/3603>`_
- Feature: The ``AutotoolsBuildEnvironment`` and ``CMake`` build helpers now adjust default for the GNU standard installation directories: ``bindir``, ``sbin``, ``libexec``, ``includedir``, ``oldincludedir``,  ``datarootdir`` `#3599 <https://github.com/conan-io/conan/pull/3599>`_
- Feature: Added ``use_default_install_dirs`` in ``AutotoolsBuildEnvironment.configure()`` to opt-out from the defaulted installation dirs. `#3599 <https://github.com/conan-io/conan/pull/3599>`_
- Feature: Clean repeated entries in the ``PATH`` when ``vcvars`` is run, mitigating the max size of the env var issues. `#3598 <https://github.com/conan-io/conan/pull/3598>`_
- Feature: Allow ``vcvars`` to run if ``clang-cl`` compiler is detected. `#3574 <https://github.com/conan-io/conan/pull/3574>`_
- Feature: Added python 2 deprecation message in the output of the conan commands. `#3567 <https://github.com/conan-io/conan/pull/3567>`_
- Feature: The :command:`conan install` command now prints information about the applied configuration. `#3561 <https://github.com/conan-io/conan/pull/3561>`_
- Feature: New naming convention for conanfile reserved/public/private attributes. `#3560 <https://github.com/conan-io/conan/pull/3560>`_
- Feature: Experimental support for Conan plugins. `#3555 <https://github.com/conan-io/conan/pull/3555>`_
- Feature: Progress bars for files unzipping. `#3545 <https://github.com/conan-io/conan/pull/3545>`_
- Feature: Improved graph propagation performance from ``O(n2)`` to ``O(n)``. `#3528 <https://github.com/conan-io/conan/pull/3528>`_
- Feature: Added ``ConanInvalidConfiguration`` as the standard way to indicate that a specific configuration is not valid for the current package. e.g library not compatible with Windows. `#3517 <https://github.com/conan-io/conan/pull/3517>`_
- Feature: Added ``libtool()`` function to the `tools.XCRun()` tool to locate the system ``libtool``. `#3515 <https://github.com/conan-io/conan/pull/3515>`_
- Feature: The tool ``tools.collect_libs()`` now search into each folder declared in ``self.cpp_info.libdirs``. `#3503 <https://github.com/conan-io/conan/pull/3503>`_
- Feature:  Added definition ``CMAKE_OSX_DEPLOYMENT_TARGET`` to the ``CMake`` build helper following the ``os.version`` setting for ``Macos``. `#3486 <https://github.com/conan-io/conan/pull/3486>`_
- Feature: The upload of files now uses the `conanmanifest.txt` file to know if a file has to be uploaded or not. It avoids issues associated with the metadata of the files permissions contained in the `tgz` files. `#3480 <https://github.com/conan-io/conan/pull/3480>`_
- Feature: The `default_options` in a `conanfile.py` can be specified now as a dictionary. `#3477 <https://github.com/conan-io/conan/pull/3477>`_
- Feature: The command `conan config install` now support relative paths. `#3468 <https://github.com/conan-io/conan/pull/3468>`_
- Feature: Added a definition `CONAN_IN_LOCAL_CACHE` to the `CMake()` build helper. `#3450 <https://github.com/conan-io/conan/pull/3450>`_
- Feature: Improved `AptTool` at `SystemPackageTool` adding a function `add_repository` to add new apt repositories. `#3445 <https://github.com/conan-io/conan/pull/3445>`_
- Feature: Experimental and initial support for the REST `apiv2` that will allow transfers in one step and revisions in the future. `#3442 <https://github.com/conan-io/conan/pull/3442>`_
- Feature: Improve the output of a :command:`conan install` command printing dependencies when a binary is not found. `#3438 <https://github.com/conan-io/conan/pull/3438>`_
- Feature: New `b2` generator. It replaces the old incomplete `boost_build` generator that is now deprecated. `#3416 <https://github.com/conan-io/conan/pull/3416>`_
- Feature: New ``tool.replace_path_in_file`` to replace Windows paths in a file doing case-insensitive comparison and indistinct path separators comparison: "/" == "\\" `#3399 <https://github.com/conan-io/conan/pull/3399>`_
- Feature: **[Experimental]** Add SCM support for SVN. `#3192 <https://github.com/conan-io/conan/pull/3192>`_
- Fix: ``None`` option value was not being propagated upstream in the dependency graph `#3684 <https://github.com/conan-io/conan/pull/3684>`_
- Fix: Apply ``system_requirements()`` always on install, in case the folder was removed. `#3647 <https://github.com/conan-io/conan/pull/3647>`_
- Fix: Included ``bottle`` package in the development requirements `#3646 <https://github.com/conan-io/conan/pull/3646>`_
- Fix: More complete architecture list in the detection of the gnu triplet and the detection of the build machine architecture. `#3581 <https://github.com/conan-io/conan/pull/3581>`_
- Fix: Avoid downloading the manifest of the recipe twice for uploads. Making this download quiet, without output. `#3552 <https://github.com/conan-io/conan/pull/3552>`_
- Fix: Fixed ``Git`` scm class avoiding to replace any character in the ``get_branch()`` function. `#3496 <https://github.com/conan-io/conan/pull/3496>`_
- Fix: Removed login username syntax checks that were no longer necessary. `#3464 <https://github.com/conan-io/conan/pull/3464>`_
- Fix: Removed bad duplicated messages about dependency overriding when using conan alias. `#3456 <https://github.com/conan-io/conan/pull/3456>`_
- Fix: Improve :command:`conan info` help message. `#3415 <https://github.com/conan-io/conan/pull/3415>`_
- Fix: The generator files are only written in disk if the content of the generated file changes. `#3412 <https://github.com/conan-io/conan/pull/3412>`_
- Fix: Improved error message when parsing a bad conanfile reference. `#3410 <https://github.com/conan-io/conan/pull/3410>`_
- Fix: Paths are replaced correctly on Windows when using ``CMake().patch_config_files()``. `#3399 <https://github.com/conan-io/conan/pull/3399>`_
- Fix: Fixed `AptTool` at `SystemPackageTool` to improve the detection of an installed package. `#3033 <https://github.com/conan-io/conan/pull/3033>`_
- BugFix: Fixes ``python_requires`` overwritten when using more than one of them in a recipe `#3628 <https://github.com/conan-io/conan/pull/3628>`_
- BugFix: Fix output overlap of decompress progress and plugins `#3622 <https://github.com/conan-io/conan/pull/3622>`_
- Bugfix: Check if the ``system_requirements()`` have to be executed even when the package is retrieved from the local cache. `#3616 <https://github.com/conan-io/conan/pull/3616>`_
- Bugfix: All API calls are now logged into the ``CONAN_TRACE_FILE`` log file. `#3613 <https://github.com/conan-io/conan/pull/3613>`_
- Bugfix: Renamed ``os`` (reserved symbol) parameter to ``os_`` in the ``get_gnu_triplet`` tool. `#3603 <https://github.com/conan-io/conan/pull/3603>`_
- Bugfix: :command:`conan get` command now works correctly with enabled ``short paths``. `#3600 <https://github.com/conan-io/conan/pull/3600>`_
- Bugfix: Fixed ``scm`` replacement of the variable when exporting a conanfile. `#3576 <https://github.com/conan-io/conan/pull/3576>`_
- Bugfix: `apiv2` was retrying the downloads even when a 404 error was raised. `#3562 <https://github.com/conan-io/conan/pull/3562>`_
- Bugfix: Fixed ``export_sources`` excluded patterns containing symlinks. `#3537 <https://github.com/conan-io/conan/pull/3537>`_
- Bugfix: Fixed bug with transitive private dependencies. `#3525 <https://github.com/conan-io/conan/pull/3525>`_
- Bugfix: ``get_cased_path`` crashed when the path didn't exist. `#3516 <https://github.com/conan-io/conan/pull/3516>`_
- BugFix: Fixed failures when Conan walk directories with files containing not ASCCI characters in the file name. `#3505 <https://github.com/conan-io/conan/pull/3505>`_
- Bugfix: The `scm` feature now looks for the repo root even when the `conanfile.py` is in a subfolder. `#3479 <https://github.com/conan-io/conan/pull/3479>`_
- Bugfix: Fixed `OSInfo.bash_path()` when there is no `windows_subsystem`. `#3455 <https://github.com/conan-io/conan/pull/3455>`_
- Bugfix: AutotoolsBuildEnvironment was not defaulting the output library directory causing broken consumption of packages when rebuilding from sources in different Linux distros using lib64 default. Read more :ref:`here<autotools_lib64_warning>`. `#3388 <https://github.com/conan-io/conan/pull/3388>`_


1.7.4 (18-September-2018)
-------------------------

- Bugfix: Fixed a bug in `apiv2`.
- Fix: Disabled `apiv2` by default until it gets more stability.


1.7.3 (6-September-2018)
------------------------

- Bugfix: Uncontrolled exception was raised while printing the output of an error downloading a file.
- Bugfix: Fixed :command:`*:option` pattern for conanfile consumers.


1.7.2 (4-September-2018)
------------------------

- Bugfix: Reverted default options initialization to empty string with `varname=`.
- Bugfix: Fixed `conan build` command with `--test` and `--install` arguments.


1.7.1 (31-August-2018)
----------------------

- Fix: Trailing sentences in Conan help command.
- Fix: Removed hardcoded :command:`-c init.templateDir=` argument in :command:`git clone` for :command:`conan config install`, in favor of
  a new :command:`--args` parameter that allows custom arguments.
- Fix: SCM can now handle nested subfolders.
- BugFix: Fix :command:`conan export-pkg` unnecessarily checking remotes.


1.7.0 (29-August-2018)
----------------------

- Feature: Support for C++20 in CMake > 3.12.
- Feature: Included support for Python 3.7 in all platforms.
- Feature: **[Experimental]** New ``python_requires`` function that allows you to reuse Python code by "requiring" it in Conan packages, even to extend the
  ``ConanFile`` class. See: :ref:`Python requires: reusing python code in recipes<python_requires>`
- Feature: ``CMake`` method ``patch_config_paths`` replaces absolute paths to a Conan package's dependencies as well as to the Conan package itself.
- Feature: ``MSBuild`` and ``VisualStudioBuildEnvironment`` build helpers adjust the ``/MP`` flag to build code in parallel using multiple
  cores.
- Feature: Added a ``print_errors`` parameter to ``tools.PkgConfig()`` helper.
- Feature: Added :command:`--query` argument to :command:`conan upload`.
- Feature: ``virtualenv``/``virtualbuildenv``/``virtualrunenv`` generators now create bash scripts in Windows for use in subsystems.
- Feature: Improved resolution speed for version ranges through caching of remote requests.
- Feature: Improved the result of ``tools.vcvars_dict(only_diff=True)`` including a "list" return type that can be used with
  ``tools.environment_append()``.
- Fix: ``AutoToolsBuildEnvironment`` build helper now keeps the ``PKG_CONFIG_PATHS`` variable previously set in the environment.
- Fix: The SCM feature keeps the ``.git`` folder during the copy of a local directory to the local cache.
- Fix: The SCM feature now correctly excludes the folders ignored by Git during the copy of a local directory to the local cache.
- Fix: Conan messages now spell "overridden" correctly.
- Fix: ``MSBuild`` build helper arguments using quotes.
- Fix: ``vcvars_command`` and ``MSBuild`` build helper use the ``amd64_x86`` parameter when Visual Studio > 12 and when cross building for x86.
- Fix: Disabled ``-c init.TemplateDir`` in :command:`conan config install` from a Git repository.
- Fix: Clang compiler check in ``cmake`` generator.
- Fix: Detection of Zypper package tool on latest versions of openSUSE.
- Fix: Improved help output of some commands.
- BugFix: ``qmake`` generator hyphen.
- Bugfix: Git submodules are now initialized from repo *HEAD* **after** checking out the referenced revision when using the ``scm`` attribute.
- BugFix: Declaration ``default_options`` without value, e.g. ``default_options = "config="``. Now it will throw an exception.
- BugFix: Deactivate script in ``virtualenv`` generator causes PS1 to go unset.
- BugFix: Apply general scope options to a consumer ConanFile first.
- BugFix: Fixed detection of a valid repository for Git in the SCM feature.



1.6.1 (27-July-2018)
--------------------

- Bugfix: :command:`conan info --build-order` was showing duplicated nodes for build-requires and private dependencies.
- Fix: Fixed failure with the ``alias`` packages when the name of the package (excluded the version) was different from the aliased package. Now it is limited in the :command:`conan alias` command.


1.6.0 (19-July-2018)
--------------------

- Feature: Added a new ``self.run(..., run_environment=True)`` argument, that automatically applies ``PATH``, ``LD_LIBRARY_PATH`` and
  ``DYLD_LIBRARY_PATH`` environment variables from the dependencies, to the execution of the current command.
- Feature: Added a new ``tools.run_environment()`` method as a shortcut to using ``tools.environment_append`` and ``RunEnvironment()`` together.
- Feature: Added a new ``self.run(..., ignore_errors=True)`` argument that represses launching an exception if the commands fails, so user can
  capture the return code.
- Feature: Improved ``tools.Git`` to allow capturing the current branch and enabling the export of a package whose version is based on the branch and commit.
- Feature: The ``json`` generator now outputs settings and options
- Feature: :command:`conan remote list --raw` prints remote information in a format valid for *remotes.txt*, so it can be used for ``conan config install``
- Feature: Visual Studio generator creates the *conanbuildinfo.props* file using the ``$(USERPROFILE)`` macro.
- Feature: Added a ``filename`` parameter to ``tools.get()`` in case it cannot be deduced from the URL.
- Feature: Propagated ``keep_permissions`` and ``pattern`` parameters from ``tools.get()`` to ``tools.unzip()``.
- Feature: Added XZ extensions to ``unzip()``. This will only work in Python 3 with lzma support enabled, otherwise, and error is produced.
- Feature: Added ``FRAMEWORK_SEARCH_PATHS`` var to the Xcode generator to support packaging Apple Frameworks. Read more
  :ref:`here<package_apple_framework>`.
- Feature: Added :command:`conan build --test` and a ``should_configure`` attribute to control the test stage. Read more
  :ref:`here<attribute_build_stages>`.
- Feature: New tools to convert between files with LF and CRLF line endings: :ref:`tools_unix2dos` and :ref:`tools_dos2unix`.
- Feature: Added :command:`conan config install [url] --type=git` to force cloning of a Git repo for ``http://...`` git urls.
- Feature: Improved output information when a package is missing in a remote to show which package requires the missing one.
- Feature: Improved the management of an upload interruption to avoid uploads of incomplete tarballs.
- Feature: Added new ``LLVM`` toolsets to the base ``settings.yml`` (Visual Studio).
- Feature: Created a plugin for pylint with the previous Conan checks (run in the export) enabling usage of the plugin in IDEs and command line to check if recipes are correct.
- Feature: Improved the ``deb`` installer to guarantee that it runs correctly in Debian 9 and other distros.
- Fix: Fixed :command:`conan search -q` and :command:`conan remove -q` to not return packages that don't have the setting specified in the query.
- Fix: Fixed ``SystemPackageTool`` when calling to update with ``sudo`` is not enabled  and ``mode=verify``.
- Fix: Removed ``pyinstaller`` shared libraries from the linker environment for any Conan subprocess.
- BugFix: The ``YumTool`` now calls ``yum update`` instead of ``yum check-update``.
- Bugfix: Solved a bug in which using ``--manifest`` parameter with :command:`conan create` caused the deletion of information in the dependency graph.
- Bugfix: Solved bug in which the ``build`` method of the ``Version`` model was not showing the version build field correctly .
- Bugfix: Fixed a Conan crash caused by a dependency tree containing transitive private nodes.


1.5.2 (5-July-2018)
-------------------

- Bugfix: Fixed bug with pre-1.0 packages with sources.
- Bugfix: Fixed regression in private requirements.


1.5.1 (29-June-2018)
--------------------

- Bugfix: Sources in the local cache weren't removed when using scm pointing to the local source directory, causing changes in local sources not applied to the conan create process.
- Bugfix: Fixed bug causing duplication of build requires in the dependency graph.


1.5.0 (27-June-2018)
--------------------

- Feature: :command:`conan search <pkg-ref> -r=all` now is able to search for binaries too in all remotes
- Feature: Dependency graph improvements: ``build_requires`` are represented in the graph (visible in :command:`conan info``, also in the
  HTML graph). :command:`conan install` and :command:`conan info` commands shows extended information of the binaries status (represented in
  colors in HTML graph). The dependencies declaration order in recipes is respected (as long as it doesn't break the dependency graph order).
- Feature: improved remote management, it is possible to get binaries from different remotes.
- Feature: :command:`conan user` command is now able to show authenticated users.
- Feature: Added :command:`conan user --json` json output to the command.
- Feature: New ``pattern`` argument to ``tools.unzip()`` and ``tools.untargz`` functions, that allow efficient extraction of certain files
  only.
- Feature : Added Manjaro support for ``SystemPackageTools``.
- Feature: Added ``Macos`` ``version`` subsetting in the default *settings.yml* file, to account for the "min OSX version" configuration.
- Feature: SCM helper argument to recursively clone submodules
- Feature: SCM helper management of subfolder, allows using ``exports`` and ``exports_sources``, manage symlinks, and do not copy files that
  are *.gitignored*. Also, works better in the local development flow.
- Feature: Modifies user agent header to output the Conan client version and the Python version. Example: ``Conan/1.5.0 (Python 2.7.1)``
- Fix: The ``CMake()`` helper now doesn't require a compiler input to deduce the default generator.
- Fix: :command:`conan search <pattern>` now works consistently in local cache and remotes.
- Fix: Proxy related environment variables are removed if *conan.conf* declares proxy configuration.
- Fix: Fixed the parsing of invalid JSON when Microsoft ``vswhere`` tool outputs invalid non utf-8 text.
- Fix: Applying ``winsdk`` and ``vcvars_ver`` to MSBuild and ``vcvars_command`` for VS 14 too.
- Fix: Workspaces now support ``build_requires``.
- Fix: ``CMake()`` helper now defines by default ``CMAKE_EXPORT_NO_PACKAGE_REGISTRY``.
- Fix: Settings constraints declared in recipes now don't error for single strings (instead of a list with a string element).
- Fix: ``cmake_minimum_required()`` is now before ``project()`` in templates and examples.
- Fix: ``CONAN_SYSREQUIRES_MODE=Disabled`` now doesn't try to update the system packages registry.
- Bugfix: Fixed SCM origin path of windows folder (with backslashes).
- Bugfix: Fixed SCM dictionary order when doing replacement.
- Bugfix: Fixed auto-detection of apple-clang 10.0.
- Bugfix: Fixed bug when doing a :command:`conan search` without registry file (just before installation).


1.4.5 (22-June-2018)
--------------------

- Bugfix: The package_id recipe method was being called twice causing issues with info objects being populated with wrong information.


1.4.4 (11-June-2018)
--------------------

- Bugfix: Fix link order with private requirements.
- Bugfix: Removed duplicate ``-std`` flag in CMake < 3 or when the standard is not yet supported by ``CMAKE_CXX_STANDARD``.
- Bugfix: Check ``scm`` attribute to avoid breaking recipes with already defined one.
- Feature: Conan workspaces.


1.4.3 (6-June-2018)
-------------------

- Bugfix: Added system libraries to the cmake_find_package generator.
- Fix: Added SIGTERM signal handler to quit safely.
- Bugfix: Fixed miss-detection of gcc 1 when no gcc was on a Linux machine.


1.4.2 (4-June-2018)
-------------------

- Bugfix: Fixed multi-config packages.
- Bugfix: Fixed `cppstd` management with CMake and 20 standard version.



1.4.1 (31-May-2018)
-------------------

- Bugfix: Solved issue with symlinks making recipes to fail with ``self.copy``.
- Bugfix: Fixed c++20 standard usage with modern compilers and the creation of the *settings.yml* containing the settings values.
- Bugfix: Fixed error with cased directory names in Windows.
- BugFix: Modified confusing warning message in the SCM tool when the remote couldn't be detected.


1.4.0 (30-May-2018)
-------------------

- Feature: Added ``scm`` conanfile attribute, to easily clone/checkout from remote repositories and
  to capture the remote and commit in the exported recipe when the recipe and the sources lives in the same repository.
  Read more in ":ref:`Recipe and sources in a different repo <external_repo>`" and ":ref:`Recipe and sources in the same repo <package_repo>`".
- Feature: Added ``cmake_paths`` generator to create a file setting ``CMAKE_MODULE_PATH`` and ``CMAKE_PREFIX_PATH`` to the packages folders.
  It can be used as a CMake toolchain to perform a transparent CMake usage, without include any line of cmake code related to Conan.
  Read more :ref:`here <cmake_paths_generator>`.
- Feature: Added ``cmake_find_package`` generator that generates one ``FindXXX.cmake`` file per each dependency both with classic CMake approach and modern
  using transitive CMake targets. Read more :ref:`here <cmake_find_package_generator>`.
- Feature: Added :command:`conan search --json` json output to the command.
- Feature: CMake build helper now sets ``PKG_CONFIG_PATH`` automatically and receives new parameter ``pkg_config_paths`` to override it.
- Feature: CMake build helper doesn't require to specify "arch" nor "compiler" anymore when the generator is "Unix Makefiles".
- Feature: Introduced default settings for GCC 8, Clang 7.
- Feature: Introduced support for c++ language standard c++20.
- Feature: Auto-managed ``fPIC`` option in AutoTools build helper.
- Feature: ``tools.vcvars_command()`` and ``tools.vcvars_dict()`` now take ``vcvars_ver`` and ``winsdk_version`` as parameters.
- Feature: ``tools.vcvars_dict()`` gets only the env vars set by vcvars with new parameter ``only_diff=True``.
- Feature: Generator ``virtualbuildenv`` now sets Visual Studio env vars via ``tool.vcvars_dict()``.
- Feature: New tools for Apple development including XCRun wrapper.
- Fix: Message "Package '1' created" in package commands with ``short_paths=True`` now shows package ID.
- Fix: ``tools.vcvars_dict()`` failing to create dictionary due to newlines in vcvars command output.
- Bugfix: ``tools.which()`` returning directories instead of only files.
- Bugfix: Inconsistent local cache when developing a recipe with ``short_paths=True``.
- Bugfix: Fixed reusing MSBuild() helper object for multi-configuration packages.
- Bugfix: Fixed authentication using env vars such as ``CONAN_PASSWORD`` when ``CONAN_NON_INTERACTIVE=True``.
- Bugfix: Fixed Android api_level was not used to adjust CMAKE_SYSTEM_VERSION.
- Bugfix: Fixed MSBuild() build helper creating empty XML node for runtime when the setting was not declared.
- Bugfix: Fixed ``default_options`` not supporting ``=`` in value when specified as tuple.
- Bugfix: AutoToolsBuildEnvironment build helper's ``pkg_config_paths`` parameter now sets paths relative to the install folder or absolute
  ones if provided.


1.3.3 (10-May-2018)
-------------------

- Bugfix: Fixed encoding issues writing to files and calculating md5 sums.


1.3.2 (7-May-2018)
------------------

- Bugfix: Fixed broken ``run_in_windows_bash`` due to wrong argument.
- Bugfix: Fixed ``VisualStudioBuildEnvironment`` when toolset was not defined.
- Bugfix: Fixed md5 computation of conan .tgz files for recipe, exported sources and packages due to file ordering and flags.
- Bugfix: Fixed ``conan download -p=wrong_id`` command
- Fix: Added apple-clang 9.1


1.3.1 (3-May-2018)
------------------

- Bugfix: Fixed regression with ``AutoToolsBuildEnvironment`` build helper that raised exception with not supported architectures during the calculation of the GNU triplet.
- Bugfix: Fixed ``pkg_config`` generator, previously crashing when there was no library directories in the requirements.
- Bugfix: Fixed ``conanfile.run()`` with ``win_bash=True``  quoting the paths correctly.
- Bugfix: Recovered parameter "append" to the ``tools.save`` function.
- Bugfix: Added support (documented but missing) to delete options in ``package_id()`` method using ``del self.info.options.<option>``


1.3.0 (30-April-2018)
---------------------
- Feature: Added new build types to default ``settings.yml``: **RelWithDebInfo** and **MinSizeRel**.
  Compiler flags will be automatically defined in build helpers that do not understand them (``MSBuild``, ``AutotoolsBuildEnvironment``)
- Feature: Improved package integrity. Interrupted downloads or builds shouldn't leave corrupted packages.
- Feature: Added :command:`conan upload --json` json output to the command.
- Feature: new :command:`conan remove --locks` to clear cache locks. Useful when killing conan.
- Feature: New **CircleCI** template scripts can be generated with the :command:`conan new` command.
- Feature: The CMake() build helper manages the fPIC flag automatically based on the options ``fPIC`` and ``shared`` when present.
- Feature: Allowing requiring color output with ``CONAN_COLOR_DISPLAY=1`` environment variable.
  If ``CONAN_COLOR_DISPLAY`` is not set rely on tty detection for colored output.
- Feature: New :command:`conan remote rename` and :command:`conan add --force` commands to handle remotes.
- Feature: Added parameter ``use_env`` to the ``MSBuild().build()`` build helper method to control the ``/p:UseEnv`` msbuild argument.
- Feature: Timeout for downloading files from remotes is now configurable (defaulted to 60 seconds)
- Feature: Improved Autotools build helper with new parameters and automatic set of ``--prefix`` to ``self.package_folder``.
- Feature: Added new tool to compose GNU like triplets for cross-building: ``tools.get_gnu_triplet()``
- Fix: Use International Units for download/upload transfer sizes (Mb, Kb, etc).
- Fix: Removed duplicated paths in ``cmake_multi`` generated files.
- Fix: Removed false positive linter warning for local imports.
- Fix: Improved command line help for positional arguments
- Fix :command:`-ks` alias for :command:`--keep-source` argument in :command:`conan create` and :command:`conan export`.
- Fix: removed confusing warnings when ``self.copy()`` doesn't copy files in the ``package()`` method.
- Fix: ``None`` is now a possible value for settings with nested subsettings in ``settings.yml``.
- Fix: if ``vcvars_command`` is called and Visual is not found, raise an error instead of warning.
- Bugfix: ``self.env_info.paths`` and ``self.env_info.PATHS`` both map now to PATHS env-var.
- Bugfix: Local flow was not correctly recovering state for option values.
- Bugfix: Windows NTFS permissions failed in case USERDOMAIN env-var was not defined.
- Bugfix: Fixed generator ``pkg_config`` when there are absolute paths (not use prefix)
- Bugfix: Fixed parsing of settings values with ``"="`` character in conaninfo.txt files.
- Bugfix: Fixed misdetection of MSYS environments (generation of default profile)
- Bugfix: Fixed string escaping in CMake files for preprocessor definitions.
- Bugfix: ``upload --no-overwrite`` failed when the remote package didn't exist.
- Bugfix: Don't raise an error if ``detect_windows_subsystem`` doesn't detect a subsystem.

1.2.3 (10-Apr-2017)
-------------------

- Bugfix: Removed invalid version field from scons generator.

1.2.1 (3-Apr-2018)
------------------

- Feature: Support for `apple-clang 9.1`
- Bugfix: `compiler_args` generator manage correctly the flag for the `cppstd` setting.
- Bugfix: Replaced exception with a warning message (recommending the `six` module) when using `StringIO` class from the `io` module.


1.2.0 (28-Mar-2018)
-------------------

- Feature: The command :command:`conan build` has new ``--configure, --build, --install`` arguments to control the different stages of the
  ``build()`` method.
- Feature: The command :command:`conan export-pkg` now has a :command:`--package-folder` that can be used to export an exact copy of the
  provided folder, irrespective of the ``package()`` method. It assumes the package has been locally created with a previous
  :command:`conan package` or with a :command:`conan build` using a ``cmake.install()`` or equivalent feature.
- Feature: New ``json`` generator, generates a json file with machine readable information from dependencies.
- Feature: Improved proxies configuration with ``no_proxy_match`` configuration variable.
- Feature: New :command:`conan upload` parameter :command:`--no-overwrite` to forbid the overwriting of recipe/packages if they have
  changed.
- Feature: Exports are now copied to ``source_folder`` when doing :command:`conan source`.
- Feature: ``tools.vcvars()`` context manager has no effect if platform is different from Windows.
- Feature: :command:`conan download` has new optional argument :command:`--recipe` to download only the recipe of a package.
- Feature: Added ``CONAN_NON_INTERACTIVE`` environment variable to disable interactive prompts.
- Feature: Improved ``MSbuild()`` build helper using ``vcvars()`` and generating property file to adjust the runtime automatically.
  New method ``get_command()`` with the call to ``msbuild`` tool. Deprecates ``tools.build_sln_command()`` and ``tools.msvc_build_command()``.
- Feature: Support for clang 6.0 correctly managing cppstd flags.
- Feature: Added configuration to specify a client certificate to connect to SSL server.
- Feature: Improved ``ycm`` generator to show json dependencies.
- Feature: Experimental ``--json`` parameter for :command:`conan install` and :command:`conan create` to generate a JSON file with install information.
- Fix: :command:`conan install --build` does not absorb more than one parameter.
- Fix: Made conanfile templates generated with :command:`conan new` PEP8 compliant.
- Fix: :command:`conan search` output improved when there are no packages for the given reference.
- Fix: Made :command:`conan download` also retrieve sources.
- Fix: Pylint now runs as an external process.
- Fix: Made ``self.user`` and ``self.channel`` available in test_package.
- Fix: Made files writable after a ``deploy()`` or ``imports()`` when ``CONAN_READ_ONLY_CACHE```/``general.read_only_cache``
  environment/config variable is ``True``.
- Fix: Linter showing warnings with ``cpp_info`` object in ``deploy()`` method.
- Fix: Disabled linter for Conan pyinstaller as it was not able to find the python modules.
- Fix: :command:`conan user -r=remote_name` showed all users for all remotes, not the one given.
- BugFix: Python reuse code failing to import module in ``package_info()``.
- BugFix: Added escapes for backslashes in ``cmake`` generator.
- BugFix: :command:`conan config install` now raises error if :command:`git clone` fails.
- BugFix: Alias resolution not working in diamond shaped dependency trees.
- BugFix: Fixed builds with Cygwin/MSYS2 failing in Windows with `self.short_paths=True` and NTFS file systems due to ACL permissions.
- BugFix: Failed to adjust architecture when running Conan platform detection in ARM devices.
- BugFix: Output to StringIO failing in Python 2.
- BugFix: :command:`conan profile update` not working to update ``[env]`` section.
- BugFix: :command:`conan search` not creating default remotes when running it as the very first command after Conan installation.
- BugFix: Package folder was not cleaned after the installation and download of a package had failed.

1.1.1 (5-Mar-2018)
------------------

- Feature: ``build_sln_command()`` and ``msvc_build_command()`` receive a new optional parameter ``platforms`` to match the definition of the *.sln* Visual Studio project architecture. (Typically Win32 vs x86 problem).
- Bugfix:  Flags for Visual Studio command (cl.exe) using "-" instead of "/" to avoid problems in builds using AutoTools scripts with Visual Studio compiler.
- Bugfix: Visual Studio runtime flags adjusted correctly in ``AutoToolsBuildEnvironment()`` build helper
- Bugfix: ``AutoToolsBuildEnvironment()`` build helper now adjust the correct build flag, not using eabi suffix, for architecture x86.


1.1.0 (27-Feb-2018)
-------------------

- Feature: New :command:`conan create --keep-build` option that allows re-packaging from conan local cache, without re-building.
- Feature: :command:`conan search <pattern> -r=all` now searches in all defined remotes.
- Feature: Added setting ``cppstd`` to manage the C++ standard. Also improved build helpers to adjust the standard automatically when the user activates the setting. ``AutoToolsBuildEnvironment()``, ``CMake()``, ``MSBuild()`` and ``VisualStudioBuildEnvironment()``.
- Feature: New ``compiler_args`` generator, for directly calling the compiler from command line, for multiple compilers: VS, gcc, clang.
- Feature: Defined ``sysrequires_mode`` variable (``CONAN_SYSREQUIRES_MODE`` env-var) with values ``enabled, verify, disabled`` to control the installation of system dependencies via ``SystemPackageTool`` typically used in :ref:`method_system_requirements`.
- Feature: automatically apply ``pythonpath`` environment variable for dependencies containing python code to be reused to recipe ``source()``, ``build()``, ``package()`` methods.
- Feature: ``CMake`` new ``patch_config_paths()`` methods that will replace absolute paths to conan package path variables, so cmake find scripts are relocatable.
- Feature: new :command:`--test-build-folder` command line argument to define the location of the *test_package* build folder, and new conan.conf ``temp_test_folder`` and environment variable ``CONAN_TEMP_TEST_FOLDER``, that if set to True will automatically clean the test_package build folder after running.
- Feature: Conan manages relative urls for upload/download to allow access the server from different configured networks or in domain subdirectories.
- Feature: Added ``CONAN_SKIP_VS_PROJECTS_UPGRADE`` environment variable to skip the upgrade of Visual Studio project when using :ref:`tools_build_sln_command`, the :ref:`msvc_build_command<tools_msvc_build_command>` and the :ref:`MSBuild()<msbuild>` build helper.
- Feature: Improved detection of Visual Studio installations, possible to prioritize between multiple installed Visual tools with the ``CONAN_VS_INSTALLATION_PREFERENCE`` env-var and ``vs_installation_preference`` conan.conf variable.
- Feature: Added ``keep_path`` parameter to ``self.copy()`` within the ``imports()`` method.
- Feature: Added ``[build_requires]`` section to *conanfile.txt*.
- Feature: Added new :command:`conan help <command>` command, as an alternative to :command:`--help`.
- Feature: Added ``target`` parameter to ``AutoToolsBuildEnvironment.make`` method, allowing to select build target on running make
- Feature: The ``CONAN_MAKE_PROGRAM`` environment variable now it is used by the ``CMake()`` build helper to set a custom make program.
- Feature: Added :command:`--verify-ssl` optional parameter to :command:`conan config install` to allow self-signed SSL certificates in download.
- Feature: ``tools.get_env()`` helper method to automatically convert environment variables to python types.
- Fix: Added a visible warning about ``libcxx`` compatibility and the detected one for the default profile.
- Fix: Wrong detection of compiler in OSX for gcc frontend to clang.
- Fix: Disabled *conanbuildinfo.cmake* compiler checks for unknown compilers.
- Fix: ``visual_studio`` generator added missing *ResourceCompile* information.
- Fix: Don't output password from URL for :command:`conan config install` command.
- Fix: Signals exit with error code instead of 0.
- Fix: Added package versions to generated SCons file.
- Fix: Error message when package was not found in remotes has been improved.
- Fix: :command:`conan profile` help message.
- Fix: Use gcc architecture flags -m32, -m64 for MinGW as well.
- Fix: ``CMake()`` helper do not require settings if ``CONAN_CMAKE_GENERATOR`` is defined.
- Fix: improved output of package remote origins.
- Fix: Profiles files use same structure as :command:`conan profile show` command.
- Fix: *conanpath.bat* file is removed after conan Windows installer uninstall.
- Fix: Do not add GCC-style flags -m32, -m64, -g, -s to MSVC when using ``AutoToolsBuildEnvironment``
- Fix: "Can't find a binary package" message now includes the Package ID.
- Fix: added clang 5.0 and gcc 7.3 to default *settings.yml*.
- Bugfix:  ``build_id()`` logic does not apply unless the ``build_id`` is effectively changed.
- Bugfix: ``self.install_folder`` was not correctly set in all necessary cases.
- Bugfix: :command:`--update` option does not ignore local packages for version-ranges.
- Bugfix: Set ``self.develop=True`` for ``export-pkg`` command.
- Bugfix: Server HTTP responses were incorrectly captured, not showing errors for some server errors.
- Bugfix: Fixed ``config`` section update for sequential calls over the python API.
- Bugfix: Fixed wrong ``self.develop`` set to ``False`` for :command:`conan create` with *test_package*.
- Deprecation: Removed **conan-transit** from default remotes registry.


1.0.4 (30-January-2018)
-----------------------

- Bugfix: Fixed default profile defined in *conan.conf* that includes another profile
- Bugfix: added missing management of ``sysroot`` in *conanbuildinfo.txt* affecting :command:`conan build` and *test_package*.
- Bugfix: Fixed warning in :command:`conan source` because of incorrect management of settings.
- Bugfix: Fixed priority order of environment variables defined in included profiles
- Bugfix: NMake error for parallel builds from the ``CMake`` build helper have been fixed
- Bugfix: Fixed options pattern not applied to root node (``-o *:shared=True`` not working for consuming package)
- Bugfix: Fixed shadowed options by package name (``-o *:shared=True -o Pkg:other=False`` was not applying ``shared`` value to Pkg)
- Fix: Using ``filter_known_paths=False`` as default to ``vcvars_dict()`` helper.
- Fix: Fixed wrong package name for output messages regarding build-requires
- Fix: Added correct metadata to conan.exe when generated via pyinstaller


1.0.3 (22-January-2018)
-----------------------

- Bugfix: Correct load of stored settings in conaninfo.txt (for :command:`conan build`) when ``configure()`` remove some setting.
- Bugfix: Correct use of unix paths in Windows subsystems (msys, cygwin) when needed.
- Fix: fixed wrong message for :command:`conan alias --help`.
- Fix: Normalized all arguments to :command:`--xxx-folder` in command line help.



1.0.2 (16-January-2018)
-----------------------

- Fix: Adding a warning message for simultaneous use of ``os`` and ``os_build`` settings.
- Fix: Do not raise error from *conanbuildinfo.cmake* for Intel MSVC toolsets.
- Fix: Added more architectures to default *settings.yml* ``arch_build`` setting.
- Fix: using :command:`--xxx-folder` in command line help messages.
- Bugfix: using quotes for Windows bash path with spaces.
- Bugfix: vcvars/vcvars_dict not including windows and windows/system32 directories in the path.


1.0.1 (12-January-2018)
-----------------------

- Fix: :command:`conan new` does not generate cross-building (like ``os_build``) settings by default. They make only sense for dev-tools used as ``build_requires``
- Fix: *conaninfo.txt* file does not dump settings with None values


1.0.0 (10-January-2018)
-----------------------

- Bugfix: Fixed bug from ``remove_from_path`` due to Windows path backslash
- Bugfix: Compiler detection in *conanbuildinfo.cmake* for Visual Studio using toolchains like LLVM (Clang)
- Bugfix: Added quotes to bash path.


1.0.0-beta5 (8-January-2018)
----------------------------

- Fix: Errors from remotes different to a 404 will raise an error. Disconnected remotes have to be removed from remotes or use explicit remote with ``-r myremote``
- Fix: cross-building message when building different architecture in same OS
- Fix: :command:`conan profile show` now shows profile with same syntax as profile files
- Fix: generated test code in :command:`conan new` templates will not run example app if cross building.
- Fix: :command:`conan export-pkg` uses the *conanfile.py* folder as the default :command:`--source-folder`.
- Bugfix: :command:`conan download` didn't download recipe if there are no binaries. Force recipe download.
- Bugfix: Fixed blocked ``self.run()`` when stderr outputs large tests, due to full pipe.


1.0.0-beta4 (4-January-2018)
----------------------------

- Feature: ``run_in_windows_bash`` accepts a dict of environment variables to be prioritized inside the bash shell, mainly intended to control the priority of the tools in the path. Use with ``vcvars`` context manager and ``vcvars_dict``, that returns the PATH environment variable only with the Visual Studio related directories
- Fix: Adding all values to ``arch_target``
- Fix: :command:`conan new` templates now use new ``os_build`` and ``arch_build`` settings
- Fix: Updated ``CMake`` helper to account for ``os_build`` and ``arch_build`` new settings
- Fix: Automatic creation of *default* profile when it is needed by another one (like ``include(default)``)
- BugFix: Failed installation (non existing package) was leaving lock files in the cache, reporting a package for :command:`conan search`.
- BugFix: Environment variables are now applied to ``build_requirements()`` for :command:`conan install .`.
- BugFix: Dependency graph was raising conflicts for diamonds with **alias** packages.
- BugFix: Fixed :command:`conan export-pkg` after a :command:`conan install` when recipe has options.


1.0.0-beta3 (28-December-2017)
------------------------------

- Fix: Upgraded pylint and astroid to latest
- Fix: Fixed ``build_requires`` with transitive dependencies to other build_requires
- Fix: Improved pyinstaller creation of executable, to allow for py3-64 bits (windows)
- Deprecation: removed all :command:`--some_argument`, use instead :command:`--some-argument` in command line.


1.0.0-beta2 (23-December-2017)
------------------------------

- Feature: New command line UI. Most commands use now the path to the package recipe, like :command:`conan export . user/testing` or
  :command:`conan create folder/myconanfile.py user/channel`.
- Feature: Better cross-compiling. New settings model for ``os_build``, ``arch_build``, ``os_target``, ``arch_target``.
- Feature: Better Windows OSS ecosystem, with utilities and settings model for MSYS, Cygwin, Mingw, WSL
- Feature: ``package()`` will not warn of not copied files for known use cases.
- Feature: reduce the scope of definition of ``cpp_info``, ``env_info``, ``user_info`` attributes to ``package_info()``
  method, to avoid unexpected errors.
- Feature: extended the use of addressing folder and conanfiles with different names for ``source``, ``package`` and ``export-pkg``
  commands
- Feature: added support for Zypper system package tool
- Fix: Fixed application of build requires from profiles that didn't apply to requires in recipes
- Fix: Improved "test package" message in output log
- Fix: updated CI templates generated with :command:`conan new`
- Deprecation: Removed ``self.copy_headers`` and family for the ``package()`` method
- Deprecation: Removed ``self.conanfile_directory`` attribute.

.. note::

  This is a beta release, shouldn't be installed unless you do it explicitly

  $ pip install conan==1.0.0b2 --upgrade

  **Breaking changes**

  - The new command line UI breaks command line tools and integration. Most cases, just add a :command:`.` to the command.
  - Removed ``self.copy_headers``, ``self.copy_libs``, methods for ``package()``. Use ``self.copy()`` instead.
  - Removed ``self.conanfile_directory`` attribute. Use ``self.source_folder``, ``self.build_folder``, etc.
    instead


0.30.3 (15-December-2017)
-------------------------

- Reverted ``CMake()`` and ``Meson()`` build helpers to keep old behavior.
- Forced Astroid dependency to < 1.6 because of py3 issues.


0.30.2 (14-December-2017)
-------------------------

- Fix: ``CMake()`` and ``Meson()`` build helpers and relative directories regression.
- Fix: ``ycm`` generator, removed the access of ``cpp_info`` to generators, keeping the access to ``deps_cpp_info``.


0.30.1 (12-December-2017)
-------------------------

- Feature: Introduced major versions for gcc (5, 6, 7) as defaults settings for OSS packages, as minors are compatible by default
- Feature: ``VisualStudioBuildEnvironment`` has added more compilation and link flags.
- Feature: new ``MSBuild()`` build helper that wraps the call to ``msvc_build_command()`` with the correct application of environment
  variables with the improved ``VisualStudioBuildEnvironment``
- Feature: ``CMake`` and ``Meson`` build helpers got a new ``cache_build_dir`` argument for ``configure(cache_build_dir=None)``
  that will be used to define a build directory while the package is being built in local cache, but not when built locally
- Feature: ``conanfiles`` got a new ``apply_env`` attribute, defaulted to ``True``. If false, the environment variables from
  dependencies will not be automatically applied. Useful if you don't want some dependency adding itself to the PATH by default,
  for example
- Feature: allow recipes to use and run python code installed with :command:`conan config install`.
- Feature: ``conanbuildinfo.cmake`` now has ``KEEP_RPATHS`` as argument to keep the RPATHS, as opposed to old SKIP_RPATH which
  was confusing. Also, it uses set(CMAKE_INSTALL_NAME_DIR "") to keep the old behavior even for CMake >= 3.9
- Feature: :command:`conan info` is able to get profile information from the previous install, instead of requiring it as input again
- Feature: ``tools.unix_path`` support MSYS, Cygwin, WSL path flavors
- Feature: added ``destination`` folder argument to ``tools.get()`` function
- Feature: ``SystemPackageTool`` for apt-get now uses :command:`--no-install-recommends` automatically.
- Feature: ``visual_studio_multi`` generator now uses toolsets instead of IDE version to identify files.
- Fix: generators failures print traces to help debugging
- Fix: typos in generator names, or non-existing generator now raise an Error instead of a warning
- Fix: ``short_paths`` feature is active by default in Windows. If you want to opt-out, you can use ``CONAN_USER_HOME_SHORT=None``
- Fix: ``SystemPackageTool`` doesn't use sudo in Windows
- BugFix: Not using parallel builds for Visual<10 in CMake build helper.
- Deprecation: ``conanfile_directory` shouldn't be used anymore in recipes. Use ``source_folder``, ``build_folder``, etc.

.. note::

  **Breaking changes**

  - ``scopes`` have been completely removed. You can use environment variables, or the ``conanfile.develop`` or ``conanfile.in_local_cache``
    attributes instead.
  - Command *test_package* has been removed. Use :command:`conan create`` instead, and :command:`conan test`` for just running package tests.
  - ``werror`` behavior is now by default. Dependencies conflicts will now error, and have to be fixed.
  - ``short_paths`` feature is again active by default in Windows, even with Py3.6 and system LongPathsEnabled.
  - ``ConfigureEnvironment`` and ``GCC`` build helpers have been completely removed


0.29.2 (2-December-2017)
------------------------

- Updated python cryptography requirement for OSX due the pyOpenSSL upgrade. See more: https://pypi.org/project/pyOpenSSL/


0.29.1 (23-November-2017)
-------------------------

- Support for OSX High Sierra
- Reverted concurrency locks to counters, removed ``psutil`` dependency
- Implemented migration for settings.yml (for new VS toolsets)
- Fixed encoding issues in conan_server


0.29.0 (21-November-2017)
-------------------------

- Feature: Support for WindowsStore (WinRT, UWP)
- Feature: Support for Visual Studio Toolsets.
- Feature: New ``boost-build`` generator for generic bjam (not only Boost)
- Feature: new ``tools.PkgConfig`` helper to parse pkg-config (.pc) files.
- Feature: Added ``self.develop`` conanfile variable. It is true for :command:`conan create` packages and for local development.
- Feature: Added ``self.keep_imports`` to avoid removal of imported files in the ``build()`` method. Convenient for re-packaging.
- Feature: Autodetected MSYS2 for ``SystemPackageTool``
- Feature: ``AutoToolsBuildEnvironment`` now auto-loads ``pkg_config_path`` (to use with ``pkg_config`` generator)
- Feature: Changed search for profiles. Profiles not found in the default ``profiles`` folder, will be searched for locally. Use ``./myprofile`` to force local search only.
- Feature: Parallel builds for Visual Studio (previously it was only parallel compilation within builds)
- Feature: implemented syntax to check options with ``if "something" in self.options.myoption``
- Fix: Fixed CMake dependency graph when using TARGETS, that produced wrong link order for transitive dependencies.
- Fix: Trying to download the ``exports_sources`` is not longer done if such attribute is not defined
- Fix: Added output directories in ``cmake`` generator for RelWithDebInfo and MinSizeRel configs
- Fix: Locks for concurrent access to local cache now use process IDs (PIDs) to handle interruptions and inconsistent states. Also, adding messages when locking.
- Fix: Not remove the .zip file after a :command:`conan config install` if such file is local
- Fix: Fixed ``CMake.test()`` for the Ninja generator
- Fix: Do not create local conaninfo.txt file for :command:`conan install <pkg-ref>` commands.
- Fix: Solved issue with multiple repetitions of the same command line argument
- BugFix: Don't rebuild conan created (with conan-create) packages when ``build_policy="always"``
- BugFix: :command:`conan copy` was always copying binaries, now can copy only recipes
- BugFix: A bug in download was causing appends instead of overwriting for repeated downloads.
- Development: Large restructuring of files (new cmd and build folders)
- Deprecation: Removed old CMake helper methods (only valid constructor is ``CMake(self)``)
- Deprecation: Removed old ``conan_info()`` method, that was superseded by ``package_id()``

.. note::

  **Breaking changes**

  - CMAKE_LIBRARY_OUTPUT_DIRECTORY definition has been introduced in ``conan_basic_setup()``, it will send shared libraries .so
    to the ``lib`` folder in Linux systems. Right now it was undefined.
  - Profile search logic has slightly changed. For ``-pr=myprofile``, such profile will be searched both in the default folder
    and in the local one if not existing. Use ``-pr=./myprofile`` to force local search only.
  - The :command:`conan copy` command has been fixed. To copy all binaries, it is necessary to explicit :command:`--all`, as other commands do.
  - The only valid use of CMake helper is ``CMake(self)`` syntax.
  - If using ``conan_info()``, replace it with ``package_id()``.
  - Removed environment variable ``CONAN_CMAKE_TOOLSET``, now the toolset can be specified as a subsetting of Visual Studio compiler or specified in the build helpers.


0.28.1 (31-October-2017)
------------------------

- BugFix: Downloading (``tools.download``) of files with ``content-encoding=gzip`` were raising an exception
  because the downloaded content length didn't match the http header ``content-length``


0.28.0 (26-October-2017)
------------------------

This is a big release, with many important and core changes. Also with a huge number of community contributions,
thanks very much!

- Feature: Major revamp of most conan commands, making command line arguments homogeneous. Much
  better development flow adapting to user layouts, with ``install-folder``, ``source-folder``,
  ``build-folder``, ``package-folder``.
- Feature: new ``deploy()`` method, useful for installing binaries from conan packages
- Feature: Implemented some **concurrency** support for the conan local cache. Parallel :command:`conan install`
  and :command:`conan create` for different configurations should be possible.
- Feature: options now allow patterns in command line: ``-o *:myoption=myvalue`` applies to all packages
- Feature: new ``pc`` generator that generates files from dependencies for ``pkg-config``
- Feature: new ``Meson`` helper, similar to ``CMake`` for Meson build system. Works well with ``pc`` generator.
- Feature: Support for read-only cache with ``CONAN_READ_ONLY_CACHE`` environment variable
- Feature: new ``visual_studio_multi`` generator to load Debug/Release, 32/64 configs at once
- Feature: new ``tools.which`` helper to locate executables
- Feature: new :command:`conan --help` layout
- Feature: allow to override compiler version in ``vcvars_command``
- Feature: :command:`conan user` interactive (and not exposed) password input for empty ``-p`` argument
- Feature: Support for ``PacManTool`` for ``system_requirements()`` for ArchLinux
- Feature: Define VS toolset in ``CMake`` constructor and from environment variable CONAN_CMAKE_TOOLSET
- Feature: :command:`conan create` now accepts ``werror`` argument
- Feature: ``AutoToolsBuildEnvironment`` can use ``CONAN_MAKE_PROGRAM`` env-var to define make program
- Feature: added xcode9 for apple-clang 9.0, clang 5 to default settings.yml
- Feature: deactivation of ``short_paths`` in Windows 10 with Py3.6 and long path support is automatic
- Feature: show unzip progress by percentage, not by file (do not clutters output)
- Feature: do not use ``sudo`` for system requirements if already running as root
- Feature: ``tools.download`` able to use headers/auth
- Feature: conan does not longer generate bytecode from recipes (no more .pyc, and more efficient)
- Feature: add parallel argument to ``build_sln_command`` for VS
- Feature: Show warning if vs150comntools is an invalid path
- Feature: ``tools.get()`` now has arguments for hash checking
- Fix: upload pattern now accepts ``Pkg/*``
- Fix: improved downloader, make more robust, better streaming
- Fix: ``tools.patch`` now support adding/removal of files
- Fix: The ``default`` profile is no longer taken as a base and merged with user profile.
  Use explicit ``include(default)`` instead.
- Fix: properly manage x86 as cross building with autotools
- Fix: ``tools.unzip`` removed unnecessary long-paths check in Windows
- Fix: ``package_info()`` is no longer executed at install for the consumer conanfile.py
- BugFix: source folder was not being correctly removed when recipe was updated
- BugFix: fixed ``CMAKE_C_FLAGS_DEBUG`` definition in ``cmake`` generator
- BugFix: ``CMAKE_SYSTEM_NAME`` is now Darwin for iOS, watchOS and tvOS
- BugFix: ``xcode`` generator fixed handling of compiler flags
- BugFix: pyinstaller hidden import that broke .deb installer
- BugFix: :command:`conan profile list` when local files matched profile names

.. note::

  **Breaking changes**

  This is an important release towards stabilizing conan and moving out of beta. Some breaking changes have been done,
  but mostly to command line arguments, so they should be easy to fix. Package recipes or existing packages shouldn't break.
  Please **update**, it is very important to ease the transition of future stable releases. Do not hesitate to ask questions,
  or for help if you need it. This is a possibly not complete list of things to take into account:

  - The command :command:`conan install` doesn't accept ``cwd`` anymore, to change the directory where the generator
    files are written, use the :command:`--install-folder` parameter.
  - The command :command:`conan install` doesn't accept :command:`--all` anymore. Use :command:`conan download <ref>` instead.
  - The command :command:`conan build` now requires the path to the ``conanfile.py`` (optional before)
  - The command :command:`conan package` not longer re-package a package in the local cache, now it only
    operates in a user local folder. The recommended way to re-package a package is using :command:`conan build` and then
    :command:`conan export-pkg`.
  - Removed :command:`conan package_files` in favor of a new command :command:`conan export-pkg`. It requires a local recipe
    with a ``package()`` method.
  - The command :command:`conan source` no longer operates in the local cache. now it only operates in a user local folder.
    If you used :command:`conan source` with a reference to workaround the concurrency, now it natively supported, you
    can remove the command call and trust concurrent install processes.
  - The command :command:`conan imports` doesn't accept ``-d, --dest`` anymore, use :command:`--imports-folder` parameter instead.
  - If you specify a profile in a conan command, like conan create or conan install the base profile *~/.conan/profiles/default* won't be
    applied. Use explicit ``include`` to keep the old behavior.

0.27.0 (20-September-2017)
--------------------------

- Feature: :command:`conan config install <url>` new command. Will install remotes, profiles, settings, conan.conf and other files into the local conan installation. Perfect to synchronize configuration among teams
- Feature: improved traceback printing when errors are raised for more context. Configurable via env
- Feature: filtering out non existing directories in ``cpp_info`` (include, lib, etc), so some build systems don't complain about them.
- Feature: Added include directories to ResourceCompiler and to MIDL compiler in ``visual_studio`` generator
- Feature: new ``visual_studio_legacy`` generator for Visual Studio 2008
- Feature: show path where manifests are locally stored
- Feature: ``replace_in_file`` now raises error if replacement is not done (opt-out parameter)
- Feature: enabled in conan.conf ``[proxies]`` section ``no_proxy=url1,url2`` configuration (to skip proxying for those URLs), as well as ``http=None`` and ``https=None`` to explicitly disable them.
- Feature: new conanfile ``self.in_local_cache`` attribute for conditional logic to apply in user folders local commands
- Feature: ``CONAN_USER_HOME_SHORT=None`` can disable the usage of ``short_paths`` in Windows, for modern Windows that enable long paths at the system level
- Feature: ``if "arm" in self.settings.arch`` is now a valid check (without casting to str(self.settings.arch))
- Feature: added cwd`` argument to :command:`conan source` local method.
- Fix: unzip crashed for 0 Bytes zip files
- Fix: ``collect_libs`` moved to the ``tools`` module
- Bugfix: fixed wrong regex in ``deps_cpp_info`` causing issues with dots and dashes in package names
- Development: Several internal refactorings (tools module, installer), testing (using VS2015 as default, removing VS 12 in testing). Conditional CI in travis for faster builds in developers, downgrading to CMake 3.7 in appveyor
- Deprecation: ``dev_requires`` have been removed (it was not documented, but accessible via the ``requires(dev=True)`` parameter. Superseded by ``build_requires``.
- Deprecation: sources tgz files for exported sources no longer contain ".c_src" subfolder. Packages created with 0.27 will be incompatible with conan < 0.25


0.26.1 (05-September-2017)
--------------------------

- Feature: added apple-clang 9.0 to default settings.
- Fix: :command:`conan copy` command now supports symlinks.
- Fix: fixed removal of "export_source" folder when files have no permissions
- Bugfix: fixed parsing of *conanbuildinfo.txt* with package names containing dots.


0.26.0 (31-August-2017)
-----------------------

- Feature: :command:`conan profile` command has implemented ``update``, ``new``, ``remove`` subcommands, with detect``, to allow creation, edition and management of profiles.
- Feature: :command:`conan package_files` command now can call recipe ``package()`` method if build_folder`` or source_folder`` arguments are defined
- Feature: graph loading algorithm improved to avoid repeating nodes. Results in much faster times for dense graphs, and avoids duplications of private requirements.
- Feature: authentication based on environment variables. Allows very long processes without tokens being expired.
- Feature: Definition of Visual Studio runtime setting ``MD`` or ``MDd`` is now automatic based on build type, not necessary to default in profile.
- Feature: Capturing ``SystemExit`` to return user error codes to the system with ``sys.exit(code)``
- Feature: Added SKIP_RPATH argument to cmake ``conan_basic_setup()`` function
- Feature: Optimized uploads, now uploads will be skipped if there are no changes, irrespective of timestamp
- Feature: Automatic detection of VS 15-2017, via both a ``vs150comntools`` variable, and using ``vswhere.exe``
- Feature: Added NO_OUTPUT_DIRS argument to cmake ``conan_basic_setup()`` function
- Feature: Add support for Chocolatey system package manager for Windows.
- Feature: Improved in conan user home and path storage configuration, better error checks.
- Feature: ``export`` command is now able to export recipes without name or version, specifying the full reference.
- Feature: Added new default settings, Arduino, gcc-7.2
- Feature: Add conan settings to cmake generated file
- Feature: new ``tools.replace_prefix_in_pc_file()`` function to help with .pc files.
- Feature: Adding support for system package tool ``pkgutil`` on Solaris
- Feature: :command:`conan remote update` now allows :command:`--insert` argument to change remote order
- Feature: Add ``verbose`` definition to ``CMake`` helper.
- Fix: :command:`conan package` working locally failed if not specified build_folder
- Fix: Search when using wildcards for version like ``Pkg/*@user/channel``
- Fix: Change current working directory to the conanfile.py one before loading it, so relative python imports or code work.
- Fix: ``package_files`` command now works with ``short_paths`` too.
- Fix: adding missing require of tested package in test_package/conanfile build() method
- Fix: path joining in ``vcvars_command`` for custom VS paths defined via env-vars
- Fix: better managing string escaping in CMake variables
- Fix: ``ExecutablePath`` assignment has been removed from the ``visual_studio`` generator.
- Fix: removing ``export_source`` folder containing exported code, fix issues with read-only files and keeps cache consistency better.
- Fix: Accept 100 return code from yum check-update
- Fix: importing \*.so files from the :command:`conan new` generated test templates
- Fix: progress bars display when download/uploads are not multipart (reported size 0)
- Bugfix: fixed wrong OSX ``DYLD_LIBRARY_PATH`` variable for virtual environments
- Bugfix: ``FileCopier`` had a bug that affected ``self.copy()`` commands, changing base reference directory.


0.25.1 (20-July-2017)
---------------------

- Bugfix: Build requires are now applied correctly to test_package projects.
- Fix: Fixed search command to print an error when --table parameter is used without a reference.
- Fix: install() method of the CMake() helper, allows parallel building, change build folder and custom parameters.
- Fix: Controlled errors in migration, print warning if conan is not able to remove a package directory.

0.25.0 (19-July-2017)
---------------------

.. note::

  This release introduces a new layout for the local cache, with dedicated ``export_source`` folder to store the source code exported with ``exports_sources`` feature, which is much cleaner than the old ``.c_src`` subfolder. A migration is included to remove from the local cache packages with the old layout.

- Feature: new :command:`conan create` command that supersedes *test_package* for creating and testing package. It works even without the test_package folder, and have improved management for user, channel. The test_package recipe no longer defines ``requires``
- Feature: new :command:`conan get` command that display (with syntax highlight) package recipes, and any other file from conan: recipes, conaninfo.txt, manifests, etc.
- Feature: new :command:`conan alias` command that creates a special package recipe, that works like an **alias** or a **proxy** to other package, allowing easy definition and transparent management of "using the latest minor" and similar policies. Those special alias packages do not appear in the dependency graph.
- Feature: new :command:`conan search --table=file.html` command that will output an html file with a graphical representation of available binaries
- Feature: created **default profile**, that replace the ``[settings_default]`` in **conan.conf** and augments it, allowing to define more things like env-vars, options, build_requires, etc.
- Feature: new ``self.user_info`` member that can be used in ``package_info()`` to define custom user variables, that will be translated to general purpose variables by generators.
- Feature: :command:`conan remove` learned the :command:`--outdated` argument, to remove those binary packages that are outdated from the recipe, both from local cache and remotes
- Feature: :command:`conan search` learned the :command:`--outdated` argument, to show only those binary packages that are outdated from the recipe, both from local cache and remotes
- Feature: Automatic management ``CMAKE_TOOLCHAIN_FILE`` in ``CMake`` helper for cross-building.
- Feature: created ``conan_api``, a python API interface to conan functionality.
- Feature: new ``cmake.install()`` method of ``CMake`` helper.
- Feature: ``short_paths`` feature now applies also to ``exports_sources``
- Feature: ``SystemPackageTool`` now supports **FreeBSD** system packages
- Feature: ``build_requires`` now manage options too, also default options in package recipes
- Feature: :command:`conan build` learned new :command:`--package_folder` argument, useful if the build system perform the packaging
- Feature: ``CMake`` helper now defines by default ``CMAKE_INSTALL_PREFIX`` pointing to the current package_folder, so ``cmake.install()`` can transparently execute the packaging.
- Feature: improved command UX with cwd`` arguments to allow define the current directory for the command
- Feature: improved ``VisualStudioBuildEnvironment``
- Feature: transfers now show size (MB, KB) of download/uploaded files, and current status of transfer.
- Feature: :command:`conan new` now has arguments to generate CI scripts for Gitlab CI.
- Feature: Added ``MinRelSize`` and ``RelWithDebInfo`` management in ``CMake`` helper.
- Fix: make ``mkdir``, ``rmdir``, ``relative_dirs`` available for import from :command:`conans` module.
- Fix: improved detection of Visual Studio default under cygwin environment.
- Fix: ``package_files`` now allows symlinks
- Fix: Windows installer now includes conan_build_info tool.
- Fix: appending environment variables instead of overwriting them when they come from different origins: upstream dependencies and profiles.
- Fix: made opt-in the check of package integrity before uploads, it was taking too much time, and provide little value for most users.
- Fix: Package recipe linter removed some false positives
- Fix: default settings from conan.conf do not fail for constrained settings in recipes.
- Fix: Allowing to define package remote with :command:`conan remote add_ref` before download/upload.
- Fix: removed duplicated BUILD_SHARED_LIBS in test_package
- Fix: add "rhel" to list of distros using yum.
- Bugfix: allowing relative paths in ``exports`` and ``exports_sources`` fields
- Bugfix: allow custom user generators with underscore


0.24.0 (15-June-2017)
---------------------

- Feature: :command:`conan new` new arguments to generate **Travis-CI** and **Appveyor** files for Continuous Integration
- Feature: Profile files with ``include()`` and variable declaration
- Feature: Added ``RelWithDebInfo/MinRelSize`` to cmake generators
- Feature: Improved linter, removing false positives due to dynamic conanfile attributes
- Feature: Added ``tools.ftp_download()`` function for FTP retrieval
- Feature: Managing symlinks between folders.
- Feature: :command:`conan remote add` command learned new insert`` option to add remotes in specific order.
- Feature: support multi-config in the ``SCons`` generator
- Feature: support for gcc 7.1+ detection
- Feature: ``tools`` now are using global ``requests`` and ``output`` instances. Proxies will work for ``tools.download()``
- Feature: json`` parameter added to :command:`conan info`` command to create a JSON with the ``build_order``.
- Fix: update default repos, now pointing to Bintray.
- Fix: printing ``outdated from recipe`` also for remotes
- Fix: Fix required slash in ``configure_dir`` of ``AutoToolsBuildEnvironment``
- Fix: command ``new`` with very short names, now errors earlier.
- Fix: better error detection for incorrect ``Conanfile.py`` letter case.
- Fix: Improved some cmake robustness using quotes to avoid cmake errors
- BugFix: Fixed incorrect firing of building due to build`` patterns error
- BugFix: Fixed bug with options incorrectly applied to ``build_requires`` and crashing
- Refactor: internal refactorings toward having a python api to conan functionality


0.23.1 (05-June-2017)
---------------------

- BugFix: Fixed bug while packaging symlinked folders in build folder, and target not being packaged.
- Relaxed OSX requirement of pyopenssl to <18


0.23.0 (01-June-2017)
---------------------

- Feature: new ``build_requires`` field and ``build_requirements()`` in package recipes
- Feature: improved commands (source, build, package, package_files) and workflows for local development of packages in user folders.
- Feature: implemented ``no_copy_source`` attribute in recipes to avoid the copy of source code from "source" to "build folder". Created new ``self.source_folder``, ``self.build_folder``, ``self.package_folder`` for recipes to use.
- Feature: improved ``qmake`` generator with multi-config support, resource directories
- Feature: improved exception capture and formatting for all recipe user methods exceptions
- Feature: new ``tools.sha256()`` method
- Feature: folder symlinks working now for packages and upload/download
- Feature: added ``set_find_paths()`` to ``cmake-multi``, to set CMake FindXXX.cmake paths. This will work only for single-config build-systems.
- Feature: using environment variables for ``configure()``, ``requirements()`` and ``test()`` methods
- Feature: added a ``pylintrc`` environment variable in ``conan.conf`` to define a PYLINTRC file with custom style definitions (like indents).
- Feature: fixed ``vcvars`` architecture setting
- Fix: Make ``cacert.pem`` folder use CONAN_USER_HOME if existing
- Fix: fixed ``options=a=b`` option definition
- Fix: ``package_files`` command allows force`` argument to overwrite existing instead of failing
- BugFix: Package names with underscore when parsing ``conanbuildinfo.txt``


0.22.3 (03-May-2017)
--------------------

- Fix: Fixed CMake generator (in targets mode) with linker/exe flags like --framework XXX containing spaces.


0.22.2 (20-April-2017)
----------------------

- Fix: Fixed regression with usernames starting with non-alphabetical characters, introduced by 0.22.0


0.22.1 (18-April-2017)
----------------------

- Fix: "-" symbol available again in usernames.
- Fix: Added ``future`` requirement to solve an error with pyinstaller generating the Windows installer.


0.22.0 (18-April-2017)
----------------------

- Feature: ``[build_requires]`` can now be declared in ``profiles`` and apply them to build packages. Those requirements are only installed if the package is required to build from sources, and do not affect its package ID hash, and it is not necessary to define them in the package recipe. Ideal for testing libraries, cross compiling toolchains (like Android), development tools, etc.
- Feature: Much improved support for cross-building. Support for cross-building to **Android** provided, with toolchains installable via ``build_requires``.
- Feature: New ``package_files`` command, that is able to create binary packages directly from user files, without needing to define ``build()`` or ``package()`` methods in the the recipes.
- Feature: command :command:`conan new` with a new bare`` option that will create a minimal package recipe, usable with the ``package_files`` command.
- Feature: Improved ``CMake`` helper, with ``test()`` method, automatic setting of BUILD_SHARED_LIBS, better management of variables, support for parallel compilation in MSVC (via /MP)
- Feature: new ``tools.msvc_build_command()`` helper that both sets the Visual vcvars and calls Visual to build the solution. Also ``vcvars_command`` is improved to return non-empty string even if vcvars is set, for easier concatenation.
- Feature: Added package recipe linter, warning for potential errors and also about Python 3 incompatibilities when running from Python 2. Enabled by default can be opt-out.
- Feature: Improvements in HTML output of :command:`conan info --graph`.
- Feature: allow custom path to bash, as configuration and environment variable.
- Fix: Not issuing an unused variable warning in CMake for the CONAN_EXPORTED variable
- Fix: added new ``mips`` architectures and latest compiler versions to default settings.yml
- Fix: Unified username allowed patterns to those used in package references.
- Fix: hardcoded vs15 version in tools.vcvars
- BugFix: Clean crash and improved error messages when manifests mismatch exists in conan upload.


0.21.2 (04-April-2017)
----------------------

- Bugfix: virtualenv generator quoting environment variables in Windows.


0.21.1 (23-March-2017)
----------------------

- BugFix: Fixed missing dependencies in ``AutoToolsBuildEnvironment``
- BugFix: Escaping single quotes in html graph of :command:`conan info --graph=file.html`.
- BugFix: Fixed loading of auth plugins in conan_server
- BugFix: Fixed ``visual_studio`` generator creating XML with dots.


0.21.0 (21-March-2017)
----------------------

- Feature: :command:`conan info --graph` or graph=file.html`` will generate a dependency graph representation in dot or html formats.
- Feature: Added better support and tests for Solaris Sparc.
- Feature: custom authenticators are now possible in :command:`conan_server`` with plugins.
- Feature: extended :command:`conan info` command with path information and filter by packages.
- Feature: enabled conditional binary packages removal with :command:`conan remove` with query syntax
- Feature: enabled generation and validation of manifests from *test_package*.
- Feature: allowing ``options`` definitions in profiles
- Feature: new ``RunEnvironment`` helper, that makes easier to run binaries from dependent packages
- Feature: new ``virtualrunenv`` generator that activates environment variable for execution of binaries from installed packages, without requiring ``imports`` of shared libraries.
- Feature: adding new version modes for ABI compatibility definition in ``package_id()``.
- Feature: Extended :command:`conan new` command with new option for ``exports_sources`` example recipe.
- Feature: ``CMake`` helper defining parallel builds for gcc-like compilers via jN``, allowing user definition with environment variable and in conan.conf.
- Feature: :command:`conan profile`` command now show profiles in alphabetical order.
- Feature: extended ``visual_studio`` generator with more information and binary paths for execution with DLLs paths.
- Feature: Allowing relative paths with $PROFILE_DIR place holder in ``profiles``
- Fix: using only file checksums to decide for modified recipe in remote, for possible concurrent builds & uploads.
- Fix: Improved build`` modes management, with better checks and allowing multiple definitions and mixtures of conditions
- Fix: Replaced warning for non-matching OS to one message stating the cross-build
- Fix: local :command:`conan source`` command (working in user folder) now properly executes the equivalent of ``exports`` functionality
- Fix: Setting command line arguments to cmake command as CMake flags, while using the TARGETS approach. Otherwise, arch flags like -m32 -m64 for gcc were not applied.
- BugFix: fixed :command:`conan imports` destination folder issue.
- BugFix: Allowing environment variables with spaces
- BugFix: fix for CMake with targets usage of multiple flags.
- BugFix: Fixed crash of ``cmake_multi`` generator for "multi-config" packages.


0.20.3 (06-March-2017)
----------------------

- Fix: Added opt-out for ``CMAKE_SYSTEM_NAME`` automatically added when cross-building, causing users
  providing their own cross-build to fail
- BugFix: Corrected usage of ``CONAN_CFLAGS`` instead of ``CONAN_C_FLAGS`` in cmake targets


0.20.2 (02-March-2017)
----------------------

- Fix: Regression of ``visual_studio``generator using ``%(ExecutablePath)`` instead of ``$(ExecutablePath)``
- Fix: Regression for build=outdated --build=Pkg`` install pattern


0.20.1 (01-March-2017)
----------------------

- Fix: Disabled the use of cached settings and options from installed ``conaninfo.txt``
- Fix: Revert the use of quotes in ``cmake`` generator for flags.
- Fix: Allow comments in artifacts.properties
- Fix: Added missing commit for CMake new helpers


0.20.0 (27-February-2017)
-------------------------

**NOTE:** It is important that if you upgrade to this version, all the clients connected to the same
remote, should upgrade too. Packages created with conan>=0.20.0 might not be usable with conan older conan clients.

- Feature: Largely improved management of **environment variables**, declaration in ``package_info()``,
  definition in profiles, in command line, per package, propagation to consumers.
- Feature: New build helpers ``AutotoolsBuildEnvironment``, ``VisualStudioBuildEnvironment``, which
  deprecate ``ConfigureEnvironment``, with much better usage of environment variables
- Feature: New ``virtualbuildenv`` generator that will generate a composable environment with build
  information from installed dependencies.
- Feature: New ``build_id()`` recipe method that allows to define logic to build once, and package
  multiple times without building. E.g.: build once both debug and release artifacts, then package
  separately.
- Feature: **Multi-config packages**. Now packages can provide multi-configuration packages, like
  both debug/release artifacts in the same package, with ``self.cpp_info.debug.libs = [...]`` syntax.
  Not restricted to debug/release, can be used for other purposes.
- Feature: new :command:`conan config` command to manage, edit, display ``conan.conf`` entries
- Feature: :ref:`Improvements<cmake_reference>` to ``CMake`` build helper, now it has ``configure()`` and ``build()`` methods
  for common operations.
- Feature: Improvements to ``SystemPackageTool`` with detection of installed packages, improved
  implementation, installation of multi-name packages.
- Feature: Unzip with ``tools.unzip`` maintaining permissions (Linux, OSX)
- Feature: :command:`conan info` command now allows profiles too
- Feature: new tools ``unix_path()``, ``escape_windows_cmd()``, ``run_in_windows_bash()``, useful
  for autotools projects in Win/MinGW/Msys
- Feature: new context manager ``tools.chdir``, to temporarily change directory.
- Feature: CMake using ``CMAKE_SYSTEM_NAME`` for cross-compiling.
- Feature: Artifactory build-info extraction from traces
- Feature: Attach custom headers to artifacts uploads with an `artifacts.properties` file.
- Feature: allow and copy symlinks while :command:`conan export`
- Fix: removing quotes in some cmake variables that were generating incorrect builds
- Fix: providing better error messages for non existing binaries, with links to the docs
- Fix: improved error messages if ``tools.patch`` failed
- Fix: adding ``resdirs`` to ``cpp_info`` propagated information, and cmake variables, for directories
  containing resources and other data.
- Fix: printing error messages if a build`` policy doesn't match any package
- Fix: managing VS2017 by ``tools``. Still the manual definition of ``vs150comntools`` required.
- Bug fix: crashes when not supported characters were dumped to terminal by logger
- Bug fix: wrong executable path in Visual Studio generator


0.19.3 (27-February-2017)
-------------------------

- Fix: backward compatibility for new environment variables. New features to be introduced in 0.20
  will produce that ``conaninfo.txt`` will not be correctly parsed, and then package would be "missing".
  This will happen for packages created with 0.20, and consumed with older than 0.19.3

NOTE: It is important that you upgrade at least to this version if you are using remotes with packages
that might be created with latest conan releases (like conan.io).


0.19.2 (15-February-2017)
-------------------------

- Bug fix: Fixed bug with remotes behind proxies
- Bug fix: Fixed bug with ``exports_sources`` feature and nested folders


0.19.1 (02-February-2017)
-------------------------

- Bug fix: Fixed issue with :command:`conan copy`` followed by :command:`conan upload`` due to the new ``exports_sources``
  feature.


0.19.0 (31-January-2017)
------------------------

- Feature: ``exports_sources`` allows to snapshot sources (like ``exports``) but retrieve them strictly
  when necessary, to build from sources. This can largely improve install times for package recipes
  containing sources
- Feature: new configurable **tracer** able to create structured logs of conan actions: commands, API calls, etc
- Feature: new logger for ``self.run`` actions, able to log information from builds and other commands
  to files, that can afterwards be packaged together with the binaries.
- Feature: support for **Solaris SunOS**
- Feature: ``Version`` helper improved with ``patch, pre, build`` capabilities to handle ``1.3.4-alpha2+build1`` versions
- Feature: compress level of tgz is now configurable via ``CONAN_COMPRESSION_LEVEL`` environment variable,
  default 9. Reducing it can lead to faster compression times, at the expense of slightly bigger archives
- Feature: Add **powershell** support for virtualenv generator in Windows
- Feature: Improved ``system_requirements()`` raising errors when failing, retrying if not successful,
  being able to execute in user space for local recipes
- Feature: new cmake helper macro ``conan_target_link_libraries()``.
- Feature: new cmake ``CONAN_EXPORTED`` variable, can be used in CMakeLists.txt to differentiate building
  in the local conan cache as package and building in user space
- Fix: improving the caching of options from :command:`conan install` in conaninfo.txt and precedence.
- Fix: conan definition of cmake output dirs has been disabled for ``cmake_multi`` generator
- Fix: ``imports()`` now uses environment variables at "conan install" (but not at "conan imports" yet)
- Fix: ``conan_info()`` method has been renamed to ``package_id()``. Backward compatibility is maintained,
  but it is strongly encouraged to use the new name.
- Fix: ``conan_find_libraries`` now use the NO_CMAKE_FIND_ROOT_PATH parameter for avoiding issue while cross-compiling
- Fix: disallowing duplicate URLs in remotes, better error management
- Fix: improved error message for wildcard uploads not matching any package
- Fix: remove deprecated ``platform.linux_distribution()``, using new "distro" package
- Bugfix: fixed management of ``VerifySSL`` parameter for remotes
- Bugfix: fixed misdetection of compiler version in conanbuildinfo.cmake for apple-clang
- Bugfix: fixed trailing slash in remotes URLs producing crashes
- Refactor: A big refactor has been do to ``options``. Nested options are no longer supported, and
  ``option.suboption`` will be managed as a single string option.

This has been a huge release with contributors of 11 developers. Thanks very much to all of them!


0.18.1 (11-January-2017)
------------------------

- Bug Fix: Handling of transitive private dependencies in modern cmake targets
- Bug Fix: Missing quotes in CMake macro for modern cmake targets
- Bug Fix: Handling LINK_FLAGS in cmake modern targets
- Bug Fix: Environment variables no propagating to test project with test_package command


0.18.0 (3-January-2017)
-----------------------

- Feature: uploads and downloads with **retries** on failures. This helps to avoid having to fully
  rebuild on CI when a network transfer fails
- Feature: added **SCons** generator
- Feature: support for **Python 3.6**, with several fixes. Added Python 3.6 to CI.
- Feature: show package dates in :command:`conan info` command
- Feature: new ``cmake_multi`` generator for multi-configuration IDEs like Visual Studio and Xcode
- Feature: support for **Visual Studio 2017**, VS-15
- Feature: **FreeBSD** now passes test suite
- Feature: :command:`conan upload` showing error messages or URL of remote
- Feature: **wildcard or pattern upload**. Useful to upload multiple packages to a remote.
- Feature: allow defining **settings as environment variables**. Useful for use cases like dockerized builds.
- Feature: improved help`` messages
- Feature: cmake helper tools to launch conan directly from cmake
- Added **code coverage** for code repository
- Fix: conan.io badges when containing dash
- Fix: manifests errors due to generated .pyc files
- Bug Fix: unicode error messages crashes
- Bug Fix: duplicated build of same binary package for private dependencies
- Bug Fix: duplicated requirement if using version-ranges and ``requirements()`` method.


0.17.2 (21-December-2016)
-------------------------

- Bug Fix: ConfigureEnvironment helper ignoring libcxx setting. #791


0.17.1 (15-December-2016)
-------------------------

- Bug Fix: conan install --all generating corrupted packages. Thanks to @yogeva
- Improved case sensitive folder management.
- Fix: appveyor links in README.


0.17.0 (13-December-2016)
-------------------------

- Feature: support for **modern cmake** with cmake ``INTERFACE IMPORTED`` targets defined per package
- Feature: support for more advanced queries in search.
- Feature: new ``profile list|show`` command, able to list or show details of profiles
- Feature: adding preliminary support for **FreeBSD**
- Feature: added new ``description`` field, to document package contents.
- Feature: generation of **imports manifest** and :command:`conan imports --undo` functionality to remove
  imported files
- Feature: optional SSL certificate verification for remotes, to allow self signed certificates
- Feature: allowing custom paths in profiles, so profiles can be easily shared in teams, just
  inside the source repository or elsewhere.
- Feature: fields ``user`` and ``channel`` now available in conan recipes. That allows to declare
  requirements for the same user/channel as the current package.
- Feature: improved conan.io package web, adding description.
- Fix: allow to modify cmake generator in ``CMake`` helper class.
- Fix: added ``strip`` parameter to ``tools.patch()`` utility
- Fix: removed unused dependency to Boto
- Fix: wrong line endings in Windows for conan.conf
- Fix: proper automatic use of ``txt`` and ``env`` generators in *test_package*
- Bug fix: solved problem when uploading python packages that generated .pyc at execution
- Bug fix: crash when duplicate requires were declared in conanfile
- Bug fix: crash with existing imported files with symlinks
- Bug fix: options missing in "copy install command to clipboard" in web


0.16.1 (05-December-2016)
-------------------------

- Solved bug with *test_package* with arguments, like scopes.


0.16.0 (19-November-2016)
-------------------------

**Upgrade**: The build=outdated`` feature had a change in the hash computation, it might report
outdated binaries from recipes. You can re-build the binaries or ignore it (if you haven't changed
your recipes without re-generating binaries)

- Feature: **version ranges**. Conan now supports defining requirements with version range expressions
  like ``Pkg/[>1.2,<1.9||1.0.1]@user/channel``. Check the :ref:`version ranges reference <version_ranges>` for details
- Feature: decoupled ``imports`` from normal install. Now :command:`conan install --no-imports` skips the
  imports section.
- Feature: new :command:`conan imports` command that will execute the imports section without running install
- Feature: **overriding settings per package**. Now it is possible to specify individual settings
  for each package. This can be specified both in the command line and in ``profiles``
- Feature: **environment variables** definition in the command line, global and per package. This
  allows to define specific environment variables as the compiler (CC, CXX) for a specific package.
  These environment variables can also be defined in ``profiles``. Check :ref:`profiles reference <profiles>`
- Feature: Now conan files copies handle **symlinks**, so files are not duplicated. This will
  save some space and improve download speed in some large packages. To enable it, use
  ``self.copy(..., links=True)``
- Fix: Enabling correct use of **MSYS** in Windows, by using the Windows ``C:/...`` path instead of
  the MSYS ones
- Fix: Several fixes in :command:`conan search`, both local and in remotes
- Fix: Manifests line endings and order fix, and hash computation fixed (it had wrong ordering)
- Fix: Removed http->https redirection in conan_server that produced some issues for SSL reversed
  proxies
- Fix: Taking into account "ANY" definition of settings and options
- Fix: Improved some error messages and failures to encode OS errors with unicode characters
- Update: added new arch ``ppc64`` to default settings
- Update: updated python-requests library version
- Fix: Using ``generator()`` instead of compiler to decide on cmake multi-configuration for Ninja+cl
  builds
- Improved and completed documentation


0.15.0 (08-November-2016)
-------------------------

**Upgrade**: If you were using the ``short_paths`` feature in Windows for packages with long paths, please
reset your local cache. You could manually remove packages or just run :command:`conan remove "*"`

- Feature: New build=outdated`` functionality, that allows to build the binary packages for
  those dependencies whose recipe has been changed, or if the binary is not existing. Each
  binary package stores a hash of the recipe to know if they have to be regenerated (are outdated).
  This information is also provided in the :command:`conan search <ref>`` command. Useful for package
  creators and CI.
- Feature: Extended the ``short_paths`` feature for Windows path limit to the ``package`` folder, so package
  with very long paths, typically in headers in nested folder hierarchies are supported.
- Feature: New ``tool.build_sln_command()`` helper to ``build()`` Microsoft Visual Studio solution (.sln)
  projects
- Feature: Extended the ``source`` and ``package`` command, so together with ``build`` they can be fully
  executed in a user folder, as a convenience for package creation and testing.
- Feature: Extending the scope of ``tools.pythonpath`` to work in local commands too
- Improved the parsing of ``profiles`` and better error messages
- Not adding ``-s`` compiler flag for clang, as it doesn't use it.
- Automatic generation of *conanenv.txt* in local cache, warnings if using local commands and no
  ``conanbuildinfo.txt`` and no *conanenv.txt* are present to cache the information form install
- Fix: Fixed bug when using empty initial requirements (``requires = ""``)
- Fix: Added ``glob`` hidden import to pyinstaller
- Fix: Fixed minor bugs with ``short_paths`` as local search not listing packages
- Fix: Fixed problem with virtual envs in Windows with paths separator (using / instead of \)
- Fix: Fixed parsing of conanbuildinfo.txt, so the root folder for each dependency is available in local
  commands too
- Fix: Fixed bug in *test_package* with the test project using the ``requirements()`` method.

0.14.1 (20-October-2016)
------------------------

- Fixed bug with `short_paths` feature in windows.
- Improved error messages for non-valid `profile` test files.
- Remove downloaded tgz package files from remotes after decompress them.
- Fixes bug with `install --all` and short_paths


0.14.0 (20-October-2016)
------------------------

- Feature: Added profiles, as user predefined settings and environment variables (as CC and CXX
  for compiler paths). They are stored in files in the conan cache, so they can be easily edited,
  added, and shared. Use them with :command:`conan install --profile=name`
- Feature: ``short_paths`` feature for Windows now also handle long paths for the final package,
  in case that a user library has a very long final name, with nested subfolders.
- Feature: Added ``tools.cpu_count()`` as a helper to retrieve the number of cores, so it can be
  used in concurrent builds
- Feature: Detects cycles in the dependency graph, and raise error instead of exhausting recursion
  limits
- Feature: Conan learned the werror`` option that will raise error and stop installation under
  some cases treated as warnings otherwise: Duplicated dependencies, or dependencies conflicts
- Feature: New ``env`` generator that generates a text file with the environment variables defined
  by dependencies, so it can be stored. Such file is parsed by :command:`conan build` to be able to use
  such environment variables for ``self.deps_env_info`` too, in the same way it uses the ``txt``
  generator to load variables for ``self.deps_cpp_info``.
- Fix: Do not print progress bars when output is a file
- Fix: Improved the local conan search, using options too in the query :command:`conan search -q option=value`
- Fix: Boto dependency updated to 2.43.0 (necessary for ArchLinux)
- Fix: Simplified the :command:`conan package` command, removing unused and confusing options, and more
  informative messages about errors and utility of this command.
- Fix: More fixes and improvements on ``ConfigureEnvironment``, mainly for Windows
- Fix: Conan now does not generate a ``conanbuildinfo.txt`` file when doing :command:`conan install <PkgRef>`.
- Bug fix: Files of a package recipe are "touched" to update their timestamps to current time when
  retrieved, otherwise some build systems as Ninja can have problems with them.
- Bug fix: ``qmake`` generator now uses quotes to handle paths with spaces
- Bug fix: Fixed ``OSInfo`` to return the short distro name instead of the long one.
- Bug fix: fixed transitivity of ``private`` dependencies


0.13.3 (13-October-2016)
------------------------

This minor solves some problems with ``ConfigureEnvironment``, mainly for Windows, but also fixes
other things:

- Fixed concatenation problems in Windows for several environment variables. Fixed problems with
  path with spaces
- A batch file is created in Windows to be called, as ``if defined`` structures doesn't seem to
  work in the command line.
- The ``vcvars_command`` from ``tools`` now checks the Visual Studio environment variable, if it is
  already set, it will check it with the current project settings, throwing an error if not matching,
  returning an empty command if matches.
- Added a ``compile_flags`` property to ``ConfigureEnvironment``, to be passed in the command line
  to the compiler, but not as environment variables
- Added ``defines`` to environment for nix systems, it was not being handled before
- Added new tests, compiling simple projects and diamond dependencies with cmake, cl (msvc), gcc (gcc in linux, mingw in win)
  and clang (OSX), for a better coverage of the ``ConfigureEnvironment`` functionality.
- Fixed wrong ``CPP_INCLUDE_PATH``, it is now ``CPLUS_INCLUDE_PATH``


0.13.0 (03-October-2016)
------------------------

**IMPORTANT UPGRADE ISSUE:** There was a small error in the computation of binary packages IDs, that
has been addressed by conan 0.13. It affects to third level (and higher) binary packages, i.e. A
and B in A->B->C->D, which binaries **must** be regenerated for the new hashes. If you don't plan
to provide support for older conan releases (<=0.12), which would be reasonable, you should remove
all binaries first (:command:`conan remove -p`, works both locally and remotely), then re-build your binaries.

Features:

- Streaming from/to disk for all uploads/downloads. Previously, this was done for memory, but conan
  started to have issues for huge packages (>many hundreds MBs), that sometimes could be alleviated
  using Python 64 bits distros. This issues should be alleviated now
- New security system that allows capturing and checking the package recipes and binaries manifests
  into user folders (project or any other folder). That ensures that packages cannot be replaced,
  hacked, forged, changed or wrongly edited, either locally or in any remote server, without notice.
- Possible to handle and reuse python code in recipes. Actually, conan can be used as a package
  manager for python, by adding the package path to ``env_info.PYTHONPATH``. Useful if you want to
  reuse common python code between different package recipes.
- Avoiding re-compress the tgz for packages after uploads if it didn't change.
- New command :command:`conan source` that executes the ``source()`` method of a given conanfile. Very
  useful for CI, if desired to run in parallel the construction of different binaries.
- New propagation of ``cpp_info``, so it now allows for capturing binary packages libraries with new
  ``collect_libs()`` helper, and access to created binaries to compute the ``package_info()`` in general.
- Command *test_package* now allows the update`` option, to automatically update dependencies.
- Added new architectures for ``ppc64le`` and detection for ``AArch64``
- New methods for defining requires effect over binary packages ID (hash) in ``conan_info()``
- Many bugs fixes: error in ``tools.download`` with python 3, restore correct prompt in virtualenvs,
  bug if removing an option in ``config_options()``, setup.py bug...

This release has contributions from @tru, @raulbocanegra, @tivek, @mathieu, and the feedback of many
other conan users, thanks very much to all of them!


0.12.0 (13-September-2016)
--------------------------

- Major changes to **search** api and commands. Decoupled the search of package recipes, from the
  search of binary packages.
- Fixed bug that didn't allow to ``export`` or ``upload`` packages with settings restrictions if the
  restrictions didn't match the host settings
- Allowing disabling color output with ``CONAN_COLOR_DISPLAY=0`` environment variable, or to configure
  color schema for light console backgrounds with ``CONAN_COLOR_DARK=1`` environment variable
- Imports can use absolute paths, and files copied from local conan cache to those paths will not
  be removed when :command:`conan install`. Can be used as a way to install machine-wise things (outside
  conan local cache)
- More robust handling of failing transfers (network disconnect), and inconsistent status after such
- Large internal refactor for storage managers. Improved implementations and decoupling between
  server and client
- Fixed slow :command:`conan remove` for caches with many packages due to slow deletion of empty folders
- Always allowing explicit options scopes, ``- o Package:option=value`` as well as the implicit
  ``-o option=value`` for current ``Package``, for consistency
- Fixed some bugs in client-server auth process.
- Allow to extract ``.tar`` files in ``tools.unzip()``
- Some helpers for ``conan_info()``, as ``self.info.requires.clear()`` and removal of settings and options


0.11.1 (31-August-2016)
-----------------------

- New error reporting for failures in conanfiles, including line number and offending line, much
  easier for package creators
- Removed message requesting to create an account in **conan.io** for other remotes
- Removed localhost:9300 remote that was added by default mostly for demo purposes. Clarified in docs.
- Fixed usernames case-sensitivity in conan_server, due to ConfigParser it was forcing lowercase
- Handling unicode characters in remote responses, fixed crash
- Added new compilers gcc 6.2, clang 8.0 to the default ``settings.yml``
- Bumped cryptography, boto and other conan dependencies, mostly for ArchLinux compatibility and
  new OSX security changes


0.11.0 (3-August-2016)
----------------------

- New solution for the path length limit in Windows, more robust and complete. Package conanfile.py
  just have to declare an attribute ``short_paths=True`` and everything will be managed. The old
  approach is deprecated and totally removed, so no shorts_paths.conf file is necessary. It should
  fix also the issues with uploads/retrievals.
- New ``virtualenv`` generator that generates ``activate`` and ``deactivate`` scripts that set
  environment variables in the current shell. It is very useful, for example to install tools
  (like CMake, MinGW) with conan packages, so multiple versions can be installed in the same machine,
  and switch between them just by activating such virtual environments. Packages for MinGW and CMake
  are already available as a demo
- ConfigureEnvironment takes into account environment variables, defined in packages in new ``env_info``,
  which is similar to ``cpp_info`` but for environment information (like paths).
- New per-package ``build_policy``, which can be set to ``always`` or ``missing``, so it is not
  necessary to create packages or specify the build`` parameter in command line. Useful for example
  in header only libraries or to create packages that always get the latest code from a branch in a github
  repository.
- Command :command:`conan test_package`` now executes by default a :command:`conan export` with smarter package
  reference deduction. It is introduced as opt-out behavior.
- Conan :command`export` command avoids copying *test_package/build* temporary files in case of ``export=*``
- Now, ``package_info()`` allows absolute paths in ``includedir``, ``libdirs`` and ``bindirs``, so
  wrapper packages can be defined that use system or manually installed libraries.
- LDFLAGS in ``ConfigureEnvironment`` management of OSX frameworks.
- Options allow the ``ANY`` value, so such option would accept any value. For example a commit of a
  git repository, useful to create packages that can build any specific commit of a git repo.
- Added gcc 5.4 to the default settings, as well as MinGW options (Exceptions, threads...)
- Command :command:`conan info` learned a new option to output the packages from a project dependency tree that
  should be rebuilt in case of a modification of a certain package. It outputs a machine readable **ordered**
  list of packages to be built in that order. Useful for CI systems.
- Better management of incomplete, dirty or failed ``source`` directories (e.g. in case of a user
  interrupting with Ctrl+C a git clone inside the ``source()`` method.
- Added tools for easier detection of different OS versions and distributions, as well as command
  wrappers to install system packages (apt, yum). They use ``sudo`` via a new environment variable
  CONAN_SYSREQUIRES_SUDO, so using sudo is opt-in/out, for users with different sudo needs. Useful for ``system_requirements()``
- Deprecated the ``config()`` method (still works, for backwards compatibility), but has been replaced
  by a ``config_options()`` to modify options based on settings, and a ``configure()`` method for
  most use cases. This removes a nasty behavior of having the ``config()`` method called twice with
  side effects.
- Now, running a :command:`conan install MyLib/0.1@user/channel` to directly install packages without any
  consuming project, is also able to generate files with the ``-g`` option. Useful for installing
  tool packages (MinGW, CMake) and generate ``virtualenvs``.
- Many small fixes and improvements: detect compiler bug in Py3, search was crashing for remotes,
  conan new failed if the package name had a dash, etc.
- Improved some internal duplications of code, refactored many tests.

This has been a big release. Practically 100% of the released features are thanks to active users
feedback and contributions. Thanks very much again to all of them!


0.10.0 (29-June-2016)
---------------------

- **conan new** command, that creates conan package conanfile.py templates, with a *test_package* package test (-t option),
  also for header only packages (-i option)
- Definition of **scopes**. There is a default **dev** scope for the user project, but any other scope (test, profile...) can be defined and used in packages. They can be used to fire extra processes (as running tests), but they do not affect the package binaries, and are not included in the package IDs (hash).
- Definition of **dev_requires**. Those are requirements that are only retrieved when the package is in **dev** scope, otherwise they are not. They do not affect the binary packages. Typical use cases would be test libraries or build scripts.
- Allow **shorter paths** for specific packages, which can be necessary to build packages with very long path names (e.g. Qt) in Windows.
- Support for bzip2 and gzip decompression in ``tools``
- Added ``package_folder`` attribute to conanfile, so the ``package()`` method can for example call ``cmake install`` to create the package.
- Added ``CONAN_CMAKE_GENERATOR`` environment variable that allows to override the ``CMake`` default generator. That can be useful to build with Ninja instead of the default Unix Makefiles
- Improved ``ConfigureEnvironment`` with include paths in CFLAGS and CPPFLAGS, and fixed bug.
- New :command:`conan user --clean` option, to completely remove all user data for all remotes.
- Allowed to raise ``Exceptions`` in ``config()`` method, so it is easier for package creators to raise under non-supported configurations
- Fixed many small bugs and other small improvements

As always, thanks very much to all contributors and users providing feedback.

0.9.2 (11-May-2016)
-------------------
- **Fixed download bug** that made it specially slow to download, even crash. Thanks to github @melmdk for fixing it.
- **Fixed cmake check of CLang**, it was being skipped
- **Improved performance**. Check for updates has been removed from install, made it opt-in in :command:`conan info` command, as it
  was very slow, seriously affecting performance of large projects.
- Improved internal representation of graph, also improves performance for large projects.
- Fixed bug in :command:`conan install --update`.


0.9 (3-May-2016)
----------------

- **Python 3** "experimental" support. Now the main conan codebase is Python 2 and 3 compatible.
  Python 2 still the reference platform, Python 3 stable support in next releases.
- Create and share your **own custom generators for any build system or tool**. With "generator packages",
  you can write a generator just as any other package, upload it, modify and version it, etc. Require
  them by reference, as any other package, and pull it into your projects dynamically.
- **Premake4** initial experimental support via a generator package.
- Very large **re-write of the documentation**. New "creating packages" sections with in-source and out-source explicit examples.
  Please read it! :)
- Improved :command:`conan test`. Renamed ``test`` to *test_package* both for the command and the folder,
  but backwards compatibility remains. Custom folder name also possible.
  **Adapted test layout** might require minor changes to your package test,
  automatic warnings added for your convenience.
- Upgraded pyinstaller to generate binary OS installers from 2.X to 3.1
- :command:`conan search` now has command line options:, less verbose, verbose, extra verbose
- Added variable with full list of dependencies in conanbuildinfo.cmake
- Several minor bugfixes (check github issues)
- Improved :command:`conan user` to manage user login to multiple remotes


0.8.4 (28-Mar-2016)
-------------------

- Fixed linker problems with the new apple-clang 7.3 due to libraries with no timestamp set.
- Added apple-clang 7.3 to default settings
- Fixed default libcxx for apple-clang in auto detection of base conan.conf


0.8 (15-Mar-2016)
-----------------

- New **conan remote** command to manage remotes. Redesigned remotes architecture, now allows
  to work with several remotes in a more consistent, powerful and "git-like" way. New remotes
  registry keeps track of the remote of every installed package, and this information is shown
  in :command:`conan info` command too. Also, it keeps different user logins for different remotes, to
  improve support in corporate environments running in-house servers.
- New **update** functionality. Now it is possible to :command:`conan install --update` to update packages
  that became obsolete because new ones were uploaded to the corresponding remote. Conan commands
  as install and info show information about the status of the local packages compared with the
  remote ones. In this way, using latest versions during development is much more natural.
- Added new **compiler.libcxx** setting in order to support the different c++ standard libraries.
  It can take libstdc++, libstdc++11 or libc++ values to take into account different standard
  libraries for modern gcc and clang compilers. It is also possible to remove not needed settings,
  like this one in pure C projects, with the new syntax: ``del self.settings.compiler.libcxx``
- Conan **virtual environment**: Define a custom conan directory with **CONAN_USER_HOME** env variable,
  and have a per project or per workspace storage for your dependencies. So you can isolate your
  dependencies and even bundle them within your project, by just setting the CONAN_USER_HOME
  variable to your ``<project>/deps`` folder, for example. This also improves support for continuous
  integration CI systems, in which many builds from different users could be run in parallel.
- Better conanfile download method. More stable and now checks (opt-out) the **ssl certificates**.
- Lots of improvements: Increased library name length limit, Improved and cleaner output messages.
- Fixed several minor bugs: removing empty folders, case sensitive exports, arm settings detection.
- Introduced the concept of **"package recipe"** that refers to conanfile.py and exported files.
- Improved settings display in web, with new "copy install command to clipboard" to assist in
  installing packages discovered in web.
- The macOS installer, problematic with latest macOS releases, has been deprecated in favor
  of homebrew and pip install procedures.


0.7 (5-Feb-2016)
----------------

- Custom conanfile names are allowed for developing. With file`` option you can define
  the file you want to use, allowing for ``.conaninfo.txt`` or having multiple ``conanfile_dev.py``,
  ``conanfile_test.py`` besides the standard ``conanfile.py`` which is used for sharing the package.
  Inheritance is allowed, e.g. ``conanfile_dev.py`` might extend/inherit from ``conanfile.py``.
- New :command:`conan copy` command that can be used to copy/rename packages, promote them between channels,
  forking other users packages.
- New all`` and package`` options for :command:`conan install` that allows to download one, several,
  or all package configurations for a given reference.
- Added ``patch()`` tool to easily patch sources if necessary.
- New **qmake** and **qbs** generators
- Upload of conanfile **exported** files is also **tgz'd**, allowing fast upload/downloads of
  full sources if desired, avoiding retrieval of sources from externals sources.
- :command:`conan info` command improved showing info of current project too
- Output of ``run()`` can be redirected to buffer string for processing, or even removed.
- Added **proxy** configuration to conan.conf for users behinds proxies.
- Large improvements in commands output, prefixed with package reference, and much clear.
- Updated settings for more versions of gcc and new arm architectures
- Treat dependencies includes as SYSTEM in cmake, so no warnings are raised
- Deleting source folder after :command:`conan export` so no manual removal is needed
- Normalizing to CRLF generated user files in Win
- Better detection and checks for compilers as VS, apple-clang
- Fixed CMAKE_SHARED_LINKER_FLAGS typo in cmake files
- Large internal refactor in generators


0.6 (11-Jan-2016)
-----------------

- New cmake variables in cmake generator to make FindPackage work better thanks to the underlaying FindLibrary. Now many FindXXX.cmake work "as-is" and the package creator does not have to create a custom override, and consumers can use packages transparently with the originals FindXXX.cmakes
- New "conan info" command that shows the full dependency graph and details (license, author, url, dependants, dependencies) for each dependency.
- New environment helper with a ConfigureEnvironment class, that is able to translate conan information to autotools configure environment definition
- Relative importing from conanfiles now is possible. So if you have common functionality between different packages, you can reuse those python files by importing them from the conanfile.py. Note that export="..." might be necessary, as packages as to be self-contained.
- Added YouCompleteMe generator for vim auto-completion of dependencies.
- New "conanfile_directory" property that points to the file in which the conanfile.py is located. This helps if using the conanfile.py "build" method to build your own project as a project, not a package, to be able to use any workflow, out-of-source builds, etc.
- Many edits and improvements in help, docs, output messages for many commands.
- All cmake syntax in modern lowercase
- Fixed several minor bugs: gcc detection failure when gcc not installed, missing import, copying source->build failing when symlinks


0.5 (18-Dec-2015)
-----------------

- New cmake functionality allows package creators to provide cmake finders, so that package consumers
  can use their CMakeLists.txt with typical FindXXX.cmake files, without any change to them. CMake CONAN_CMAKE_MODULES_PATH
  added, so that package creators can provide any additional cmake scripts for consumers.
- Now it is possible to generate out-of-source and multiple configuration installations for the
  same project, so you can switch between them without having to :command:`conan install` again. Check :ref:`the new workflows<workflows>`
- New qmake generator (thanks @dragly)
- Improved removal/deletion of folders with shutil.rmtree, so :command:`conan remove` commands and other
  processes requiring deletion of folders do not fail due to permissions and require manual deletion.
  This is an improvement, especially in Win.
- Created ``pip`` package, so conan can be installed via: ``pip install conan``
- Released ``pyinstaller`` code for the creation of binaries from conan python source code. Distros package creators can
  create packages for the conan apps easily from those binaries.
- Added md5, sha1, sha256 helpers in ``tools``, so external downloads from ``conanfile.py`` files ``source()``
  can be checked.
- Added latest gcc versions to default ``settings.yml``
- Added CI support for conan development: travis-ci, appveyor
- Improved human-readability for download progress, help messages.
- Minor bug fixes
