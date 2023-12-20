.. code-block:: text

    $ conan config list

    core.cache:storage_path: Absolute path where the packages and database are stored
    core.download:download_cache: Define path to a file download cache
    core.download:parallel: Number of concurrent threads to download packages
    core.download:retry: Number of retries in case of failure when downloading from Conan server
    core.download:retry_wait: Seconds to wait between download attempts from Conan server
    core.gzip:compresslevel: The Gzip compression level for Conan artifacts (default=9)
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
    core.sources:download_cache: Folder to store the sources backup
    core.sources:download_urls: List of URLs to download backup sources from
    core.sources:exclude_urls: URLs which will not be backed up
    core.sources:upload_url: Remote URL to upload backup sources to
    core.upload:retry: Number of retries in case of failure when uploading to Conan server
    core.upload:retry_wait: Seconds to wait between upload attempts to Conan server
    core.version_ranges:resolve_prereleases: Whether version ranges can resolve to pre-releases or not
    core:allow_uppercase_pkg_names: Temporarily (will be removed in 2.X) allow uppercase names
    core:default_build_profile: Defines the default build profile ('default' by default)
    core:default_profile: Defines the default host profile ('default' by default)
    core:non_interactive: Disable interactive user input, raises error if input necessary
    core:required_conan_version: Raise if current version does not match the defined range.
    core:skip_warnings: Do not show warnings matching any of the patterns in this list. Current warning tags are 'network', 'deprecated'
    core:warnings_as_errors: Treat warnings matching any of the patterns in this list as errors and then raise an exception. Current warning tags are 'network', 'deprecated'
    tools.android:cmake_legacy_toolchain: Define to explicitly pass ANDROID_USE_LEGACY_TOOLCHAIN_FILE in CMake toolchain
    tools.android:ndk_path: Argument for the CMAKE_ANDROID_NDK
    tools.apple:enable_arc: (boolean) Enable/Disable ARC Apple Clang flags
    tools.apple:enable_bitcode: (boolean) Enable/Disable Bitcode Apple Clang flags
    tools.apple:enable_visibility: (boolean) Enable/Disable Visibility Apple Clang flags
    tools.apple:sdk_path: Path to the SDK to be used
    tools.build.cross_building:can_run: Bool value that indicates whether is possible to run a non-native app on the same architecture. It's used by 'can_run' tool
    tools.build:cflags: List of extra C flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
    tools.build:compiler_executables: Defines a Python dict-like with the compilers path to be used. Allowed keys {'c', 'cpp', 'cuda', 'objc', 'objcxx', 'rc', 'fortran', 'asm', 'hip', 'ispc'}
    tools.build:cxxflags: List of extra CXX flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
    tools.build:defines: List of extra definition flags used by different toolchains like CMakeToolchain and AutotoolsToolchain
    tools.build:download_source: Force download of sources for every package
    tools.build:exelinkflags: List of extra flags used by CMakeToolchain for CMAKE_EXE_LINKER_FLAGS_INIT variable
    tools.build:jobs: Default compile jobs number -jX Ninja, Make, /MP VS (default: max CPUs)
    tools.build:linker_scripts: List of linker script files to pass to the linker used by different toolchains like CMakeToolchain, AutotoolsToolchain, and MesonToolchain
    tools.build:sharedlinkflags: List of extra flags used by CMakeToolchain for CMAKE_SHARED_LINKER_FLAGS_INIT variable
    tools.build:skip_test: Do not execute CMake.test() and Meson.test() when enabled
    tools.build:sysroot: Pass the --sysroot=<tools.build:sysroot> flag if available. (None by default)
    tools.build:verbosity: Verbosity of build systems if set. Possible values are 'quiet' and 'verbose'
    tools.cmake.cmake_layout:build_folder_vars: Settings and Options that will produce a different build folder and different CMake presets names
    tools.cmake.cmaketoolchain:find_package_prefer_config: Argument for the CMAKE_FIND_PACKAGE_PREFER_CONFIG
    tools.cmake.cmaketoolchain:generator: User defined CMake generator to use instead of default
    tools.cmake.cmaketoolchain:presets_environment: String to define wether to add or not the environment section to the CMake presets. Empty by default, will generate the environment section in CMakePresets. Can take values: 'disabled'.
    tools.cmake.cmaketoolchain:system_name: Define CMAKE_SYSTEM_NAME in CMakeToolchain
    tools.cmake.cmaketoolchain:system_processor: Define CMAKE_SYSTEM_PROCESSOR in CMakeToolchain
    tools.cmake.cmaketoolchain:system_version: Define CMAKE_SYSTEM_VERSION in CMakeToolchain
    tools.cmake.cmaketoolchain:toolchain_file: Use other existing file rather than conan_toolchain.cmake one
    tools.cmake.cmaketoolchain:toolset_arch: Toolset architecture to be used as part of CMAKE_GENERATOR_TOOLSET in CMakeToolchain
    tools.cmake.cmaketoolchain:user_toolchain: Inject existing user toolchains at the beginning of conan_toolchain.cmake
    tools.cmake:cmake_program: Path to CMake executable
    tools.cmake:install_strip: Add --strip to cmake.install()
    tools.compilation:verbosity: Verbosity of compilation tools if set. Possible values are 'quiet' and 'verbose'
    tools.deployer:symlinks: Set to False to disable deployers copying symlinks
    tools.env.virtualenv:powershell: If it is set to True it will generate powershell launchers if os=Windows
    tools.files.download:retry: Number of retries in case of failure when downloading
    tools.files.download:retry_wait: Seconds to wait between download attempts
    tools.files.download:verify: If set, overrides recipes on whether to perform SSL verification for their downloaded files. Only recommended to be set while testing
    tools.gnu:define_libcxx11_abi: Force definition of GLIBCXX_USE_CXX11_ABI=1 for libstdc++11
    tools.gnu:host_triplet: Custom host triplet to pass to Autotools scripts
    tools.gnu:make_program: Indicate path to make program
    tools.gnu:pkg_config: Path to pkg-config executable used by PkgConfig build helper
    tools.google.bazel:bazelrc_path: List of paths to bazelrc files to be used as 'bazel --bazelrc=rcpath1 ... build'
    tools.google.bazel:configs: List of Bazel configurations to be used as 'bazel build --config=config1 ...'
    tools.graph:skip_binaries: Allow the graph to skip binaries not needed in the current configuration (True by default)
    tools.info.package_id:confs: List of existing configuration to be part of the package ID
    tools.intel:installation_path: Defines the Intel oneAPI installation root path
    tools.intel:setvars_args: Custom arguments to be passed onto the setvars.sh|bat script from Intel oneAPI
    tools.meson.mesontoolchain:backend: Any Meson backend: ninja, vs, vs2010, vs2012, vs2013, vs2015, vs2017, vs2019, xcode
    tools.meson.mesontoolchain:extra_machine_files: List of paths for any additional native/cross file references to be appended to the existing Conan ones
    tools.microsoft.bash:active: If Conan is already running inside bash terminal in Windows
    tools.microsoft.bash:path: The path to the shell to run when conanfile.win_bash==True
    tools.microsoft.bash:subsystem: The subsystem to be used when conanfile.win_bash==True. Possible values: msys2, msys, cygwin, wsl, sfu
    tools.microsoft.msbuild:installation_path: VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community. Use empty string to disable
    tools.microsoft.msbuild:max_cpu_count: Argument for the /m when running msvc to build parallel projects
    tools.microsoft.msbuild:vs_version: Defines the IDE version (15, 16, 17) when using the msvc compiler. Necessary if compiler.version specifies a toolset that is not the IDE default
    tools.microsoft.msbuilddeps:exclude_code_analysis: Suppress MSBuild code analysis for patterns
    tools.microsoft.msbuildtoolchain:compile_options: Dictionary with MSBuild compiler options
    tools.microsoft:winsdk_version: Use this winsdk_version in vcvars
    tools.system.package_manager:mode: Mode for package_manager tools: 'check', 'report', 'report-installed' or 'install'
    tools.system.package_manager:sudo: Use 'sudo' when invoking the package manager tools in Linux (False by default)
    tools.system.package_manager:sudo_askpass: Use the '-A' argument if using sudo in Linux to invoke the system package manager (False by default)
    tools.system.package_manager:tool: Default package manager tool: 'apk', 'apt-get', 'yum', 'dnf', 'brew', 'pacman', 'choco', 'zypper', 'pkg' or 'pkgutil'
