.. _global_conf:

global.conf
===========

.. warning::

    This new configuration mechanism is an **experimental** feature subject to breaking changes in future releases.


The **global.conf** file is located in the Conan user home directory.

Global configuration
--------------------

- ``core:required_conan_version = expression`` allows defining a version expression like ``>=1.30``. Conan will raise an error if its current version does not satisfy the condition
- ``core.package_id:msvc_visual_incompatible`` allows opting-out the fallback from the new ``msvc`` compiler to the ``Visual Studio`` compiler existing binaries



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

.. code-block:: bash

    $ conan config list
    Supported Conan *experimental* global.conf and [conf] properties:
    core:required_conan_version: Raise if current version does not match the defined range.
    core:non_interactive: Disable interactive user input, raises error if input necessary
    core.package_id:msvc_visual_incompatible: Allows opting-out the fallback from the new msvc compiler to the Visual Studio compiler existing binaries
    core:default_profile: Defines the default host profile ('default' by default)
    core:default_build_profile: Defines the default build profile (None by default)
    core.upload:retry: Number of retries in case of failure when uploading to Conan server
    core.upload:retry_wait: Seconds to wait between upload attempts to Conan server
    core.download:parallel: Number of concurrent threads to download packages
    core.download:retry: Number of retries in case of failure when downloading from Conan server
    core.download:retry_wait: Seconds to wait between download attempts from Conan server
    core.net.http:max_retries: Maximum number of connection retries (requests library)
    core.net.http:timeout: Number of seconds without response to timeout (requests library)
    core.net.http:no_proxy_match: List of urls to skip from proxies configuration
    core.net.http:proxies: Dictionary containing the proxy configuration
    core.net.http:cacert_path: Path containing a custom Cacert file
    core.net.http:client_cert: Path or tuple of files containing a client cert (and key)
    core.net.http:clean_system_proxy: If defined, the proxies system env-vars will be discarded
    core.gzip:compresslevel: The Gzip compresion level for Conan artifacts (default=9)
    tools.android:ndk_path: Argument for the CMAKE_ANDROID_NDK
    tools.build:skip_test: Do not execute CMake.test() and Meson.test() when enabled
    tools.build:jobs: Default compile jobs number -jX Ninja, Make, /MP VS (default: max CPUs)
    tools.cmake.cmaketoolchain:generator: User defined CMake generator to use instead of default
    tools.cmake.cmaketoolchain:find_package_prefer_config: Argument for the CMAKE_FIND_PACKAGE_PREFER_CONFIG
    tools.cmake.cmaketoolchain:toolchain_file: Use other existing file rather than conan_toolchain.cmake one
    tools.cmake.cmaketoolchain:user_toolchain: Inject existing user toolchain at the beginning of conan_toolchain.cmake
    tools.cmake.cmaketoolchain:system_name: Define CMAKE_SYSTEM_NAME in CMakeToolchain
    tools.cmake.cmaketoolchain:system_version: Define CMAKE_SYSTEM_VERSION in CMakeToolchain
    tools.cmake.cmaketoolchain:system_processor: Define CMAKE_SYSTEM_PROCESSOR in CMakeToolchain
    tools.files.download:retry: Number of retries in case of failure when downloading
    tools.files.download:retry_wait: Seconds to wait between download attempts
    tools.gnu:make_program: Indicate path to make program
    tools.google.bazel:config: Define Bazel config file
    tools.google.bazel:bazelrc_path: Defines Bazel rc-path
    tools.microsoft.msbuild:verbosity: Verbosity level for MSBuild: 'Quiet', 'Minimal', 'Normal', 'Detailed', 'Diagnostic'
    tools.microsoft.msbuild:vs_version: Defines the IDE version when using the new msvc compiler
    tools.microsoft.msbuild:max_cpu_count: Argument for the /m when running msvc to build parallel projects
    tools.microsoft.msbuild:installation_path: VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community
    tools.microsoft.msbuilddeps:exclude_code_analysis: Suppress MSBuild code analysis for patterns
    tools.microsoft.msbuildtoolchain:compile_options: Dictionary with MSBuild compiler options
    tools.intel:installation_path: Defines the Intel oneAPI installation root path
    tools.intel:setvars_args: Custom arguments to be passed onto the setvars.sh|bat script from Intel oneAPI


Configuration from tool_requires
--------------------------------

From Conan 1.37, it is possible to define configuration in packages that are ``tool_requires``. For example, assuming
there is a package that bundles the AndroidNDK, it could define the location of such NDK to the ``tools.android:ndk_path``
configuration as:


.. code-block:: python

    import os
    from conans import ConanFile

    class Pkg(ConanFile):
        name = "android_ndk"

        def package_info(self):
            self.conf_info["tools.android:ndk_path"] = os.path.join(self.package_folder, "ndk")


Note that this only propagates from the immediate, direct ``tool_requires`` of a recipe.
