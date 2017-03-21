.. _changelog:


Changelog
=========

Check https://github.com/conan-io/conan for issues and more details about development, contributors, etc.


0.21.0 (21-March-2017)
-------------------------
- Feature: ``conan info --graph`` or ``--graph=file.html`` will generate a dependency graph representation in dot or html formats.
- Feature: Added better support and tests for Solaris Sparc.
- Feature: custom authenticators are now possible in ``conan_server`` with plugins.
- Feature: extended ``conan info`` command with path information and filter by packages.
- Feature: enabled conditional package binaries removal with ``conan remove`` with query syntax
- Feature: enabled generation and validation of manifests from ``test_package``.
- Feature: allowing ``options`` definitions in profiles
- Feature: new ``RunEnvironment`` helper, that makes easier to run binaries from dependent packages
- Feature: new ``virtualrunenv`` generator that activates environment variable for execution of binaries from installed packages, without requiring ``imports`` of shared libraries.
- Feature: adding new version modes for ABI compatibility definition in ``package_id()``.
- Feature: Extended ``conan new`` command with new option for ``exports_sources`` example recipe.
- Feature: ``CMake`` helper defining parallel builds for gcc-like compilers via ``--jN``, allowing user definition with environment variable and in conan.conf.
- Feature: ``conan profile`` command now show profiles in alphabetical order.
- Feature: extended ``visual_studio`` generator with more information and binary paths for execution with DLLs paths.
- Feature: Allowing relative paths with $PROFILE_DIR place holder in ``profiles``
- Fix: using only file checksums to decide for modified recipe in remote, for possible concurrent builds & uploads.
- Fix: Improved ``--build`` modes management, with better checks and allowing multiple definitions and mixtures of conditions
- Fix: Replaced warning for non-matching OS to one message stating the cross-build
- Fix: local ``conan source`` command (working in user folder) now properly executes the equivalent of ``exports`` functionality
- Fix: Setting command line arguments to cmake command as CMake flags, while using the TARGETS approach. Otherwise, arch flags like -m32 -m64 for gcc were not applied.
- BugFix: fixed ``conan imports`` destination folder issue.
- BugFix: Allowing environment variables with spaces
- BugFix: fix for CMake with targets usage of multiple flags.
- BugFix: Fixed crash of ``cmake_multi`` generator for "multi-config" packages.


0.20.3 (06-March-2017)
-------------------------
- Fix: Added opt-out for ``CMAKE_SYSTEM_NAME`` automatically added when cross-building, causing users
  providing their own cross-build to fail
- BugFix: Corrected usage of ``CONAN_CFLAGS`` instead of ``CONAN_C_FLAGS`` in cmake targets

0.20.2 (02-March-2017)
-------------------------
- Fix: Regression of ``visual_studio``generator using ``%(ExecutablePath)`` instead of ``$(ExecutablePath)``
- Fix: Regression for ``--build=outdated --build=Pkg`` install pattern


0.20.1 (01-March-2017)
-------------------------
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
- Feature: new ``conan config`` command to manage, edit, display ``conan.conf`` entries
- Feature: :ref:`Improvements<building_with_cmake>` to ``CMake`` build helper, now it has ``configure()`` and ``build()`` methods
  for common operations.
- Feature: Improvements to ``SystemPackageTool`` with detection of installed packages, improved 
  implementation, installation of multi-name packages.
- Feature: Unzip with ``tools.unzip`` maintaining permissions (Linux, OSX)
- Feature: ``conan info`` command now allows profiles too
- Feature: new tools ``unix_path()``, ``escape_windows_cmd()``, ``run_in_windows_bash()``, useful
  for autotools projects in Win/MinGW/Msys
