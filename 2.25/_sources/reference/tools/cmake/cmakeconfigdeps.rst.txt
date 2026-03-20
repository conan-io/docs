.. _conan_tools_cmakeconfigdeps:

CMakeConfigDeps
===============

.. include:: ../../../common/experimental_warning.inc


This generator (available as experimental from Conan 2.25) is designed as a replacement of the current ``CMakeDeps`` generator, with multiple pending fixes and improvements that couldn't easily be done in the current one without breaking.

.. note::
    
    To simplify the testing and validation of the ``CMakeDeps`` -> ``CMakeConfigDeps`` migration, the ``-c tools.cmake.cmakedeps:new=will_break_next`` configuration can be used. It performs a hot replacement of every ``CMakeDeps`` in recipes by ``CMakeConfigDeps``, without needing to edit the recipes at all. Note that this configuration is not necessary if the recipe explicitly uses ``CMakeConfigDeps``.



That means that it can be used as any other generator in conanfiles, and in command line ``-g CMakeConfigDeps``:

.. code-block::
   :caption: conanfile.txt

   [requires]
   hello/0.1

   [generators]
   CMakeConfigDeps


.. code-block:: python
   :caption: conanfile.py

   class Pkg(ConanFile):
      ...
      requires = "hello/0.1"
      generators = "CMakeConfigDeps"

Or: 

.. code-block:: python
   :caption: conanfile.py

   from conan import ConanFile
   from conan.tools.cmake import CMakeConfigDeps

   class TestConan(ConanFile):
      ...
      requires = "hello/0.1"
    
      def generate(self):
         deps = CMakeConfigDeps(self)
         deps.generate()


The ``CMakeConfigDeps`` generator produces the necessary files for each dependency to be able to use the cmake
``find_package()`` function to locate the dependencies. It can be used like:

.. code-block:: cmake
    :caption: **CMakeLists.txt**
    :emphasize-lines: 4

    cmake_minimum_required(VERSION 3.15)
    project(compressor C)

    find_package(hello CONFIG REQUIRED)

    add_executable(${PROJECT_NAME} src/main.c)
    target_link_libraries(${PROJECT_NAME} hello::hello)


By default, for a ``hello`` requires, you need to use ``find_package(hello)`` and link with the target ``hello::hello``.


Generated files
---------------

- **xxx-config.cmake**: By default, the ``CMakeConfigDeps`` generator will create config files declaring the targets for the dependencies
  and their components (if declared).

- This generator is only intended to generate ``xxx-config.cmake`` config files, it will not generate ``Find*.cmake`` find modules, and support for it is not planned. Use the ``CMakeDeps`` generator for that, or patch the consumers to use CMake config files instead of modules

- **Other necessary *.cmake**:  files like version, flags and directory data or configuration.

- **conan_cmakedeps_paths.cmake**: file containing the definition of ``xxx_DIR`` variables that point to the
  folder containing the ``xxx-config.cmake`` files to be located when doing the ``find_package()``. This file
  will be included by default by the ``conan_toolchain.cmake``, but it might also be useful in other tools like
  ``cmake-conan`` integration. This file will also contain other path variables such as ``CMAKE_VS_DEBUGGER_ENVIRONMENT``, ``CMAKE_PROGRAM_PATH``, ``CMAKE_LIBRARY_PATH``, etc., that help consumers
  to locate dependencies for different scenarios like runtime or with other CMake ``find_program()`` utilities.


Improvements over ``CMakeDeps``
-------------------------------

This is a brief summary of the improvements and fixes of ``CMakeConfigDeps`` over ``CMakeDeps``:

- Creates real ``SHARED/STATIC/INTERFACE IMPORTED`` targets, no more artificial interface targets. The ``CONAN_LIB::`` and other similar targets do not exist anymore.
- Defines ``IMPORTED_CONFIGURATIONS`` for targets.
- ``CONFIG`` definition of dependencies matching the dependency ``Release/Debug/etc`` ``build_type``, no longer using the consumer one.
- Definition of ``IMPORTED_LOCATION`` and ``IMPORTED_IMPLIB`` for library targets.
- Definition of ``LINK_LANGUAGES`` based on the recipe ``languages`` and ``cpp_info/component`` ``languages`` properties.
- All these allows better propagation of linkage requirement and visibility, avoiding some linkage error of transitive shared libraries in Linux.
- Better definition of ``requires`` relationships across components inside the same package and with respect to other packages.
- It doesn't need any ``build_context_activated`` or ``build_context_suffix`` to use ``tool_requires`` dependencies.
- Checking CMake ``COMPONENTS`` definition by default.
- Definition of ``cpp_info/components`` ``.exe`` information (should include the ``.location`` definition too), to define ``EXECUTABLE`` targets that can be run.
- Executables from ``requires`` can also be used in non cross-build scenarios. When a ``tool_requires`` to the same dependency exists, then those executables will have priority.
- Creation of a new ``conan_cmakedeps_paths.cmake`` that contains definitions of ``<pkg>_DIR`` paths for direct finding of the dependencies. This file is also planned to be used in ``cmake-conan`` to extend its usage and avoid some current limitations due to the fact that a CMake driven installation cannot inject a toolchain later.
- Better management of the system OSX Frameworks through ``cpp_info.frameworks``.
- Definition of ``cpp_info/component.package_framework`` information (should include the ``.location`` definition too,
  e.g., ``os.path.join(self.package_folder, "MyFramework.framework", "MyFramework")``) to define the custom OSX Framework library to be linked against.
- Definition of ``self.cpp_info.sources = ["src/mylib.cpp", "src/other.cpp"]`` that will add ``INTERFACE_SOURCES`` to the CMake target to be consumed downstream.



Targets generation
------------------

