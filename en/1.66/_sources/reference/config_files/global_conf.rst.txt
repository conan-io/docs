.. _global_conf:

global.conf
===========

.. important::

    This feature is still **under development**, while it is recommended and usable and we will try not to break them in future releases,
    some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.


The **global.conf** file is located in the Conan user home directory.

Global configuration
--------------------

- ``core:required_conan_version = expression`` allows defining a version expression like
  ``>=1.30``. Conan will raise an error if its current version does not satisfy the
  condition
- ``core.package_id:msvc_visual_incompatible`` allows opting-out the fallback from the new
  ``msvc`` compiler to the ``Visual Studio`` compiler existing binaries
- ``core:default_profile`` defines the default host profile ('default' by default)
- ``core:default_build_profile`` defines the default build profile (None by default)

Tools configurations
--------------------

Tools and user configurations allows them to be defined both in the *global.conf* file and in profile files. Profile values will
have priority over globally defined ones in *global.conf*, and can be defined as:

.. code-block:: text

    [settings]
    ...

    [conf]
    tools.microsoft.msbuild:verbosity=Diagnostic
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10


To list all possible configurations available, run :command:`conan config list`.

.. code-block:: text

    $ conan config list

    core.package_id:msvc_visual_incompatible: Allows opting-out the fallback from the new msvc compiler to the Visual Studio compiler existing binaries
    core:default_build_profile: Defines the default build profile (None by default)
    core:default_profile: Defines the default host profile ('default' by default)
    core:required_conan_version: Raise if current version does not match the defined range
    tools.android:ndk_path: Argument for the CMAKE_ANDROID_NDK
    tools.apple.xcodebuild:verbosity: Verbosity level for xcodebuild: 'verbose' or 'quiet
    tools.apple:enable_arc: (boolean) Enable/Disable ARC Apple Clang flags
    tools.apple:enable_bitcode: (boolean) Enable/Disable Bitcode Apple Clang flags
    tools.apple:enable_visibility: (boolean) Enable/Disable Visibility Apple Clang flags
    tools.apple:sdk_path: Path for the sdk location. This value will be passed as SDKROOT or -isysroot depending on the generator used
    tools.build.cross_building:can_run: Set the return value for the 'conan.tools.build.can_run()' tool
    tools.build:cflags: List of extra C flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
    tools.build:compiler_executables: Defines a Python dict-like with the compilers path to be used. Allowed keys {'c', 'cpp', 'cuda', 'objc', 'objcxx', 'rc', 'fortran', 'asm', 'hip', 'ispc'}
    tools.build:cxxflags: List of extra CXX flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
    tools.build:defines: List of extra definition flags used by different toolchains like CMakeToolchain and AutotoolsToolchain
    tools.build:exelinkflags: List of extra flags used by CMakeToolchain for CMAKE_EXE_LINKER_FLAGS_INIT variable
    tools.build:jobs: Default compile jobs number -jX Ninja, Make, /MP VS (default: max CPUs)
    tools.build:linker_scripts: List of linker scripts used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
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
    tools.cmake.cmaketoolchain:toolset_arch: Will add the ',host=xxx' specifier in the 'CMAKE_GENERATOR_TOOLSET' variable of 'conan_toolchain.cmake' file
    tools.cmake.cmaketoolchain:user_toolchain: Inject existing user toolchains at the beginning of conan_toolchain.cmake
    tools.env.virtualenv:auto_use: Automatically activate virtualenv file generation
    tools.env.virtualenv:powershell: Opt-in to generate Powershell '.ps1' scripts instead of '.bat'
    tools.files.download:download_cache: Location for the download cache
    tools.files.download:retry: Number of retries in case of failure when downloading
    tools.files.download:retry_wait: Seconds to wait between download attempts
    tools.gnu:define_libcxx11_abi: Force definition of GLIBCXX_USE_CXX11_ABI=1 for libstdc++11
    tools.gnu:host_triplet: Custom host triplet to pass to Autotools scripts
    tools.gnu:make_program: Indicate path to make program
    tools.gnu:pkg_config: Define the 'pkg_config' executable name or full path
    tools.google.bazel:bazelrc_path: Defines Bazel rc-path
    tools.google.bazel:configs: Define Bazel config file
    tools.intel:installation_path: Defines the Intel oneAPI installation root path
    tools.intel:setvars_args: Custom arguments to be passed onto the setvars.sh|bat script from Intel oneAPI
    tools.meson.mesontoolchain:backend: Set the Meson backend. Possible values: 'ninja', 'vs', 'vs2010', 'vs2015', 'vs2017', 'vs2019', 'xcode'
    tools.meson.mesontoolchain:extra_machine_files: List of paths for any additional native/cross file references to be appended to the existing Conan ones
    tools.microsoft.bash:path: Path to the shell executable. Default: 'bash'
    tools.microsoft.bash:subsystem: Set subsystem to use for Windows. Possible values: 'msys2', 'msys', 'cygwin', 'wsl' and 'sfu'
    tools.microsoft.msbuild:installation_path: VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community. Use empty string to disable.
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

    This list may be outdated. Please, run the command :command:`conan config list` to check the latest configurations.


Configuration file template
---------------------------

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

It is possible to use **jinja2** template engine for *global.conf*. When Conan loads this file, immediately parses
and renders the template, which must result in a standard tools-configuration text.

  .. code:: jinja

     # Using all the cores automatically
     tools.build:jobs={{os.cpu_count()}}
     # Using the current OS
     user.myconf.system:name = {{platform.system()}}


.. note::

    The Python packages passed to render the template are ``os`` and ``platform`` for all platforms and ``distro`` in Linux platforms.



Added in `1.60.0 <https://github.com/conan-io/conan/releases/tag/1.60.0>`_: Make variable ``conan_version`` available


Configuration data types
------------------------

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

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

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

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
    [build_requires]
    [env]
    [conf]
    user.myconf.build:cflags=!
    user.myconf.build:ldflags=['--prefix prefix-value', '--flag1 value1', '--flag2 value2']
    ...


Configuration patterns
----------------------

You can use package patterns to apply the configuration in those dependencies which are matching:

.. code-block:: text

    *:tools.cmake.cmaketoolchain:generator=Ninja
    zlib/*:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019

This example shows you how to specify a general `generator` for all your packages, but for `zlib` one. `zlib` is defining
`Visual Studio 16 2019` as its own generator.

Besides that, it's quite relevant to say that **the order matters**. So, if we change the order of the
configuration lines above:

.. code-block:: text

    zlib/*:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019
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


Configuration from tool_requires
--------------------------------

From Conan 1.37, it is possible to define configuration in packages that are ``tool_requires``. For example, assuming
there is a package that bundles the AndroidNDK, it could define the location of such NDK to the ``tools.android:ndk_path``
configuration as:


.. code-block:: python

    import os
    from conan import ConanFile

    class Pkg(ConanFile):
        name = "android_ndk"

        def package_info(self):
            self.conf_info.define("tools.android:ndk_path", os.path.join(self.package_folder, "ndk"))


Note that this only propagates from the immediate, direct ``tool_requires`` of a recipe.