- Feature: new context manager ``tools.chdir``, to temporarily change directory.
- Feature: CMake using ``CMAKE_SYSTEM_NAME`` for cross-compiling.
- Feature: Artifactory build-info extraction from traces
- Feature: Attach custom headers to artifacts uploads with an `artifacts.properties` file.
- Feature: allow and copy symlinks while ``conan export``
- Fix: removing quotes in some cmake variables that were generating incorrect builds
- Fix: providing better error messages for non existing binaries, with links to the docs
- Fix: improved error messages if ``tools.patch`` failed
- Fix: adding ``resdirs`` to ``cpp_info`` propagated information, and cmake variables, for directories
  containing resources and other data.
- Fix: printing error messages if a ``--build`` policy doesn't match any package
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
- Bug fix: Fixed issue with ``conan copy`` followed by ``conan upload`` due to the new ``exports_sources``
  feature.
  
  
0.19.0 (31-January-2017)
-------------------------
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
- Feature: new cmake helper macro ``conan_target_link_libraries()``
- Feature: new cmake ``CONAN_EXPORTED`` variable, can be used in CMakeLists.txt to differentiate building
  in the local conan cache as package and building in user space
- Fix: improving the caching of options from ``conan install`` in conaninfo.txt and precedence.
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
-------------------------
- Bug Fix: Handling of transitive private dependencies in modern cmake targets
- Bug Fix: Missing quotes in CMake macro for modern cmake targets
- Bug Fix: Handling LINK_FLAGS in cmake modern targets
- Bug Fix: Environment variables no propagating to test project with test_package command


0.18.0 (3-January-2017)
-------------------------
- Feature: uploads and downloads with **retries** on failures. This helps to avoid having to fully
  rebuild on CI when a network transfer fails
- Feature: added **SCons** generator
- Feature: support for **Python 3.6**, with several fixes. Added Python 3.6 to CI.
- Feature: show package dates in ``conan info`` command
- Feature: new ``cmake_multi`` generator for multi-configuration IDEs like Visual Studio and XCode
- Feature: support for **Visual Studio 2017**, VS-15
- Feature: **FreeBSD** now passes test suite
- Feature: ``conan upload`` showing error messages or URL of remote
- Feature: **wildcard or pattern upload**. Useful to upload multiple packages to a remote.
- Feature: allow defining **settings as environment variables**. Useful for use cases like dockerized builds.
- Feature: improved ``--help`` messages
- Feature: cmake helper tools to launch conan directly from cmake
- Added **code coverage** for code repository
- Fix: conan.io badges when containing dash
- Fix: manifests errors due to generated .pyc files
- Bug Fix: unicode error messages crashes
- Bug Fix: duplicated build of same package binary for private dependencies
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
- Feature: generation of **imports manifest** and ``conan imports --undo`` functionality to remove
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
- Fix: proper automatic use of ``txt`` and ``env`` generators in ``test_package``
- Bug fix: solved problem when uploading python packages that generated .pyc at execution
- Bug fix: crash when duplicate requires were declared in conanfile
- Bug fix: crash with existing imported files with symlinks
- Bug fix: options missing in "copy install command to clipboard" in web


0.16.1 (05-December-2016)
-------------------------
- Solved bug with ``test_package`` with arguments, like scopes.


0.16.0 (19-November-2016)
-------------------------
**Upgrade**: The ``--build=outdated`` feature had a change in the hash computation, it might report
outdated binaries from recipes. You can re-build the binaries or ignore it (if you haven't changed
your recipes without re-generating binaries)

- Feature: **version ranges**. Conan now supports defining requirements with version range expressions
  like ``Pkg/[>1.2,<1.9||1.0.1]@user/channel``. Check the :ref:`version ranges reference <version_ranges>` for details
- Feature: decoupled ``imports`` from normal install. Now ``conan install --no-imports`` skips the
  imports section.
- Feature: new ``conan imports`` command that will execute the imports section without running install
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
- Fix: Several fixes in ``conan search``, both local and in remotes
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
reset your local cache. You could manually remove packages or just run ``conan remove "*"``

