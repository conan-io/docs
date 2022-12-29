conan config
============

conan config home
-----------------

.. code-block:: bash

    $  conan config home -h
    usage: conan config home [-h] [-v [V]] [--logger]

    Gets the Conan home folder

    optional arguments:
    -h, --help  show this help message and exit
    -v [V]      Level of detail of the output. Valid options from less verbose to more verbose:
                -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                -vvv or -vtrace
    --logger    Show the output with log format, with time, type and message.


.. code-block:: bash

    $ conan config home


conan config install
--------------------

.. code-block:: bash

    $ conan config install -h
    usage: conan config install [-h] [-v [V]] [--logger] [--verify-ssl [VERIFY_SSL]]
                                [-t {git,dir,file,url}] [-a ARGS] [-sf SOURCE_FOLDER]
                                [-tf TARGET_FOLDER]
                                item

    Installs the configuration (remotes, profiles, conf), from git, http or folder

    positional arguments:
    item                  git repository, local file or folder or zip file (local or http) where
                            the configuration is stored

    optional arguments:
    -h, --help            show this help message and exit
    -v [V]                Level of detail of the output. Valid options from less verbose to more
                            verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or
                            -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.
    --verify-ssl [VERIFY_SSL]
                            Verify SSL connection when downloading file
    -t {git,dir,file,url}, --type {git,dir,file,url}
                            Type of remote config
    -a ARGS, --args ARGS  String with extra arguments for "git clone"
    -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                            Install files only from a source subfolder from the specified origin
    -tf TARGET_FOLDER, --target-folder TARGET_FOLDER
                            Install to that path in the conan cache



The ``conan config install`` command is intended to install in the current home a common shared Conan
configuration, like the definitions of ``remotes``, ``profiles``, ``settings``, ``hooks``, ``extensions``, etc.

The command can use as source any of the following:

- A URL pointing to a zip archive containing the configuration files
- A git repository containing the files
- A local folder
- Just one file

Files in the current Conan home will be replaced by the ones from the installation source.
All the configuration files can be shared and installed this way:

- ``remotes.json`` for the definition of remotes
- Any custom profile files inside a ``profiles`` subfolder
- Custom ``settings.yml``
- Custom ``global.conf``
- All the extensions, including plugins, hooks.
- Custom user commands.


**Examples**:

- Install the configuration from a URL:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip


- Install the configuration from a URL, but only getting the files inside a *origin* folder
  inside the zip file, and putting them inside a *target* folder in the local cache:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip -sf=origin -tf=target

- Install configuration from 2 different zip files from 2 different urls, using different source
  and target folders for each one, then update all:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip -sf=origin -tf=target
      $ conan config install http://url/to/some/config.zip -sf=origin2 -tf=target2
      $ conan config install http://other/url/to/other.zip -sf=hooks -tf=hooks

- Install the configuration from a Git repository with submodules:

  .. code-block:: bash

      $ conan config install http://github.com/user/conan_config/.git --args "--recursive"

  You can also force the git download by using :command:`--type git` (in case it is not deduced from the URL automatically):

  .. code-block:: bash

      $ conan config install http://github.com/user/conan_config/.git --type git

- Install from a URL skipping SSL verification:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip --verify-ssl=False

  This will disable the SSL check of the certificate.

- Install a specific file from a local path:

  .. code-block:: bash

      $ conan config install my_settings/settings.yml

- Install the configuration from a local path:

  .. code-block:: bash

      $ conan config install /path/to/some/config.zip


conan config list
-----------------
.. code-block:: bash

    $ conan config list -h
    usage: conan config list [-h] [-f FORMAT] [-v [V]] [--logger]

    Prints all the Conan available configurations: core and tools.

    optional arguments:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Select the output format: json
    -v [V]                Level of detail of the output. Valid options from less verbose to more
                            verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or
                            -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.


Displays all the Conan built-in configurations. There are 2 groups:

- ``core.xxxx``: These can only be defined in ``global.conf`` and are used by Conan internally
- ``tools.xxxx``: Thesa can be defined both in ``global.conf`` and profiles, and will be used by
  recipes and tools used within recipes, like ``CMakeToolchain``


.. code-block:: bash

    $ conan config list
    core.cache:storage_path: Absolute path where the packages and database are stored
    core.download:download_cache: Define path to a file download cache
    core.download:parallel: Number of concurrent threads to download packages
    core.download:retry: Number of retries in case of failure when downloading from Conan server
    core.download:retry_wait: Seconds to wait between download attempts from Conan server
    core.gzip:compresslevel: The Gzip compresion level for Conan artifacts (default=9)
    core.net.http:cacert_path: Path containing a custom Cacert file
    core.net.http:clean_system_proxy: If defined, the proxies system env-vars will be discarded
    core.net.http:client_cert: Path or tuple of files containing a client cert (and key)
    core.net.http:max_retries: Maximum number of connection retries (requests library)
    core.net.http:no_proxy_match: List of urls to skip from proxies configuration
    core.net.http:proxies: Dictionary containing the proxy configuration
    core.net.http:timeout: Number of seconds without response to timeout (requests library)
    core.package_id:default_build_mode: By default, 'None'
    core.package_id:default_embed_mode: By default, 'full_mode'
    core.package_id:default_non_embed_mode: By default, 'minor_mode'
    core.package_id:default_python_mode: By default, 'minor_mode'
    core.package_id:default_unknown_mode: By default, 'semver_mode'
    core.upload:retry: Number of retries in case of failure when uploading to Conan server
    core.upload:retry_wait: Seconds to wait between upload attempts to Conan server
    core:default_build_profile: Defines the default build profile (None by default)
    core:default_profile: Defines the default host profile ('default' by default)
    core:non_interactive: Disable interactive user input, raises error if input necessary
    core:required_conan_version: Raise if current version does not match the defined range.
    tools.android:ndk_path: Argument for the CMAKE_ANDROID_NDK
    tools.apple.xcodebuild:verbosity: Verbosity level for xcodebuild: 'verbose' or 'quiet
    tools.apple:enable_arc: (boolean) Enable/Disable ARC Apple Clang flags
    tools.apple:enable_bitcode: (boolean) Enable/Disable Bitcode Apple Clang flags
    tools.apple:enable_visibility: (boolean) Enable/Disable Visibility Apple Clang flags
    tools.apple:sdk_path: Path to the SDK to be used
    tools.build.cross_building:can_run: Bool value that indicates whether is possible to run a non-native app on the same architecture. It's used by 'can_run' tool
    tools.build:cflags: List of extra C flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
    tools.build:cxxflags: List of extra CXX flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
    tools.build:defines: List of extra definition flags used by different toolchains like CMakeToolchain and AutotoolsToolchain
    tools.build:exelinkflags: List of extra flags used by CMakeToolchain for CMAKE_EXE_LINKER_FLAGS_INIT variable
    tools.build:jobs: Default compile jobs number -jX Ninja, Make, /MP VS (default: max CPUs)
    tools.build:sharedlinkflags: List of extra flags used by CMakeToolchain for CMAKE_SHARED_LINKER_FLAGS_INIT variable
    tools.build:skip_test: Do not execute CMake.test() and Meson.test() when enabled
    tools.build:sysroot: Pass the --sysroot=<tools.build:sysroot> flag if available. (None by default)
    tools.cmake.cmake_layout:build_folder_vars: Settings and Options that will produce a different build folder and different CMake presets names
    tools.cmake.cmaketoolchain.presets:max_schema_version: Generate CMakeUserPreset.json compatible with the supplied schema version
    tools.cmake.cmaketoolchain:find_package_prefer_config: Argument for the CMAKE_FIND_PACKAGE_PREFER_CONFIG
    tools.cmake.cmaketoolchain:generator: User defined CMake generator to use instead of default
    tools.cmake.cmaketoolchain:system_name: Define CMAKE_SYSTEM_NAME in CMakeToolchain
    tools.cmake.cmaketoolchain:system_processor: Define CMAKE_SYSTEM_PROCESSOR in CMakeToolchain
    tools.cmake.cmaketoolchain:system_version: Define CMAKE_SYSTEM_VERSION in CMakeToolchain
    tools.cmake.cmaketoolchain:toolchain_file: Use other existing file rather than conan_toolchain.cmake one
    tools.cmake.cmaketoolchain:toolset_arch: Toolset architecture to be used as part of CMAKE_GENERATOR_TOOLSET in CMakeToolchain
    tools.cmake.cmaketoolchain:user_toolchain: Inject existing user toolchains at the beginning of conan_toolchain.cmake
    tools.env.virtualenv:powershell: If it is set to True it will generate powershell launchers if os=Windows
    tools.files.download:download_cache: Define the cache folder to store downloads from files.download()/get()
    tools.files.download:retry: Number of retries in case of failure when downloading
    tools.files.download:retry_wait: Seconds to wait between download attempts
    tools.gnu:define_libcxx11_abi: Force definition of GLIBCXX_USE_CXX11_ABI=1 for libstdc++11
    tools.gnu:host_triplet: Custom host triplet to pass to Autotools scripts
    tools.gnu:make_program: Indicate path to make program
    tools.gnu:pkg_config: Path to pkg-config executable used by PkgConfig build helper
    tools.google.bazel:bazelrc_path: Defines Bazel rc-path
    tools.google.bazel:configs: Define Bazel config file
    tools.info.package_id:confs: List of existing configuration to be part of the package ID
    tools.intel:installation_path: Defines the Intel oneAPI installation root path
    tools.intel:setvars_args: Custom arguments to be passed onto the setvars.sh|bat script from Intel oneAPI
    tools.meson.mesontoolchain:backend: Any Meson backend: ninja, vs, vs2010, vs2012, vs2013, vs2015, vs2017, vs2019, xcode
    tools.microsoft.bash:active: If Conan is already running inside bash terminal in Windows
    tools.microsoft.bash:path: The path to the shell to run when conanfile.win_bash==True
    tools.microsoft.bash:subsystem: The subsystem to be used when conanfile.win_bash==True. Possible values: msys2, msys, cygwin, wsl, sfu
    tools.microsoft.msbuild:installation_path: VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community
    tools.microsoft.msbuild:max_cpu_count: Argument for the /m when running msvc to build parallel projects
    tools.microsoft.msbuild:verbosity: Verbosity level for MSBuild: 'Quiet', 'Minimal', 'Normal', 'Detailed', 'Diagnostic'
    tools.microsoft.msbuild:vs_version: Defines the IDE version when using the new msvc compiler
    tools.microsoft.msbuilddeps:exclude_code_analysis: Suppress MSBuild code analysis for patterns
    tools.microsoft.msbuildtoolchain:compile_options: Dictionary with MSBuild compiler options
    tools.system.package_manager:mode: Mode for package_manager tools: 'check' or 'install'
    tools.system.package_manager:sudo: Use 'sudo' when invoking the package manager tools in Linux (False by default)
    tools.system.package_manager:sudo_askpass: Use the '-A' argument if using sudo in Linux to invoke the system package manager (False by default)
    tools.system.package_manager:tool: Default package manager tool: 'apt-get', 'yum', 'dnf', 'brew', 'pacman', 'choco', 'zypper', 'pkg' or 'pkgutil'
    