``CMakeConfigDeps`` can both generate CMake files from the dependencies ``package_info()`` information
or use the in-package ``xxx-config.cmake`` files (when ``self.cpp_info.set_property("cmake_find_mode", "none")`` is defined, that indicates that the generator will not create any files.

This section explains how ``CMakeConfigDeps`` generates CMake targets from the information of the ``package_info()`` dependencies method.

cpp_info
^^^^^^^^

``CMakeConfigDeps`` will use the common :ref:`self.cpp_info<conan_conanfile_model_cppinfo>` fields, like ``includedirs``, ``libs``, etc.
to create and populate the targets the consumers will use.

But besides these common fields, there are a few new fields, exclusively used at the moment by ``CMakeConfigDeps``, that implement some of the new capabilities of this generator that can be defined in the ``cpp_info`` or ``cpp_info.components``:

.. code-block:: python

   # EXPERIMENTAL FIELDS, used exclusively by new CMakeConfigDeps
   self.cpp_info.type  # The type of this artifact "shared-library", "static-library", etc (same as package_type)
   self.cpp_info.location # full location (path and filename with extension) of the artifact or the Apple Framework library one
   self.cpp_info.link_location  # Location of the import library for Windows .lib associated to a dll
   self.cpp_info.languages # same as "languages" attribute, it can be "C", "C++"
   self.cpp_info.exe  # Definition of an executable artifact
   self.cpp_info.package_framework  # Definition of an Apple Framework (new since Conan 2.14)
   self.cpp_info.sources  # List of paths to source files in the package (for packages that provide source code to consumers)


These fields will be auto-deduced from the other ``cpp_info`` and ``components`` definitions, like the ``libs`` or ``libdirs`` fields, but the automatic deduction might have limitations. Defining them explicitly will inhibit the auto deduction and use the value as provided by the recipe.

Declare sources for targets with:

.. code-block:: python

   self.cpp_info.sources = ["src/mylib.cpp", "src/other.cpp"]

This allows packages to provide source code as a dependency to consumers. The paths should be relative to the package folder.
The source files will be added as `INTERFACE_SOURCES` property to the CMake library (or component) target and consumers that
link with this target will compile the sources when building their own targets.


.. _CMakeConfigDeps Properties:

Properties
^^^^^^^^^^

The following properties affect the ``CMakeConfigDeps`` generator:

- **cmake_file_name**: The config file generated for the current package will follow the ``<VALUE>-config.cmake`` pattern,
  so to find the package you write ``find_package(<VALUE>)``.
- **cmake_target_name**: Name of the target to be consumed.
- **cmake_target_aliases**: List of aliases that Conan will create for an already existing target.
- **cmake_find_mode**: Defaulted to ``config``. Possible values are:

  - ``config``: The ``CMakeConfigDeps`` generator will create config scripts for the dependency.
  - ``module``: Not supported, will be ignored and generate only ``xxx-config.cmake`` files (with a warning).
  - ``both``: Not supported, will be ignored and generate only ``xxx-config.cmake`` files (with a warning).
  - ``none``: Won't generate any file. It can be used, for instance, to create a system wrapper package so the consumers find the config files in the CMake installation config path and not in the generated by Conan (because it has been skipped).
- **cmake_build_modules**: List of ``.cmake`` files (path relative to root package folder) that are automatically
  included when the consumer run the ``find_package()``. This property cannot be set in the components, only in the root ``self.cpp_info``.
- **cmake_config_version_compat**: By default ``SameMajorVersion``, it can take the values ``"AnyNewerVersion", "SameMajorVersion", "SameMinorVersion", "ExactVersion"``. It will use that policy in the generated ``<PackageName>ConfigVersion.cmake`` file
- **system_package_version**: version of the package used to generate the ``<PackageName>ConfigVersion.cmake`` file. Can be useful when creating system packages or other wrapper packages, where the conan package version is different to the eventually referenced package version to keep compatibility to ``find_package(<PackageName> <Version>)`` calls.
- **cmake_additional_variables_prefixes**: List of prefixes to be used when creating CMake variables in the config
  files. These variables are created with ``file_name`` as prefix by default, but setting this property will create
  additional variables with the specified prefixes alongside the default ``file_name`` one.
- **cmake_extra_variables**: Dictionary of extra variables to be added to the generated config file.
  The keys of the dictionary are the variable names and the values are the variable values,
  which can be a plain string, a number or a dict-like python object which must specify
  the ``value`` (string/number) , ``cache`` (boolean), ``type`` (CMake cache type) and optionally,
  ``docstring`` (string: defaulted to variable name) and ``force`` (boolean) keys. Note that this has
  less preference over those values defined in the ``tools.cmake.cmaketoolchain:extra_variables`` conf.
- **cmake_link_feature**: Sets the link feature for the generated target. This can be any of the built-in
  link features supported by CMake like ``WHOLE_ARCHIVE`` etc., or a custom one, provided you also set
  the expected ``CMAKE_LINK_LIBRARY_USING_<FEATURE>_SUPPORTED`` and ``CMAKE_LINK_LIBRARY_USING_<FEATURE>`` variables.
  (Possibly using the **cmake_extra_variables** property). Supported when using CMake 3.24 or newer.
  This property performs **no** checks on the given feature, it is up to the recipe author to ensure
  that the feature is usable.


Example:

.. code-block:: python

    def package_info(self):
        ...
        # MyFileName-config.cmake
        self.cpp_info.set_property("cmake_file_name", "MyFileName")
        # Names for targets are absolute, Conan won't add any namespace to the target names automatically
        self.cpp_info.set_property("cmake_target_name", "Foo::Foo")
        # Automatically include the lib/mypkg.cmake file when calling find_package()
        # This property cannot be set in a component.
        self.cpp_info.set_property("cmake_build_modules", [os.path.join("lib", "mypkg.cmake")])

        # Create a new target "MyFooAlias" that is an alias to the "Foo::Foo" target
        self.cpp_info.set_property("cmake_target_aliases", ["MyFooAlias"])

        # Skip this package when generating the files for the whole dependency tree in the consumer
        # note: it will make useless the previous adjustments.
        # self.cpp_info.set_property("cmake_find_mode", "none")

        # Add extra variables to the generated config file
        self.cpp_info.set_property("cmake_extra_variables", {
                                       "FOO": 42,
                                       "CMAKE_GENERATOR_INSTANCE": "${GENERATOR_INSTANCE}/buildTools/",
                                       "CACHE_VAR_DEFAULT_DOC": {"value": "hello world",
                                                                 "cache": True, "type": "STRING"}
                                   })

        self.cpp_info.set_property("cmake_link_feature", "WHOLE_ARCHIVE")

    # Or if using components
    def package_info(self):
        self.cpp_info.components["mycomponent"].set_property("cmake_target_name", "Foo::Var")

        # Create a new target "VarComponent" that is an alias to the "Foo::Var" component target
        self.cpp_info.components["mycomponent"].set_property("cmake_target_aliases", ["VarComponent"])


Using ``CMakeConfigDeps.set_property()`` method you can overwrite the property values set by the
Conan recipes from the consumer. This can be done for every property listed above.

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):

        requires = "zlib/1.3.1"
        ...

        def generate(self):
            deps = CMakeConfigDeps(self)
            # This will require in CMakeLists.txt a 
            # target_link_libraries(mytarget PUBLIC MyZlib::MyZlib)
            deps.set_property("zlib", "cmake_target_name", "MyZlib::MyZlib")
            deps.generate()


