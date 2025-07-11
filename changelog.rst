Changelog
=========

For a more detailed description of the major changes that Conan 2 brings, compared with Conan 1.X, please read :ref:`whatsnew`

2.18.1 (04-Jul-2025)
--------------------

- Bugfix: Revert remote caching for missing packages `#18586 <https://github.com/conan-io/conan/pull/18586>`_

2.18.0 (30-Jun-2025)
--------------------

- Feature: Allow consuming meson libname.a libs in ``MSBuildDeps``. `#18557 <https://github.com/conan-io/conan/pull/18557>`_
- Feature:  Avoid library renames when using Meson + MSVC + static builds. `#18533 <https://github.com/conan-io/conan/pull/18533>`_
- Feature: Added `threads` subsetting in `emcc` compiler model. `#18520 <https://github.com/conan-io/conan/pull/18520>`_ . Docs `here <https://github.com/conan-io/docs/pull/4115>`__
- Feature: New ``conan cache ref <path>`` to reverse look the Conan cache, with a path argument will return the reference of the artifact in that folder. Intended exclusively for debugging purposes. `#18518 <https://github.com/conan-io/conan/pull/18518>`_ . Docs `here <https://github.com/conan-io/docs/pull/4146>`__
- Feature: New linker flags autodetected by conan based on profile architecture. `#18498 <https://github.com/conan-io/conan/pull/18498>`_
- Feature: Changed `conanws.yml` format. Now, `packages` is a list of dict-like objects. `#18493 <https://github.com/conan-io/conan/pull/18493>`_ . Docs `here <https://github.com/conan-io/docs/pull/4138>`__
- Feature: Added support for ``.exe`` in editables packages in ``CMakeConfigDeps``. `#18489 <https://github.com/conan-io/conan/pull/18489>`_
- Feature: Add `build_folder` parameter in `basic_layout`. `#18442 <https://github.com/conan-io/conan/pull/18442>`_ . Docs `here <https://github.com/conan-io/docs/pull/4140>`__
- Feature: Using `pkg_config_name = 'none'` to skip the `*.pc` file creation. `#18439 <https://github.com/conan-io/conan/pull/18439>`_ . Docs `here <https://github.com/conan-io/docs/pull/4135>`__
- Feature: Add support for sbom and lockfiles to `conan audit list`. `#18437 <https://github.com/conan-io/conan/pull/18437>`_ . Docs `here <https://github.com/conan-io/docs/pull/4134>`__
- Feature: Added first class citizen emscripten support (new wasm64 architecture + emcc). `#18432 <https://github.com/conan-io/conan/pull/18432>`_ . Docs `here <https://github.com/conan-io/docs/pull/4115>`__
- Feature: Replace `tools.cmake:install_strip` by `tools.install:strip`. Affect both CMake and Meson tool helpers. `#18429 <https://github.com/conan-io/conan/pull/18429>`_ . Docs `here <https://github.com/conan-io/docs/pull/4121>`__
- Feature: Add `open` to `TestClient` to open files locally. `#18399 <https://github.com/conan-io/conan/pull/18399>`_
- Feature: New ``conan workspace create`` orchestrated. `#18390 <https://github.com/conan-io/conan/pull/18390>`_ . Docs `here <https://github.com/conan-io/docs/pull/4138>`__
- Feature: Add ``context`` variable to profile jinja2 rendering (can be "build", "host" and ``None``). `#18383 <https://github.com/conan-io/conan/pull/18383>`_ . Docs `here <https://github.com/conan-io/docs/pull/4136>`__
- Feature: Implement ``cpp_info.sources`` to support source targets. `#18350 <https://github.com/conan-io/conan/pull/18350>`_ . Docs `here <https://github.com/conan-io/docs/pull/4128>`__
- Feature: Add support for source targets in CMakeConfigDeps generator. `#18350 <https://github.com/conan-io/conan/pull/18350>`_ . Docs `here <https://github.com/conan-io/docs/pull/4128>`__
- Feature: New `conan report diff` command to inspect diffs between versions and revisions. `#18247 <https://github.com/conan-io/conan/pull/18247>`_ . Docs `here <https://github.com/conan-io/docs/pull/4127>`__
- Feature: Add premake toolchain and improved premake integration in conan with new premake5. `#17898 <https://github.com/conan-io/conan/pull/17898>`_ . Docs `here <https://github.com/conan-io/docs/pull/4090>`__
- Fix: Better error message in ``CMakeConfigDeps`` for incorrect component requires. `#18562 <https://github.com/conan-io/conan/pull/18562>`_
- Fix: Avoid incorrect absolute path inputs in ``-of`` for relativize paths in generators. `#18561 <https://github.com/conan-io/conan/pull/18561>`_
- Fix: Better error message when an incorrect ``cpp_info.requires`` is defined. `#18552 <https://github.com/conan-io/conan/pull/18552>`_
- Fix: Avoid hyphens for msbuild verbosity argument passed to CMake after `--` by powershell. `#18548 <https://github.com/conan-io/conan/pull/18548>`_
- Fix: Improve `conan cache check-integrity` output. `#18544 <https://github.com/conan-io/conan/pull/18544>`_
- Fix: Raise an error for incorrect definition of ``conf_info`` items. `#18541 <https://github.com/conan-io/conan/pull/18541>`_
- Fix: Fix ``qcc`` ``cppstd`` support for latest QNX 8.0 with c++20. `#18538 <https://github.com/conan-io/conan/pull/18538>`_
- Fix: SBOM component `bom-ref` should not use `has_special_root_node`. `#18515 <https://github.com/conan-io/conan/pull/18515>`_
- Fix: Add a deprecated warning message for ``Node.dependencies``, now renamed to ``Node.edges``. `#18472 <https://github.com/conan-io/conan/pull/18472>`_
- Fix: Fix issue with missing folder in local-recipes-index. `#18449 <https://github.com/conan-io/conan/pull/18449>`_
- Fix: `Git.get_remote_url` now returns only the URL when using treeless repository. `#18444 <https://github.com/conan-io/conan/pull/18444>`_
- Fix: Improvement over ill-formed graphs with different `visible=True/False` for the same dependency. `#18440 <https://github.com/conan-io/conan/pull/18440>`_ . Docs `here <https://github.com/conan-io/docs/pull/4139>`__
- Fix: Fixing CMake presets on Windows with backslash. `#18435 <https://github.com/conan-io/conan/pull/18435>`_
- Fix: Do not output upload-urls on basic text :command:`conan upload` output. `#18430 <https://github.com/conan-io/conan/pull/18430>`_
- Fix: Create folders if they don't exist when using `--out-file`. `#18427 <https://github.com/conan-io/conan/pull/18427>`_
- Fix: Fix AutotoolsToolchain/GnuToolchain with LLVM/Clang in Windows for dynamic runtime in Debug. `#18422 <https://github.com/conan-io/conan/pull/18422>`_
- Fix: Test ``NMake`` integration with ``clang-cl``. `#18422 <https://github.com/conan-io/conan/pull/18422>`_
- Fix: Ensure old gcc version are detected up to minor version only. `#18419 <https://github.com/conan-io/conan/pull/18419>`_
- Fix: Fixing source retrieval when resetting local-index remote. `#18418 <https://github.com/conan-io/conan/pull/18418>`_
- Fix: Allow minors greater than 9 in `detect_api`. `#18410 <https://github.com/conan-io/conan/pull/18410>`_
- Fix: Removed ``Workspaces`` product definition and make ``conan workspace build`` work computing the right build-order. `#18390 <https://github.com/conan-io/conan/pull/18390>`_ . Docs `here <https://github.com/conan-io/docs/pull/4138>`__
- Fix: Forward `ConanInvalidConfiguration` when raised in hooks. `#18385 <https://github.com/conan-io/conan/pull/18385>`_
- Bugfix: Avoid crash when installing packages with tuple `generators` attribute and requirements to tool requires that provide `self.generator_info` generators. `#18503 <https://github.com/conan-io/conan/pull/18503>`_
- Bugfix: Fix detection of riscv64 cpu in Meson toolchain. `#18495 <https://github.com/conan-io/conan/pull/18495>`_
- Bugfix: Redirected Apple ARC flags to the ObjC/C++ ones. `#18485 <https://github.com/conan-io/conan/pull/18485>`_
- Bugfix: Fix `TestClient` mocked `HEAD` requests. `#18477 <https://github.com/conan-io/conan/pull/18477>`_
- Bugfix: Avoid leak of ``global.conf`` and ``-cc`` configuration for ``core.xxx`` items in Conan profiles, the ``core`` conf is exclusively for Conan internals, not for recipes neither for profiles. `#18474 <https://github.com/conan-io/conan/pull/18474>`_
- Bugfix: XcodeToolchain sets correct `..._DEPLOYMENT_TARGET` for all Apple OSs. `#18471 <https://github.com/conan-io/conan/pull/18471>`_ . Docs `here <https://github.com/conan-io/docs/pull/4126>`__
- Bugfix: :command:`conan export-pkg` now correctly passes a `str` as the conanfile version. `#18456 <https://github.com/conan-io/conan/pull/18456>`_
- Bugfix: Fix conan cache backup-upload ignoring `-cc` arguments. `#18447 <https://github.com/conan-io/conan/pull/18447>`_
- Bugfix: Fixed `CMakeConfigDeps` behavior with multiple `find_package` in folders and subfolders. `#18407 <https://github.com/conan-io/conan/pull/18407>`_
- Bugfix: Fixes issue where conanfile's `source()` method doesn't use `folders.root` when present. `#18377 <https://github.com/conan-io/conan/pull/18377>`_

2.17.1 (23-Jun-2025)
--------------------

- Bugfix: add support for ``Git()`` for git<2.36, for operations that check if a commit exists in a remote. `#18501 <https://github.com/conan-io/conan/pull/18501>`_

2.17.0 (28-May-2025)
--------------------

- Feature: Add support for gcc 13.4 `#18374 <https://github.com/conan-io/conan/pull/18374>`_ . Docs `here <https://github.com/conan-io/docs/pull/4108>`__
- Feature: Renamed 'editables' to 'packages'. `#18359 <https://github.com/conan-io/conan/pull/18359>`_ . Docs `here <https://github.com/conan-io/docs/pull/4106>`__
- Feature: Putting a folder named `conanws` as the top limit search if it exists. `#18343 <https://github.com/conan-io/conan/pull/18343>`_ . Docs `here <https://github.com/conan-io/docs/pull/4106>`__
- Feature: Removed the `home_folder` definition mechanism from the `conanws.[yml | py]` file. `#18339 <https://github.com/conan-io/conan/pull/18339>`_ . Docs `here <https://github.com/conan-io/docs/pull/4106>`__
- Feature: Packages/products do not need to be within the `workspace` folder. `#18334 <https://github.com/conan-io/conan/pull/18334>`_ . Docs `here <https://github.com/conan-io/docs/pull/4106>`__
- Feature: Add `tools.gnu:configure_args` conf to GnuToolchain and Autotoolchain generator to allow extra arguments to be added to the configure command. `#18333 <https://github.com/conan-io/conan/pull/18333>`_ . Docs `here <https://github.com/conan-io/docs/pull/4100>`__
- Feature: Add gcc 14.3 support. `#18322 <https://github.com/conan-io/conan/pull/18322>`_ . Docs `here <https://github.com/conan-io/docs/pull/4096>`__
- Feature: Auto detection of C standard. `#18290 <https://github.com/conan-io/conan/pull/18290>`_ . Docs `here <https://github.com/conan-io/docs/pull/4097>`__
- Feature: define CMAKE_C/CXX_COMPILER in ``CMakeToolchain`` generated presets, only for MSVC cl-like compilers, automatically only for Ninja generator. `#18280 <https://github.com/conan-io/conan/pull/18280>`_
- Feature: Add `header_lib` template to :command:`conan new`. `#18249 <https://github.com/conan-io/conan/pull/18249>`_ . Docs `here <https://github.com/conan-io/docs/pull/4094>`__
- Feature: `to_cppstd_flag`/`to_cstd_flag` methods are not using fixed values. `#18246 <https://github.com/conan-io/conan/pull/18246>`_
- Feature: Add ``subprocess`` to the profile jinja rendering. `#18244 <https://github.com/conan-io/conan/pull/18244>`_ . Docs `here <https://github.com/conan-io/docs/pull/4098>`__
- Feature: New ``conan cache save ... --no-source`` to avoid storing downloaded sources in the `.tgz`. `#18243 <https://github.com/conan-io/conan/pull/18243>`_ . Docs `here <https://github.com/conan-io/docs/pull/4099>`__
- Feature: Add verbose logs for `conan cache clean`. `#18228 <https://github.com/conan-io/conan/pull/18228>`_
- Feature: Add `--list` inputs to `conan cache clean` and `conan cache check-integrity`. `#18219 <https://github.com/conan-io/conan/pull/18219>`_ . Docs `here <https://github.com/conan-io/docs/pull/4095>`__
- Feature: Add `allowed_packages` info to remote json output. `#18206 <https://github.com/conan-io/conan/pull/18206>`_
- Feature: Add URL information to json output format for conan upload. `#18166 <https://github.com/conan-io/conan/pull/18166>`_ . Docs `here <https://github.com/conan-io/docs/pull/4088>`__
- Feature: New ``conan workspace clean`` command, removes the ``output-folder`` of editables if defined, otherwise nothing. Can be custom implemented by users in the ``conanws.py`` file. `#17763 <https://github.com/conan-io/conan/pull/17763>`_ . Docs `here <https://github.com/conan-io/docs/pull/4101>`__
- Fix: Fix PyInstaller `--exclude-module` adding wildcard for `conan.test`. `#18381 <https://github.com/conan-io/conan/pull/18381>`_
- Fix: Fix urls for conan audit. `#18360 <https://github.com/conan-io/conan/pull/18360>`_
- Fix: Validate if the licenses in the SBOM are SPDX compatible. `#18358 <https://github.com/conan-io/conan/pull/18358>`_
- Fix: Autotools in Windows working for both LLVM/Clang both clang and clang-cl frontends. `#18347 <https://github.com/conan-io/conan/pull/18347>`_ . Docs `here <https://github.com/conan-io/docs/pull/4109>`__
- Fix: Change wording on unzip tool when uncompressing file. `#18327 <https://github.com/conan-io/conan/pull/18327>`_
- Fix: Avoid duplicate component requirement names in `PkgConfigDeps` and `BazelDeps`. `#18324 <https://github.com/conan-io/conan/pull/18324>`_
- Fix: Avoid grafted commits in ``Git`` helper for ``commit_in_remote()`` affecting also ``coordinates_to_conandata()``, ``get_url_and_commit()``. `#18315 <https://github.com/conan-io/conan/pull/18315>`_
- Fix: `copy()` now is capable of excluding symlinks to folders. `#18304 <https://github.com/conan-io/conan/pull/18304>`_
- Fix: Better error message in `conan list --graph=file.json` when using filtered graph. `#18303 <https://github.com/conan-io/conan/pull/18303>`_
- Fix: Always sort overrides serialization. `#18274 <https://github.com/conan-io/conan/pull/18274>`_
- Fix: Allow composition of conf values that are different categories of numbers. `#18265 <https://github.com/conan-io/conan/pull/18265>`_
- Fix: Avoid incorrect warning in ``test_package`` of ``python_requires`` about "tested_reference_str". `#18226 <https://github.com/conan-io/conan/pull/18226>`_
- Fix: CycloneDX 1.6 authors field. `#18208 <https://github.com/conan-io/conan/pull/18208>`_
- Fix: Make ``CMakeConfigDeps`` incubating generator paths relative for ``deployers``. `#18197 <https://github.com/conan-io/conan/pull/18197>`_
- Fix: Add the full conan package in PyInstaller bundle. `#18195 <https://github.com/conan-io/conan/pull/18195>`_
- Bugfix: Remove ``LT_INIT`` from ``conan new autotools_exe`` template ``configure.ac``. `#18378 <https://github.com/conan-io/conan/pull/18378>`_
- Bugfix: Fix CMakeConfigDeps link flags. `#18367 <https://github.com/conan-io/conan/pull/18367>`_
- BugFix: Fix ``conan audit`` producing `_parse_error_threshold` crash when some package was not found in the catalog. `#18363 <https://github.com/conan-io/conan/pull/18363>`_
- Bugfix: The first edge on `conan graph info ... -f=html` now shows require information. `#18245 <https://github.com/conan-io/conan/pull/18245>`_
- Bugfix: ``conan cache save`` no longer zips downloaded artifacts like ``conan_export.tgz`` and ``conan_sources.tgz``. `#18243 <https://github.com/conan-io/conan/pull/18243>`_ . Docs `here <https://github.com/conan-io/docs/pull/4099>`__
- Bugfix: Allow to :command:`conan create` a ``python-requires`` package with a profile that contains tool-requires. `#18226 <https://github.com/conan-io/conan/pull/18226>`_
- Bugfix: Let `conan config install` walk the fs tree looking for a `.conanignore`. `#18170 <https://github.com/conan-io/conan/pull/18170>`_

