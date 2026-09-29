.. _conan-cmake-toolchain:

CMakeToolchain
--------------

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.


The ``CMakeToolchain`` is the toolchain generator for CMake. It will generate toolchain files that can be used in the
command line invocation of CMake with the ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake``. This generator translates
the current package configuration, settings, and options, into CMake toolchain syntax.


.. important::

    This class will require very soon to define both the "host" and "build" profiles. It is very recommended to
    start defining both profiles immediately to avoid future breaking. Furthermore, some features, like trying to
    cross-compile might not work at all if the "build" profile is not provided.

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
        generators = "CMakeDeps"
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

- *conanbuild.conf*: The toolchain can also generate a ``conanbuild.conf`` file that contains arguments to
  the command line ``CMake()`` helper used in the recipe ``build()`` method. At the moment it contains only the CMake
  generator and the CMake toolchain file. The CMake generator will be deduced from the current Conan compiler settings:

  - For ``settings.compiler="Visual Studio"``, the CMake generator is a direct mapping of ``compiler.version``, as this version represents the IDE version, not the compiler version.
  - For ``settings.compiler=msvc``, the applied CMake generator will be, by default, the Visual Studio that introduced the specified `settings.compiler.version`. e.g: (``settings.compiler.version = 190`` => ``Visual Studio 14``, ``settings.compiler.version =  191`` => ``Visual Studio 15``, etc). This can be changed, using the ``tools.microsoft.msbuild:vs_version`` [conf] configuration. If it is defined, that Visual Studio version will be used as the CMake generator, and the specific compiler version and toolset will be defined in the ``conan_toolchain.cmake`` file..

- *conanvcvars.bat*: In some cases, the Visual Studio environment needs to be defined correctly for building,
  like when using the Ninja or NMake generators. If necessary, the ``CMakeToolchain`` will generate this script,
  so defining the correct Visual Studio prompt is easier.


constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, generator=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: this argument avoids collisions when you have multiple toolchain calls in the same
  recipe. By setting this argument, the *conanbuild.conf* file used to pass information to the
  build helper will be named as: *<namespace>_conanbuild.conf*. The default value is ``None`` meaning that
  the name of the generated file is *conanbuild.conf*. This namespace must be also set with the same
  value in the constructor of the :ref:`CMake build helper<conan-cmake-build-helper>` so that it reads the
  information from the proper file.

Most of the arguments are optional and will be deduced from the current ``settings``, and not
necessary to define them.

preprocessor_definitions
++++++++++++++++++++++++

This attribute allows defining compiler preprocessor definitions, for multiple configurations (Debug, Release, etc).

.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.preprocessor_definitions["MYDEF"] = "MyValue"
        tc.preprocessor_definitions.debug["MYCONFIGDEF"] = "MyDebugValue"
        tc.preprocessor_definitions.release["MYCONFIGDEF"] = "MyReleaseValue"
        tc.generate()

This will be translated to:

- One ``add_definitions()`` definition for ``MYDEF`` in ``conan_toolchain.cmake`` file.
- One ``add_definitions()`` definition, using a cmake generator expression in ``conan_toolchain.cmake`` file,
  using the different values for different configurations.

variables
+++++++++

This attribute allows defining CMake variables, for multiple configurations (Debug, Release, etc).

.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["MYVAR"] = "MyValue"
        tc.variables.debug["MYCONFIGVAR"] = "MyDebugValue"
        tc.variables.release["MYCONFIGVAR"] = "MyReleaseValue"
        tc.generate()

This will be translated to:

- One ``set()`` definition for ``MYVAR`` in ``conan_toolchain.cmake`` file.
- One ``set()`` definition, using a cmake generator expression in ``conan_toolchain.cmake`` file,
  using the different values for different configurations.

The booleans assigned to a variable will be translated to ``ON`` and ``OFF`` symbols in CMake:

.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["FOO"] = True
        tc.variables["VAR"] = False
        tc.generate()


