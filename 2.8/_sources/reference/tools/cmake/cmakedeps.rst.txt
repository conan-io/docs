.. _conan_tools_cmakedeps:

CMakeDeps
=========


The ``CMakeDeps`` generator produces the necessary files for each dependency to be able to use the cmake
``find_package()`` function to locate the dependencies. It can be used like:


.. code-block:: python

    from conan import ConanFile

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        generators = "CMakeDeps"


The full instantiation, that allows custom configuration can be done in the ``generate()`` method:


.. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"

        def generate(self):
            cmake = CMakeDeps(self)
            cmake.generate()


.. code-block:: cmake
    :caption: **CMakeLists.txt**
    :emphasize-lines: 4

    cmake_minimum_required(VERSION 3.15)
    project(compressor C)

    find_package(hello REQUIRED)

    add_executable(${PROJECT_NAME} src/main.c)
    target_link_libraries(${PROJECT_NAME} hello::hello)


By default, for a ``hello`` requires, you need to use ``find_package(hello)`` and link with the target ``hello::hello``.
Check :ref:`the properties affecting CMakeDeps<CMakeDeps Properties>` like ``cmake_target_name`` to customize the file and
the target names in the conanfile.py of the dependencies and their components.


.. note::

    The ``CMakeDeps`` is intended to run with the ``CMakeToolchain`` generator. It will set ``CMAKE_PREFIX_PATH`` and
    ``CMAKE_MODULE_PATH`` to the right folder (``conanfile.generators_folder``) so CMake can locate the generated config/module files.


Generated files
---------------

- **XXX-config.cmake**: By default, the CMakeDeps generator will create config files declaring the targets for the dependencies
  and their components (if declared).

- **FindXXX.cmake**: Only when the property ``cmake_find_mode`` is set by the dependency with "module" or "both". See :ref:`The properties affecting CMakeDeps<CMakeDeps Properties>` is set in the dependency.

- **Other necessary *.cmake**:  files like version, flags and directory data or configuration.


Note that it will also generate a **conandeps_legacy.cmake** file. This is a file that provides a behavior similar to the Conan 1 ``cmake`` generator, allowing to include this file with ``include(${CMAKE_BINARY_DIR}/generators/conandeps_legacy.cmake)``, and providing a single CMake ``CONANDEPS_LEGACY`` variable that allows to link with all the direct and transitive dependencies without explicitly enumerating them like: ``target_link_libraries(app ${CONANDEPS_LEGACY})``. This is a convenience provided for Conan 1.X users to upgrade to Conan 2 without changing their overall developer flow, but it is not recommended otherwise, and using the CMake canonical flow of explicitly using ``find_package()`` and ``target_link_libraries(... pkg1::pkg1 pkg2::pkg2)`` with targets is the correct approach. 


Customization
-------------

There are some attributes you can adjust in the created ``CMakeDeps`` object to change the default behavior:

configuration
^^^^^^^^^^^^^

Allows to define custom user CMake configuration besides the standard Release, Debug, etc ones.

.. code-block:: python

    def generate(self):
        deps = CMakeDeps(self)
        # By default, ``deps.configuration`` will be ``self.settings.build_type``
        if self.options["hello"].shared:
            # Assuming the current project ``CMakeLists.txt`` defines the ReleasedShared configuration.
            deps.configuration = "ReleaseShared"
        deps.generate()


The ``CMakeDeps`` is a *multi-configuration* generator, it can correctly create files for Release/Debug configurations
to be simultaneously used by IDEs like Visual Studio. In single configuration environments, it is necessary to have
a configuration defined, which must be provided via the ``cmake ... -DCMAKE_BUILD_TYPE=<build-type>`` argument in command line
(Conan will do it automatically when necessary, in the ``CMake.configure()`` helper).


build_context_activated
^^^^^^^^^^^^^^^^^^^^^^^

When you have a **build-require**, by default, the config files (`xxx-config.cmake`) files are not generated.
But you can activate it using the **build_context_activated** attribute:

.. code-block:: python

    tool_requires = ["my_tool/0.0.1"]

    def generate(self):
        cmake = CMakeDeps(self)
        # generate the config files for the tool require
        cmake.build_context_activated = ["my_tool"]
        cmake.generate()


build_context_suffix
^^^^^^^^^^^^^^^^^^^^

When you have the same package as a **build-require** and as a **regular require** it will cause a conflict in the generator
because the file names of the config files will collide as well as the targets names, variables names etc.

For example, this is a typical situation with some requirements (capnproto, protobuf...) that contain
a tool used to generate source code at build time (so it is a **build_require**),
but also providing a library to link to the final application, so you also have a **regular require**.
Solving this conflict is specially important when we are cross-building because the tool
(that will run in the building machine) belongs to a different binary package than the library, that will "run" in the
host machine.