2.16.1 (29-Apr-2025)
--------------------

- Feature: Add missing GCC 15 key to `settings.yml` `#18193 <https://github.com/conan-io/conan/pull/18193>`_ . Docs `here <https://github.com/conan-io/docs/pull/4084>`__

2.16.0 (29-Apr-2025)
--------------------

- Feature: Add support for GCC 15.1. `#18175 <https://github.com/conan-io/conan/pull/18175>`_ . Docs `here <https://github.com/conan-io/docs/pull/4081>`__
- Feature: Allow ``CMakeConfigDeps`` to support components with multilibs (with deprecation warning). `#18172 <https://github.com/conan-io/conan/pull/18172>`_
- Feature: add CMAKE_MODULE_PATH to CMakeConfigDeps for include(module). `#18162 <https://github.com/conan-io/conan/pull/18162>`_
- Feature: Add threshold for severity level in the conan audit scan command. `#18160 <https://github.com/conan-io/conan/pull/18160>`_ . Docs `here <https://github.com/conan-io/docs/pull/4080>`__
- Feature: `GnuToolchain` including the latest changes from `AutotoolsToolchain`. `#18159 <https://github.com/conan-io/conan/pull/18159>`_
- Feature: Add `CycloneDx 1.6` support. `#18108 <https://github.com/conan-io/conan/pull/18108>`_ . Docs `here <https://github.com/conan-io/docs/pull/4077>`__
- Feature: Introduce a new ``no_skip=True`` requirement trait for exceptional cases like one application depending on another application privately with ``requires`` to avoid it being skipped. `#18101 <https://github.com/conan-io/conan/pull/18101>`_ . Docs `here <https://github.com/conan-io/docs/pull/4078>`__
- Feature: Raise error early if ``conf_info`` is assigned with raw settings/options etc `#18083 <https://github.com/conan-io/conan/pull/18083>`_
- Feature: Moving functionality from ``Command`` layer to the ``ConanAPI`` for clearing old private imports ``from conans``. `#18079 <https://github.com/conan-io/conan/pull/18079>`_
- Feature: Document publicly the ``MSBuildDeps.platform`` attribute to allow customization for wix projects needing ``x86`` value. `#18078 <https://github.com/conan-io/conan/pull/18078>`_ . Docs `here <https://github.com/conan-io/docs/pull/4050>`__
- Feature: Add missing intel-cc releases `#18054 <https://github.com/conan-io/conan/pull/18054>`_ . Docs `here <https://github.com/conan-io/docs/pull/4076>`__
- Feature: Add information about the configuration each package is building for `#18019 <https://github.com/conan-io/conan/pull/18019>`_
- Feature: Add `-vv` information for the configuration of each dependency in the graph `#18019 <https://github.com/conan-io/conan/pull/18019>`_
- Fix: Some improvements in conan audit reports. `#18171 <https://github.com/conan-io/conan/pull/18171>`_
- Fix: Fix ordering by severity value in audit html output. `#18161 <https://github.com/conan-io/conan/pull/18161>`_
- Fix: Fix column overflow in audit html output. `#18161 <https://github.com/conan-io/conan/pull/18161>`_
- Fix: Make `audit_providers.json` read/writeable only by owner. `#18158 <https://github.com/conan-io/conan/pull/18158>`_
- Fix: Remove bogus SDK versions for some Apple OS's. `#18152 <https://github.com/conan-io/conan/pull/18152>`_ . Docs `here <https://github.com/conan-io/docs/pull/4076>`__
- Fix: Make the ``conan.cli`` command layer fully independent of legacy ``from conans`` imports that will break. `#18127 <https://github.com/conan-io/conan/pull/18127>`_
- Fix: Explicit ``git fetch commit`` in ``Git.checkout_from_conandata_coordinates()``, for cases like Azure DevOps creating commits that are not fetched by default in ``git clone``. `#18110 <https://github.com/conan-io/conan/pull/18110>`_
- Fix: Add ``ARM64EC`` platform in ``MSBuild``, it was missing. `#18100 <https://github.com/conan-io/conan/pull/18100>`_ . Docs `here <https://github.com/conan-io/docs/pull/4079>`__
- Fix: Allow ``conan graph build-order`` to output ``build_args`` for "editable" packages. `#18097 <https://github.com/conan-io/conan/pull/18097>`_
- Fix: Improve error message when private audit providers don't have curation. `#18094 <https://github.com/conan-io/conan/pull/18094>`_
- Fix: Making some ``Command`` formatter helpers private (only the ones in ``printers`` are common for reusage), and making some ConanAPI attributes private. `#18079 <https://github.com/conan-io/conan/pull/18079>`_
- Bugfix: Raise a not-found error if "local recipes index" ``user/channel`` doesn't match requested one. `#18153 <https://github.com/conan-io/conan/pull/18153>`_
- Bugfix: Fixed bug using `MesonToolchain` and `visionOS`. `#18151 <https://github.com/conan-io/conan/pull/18151>`_
- Bugfix: Add IMPORTED_CONFIGURATIONS to INTERFACE libraries to in ``CMakeConfigDeps`` `#18088 <https://github.com/conan-io/conan/pull/18088>`_
- Bugfix: Apply Apple ``bitcode``, ``visibility`` and ``arc`` confs to ``Autootools/Gnu/Meson Toolchains`` `#18085 <https://github.com/conan-io/conan/pull/18085>`_


2.15.1 (14-Apr-2025)
--------------------

- Feature: Update Apple products supported versions. `#18122 <https://github.com/conan-io/conan/pull/18122>`_ . Docs `here <https://github.com/conan-io/docs/pull/4063>`__


2.15.0 (31-Mar-2025)
--------------------

- Feature: Improve error messages when dealing with incorrect JSON input file formats. `#18037 <https://github.com/conan-io/conan/pull/18037>`_
- Feature: Added new `--graph-context` to `conan list` command. `#18015 <https://github.com/conan-io/conan/pull/18015>`_ . Docs `here <https://github.com/conan-io/docs/pull/4042>`__
- Feature: Add version-ranges patterns defined with ``[1.2.3.4.*]`` with the ``*`` at the end of the string. `#18012 <https://github.com/conan-io/conan/pull/18012>`_ . Docs `here <https://github.com/conan-io/docs/pull/4040>`__
- Feature: Added `subsystem` field in MesonToolchain if cross-compiling between Apple OSs. `#17985 <https://github.com/conan-io/conan/pull/17985>`_
- Feature: Added new kwarg `build_context`to `is_apple_os` helper function. `#17985 <https://github.com/conan-io/conan/pull/17985>`_
- Feature: Integrate chmod feature in `tools.files`. `#17800 <https://github.com/conan-io/conan/pull/17800>`_ . Docs `here <https://github.com/conan-io/docs/pull/4038>`__
- Fix: Remove backup sources from unknown refs when calling `conan cache clean`. `#18018 <https://github.com/conan-io/conan/pull/18018>`_
- Fix: Fix SBOM author field. `#18014 <https://github.com/conan-io/conan/pull/18014>`_
- Fix: Avoid resolving the symlinks path by default if they match the library name. `#17964 <https://github.com/conan-io/conan/pull/17964>`_
- Fix: Make some ``from conan.internal`` and ``from conans`` usages from ``CLI`` commands private, moving to ConanAPI. `#17961 <https://github.com/conan-io/conan/pull/17961>`_
- Fix: Add warning for ``deprecated`` attribute in recipes. `#17957 <https://github.com/conan-io/conan/pull/17957>`_ . Docs `here <https://github.com/conan-io/docs/pull/4041>`__
- Fix: Improve relative paths in generators to be as short as possible. `#17945 <https://github.com/conan-io/conan/pull/17945>`_
- Fix: `_Component()` has no `package_type` property. `#17943 <https://github.com/conan-io/conan/pull/17943>`_
- Bugfix: Fix ``global.conf`` precedence over profiles ``[conf]`` and order change of per-package pattern confs. `#18028 <https://github.com/conan-io/conan/pull/18028>`_
- Bugfix: Solve issue with ``update_policy=legacy`` and using lockfiles. `#18009 <https://github.com/conan-io/conan/pull/18009>`_
- Bugfix: `untargz()` method was failing if directories had a more restrictive mode. `#17998 <https://github.com/conan-io/conan/pull/17998>`_
- Bugfix: `CppInfo.auto_deduce_location` method gives more prio to exact match. `#17975 <https://github.com/conan-io/conan/pull/17975>`_
- Bugfix: Avoid crash of ``--format=json`` serialization when custom generators inside tool-requires are referenced by class, not by name. `#17954 <https://github.com/conan-io/conan/pull/17954>`_
- BugFix: Add correct info in metadata + prevent crash when no component is associated to root_node. `#17925 <https://github.com/conan-io/conan/pull/17925>`_

2.14.0 (12-Mar-2025)
--------------------

- Feature: Add :command:`conan audit` command for scanning Conan packages for CVE's `#17951 <https://github.com/conan-io/conan/pull/17951>`_ . Docs `here <https://github.com/conan-io/docs/pull/4026>`__
- Feature: Add clang 20 support. `#17920 <https://github.com/conan-io/conan/pull/17920>`_ . Docs `here <https://github.com/conan-io/docs/pull/4011>`__
- Feature: Allow partial ``workspace install <path1> ... <pathN>`` installation of workspace. `#17887 <https://github.com/conan-io/conan/pull/17887>`_ . Docs `here <https://github.com/conan-io/docs/pull/4016>`__
- Feature: Add hooks for validate method: `pre_validate` and `post_validate`. `#17856 <https://github.com/conan-io/conan/pull/17856>`_ . Docs `here <https://github.com/conan-io/docs/pull/4013>`__
- Feature: Added complete Apple Frameworks management to `CMakeConfigDeps`. `#17725 <https://github.com/conan-io/conan/pull/17725>`_ . Docs `here <https://github.com/conan-io/docs/pull/4017>`__
- Feature: Added new `cpp_info.package_framework` to `cpp_info`. `#17725 <https://github.com/conan-io/conan/pull/17725>`_ . Docs `here <https://github.com/conan-io/docs/pull/4017>`__
- Feature: Fix several bugs in docker runner, added new configuration options and improved logging system `#17542 <https://github.com/conan-io/conan/pull/17542>`_ . Docs `here <https://github.com/conan-io/docs/pull/3977>`__
- Fix: Improve error message when ``jinja2`` profile rendering fails due to unexpected syntax. `#17940 <https://github.com/conan-io/conan/pull/17940>`_
- Fix: Do not warn in auto-deduce location for exact library matches. `#17923 <https://github.com/conan-io/conan/pull/17923>`_
- Fix: the ``cmake_set_interface_link_directories`` property is not really necessary at all in ``CMakeDeps`` and it becomes invalid in ``CMakeConfigDeps`` as it will require full ``package_info()`` definition. `#17917 <https://github.com/conan-io/conan/pull/17917>`_ . Docs `here <https://github.com/conan-io/docs/pull/4015>`__
- Fix: Do not convert ``\\`` to ``/`` in ``MSBuildDeps`` generator as some MSBuild functionality needs Windows ``\\`` paths. `#17901 <https://github.com/conan-io/conan/pull/17901>`_
- Fix: Avoid workspace incorrectly defining a "local-recipes-index" auxiliary cache. `#17883 <https://github.com/conan-io/conan/pull/17883>`_
- Fix: Improve the output of the profile dumping for environment, with correct prepend order. `#17863 <https://github.com/conan-io/conan/pull/17863>`_
- Fix: Fixes VCVars vcvarsall.bat generation if OS is set to WindowsStore. `#17849 <https://github.com/conan-io/conan/pull/17849>`_
- Bugfix: Avoid self-requirement and loop when a ``[tool_requires]`` in the build profile depends on itself with a version range. `#17931 <https://github.com/conan-io/conan/pull/17931>`_
- Bugfix: Fix ``conan graph build-order --reduce --order-by=recipe`` that was not filtering all packages != "Build". `#17909 <https://github.com/conan-io/conan/pull/17909>`_
- Bugfix: Solve conflict not raised when version-ranges have different user. `#17877 <https://github.com/conan-io/conan/pull/17877>`_

2.13.0 (26-Feb-2025)
--------------------