Will generate the sentences: ``set(FOO ON ...)`` and ``set(VAR OFF ...)``.



Generators
++++++++++

The ``CMakeToolchain`` is intended to run with the ``CMakeDeps`` dependencies generator. Please do not use other
CMake legacy generators (like ``cmake``, or ``cmake_paths``) with it.


Using a custom toolchain file
+++++++++++++++++++++++++++++

There are two ways of providing custom CMake toolchain files:

- The ``conan_toolchain.cmake`` file can be completely skipped and replaced by a user one, defining the
  ``tools.cmake.cmaketoolchain:toolchain_file=<filepath>`` configuration value.
- A custom user toolchain file can be added (included from) to the ``conan_toolchain.cmake`` one, by using the
  ``user_toolchain`` block described below, and defining the ``tools.cmake.cmaketoolchain:user_toolchain=["<filepath>"]``
  configuration value.

  The configuration ``tools.cmake.cmaketoolchain:user_toolchain=["<filepath>"]`` can be defined in the :ref:`global.conf<global_conf>`
  but also creating a Conan package for your toolchain and using ``self.conf_info`` to declare the toolchain file:

    .. code:: python

        import os
        from conans import ConanFile
        class MyToolchainPackage(ConanFile):
            ...
            def package_info(self):
                f = os.path.join(self.package_folder, "mytoolchain.cmake")
                self.conf_info.define("tools.cmake.cmaketoolchain:user_toolchain", [f])


  If you declare the previous package as a ``tool_require``, the toolchain will be automatically applied.
- If you have more than one ``tool_requires`` defined, you can easily append all the user toolchain values
  together using the ``append`` method in each of them, for instance:

    .. code:: python

        import os
        from conans import ConanFile
        class MyToolRequire(ConanFile):
            ...
            def package_info(self):
                f = os.path.join(self.package_folder, "mytoolchain.cmake")
                # Appending the value to any existing one
                self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", f)


  So, they'll be automatically applied by your ``CMakeToolchain`` generator without writing any extra code:

    .. code:: python

        from conans import ConanFile
        from conan.tools.cmake import CMake
        class Pkg(ConanFile):
            settings = "os", "compiler", "arch", "build_type"
            exports_sources = "CMakeLists.txt"
            tool_requires = "toolchain1/0.1", "toolchain2/0.1"
            generators = "CMakeToolchain"

            def build(self):
                cmake = CMake(self)
                cmake.configure()


Using the toolchain in developer flow
+++++++++++++++++++++++++++++++++++++

One of the advantages of using Conan toolchains is that they can help to achieve the exact same build
with local development flows, than when the package is created in the cache.

With the ``CMakeToolchain`` it is possible to do, for multi-configuration systems like Visual Studio
(assuming we are using the ``CMakeDeps`` generator):

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

    # debug tool requires its own folder
    $ cd .. && mkdir build_debug && cd build_debug
    $ conan install .. -s build_type=Debug
    # the build type Debug is encoded in the toolchain already.
    # This conan_toolchain.cmake is specific for debug
    $ cmake .. -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build .  # or just "make"


Extending and customizing CMakeToolchain
++++++++++++++++++++++++++++++++++++++++

Since Conan 1.36, ``CMakeToolchain`` implements a powerful capability for extending and customizing the resulting toolchain file.

The following predefined blocks are available, and added in this order:

- ``user_toolchain``: Allows to include user toolchains from the ``conan_toolchain.cmake`` file.
  If the configuration ``tools.cmake.cmaketoolchain:user_toolchain=["xxxx", "yyyy"]`` is defined, its values will be ``include(xxx)\ninclude(yyyy)`` as the
  first lines in ``conan_toolchain.cmake``.