You can use the **build_context_suffix** attribute to specify a suffix for a requirement,
so the files/targets/variables of the requirement in the build context (tool require) will be renamed:

.. code-block:: python

    tool_requires = ["my_tool/0.0.1"]
    requires = ["my_tool/0.0.1"]

    def generate(self):
        cmake = CMakeDeps(self)
        # generate the config files for the tool require
        cmake.build_context_activated = ["my_tool"]
        # disambiguate the files, targets, etc
        cmake.build_context_suffix = {"my_tool": "_BUILD"}
        cmake.generate()



build_context_build_modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Also there is another issue with the **build_modules**. As you may know, the recipes of the requirements can declare a
`cppinfo.build_modules` entry containing one or more **.cmake** files.
When the requirement is found by the cmake ``find_package()``
function, Conan will include automatically these files.

By default, Conan will include only the build modules from the
``host`` context (regular requires) to avoid the collision, but you can change the default behavior.

Use the **build_context_build_modules** attribute to specify require names to include the **build_modules** from
**tool_requires**:

.. code-block:: python

    tool_requires = ["my_tool/0.0.1"]

    def generate(self):
        cmake = CMakeDeps(self)
        # generate the config files for the tool require
        cmake.build_context_activated = ["my_tool"]
        # Choose the build modules from "build" context
        cmake.build_context_build_modules = ["my_tool"]
        cmake.generate()

.. _conan_tools_cmakedeps_check_components_exist:

check_components_exist
++++++++++++++++++++++

.. warning::

  The ``check_components_exist`` attribute is **experimental** and subject to change.


This property is ``False`` by default. Use this property if you want to add a check when
you require specifying components in the consumers' ``find_package()``. For example, if we
are consuming a Conan package like Boost that declares several components. If we set the
attribute to ``True``, the ``find_package()`` call of the consumer, will check that the
required components exist and raise an error otherwise. You can set this attribute in the
``generate()`` method:

.. code-block:: python

    requires = "boost/1.81.0"

    ...

    def generate(self):
        deps = CMakeDeps(self)
        deps.check_components_exist = True
        deps.generate()

Then, when consuming Boost the ``find_package()`` will raise an error as `fakecomp` does
not exist:

..  code-block:: text

    cmake_minimum_required(VERSION 3.15)
    ...
    find_package(Boost COMPONENTS random regex fakecomp REQUIRED)
    ...


Reference
---------


.. currentmodule:: conan.tools.cmake.cmakedeps.cmakedeps

.. autoclass:: CMakeDeps
    :members:


.. _CMakeDeps Properties:

Properties
^^^^^^^^^^

The following properties affect the CMakeDeps generator:

- **cmake_file_name**: The config file generated for the current package will follow the ``<VALUE>-config.cmake`` pattern,
  so to find the package you write ``find_package(<VALUE>)``.
- **cmake_target_name**: Name of the target to be consumed.
- **cmake_target_aliases**: List of aliases that Conan will create for an already existing target.
- **cmake_find_mode**: Defaulted to ``config``. Possible values are:

  - ``config``: The CMakeDeps generator will create config scripts for the dependency.
  - ``module``: Will create module config (FindXXX.cmake) scripts for the dependency.
  - ``both``: Will generate both config and modules.
  - ``none``: Won't generate any file. It can be used, for instance, to create a system wrapper package so the consumers find the config files in the CMake installation config path and not in the generated by Conan (because it has been skipped).

- **cmake_module_file_name**: Same as **cmake_file_name** but when generating modules with ``cmake_find_mode=module/both``. If not specified it will default to **cmake_file_name**.
- **cmake_module_target_name**: Same as **cmake_target_name**  but when generating modules with ``cmake_find_mode=module/both``.  If not specified it will default to **cmake_target_name**.
- **cmake_build_modules**: List of ``.cmake`` files (route relative to root package folder) that are automatically
  included when the consumer run the ``find_package()``. This property cannot be set in the components, only in the root ``self.cpp_info``.
- **cmake_set_interface_link_directories**: boolean value that should be only used by dependencies that don't declare `self.cpp_info.libs` but have ``#pragma comment(lib, "foo")`` (automatic link) declared at the public headers. Those dependencies should
  add this property to their *conanfile.py* files at root ``cpp_info`` level (components not supported for now).
- **nosoname**: boolean value that should be used only by dependencies that are defined as ``SHARED`` and represent a library built without the ``soname`` flag option.
- **cmake_config_version_compat**: By default ``SameMajorVersion``, it can take the values ``"AnyNewerVersion", "SameMajorVersion", "SameMinorVersion", "ExactVersion"``. It will use that policy in the generated ``<PackageName>ConfigVersion.cmake`` file
- **system_package_version**: version of the package used to generate the ``<PackageName>ConfigVersion.cmake`` file. Can be useful when creating system packages or other wrapper packages, where the conan package version is different to the eventually referenced package version to keep compatibility to ``find_package(<PackageName> <Version>)`` calls.
- **cmake_additional_variables_prefixes**: List of prefixes to be used when creating CMake variables in the config
  files. These variables are created with ``file_name`` as prefix by default, but setting this property will create
  additional variables with the specified prefixes alongside the default ``file_name`` one.

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

        self.cpp_info.components["mycomponent"].set_property("cmake_target_name", "Foo::Var")

        # Create a new target "VarComponent" that is an alias to the "Foo::Var" component target
        self.cpp_info.components["mycomponent"].set_property("cmake_target_aliases", ["VarComponent"])

        # Skip this package when generating the files for the whole dependency tree in the consumer
        # note: it will make useless the previous adjustements.
        # self.cpp_info.set_property("cmake_find_mode", "none")

        # Generate both MyFileNameConfig.cmake and FindMyFileName.cmake
        self.cpp_info.set_property("cmake_find_mode", "both")


Overwrite properties from the consumer side using CMakeDeps.set_property()
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Using ``CMakeDeps.set_property()`` method you can overwrite the property values set by the
Conan recipes from the consumer. This can be done for every property listed above,
except for ``cmake_target_aliases``.

Imagine we have a *compressor/1.0* package that depends on *zlib/1.2.11*. The *zlib* recipe
defines some properties:


.. code-block:: python
    :caption: Zlib conanfile.py

    class ZlibConan(ConanFile):
        name = "zlib"

        ...

        def package_info(self):
            self.cpp_info.set_property("cmake_find_mode", "both")
            self.cpp_info.set_property("cmake_file_name", "ZLIB")
            self.cpp_info.set_property("cmake_target_name", "ZLIB::ZLIB")
            ...

This recipe defines several properties. For example the ``cmake_find_mode`` property is
set to ``both``. That means that module and config files are generated for Zlib. Maybe we
need to alter this behaviour and just generate config files. You could do that in the
compressor recipe using the ``CMakeDeps.set_property()`` method:


.. code-block:: python
    :caption: compressor conanfile.py

    class Compressor(ConanFile):
        name = "compressor"

        requires = "zlib/1.2.11"
        ...

        def generate(self):
            deps = CMakeDeps(self)
            deps.set_property("zlib", "cmake_find_mode", "config")
            deps.generate()
            ...

You can also use the ``set_property()`` method to invalidate the property values set by
the upstream recipe and use the values that Conan assigns by default. To do so, set the
value ``None`` to the property like this:

.. code-block:: python
    :caption: compressor conanfile.py

    class Compressor(ConanFile):
        name = "compressor"

        requires = "zlib/1.2.11"
        ...

        def generate(self):
            deps = CMakeDeps(self)
            deps.set_property("zlib", "cmake_target_name", None)
            deps.generate()
            ...

After doing this the generated target name for the Zlib library will be ``zlib::zlib``
instead of ``ZLIB::ZLIB``

Additionally, `CMakeDeps.set_property()` can also be used for packages that have
components. In this case, you will need to provide the package name along with its
component separated by a double colon (`::`). Here's an example:

.. code-block:: python

    def generate(self):
        deps = CMakeDeps(self)
        deps.set_property("pkg::component", "cmake_target_name", <new_component_target_name>)
        deps.generate()
        ...


.. _Disable CMakeDeps For Installed CMake imports:

Disable CMakeDeps For Installed CMake configuration files
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Some projects may want to disable the ``CMakeDeps`` generator for downstream consumers. This can be done by settings ``cmake_find_mode`` to ``none``.
If the project wants to provide its own configuration targets, it should append them to the ``buildirs`` attribute of ``cpp_info``.

This method is intended to work with downstream consumers using the ``CMakeToolchain`` generator, which will be populated with the ``builddirs`` attribute.

Example:

.. code-block:: python

    def package(self):
        ...
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none") # Do NOT generate any files
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "foo"))


Map from project configuration to imported target's configuration
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

As mentioned above, ``CMakeDeps`` provides support for multiple configuration environments (Debug, Release, etc.)
This is achieved by populating properties on the imported targets according to the ``build_type`` setting
when installing dependencies. When a consumer project is configured with a single-configuration CMake generator, however, 
it is necessary to define the ``CMAKE_BUILD_TYPE`` with a value that matches that of the installed dependencies.

If the consumer CMake project is configured with a different build type than the dependencies, it is necessary to
tell CMake how to map the configurations from the current project to the imported targets by setting the 
``CMAKE_MAP_IMPORTED_CONFIG_<CONFIG>`` CMake variable. 

.. code-block:: bash

    cd build-coverage/
    conan install .. -s build_type=Debug
    cmake .. -DCMAKE_BUILD_TYPE=Coverage -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_MAP_IMPORTED_CONFIG_COVERAGE=Debug
