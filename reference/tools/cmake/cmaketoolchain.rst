.. _conan-cmake-toolchain:
.. _conan_tools_cmaketoolchain:

CMakeToolchain
==============


The ``CMakeToolchain`` is the toolchain generator for CMake. It produces the toolchain file that can be used in the
command line invocation of CMake with the ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake``. This generator translates
the current package configuration, settings, and options, into CMake toolchain syntax.


It can be declared as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        generators = "CMakeToolchain"

Or fully instantiated in the ``generate()`` method:

.. code-block:: python

    from conan import ConanFile
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
  - Definition of ``CMAKE_VS_DEBUGGER_ENVIRONMENT`` when on Windows with Visual Studio.
    This sets up the ``PATH`` environment variable to point to directories containing DLLs,
    to allow debugging directly from the Visual Studio IDE without copying DLLs (requires CMake 3.27).
  - Definition of ``CONAN_RUNTIME_LIB_DIRS`` to allow collecting runtime dependencies (shared libraries),
    see below for details.

- **conanvcvars.bat**: In some cases, the Visual Studio environment needs to be defined correctly for building,
  like when using the Ninja or NMake generators. If necessary, the ``CMakeToolchain`` will generate this script,
  so defining the correct Visual Studio prompt is easier.


- **CMakePresets.json**: This toolchain generates a standard `CMakePresets.json` file. For
  more information, refer to the documentation `here
  <https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html>`_. It currently uses
  version "3" of the JSON schema. Conan adds *configure*, *build*, and *test* preset
  entries to the JSON file:

    - `configurePresets` storing the following information:
        - The `generator` to be used.
        - The path to the `conan_toolchain.cmake`.
        - Cache variables corresponding to the specified settings that cannot work if
          specified in the toolchain.
        - The `CMAKE_BUILD_TYPE` variable for single-configuration generators.
        - The `BUILD_TESTING` variable set to `OFF` when the configuration
          `tools.build:skip_test` is true.
        - An environment section, setting all the environment information related to the
          :ref:`VirtualBuildEnv<conan_tools_env_virtualbuildenv>`, if applicable. This
          environment can be modified in the `generate()` method of the recipe by passing
          an environment through the `CMakeToolchain.presets_build_environment` attribute.
          Generation of this section can be skipped by using the
          `tools.cmake.cmaketoolchain:presets_environment` configuration.
        - By default, preset names will be `conan-xxxx`, but the "conan-" prefix can be
          customized with the `CMakeToolchain.presets_prefix = "conan"` attribute.
        - Preset names are controlled by the `layout()` `self.folders.build_folder_vars`
          definition, which can contain a list of settings, options,
          ``self.name`` and ``self.version`` and constants ``const.xxx`` like
          `["settings.compiler", "settings.arch", "options.shared", "const.myname"]`.
        - If CMake is found as a direct `tool_requires` dependency, or if
          `tools.cmake:cmake_program` is set, the configure preset will include a
          `cmakeExecutable` field. This field represents the path to the CMake executable
          to be used for this preset. As stated in the CMake documentation, this field is
          reserved for use by IDEs and is not utilized by CMake itself.


    - `buildPresets` storing the following information:
        - The `configurePreset` associated with this build preset.

    - `testPresets` storing the following information:
        - The `configurePreset` associated with this build preset.
        - An environment section, setting all the environment information related to the
          :ref:`VirtualRunEnv<conan_tools_env_virtualrunenv>`, if applicable. This
          environment can be modified in the `generate()` method of the recipe by passing
          an environment through the `CMakeToolchain.presets_run_environment` attribute.
          Please note that since this preset inherits from a `configurePreset`, it will
          also inherit its environment. Generation of this section can be skipped by using
          the`tools.cmake.cmaketoolchain:presets_environment` configuration.

