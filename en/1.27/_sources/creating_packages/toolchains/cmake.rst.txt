CMakeToolchain
==============

The ``CMakeToolchain`` can be used in the ``toolchain()`` method:


.. code:: python

    from conans import ConanFile, CMake, CMakeToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        generators = "cmake_find_package_multi"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def toolchain(self):
            tc = CMakeToolchain(self)
            return tc


The ``CMakeToolchain`` will generate 2 files, after a ``conan install`` command (or
before calling the ``build()`` method when the package is being built in the cache):

- The main *conan_toolchain.cmake* file, that can be used in the command line.
- A *conan_project_include.cmake* file, that will automatically be called right after the 
  ``project()`` call for cmake>=3.15, containing definitions that only take effect after such
  call. For older cmake versions you should explicitly call ``include(.../conan_project_include.cmake)``
  in your *CMakeLists.txt*.


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
                 cmake_system_name=True, toolset=None, parallel=True, make_program=None):


Most of the arguments are optional and will be deduced from the current ``settings``, and not
necessary to define them.


definitions
+++++++++++

This attribute allows defining CMake variables, for multiple configurations (Debug, Release, etc).

.. code:: python

    def toolchain(self):
        tc = CMakeToolchain(self)
        tc.definitions["MYVAR"] = "MyValue"
        tc.definitions.debug["MYCONFIGVAR"] = "MyDebugValue"
        tc.definitions.release["MYCONFIGVAR"] = "MyReleaseValue"
        return tc

This will be translated to:

- One ``set()`` definition for ``MYVAR`` in ``conan_toolchain.cmake`` file.
- One ``set()`` definition, using a cmake generator expression in ``conan_project_include.cmake`` file,
  using the different values for different configurations. It is important to recall that things
  that depend on the build type cannot be directly set in the toolchain.

generators
----------

The ``CMakeToolchain`` only works with the ``cmake_find_package`` and ``cmake_find_package_multi``
generators. Using others will raise, as they can have overlapping definitions that can conflict.


Using the toolchain in developer flow
-------------------------------------

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



CMake build helper
------------------

The ``CMake()`` build helper that works with the ``CMakeToolchain`` is also experimental,
and subject to breaking change in the future. It will evolve to adapt and complement the
toolchain functionality. 

The helper is intended to be used in the ``build()`` method, to call CMake commands automatically
when a package is being built directly by Conan (create, install)

.. code:: python

    from conans import CMake

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="src")
        cmake.build()


It supports the following methods:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, generator=None, build_folder=None, parallel=True,
                 msbuild_verbosity="minimal"):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``generator``: CMake generator. Define it only to override the default one (like ``Visual Studio 15``).
  Note that as the platform (x64, Win32...) is now defined in the toolchain it is not necessary to specify it here.
- ``build_folder``: Relative path to a folder to contain the temporary build files
- ``parallel``: Set it to ``False`` to deactivate using parallel builds. If activated, it will use
  ``cpu_count`` configuration as the number of parallel jobs to use.
- ``msbuild_verbosity``: Used to define the output of MSBuild builds.


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
