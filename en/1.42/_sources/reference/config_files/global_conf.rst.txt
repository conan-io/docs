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
    tools.microsoft.msbuild:max_cpu_count=20
    tools.microsoft.msbuild:vs_version = 16
    tools.build:processes=10
    tools.ninja:jobs=30
    tools.gnu.make:jobs=40


To list all possible configurations available, run :command:`conan config list`.

- core:required_conan_version: Raise if current version does not match the defined range.
- core.package_id:msvc_visual_incompatible: Allows opting-out the fallback from the new msvc compiler to the Visual Studio compiler existing binaries
- core:default_profile: Defines the default host profile ('default' by default)
- core:default_build_profile: Defines the default build profile (None by default)
- tools.android:ndk_path: Argument for the CMAKE_ANDROID_NDK
- tools.build:skip_test: Do not execute CMake.test() and Meson.test() when enabled
- tools.build:processes: Default jobs number
- tools.cmake.cmaketoolchain:generator: User defined CMake generator to use instead of default
- tools.cmake.cmaketoolchain:msvc_parallel_compile: Argument for the /MP when running msvc
- tools.cmake.cmaketoolchain:find_package_prefer_config: Argument for the CMAKE_FIND_PACKAGE_PREFER_CONFIG
- tools.cmake.cmaketoolchain:toolchain_file: Use other existing file rather than conan_toolchain.cmake one
- tools.cmake.cmaketoolchain:user_toolchain: Inject existing user toolchain at the beginning of conan_toolchain.cmake
- tools.cmake.cmaketoolchain:system_name: Define CMAKE_SYSTEM_NAME in CMakeToolchain
- tools.cmake.cmaketoolchain:system_version: Define CMAKE_SYSTEM_VERSION in CMakeToolchain
- tools.cmake.cmaketoolchain:system_processor: Define CMAKE_SYSTEM_PROCESSOR in CMakeToolchain
- tools.env.virtualenv:auto_use: Automatically activate virtualenv file generation
- tools.files.download:retry: Number of retries in case of failure when downloading
- tools.files.download:retry_wait: Seconds to wait between download attempts
- tools.gnu:make_program: Indicate path to make program
- tools.gnu.make:jobs: Argument for the -j parameter when running Make generator
- tools.google.bazel:config: Define Bazel config file
- tools.google.bazel:bazelrc_path: Defines Bazel rc-path
- tools.microsoft.msbuild:verbosity: Verbosity level for MSBuild: 'Quiet', 'Minimal', 'Normal', 'Detailed', 'Diagnostic'
- tools.microsoft.msbuild:max_cpu_count: Argument for the /m (/maxCpuCount) when running MSBuild
- tools.microsoft.msbuild:vs_version: Defines the IDE version when using the new msvc compiler
- tools.microsoft.msbuild:installation_path: VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community
- tools.microsoft.msbuilddeps:exclude_code_analysis: Suppress MSBuild code analysis for patterns
- tools.microsoft.msbuildtoolchain:compile_options: Dictionary with MSBuild compiler options
- tools.ninja:jobs: Argument for the --jobs parameter when running Ninja generator


Configuration from build_requires
-----------------------------------

From Conan 1.37, it is possible to define configuration in packages that are ``build_requires``. For example, assuming
there is a package that bundles the AndroidNDK, it could define the location of such NDK to the ``tools.android:ndk_path``
configuration as:


.. code-block:: python

    import os
    from conans import ConanFile

    class Pkg(ConanFile):
        name = "android_ndk"

        def package_info(self):
            self.conf_info["tools.android:ndk_path"] = os.path.join(self.package_folder, "ndk")


Note that this only propagates from the immediate, direct ``build_requires`` of a recipe.
