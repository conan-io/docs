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


The ``CMakeToolchain`` will generate 2 files:

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

This attribute allows to define cmake variables, for multiple configurations (Debug, Release, etc)

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


CMake build helper
------------------

The ``CMake()`` build helper that works with the ``CMakeToolchain`` is also experimental,
and subject to breaking change in the future. It will evolve to adapt and complement the
toolchain functionality. It supports the following methods:

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


- ``source_folder``: Relative path to the folder containing the root *CMakeLists.txt*


build()
+++++++

.. code:: python

    def build(self, build_type=None, target=None):


Calls the build system. Equivalent to call ``cmake --build .`` in the build folder.


- ``build_type``: Use it only to override the value defined in the ``settings.build_type``. It 
  can fail if the build is single configuration (e.g. Unix Makefiles), as in that case the build
  type must be specified at configure time, not build type.
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
- ``target``: name of the build target to run, by default ``RUN_TESTS`` or ``test``