- Feature: ``CMakeDeps`` generated ``Findxxxx.cmake`` files now can define ``{prefix}_FOUND`` and ``{prefix}_VERSION`` for the ``cmake_additional_variables_prefixes``. `#17838 <https://github.com/conan-io/conan/pull/17838>`_
- Feature: Make available in conanfiles the new incubating ``CMakeConfigDeps`` generator, still under the incubating "conf" feature flag. `#17831 <https://github.com/conan-io/conan/pull/17831>`_ . Docs `here <https://github.com/conan-io/docs/pull/3999>`__
- Feature: Add a warning if a specific revision different than the current one is requested to a ``local-recipes-index`` remote. `#17819 <https://github.com/conan-io/conan/pull/17819>`_
- Feature: Forward repository parameter (with same default) from `coordinates_to_conandata()` to `get_url_and_commit()`. `#17722 <https://github.com/conan-io/conan/pull/17722>`_
- Feature: Add ``mcf`` threading for ``gcc`` MinGW compiler `settings.yml`. `#17704 <https://github.com/conan-io/conan/pull/17704>`_
- Feature: Improve ``conanws.py`` file definition following same patterns as ``ConanFile``. `#17688 <https://github.com/conan-io/conan/pull/17688>`_ . Docs `here <https://github.com/conan-io/docs/pull/3998>`__
- Feature: Workspace new ``workspace install`` command for monolithic super-projects containing multiple ``editables``. `#17675 <https://github.com/conan-io/conan/pull/17675>`_ . Docs `here <https://github.com/conan-io/docs/pull/3998>`__
- Feature: New ``conan new workspace`` template contains CMake-based monolithic super-project that works with ``conan workspace install``. `#17675 <https://github.com/conan-io/conan/pull/17675>`_ . Docs `here <https://github.com/conan-io/docs/pull/3998>`__
- Feature: Added `CMAKE_LIBRARY_PATH` to `conan_cmakedeps_paths.cmake` (new CMakeDeps). `#17668 <https://github.com/conan-io/conan/pull/17668>`_
- Feature: Added `CMAKE_INCLUDE_PATH` to `conan_cmakedeps_paths.cmake` (new CMakeDeps). `#17668 <https://github.com/conan-io/conan/pull/17668>`_
- Feature: Add `extension_properties` access to conanfile dependencies. `#17659 <https://github.com/conan-io/conan/pull/17659>`_ . Docs `here <https://github.com/conan-io/docs/pull/3997>`__
- Feature: Introducing `in_range` method in Version which allows comparing against version ranges. `#17658 <https://github.com/conan-io/conan/pull/17658>`_ . Docs `here <https://github.com/conan-io/docs/pull/3996>`__
- Feature: Upgrade dependency ``urllib3`` to ``2.0``. `#17655 <https://github.com/conan-io/conan/pull/17655>`_
- Feature: New `lock upgrade` command to automatically upgrade desired dependencies resolving the graph. `#17577 <https://github.com/conan-io/conan/pull/17577>`_ . Docs `here <https://github.com/conan-io/docs/pull/4001>`__
- Feature: Enhanced ``Premake`` CLI wrapper with configurable Lua file path, and support for custom command-line arguments. `#17398 <https://github.com/conan-io/conan/pull/17398>`_ . Docs `here <https://github.com/conan-io/docs/pull/4000>`__
- Fix: Docstring for ``conan remote auth`` regarding CONAN_LOGIN env-var. `#17834 <https://github.com/conan-io/conan/pull/17834>`_
- Fix: runtime_deploy preserves symbolic links along with their libraries. `#17824 <https://github.com/conan-io/conan/pull/17824>`_ . Docs `here <https://github.com/conan-io/docs/pull/3992>`__
- Fix: Better message for incubating CMakeDeps about ``target_link_libraries()`` from tool-requires. `#17821 <https://github.com/conan-io/conan/pull/17821>`_
- Fix: Fix the `_calculate_licenses` SBOM method bug and add a small test. `#17801 <https://github.com/conan-io/conan/pull/17801>`_
- Fix: Allow build context information from ``conf`` in ``AutotoolsToolchain``. `#17794 <https://github.com/conan-io/conan/pull/17794>`_
- Fix: Allow msys2 subsystem path inheriting from environment variables `#17781 <https://github.com/conan-io/conan/pull/17781>`_
- Fix: Improve error messages for components definition errors and for runtime conflicts. `#17771 <https://github.com/conan-io/conan/pull/17771>`_
- Fix: Update the message for client migration. `#17751 <https://github.com/conan-io/conan/pull/17751>`_
- Fix: Improve untar performance. `#17708 <https://github.com/conan-io/conan/pull/17708>`_
- Fix: Protect erroneous assignment of ``cpp_info/components.required_components = xxx``, for ``required_components`` property. Now it will raise a proper error. `#17692 <https://github.com/conan-io/conan/pull/17692>`_
- Fix: New ``CMakeDeps`` transitive linking of shared libs. `#17459 <https://github.com/conan-io/conan/pull/17459>`_
- Bugfix: Fix self-contained ``pyinstaller`` executable to also include the new ``conan.tools.sbom`` tools. `#17809 <https://github.com/conan-io/conan/pull/17809>`_

2.12.2 (12-Feb-2025)
--------------------

- Fix: Fix default name and let cycloneDX define a custom name. `#17760 <https://github.com/conan-io/conan/pull/17760>`_ . Docs `here <https://github.com/conan-io/docs/pull/3983>`__
- Fix: Add cycloneDX `add_tests` and `add_build` parameters. `#17760 <https://github.com/conan-io/conan/pull/17760>`_ . Docs `here <https://github.com/conan-io/docs/pull/3983>`__
- Bugfix: Fix cycloneDX tool parameters. `#17760 <https://github.com/conan-io/conan/pull/17760>`_ . Docs `here <https://github.com/conan-io/docs/pull/3983>`__

2.12.1 (28-Jan-2025)
--------------------

- Bugfix: Fix `conan config clean` not regenerating every necessary file. `#17649 <https://github.com/conan-io/conan/pull/17649>`_
- Bugfix: Avoid ``compatibility.py`` migration if any of the files are modified by users. `#17647 <https://github.com/conan-io/conan/pull/17647>`_

2.12.0 (27-Jan-2025)
--------------------

- Feature: Make public documented (and experimental) the ``--build=compatible:[pattern]`` build mode, to allow building other configurations different than the current one when the current one is invalid and binary compatibility defines compatible binaries. `#17637 <https://github.com/conan-io/conan/pull/17637>`_ . Docs `here <https://github.com/conan-io/docs/pull/3963>`__
- Feature: Define new ``tools.cmake.cmaketoolchain:user_presets`` to customize the name of the generated ``CMakeUserPresets.json``, disabling its generation. Also can generate it in a subfolder. `#17613 <https://github.com/conan-io/conan/pull/17613>`_ . Docs `here <https://github.com/conan-io/docs/pull/3967>`__
- Feature: Serialize in ``--format=json`` graph output the original requirements version range, not only the resolved one. `#17603 <https://github.com/conan-io/conan/pull/17603>`_
- Feature: Add cycloneDX as a Conan tool and implement subgraph for conanfile. `#17559 <https://github.com/conan-io/conan/pull/17559>`_ . Docs `here <https://github.com/conan-io/docs/pull/3959>`__
- Feature: Initial ``conan workspace build`` command to build the full workspace, based on the definition of ``products``. `#17538 <https://github.com/conan-io/conan/pull/17538>`_ . Docs `here <https://github.com/conan-io/docs/pull/3964>`__
- Feature: Allow applying patches on "create" time for conan-center-index like layouts from an external centralized folder. `#17520 <https://github.com/conan-io/conan/pull/17520>`_ . Docs `here <https://github.com/conan-io/docs/pull/3965>`__
- Feature: Add report progress while unpacking tarball files. `#17519 <https://github.com/conan-io/conan/pull/17519>`_
- Feature: `conan profile show` can now select which context's profile to show. `#17518 <https://github.com/conan-io/conan/pull/17518>`_
- Feature: Better logging, printing the username for repositories, successful auth event and trace-level messages including full URL requests. `#17517 <https://github.com/conan-io/conan/pull/17517>`_
- Feature: Adds `conan config clean` command that will remove all custom config from conan home, excluding the generated packages. `#17514 <https://github.com/conan-io/conan/pull/17514>`_ . Docs `here <https://github.com/conan-io/docs/pull/3961>`__
- Feature: Add `reinit` method to `ConanApi`, which reinitializes every `subapi`. `#17514 <https://github.com/conan-io/conan/pull/17514>`_ . Docs `here <https://github.com/conan-io/docs/pull/3961>`__
- Feature: Allow defining ``--out-file=file.ext`` instead of ``--format=ext > file.ext`` to write to files directly and avoid issues with redirects. `#17507 <https://github.com/conan-io/conan/pull/17507>`_ . Docs `here <https://github.com/conan-io/docs/pull/3966>`__
- Feature: Cache HTTP request sessions between API calls. `#17455 <https://github.com/conan-io/conan/pull/17455>`_
- Feature: Implement caching in the ``Remote`` objects for ``RemoteManager`` calls, saving repeated calls to the server for the duration of the life of the Remote objects. `#17449 <https://github.com/conan-io/conan/pull/17449>`_ . Docs `here <https://github.com/conan-io/docs/pull/3962>`__
- Fix: Added `arch_flag` as a public attribute to the `MesonToolchain` generator. `#17629 <https://github.com/conan-io/conan/pull/17629>`_
- Fix: Increase sqlite timeout from 10 to 20 seconds for very heavily loaded CI servers. `#17616 <https://github.com/conan-io/conan/pull/17616>`_
- Fix: Make ``remotes.json`` saving transactional to avoid corruption for hard killed processes. `#17588 <https://github.com/conan-io/conan/pull/17588>`_
- Fix: Improve error message for :command:`conan create` when ``test_package`` has missing binaries. `#17581 <https://github.com/conan-io/conan/pull/17581>`_
- Fix: Fix `Git` `is_dirty` detection of excluded files with paths. `#17571 <https://github.com/conan-io/conan/pull/17571>`_
- Fix: Allow latest bottle 0.13 release for ``conan_server`` to work with Python 3.13. `#17534 <https://github.com/conan-io/conan/pull/17534>`_
- Fix: GnuToolchain's make_args handle empty values correctly. `#17532 <https://github.com/conan-io/conan/pull/17532>`_
- Fix: Fix inconsistency in ``replace_in_file``, that returned `False` if the pattern was not found (with strict off), otherwise `None`. `#17531 <https://github.com/conan-io/conan/pull/17531>`_
- Fix: `conan profile show` does not pollute stdout with information titles. `#17518 <https://github.com/conan-io/conan/pull/17518>`_
- Fix: Error out when unknown language is used in languages attribute. `#17512 <https://github.com/conan-io/conan/pull/17512>`_
- Fix: Fix ``Workspace`` when using the ``workspace_api.load()`` and using ``self.run()`` inside ``set_version()``. `#17501 <https://github.com/conan-io/conan/pull/17501>`_
- Bugfix: `conf_build` does not exist for `cli` and `conanfile.txt` contexts. `#17640 <https://github.com/conan-io/conan/pull/17640>`_
- Bugfix: Make possible to use `pattern` and `strip_root` at the same time for `conan.tools.files.unzip()`. `#17591 <https://github.com/conan-io/conan/pull/17591>`_
- Bugfix: Solve incubating ``CMakeDeps`` issues with transitive ``[replace_requires]``. `#17566 <https://github.com/conan-io/conan/pull/17566>`_
- Bugfix: Solve ``PkgConfigDeps`` issues with transitive ``[replace_requires]``. `#17566 <https://github.com/conan-io/conan/pull/17566>`_

2.11.0 (18-Dec-2024)
--------------------

- Feature: Only warn on frozen conan v1 remote if enabled. `#17482 <https://github.com/conan-io/conan/pull/17482>`_
- Feature: `AutotoolsToolchain` uses user's variables when Android cross-compilation at first. `#17470 <https://github.com/conan-io/conan/pull/17470>`_ . Docs `here <https://github.com/conan-io/docs/pull/3951>`__
- Feature: `AutotoolsToolchain` checks if Android cross-compilation paths exist. `#17470 <https://github.com/conan-io/conan/pull/17470>`_ . Docs `here <https://github.com/conan-io/docs/pull/3951>`__
- Feature: Adding the Conan cache "profiles" folder to the jinja2 search path, so profiles can be included/imported from jinja syntax even for parent and sibling folders. `#17432 <https://github.com/conan-io/conan/pull/17432>`_ . Docs `here <https://github.com/conan-io/docs/pull/3950>`__
- Feature: Updated `tools.env.virtualenv:powershell` conf to allow specifying the PowerShell executable (e.g., powershell.exe or pwsh) and passing additional arguments. `#17416 <https://github.com/conan-io/conan/pull/17416>`_ . Docs `here <https://github.com/conan-io/docs/pull/3947>`__
- Feature: Deprecate use of `tools.env.virtualenv:powershell=True/False`. `#17416 <https://github.com/conan-io/conan/pull/17416>`_ . Docs `here <https://github.com/conan-io/docs/pull/3947>`__
- Fix: Do not show powershell deprecation message if value is None. `#17500 <https://github.com/conan-io/conan/pull/17500>`_
- Fix: Fix ``LocalAPI`` definition of editables when calling ``editable_add``. `#17498 <https://github.com/conan-io/conan/pull/17498>`_
- Fix: Clarify debug message in CMakeDeps. `#17453 <https://github.com/conan-io/conan/pull/17453>`_
- Fix: Added explicitly `allow_empty = True` to `glob()` function in BazelDeps (bazel 8.x compatible). `#17444 <https://github.com/conan-io/conan/pull/17444>`_
- Fix: Fix broken `cpp_info.location` deduction due to unsanitized regex. `#17430 <https://github.com/conan-io/conan/pull/17430>`_
- Fix: Trusting the real path coming from a symlink is a good one. `#17421 <https://github.com/conan-io/conan/pull/17421>`_
- Fix: Fix user/channel when searching patterns in a local-recipes-index. `#17408 <https://github.com/conan-io/conan/pull/17408>`_
- Fix: Add warning for empty version ranges. `#17405 <https://github.com/conan-io/conan/pull/17405>`_
- Bugfix: Fix bogus duplication of component properties `#17503 <https://github.com/conan-io/conan/pull/17503>`_
- Bugfix: Fix running commands in powershell with single quotes. `#17487 <https://github.com/conan-io/conan/pull/17487>`_
- Bugfix: Fix issues with unsetting some types of confs. `#17445 <https://github.com/conan-io/conan/pull/17445>`_

2.10.3 (18-Dec-2024)
--------------------

- Bugfix: Integrate Conan 2.9.3 missing fix https://github.com/conan-io/conan/pull/17338 `#17496 <https://github.com/conan-io/conan/pull/17496>`_

2.10.2 (10-Dec-2024)
--------------------

- Fix: Solve performance issue in large graphs computing the "skip" binaries. `#17436 <https://github.com/conan-io/conan/pull/17436>`_

2.10.1 (04-Dec-2024)
--------------------

- Bugfix: Fix `[replace_requires]` for replacements of same reference name. `#17409 <https://github.com/conan-io/conan/pull/17409>`_

2.10.0 (02-Dec-2024)
--------------------

