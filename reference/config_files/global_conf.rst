.. _reference_config_files_global_conf:

global.conf
===========

The **global.conf** file is located in the Conan user home directory, e.g., *[CONAN_HOME]/global.conf*.

Introduction to configuration
-----------------------------

*global.conf* is aimed to save some core/tools configuration variables that will be used by Conan. For instance:

* Package ID modes.
* General HTTP(python-requests) configuration.
* Number of retries when downloading/uploading recipes.
* Related tools configurations (used by toolchains, helpers, etc.)
* Others (required Conan version, CLI non-interactive, etc.)


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
    core.upload:retry: Number of retries in case of failure when uploading to Conan server
    core.upload:retry_wait: Seconds to wait between upload attempts to Conan server
    core:allow_uppercase_pkg_names: Temporarily (will be removed in 2.X) allow uppercase names
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
    tools.meson.mesontoolchain:extra_machine_files: List of paths for any additional native/cross file references to be appended to the existing Conan ones
    tools.microsoft.bash:active: If Conan is already running inside bash terminal in Windows
    tools.microsoft.bash:path: The path to the shell to run when conanfile.win_bash==True
    tools.microsoft.bash:subsystem: The subsystem to be used when conanfile.win_bash==True. Possible values: msys2, msys, cygwin, wsl, sfu
    tools.microsoft.msbuild:installation_path: VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community. Use empty string to disable
    tools.microsoft.msbuild:max_cpu_count: Argument for the /m when running msvc to build parallel projects
    tools.microsoft.msbuild:verbosity: Verbosity level for MSBuild: 'Quiet', 'Minimal', 'Normal', 'Detailed', 'Diagnostic'
    tools.microsoft.msbuild:vs_version: Defines the IDE version when using the new msvc compiler
    tools.microsoft.msbuilddeps:exclude_code_analysis: Suppress MSBuild code analysis for patterns
    tools.microsoft.msbuildtoolchain:compile_options: Dictionary with MSBuild compiler options
    tools.system.package_manager:mode: Mode for package_manager tools: 'check' or 'install'
    tools.system.package_manager:sudo: Use 'sudo' when invoking the package manager tools in Linux (False by default)
    tools.system.package_manager:sudo_askpass: Use the '-A' argument if using sudo in Linux to invoke the system package manager (False by default)
    tools.system.package_manager:tool: Default package manager tool: 'apt-get', 'yum', 'dnf', 'brew', 'pacman', 'choco', 'zypper', 'pkg' or 'pkgutil'


.. important::

    Remember to run that command locally to actually see the latest list because this one may be outdated.


Tools configurations
--------------------

Tools and user configurations allows them to be defined both in the *global.conf* file and in profile files. Profile values will
have priority over globally defined ones in *global.conf*, and can be defined as:

.. code-block:: text
    :caption: profile (not global.conf)

    [settings]
    ...

    [conf]
    tools.microsoft.msbuild:verbosity=Diagnostic
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10


Configuration file template
---------------------------


It is possible to use **jinja2** template engine for *global.conf*. When Conan loads this file, immediately parses
and renders the template, which must result in a standard tools-configuration text.

  .. code:: jinja

     # Using all the cores automatically
     tools.build:jobs={{os.cpu_count()}}
     # Using the current OS
     user.myconf.system:name = {{platform.system()}}


The Python packages passed to render the template are ``os`` and ``platform`` for all platforms and ``distro`` in Linux platforms.


Configuration data types
------------------------


All the values will be interpreted by Conan as the result of the python built-in `eval()` function:

.. code-block:: text

    # String
    tools.microsoft.msbuild:verbosity=Diagnostic
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
* ``=!`` == ``unset``: gets rid of any configuration value.

.. code-block:: text
    :caption: *myprofile*

    [settings]
    ...

    [conf]
    # Define the value => ["-f1"]
    user.myconf.build:flags=["-f1"]

    # Append the value ["-f2"] => ["-f1", "-f2"]
    user.myconf.build:flags+=["-f2"]

    # Prepend the value ["-f0"] => ["-f0", "-f1", "-f2"]
    user.myconf.build:flags=+["-f0"]

    # Unset the value
    user.myconf.build:flags=!


Configuration in your profiles
--------------------------------

Let's see a little bit more complex example trying different configurations coming from the *global.conf* and a simple profile:

.. code-block:: text
    :caption: *global.conf*

    # Defining several lists
    user.myconf.build:ldflags=["--flag1 value1"]
    user.myconf.build:cflags=["--flag1 value1"]


.. code-block:: text
    :caption: *myprofile*

    [settings]
    ...

    [conf]
    # Appending values into the existing list
    user.myconf.build:ldflags+=["--flag2 value2"]

    # Unsetting the existing value (it'd be like we define it as an empty value)
    user.myconf.build:cflags=!

    # Prepending values into the existing list
    user.myconf.build:ldflags=+["--prefix prefix-value"]


Running, for instance, :command:`conan install . -pr myprofile`, the configuration output will be something like:

.. code-block:: bash

    ...
    Configuration:
    [settings]
    [options]
    [tool_requires]
    [conf]
    user.myconf.build:cflags=!
    user.myconf.build:ldflags=['--prefix prefix-value', '--flag1 value1', '--flag2 value2']
    ...


Configuration patterns
----------------------

You can use package patterns to apply the configuration in those dependencies which are matching:

.. code-block:: text

    *:tools.cmake.cmaketoolchain:generator=Ninja
    zlib:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019

This example shows you how to specify a general `generator` for all your packages, but for `zlib` one. `zlib` is defining
`Visual Studio 16 2019` as its own generator.