You can also use the ``set_property()`` method to invalidate the property values set by
the upstream recipe and use the values that Conan assigns by default. To do so, set the
value ``None`` to the property like ``deps.set_property("zlib", "cmake_target_name", None)``.

After doing this the generated target name for the Zlib library will be ``zlib::zlib``
instead of ``ZLIB::ZLIB`` which is the upstream default target name.

Additionally, `CMakeConfigDeps.set_property()` can also be used for packages that have
components. In this case, you will need to provide the package name along with its
component separated by a double colon (`::`). Here's an example:

.. code-block:: python

    def generate(self):
        deps = CMakeConfigDeps(self)
        deps.set_property("pkg::component", "cmake_target_name", <new_component_target_name>)
        deps.generate()


Configuration
^^^^^^^^^^^^^

Allows to define custom user CMake configuration besides the standard Release, Debug, etc ones.

.. code-block:: python

    def generate(self):
        deps = CMakeConfigDeps(self)
        # By default, ``deps.configuration`` will be ``self.settings.build_type``
        if self.options["hello"].shared:
            # Assuming the current project ``CMakeLists.txt`` defines the ReleasedShared configuration.
            deps.configuration = "ReleaseShared"
        deps.generate()


The ``CMakeConfigDeps`` is a *multi-configuration* generator, it can correctly create files for Release/Debug configurations
to be simultaneously used by IDEs like Visual Studio. In single configuration environments, it is necessary to have
a configuration defined, which must be provided via the ``cmake ... -DCMAKE_BUILD_TYPE=<build-type>`` argument in command line
(Conan will do it automatically when necessary, in the ``CMake.configure()`` helper).


Using "host" and "build" context dependencies
---------------------------------------------

With ``CMakeConfigDeps``, it is possible to use executable ``IMPORTED`` targets from regular "host" dependencies. This can only be done in case where platform binary compatibility is possible, and in other cases like cross-compiling, it will fail.

The ``IMPORTED`` executable targets will be automatically created from the ``self.cpp_info.exe`` and ``self.cpp_info.components["mycomponent"].exe`` information. These targets can be directly used by consumers in their own builds as tools.

When a Conan package recipe depends on the same package both as regular ``requires`` and ``tool-requires``, to be able to implement scenarios like cross-building, the "build" context will have priority when defining the executable ``IMPORTED`` targets. 
A common example is when using ``protobuf`` in a cross-building scenario, the ``protoc`` compiler inside the package that is used for the "host" architecture cannot be executed in the current "build" machine. So the recipe defines a ``self.requires("protobuf/version")`` and a ``self.tool_requires("protobuf/version")``. 
In this case, the library (headers, static/shared lib) targets will be obtained from the dependency in the "host" context, but the executable target for ``protoc`` will be defined from the "build" context.


Disable ``CMakeConfigDeps`` to use ``xxx-config.cmake`` files inside the package
--------------------------------------------------------------------------------

Some projects may want to disable the ``CMakeConfigDeps`` generator for downstream consumers. This can be done by setting ``cmake_find_mode`` to ``"none"``.
If the project wants to provide its own configuration targets, it should append them to the ``builddirs`` attribute of ``cpp_info``.

This method is intended to work with downstream consumers using the ``CMakeToolchain`` generator or by including the generated ``conan_cmakedeps_paths.cmake`` file, which will be populated with the ``builddirs`` attribute.

Example:

.. code-block:: python

    def package(self):
        ...
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none") # Do NOT generate any files
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "foo"))


Reference
---------

.. currentmodule:: conan.tools.cmake.cmakeconfigdeps.cmakeconfigdeps

.. autoclass:: CMakeConfigDeps
    :members:
