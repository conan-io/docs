.. _reference_config_files_global_conf:

global.conf
===========

The **global.conf** file is located in the Conan user home directory, e.g., *[CONAN_HOME]/global.conf*. If it does not
already exist, a default one is automatically created.

Introduction to configuration
-----------------------------

*global.conf* is aimed to save some core/tools/user configuration variables that will be used by Conan. For instance:

* Package ID modes.
* General HTTP(python-requests) configuration.
* Number of retries when downloading/uploading recipes.
* Related tools configurations (used by toolchains, helpers, etc.)
* Others (required Conan version, CLI non-interactive, etc.)

Let's briefly explain the three types of existing configurations:

* ``core.*``: aimed to configure values of Conan core behavior (download retries, package ID modes, etc.).
  Only definable in *global.conf* file.
* ``tools.*``: aimed to configure values of Conan tools (toolchains, build helpers, etc.) used in your recipes.
  Definable in both *global.conf* and :ref:`profiles <reference_config_files_profiles>`.
* ``user.*``: aimed to define personal user configurations. They can define whatever user wants.
  Definable in both *global.conf* and :ref:`profiles <reference_config_files_profiles>`.

To list all the possible configurations available, run :command:`conan config list`:

.. code-block:: text

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
    core:skip_warnings: Do not show warnings in this list
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
    tools.cmake.cmaketoolchain:system_name: Define CMAKE_SYSTEM_NAME in CMakeToolchain
    tools.cmake.cmaketoolchain:system_processor: Define CMAKE_SYSTEM_PROCESSOR in CMakeToolchain
    tools.cmake.cmaketoolchain:system_version: Define CMAKE_SYSTEM_VERSION in CMakeToolchain
    tools.cmake.cmaketoolchain:toolchain_file: Use other existing file rather than conan_toolchain.cmake one
    tools.cmake.cmaketoolchain:toolset_arch: Toolset architecture to be used as part of CMAKE_GENERATOR_TOOLSET in CMakeToolchain
    tools.cmake.cmaketoolchain:user_toolchain: Inject existing user toolchains at the beginning of conan_toolchain.cmake
    tools.cmake:cmake_program: Path to CMake executable
    tools.cmake:install_strip: Add --strip to cmake.instal()
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
    tools.google.bazel:bazelrc_path: Defines Bazel rc-path
    tools.google.bazel:configs: Define Bazel config file
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
    tools.microsoft.msbuild:vs_version: Defines the IDE version when using the new msvc compiler
    tools.microsoft.msbuilddeps:exclude_code_analysis: Suppress MSBuild code analysis for patterns
    tools.microsoft.msbuildtoolchain:compile_options: Dictionary with MSBuild compiler options
    tools.system.package_manager:mode: Mode for package_manager tools: 'check', 'report', 'report-installed' or 'install'
    tools.system.package_manager:sudo: Use 'sudo' when invoking the package manager tools in Linux (False by default)
    tools.system.package_manager:sudo_askpass: Use the '-A' argument if using sudo in Linux to invoke the system package manager (False by default)
    tools.system.package_manager:tool: Default package manager tool: 'apk', 'apt-get', 'yum', 'dnf', 'brew', 'pacman', 'choco', 'zypper', 'pkg' or 'pkgutil'


User/Tools configurations
-------------------------

Tools and user configurations can be defined in both the *global.conf* file and
:ref:`Conan profiles <reference_config_files_profiles_conf>`. They look like:


.. code-block:: text
    :caption: *global.conf*

    tools.build:verbosity=verbose
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10
    # User conf variable
    user.confvar:something=False

.. important::

    Profiles values will have priority over globally defined ones in global.conf.


These are some hints about configuration items scope and naming:

- ``core.xxx`` and ``tools.yyy`` are Conan built-ins, users cannot define their own ones in these scopes.
- ``core.xxx`` can be defined in ``global.conf`` only, but not in profiles.
- ``tools.yyy`` can be defined in ``global.conf``, in profiles ``[conf]`` section and cli ``-c`` arguments
- ``user.zzz`` can be defined everywhere, and they are totally at the user discretion, no established naming convention. However this would be more or less expected:
  - For open source libraries, specially those in conancenter, ``user.packagename:conf`` might be expected, like the ``boost`` recipe defining ``user.boost:conf`` conf
  - For private usage, the recommendation could be to use something like ``user.orgname:conf`` for global org configuration accross all projects, ``user.orgname.project:conf`` for project or package configuration, though ``user.project:conf`` might be also good if the project name is unique enough.


Configuration file template
---------------------------