Besides that, it's quite relevant to say that **the order matters**. So, if we change the order of the
configuration lines above:

.. code-block:: text

    zlib:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019
    *:tools.cmake.cmaketoolchain:generator=Ninja

The result is that you're specifying a general `generator` for all your packages, and that's it. The `zlib` line has no
effect because it's the first one evaluated, and after that, Conan is overriding that specific pattern with the most
general one, so it deserves to pay special attention to the order.


.. _conf_in_recipes:

Configuration in your recipes
-------------------------------

From Conan 1.46, the user interface to manage the configurations in your recipes has been improved. The ``self.conf_info``
object has the following methods available:

* ``get(name, default=None, check_type=None)``: gets the value for the given configuration name. Besides that you can pass
  ``check_type`` to check the Python type matches with the value type returned, e.g., ``check_type=list``. If the configuration
  does not exist, ``default`` will be returned instead. Notice that this ``default`` value won't be affected by the ``check_type=list`` param.
* ``pop(name, default=None)``: removes (if exists) the configuration name given. If the configuration does not exist,
  ``default`` will be returned instead.
* ``define(name, value)``: sets ``value`` for the given configuration name. If it already exists, the configuration will be
  overwritten with the new value.
* ``append(name, value)``: (only available for ``list``) appends ``value`` into the existing list for the given configuration name. If the list does not
  exist yet, it'll be created with the value given by default. ``value`` can be a list or a single value.
* ``prepend(name, value)``: (only available for ``list``) prepends ``value`` into the existing list for the given configuration name. If the list does not
  exist yet, it'll be created with the value given by default. ``value`` can be a list or a single value.
* ``update(name, value)``: (only available for ``dict``) updates the existing dictionary with ``value`` for the given configuration name. If the dict does not
  exist yet, it'll be created with the value given by default. ``value`` must be another dictionary.
* ``remove(name, value)``: (only available for ``dict`` and ``list``) removes ``value`` from the existing value for the given configuration name.
* ``unset(name)``: removes any existing value for the given configuration name. It's behaving like using ``define(name, None)``.

This example illustrates all of these methods:

.. code-block:: python

    import os
    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"

        def package_info(self):
            # Setting values
            self.conf_info.define("tools.microsoft.msbuild:verbosity", "Diagnostic")
            self.conf_info.define("tools.system.package_manager:sudo", True)
            self.conf_info.define("tools.microsoft.msbuild:max_cpu_count", 2)
            self.conf_info.define("user.myconf.build:ldflags", ["--flag1", "--flag2"])
            self.conf_info.define("tools.microsoft.msbuildtoolchain:compile_options", {"ExceptionHandling": "Async"})
            # Getting values
            self.conf_info.get("tools.microsoft.msbuild:verbosity")  # == "Diagnostic"
            # Getting default values from configurations that don't exist yet
            self.conf_info.get("user.myotherconf.build:cxxflags", default=["--flag3"])  # == ["--flag3"]
            # Getting values and ensuring the gotten type is the passed one otherwise an exception will be raised
            self.conf_info.get("tools.system.package_manager:sudo", check_type=bool)  # == True
            self.conf_info.get("tools.system.package_manager:sudo", check_type=int)  # ERROR! It raises a ConanException
            # Modifying configuration list-like values
            self.conf_info.append("user.myconf.build:ldflags", "--flag3")  # == ["--flag1", "--flag2", "--flag3"]
            self.conf_info.prepend("user.myconf.build:ldflags", "--flag0")  # == ["--flag0", "--flag1", "--flag2", "--flag3"]
            # Modifying configuration dict-like values
            self.conf_info.update("tools.microsoft.msbuildtoolchain:compile_options", {"ExpandAttributedSource": "false"})
            # Unset any value
            self.conf_info.unset("tools.microsoft.msbuildtoolchain:compile_options")
            # Remove
            self.conf_info.remove("user.myconf.build:ldflags", "--flag1")  # == ["--flag0", "--flag2", "--flag3"]
            # Removing completely the configuration
            self.conf_info.pop("tools.system.package_manager:sudo")


.. important::

    Legacy configuration methods to set/get values like ``self.conf_info["xxxxx"] = "yyyyy"`` and ``v = self.conf_info["xxxxx"]`` are
    deprecated since Conan 1.46 version. Use ``self.conf_info.define("xxxxx", "yyyyy")`` and ``v = self.conf_info.get("xxxxx")`` instead
    like the example above.


Configuration from build_requires
---------------------------------

From Conan 1.37, it is possible to define configuration in packages that are ``build_requires``. For example, assuming
there is a package that bundles the AndroidNDK, it could define the location of such NDK to the ``tools.android:ndk_path``
configuration as:


.. code-block:: python

    import os
    from conan import ConanFile

    class Pkg(ConanFile):
        name = "android_ndk"

        def package_info(self):
            self.conf_info.define("tools.android:ndk_path", os.path.join(self.package_folder, "ndk"))


Note that this only propagates from the immediate, direct ``build_requires`` of a recipe.


Configuration of client certificates
------------------------------------

Conan supports client TLS certificates. You can configure the path to your existing *Cacert* file and/or your client
certificate (and the key) using the following configuration variables:

* ``core.net.http:cacert_path``: Path containing a custom Cacert file.
* ``core.net.http:client_cert``: Path or tuple of files containing a client cert (and key).

For instance:

.. code-block:: text
    :caption: **[CONAN_HOME]/global.conf**

    core.net.http:cacert_path=/path/to/cacert_file
    core.net.http:client_cert=/path/to/client_certificate