- Feature: Add `--force` option to `conan remote auth` to force authentication even for remotes that have anonymous access enabled. `#17377 <https://github.com/conan-io/conan/pull/17377>`_ . Docs `here <https://github.com/conan-io/docs/pull/3924>`__
- Feature: Add `--output` option to :command:`conan new` command. `#17359 <https://github.com/conan-io/conan/pull/17359>`_
- Feature: Let the new ``CMakeDeps`` always define components and check them with ``find_package( COMPONENTS)``, listening to new property ``cmake_components``. `#17302 <https://github.com/conan-io/conan/pull/17302>`_
- Feature: Allow ``tools.microsoft.msbuild:max_cpu_count=0`` to use ``/m`` to use all available cores. `#17301 <https://github.com/conan-io/conan/pull/17301>`_ . Docs `here <https://github.com/conan-io/docs/pull/3926>`__
- Feature: define ``*`` as default argument if no args specified for ``conan list``. `#17300 <https://github.com/conan-io/conan/pull/17300>`_ . Docs `here <https://github.com/conan-io/docs/pull/3927>`__
- Feature: Improved auto deduce location function. `#17296 <https://github.com/conan-io/conan/pull/17296>`_
- Feature: BazelDeps using the new `deduce_location` mechanism to find the libraries. `#17296 <https://github.com/conan-io/conan/pull/17296>`_
- Feature: Initial ``conan workspace`` initial proposal to manage local set of editables. Introduced only as a dev/maintainers feature, behind an environment variable. `#17272 <https://github.com/conan-io/conan/pull/17272>`_ . Docs `here <https://github.com/conan-io/docs/pull/3930>`__
- Feature: Allow ``--settings`` in ``conan config install-pkg`` to create and install different configurations in different platforms. `#17217 <https://github.com/conan-io/conan/pull/17217>`_ . Docs `here <https://github.com/conan-io/docs/pull/3929>`__
- Feature: Add network to configfile for Docker runners. `#17069 <https://github.com/conan-io/conan/pull/17069>`_ . Docs `here <https://github.com/conan-io/docs/pull/3932>`__
- Fix: Fix help message for PowerShell conf. `#17389 <https://github.com/conan-io/conan/pull/17389>`_ . Docs `here <https://github.com/conan-io/docs/pull/3923>`__
- Fix: Fixed an error that occurred when using `conan.tools.scm.Git.fetch_commit()` in a subfolder. `#17369 <https://github.com/conan-io/conan/pull/17369>`_
- Fix: Adding a "risk" warning for options conflicts, so users can do warn-as-error to raise when they happen. `#17366 <https://github.com/conan-io/conan/pull/17366>`_
- Fix: New ``CMakeDeps`` generator allow ``fooConfig.cmake`` for in-package files besides ``foo-config.cmake``. `#17330 <https://github.com/conan-io/conan/pull/17330>`_
- Fix: Add a warning for editable dependencies when building in the cache. `#17325 <https://github.com/conan-io/conan/pull/17325>`_
- Fix: Raise ConanException if source patch does not exist in `export_conandata_patches`. `#17294 <https://github.com/conan-io/conan/pull/17294>`_
- Fix: Improve the UX for `CONAN_LOG_LEVEL` env-var incorrect values. `#17280 <https://github.com/conan-io/conan/pull/17280>`_
- Fix: Meson aligns with other build systems considering `x86_64`->`x86` as cross building. `#17266 <https://github.com/conan-io/conan/pull/17266>`_
- Fix: Avoid ``colorama`` bug crashing for large outputs. `#17259 <https://github.com/conan-io/conan/pull/17259>`_
- Fix: Fix arch for docker runner tests. `#17069 <https://github.com/conan-io/conan/pull/17069>`_ . Docs `here <https://github.com/conan-io/docs/pull/3932>`__
- Bugfix: Add correct flags when ``compiler=clang`` and ``compiler_executables={"c": "clang-cl"}`` to not inject incorrect flags when cross-building from Linux to Windows. `#17387 <https://github.com/conan-io/conan/pull/17387>`_
- Bugfix: Solve ``Choco().check()`` bug using legacy ``choco search --local-only``, replaced by ``choco list``. `#17382 <https://github.com/conan-io/conan/pull/17382>`_
- Bugfix: Fix adding `tools.android:ndk_path` with spaces in path. `#17379 <https://github.com/conan-io/conan/pull/17379>`_
- BugFix: Fix ``Premake`` integration. `#17350 <https://github.com/conan-io/conan/pull/17350>`_ . Docs `here <https://github.com/conan-io/docs/pull/3925>`__
- Bugfix: Solve problem with misdetection of consumer packages for the ``&`` pattern. `#17346 <https://github.com/conan-io/conan/pull/17346>`_
- Bugfix: Fix `conan graph info ... -f=html` in Safari. `#17335 <https://github.com/conan-io/conan/pull/17335>`_
- Bugfix: Allow multiple ``[replace_requires]`` by the same dependency. `#17326 <https://github.com/conan-io/conan/pull/17326>`_
- Bugfix: BazelDeps failed to find OpenSSL shared libraries. `#17296 <https://github.com/conan-io/conan/pull/17296>`_
- Bugfix: Solve bug in ``CMake`` not using the correct value from ``tools.microsoft.msbuild:max_cpu_count``. `#17292 <https://github.com/conan-io/conan/pull/17292>`_
- Bugfix: Fix ``cpp_info`` properties overwriting instead of merging for properties with list values. Necessary for ``cmake_build_modules`` to work in ``editable`` mode. `#17214 <https://github.com/conan-io/conan/pull/17214>`_

2.9.3 (21-Nov-2024)
-------------------

- Bugfix: Fixing ``is_test`` computation affecting to components checks. `#17338 <https://github.com/conan-io/conan/pull/17338>`_

2.9.2 (07-Nov-2024)
-------------------

- Feature: Use center2.conan.io as new default remote and warn about having the old one. `#17284 <https://github.com/conan-io/conan/pull/17284>`_ . Docs `here <https://github.com/conan-io/docs/pull/3893>`__
- Bugfix: Fix ROSEnv quotes for CMAKE_TOOLCHAIN_FILE variable. `#17270 <https://github.com/conan-io/conan/pull/17270>`_

2.9.1 (30-Oct-2024)
-------------------

- Bugfix: Fix `deduce_subsystem` when `scope=None` assuming the scope is `build`. `#17251 <https://github.com/conan-io/conan/pull/17251>`_
- Bugfix: Fixed false positives of ``profile.py`` plugin checks over c++26 for latest compiler versions `#17250 <https://github.com/conan-io/conan/pull/17250>`_

2.9.0 (29-Oct-2024)
-------------------

- Feature: Add missing major OS/compiler version support in `settings.yml`. `#17240 <https://github.com/conan-io/conan/pull/17240>`_ . Docs `here <https://github.com/conan-io/docs/pull/3889>`__
- Feature: :command:`conan new` learned defaults ``-d name=mypkg -d version=0.1`` for simpler UX. `#17186 <https://github.com/conan-io/conan/pull/17186>`_ . Docs `here <https://github.com/conan-io/docs/pull/3882>`__
- Feature: Warn when patching files and the recipe has `no_copy_source = True`, which could lead to unforseen issues `#17162 <https://github.com/conan-io/conan/pull/17162>`_
- Feature: Add `self.generator_info` for `tool_requires` to propagate generators to their direct dependencies. `#17129 <https://github.com/conan-io/conan/pull/17129>`_ . Docs `here <https://github.com/conan-io/docs/pull/3880>`__
- Feature: Add support for including paths that are ignored in `.conanignore`. `#17123 <https://github.com/conan-io/conan/pull/17123>`_ . Docs `here <https://github.com/conan-io/docs/pull/3879>`__
- Feature: New ``tools.graph:skip_build`` conf to be able to skip the expansion of ``tool_requires``. `#17117 <https://github.com/conan-io/conan/pull/17117>`_ . Docs `here <https://github.com/conan-io/docs/pull/3883>`__
- Feature: New ``tools.graph:skip_test`` conf to be able to skip the expansion of ``test_requires``. `#17117 <https://github.com/conan-io/conan/pull/17117>`_ . Docs `here <https://github.com/conan-io/docs/pull/3883>`__
- Feature: Add ROSEnv generator integration for ROS2 (Robot Operating System). `#17110 <https://github.com/conan-io/conan/pull/17110>`_
- Feature: Add profile arguments information to ``conan graph build-order`` to improve UX and usage in CI systems. `#17102 <https://github.com/conan-io/conan/pull/17102>`_ . Docs `here <https://github.com/conan-io/docs/pull/3884>`__
- Feature: Add C++26 support for `gcc`, `clang`, and `apple-clang`. `#17092 <https://github.com/conan-io/conan/pull/17092>`_ . Docs `here <https://github.com/conan-io/docs/pull/3878>`__
- Feature: Add Configuration and Platform keys for MSBuildDeps property sheets. `#17076 <https://github.com/conan-io/conan/pull/17076>`_ . Docs `here <https://github.com/conan-io/docs/pull/3888>`__
- Feature: New ``CMakeDeps`` generator activated by ``tools.cmake.cmakedeps:new`` conf with value ``will_break_next`` for evaluation. This new generator deduces or use ``cpp_info.location/link_location`` to define STATIC; SHARED, INTERFACE imported targets. It will also define the IMPORTED_LOCATION, the IMPORTED_CONFIGURATION, etc. `#16964 <https://github.com/conan-io/conan/pull/16964>`_
- Feature: Use ``cpp_info.languages``, that default to the recipe ``languages`` to propagate "link-language" requirements to consumers of the packages. `#16964 <https://github.com/conan-io/conan/pull/16964>`_
- Feature: Define ``cpp_info.default_components`` for the new ``CMakeDeps`` generator only. `#16964 <https://github.com/conan-io/conan/pull/16964>`_
- Feature: Model ``cpp_info.exes`` field for executable applications, used only by the new ``CMakeDeps`` generator, that generate IMPORTED executable targets in ``CMakeDeps`` for ``cpp_info.exes``. `#16964 <https://github.com/conan-io/conan/pull/16964>`_
- Fix: Use a valid prefix path for `meson.configure()` on Windows, to avoid failures in Python 3.13. `#17206 <https://github.com/conan-io/conan/pull/17206>`_
- Fix: Allow `cmake_target_aliases` to be set in CMakeDeps. `#17200 <https://github.com/conan-io/conan/pull/17200>`_ . Docs `here <https://github.com/conan-io/docs/pull/3875>`__
- Fix: Adding the startup options to each Bazel command. `#17183 <https://github.com/conan-io/conan/pull/17183>`_
- Fix: Add remote name to login prompt. `#17178 <https://github.com/conan-io/conan/pull/17178>`_
- Fix: Get credentials and re-authenticate when an expired token gives AuthenticationException. `#17127 <https://github.com/conan-io/conan/pull/17127>`_
- Fix: Moved exceptions from the legacy ``from conans.error`` to documented ``from conan.error``. `#17126 <https://github.com/conan-io/conan/pull/17126>`_ . Docs `here <https://github.com/conan-io/docs/pull/3864>`__
- Fix: ``Pacman`` as package manager shouldn't be used for ``tools.microsoft.bash:subsystem=msys2``, but when the target platform is actually msys2 ``os.subsystem=msys2`` (as a setting). `#17103 <https://github.com/conan-io/conan/pull/17103>`_
- Fix: Properly deduce RuntimeLibrary from profile in MSBuildToolchain. `#17100 <https://github.com/conan-io/conan/pull/17100>`_
- Fix: Set C++20 flag to `{gnu}c++20` for `gcc` >= 10 instead of `c++2a` until `gcc` 12. `#17092 <https://github.com/conan-io/conan/pull/17092>`_ . Docs `here <https://github.com/conan-io/docs/pull/3878>`__
- Fix: Set C++23 flag to `{gnu}c++23` for `gcc` >= 11 instead of `c++2b`. `#17092 <https://github.com/conan-io/conan/pull/17092>`_ . Docs `here <https://github.com/conan-io/docs/pull/3878>`__
- Fix: Avoid repeated login attempts to the server for 401 when the credentials come from env-vars or ``credentials.json`` file, only repeated login attempts for user interactive prompt. `#17083 <https://github.com/conan-io/conan/pull/17083>`_
- Fix: Align CMakeToolchain and AutotoolsToolchain to automatically define ``cl`` compiler for ``compiler=msvc`` if not defined (only when necessary, as when using Ninja generator in CMake). `#16875 <https://github.com/conan-io/conan/pull/16875>`_ . Docs `here <https://github.com/conan-io/docs/pull/3886>`__
- Fix: Quote `build_args` in `conan graph build-order -f=json` to avoid issues with options with spaces. `#16594 <https://github.com/conan-io/conan/pull/16594>`_
- Bugfix: Improved `bazeldeps._get_libs()` mechanism. `#17233 <https://github.com/conan-io/conan/pull/17233>`_
- Bugfix: Improve cstd check for different compiler versions at profile load time. `#17157 <https://github.com/conan-io/conan/pull/17157>`_
- Bugfix: Fix cppstd/cstd `variable_watch` when they are not defined. `#17156 <https://github.com/conan-io/conan/pull/17156>`_
- Bugfix: Fix cstd error reporting when a recipe does not support the required version. `#17156 <https://github.com/conan-io/conan/pull/17156>`_
- Bugfix: Drop the username permission validation bypass in ``conan_server``, it could be a potential security issue. `#17132 <https://github.com/conan-io/conan/pull/17132>`_
- Bugfix: Listing recipes with equal versions under semver rules but different representation (ie `1.0` & `1.0.0`) now returns both references. `#17121 <https://github.com/conan-io/conan/pull/17121>`_
- Bugfix: Conan Server: Do not return duplicated references for each revision of the same recipe reference when searching them. `#17121 <https://github.com/conan-io/conan/pull/17121>`_
- Bugfix: Empty version range results in empty condition set. `#17116 <https://github.com/conan-io/conan/pull/17116>`_
- Bugfix: Adding the `# do not sort` comment to `deps` section. Regression since Conan 1.61. `#17109 <https://github.com/conan-io/conan/pull/17109>`_
- Bugfix: Restore ConanOutput global state when using `Commands` API. `#17095 <https://github.com/conan-io/conan/pull/17095>`_
- Bugfix: `build_args` options in `graph build-order` now respect the context of the reference. `#16594 <https://github.com/conan-io/conan/pull/16594>`_

2.8.1 (17-Oct-2024)
--------------------

- Bugfix: Avoid raising an error for required components for ``test_requires`` also required as transitive ``requires``. `#17174 <https://github.com/conan-io/conan/pull/17174>`_

2.8.0 (30-Sept-2024)
--------------------

