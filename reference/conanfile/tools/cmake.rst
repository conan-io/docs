.. _conan_tools_cmake:

conan.tools.cmake
=================

.. warning::

    These tools are **experimental** and subject to breaking changes.


CMakeDeps
---------

Available since: `1.33.0 <https://github.com/conan-io/conan/releases/tag/1.33.0>`_

The ``CMakeDeps`` helper will generate one **xxxx-config.cmake** file per dependency, together with other necessary *.cmake* files
like version, flags and directory data or configuration. It can be used like:


.. code-block:: python

    from conans import ConanFile

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        generators = "CMakeDeps"


The full instantiation, that allows custom configuration can be done in the ``generate()`` method:


.. code-block:: python

    from conans import ConanFile
    from conan.tools.cmake import CMakeDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"

        def generate(self):
            cmake = CMakeDeps(self)
            cmake.configurations.append("ReleaseShared")
            if self.options["hello"].shared:
                cmake.configuration = "ReleaseShared"
            cmake.generate()

As it can be seen, it allows to define custom user CMake configurations besides the standard Release, Debug, etc ones.
If the **settings.yml** file is customized to add new configurations to the ``settings.build_type``, then, adding it
explicitly to ``.configurations`` is not necessary.

.. _conan-cmake-toolchain:

CMakeToolchain
--------------
The ``CMakeToolchain`` is the toolchain generator for CMake. It will generate toolchain files that can be used in the
command line invocation of CMake with the ``-DCMAKE_TOOLCHAIN_FILE=conantoolchain.cmake``. This generator translates
the current package configuration, settings, and options, into CMake toolchain syntax.

It can be declared as:

.. code-block:: python

    from conans import ConanFile

    class Pkg(ConanFile):
        generators = "CMakeToolchain"

Or fully instantiated in the ``generate()`` method:

.. code-block:: python

    from conans import ConanFile
    from conan.tools.cmake import CMakeToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        generators = "cmake_find_package_multi"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def generate(self):
            tc = CMakeToolchain(self)
            tc.variables["MYVAR"] = "MYVAR_VALUE"
            tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
            tc.generate()


This will generate a *conan_toolchain.cmake* file after a ``conan install`` (or when building the package
in the cache) with the information provided in the ``generate()`` method as well as information
translated from the current ``settings``.

These file will automatically manage the definition of cmake values according to current Conan
settings:

- Definition of the CMake generator platform and generator toolset
- Definition of the CMake ``build_type``
- Definition of the ``CMAKE_POSITION_INDEPENDENT_CODE``, based on ``fPIC`` option.
- Definition of the C++ standard as necessary
- Definition of the standard library used for C++
- Deactivation of rpaths in OSX

Most of these things will be configurable, please provide feedback at: https://github.com/conan-io/conan/issues

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, generator=None, generator_platform=None, build_type=None,
                 cmake_system_name=True, toolset=None):


Most of the arguments are optional and will be deduced from the current ``settings``, and not
necessary to define them.


preprocessor_definitions
++++++++++++++++++++++++

This attribute allows defining CMake variables, for multiple configurations (Debug, Release, etc).

.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.preprocessor_definitions["MYVAR"] = "MyValue"
        tc.preprocessor_definitions.debug["MYCONFIGVAR"] = "MyDebugValue"
        tc.preprocessor_definitions.release["MYCONFIGVAR"] = "MyReleaseValue"
        tc.generate()

This will be translated to:

- One ``set()`` definition for ``MYVAR`` in ``conan_toolchain.cmake`` file.
- One ``set()`` definition, using a cmake generator expression in ``conan_project_include.cmake`` file,
  using the different values for different configurations. It is important to recall that things
  that depend on the build type cannot be directly set in the toolchain.


The ``CMakeToolchain`` is intended to run with the ``CMakeDeps`` dependencies generator. It might temporarily
work with others like ``cmake_find_package`` and ``cmake_find_package_multi``, but this will be removed soon.

Using the toolchain in developer flow
+++++++++++++++++++++++++++++++++++++

One of the advantages of using Conan toolchains is that they can help to achieve the exact same build
with local development flows, than when the package is created in the cache.

With the ``CMakeToolchain`` it is possible to do, for multi-configuration systems like Visual Studio
(assuming we are using the ``cmake_find_package_multi`` generator):

.. code:: bash

    # Lets start in the folder containing the conanfile.py
    $ mkdir build && cd build
    # Install both debug and release deps and create the toolchain
    $ conan install ..
    $ conan install .. -s build_type=Debug
    # the conan_toolchain.cmake is common for both configurations
    # Need to pass the generator WITHOUT the platform, that matches your default settings
    $ cmake .. -G "Visual Studio 15" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    # Now you can open the IDE, select Debug or Release config and build
    # or, in the command line
    $ cmake --build . --config Release
    $ cmake --build . --config Debug


