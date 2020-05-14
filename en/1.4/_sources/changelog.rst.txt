.. _changelog:

Changelog
=========

Check https://github.com/conan-io/conan for issues and more details about development, contributors, etc.


.. important::

  Conan 1.4 shouldn't break any existing 1.0 recipe, or command line invocation. If it does, please report in github.
  Please read more :ref:`about Conan stability<stability>`.


1.4.5 (22-June-2018)
--------------------

- Bugfix: The package_id recipe method was being called twice causing issues with info objects being populated with wrong information.


1.4.4 (11-June-2018)
--------------------

- Bugfix: Fix link order with private requirements.
- Bugfix: Removed duplicate `-std` flag in CMake < 3 or when the standard is not yet supported by `CMAKE_CXX_STANDARD`.
- Bugfix: Check `scm` attribute to avoid breaking recipes with already defined one.
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

- Bugfix: Solved issue with symlinks making recipes to fail with `self.copy`.
- Bugfix: Fixed c++20 standard usage with modern compilers and the creation of the ``settings.yml`` containing the settings values.
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
- Bugfix: Fixed string scaping in CMake files for preprocessor definitions.
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
- Bufix:  Flags for Visual Studio command (cl.exe) using "-" instead of "/" to avoid problems in builds using AutoTools scripts with Visual Studio compiler.
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
- Feature: Added ``CONAN_SKIP_VS_PROJECTS_UPGRADE`` environment variable to skip the upgrade of Visual Studio project when using :ref:`build_sln_commmand<build_sln_commmand>`, the :ref:`msvc_build_command<msvc_build_command>` and the :ref:`MSBuild()<msbuild>` build helper.
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
- Fix: ``CMake()`` helper do not require settins if ``CONAN_CMAKE_GENERATOR`` is defined.
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
- Bugfix: Correct use of unix paths in Windows subsystems (msys, cygwing) when needed.
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

- Feature: ``run_in_windows_bash`` accepts a dict of environment variables to be prioritised inside the bash shell, mainly intended to control the priority of the tools in the path. Use with ``vcvars`` context manager and ``vcvars_dict``, that returns the PATH environment variable only with the Visual Studio related directories 
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
-------------------------

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
- Feature: Autodected MSYS2 for ``SystemPackageTool``
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
- Fix: Do not crete local conaninfo.txt file for :command:`conan install <pkg-ref>` commands.
- Fix: Solved issue with multiple repetitions of the same command line argument
- BugFix: Don't rebuild conan created (with conan-create) packages when ``build_policy="always"``
- BugFix: :command:`conan copy` was always copying binaries, now can copy only recipes
- BugFix: A bug in download was causing appends insteads of overwriting for repeated downloads.
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
- Development: Several internal refactors (tools module, installer), testing (using VS2015 as default, removing VS 12 in testing). Conditional CI in travis for faster builds in developers, downgrading to CMake 3.7 in appveyor
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
- Refactor: internal refactors toward having a python api to conan functionality


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
- BugFix: Clean crash and improved error messages when manifests mistmatch exists in conan upload.


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
- Feature: new ``cmake_multi`` generator for multi-configuration IDEs like Visual Studio and XCode
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
- Bug fix: fixed transitivy of ``private`` dependencies


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
  started to have issues for huge packages (>many hundreds Mbs), that sometimes could be alleviated
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
  most use cases. This removes a nasty behaviour of having the ``config()`` method called twice with 
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
- Definition of **scopes**. There is a default **dev** scope for the user project, but any other scope (test, profile...) can be defined and used in packages. They can be used to fire extra processes (as running tests), but they do not affect the package binares, and are not included in the package IDs (hash).
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

- Fixed linker problems with the new apple-clang 7.3 due to libraries with no setted timestamp.
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
- The OSX installer, problematic with latest OSX releases, has been deprecated in favour
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