- ``generic_system``: Defines ``CMAKE_GENERATOR_PLATFORM``, ``CMAKE_GENERATOR_TOOLSET``, ``CMAKE_C_COMPILER``, ``CMAKE_CXX_COMPILER`` and ``CMAKE_BUILD_TYPE``
- ``android_system``: Defines ``ANDROID_PLATFORM``, ``ANDROID_STL``, ``ANDROID_ABI`` and includes ``CMAKE_ANDROID_NDK/build/cmake/android.toolchain.cmake``
  where ``CMAKE_ANDROID_NDK`` comes defined in ``tools.android:ndk_path`` configuration value.
- ``apple_system``: Defines ``CMAKE_SYSTEM_NAME``, ``CMAKE_SYSTEM_VERSION``, ``CMAKE_OSX_ARCHITECTURES``, ``CMAKE_OSX_SYSROOT`` for Apple systems.
- ``fpic``: Defines the ``CMAKE_POSITION_INDEPENDENT_CODE`` when there is a ``options.fPIC``
- ``arch_flags``: Defines C/C++ flags like ``-m32, -m64`` when necessary.
- ``libcxx``: Defines ``-stdlib=libc++`` flag when necessary as well as ``_GLIBCXX_USE_CXX11_ABI``.
- ``vs_runtime``: Defines the ``CMAKE_MSVC_RUNTIME_LIBRARY`` variable, as a generator expression for multiple configurations.
- ``cppstd``: defines ``CMAKE_CXX_STANDARD``, ``CMAKE_CXX_EXTENSIONS``
- ``parallel``: defines ``/MP`` parallel build flag for Visual.
- ``cmake_flags_init``: defines ``CMAKE_XXX_FLAGS`` variables based on previously defined Conan variables. The blocks above only define ``CONAN_XXX`` variables, and this block will define CMake ones like ``set(CMAKE_CXX_FLAGS_INIT "${CONAN_CXX_FLAGS}" CACHE STRING "" FORCE)```.
- ``try_compile``: Stop processing the toolchain, skipping the blocks below this one, if ``IN_TRY_COMPILE`` CMake property is defined.
- ``find_paths``: Defines ``CMAKE_FIND_PACKAGE_PREFER_CONFIG``, ``CMAKE_MODULE_PATH``, ``CMAKE_PREFIX_PATH`` so the generated files from ``CMakeDeps`` are found.
- ``rpath``: Defines ``CMAKE_SKIP_RPATH``. By default it is disabled, and it is needed to define ``self.blocks["rpath"].skip_rpath=True`` if you want to activate ``CMAKE_SKIP_RPATH``
- ``shared``: defines ``BUILD_SHARED_LIBS``.
- ``output_dirs``: Define the ``CMAKE_INSTALL_XXX`` variables.

    - **CMAKE_INSTALL_PREFIX**: Is set with the ``package_folder``, so if a "cmake install" operation is run, the artifacts go
      to that location.
    - **CMAKE_INSTALL_BINDIR**, **CMAKE_INSTALL_SBINDIR** and **CMAKE_INSTALL_LIBEXECDIR**: Set by default to ``bin``.
    - **CMAKE_INSTALL_LIBDIR**: Set by default to ``lib``.
    - **CMAKE_INSTALL_INCLUDEDIR** and **CMAKE_INSTALL_OLDINCLUDEDIR**: Set by default to ``include``.
    - **CMAKE_INSTALL_DATAROOTDIR**: Set by default to ``res``.

    If you want to change the default values, adjust the ``cpp.package`` object at the ``layout()`` method:

        .. code:: python

            def layout(self):
                ...
                # For CMAKE_INSTALL_BINDIR, CMAKE_INSTALL_SBINDIR and CMAKE_INSTALL_LIBEXECDIR, takes the first value:
                self.cpp.package.bindirs = ["mybin"]
                # For CMAKE_INSTALL_LIBDIR, takes the first value:
                self.cpp.package.libdirs = ["mylib"]
                # For CMAKE_INSTALL_INCLUDEDIR, CMAKE_INSTALL_OLDINCLUDEDIR, takes the first value:
                self.cpp.package.includedirs = ["myinclude"]
                # For CMAKE_INSTALL_DATAROOTDIR, takes the first value:
                self.cpp.package.resdirs = ["myres"]

    .. note::
        It is **not valid** to change the self.cpp_info  at the ``package_info()`` method.


.. note::
    In Conan 1.45 the CMakeToolchain doesn't append the root package folder of the dependencies (declared in the cpp_info.builddirs)
    to the ``CMAKE_PREFIX_PATH`` variable. That interfered with the ``find_file``, ``find_path`` and ``find_program``, making,
    for example, impossible to locate only the executables from the build context. In Conan 2.0, the ``cppinfo.builddirs``
    won't contain by default the ``''`` entry (root package).


Blocks can be customized in different ways:

.. code:: python

    # remove an existing block
    def generate(self):
        tc = CMakeToolchain(self)
        tc.blocks.remove("generic_system")

    # modify the template of an existing block
    def generate(self):
        tc = CMakeToolchain(self)
        tmp = tc.blocks["generic_system"].template
        new_tmp = tmp.replace(...)  # replace, fully replace, append...
        tc.blocks["generic_system"].template = new_tmp

    # modify one or more variables of the context
    def generate(self):
        tc = CMakeToolchain(conanfile)
        # block.values is the context dictionary
        build_type = tc.blocks["generic_system"].values["build_type"]
        tc.blocks["generic_system"].values["build_type"] = "Super" + build_type

    # modify the whole context values
    def generate(self):
        tc = CMakeToolchain(conanfile)
        tc.blocks["generic_system"].values = {"build_type": "SuperRelease"}

    # modify the context method of an existing block
    import types

    def generate(self):
        tc = CMakeToolchain(self)
        generic_block = toolchain.blocks["generic_system"]

        def context(self):
            assert self  # Your own custom logic here
            return {"build_type": "SuperRelease"}
        generic_block.context = types.MethodType(context, generic_block)

    # completely replace existing block
    from conan.tools.cmake import CMakeToolchain

    def generate(self):
        tc = CMakeToolchain(self)
        # this could go to a python_requires
        class MyGenericBlock:
            template = "HelloWorld"

            def context(self):
                return {}

        tc.blocks["generic_system"] = MyGenericBlock

    # add a completely new block
    from conan.tools.cmake import CMakeToolchain
    def generate(self):
        tc = CMakeToolchain(self)
        # this could go to a python_requires
        class MyBlock:
            template = "Hello {{myvar}}!!!"

            def context(self):
                return {"myvar": "World"}

        tc.blocks["mynewblock"] = MyBlock


Recall that this is a very **experimental** feature, and these interfaces might change in the following releases.

For more information about these blocks, please have a look at the source code.


Cross building
++++++++++++++

The ``generic_system`` block contains some basic cross-building capabilities. In the general
case, the user would want to provide their own user toolchain defining all the specifics,
which can be done with the configuration ``tools.cmake.cmaketoolchain:user_toolchain``. If
this conf value is defined, the ``generic_system`` block will include the provided file or files, but
no further define any CMake variable for cross-building.

If ``user_toolchain`` is not defined and Conan detects it is cross-building, because the build
and host profiles contain different OS or architecture, it will try to define the following
variables:

- ``CMAKE_SYSTEM_NAME``: ``tools.cmake.cmaketoolchain:system_name`` configuration if defined,
  otherwise, it will try to autodetect it. This block will consider cross-building if not Apple
  or Android systems (that is managed by other blocks), and not 64bits to 32bits builds in x86_64, sparc and
  ppc systems.
- ``CMAKE_SYSTEM_VERSION``: ``tools.cmake.cmaketoolchain:system_version`` conf if defined, otherwise
  ``os.version`` subsetting (host) when defined
- ``CMAKE_SYSTEM_PROCESSOR``: ``tools.cmake.cmaketoolchain:system_processor`` conf if defined, otherwise
  ``arch`` setting (host) if defined