- Feature: Add support for iOS 18, watchOS 11, tvOS 18, visionOS 2 & macos 15. `#17012 <https://github.com/conan-io/conan/pull/17012>`_ . Docs `here <https://github.com/conan-io/docs/pull/3851>`__
- Feature: Add Clang 19 support. `#17010 <https://github.com/conan-io/conan/pull/17010>`_ . Docs `here <https://github.com/conan-io/docs/pull/3851>`__
- Feature: ``conan config list <pattern>`` to filter available configurations. `#17000 <https://github.com/conan-io/conan/pull/17000>`_ . Docs `here <https://github.com/conan-io/docs/pull/3853>`__
- Feature: New ``auth_remote.py`` plugin for custom user authentication to Conan remotes. `#16942 <https://github.com/conan-io/conan/pull/16942>`_ . Docs `here <https://github.com/conan-io/docs/pull/3846>`__
- Feature: New ``auth_source.py`` plugin for custom user authentication for generic downloads of sources. `#16942 <https://github.com/conan-io/conan/pull/16942>`_ . Docs `here <https://github.com/conan-io/docs/pull/3846>`__
- Feature: Add `--envs-generation={false}` to :command:`conan install` and :command:`conan build` to disable the generation of virtualenvs (``conanbuildenv.sh|bat`` and ``conanrunenv.sh|bat``). `#16935 <https://github.com/conan-io/conan/pull/16935>`_ . Docs `here <https://github.com/conan-io/docs/pull/3855>`__
- Feature: New ``tools.files.unzip:filter`` conf that allows to define ``data``, ``tar`` and ``fully_trusted`` extraction policies for tgz files. `#16918 <https://github.com/conan-io/conan/pull/16918>`_ . Docs `here <https://github.com/conan-io/docs/pull/3857>`__
- Feature: ``get()`` and ``unzip()`` tools for ``source()`` learned a new ``extract_filter`` argument to define ``data``, ``tar`` and ``fully_trusted`` extraction policies for tgz files. `#16918 <https://github.com/conan-io/conan/pull/16918>`_ . Docs `here <https://github.com/conan-io/docs/pull/3857>`__
- Feature: Add progress updates for large uploads (>100Mbs) every 10 seconds. `#16913 <https://github.com/conan-io/conan/pull/16913>`_
- Feature: Implement ``conan config install-pkg --url=<repo-url>`` for initial definition of remote URL when no remotes are defined yet. `#16876 <https://github.com/conan-io/conan/pull/16876>`_ . Docs `here <https://github.com/conan-io/docs/pull/3854>`__
- Feature: Allow building a compatible package still of the current profile one. `#16871 <https://github.com/conan-io/conan/pull/16871>`_
- Feature: Allow bootstrapping (depending on another variant of yourself), even for the same version. `#16870 <https://github.com/conan-io/conan/pull/16870>`_
- Feature: Allow ``[replace_requires]`` to replace the package name and ``self.dependencies`` still works with the old name. `#16443 <https://github.com/conan-io/conan/pull/16443>`_
- Fix: Let ``CMakeToolchain`` defining ``CMAKE_SYSTEM_XXX`` even if ``user_toolchain`` is defined, but protected in case the toolchain really defines them. `#17036 <https://github.com/conan-io/conan/pull/17036>`_ . Docs `here <https://github.com/conan-io/docs/pull/3852>`__
- Fix: Replace `|` character in generated CMake and Environment files. `#17024 <https://github.com/conan-io/conan/pull/17024>`_
- Fix: Redirect the ``PkgConfig`` ``stderr`` to the exception raised. `#17020 <https://github.com/conan-io/conan/pull/17020>`_
- Fix: Use always forward slashes in Windows subsystems ``bash`` path. `#16997 <https://github.com/conan-io/conan/pull/16997>`_
- Fix: Better error messages when ``conan list --graph=<graph-json-file>`` file has issues. `#16936 <https://github.com/conan-io/conan/pull/16936>`_
- Bugfix: `PkgConfigDeps.set_property()` was not setting properly all the available properties. `#17051 <https://github.com/conan-io/conan/pull/17051>`_
- Bugfix: BazelDeps did not find DLL files as Conan does not model them in the Windows platform. `#17045 <https://github.com/conan-io/conan/pull/17045>`_
- Bugfix: Do not skip dependencies of a package if it is not going to be skipped due to ``tools.graph:skip_binaries=False``. `#17033 <https://github.com/conan-io/conan/pull/17033>`_
- Bugfix: Allow ``requires(..., package_id_mode)`` trait in case of diamonds to always use the recipe defined one irrespective of ``requires()`` order. `#16987 <https://github.com/conan-io/conan/pull/16987>`_
- Bugfix: Propagate include_prerelease flag to intersection of VersionRange. `#16986 <https://github.com/conan-io/conan/pull/16986>`_
- Bugfix: Raise error if invalid value passed to conf.get(check_type=bool). `#16976 <https://github.com/conan-io/conan/pull/16976>`_
- Bugfix: Allow `remote_login` accept patterns. `#16942 <https://github.com/conan-io/conan/pull/16942>`_ . Docs `here <https://github.com/conan-io/docs/pull/3846>`__

2.7.1 (11-Sept-2024)
--------------------

- Feature: Add support apple-clang 16. `#16972 <https://github.com/conan-io/conan/pull/16972>`_
- Fix: Add test for #19960. `#16974 <https://github.com/conan-io/conan/pull/16974>`_
- Bugfix: Revert "Define compiler variables in CMakePresets.json" commit 60df72cf75254608ebe6a447106e60be4d8c05a4. `#16971 <https://github.com/conan-io/conan/pull/16971>`_

2.7.0 (28-Aug-2024)
-------------------

- Feature: Added ``Git.is_dirty(repository=False)`` new argument `#16892 <https://github.com/conan-io/conan/pull/16892>`_
- Feature: Add variable_watch for `CMAKE_{C,CXX}_STANDARD` in `conan_toolchain.cmake`. `#16879 <https://github.com/conan-io/conan/pull/16879>`_
- Feature: Add `check_type` to `get_property`  for CMakeDeps. `#16854 <https://github.com/conan-io/conan/pull/16854>`_ . Docs `here <https://github.com/conan-io/docs/pull/3815>`__
- Feature: Propagate `run` trait requirement information in the "build" context downstream when `visible` trait is `True`. `#16849 <https://github.com/conan-io/conan/pull/16849>`_ . Docs `here <https://github.com/conan-io/docs/pull/3816>`__
- Feature: Add `check_type` on  components `get_property`. `#16848 <https://github.com/conan-io/conan/pull/16848>`_ . Docs `here <https://github.com/conan-io/docs/pull/3815>`__
- Feature: Add `set_property` for PkgConfigDeps to set properties for requirements from consumer recipes. `#16789 <https://github.com/conan-io/conan/pull/16789>`_
- Feature: Define `CMAKE_<LANG>_COMPILER` variables in CMakePresets.json. `#16762 <https://github.com/conan-io/conan/pull/16762>`_
- Feature: Add support for gcc 14.2. `#16760 <https://github.com/conan-io/conan/pull/16760>`_
- Feature: Rework QbsProfile to support Conan 2. `#16742 <https://github.com/conan-io/conan/pull/16742>`_
- Feature: Add `finalize()` method for local cache final adjustments of packages. `#16646 <https://github.com/conan-io/conan/pull/16646>`_ . Docs `here <https://github.com/conan-io/docs/pull/3820>`__
- Feature: Add ``tricore`` compiler architecture support. `#16317 <https://github.com/conan-io/conan/pull/16317>`_ . Docs `here <https://github.com/conan-io/docs/pull/3819>`__
- Feature: Describe here your pull request `#16317 <https://github.com/conan-io/conan/pull/16317>`_ . Docs `here <https://github.com/conan-io/docs/pull/3819>`__
- Fix: Propagate ``repository`` argument from ``Git.get_url_and_commit(repository=True)`` to ``Git.is_dirty()``. `#16892 <https://github.com/conan-io/conan/pull/16892>`_
- Fix: Improve error when accessing `cpp_info` shorthand methods. `#16847 <https://github.com/conan-io/conan/pull/16847>`_
- Fix: Improve error message when a lockfile fails to lock a requirement, specifying its type. `#16841 <https://github.com/conan-io/conan/pull/16841>`_
- Fix: Update patch-ng 1.18.0 to avoid SyntaxWarning spam. `#16766 <https://github.com/conan-io/conan/pull/16766>`_
- Bugfix: Avoid ``CMakeToolchain`` error when both architecture flags and ``tools.build:linker_scripts`` are defined, due to missing space. `#16883 <https://github.com/conan-io/conan/pull/16883>`_
- Bugfix: When using Visual Studio's llvm-clang, set the correct Platform Toolset in `MSBuildToolchain`. `#16844 <https://github.com/conan-io/conan/pull/16844>`_
- Bugfix: Fix `export_sources` for non-existent recipes in a local recipes index. `#16776 <https://github.com/conan-io/conan/pull/16776>`_

2.6.0 (01-Aug-2024)
-------------------

- Feature: Add ``build_folder_vars=["const.myvalue"]`` to create presets for user "myvalue" arbitrary values. `#16633 <https://github.com/conan-io/conan/pull/16633>`_ . Docs `here <https://github.com/conan-io/docs/pull/3800>`__
- Feature: Added `outputRootDir` as an optional definition in Bazel new templates. `#16620 <https://github.com/conan-io/conan/pull/16620>`_
- Feature: MakeDeps generator generates make variables for dependencies and their components. `#16613 <https://github.com/conan-io/conan/pull/16613>`_ . Docs `here <https://github.com/conan-io/docs/pull/3794>`__
- Feature: Add html output for graph build-order and graph build-order-merge `#16611 <https://github.com/conan-io/conan/pull/16611>`_ . Docs `here <https://github.com/conan-io/docs/pull/3805>`__
- Feature: Introduce ``core.scm:local_url=allow|block`` to control local folder URLs in conandata ``scm``. `#16597 <https://github.com/conan-io/conan/pull/16597>`_ . Docs `here <https://github.com/conan-io/docs/pull/3801>`__
- Feature: Added `XXX_FOR_BUILD` flags and Android extra ones to `extra_env` attribute in `GnuToolchain`. `#16596 <https://github.com/conan-io/conan/pull/16596>`_
- Feature: Support ``python_requires`` in ``local-recipes-index``. `#16420 <https://github.com/conan-io/conan/pull/16420>`_ . Docs `here <https://github.com/conan-io/docs/pull/3802>`__
- Fix: Avoid ``runtime_deployer`` to deploy dependencies with ``run=False`` trait. `#16724 <https://github.com/conan-io/conan/pull/16724>`_
- Fix: Improve error message when passing a ``--deployer-folder=xxx`` argument of an incorrect folder. `#16723 <https://github.com/conan-io/conan/pull/16723>`_
- Fix: Change ``requirements.txt`` so it install ``distro`` package in FreeBSD too. `#16700 <https://github.com/conan-io/conan/pull/16700>`_
- Fix: Better error messages when loading an inexistent or broken "package list" file. `#16685 <https://github.com/conan-io/conan/pull/16685>`_
- Fix: Remove unsupported `ld` and `ar` entries from `tools.build:compiler_executables`, they had no effect in every Conan integration. `#16647 <https://github.com/conan-io/conan/pull/16647>`_
- Fix: Ensure direct tool requires conflicts are properly reported instead of hanging. `#16619 <https://github.com/conan-io/conan/pull/16619>`_
- Fix: Update ``docker`` dependency version for the ``runners`` feature `#16610 <https://github.com/conan-io/conan/pull/16610>`_
- Fix: Raise an error when trying to upload a package with a local folder URL in ``conandata`` ``scm``. `#16597 <https://github.com/conan-io/conan/pull/16597>`_ . Docs `here <https://github.com/conan-io/docs/pull/3801>`__
- Bugfix: Fix profile ``include()`` with per-package ``[settings]`` with partial definition. `#16720 <https://github.com/conan-io/conan/pull/16720>`_
- Bugfix: The ``MakeDeps`` generator was missing some aggregated variables when packages have components. `#16715 <https://github.com/conan-io/conan/pull/16715>`_
- Bugfix: Avoid `settings.update_values()` failing when deducing compatibility. `#16642 <https://github.com/conan-io/conan/pull/16642>`_
- Bugfix: Fix handling of `tools.build:defines` for Ninja Multi-Config CMake. `#16637 <https://github.com/conan-io/conan/pull/16637>`_
- Bugfix: Make conan graph <subcommand> a real "install" dry-run. Return same errors and give same messages `#16415 <https://github.com/conan-io/conan/pull/16415>`_

2.5.0 (03-Jul-2024)
-------------------

- Feature: New ``tools.cmake.cmaketoolchain:enabled_blocks`` configuration to define which blocks of ``CMakeToolchain`` should be active or not. `#16563 <https://github.com/conan-io/conan/pull/16563>`_ . Docs `here <https://github.com/conan-io/docs/pull/3786>`__
- Feature: Allow `--filter-options` in `conan list` to use `&:` scope to refer to all packages being listed. `#16559 <https://github.com/conan-io/conan/pull/16559>`_
- Feature: Highlight missing or invalid requirements while computing dependency graph. `#16520 <https://github.com/conan-io/conan/pull/16520>`_
- Feature: New ``conan lock update`` subcommand to remove + add a reference in the same command. `#16511 <https://github.com/conan-io/conan/pull/16511>`_ . Docs `here <https://github.com/conan-io/docs/pull/3784>`__
- Feature: Add support for GCC 12.4. `#16506 <https://github.com/conan-io/conan/pull/16506>`_ . Docs `here <https://github.com/conan-io/docs/pull/3783>`__
- Feature: Honoring `tools.android:ndk_path` conf. Setting the needed flags to cross-build for Android. `#16502 <https://github.com/conan-io/conan/pull/16502>`_ . Docs `here <https://github.com/conan-io/docs/pull/3787>`__
- Feature: Add ``os.ndk_version`` for ``Android``. `#16494 <https://github.com/conan-io/conan/pull/16494>`_ . Docs `here <https://github.com/conan-io/docs/pull/3783>`__
- Feature: Qbs helper now invokes Conan provider automatically. `#16486 <https://github.com/conan-io/conan/pull/16486>`_
- Feature: Added force option to `tools.cmake.cmaketoolchain:extra_variables`. `#16481 <https://github.com/conan-io/conan/pull/16481>`_ . Docs `here <https://github.com/conan-io/docs/pull/3774>`__
- Feature: Raising a ConanException if any section is duplicated in the same Conan profile file. `#16454 <https://github.com/conan-io/conan/pull/16454>`_
- Feature: Added `resolve()` method to the Qbs toolchain. `#16449 <https://github.com/conan-io/conan/pull/16449>`_
- Feature: Make ``MSBuildDeps`` generation with deployer relocatable. `#16441 <https://github.com/conan-io/conan/pull/16441>`_
- Feature: Add QbsDeps class to be used with Qbs Conan module provider. `#16334 <https://github.com/conan-io/conan/pull/16334>`_
- Feature: Add built in `runtime_deploy` deployer. `#15382 <https://github.com/conan-io/conan/pull/15382>`_ . Docs `here <https://github.com/conan-io/docs/pull/3789>`__
- Fix: Fix provides conflict error message not showing conflicting provides when a named reference matches a provider. `#16562 <https://github.com/conan-io/conan/pull/16562>`_
- Fix: Set correct `testpaths` for pytest. `#16530 <https://github.com/conan-io/conan/pull/16530>`_
- Fix: Allow ``.conanrc`` file in the root of a filesystem. `#16514 <https://github.com/conan-io/conan/pull/16514>`_
- Fix: Add support for non default docker hosts in conan runners `#16477 <https://github.com/conan-io/conan/pull/16477>`_
- Fix: Don't fail when we can't overwrite the summary file in the backup upload. `#16452 <https://github.com/conan-io/conan/pull/16452>`_
- Fix: Make ``source_credentials.json`` do not apply to Conan server repos protocol. `#16425 <https://github.com/conan-io/conan/pull/16425>`_ . Docs `here <https://github.com/conan-io/docs/pull/3785>`__
- Fix: Allow packages to have empty folders. `#16424 <https://github.com/conan-io/conan/pull/16424>`_
- Bugfix: Fix ``detect_msvc_compiler()`` from ``detect_api`` to properly detect VS 17.10 with ``compiler.version=194``. `#16581 <https://github.com/conan-io/conan/pull/16581>`_
- Bugfix: Fix unexpected error when a recipe performs `package_id()` `info` erasure and is used as a compatibility candidate. `#16575 <https://github.com/conan-io/conan/pull/16575>`_
- Bugfix: Ensure msvc cppstd compatibility fallback does not ignore 194 binaries. `#16573 <https://github.com/conan-io/conan/pull/16573>`_
- Bugfix: `XXXDeps` generators did not include an absolute path in their generated files if `--deployer-folder=xxxx` param was used. `#16552 <https://github.com/conan-io/conan/pull/16552>`_
- Bugfix: Fix `conan list ... --format=compact` for package revisions. `#16490 <https://github.com/conan-io/conan/pull/16490>`_
- Bugfix: Fix XcodeToolchain when only defines are set. `#16429 <https://github.com/conan-io/conan/pull/16429>`_

