.. _conan-cmake-toolchain:

CMakeToolchain
==============


The ``CMakeToolchain`` is the toolchain generator for CMake. It produces the toolchain file that can be used in the
command line invocation of CMake with the ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake``. This generator translates
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
        generators = "CMakeDeps"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def generate(self):
            tc = CMakeToolchain(self)
            tc.variables["MYVAR"] = "MYVAR_VALUE"
            tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
            tc.generate()


.. note::

    The ``CMakeToolchain`` is intended to run with the ``CMakeDeps`` dependencies generator. Please do not use other
    CMake legacy generators (like ``cmake``, or ``cmake_paths``) with it.


Generated files
---------------

This will generate the following files after a ``conan install`` (or when building the package
in the cache) with the information provided in the ``generate()`` method as well as information
translated from the current ``settings``:

- **conan_toolchain.cmake**: containing the translation of Conan settings to CMake variables.
  Some things that will be defined in this file:

  - Definition of the CMake generator platform and generator toolset
  - Definition of the ``CMAKE_POSITION_INDEPENDENT_CODE``, based on ``fPIC`` option.
  - Definition of the C++ standard as necessary
  - Definition of the standard library used for C++
  - Deactivation of rpaths in OSX

- **CMakePresets.json**: The toolchain also generates a ``CMakePresets.json`` standard file, check the documentation
  `here <https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html>`_. It is currently using the version "3" of
  the JSON schema.
  Conan creates a ``default`` configure preset with the information:

     - The ``generator`` to be used.
     - The path to the ``conan_toolchain.cmake``.
     - Some cache variables corresponding to the specified settings cannot work if specified in the toolchain.
     - The ``CMAKE_BUILD_TYPE`` variable when using a single-configuration generators.
     - If you run several ``conan install`` with different ``-s build_type`` values, it will generate the corresponding
       ``buildPresets`` and ``configurePresets``.