- Feature: New ``--build=outdated`` functionality, that allows to build the binary packages for
  those dependencies whose recipe has been changed, or if the binary is not existing. Each
  package binary stores a hash of the recipe to know if they have to be regenerated (are outdated).
  This information is also provided in the ``conan search <ref>`` command. Useful for package
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
- Automatic generation of ``conanenv.txt`` in local cache, warnings if using local commands and no
  ``conanbuildinfo.txt`` and no ``conanenv.txt`` are present to cache the information form install
- Fix: Fixed bug when using empty initial requirements (``requires = ""``)
- Fix: Added ``glob`` hidden import to pyinstaller
- Fix: Fixed minor bugs with ``short_paths`` as local search not listing packages
- Fix: Fixed problem with virtual envs in Windows with paths separator (using / instead of \)
- Fix: Fixed parsing of conanbuildinfo.txt, so the root folder for each dependency is available in local
  commands too
- Fix: Fixed bug in ``test_package`` with the test project using the ``requirements()`` method.



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
  added, and shared. Use them with ``$ conan install --profile=name``
- Feature: ``short_paths`` feature for Windows now also handle long paths for the final package,
  in case that a user library has a very long final name, with nested subfolders.
- Feature: Added ``tools.cpu_count()`` as a helper to retrieve the number of cores, so it can be
  used in concurrent builds
- Feature: Detects cycles in the dependency graph, and raise error instead of exhausting recursion
  limits
- Feature: Conan learned the ``--werror`` option that will raise error and stop installation under
  some cases treated as warnings otherwise: Duplicated dependencies, or dependencies conflicts
- Feature: New ``env`` generator that generates a text file with the environment variables defined
  by dependencies, so it can be stored. Such file is parsed by ``$ conan build`` to be able to use
  such environment variables for ``self.deps_env_info`` too, in the same way it uses the ``txt``
  generator to load variables for ``self.deps_cpp_info``.
- Fix: Do not print progress bars when output is a file
- Fix: Improved the local conan search, using options too in the query ``conan search -q option=value``
- Fix: Boto dependency updated to 2.43.0 (necessary for ArchLinux)
- Fix: Simplified the ``conan package`` command, removing unused and confusing options, and more
  informative messages about errors and utility of this command.
- Fix: More fixes and improvements on ``ConfigureEnvironment``, mainly for Windows
- Fix: Conan now does not generate a ``conanbuildinfo.txt`` file when doing ``$ conan install <PkgRef>``
- Bug fix: Files of a package recipe are "touched" to update their timestamps to current time when
  retrieved, otherwise some build systems as Ninja can have problems with them.