2.4.1 (10-Jun-2024)
-------------------

- Fix: Avoid `find_package`'s of transitive dependencies on `test_package` generated by `cmake_lib` template. `#16451 <https://github.com/conan-io/conan/pull/16451>`_
- Fix: Fix back migration of default compatibility.py from a clean install. `#16417 <https://github.com/conan-io/conan/pull/16417>`_
- Bugfix: Solve issue with setuptools (distributed Conan packages in Python) packaging the "test" folder. `#16446 <https://github.com/conan-io/conan/pull/16446>`_
- Bugfix: Fixed regression in ``CMakeToolchain`` with ``--deployer=full_deploy`` creating wrong escaping. `#16434 <https://github.com/conan-io/conan/pull/16434>`_

2.4.0 (05-Jun-2024)
-------------------

- Feature: Added support for MacOS sdk_version 14.5 `#16400 <https://github.com/conan-io/conan/pull/16400>`_ . Docs `here <https://github.com/conan-io/docs/pull/3758>`__
- Feature: Added `CC_FOR_BUILD` and  `CXX_FOR_BUILD` environment variable to AutotoolsToolchain. `#16391 <https://github.com/conan-io/conan/pull/16391>`_ . Docs `here <https://github.com/conan-io/docs/pull/3750>`__
- Feature: Added `extra_xxxx` flags to MesonToolchain as done in other toolchains like AutotoolsToolchain, CMakeToolchain, etc. `#16389 <https://github.com/conan-io/conan/pull/16389>`_
- Feature: Add new ``qbs_lib`` template for the :command:`conan new` command. `#16382 <https://github.com/conan-io/conan/pull/16382>`_
- Feature: new ``detect_api.detect_sdk_version()`` method `#16355 <https://github.com/conan-io/conan/pull/16355>`_ . Docs `here <https://github.com/conan-io/docs/pull/3751>`__
- Feature: Add excludes parameter to tools.files.rm to void removing pattern. `#16350 <https://github.com/conan-io/conan/pull/16350>`_ . Docs `here <https://github.com/conan-io/docs/pull/3743>`__
- Feature: Allow multiple ``--build=missing:~pattern1 --build=missing:~pattern2`` patterns. `#16327 <https://github.com/conan-io/conan/pull/16327>`_
- Feature: Deprecate use of path accessors in ConanFile. `#16247 <https://github.com/conan-io/conan/pull/16247>`_
- Feature: add support for setting `tools.cmake.cmaketoolchain:extra_variables` `#16242 <https://github.com/conan-io/conan/pull/16242>`_ . Docs `here <https://github.com/conan-io/docs/pull/3719>`__
- Feature: Add `cmake_additional_variables_prefixes` variable to CMakeDeps generator to allow adding extra names for declared CMake variables. `#16231 <https://github.com/conan-io/conan/pull/16231>`_ . Docs `here <https://github.com/conan-io/docs/pull/3721>`__
- Feature: Allow GNUInstallDirs definition in ``CMakeToolchain`` for the local ``conan install/build`` flow too. `#16214 <https://github.com/conan-io/conan/pull/16214>`_
- Feature: Let ``conan cache save`` listen to the ``core.gzip:compresslevel`` conf. `#16211 <https://github.com/conan-io/conan/pull/16211>`_
- Feature: Add support for Bazel >= 7.1. `#16196 <https://github.com/conan-io/conan/pull/16196>`_ . Docs `here <https://github.com/conan-io/docs/pull/3707>`__
- Feature: Add new ``revision_mode`` including everything down to the ``recipe-revision``, but not the ``package_id``. `#16195 <https://github.com/conan-io/conan/pull/16195>`_ . Docs `here <https://github.com/conan-io/docs/pull/3754>`__
- Feature: Allow a recipe to ``requires(..., visible=False)`` a previous version of itself without raising a loop error. `#16132 <https://github.com/conan-io/conan/pull/16132>`_
- Feature: New ``vendor=True`` package creation and build isolation strategy `#16073 <https://github.com/conan-io/conan/pull/16073>`_ . Docs `here <https://github.com/conan-io/docs/pull/3756>`__
- Feature: New ``compiler.cstd`` setting for C standard `#16028 <https://github.com/conan-io/conan/pull/16028>`_ . Docs `here <https://github.com/conan-io/docs/pull/3757>`__
- Feature: Implemented ``compatibility.py`` default compatibility for different C standards `#16028 <https://github.com/conan-io/conan/pull/16028>`_ . Docs `here <https://github.com/conan-io/docs/pull/3757>`__
- Feature: Implement ``check_min_cstd``, ``check_max_cstd``, ``valid_max_cstd``, ``valid_min_cstd``, ``supported_cstd`` tools `#16028 <https://github.com/conan-io/conan/pull/16028>`_ . Docs `here <https://github.com/conan-io/docs/pull/3757>`__
- Feature: New ``languages = "C", "C++"`` class attribute to further automate settings management `#16028 <https://github.com/conan-io/conan/pull/16028>`_ . Docs `here <https://github.com/conan-io/docs/pull/3757>`__
- Feature: Add `CONAN_RUNTIME_LIB_DIRS` variable to the `conan_toolchain.cmake`. `#15914 <https://github.com/conan-io/conan/pull/15914>`_ . Docs `here <https://github.com/conan-io/docs/pull/3698>`__
- Fix: Implement a back migration to <2.3 for default ``compatibility.py`` plugin. `#16405 <https://github.com/conan-io/conan/pull/16405>`_
- Fix: Add missing `[replace_requires]` and `[platform_requires]` to serialization/dump of profiles. `#16401 <https://github.com/conan-io/conan/pull/16401>`_
- Fix: Fix handling spaces in paths in ``Qbs`` helper. `#16382 <https://github.com/conan-io/conan/pull/16382>`_
- Fix: Make cc version detection more robust `#16362 <https://github.com/conan-io/conan/pull/16362>`_
- Fix: Allow ``--build=missing:&`` pattern to build only the consumer if missing, but not others. `#16344 <https://github.com/conan-io/conan/pull/16344>`_
- Fix: Allow "local-recipes-index" to ``conan list`` packages with custom ``user/channel``. `#16342 <https://github.com/conan-io/conan/pull/16342>`_
- Fix: Fixing docstrings for ``cppstd`` functions. `#16341 <https://github.com/conan-io/conan/pull/16341>`_
- Fix: Change autodetect of `CMAKE_SYSTEM_VERSION` to use the Darwin version. `#16335 <https://github.com/conan-io/conan/pull/16335>`_ . Docs `here <https://github.com/conan-io/docs/pull/3755>`__
- Fix: Fix `require` syntax in output in `graph build-order`. `#16308 <https://github.com/conan-io/conan/pull/16308>`_
- Fix: Improve some commands help documentation strings by adding double quotes. `#16292 <https://github.com/conan-io/conan/pull/16292>`_
- Fix: Better error message for incorrect version-ranges definitions. `#16289 <https://github.com/conan-io/conan/pull/16289>`_
- Fix: Only print info about cached recipe revision being newer when it truly is. `#16275 <https://github.com/conan-io/conan/pull/16275>`_
- Fix: Warn when using ``options`` without pattern scope, to improve UX of users expecting ``-o shared=True`` to apply to dependencies. `#16233 <https://github.com/conan-io/conan/pull/16233>`_ . Docs `here <https://github.com/conan-io/docs/pull/3720>`__
- Fix: Fix CommandAPI usage when not used by Conan custom commands. `#16213 <https://github.com/conan-io/conan/pull/16213>`_
- Fix: Avoid ``datetime`` deprecated calls in Python 3.12. `#16095 <https://github.com/conan-io/conan/pull/16095>`_
- Fix: Handle `tools.build:sysroot` on Meson toolchain. `#16011 <https://github.com/conan-io/conan/pull/16011>`_ . Docs `here <https://github.com/conan-io/docs/pull/3753>`__
- Bugfix: Fix ``LLVM/Clang`` enablement of ``vcvars`` for latest ``v14.4`` toolset version after VS 17.10 update `#16374 <https://github.com/conan-io/conan/pull/16374>`_ . Docs `here <https://github.com/conan-io/docs/pull/3752>`__
- Bugfix: Fix profile errors when using a docker runner of `type=shared` `#16364 <https://github.com/conan-io/conan/pull/16364>`_
- Bugfix: ``conan graph info .. --build=pkg`` doesn't download ``pkg`` sources unless ``tools.build:download_source`` is defined. `#16349 <https://github.com/conan-io/conan/pull/16349>`_
- Bugfix: Solved problem with relativization of paths in CMakeToolchain and CMakeDeps. `#16316 <https://github.com/conan-io/conan/pull/16316>`_
- Bugfix: Avoid sanitizing `tools.build:compiler_executables` value in MesonToolchain. `#16307 <https://github.com/conan-io/conan/pull/16307>`_
- Bugfix: Solved incorrect paths in ``conan cache save/restore`` tgz files that crashed when using ``storage_path`` custom configuration. `#16293 <https://github.com/conan-io/conan/pull/16293>`_
- Bugfix: Fix stacktrace with nonexistent graph file in `conan list`. `#16291 <https://github.com/conan-io/conan/pull/16291>`_
- Bugfix: Let ``CMakeDeps`` generator overwrite the ``xxxConfig.cmake`` when it already exists. `#16279 <https://github.com/conan-io/conan/pull/16279>`_
- Bugfix: Disallow `self.info` access in `source()` method. `#16272 <https://github.com/conan-io/conan/pull/16272>`_

2.3.2 (28-May-2024)
-------------------

- Feature: New ``tools.microsoft:msvc_update`` configuration to define the MSVC compiler ``update`` even when ``compiler.update`` is not defined. Can be used to use ``compiler.version=193`` once VS2022 is updated to 17.10, which changes the default compiler to ``compiler.version=194``. `#16332 <https://github.com/conan-io/conan/pull/16332>`_
- Bugfix: Allow default ``compatibility.py`` plugin to fallback from MSVC ``compiler.version=194->193`` and to other ``cppstd`` values. `#16346 <https://github.com/conan-io/conan/pull/16346>`_
- Bugfix: Skip dot folders in local recipe index layouts. `#16345 <https://github.com/conan-io/conan/pull/16345>`_
- Bugfix: Remove extra backslash in generated `conanvcvars.ps1`. `#16322 <https://github.com/conan-io/conan/pull/16322>`_

2.3.1 (16-May-2024)
-------------------

- Feature: Add GCC 13.3 support. `#16246 <https://github.com/conan-io/conan/pull/16246>`_ . Docs `here <https://github.com/conan-io/docs/pull/3724>`__
- Feature: Allow opt-out for ``CMakeToolchain`` default use of absolute paths for CMakeUserPresets->CMakePreset and CMakePresets->toolchainFile path. `#16244 <https://github.com/conan-io/conan/pull/16244>`_ . Docs `here <https://github.com/conan-io/docs/pull/3726>`__
- Fix: Fix config container name for Docker runner. `#16243 <https://github.com/conan-io/conan/pull/16243>`_
- Bugfix: Make compatibility checks understand update flag patterns. `#16252 <https://github.com/conan-io/conan/pull/16252>`_
- Bugfix: Solve bug with ``overrides`` from ``lockfiles`` in case of diamond structures. `#16235 <https://github.com/conan-io/conan/pull/16235>`_
- Bugfix: Allow ``export-pkg --version=xxx`` to be passed to recipes with ``python_requires`` inheriting ``set_version`` from base class. `#16224 <https://github.com/conan-io/conan/pull/16224>`_

2.3.0 (06-May-2024)
-------------------

- Feature: Allow `*` wildcard as subsetting in in `rm_safe`. `#16105 <https://github.com/conan-io/conan/pull/16105>`_ . Docs `here <https://github.com/conan-io/docs/pull/3697>`__
- Feature: Show recipe and package sizes when running :command:`conan upload`. `#16103 <https://github.com/conan-io/conan/pull/16103>`_
- Feature: Extend `conan version` to report current python and system for troubleshooting. `#16102 <https://github.com/conan-io/conan/pull/16102>`_ . Docs `here <https://github.com/conan-io/docs/pull/3691>`__
- Feature: Add ``detect_xxxx_compiler()`` for mainstream compilers as gcc, msvc, clang. to the public ``detect_api``. `#16092 <https://github.com/conan-io/conan/pull/16092>`_ . Docs `here <https://github.com/conan-io/docs/pull/3702>`__
- Feature: Add comment support for `.conanignore` file. `#16087 <https://github.com/conan-io/conan/pull/16087>`_
- Feature: In graph `html` search bar now takes in multiple search patterns separated by commas. `#16083 <https://github.com/conan-io/conan/pull/16083>`_
- Feature: In graph `html` added 'filter packages' bar that takes in multiple search patterns separated by comma and hides filters them from graph. `#16083 <https://github.com/conan-io/conan/pull/16083>`_
- Feature: Add an argument `hide_url` to Git operations to allow logging of the repository URL. By default, URLs will stay `<hidden>`, but users may opt-out of this. `#16038 <https://github.com/conan-io/conan/pull/16038>`_
- Feature: Allow ``.conf`` access (exclusively to ``global.conf`` information, not to profile information) in the ``export()`` and ``export_sources()`` methods. `#16034 <https://github.com/conan-io/conan/pull/16034>`_ . Docs `here <https://github.com/conan-io/docs/pull/3703>`__
- Feature: Avoid copying identical existing files in ``copy()``. `#16031 <https://github.com/conan-io/conan/pull/16031>`_
- Feature: New ``conan pkglist merge`` command to merge multiple package lists. `#16022 <https://github.com/conan-io/conan/pull/16022>`_ . Docs `here <https://github.com/conan-io/docs/pull/3704>`__
- Feature: New ``conan pkglist find-remote`` command to find matching in remotes for list of packages in the cache. `#16022 <https://github.com/conan-io/conan/pull/16022>`_ . Docs `here <https://github.com/conan-io/docs/pull/3704>`__
- Feature: Relativize paths in `CMakePresets` generation. `#16015 <https://github.com/conan-io/conan/pull/16015>`_
- Feature: Add new ``test_package_folder`` attribute to ``conanfile.py`` to define a different custom location and name rather than ``test_package`` default. `#16013 <https://github.com/conan-io/conan/pull/16013>`_ . Docs `here <https://github.com/conan-io/docs/pull/3705>`__
- Feature: New ``conan create --test-missing`` syntax to optionally run the ``test_package`` only when the package is actually created (useful with ``--build=missing``). `#15999 <https://github.com/conan-io/conan/pull/15999>`_ . Docs `here <https://github.com/conan-io/docs/pull/3705>`__
- Feature: Add `tools.gnu:build_triplet` to conf. `#15965 <https://github.com/conan-io/conan/pull/15965>`_
- Feature: Add ``--exist-ok`` argument to ``conan profile detect`` to not fail if the profile already exists, without overwriting it. `#15933 <https://github.com/conan-io/conan/pull/15933>`_
- Feature: MesonToolchain can generate a native file if native=True (only makes sense when cross-building). `#15919 <https://github.com/conan-io/conan/pull/15919>`_ . Docs `here <https://github.com/conan-io/docs/pull/3710>`__
- Feature: Meson helper injects native and cross files if both exist. `#15919 <https://github.com/conan-io/conan/pull/15919>`_ . Docs `here <https://github.com/conan-io/docs/pull/3710>`__
- Feature: Add support for meson subproject. `#15916 <https://github.com/conan-io/conan/pull/15916>`_ . Docs `here <https://github.com/conan-io/docs/pull/3655>`__
- Feature: Added transparent support for running Conan within a Docker container. `#15856 <https://github.com/conan-io/conan/pull/15856>`_ . Docs `here <https://github.com/conan-io/docs/pull/3699>`__
- Fix: Allow defining ``CC=/usr/bin/cc`` (and for CXX) for ``conan profile detect`` auto-detection. `#16187 <https://github.com/conan-io/conan/pull/16187>`_
- Fix: Solve issue in ``pyinstaller.py`` script, it will no longer install ``pip install pyinstaller``, having it installed will be a precondition `#16186 <https://github.com/conan-io/conan/pull/16186>`_
- Fix: Use backslash in ``CMake`` helper for the CMakeLists.txt folder, fixes issue when project is in the drive root, like ``X:`` `#16180 <https://github.com/conan-io/conan/pull/16180>`_
- Fix: Allowing ``conan editable remove <path>`` even when the path has been already deleted. `#16170 <https://github.com/conan-io/conan/pull/16170>`_
- Fix: Fix `conan new --help` formatting issue. `#16155 <https://github.com/conan-io/conan/pull/16155>`_
- Fix: Improved error message when there are conflicts in the graph. `#16137 <https://github.com/conan-io/conan/pull/16137>`_
- Fix: Improve error message when one URL is not a valid server but still returns 200-ok under a Conan "ping" API call. `#16126 <https://github.com/conan-io/conan/pull/16126>`_
- Fix: Solve ``sqlite3`` issues in FreeBSD due to queries with double quotes. `#16123 <https://github.com/conan-io/conan/pull/16123>`_
- Fix: Clean error message for ``conan cache restore <non-existing-file>``. `#16113 <https://github.com/conan-io/conan/pull/16113>`_
- Fix: Improve UX and error messages when a remotes or credentials file in the cache is invalid/empty. `#16091 <https://github.com/conan-io/conan/pull/16091>`_
- Fix: Use ``cc`` executable in Linux systems for autodetect compiler (``conan profile detect`` and ``detect_api``). `#16074 <https://github.com/conan-io/conan/pull/16074>`_
- Fix: Improve the definition of version ranges UX with better error message for invalid ``==, ~=, ^=`` operators. `#16069 <https://github.com/conan-io/conan/pull/16069>`_
- Fix: Improve error message UX when incorrect ``settings.yml`` or ``settings_user.yml``. `#16065 <https://github.com/conan-io/conan/pull/16065>`_
- Fix: Print a warning for Python 3.6 usage which is EOL since 2021. `#16003 <https://github.com/conan-io/conan/pull/16003>`_
- Fix: Remove duplicated printing of command line in ``Autotools`` helper. `#15991 <https://github.com/conan-io/conan/pull/15991>`_
- Fix: Add response error message output to HTTP Status 401 Errors in FileDownloader. `#15983 <https://github.com/conan-io/conan/pull/15983>`_
- Fix: Add gcc 14 to default ``settings.yml``. `#15958 <https://github.com/conan-io/conan/pull/15958>`_
- Fix: Make ``VCVars`` use the ``compiler.update`` to specify the toolset. `#15947 <https://github.com/conan-io/conan/pull/15947>`_
- Fix: Add ``rc`` to ``AutotoolsToolchain`` mapping of ``compiler_executables`` for cross-build Linux->Windows. `#15946 <https://github.com/conan-io/conan/pull/15946>`_
- Fix: Add ``Pop!_OS`` to the distros using ``apt-get`` as system package manager. `#15931 <https://github.com/conan-io/conan/pull/15931>`_
- Fix: Do not warn with package names containing the `-` character. `#15920 <https://github.com/conan-io/conan/pull/15920>`_
- Fix: Fix html escaping of new ``--format=html`` graph output, and pass the graph serialized object instead of the string. `#15915 <https://github.com/conan-io/conan/pull/15915>`_
- Bugfix: Make MesonToolchain listen to `tools.build:defines` conf variable. `#16172 <https://github.com/conan-io/conan/pull/16172>`_ . Docs `here <https://github.com/conan-io/docs/pull/3709>`__
- Bugfix: Disallow `self.cpp_info` access in `validate_build()` method. `#16135 <https://github.com/conan-io/conan/pull/16135>`_
- Bugfix: Don't show a trace when `.conanrc`'s `conan_home` is invalid. `#16134 <https://github.com/conan-io/conan/pull/16134>`_
- Bugfix: Avoid the propagation of transitive dependencies of ``tool_requires`` to generators information even if they are marked as ``visible=True``. `#16077 <https://github.com/conan-io/conan/pull/16077>`_
- Bugfix: `BazelDeps` now uses the `requirement.build` property instead of `dependency.context` one. `#16025 <https://github.com/conan-io/conan/pull/16025>`_
- Bugfix: Make `conan cache restore` work correctly when restoring over a package already in the local cache. `#15950 <https://github.com/conan-io/conan/pull/15950>`_

2.2.3 (17-Apr-2024)
-------------------

- Fix: Fix `to_apple_archs` method when using architectures from settings_user. `#16090 <https://github.com/conan-io/conan/pull/16090>`_

2.2.2 (25-Mar-2024)
-------------------

- Fix: Avoid issues with recipe ``print(..., file=fileobj)``. `#15934 <https://github.com/conan-io/conan/pull/15934>`_
- Fix: Fix broken calls to `print(x, file=y)` with duplicate keyword arguments. `#15912 <https://github.com/conan-io/conan/pull/15912>`_
- Bugfix: Fix handling of `tools.build:defines` for multiconfig CMake. `#15924 <https://github.com/conan-io/conan/pull/15924>`_

2.2.1 (20-Mar-2024)
-------------------

- Fix: Add `copytree_compat` method for compatibility with Python>=3.12 after distutils removal. `#15906 <https://github.com/conan-io/conan/pull/15906>`_

2.2.0 (20-Mar-2024)
-------------------