- **CMakeUserPresets.json**:  If you declare a ``layout()`` in the recipe and your ``CMakeLists.txt`` file is found at
  the ``conanfile.source_folder`` folder, a ``CMakeUserPresets.json`` file will be generated (if doesn't exist already) including
  automatically the ``CMakePresets.json`` (at the ``conanfile.generators_folder``) to allow your IDE (Visual Studio,
  Visual Studio Code, CLion...) or ``cmake`` tool to locate the ``CMakePresets.json``. The version schema of the generated
  ``CMakeUserPresets.json`` is "4" and requires CMake >= 3.23.


- **conanvcvars.bat**: In some cases, the Visual Studio environment needs to be defined correctly for building,
  like when using the Ninja or NMake generators. If necessary, the ``CMakeToolchain`` will generate this script,
  so defining the correct Visual Studio prompt is easier.


Customization
-------------


preprocessor_definitions
^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^

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


Using a custom toolchain file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two ways of providing custom CMake toolchain files:

- The ``conan_toolchain.cmake`` file can be completely skipped and replaced by a user one, defining the
  ``tools.cmake.cmaketoolchain:toolchain_file=<filepath>`` configuration value.
- A custom user toolchain file can be added (included from) to the ``conan_toolchain.cmake`` one, by using the
  ``user_toolchain`` block described below, and defining the ``tools.cmake.cmaketoolchain:user_toolchain=["<filepath>"]``
  configuration value.

  The configuration ``tools.cmake.cmaketoolchain:user_toolchain=["<filepath>"]`` can be defined in the ``global.conf``.
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


Extending and advanced customization
------------------------------------

``CMakeToolchain`` implements a powerful capability for extending and customizing the resulting toolchain file.

The contents are organized by ``blocks`` that can be customized. The following predefined blocks are available,
and added in this order:

- **user_toolchain**: Allows to include user toolchains from the ``conan_toolchain.cmake`` file.
  If the configuration ``tools.cmake.cmaketoolchain:user_toolchain=["xxxx", "yyyy"]`` is defined, its values will be ``include(xxx)\ninclude(yyyy)`` as the
  first lines in ``conan_toolchain.cmake``.
- **generic_system**: Defines ``CMAKE_SYSTEM_NAME``, ``CMAKE_SYSTEM_VERSION``, ``CMAKE_SYSTEM_PROCESSOR``,
  ``CMAKE_GENERATOR_PLATFORM``, ``CMAKE_GENERATOR_TOOLSET``, ``CMAKE_C_COMPILER``,
  ``CMAKE_CXX_COMPILER``
- **android_system**: Defines ``ANDROID_PLATFORM``, ``ANDROID_STL``, ``ANDROID_ABI`` and includes ``ANDROID_NDK_PATH/build/cmake/android.toolchain.cmake``
  where ``ANDROID_NDK_PATH`` comes defined in ``tools.android:ndk_path`` configuration value.
- **apple_system**: Defines ``CMAKE_OSX_ARCHITECTURES``, ``CMAKE_OSX_SYSROOT`` for Apple systems.
- **fpic**: Defines the ``CMAKE_POSITION_INDEPENDENT_CODE`` when there is a ``options.fPIC``
- **arch_flags**: Defines C/C++ flags like ``-m32, -m64`` when necessary.
- **libcxx**: Defines ``-stdlib=libc++`` flag when necessary as well as ``_GLIBCXX_USE_CXX11_ABI``.
- **vs_runtime**: Defines the ``CMAKE_MSVC_RUNTIME_LIBRARY`` variable, as a generator expression for multiple configurations.
- **cppstd**: defines ``CMAKE_CXX_STANDARD``, ``CMAKE_CXX_EXTENSIONS``
- **parallel**: defines ``/MP`` parallel build flag for Visual.
- **cmake_flags_init**: defines ``CMAKE_XXX_FLAGS`` variables based on previously defined Conan variables. The blocks above only define ``CONAN_XXX`` variables, and this block will define CMake ones like ``set(CMAKE_CXX_FLAGS_INIT "${CONAN_CXX_FLAGS}" CACHE STRING "" FORCE)```.
- **try_compile**: Stop processing the toolchain, skipping the blocks below this one, if ``IN_TRY_COMPILE`` CMake property is defined.
- **find_paths**: Defines ``CMAKE_FIND_PACKAGE_PREFER_CONFIG``, ``CMAKE_MODULE_PATH``, ``CMAKE_PREFIX_PATH`` so the generated files from ``CMakeDeps`` are found.
- **rpath**: Defines ``CMAKE_SKIP_RPATH``. By default it is disabled, and it is needed to define ``self.blocks["rpath"].skip_rpath=True`` if you want to activate ``CMAKE_SKIP_RPATH``
- **shared**: defines ``BUILD_SHARED_LIBS``.
- **output_dirs**: Define the ``CMAKE_INSTALL_XXX`` variables.

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


Customizing the content blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every block can be customized in different ways:

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
        toolset = tc.blocks["generic_system"].values["toolset"]
        tc.blocks["generic_system"].values["toolset"] = "other_toolset"

    # modify the whole context values
    def generate(self):
        tc = CMakeToolchain(conanfile)
        tc.blocks["generic_system"].values = {"toolset": "other_toolset"}

    # modify the context method of an existing block
    import types

    def generate(self):
        tc = CMakeToolchain(self)
        generic_block = toolchain.blocks["generic_system"]

        def context(self):
            assert self  # Your own custom logic here
            return {"toolset": "other_toolset"}
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


For more information about these blocks, please have a look at the source code.


Cross building
--------------

The ``generic_system`` block contains some basic cross-building capabilities. In the general
case, the user would want to provide their own user toolchain defining all the specifics,
which can be done with the configuration ``tools.cmake.cmaketoolchain:user_toolchain``. If
this conf value is defined, the ``generic_system`` block will include the provided file or files, but
no further define any CMake variable for cross-building.

If ``user_toolchain`` is not defined and Conan detects it is cross-building, because the build
and host profiles contain different OS or architecture, it will try to define the following
variables:

- ``CMAKE_SYSTEM_NAME``: ``tools.cmake.cmaketoolchain:system_name`` configuration if
  defined, otherwise, it will try to autodetect it. This block will consider
  cross-building if Android systems (that is managed by other blocks), and not 64bits to
  32bits builds in x86_64, sparc and ppc systems.
- ``CMAKE_SYSTEM_VERSION``: ``tools.cmake.cmaketoolchain:system_version`` conf if defined, otherwise
  ``os.version`` subsetting (host) when defined
- ``CMAKE_SYSTEM_PROCESSOR``: ``tools.cmake.cmaketoolchain:system_processor`` conf if defined, otherwise
  ``arch`` setting (host) if defined



Reference
---------

.. currentmodule:: conan.tools.cmake.toolchain.toolchain

.. autoclass:: CMakeToolchain
    :members:


conf
^^^^

CMakeToolchain is affected by these ``[conf]`` variables:

- **tools.cmake.cmaketoolchain:toolchain_file** user toolchain file to replace the ``conan_toolchain.cmake`` one.
- **tools.cmake.cmaketoolchain:user_toolchain** list of user toolchains to be included from the ``conan_toolchain.cmake`` file.
- **tools.android:ndk_path** value for ``ANDROID_NDK_PATH``.
- **tools.cmake.cmaketoolchain:system_name** is not necessary in most cases and is only used to force-define ``CMAKE_SYSTEM_NAME``.
- **tools.cmake.cmaketoolchain:system_version** is not necessary in most cases and is only used to force-define ``CMAKE_SYSTEM_VERSION``.
- **tools.cmake.cmaketoolchain:system_processor** is not necessary in most cases and is only used to force-define ``CMAKE_SYSTEM_PROCESSOR``.
- **tools.build:cxxflags** list of extra C++ flags that will be appended to ``CMAKE_CXX_FLAGS_INIT``.
- **tools.build:cflags** list of extra of pure C flags that will be appended to ``CMAKE_C_FLAGS_INIT``.
- **tools.build:sharedlinkflags** list of extra linker flags that will be appended to ``CMAKE_SHARED_LINKER_FLAGS_INIT``.
- **tools.build:exelinkflags** list of extra linker flags that will be appended to ``CMAKE_EXE_LINKER_FLAGS_INIT``.
- **tools.build:defines** list of preprocessor definitions that will be used by ``add_definitions()``.
- **tools.build:tools.apple:enable_bitcode** boolean value to enable/disable Bitcode Apple Clang flags, e.g., ``CMAKE_XCODE_ATTRIBUTE_ENABLE_BITCODE``.
- **tools.build:tools.apple:enable_arc** boolean value to enable/disable ARC Apple Clang flags, e.g., ``CMAKE_XCODE_ATTRIBUTE_CLANG_ENABLE_OBJC_ARC``.
- **tools.build:tools.apple:enable_visibility** boolean value to enable/disable Visibility Apple Clang flags, e.g., ``CMAKE_XCODE_ATTRIBUTE_GCC_SYMBOLS_PRIVATE_EXTERN``.