- Bug fix: ``qmake`` generator now uses quotes to handle paths with spaces
- Bug fix: Fixed ``OSInfo`` to return the short distro name instead of the long one.
- Bug fix: fixed transitivy of ```private`` dependencies


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
has been addressed by conan 0.13. It affects to third level (and higher) package binaries, i.e. A
and B in A->B->C->D, which binaries **must** be regenerated for the new hashes. If you don't plan
to provide support for older conan releases (<=0.12), which would be reasonable, you should remove
all binaries first (``conan remove -p``, works both locally and remotely), then re-build your binaries.

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
- New command ``conan source`` that executes the ``source()`` method of a given conanfile. Very
  useful for CI, if desired to run in parallel the construction of different binaries.
- New propagation of ``cpp_info``, so it now allows for capturing binary package libraries with new
  ``collect_libs()`` helper, and access to created binaries to compute the ``package_info()`` in general.
- Command ``test_package`` now allows the ``--update`` option, to automatically update dependencies.
- Added new architectures for ``ppc64le`` and detection for ``AArch64``
- New methods for defining requires effect over binary package ID (hash) in ``conan_info()``
- Many bugs fixes: error in ``tools.download`` with python 3, restore correct prompt in virtualenvs,
  bug if removing an option in ``config_options()``, setup.py bug...
  
This release has contributions from @tru, @raulbocanegra, @tivek, @mathieu, and the feedback of many
other conan users, thanks very much to all of them!



0.12.0 (13-September-2016)
--------------------------
- Major changes to **search** api and commands. Decoupled the search of package recipes, from the
  search of package binaries.
- Fixed bug that didn't allow to ``export`` or ``upload`` packages with settings restrictions if the
  restrictions didn't match the host settings
- Allowing disabling color output with ``CONAN_COLOR_DISPLAY=0`` environment variable, or to configure
  color schema for light console backgrounds with ``CONAN_COLOR_DARK=1`` environment variable
- Imports can use absolute paths, and files copied from local conan cache to those paths will not
  be removed when ``conan install``. Can be used as a way to install machine-wise things (outside
  conan local cache)
- More robust handling of failing transfers (network disconnect), and inconsistent status after such
- Large internal refactor for storage managers. Improved implementations and decoupling between
  server and client
- Fixed slow ``conan remove`` for caches with many packages due to slow deletion of empty folders
- Always allowing explicit options scopes, ``- o Package:option=value`` as well as the implicit
  ``-o option=value`` for current ``Package``, for consistency
- Fixed some bugs in client-server auth process.
- Allow to extract ``.tar`` files in ``tools.unzip()``
- Some helpers for ``conan_info()``, as ``self.info.requires.clear()`` and removal of settings and options


0.11.1 (31-August-2016)
-----------------------
- New error reporting for failures in conanfiles, including line number and offending line, much
  easier for package creators
- Removed message requesting to create an account in ``conan.io`` for other remotes
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
- New per-package **build_policy**, which can be set to ``always`` or ``missing``, so it is not
  necessary to create packages or specify the ``--build`` parameter in command line. Useful for example
  in header only libraries or to create packages that always get the latest code from a branch in a github
  repository.
- Command ``conan test_package`` now executes by default a ``conan export`` with smarter package
  reference deduction. It is introduced as opt-out behavior.
- Conan ``export`` command avoids copying ``test_package/build`` temporary files in case of ``export=*``
- Now, ``package_info()`` allows absolute paths in ``includedir``, ``libdirs`` and ``bindirs``, so
  wrapper packages can be defined that use system or manually installed libraries.
- LDFLAGS in ``ConfigureEnvironment`` management of OSX frameworks.
- Options allow the ``ANY`` value, so such option would accept any value. For example a commit of a
  git repository, useful to create packages that can build any specific commit of a git repo.
- Added gcc 5.4 to the default settings, as well as MinGW options (Exceptions, threads...)
- Command ``conan info`` learned a new option to output the packages from a project dependency tree that
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
- Now, running a ``conan install MyLib/0.1@user/channel`` to directly install packages without any
  consuming project, is also able to generate files with the ``-g`` option. Useful for installing
  tool packages (MinGW, CMake) and generate ``virtualenvs``.
- Many small fixes and improvements: detect compiler bug in Py3, search was crashing for remotes,
  conan new failed if the package name had a dash, etc.
- Improved some internal duplications of code, refactored many tests. 

This has been a big release. Practically 100% of the released features are thanks to active users
feedback and contributions. Thanks very much again to all of them!



0.10.0 (29-June-2016)
---------------------
- **conan new** command, that creates conan package conanfile.py templates, with a ``test_package`` package test (-t option),
  also for header only packages (-i option)
- Definition of **scopes**. There is a default **dev** scope for the user project, but any other scope (test, profile...) can be defined and used in packages. They can be used to fire extra processes (as running tests), but they do not affect the package binares, and are not included in the package IDs (hash).
- Definition of **dev_requires**. Those are requirements that are only retrieved when the package is in **dev** scope, otherwise they are not. They do not affect the package binaries. Typical use cases would be test libraries or build scripts.
- Allow **shorter paths** for specific packages, which can be necessary to build packages with very long path names (e.g. Qt) in Windows.
- Support for bzip2 and gzip decompression in ``tools``
- Added ``package_folder`` attribute to conanfile, so the ``package()`` method can for example call ``cmake install`` to create the package.
- Added ``CONAN_CMAKE_GENERATOR`` environment variable that allows to override the ``CMake`` default generator. That can be useful to build with Ninja instead of the default Unix Makefiles
- Improved ``ConfigureEnvironment`` with include paths in CFLAGS and CPPFLAGS, and fixed bug.
- New ``conan user --clean`` option, to completely remove all user data for all remotes.
- Allowed to raise ``Exceptions`` in ``config()`` method, so it is easier for package creators to raise under non-supported configurations
- Fixed many small bugs and other small improvements

As always, thanks very much to all contributors and users providing feedback.

0.9.2 (11-May-2016)
-------------------
- **Fixed download bug** that made it specially slow to download, even crash. Thanks to github @melmdk for fixing it.
- **Fixed cmake check of CLang**, it was being skipped
- **Improved performance**. Check for updates has been removed from install, made it opt-in in ``conan info`` command, as it
  was very slow, seriously affecting performance of large projects.
- Improved internal representation of graph, also improves performance for large projects.
- Fixed bug in ``conan install --update``


0.9 (3-May-2016)
----------------

- **Python 3** "experimental" support. Now the main conan codebase is Python 2 and 3 compatible. 
  Python 2 still the reference platform, Python 3 stable support in next releases.
- Create and share your **own custom generators for any build system or tool**. With "generator packages",
  you can write a generator just as any other package, upload it, modify and version it, etc. Require
  them by reference, as any other package, and pull it into your projects dynamically.
- **Premake4** initial experimental support via a generator package. Check https://www.conan.io/source/PremakeGen/0.1/memsharded/testing
- Very large **re-write of the documentation**. New "creating packages" sections with in-source and out-source explicit examples.
  Please read it! :)
- Improved ``conan test``. Renamed ``test`` to ``test_package`` both for the command and the folder,
  but backwards compatibility remains. Custom folder name also possible. 
  **Adapted test layout** might require minor changes to your package test, 
  automatic warnings added for your convenience.
- Upgraded pyinstaller to generate binary OS installers from 2.X to 3.1
- ``conan search`` now has command line options:, less verbose, verbose, extra verbose
- Added variable with full list of dependencies in conanbuildinfo.cmake
- Several minor bugfixes (check github issues)
- Improved ``conan user`` to manage user login to multiple remotes


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
  in ``conan info`` command too. Also, it keeps different user logins for different remotes, to
  improve support in corporate environments running in-house servers.
- New **update** functionality. Now it is possible to ``conan install --update`` to update packages
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

- Custom conanfile names are allowed for developing. With ``--file`` option you can define
  the file you want to use, allowing for ``.conaninfo.txt`` or having multiple ``conanfile_dev.py``,
  ``conanfile_test.py`` besides the standard ``conanfile.py`` which is used for sharing the package.
  Inheritance is allowed, e.g. ``conanfile_dev.py`` might extend/inherit from ``conanfile.py``.
- New ``conan copy`` command that can be used to copy/rename packages, promote them between channels,
  forking other users packages.
- New ``--all`` and ``--package`` options for ``conan install`` that allows to download one, several,
  or all package configurations for a given reference.
- Added ``patch()`` tool to easily patch sources if necessary.
- New **qmake** and **qbs** generators
- Upload of conanfile **exported** files is also **tgz'd**, allowing fast upload/downloads of
  full sources if desired, avoiding retrieval of sources from externals sources.
- ``conan info`` command improved showing info of current project too
- Output of ``run()`` can be redirected to buffer string for processing, or even removed.
- Added **proxy** configuration to conan.conf for users behinds proxies.
- Large improvements in commands output, prefixed with package reference, and much clear.
- Updated settings for more versions of gcc and new arm architectures
- Treat dependencies includes as SYSTEM in cmake, so no warnings are raised
- Deleting source folder after ``conan export`` so no manual removal is needed
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
  same project, so you can switch between them without having to ``conan install`` again. Check :ref:`the new workflows<workflows>`
- New qmake generator (thanks @dragly)
- Improved removal/deletion of folders with shutil.rmtree, so ``conan remove`` commands and other
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
  