- Feature: Raise for toolchains different than CMakeToolchain if using universal binary syntax. `#15896 <https://github.com/conan-io/conan/pull/15896>`_
- Feature: Warn on misplaced requirement function calls `#15888 <https://github.com/conan-io/conan/pull/15888>`_
- Feature: Print options conflicts in the graph caused by different branches recipes defining options values. `#15876 <https://github.com/conan-io/conan/pull/15876>`_ . Docs `here <https://github.com/conan-io/docs/pull/3643>`__
- Feature: Add macOS versions 14.2, 14.3, 14.4 to `settings.yml`. `#15859 <https://github.com/conan-io/conan/pull/15859>`_ . Docs `here <https://github.com/conan-io/docs/pull/3628>`__
- Feature: New graph ``html``: more information, test-requires, hiding/showing different packages (build, test). `#15846 <https://github.com/conan-io/conan/pull/15846>`_ . Docs `here <https://github.com/conan-io/docs/pull/3644>`__
- Feature: Add `--backup-sources` flag to `conan cache clean`. `#15845 <https://github.com/conan-io/conan/pull/15845>`_
- Feature: Add `conan graph outdated` command that lists the dependencies that have newer versions in remotes `#15838 <https://github.com/conan-io/conan/pull/15838>`_ . Docs `here <https://github.com/conan-io/docs/pull/3641>`__
- Feature: Set `CMAKE_VS_DEBUGGER_ENVIRONMENT` from CMakeToolchain to point to all binary directories when using Visual Studio. This negates the need to copy DLLs to launch executables from the Visual Studio IDE (requires CMake 3.27 or newer). `#15830 <https://github.com/conan-io/conan/pull/15830>`_ . Docs `here <https://github.com/conan-io/docs/pull/3639>`__
- Feature: Add a parameter to `trim_conandata` to avoid raising an exception when conandata.yml file doesn't exist. `#15829 <https://github.com/conan-io/conan/pull/15829>`_ . Docs `here <https://github.com/conan-io/docs/pull/3624>`__
- Feature: Added `build_context_folder ` to PkgConfigDeps. `#15813 <https://github.com/conan-io/conan/pull/15813>`_ . Docs `here <https://github.com/conan-io/docs/pull/3640>`__
- Feature: Included `build.pkg_config_path ` in the built-in options section in the MesonToolchain template. `#15813 <https://github.com/conan-io/conan/pull/15813>`_ . Docs `here <https://github.com/conan-io/docs/pull/3640>`__
- Feature: Update `_meson_cpu_family_map` to support `arm64ec`. `#15812 <https://github.com/conan-io/conan/pull/15812>`_
- Feature: Added support for Clang 18. `#15806 <https://github.com/conan-io/conan/pull/15806>`_ . Docs `here <https://github.com/conan-io/docs/pull/3637>`__
- Feature: Add basic support in CMakeToolchain for universal binaries. `#15775 <https://github.com/conan-io/conan/pull/15775>`_ . Docs `here <https://github.com/conan-io/docs/pull/3642>`__
- Feature: New ``tools.cmake.cmake_layout:build_folder`` config that allows re-defining ``cmake_layout`` local build-folder. `#15767 <https://github.com/conan-io/conan/pull/15767>`_ . Docs `here <https://github.com/conan-io/docs/pull/3646>`__
- Feature: New ``tools.cmake.cmake_layout:test_folder`` config that allows re-defining ``cmake_layout`` output build folder for ``test_package``, including a ``$TMP`` placeholder to create a temporary folder in system ``tmp``. `#15767 <https://github.com/conan-io/conan/pull/15767>`_ . Docs `here <https://github.com/conan-io/docs/pull/3646>`__
- Feature: (Experimental) Add ``conan config install-pkg myconf/[*]`` new configuration inside Conan packages with new ``package_type = "configuration"``. `#15748 <https://github.com/conan-io/conan/pull/15748>`_ . Docs `here <https://github.com/conan-io/docs/pull/3648>`__
- Feature: (Experimental) New ``core.package_id:config_mode`` that allows configuration package reference to affect the ``package_id`` of all packages built with that configuration. `#15748 <https://github.com/conan-io/conan/pull/15748>`_ . Docs `here <https://github.com/conan-io/docs/pull/3648>`__
- Feature: Make `cppstd_flag` public to return the corresponding C++ standard flag based on the settings. `#15710 <https://github.com/conan-io/conan/pull/15710>`_ . Docs `here <https://github.com/conan-io/docs/pull/3599>`__
- Feature: Allow ``self.name`` and ``self.version`` in ``build_folder_vars`` attribute and conf. `#15705 <https://github.com/conan-io/conan/pull/15705>`_ . Docs `here <https://github.com/conan-io/docs/pull/3636>`__
- Feature: Add ``conan list --filter-xxx`` arguments to list package binaries that match settings+options. `#15697 <https://github.com/conan-io/conan/pull/15697>`_ . Docs `here <https://github.com/conan-io/docs/pull/3647>`__
- Feature: Add `detect_libc` to the `detect_api` to get the name and version of the C library. `#15683 <https://github.com/conan-io/conan/pull/15683>`_ . Docs `here <https://github.com/conan-io/docs/pull/3590>`__
- Feature: New ``CommandAPI`` subapi in the ``ConanAPI`` that allows calling other commands. `#15630 <https://github.com/conan-io/conan/pull/15630>`_ . Docs `here <https://github.com/conan-io/docs/pull/3635>`__
- Fix: Avoid unnecessary build of ``tool_requires`` when ``--build=missing`` and repeated ``tool_requires``. `#15885 <https://github.com/conan-io/conan/pull/15885>`_
- Fix: Fix ``CMakeDeps`` ``set_property(... APPEND`` argument order. `#15877 <https://github.com/conan-io/conan/pull/15877>`_
- Fix: Raising an error when an infinite loop is found in the install graph (ill-formed dependency graph with loops). `#15835 <https://github.com/conan-io/conan/pull/15835>`_
- Fix: Make sure `detect_default_compiler()` always returns a 3-tuple. `#15832 <https://github.com/conan-io/conan/pull/15832>`_
- Fix: Print a clear message for ``conan graph explain`` when no binaries exist for one revision. `#15823 <https://github.com/conan-io/conan/pull/15823>`_
- Fix: Add ``package_type="static-library"`` to the ``conan new msbuild_lib`` template. `#15807 <https://github.com/conan-io/conan/pull/15807>`_
- Fix: Avoid ``platform_requires`` to fail when explicit options are being passed via ``requires(.., options={})``. `#15804 <https://github.com/conan-io/conan/pull/15804>`_
- Fix: Make ``CMakeToolchain`` end with newline. `#15788 <https://github.com/conan-io/conan/pull/15788>`_
- Fix: Do not allow ``conan list`` binary filters or package query if a binary pattern is not provided. `#15781 <https://github.com/conan-io/conan/pull/15781>`_
- Fix: Avoid ``CMakeToolchain.preprocessor_definition`` definitions to ``"None"`` literal string when it  has no value (Python ``None``). `#15756 <https://github.com/conan-io/conan/pull/15756>`_
- Fix: Improved ``conan install <path> --deployer-package=*`` case that was crashing when using ``self.package_folder``. `#15737 <https://github.com/conan-io/conan/pull/15737>`_
- Fix: Fix `conan graph info --format=html` for large dependency graphs. `#15724 <https://github.com/conan-io/conan/pull/15724>`_
- Fix: Make all recipe and plugins python file ``print()`` to ``stderr``, so json outputs to ``stdout`` are not broken. `#15704 <https://github.com/conan-io/conan/pull/15704>`_
- Fix: Fix getting the gnu triplet for Linux x86. `#15699 <https://github.com/conan-io/conan/pull/15699>`_
- Bugfix: Solve backslash issues with ``conan_home_folder`` in ``global.conf`` when used in strings inside lists. `#15870 <https://github.com/conan-io/conan/pull/15870>`_
- Bugfix: Fix ``CMakeDeps`` multi-config when there are conditional dependencies on the ``build_type``. `#15853 <https://github.com/conan-io/conan/pull/15853>`_
- Bugfix: Move `get_backup_sources()` method to expected `CacheAPI` from `UploadAPI`. `#15845 <https://github.com/conan-io/conan/pull/15845>`_
- Bugfix: Avoid TypeError when a version in conandata.yml lists no patches. `#15842 <https://github.com/conan-io/conan/pull/15842>`_
- Bugfix: Solve ``package_type=build-scripts`` issue with lockfiles and :command:`conan create`. `#15802 <https://github.com/conan-io/conan/pull/15802>`_
- Bugfix: Allow ``--channel`` command line argument if the recipe specifies ``user`` attribute. `#15794 <https://github.com/conan-io/conan/pull/15794>`_
- Bugfix: Fix cross-compilation to Android from Windows when using ``MesonToolchain``. `#15790 <https://github.com/conan-io/conan/pull/15790>`_
- Bugfix: Fix ``CMakeToolchain`` GENERATOR_TOOLSET when ``compiler.update`` is defined. `#15789 <https://github.com/conan-io/conan/pull/15789>`_
- Bugfix: Solved evaluation of ``conf`` items when they matched a Python module `#15779 <https://github.com/conan-io/conan/pull/15779>`_
- Bugfix: Fix ``PkgConfigDeps`` generating .pc files for its ``tool_requires`` when it is in the build context already. `#15763 <https://github.com/conan-io/conan/pull/15763>`_
- Bugfix: Adding `VISIBILITY` flags to `CONAN_C_FLAGS` too. `#15762 <https://github.com/conan-io/conan/pull/15762>`_
- Bugfix: Fix `conan profile show --format=json` for profiles with scoped confs. `#15747 <https://github.com/conan-io/conan/pull/15747>`_
- Bugfix: Fix legacy usage of `update` argument in Conan API. `#15743 <https://github.com/conan-io/conan/pull/15743>`_
- Bugfix: Solve broken profile ``[conf]`` when strings contains Windows backslash. `#15727 <https://github.com/conan-io/conan/pull/15727>`_
- Bugfix: Fix version precendence for metadata version ranges. `#15653 <https://github.com/conan-io/conan/pull/15653>`_

2.1.0 (15-Feb-2024)
-------------------

- Feature: Implement multi-config ``tools.build:xxxx`` flags in ``CMakeToolchain``. `#15654 <https://github.com/conan-io/conan/pull/15654>`_
- Feature: Add ability to pass patterns to `--update` flag. `#15652 <https://github.com/conan-io/conan/pull/15652>`_ . Docs `here <https://github.com/conan-io/docs/pull/3587>`__
- Feature: Add  `--format=json`  formatter to :command:`conan build`. `#15651 <https://github.com/conan-io/conan/pull/15651>`_
- Feature: Added `tools.build.cross_building:cross_build` to decide whether cross-building or not regardless of the internal Conan mechanism. `#15616 <https://github.com/conan-io/conan/pull/15616>`_
- Feature: Add `--format=json` option to `conan cache path`. `#15613 <https://github.com/conan-io/conan/pull/15613>`_
- Feature: Add the --order-by argument for conan graph build-order. `#15602 <https://github.com/conan-io/conan/pull/15602>`_ . Docs `here <https://github.com/conan-io/docs/pull/3582>`__
- Feature: Provide a new ``graph build-order --reduce`` argument to reduce the order exclusively to packages that need to be built from source. `#15573 <https://github.com/conan-io/conan/pull/15573>`_ . Docs `here <https://github.com/conan-io/docs/pull/3584>`__
- Feature: Add configuration to specify desired CUDA Toolkit in CMakeToolchain for Visual Studio CMake generators. `#15572 <https://github.com/conan-io/conan/pull/15572>`_ . Docs `here <https://github.com/conan-io/docs/pull/3568>`__
- Feature: New "important" options values definition, with higher precedence over regular option value definitions. `#15571 <https://github.com/conan-io/conan/pull/15571>`_ . Docs `here <https://github.com/conan-io/docs/pull/3585>`__
- Feature: Display message when calling `deactivate_conanvcvars`. `#15557 <https://github.com/conan-io/conan/pull/15557>`_
- Feature: Add ``self.info`` information of ``package_id`` to serialized output in the graph, and forward it to package-lists. `#15553 <https://github.com/conan-io/conan/pull/15553>`_ . Docs `here <https://github.com/conan-io/docs/pull/3553>`__
- Feature: Log Git tool commands when running in verbose mode. `#15514 <https://github.com/conan-io/conan/pull/15514>`_
- Feature: Add verbose debug information (with ``-vvv``) for ``conan.tools.files.copy()`` calls. `#15513 <https://github.com/conan-io/conan/pull/15513>`_
- Feature: Define ``python_requires = "tested_reference_str"`` for explicit ``test_package`` of ``python_requires``. `#15485 <https://github.com/conan-io/conan/pull/15485>`_ . Docs `here <https://github.com/conan-io/docs/pull/3537>`__
- Feature: Adding `CMakeToolchain.presets_build/run_environment` to modify `CMakePresets` environment in `generate()` method. `#15470 <https://github.com/conan-io/conan/pull/15470>`_ . Docs `here <https://github.com/conan-io/docs/pull/3547>`__
- Feature: Add `--allowed-packges` to remotes to limit what references a remote can supply. `#15464 <https://github.com/conan-io/conan/pull/15464>`_ . Docs `here <https://github.com/conan-io/docs/pull/3534>`__
- Feature: Initial documentation to make ``RemotesAPI`` publicly available (experimental). `#15462 <https://github.com/conan-io/conan/pull/15462>`_
- Feature: Add support for use of vcvars env variables when calling from powershell. `#15461 <https://github.com/conan-io/conan/pull/15461>`_ . Docs `here <https://github.com/conan-io/docs/pull/3541>`__
- Feature: New ``Git(..., excluded=[])`` feature to avoid "dirty" errors in ``Git`` helper. `#15457 <https://github.com/conan-io/conan/pull/15457>`_ . Docs `here <https://github.com/conan-io/docs/pull/3538>`__
- Feature: New ``core.scm:excluded`` feature to avoid "dirty" errors in ``Git`` helper and ``revision_mode = "scm"``. `#15457 <https://github.com/conan-io/conan/pull/15457>`_ . Docs `here <https://github.com/conan-io/docs/pull/3538>`__
- Feature: Recipe ``python_package_id_mode`` for ``python_requires`` recipes, to define per-recipe effect on consumers ``package_id``. `#15453 <https://github.com/conan-io/conan/pull/15453>`_ . Docs `here <https://github.com/conan-io/docs/pull/3542>`__
- Feature: Add cmakeExecutable to configure preset. `#15447 <https://github.com/conan-io/conan/pull/15447>`_ . Docs `here <https://github.com/conan-io/docs/pull/3548>`__
- Feature: Add new ``--core-conf`` command line argument to allow passing `core.` confs via CLI. `#15441 <https://github.com/conan-io/conan/pull/15441>`_ . Docs `here <https://github.com/conan-io/docs/pull/3515>`__
- Feature: Add ``detect_api.detect_msvc_update(version)`` helper to ``detect_api``. `#15435 <https://github.com/conan-io/conan/pull/15435>`_ . Docs `here <https://github.com/conan-io/docs/pull/3535>`__
- Feature: ``CMakeToolchain`` defines ``jobs`` in generated ``CMakePresets.json`` buildPresets. `#15422 <https://github.com/conan-io/conan/pull/15422>`_
- Feature: Allow nested "ANY" definitions in ``settings.yml``. `#15415 <https://github.com/conan-io/conan/pull/15415>`_ . Docs `here <https://github.com/conan-io/docs/pull/3546>`__
- Feature: Helpers ``Git().coordinates_to_conandata()`` and ``Git().checkout_from_conandata_coordinates()`` to simplify scm based flows. `#15377 <https://github.com/conan-io/conan/pull/15377>`_
- Feature: ``AutotoolsToolchain`` automatically inject ``-FS`` for VS. `#15375 <https://github.com/conan-io/conan/pull/15375>`_
- Feature: New :command:`conan upload` ``core.upload:parallel`` for faster parallel uploads. `#15360 <https://github.com/conan-io/conan/pull/15360>`_ . Docs `here <https://github.com/conan-io/docs/pull/3540>`__
- Feature: Intel oneAPI compiler detection improvement. `#15358 <https://github.com/conan-io/conan/pull/15358>`_
- Feature: Display progress for long ``conan list`` commands. `#15354 <https://github.com/conan-io/conan/pull/15354>`_
- Feature: Add `extension_properties` attribute to pass information to extensions from recipes. `#15348 <https://github.com/conan-io/conan/pull/15348>`_ . Docs `here <https://github.com/conan-io/docs/pull/3549>`__
- Feature: Implement `compatibility_cppstd` in `extension_properties` for the ``compatibility.py`` plugin to disable fallback to other cppstd for the recipe. `#15348 <https://github.com/conan-io/conan/pull/15348>`_ . Docs `here <https://github.com/conan-io/docs/pull/3549>`__
- Feature: Add ``Git.get_commit(..., repository=True)`` to obtain the repository commit, not the folder commit. `#15304 <https://github.com/conan-io/conan/pull/15304>`_
- Feature: Ensure ``--build=editable`` and ``--build=cascade`` works together. `#15300 <https://github.com/conan-io/conan/pull/15300>`_ . Docs `here <https://github.com/conan-io/docs/pull/3550>`__
- Feature: New ``conan graph build-order --order=configuration`` to output a different order, sorted by package binaries/configurations, not grouped by recipe revisions. `#15270 <https://github.com/conan-io/conan/pull/15270>`_ . Docs `here <https://github.com/conan-io/docs/pull/3552>`__
- Feature: Allow copy&paste of recipe revisions with timestamps from ``--format=compact`` into ``conan lock add``. `#15262 <https://github.com/conan-io/conan/pull/15262>`_ . Docs `here <https://github.com/conan-io/docs/pull/3533>`__
- Fix: Guarantee order of `generators` attribute execution. `#15678 <https://github.com/conan-io/conan/pull/15678>`_
- Fix: Solve issue with ``[platform_tool_requires]`` in the build profile and context. Discard ``[platform_requires]`` in build profile. `#15665 <https://github.com/conan-io/conan/pull/15665>`_
- Fix: Fix gcc detection in conda environments. `#15664 <https://github.com/conan-io/conan/pull/15664>`_
- Fix: Improve handling of `.dirty` download files when uploading backup sources. `#15601 <https://github.com/conan-io/conan/pull/15601>`_
- Fix: Fix relativize paths in generated files. `#15592 <https://github.com/conan-io/conan/pull/15592>`_
- Fix: Allow ``None`` values for ``CMakeToolchain.preprocessor_definitions`` that will map to definitions without values. `#15545 <https://github.com/conan-io/conan/pull/15545>`_ . Docs `here <https://github.com/conan-io/docs/pull/3551>`__
- Fix: Fix `graph build-order --order=configuration` text format output. `#15538 <https://github.com/conan-io/conan/pull/15538>`_
- Fix: Raise a helpful error when the remote is not reachable in case the user wants to work in offline mode. `#15516 <https://github.com/conan-io/conan/pull/15516>`_
- Fix: Avoid missing file stacktrace when no metadata exists for a source backup. `#15501 <https://github.com/conan-io/conan/pull/15501>`_
- Fix: Remove ``--lockfile-packages`` argument, it was not documented as it is was not intended for public usage. `#15499 <https://github.com/conan-io/conan/pull/15499>`_ . Docs `here <https://github.com/conan-io/docs/pull/3536>`__
- Fix: Raise if `check_type=int` and conf value is set to `bool`. `#15378 <https://github.com/conan-io/conan/pull/15378>`_
- Fix: Add `pkg-config` entry to machine file generated by MesonToolchain, due to `pkgconfig` entry being deprecated since Meson 1.3.0. `#15369 <https://github.com/conan-io/conan/pull/15369>`_
- Fix: Fix `graph explain` not showing some differences in requirements if missing. `#15355 <https://github.com/conan-io/conan/pull/15355>`_
- Fix: Fix `tools.info.package_id:confs` when pattern did not match any defined conf. `#15353 <https://github.com/conan-io/conan/pull/15353>`_
- Fix: Fix ``upload_policy=skip`` with ``--build=missing`` issues. `#15336 <https://github.com/conan-io/conan/pull/15336>`_
- Fix: Accept  ``conan download/upload --list=.. --only-recipe`` to download only the recipes. `#15312 <https://github.com/conan-io/conan/pull/15312>`_
- Fix: Allow ``cmake.build(build_type="Release")`` for recipes built with multi-config systems but without ``build_type`` setting. `#14780 <https://github.com/conan-io/conan/pull/14780>`_
- Bugfix: Fix ``MSBuildDeps`` with components and skipped dependencies. `#15626 <https://github.com/conan-io/conan/pull/15626>`_
- Bugfix: Avoid ``provides`` raising an error for packages that self ``tool_requires`` to themselves to cross-build. `#15575 <https://github.com/conan-io/conan/pull/15575>`_
- Bugfix: Fix build scope OS detection in `tools.microsoft.visual.VCVars`. `#15568 <https://github.com/conan-io/conan/pull/15568>`_
- Bugfix: Fix wrong propagation over ``visible=False`` when dependency is header-only. `#15564 <https://github.com/conan-io/conan/pull/15564>`_
- Bugfix: Store the temporary cache folders inside ``core.cache:storage_path``, so ``conan cache clean`` also finds and clean them correctly. `#15505 <https://github.com/conan-io/conan/pull/15505>`_
- Bugfix: The ``conan export-pkg --format=json`` output now returns ``recipe = "cache"`` status, as the recipe is in the cache after the command. `#15504 <https://github.com/conan-io/conan/pull/15504>`_
- Bugfix: The :command:`conan export-pkg` command stores the lockfile excluding the ``test_package``, following the same behavior as :command:`conan create`. `#15504 <https://github.com/conan-io/conan/pull/15504>`_
- Bugfix: Avoid :command:`conan test` failing for ``python_requires`` test-package. `#15485 <https://github.com/conan-io/conan/pull/15485>`_ . Docs `here <https://github.com/conan-io/docs/pull/3537>`__
- Bugfix: MesonToolchain calculates a valid `apple_min_version_flag`. `#15465 <https://github.com/conan-io/conan/pull/15465>`_
- Bugfix: Allow to limit ``os``, ``compiler`` and other settings with subsettings in ``build_id()`` and ``package_id()`` methods. `#15439 <https://github.com/conan-io/conan/pull/15439>`_
- Bugfix: Fix getting environment variable CONAN_LOGIN_USERNAME_REMOTE. `#15388 <https://github.com/conan-io/conan/pull/15388>`_
- Bugfix: Don't take `.` folder into consideration for `tools.files.copy()` `excludes` patterns. `#15349 <https://github.com/conan-io/conan/pull/15349>`_
- Bugfix: Disable creating editables without name and version. `#15337 <https://github.com/conan-io/conan/pull/15337>`_
- Bugfix: Fix `Git.get_url_and_commit` raising for some Git configs. `#15271 <https://github.com/conan-io/conan/pull/15271>`_
- Bugfix: Direct dependencies in the "host" context of packages being built shouldn't be skipped. This allows for non C/C++ libraries artifacts, like images, in the "host" context, to be used as build-time resources. `#15128 <https://github.com/conan-io/conan/pull/15128>`_


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