It is possible to use **jinja2** template engine for *global.conf*. When Conan loads this file, it immediately parses
and renders the template, which must result in a standard tools-configuration text.

  .. code:: jinja

     # Using all the cores automatically
     tools.build:jobs={{os.cpu_count()}}
     # Using the current OS
     user.myconf.system:name = {{platform.system()}}


The Python packages passed to render the template are ``os`` and ``platform`` for all platforms and ``distro`` in Linux platforms.
Additionally, the variables ``conan_version`` and ``conan_home_folder`` are also available.


Configuration data types
------------------------


All the values will be interpreted by Conan as the result of the python built-in `eval()` function:

.. code-block:: text

    # String
    tools.build:verbosity=verbose
    # Boolean
    tools.system.package_manager:sudo=True
    # Integer
    tools.microsoft.msbuild:max_cpu_count=2
    # List of values
    user.myconf.build:ldflags=["--flag1", "--flag2"]
    # Dictionary
    tools.microsoft.msbuildtoolchain:compile_options={"ExceptionHandling": "Async"}


Configuration data operators
----------------------------

It's also possible to use some extra operators when you're composing tool configurations in your *global.conf* or
any of your profiles:

* ``+=`` == ``append``: appends values at the end of the existing value (only for lists).
* ``=+`` == ``prepend``: puts values at the beginning of the existing value (only for lists).
* ``*=`` == ``update``: updates the specified keys only, leaving the rest unmodified (only for dictionaries)
* ``=!`` == ``unset``: gets rid of any configuration value.

.. code-block:: text
    :caption: *global.conf*

    # Define the value => ["-f1"]
    user.myconf.build:flags=["-f1"]

    # Append the value ["-f2"] => ["-f1", "-f2"]
    user.myconf.build:flags+=["-f2"]

    # Prepend the value ["-f0"] => ["-f0", "-f1", "-f2"]
    user.myconf.build:flags=+["-f0"]

    # Unset the value
    user.myconf.build:flags=!

    # Define the value => {"a": 1, "b": 2}
    user.myconf.build:other={"a": 1, "b": 2}

    # Update b = 4 => {"a": 1, "b": 4}
    user.myconf.build:other*={"b": 4}


Configuration patterns
----------------------

You can use package patterns to apply the configuration in those dependencies which are matching:

.. code-block:: text

    *:tools.cmake.cmaketoolchain:generator=Ninja
    zlib:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019

This example shows you how to specify a general ``generator`` for all your packages except for `zlib` which is defining
`Visual Studio 16 2019` as its generator.

Besides that, it's quite relevant to say that **the order matters**. So, if we change the order of the
configuration lines above:

.. code-block:: text

    zlib:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019
    *:tools.cmake.cmaketoolchain:generator=Ninja

The result is that you're specifying a general `generator` for all your packages, and that's it. The `zlib` line has no
effect because it's the first one evaluated, and after that, Conan is overriding that specific pattern with the most
general one, so it deserves to pay special attention to the order.


Information about built-in confs
================================

This section provides extra information about specific confs.

Networking confs
----------------

.. _reference_config_files_global_conf_ssl_certificates:

Configuration of client certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Conan supports client TLS certificates. You can configure the path to your existing *Cacert* file and/or your client
certificate (and the key) using the following configuration variables:

* ``core.net.http:cacert_path``: Path containing a custom Cacert file.
* ``core.net.http:client_cert``: Path or tuple of files containing a client certificate (and the key). See more details in
  `Python requests and Client Side Certificates <https://requests.readthedocs.io/en/latest/user/advanced/#client-side-certificates>`_

For instance:

.. code-block:: text
    :caption: **[CONAN_HOME]/global.conf**

    core.net.http:cacert_path=/path/to/cacert.pem
    core.net.http:client_cert=('/path/client.cert', '/path/client.key')


.. seealso::

    * :ref:`Managing configuration in your recipes (self.conf_info) <conan_conanfile_model_conf_info>`


* ``tools.files.download:verify``: Setting ``tools.files.download:verify=False`` constitutes a security risk if enabled,
  as it disables certificate validation. Do not use it unless you understand the implications
  (And even then, properly scoping the conf to only the required recipes is a good idea)
  or if you are using it for development purposes


UX confs
--------

Skip warnings
~~~~~~~~~~~~~

There are several warnings that Conan outputs in certain cases which can be omitted via the ``core:skip_warnings`` conf,
by adding the warning tag to its value.

Those warnings are:

  - ``deprecated``: Messages for deprecated features such as legacy generators