- **CMakeUserPresets.json**:  If you declare a ``layout()`` in the recipe and your
  ``CMakeLists.txt`` file is found at the ``conanfile.source_folder`` folder, a
  ``CMakeUserPresets.json`` file will be generated (if doesn't exist already) including
  automatically the ``CMakePresets.json`` (at the ``conanfile.generators_folder``) to
  allow your IDE (Visual Studio, Visual Studio Code, CLion...) or ``cmake`` tool to locate
  the ``CMakePresets.json``. The location of the generated ``CMakeUserPresets.json`` can
  be further tweaked by the ``user_presets_path`` attribute, as documented below. The
  version schema of the generated ``CMakeUserPresets.json`` is "4" and requires CMake >=
  3.23.
  The file name of this file can be configured with the ``CMakeToolchain.user_presets_path = "CMakeUserPresets.json"```
  attribute, so if you want to generate a "ConanPresets.json" instead to be included from your own file, 
  you can define ``tc.user_presets_path = "ConanPresets.json"`` in the ``generate()`` method.
  See :ref:`extending your own CMake presets<examples-tools-cmake-toolchain-build-project-extend-presets>` for a full example.

  **Note:** Conan will skip the generation of the ``CMakeUserPresets.json`` if it already exists and was not
  generated by Conan.
  
  **Note:** To list all available presets, use the ``cmake --list-presets`` command:

.. note::

    The version schema of the generated ``CMakeUserPresets.json`` is 4 (compatible
    with CMake>=3.23) and the schema for the ``CMakePresets.json`` is 3 (compatible with
    CMake>=3.21).


CONAN_RUNTIME_LIB_DIRS
^^^^^^^^^^^^^^^^^^^^^^

This variable in the generated ``conan_toolchain.cmake`` file contains a list of directories 
that contain runtime libraries (like DLLs)
from all dependencies in the host context. This is intended to be used when relying on 
CMake functionality to collect shared libraries to create a relocatable bundle, as
per the example below.


Just pass the ``CONAN_RUNTIME_LIB_DIRS`` variable to the ``DIRECTORIES`` argument
in the ``install(RUNTIME_DEPENDENCY_SET ...)``` invocation. 

.. code:: cmake

    install(RUNTIME_DEPENDENCY_SET my_app_deps
        PRE_EXCLUDE_REGEXES
            [[api-ms-win-.*]]
            [[ext-ms-.*]]
            [[kernel32\.dll]]
            [[libc\.so\..*]] [[libgcc_s\.so\..*]] [[libm\.so\..*]] [[libstdc\+\+\.so\..*]]
        POST_EXCLUDE_REGEXES
            [[.*/system32/.*\.dll]]
            [[^/lib.*]]
            [[^/usr/lib.*]]
        DIRECTORIES ${CONAN_RUNTIME_LIB_DIRS}
    )


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
        # Setting to None will add the definition with no value
        tc.preprocessor_definitions["NOVALUE_DEF"] = None
        tc.generate()

This will be translated to:

- One ``add_compile_definitions()`` definition for ``MYDEF`` in ``conan_toolchain.cmake`` file.
- One ``add_compile_definitions()`` definition, using a cmake generator expression in ``conan_toolchain.cmake`` file,
  using the different values for different configurations.

.. _conan-cmake-toolchain-cache_variables:

cache_variables
^^^^^^^^^^^^^^^

This attribute allows defining CMake cache-variables. These variables, unlike the ``variables``, are single-config. They
will be stored in the ``CMakePresets.json`` file (at the `cacheVariables` in the `configurePreset`) and will be
applied with ``-D`` arguments when calling ``cmake.configure`` using the :ref:`CMake() build helper<conan_tools_cmake>`.


.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["foo"] = True
        tc.cache_variables["foo2"] = False
        tc.cache_variables["var"] = "23"

The booleans assigned to a cache_variable will be translated to ``ON`` and ``OFF`` symbols in CMake.

variables
^^^^^^^^^

This attribute allows defining CMake variables, for multiple configurations (Debug,
Release, etc). These variables should be used to define things related to the toolchain
and for the majority of cases
:ref:`cache_variables<conan-cmake-toolchain-cache_variables>` is what you probably want to
use. Also, take into account that as these variables are defined inside the
*conan_toolchain.cmake* file, and the toolchain is loaded several times by CMake, the
definition of these variables will be done at those points as well.

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


user_presets_path
^^^^^^^^^^^^^^^^^

This attribute allows specifying the location of the generated ``CMakeUserPresets.json`` file.
Accepted values:

- An absolute path
- A path relative to ``self.source_folder``
- The boolean value ``False``, to suppress the generation of the file altogether.

For example, we can prevent the generator from creating ``CMakeUserPresets.json`` in the 
following way:

.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.user_presets_path = False
        tc.generate()

It's also possible to use the ``tools.cmake.cmaketoolchain:user_presets`` experimental configuration to
change the name and location of the ``CMakeUserPresets.json`` file. Assigning it to an empty string will disable the generation of the file. Please check the :ref:`conf section<conan-cmake-toolchain_conf>` for more information.

presets_build_environment, presets_run_environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These attributes enable the modification of the build and run environments associated with 
the presets, respectively, by assigning an 
:ref:`Environment<conan_tools_env_environment_model>`. This can be accomplished in the 
`generate()` method.

For example, you can override the value of an environment variable already set in the 
build environment:

.. code:: python

    def generate(self):
        buildenv = VirtualBuildEnv(self)
        buildenv.environment().define("MY_BUILD_VAR", "MY_BUILDVAR_VALUE_OVERRIDDEN")
        buildenv.generate()

        tc = CMakeToolchain(self)
        tc.presets_build_environment = buildenv.environment()
        tc.generate()

Or generate a new environment and compose it with an already existing one:

.. code:: python

    def generate(self):
        runenv = VirtualRunEnv(self)
        runenv.environment().define("MY_RUN_VAR", "MY_RUNVAR_SET_IN_GENERATE")
        runenv.generate()

        env = Environment()
        env.define("MY_ENV_VAR", "MY_ENV_VAR_VALUE")
        env = env.vars(self, scope="run")
        env.save_script("other_env")

        tc = CMakeToolchain(self)
        tc.presets_run_environment = runenv.environment().compose_env(env)
        tc.generate()


Extra compilation flags
^^^^^^^^^^^^^^^^^^^^^^^

You can use the following attributes to append extra compilation flags to the toolchain:

- **extra_cxxflags** (defaulted to ``[]``) for additional cxxflags
- **extra_cflags** (defaulted to ``[]``) for additional cflags
- **extra_sharedlinkflags** (defaulted to ``[]``) for additional shared link flags
- **extra_exelinkflags** (defaulted to ``[]``) for additional exe link flags

.. note::

    **flags order of preference**: Flags specified in the `tools.build` configuration,
    such as `cxxflags`, `cflags`, `sharedlinkflags` and `exelinkflags`, will
    always take precedence over those set by the CMakeToolchain attributes.


presets_prefix
^^^^^^^^^^^^^^

By default it is ``"conan"``, and it will generate CMake presets named "conan-xxxx".
This is done to avoid potential name clashes with users own presets.


absolute_paths
^^^^^^^^^^^^^^

By default, ``CMakeToolchain`` will generate relative paths. For example the ``CMakeUserPresets.json`` will have a
relative path to the included ``CMakePresets.json`` (both files generated by ``CMakeToolchain``), and the 
``CMakePresets.json`` file will have a relative path to the ``conan_toolchain.cmake`` file defined in its ``toolchainFile``
field, that will be relative to the build folder, as specified by the CMake presets documentation.

If for some reason using absolute paths was desired, it is possible to do it with:

.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.absolute_paths = True
        tc.generate()



.. _conan_cmake_user_toolchain:

Using a custom toolchain file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two ways of providing custom CMake toolchain files:

- The ``conan_toolchain.cmake`` file can be completely skipped and replaced by a user one, defining the
  ``tools.cmake.cmaketoolchain:toolchain_file=<filepath>`` configuration value. Note this approach will translate
  all the toolchain responsibility to the user provided toolchain, but things like locating the necessary ``xxx-config.cmake``
  files from dependencies can be challenging without some help. For this reason, using the following
  ``tools.cmake.cmaketoolchain:user_toolchain`` is recommended in most cases, and if necessary, 
  using ``tools.cmake.cmaketoolchain:enabled_blocks`` can be used.
- A custom user toolchain file can be added (included from) to the ``conan_toolchain.cmake`` one, by using the
  ``user_toolchain`` block described below, and defining the ``tools.cmake.cmaketoolchain:user_toolchain=["<filepath>"]``
  configuration value.

  The configuration ``tools.cmake.cmaketoolchain:user_toolchain=["<filepath>"]`` can be defined in the ``global.conf``.
  but also creating a Conan package for your toolchain and using ``self.conf_info`` to declare the toolchain file:

    .. code:: python

        import os
        from conan import ConanFile
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
        from conan import ConanFile
        class MyToolRequire(ConanFile):
            ...
            def package_info(self):
                f = os.path.join(self.package_folder, "mytoolchain.cmake")
                # Appending the value to any existing one
                self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", f)


  So, they'll be automatically applied by your ``CMakeToolchain`` generator without writing any extra code:

    .. code:: python

        from conan import ConanFile
        from conan.tools.cmake import CMake
        class Pkg(ConanFile):
            settings = "os", "compiler", "arch", "build_type"
            exports_sources = "CMakeLists.txt"
            tool_requires = "toolchain1/0.1", "toolchain2/0.1"
            generators = "CMakeToolchain"

            def build(self):
                cmake = CMake(self)
                cmake.configure()


.. note::

    **Important notes**

    - In most cases, ``tools.cmake.cmaketoolchain:user_toolchain`` will be preferred over ``tools.cmake.cmaketoolchain:toolchain_file``
    - The ``user_toolchain`` files can define variables for cross-building, such as ``CMAKE_SYSTEM_NAME``, ``CMAKE_SYSTEM_VERSION``
      and ``CMAKE_SYSTEM_PROCESSOR``. If these variables are defined in the user toolchain file, they will be respected, and the 
      ``conan_toolchain.cmake`` deduced ones will not overwrite the user defined ones. If those variables are not defined in the
      user toolchain file, then the Conan automatically deduced ones will be used. Those variables defined in the ``user_toolchain``
      files will also have higher precedence than the configuration defined ones like ``tools.cmake.cmaketoolchain:system_name``.
    - The usage of ``tools.cmake.cmaketoolchain:enabled_blocks`` can be used together with ``tools.cmake.cmaketoolchain:user_toolchain``
      to enable only certain blocks but avoid CMakeToolchain to override CMake values defined in the user toolchain
      file.


Extending and advanced customization
------------------------------------

``CMakeToolchain`` implements a powerful capability for extending and customizing the resulting toolchain file.

The contents are organized by ``blocks`` that can be customized. The following predefined blocks are available,
and added in this order:

- **user_toolchain**: Allows to include user toolchains from the ``conan_toolchain.cmake`` file.
  If the configuration ``tools.cmake.cmaketoolchain:user_toolchain=["xxxx", "yyyy"]`` is defined, its values will be ``include(xxx)\ninclude(yyyy)`` as the
  first lines in ``conan_toolchain.cmake``.
- **generic_system**: Defines ``CMAKE_SYSTEM_NAME``, ``CMAKE_SYSTEM_VERSION``, ``CMAKE_SYSTEM_PROCESSOR``,
  ``CMAKE_GENERATOR_PLATFORM``, ``CMAKE_GENERATOR_TOOLSET``
- **compilers**: Defines ``CMAKE_<LANG>_COMPILER`` for different languages, as defined by ``tools.build:compiler_executables`` configuration.
- **android_system**: Defines ``ANDROID_PLATFORM``, ``ANDROID_STL``, ``ANDROID_ABI`` and includes ``ANDROID_NDK_PATH/build/cmake/android.toolchain.cmake``
  where ``ANDROID_NDK_PATH`` comes defined in ``tools.android:ndk_path`` configuration value.
- **apple_system**: Defines ``CMAKE_OSX_ARCHITECTURES`` (see the :ref:`universal binaries section<conan_tools_cmaketoolchain_universal_binaries>`), ``CMAKE_OSX_SYSROOT`` for Apple systems.
- **fpic**: Defines the ``CMAKE_POSITION_INDEPENDENT_CODE`` when there is a ``options.fPIC``
- **arch_flags**: Defines C/C++ flags like ``-m32, -m64`` when necessary.
- **linker_scripts**: Defines the flags for any provided linker scripts.
- **libcxx**: Defines ``-stdlib=libc++`` flag when necessary as well as ``_GLIBCXX_USE_CXX11_ABI``.
- **vs_runtime**: Defines the ``CMAKE_MSVC_RUNTIME_LIBRARY`` variable, as a generator expression for multiple configurations.
- **vs_debugger_environment**: Defines ``CMAKE_VS_DEBUGGER_ENVIRONMENT`` from "bindirs" folders of dependencies, exclusively for Visual Studio.
- **cppstd**: defines ``CMAKE_CXX_STANDARD``, ``CMAKE_CXX_EXTENSIONS``
- **parallel**: defines ``/MP`` parallel build flag for Visual.
- **extra_flags**: Adds extra definitions, compile and link flags from ``tools.build:cxxflags``, ``tools.build:cflags``, ``tools.build:defines``, ``tools.build:sharedlinkflags``, etc.
- **cmake_flags_init**: defines ``CMAKE_XXX_FLAGS`` variables based on previously defined Conan variables. The blocks above only define ``CONAN_XXX`` variables, and this block will define CMake ones like ``set(CMAKE_CXX_FLAGS_INIT "${CONAN_CXX_FLAGS}" CACHE STRING "" FORCE)```.
- **extra_variables**: Definition of extra CMake variables from ``tools.cmake.cmaketoolchain:extra_variables``
- **try_compile**: Stop processing the toolchain, skipping the blocks below this one, if ``IN_TRY_COMPILE`` CMake property is defined.
- **find_paths**: Defines ``CMAKE_FIND_PACKAGE_PREFER_CONFIG``, ``CMAKE_MODULE_PATH``, ``CMAKE_PREFIX_PATH`` so the generated files from ``CMakeDeps`` are found.
- **pkg_config**: Defines ``PKG_CONFIG_EXECUTABLE`` based on ``tools.gnu:pkg_config`` and adds ``CMAKE_CURRENT_LIST_DIR`` to ``ENV{PKG_CONFIG_PATH}`` to let pkg-config find generated .pc files.
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
        It is **not valid** to change the self.cpp_info  at the ``package_info()`` method, the ``self.cpp.package``
        needs to be defined instead.

- **variables**: Define CMake variables from the ``CMakeToolchain.variables`` attribute.
- **preprocessor**: Define preprocessor directives from ``CMakeToolchain.preprocessor_definitions`` attribute


Customizing the content blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every block can be customized in different ways (recall to call ``tc.generate()`` after the customization):

.. code:: python

    # tc.generate() should be called at the end of every one

    # remove an existing block, the generated conan_toolchain.cmake
    # will not contain code for that block at all
    def generate(self):
        tc = CMakeToolchain(self)
        tc.blocks.remove("generic_system")

    # remove several blocks
    def generate(self):
        tc = CMakeToolchain(self)
        tc.blocks.remove("generic_system", "cmake_flags_init")

    # LEGACY: keep one block, remove all the others
    # If you want to generate conan_toolchain.cmake with only that
    # block. Use "tc.blocks.enabled()" instead
    def generate(self):
        tc = CMakeToolchain(self)
        # this still leaves blocks "variables" and "preprocessor"
        # use "tc.blocks.enabled()"" instead
        tc.blocks.select("generic_system")

    # LEGACY: keep several blocks, remove the other blocks
    # Use "tc.blocks.enabled()" instead
    def generate(self):
        tc = CMakeToolchain(self)
        # this still leaves blocks "variables" and "preprocessor"
        # use "tc.blocks.enabled()" instead
        tc.blocks.select("generic_system", "cmake_flags_init")

    # keep several blocks, remove the other blocks
    # This can be done from configuration with 
    # tools.cmake.cmaketoolchain:enabled_blocs
    def generate(self):
        tc = CMakeToolchain(self)
        # Discard all the other blocks except ``generic_system``
        tc.blocks.enabled("generic_system")

    # iterate blocks
    def generate(self):
        tc = CMakeToolchain(self)
        for block_name in tc.blocks.keys():
            # do something with block_name
        for block_name, block in tc.blocks.items():
            # do something with block_name and block

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


It is possible to select which blocks are active from configuration in profiles, using the
``tools.cmake.cmaketoolchain:enabled_blocks`` configuration. This is a list of blocks, so doing:

.. code-block::

    [conf]
    tools.cmake.cmaketoolchain:enabled_blocks=["generic_system"]

Will leave only the ``generic_system`` block, and discard all others.
This feature can be used for example when users are providing their own toolchain files, and they don't
need Conan ``CMakeToolchain`` to define any flags or CMake variables, except for the necessary paths so
dependencies can be found. For this case, it should be possible to do something like:


.. code-block::

    [conf]
    tools.cmake.cmaketoolchain:user_toolchain+=my_user_toolchain.cmake
    tools.cmake.cmaketoolchain:enabled_blocks=["find_paths"]


For more information about these blocks, please have a look at the source code.

Finding dependencies paths
--------------------------

The generated ``conan_toolchain.cmake`` contains information in its ``find_paths`` block for variables such as
``CMAKE_PROGRAM_PATH``, ``CMAKE_LIBRARY_PATH``, ``CMAKE_INCLUDE_PATH`` and others, that allow CMake to run
``find_program()``, ``find_file()`` and other special "finder" routines that find artifacts without a explicit
package and targets definition via the overall recommended ``find_package()``.

With the new incubating ``CMakeConfigDeps``, the ``conan_toolchain.cmake`` block ``find_paths`` no longer
defines the information itself, but it just loads a new file generated by the ``CMakeConfigDeps`` generator, the
``conan_cmakedeps_paths.cmake`` file. This way, the responsibility for creating information about dependencies is
the ``CMakeConfigDeps`` generator, and that new file can be used in some scenarios in which passing a toolchain
is not possible.


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
  ``os.version`` subsetting (host) when defined. On Apple systems, this ``os.version`` is converted to the corresponding Darwin version.
- ``CMAKE_SYSTEM_PROCESSOR``: ``tools.cmake.cmaketoolchain:system_processor`` conf if defined, otherwise
  ``arch`` setting (host) if defined

.. _conan_tools_cmaketoolchain_universal_binaries:

Support for Universal Binaries in macOS
---------------------------------------

.. include:: ../../../common/experimental_warning.inc

Starting in Conan 2.2.0, there's preliminary support for building universal binaries on
macOS using CMakeToolchain. To specify multiple architectures for a universal binary in
Conan, use the `|` separator when defining the architecture in the settings. This approach
enables passing a list of architectures. For example, running:

.. code:: bash

    conan create . --name=mylibrary --version=1.0 -s="arch=armv8|x86_64"

will create a universal binary for *mylibrary* containing both ``armv8`` and ``x86_64``
architectures, by setting ``CMAKE_OSX_ARCHITECTURES`` with a value of ``arm64;x86_64`` in
the *conan_toolchain.cmake* file.

.. warning::

    It is important to note that this method is not applicable to build systems other than
    CMake.

    Be aware that this feature is primarily beneficial for building final univeral
    binaries for release purposes. The default Conan behavior of managing one binary per
    architecture generally provides a more reliable and trouble-free experience. Users
    should be cautious and not overly rely on this feature for broader use cases.


Reference
---------

.. currentmodule:: conan.tools.cmake.toolchain.toolchain

.. autoclass:: CMakeToolchain
    :members:

.. _conan-cmake-toolchain_conf:

conf
^^^^

CMakeToolchain is affected by these ``[conf]`` variables:

- **tools.cmake.cmaketoolchain:toolchain_file** user toolchain file to replace the ``conan_toolchain.cmake`` one.
- **tools.cmake.cmaketoolchain:user_toolchain** list of user toolchains to be included from the ``conan_toolchain.cmake`` file.
- **tools.android:ndk_path** value for ``ANDROID_NDK_PATH``.
- **tools.android:cmake_legacy_toolchain**: boolean value for ``ANDROID_USE_LEGACY_TOOLCHAIN_FILE``. It will only be defined in ``conan_toolchain.cmake`` if given a value. This is 
  taken into account by the CMake toolchain inside the Android NDK specified in the ``tools.android:ndk_path`` config, for versions ``r23c`` and above. 
  It may be useful to set this to ``False`` if compiler flags are defined via ``tools.build:cflags`` or ``tools.build:cxxflags`` to prevent Android's legacy CMake toolchain 
  from overriding the values. If setting this to ``False``, please ensure you are using CMake 3.21 or above.
- **tools.cmake.cmaketoolchain:system_name** is not necessary in most cases and is only used to force-define ``CMAKE_SYSTEM_NAME``.
- **tools.cmake.cmaketoolchain:system_version** is not necessary in most cases and is only used to force-define ``CMAKE_SYSTEM_VERSION``.
- **tools.cmake.cmaketoolchain:system_processor** is not necessary in most cases and is only used to force-define ``CMAKE_SYSTEM_PROCESSOR``.
- **tools.cmake.cmaketoolchain:enabled_blocks** define which blocks are enabled and discard the others.
- **tools.cmake.cmaketoolchain:extra_variables**: dict-like python object which specifies the CMake variable name and value. The value can be a plain string, a number or a dict-like python object which must specify the ``value`` (string/number) , ``cache`` (boolean), ``type`` (CMake cache type) and optionally, ``docstring`` (string: defaulted to variable name) and ``force`` (boolean) keys. It can override CMakeToolchain defined variables, for which users are at their own risk. E.g.
    
.. code-block:: text

    [conf]
    tools.cmake.cmaketoolchain:extra_variables={'MY_CMAKE_VAR': 'MyValue'}

Resulting in:

.. code-block:: cmake

    set(MY_CMAKE_VAR "MyValue")

Which will be injected later so it can override default Conan variables.

Another advanced usage:

.. code-block:: text

    tools.cmake.cmaketoolchain:extra_variables={'MyIntegerVariable': 42, 'CMAKE_GENERATOR_INSTANCE': '${ENV}/buildTools/'}
    tools.cmake.cmaketoolchain:extra_variables*={'CACHED_VAR': {'value': '/var/run', 'cache': True, 'type': 'PATH', 'docstring': 'test cache var', 'force': True}}

Resulting in:

.. code-block:: cmake

    set(MyIntegerVariable 42)
    set(CMAKE_GENERATOR_INSTANCE "${ENV}/buildTools/")
    set(CACHED_VAR "/var/run" CACHE BOOL "test cache var" FORCE)

This block injects ``$`` which will be expanded later. It also defines a cache variable of type ``PATH``.

.. tip::

    Use the :ref:`configuration data operator<configuration_data_operators>` ``*=`` to **update** (instead of redefining) conf variables already set in profiles or the global configuration.

- **tools.cmake.cmaketoolchain:toolset_arch**: Will add the ``,host=xxx`` specifier in the ``CMAKE_GENERATOR_TOOLSET`` variable of ``conan_toolchain.cmake`` file.
- **tools.cmake.cmaketoolchain:toolset_cuda**: (Experimental) Will add the ``,cuda=xxx`` specifier in the ``CMAKE_GENERATOR_TOOLSET`` variable of ``conan_toolchain.cmake`` file.
- **tools.cmake.cmake_layout:build_folder_vars**: Settings, Options, ``self.name`` and ``self.version`` and constants ``const.uservalue`` that will produce a different build folder and different CMake presets names.
- **tools.cmake.cmaketoolchain:presets_environment**: Set to ``'disabled'`` to prevent the addition of the environment section to the generated CMake presets.
- **tools.cmake.cmaketoolchain:user_presets**: (Experimental) Allows setting a custom name or subfolder for the `CMakeUserPresets.json` file. An empty string disables file generation entirely.
- **tools.build:cxxflags** list of extra C++ flags that will be appended to ``CMAKE_CXX_FLAGS_INIT``.
- **tools.build:cflags** list of extra of pure C flags that will be appended to ``CMAKE_C_FLAGS_INIT``.
- **tools.build:sharedlinkflags** list of extra linker flags that will be appended to ``CMAKE_SHARED_LINKER_FLAGS_INIT``.
- **tools.build:exelinkflags** list of extra linker flags that will be appended to ``CMAKE_EXE_LINKER_FLAGS_INIT``.
- **tools.build:defines** list of preprocessor definitions that will be used by ``add_definitions()``.
- **tools.apple:sdk_path** value for ``CMAKE_OSX_SYSROOT``. In the general case it's not needed and will be passed to CMake by the settings values.
- **tools.apple:enable_bitcode** boolean value to enable/disable Bitcode Apple Clang flags, e.g., ``CMAKE_XCODE_ATTRIBUTE_ENABLE_BITCODE``.
- **tools.apple:enable_arc** boolean value to enable/disable ARC Apple Clang flags, e.g., ``CMAKE_XCODE_ATTRIBUTE_CLANG_ENABLE_OBJC_ARC``.
- **tools.apple:enable_visibility** boolean value to enable/disable Visibility Apple Clang flags, e.g., ``CMAKE_XCODE_ATTRIBUTE_GCC_SYMBOLS_PRIVATE_EXTERN``.
- **tools.build:sysroot** defines the value of ``CMAKE_SYSROOT``.
- **tools.microsoft:winsdk_version** Defines the ``CMAKE_SYSTEM_VERSION`` or the ``CMAKE_GENERATOR_PLATFORM`` according to CMake policy ``CMP0149``.
- **tools.build:compiler_executables** dict-like Python object which specifies the
  compiler as key and the compiler executable path as value. Those keys will be mapped as
  follows:

  * ``c``: will set ``CMAKE_C_COMPILER`` in *conan_toolchain.cmake*.
  * ``cpp``: will set ``CMAKE_CXX_COMPILER`` in *conan_toolchain.cmake*.
  * ``RC``: will set ``CMAKE_RC_COMPILER`` in *conan_toolchain.cmake*.
  * ``objc``: will set ``CMAKE_OBJC_COMPILER`` in *conan_toolchain.cmake*.
  * ``objcpp``: will set ``CMAKE_OBJCXX_COMPILER`` in *conan_toolchain.cmake*.
  * ``cuda``: will set ``CMAKE_CUDA_COMPILER`` in *conan_toolchain.cmake*.
  * ``fortran``: will set ``CMAKE_Fortran_COMPILER`` in *conan_toolchain.cmake*.
  * ``asm``: will set ``CMAKE_ASM_COMPILER`` in *conan_toolchain.cmake*.
  * ``hip``: will set ``CMAKE_HIP_COMPILER`` in *conan_toolchain.cmake*.
  * ``ispc``: will set ``CMAKE_ISPC_COMPILER`` in *conan_toolchain.cmake*.