**NOTE**: The platform (Win64), is already encoded in the toolchain. The command line shouldn't pass it, so using
``-G "Visual Studio 15"`` instead of the ``-G "Visual Studio 15 Win64"``


For single-configuration build systems:

.. code:: bash

    # Lets start in the folder containing the conanfile.py
    $ mkdir build_release && cd build_release
    $ conan install ..
    # the build type Release is encoded in the toolchain already.
    # This conan_toolchain.cmake is specific for release
    $ cmake .. -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build .  # or just "make"

    # debug build requires its own folder
    $ cd .. && mkdir build_debug && cd build_debug
    $ conan install .. -s build_type=Debug
    # the build type Debug is encoded in the toolchain already.
    # This conan_toolchain.cmake is specific for debug
    $ cmake .. -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build .  # or just "make"


Conan is able to generate a toolchain file for different systems. In the
following sections you can find more information about them:

 * :ref:`Android <conan-cmake-toolchain-android>`.
 * :ref:`iOS <conan-cmake-toolchain-ios>`.


CMake
-----
The ``CMake`` build helper is a wrapper around the command line invocation of cmake. It will abstract the
calls like ``cmake --build . --config Release`` into Python method calls. It will also add the argument
``-DCMAKE_TOOLCHAIN_FILE=conantoolchain.cmake`` to the ``configure()`` call.

The helper is intended to be used in the ``build()`` method, to call CMake commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conans import ConanFile
    from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()
            deps = CMakeDeps(self)
            deps.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

**Note:** This helper includes the additional flag `-DCMAKE_SH="CMAKE_SH-NOTFOUND"` when using the `MinGW Makefiles` CMake's
generator, to avoid the error of `sh` being in the PATH (CMake version < 3.17.0).

It supports the following methods:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, generator=None, build_folder=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``generator``: CMake generator. Define it only to override the default one (like ``Visual Studio 15``).
  Note that as the platform (x64, Win32...) is now defined in the toolchain it is not necessary to specify it here.
- ``build_folder``: Relative path to a folder to contain the temporary build files


configure()
+++++++++++

.. code:: python

    def configure(self, source_folder=None):

Calls ``cmake``, with the given generator and passing ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake``.
It will also provide the CMake generator in the command like, like ``-G "Visual Studio 15"``. Note
that it is not necessary to specify the platform, like ``-G "Visual Studio 15 Win64"``, as the
platform is already defined in the toolchain file.

- ``source_folder``: Relative path to the folder containing the root *CMakeLists.txt*


build()
+++++++

.. code:: python

    def build(self, build_type=None, target=None):


Calls the build system. Equivalent to :command:`cmake --build .` in the build folder.


- ``build_type``: Use it only to override the value defined in the ``settings.build_type`` for a multi-configuration generator (e.g. Visual Studio, XCode).
  This value will be ignored for single-configuration generators, they will use the one defined in the toolchain file during the install step.
- ``target``: name of the build target to run.


install()
+++++++++

.. code:: python

    def install(self, build_type=None):


Equivalent to run ``cmake --build . --target=install``

- ``build_type``: Use it only to override the value defined in the ``settings.build_type``. It
  can fail if the build is single configuration (e.g. Unix Makefiles), as in that case the build
  type must be specified at configure time, not build type.


test()
++++++

.. code:: python

    def test(self, build_type=None, target=None, output_on_failure=False):


Equivalent to running :command:`cmake --build . --target=RUN_TESTS`.

- ``build_type``: Use it only to override the value defined in the ``settings.build_type``. It
  can fail if the build is single configuration (e.g. Unix Makefiles), as in that case the build
  type must be specified at configure time, not build type.
- ``target``: name of the build target to run, by default ``RUN_TESTS`` or ``test``.


conf
++++

- ``tools.microsoft.msbuild:verbosity`` will accept one of ``"Quiet", "Minimal", "Normal", "Detailed", "Diagnostic"`` to be passed
  to the ``CMake.build()`` command, when a Visual Studio generator (MSBuild build system) is being used for CMake. It is passed as
  an argument to the underlying build system via the call ``cmake --build . --config Release -- /verbosity:Diagnostic``

- ``tools.ninja:jobs`` argument for the ``--jobs`` parameter when running Ninja generator. (overrides
  the general ``tools.build:processes``).

- ``tools.microsoft.msbuild:max_cpu_count`` argument for the ``/m`` (``/maxCpuCount``) when running
  ``MSBuild`` (overrides the general ``tools.build:processes``).
