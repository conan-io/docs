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


This will generate the following files after a ``conan install`` (or when building the package
in the cache) with the information provided in the ``generate()`` method as well as information
translated from the current ``settings``:

- *conan_toolchain.cmake* file, containing the translation of Conan settings to CMake variables.
  Some things that will be defined in this file:

  - Definition of the CMake generator platform and generator toolset
  - Definition of the CMake ``build_type``
  - Definition of the ``CMAKE_POSITION_INDEPENDENT_CODE``, based on ``fPIC`` option.
  - Definition of the C++ standard as necessary
  - Definition of the standard library used for C++
  - Deactivation of rpaths in OSX

- *conanbuild.json*: The toolchain can also generate a ``conanbuild.json`` file that contains arguments to
  the command line ``CMake()`` helper used in the recipe ``build()`` method. At the moment it contains only the CMake
  generator. The CMake generator will be deduced from the current Conan compiler settings:

  - For ``settings.compiler="Visual Studio"``, the CMake generator is a direct mapping of ``compiler.version``, as this version represents the IDE version, not the compiler version.
  - For ``settings.compiler=msvc``, the CMake generator will be by default the one of the Visual Studio that introduced this compiler version (``msvc 19.0`` => ``Visual Studio 14``, ``msvc 19.1`` => ``Visual Studio 15``, etc). This can be changed, using the ``tools.microsoft.msbuild:vs_version`` [conf] configuration. If it is defined, that Visual Studio version will be used as the CMake generator, and the specific compiler version and toolset will be defined in the ``conan_toolchain.cmake`` file.

- *conanvcvars.bat*: In some cases, the Visual Studio environment needs to be defined correctly for building,
  like when using the Ninja or NMake generators. If necessary, the ``CMakeToolchain`` will generate this script,
  so defining the correct Visual Studio prompt is easier.


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
- One ``set()`` definition, using a cmake generator expression in ``conan_toolchain.cmake`` file,
  using the different values for different configurations.


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


Extending and customizing CMakeToolchain
++++++++++++++++++++++++++++++++++++++++

Since Conan 1.36, ``CMakeToolchain`` implements a powerful capability for extending and customizing the resulting toolchain file.

The following predefined blocks are available:

- ``generic_system``: Defines ``CMAKE_GENERATOR_PLATFORM``, ``CMAKE_GENERATOR_TOOLSET``, ``CMAKE_C_COMPILER``,``CMAKE_CXX_COMPILER`` and ``CMAKE_BUILD_TYPE``
- ``android_system``: Defines ``ANDROID_PLATFORM``, ``ANDROID_STL``, ``ANDROID_ABI`` and includes ``CMAKE_ANDROID_NDK/build/cmake/android.toolchain.cmake``
  where CMAKE_ANDROID_NDK comes defined in ``tools.android:ndk_path``
- ``ios_system``: Defines ``CMAKE_SYSTEM_NAME``, ``CMAKE_SYSTEM_VERSION``, ``CMAKE_OSX_ARCHITECTURES``, ``CMAKE_OSX_SYSROOT`` for Apple systems.
- ``find_paths``: Defines ``CMAKE_FIND_PACKAGE_PREFER_CONFIG``, ``CMAKE_MODULE_PATH``, ``CMAKE_PREFIX_PATH`` so the generated files from ``CMakeDeps`` are found.
- ``fpic``: Defines the ``CMAKE_POSITION_INDEPENDENT_CODE`` when there is a ``options.fPIC``
- ``rpath``: Defines ``CMAKE_SKIP_RPATH`` for OSX
- ``arch_flags``: Defines C/C++ flags like ``-m32, -m64`` when necessary.
- ``libcxx``: Defines ``-stdlib=libc++`` flag when necessary as well as ``_GLIBCXX_USE_CXX11_ABI``.
- ``vs_runtime``: Defines the ``CMAKE_MSVC_RUNTIME_LIBRARY`` variable, as a generator expression for
  for multiple configurations.
- ``cppstd``: defines ``CMAKE_CXX_STANDARD``, ``CMAKE_CXX_EXTENSIONS``
- ``shared``: defines ``BUILD_SHARED_LIBS``
- ``parallel``: defines ``/MP`` parallel build flag for Visual.


Blocks can be customized in different ways:

.. code:: python

    # remove an existing block
    def generate(self):
        tc = CMakeToolchain(self)
        tc.pre_blocks.remove("generic_system")

    # modify the template of an existing block
    def generate(self):
        tc = CMakeToolchain(self)
        tmp = tc.pre_blocks["generic_system"].template
        new_tmp = tmp.replace(...)  # replace, fully replace, append...
        tc.pre_blocks["generic_system"].template = new_tmp

    # modify the context (variables) of an existing block
    import types

    def generate(self):
        tc = CMakeToolchain(self)
        generic_block = toolchain.pre_blocks["generic_system"]

        def context(self):
            assert self  # Your own custom logic here
            return {"build_type": "SuperRelease"}
        generic_block.context = types.MethodType(context, generic_block)

    # completely replace existing block
    def generate(self):
        tc = CMakeToolchain(self)
        # this could go to a python_requires
        class MyGenericBlock(Block):
            template = "HelloWorld"

            def context(self):
                return {}

        tc.pre_blocks["generic_system"] = MyBlock

    # add a completely new block
    def generate(self):
        tc = CMakeToolchain(self)
        # this could go to a python_requires
        class MyBlock(Block):
            template = "Hello {{myvar}}!!!"

            def context(self):
                return {"myvar": "World"}

        tc.pre_blocks["mynewblock"] = MyBlock


    # extend from an existing block
    def generate(self):
        tc = CMakeToolchain(self)
        # this could go to a python_requires
        class MyBlock(GenericSystemBlock):
            template = "Hello {{build_type}}!!"

            def context(self):
                c = super(MyBlock, self).context()
                c["build_type"] = c["build_type"] + "Super"
                return c

        tc.pre_blocks["generic_system"] = MyBlock

Recall that this is a very **experimental** feature, and these interfaces might change in the following releases.

For more information about these blocks, please have a look at the source code.


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

    def __init__(self, conanfile, build_folder=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``build_folder``: Relative path to a folder to contain the temporary build files


configure()
+++++++++++

.. code:: python

    def configure(self, source_folder=None):

Calls ``cmake``, with the generator defined in the ``cmake_generator`` field of the
``conanbuild.json`` file, and passing ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake``.
If ``conanbuild.json`` file is not there, no generator will be passed.

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
