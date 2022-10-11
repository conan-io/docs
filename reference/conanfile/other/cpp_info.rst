.. _conan_conanfile_model_cppinfo:

self.cpp and self.cpp_info
--------------------------

Properties to declare all the information needed by the consumers of a package: include directories,
library names, library paths... Used both for editable packages and regular packages in the cache.


Usage
^^^^^

There are four instances available, only while running the following methods:

- At ``layout(self)`` method:
    - **self.cpp.package**: For a regular package being used from the Conan cache.
    - **self.cpp.source**: For "editable" packages, to describe the artifacts under ``self.source_folder``.
    - **self.cpp.build**: For "editable" packages, to describe the artifacts under ``self.build_folder``.

        .. code-block:: python

            def layout(self):
                ...
                self.folders.source = "src"
                self.folders.build = "build"

                # In the local folder (before a conan create) the artifacts can be found:
                self.cpp.source.includedirs = ["my_includes"]
                self.cpp.build.libdirs = ["lib/x86_64"]
                self.cpp.build.libs = ["foo"]

                # In the Conan cache, we packaged everything at the default standard directories, the library to link
                # is "foo"
                self.cpp.package.libs = ["foo"]


- At ``package_info(self)`` method:
    - **self.cpp_info**: Same as *self.cpp.package* but, at this point, the package contents are in
      ``self.package_folder`` so you can access the artifacts to fill the ``self.cpp_info``, for example, using
      the :ref:`collect_libs()<conan_tools_files_collect_libs>` tool.

        .. code-block:: python

            def package_info(self):
                self.cpp_info.libs = ["foo"]


Attributes
^^^^^^^^^^

+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| NAME                                 | DESCRIPTION                                                                                             |
+======================================+=========================================================================================================+
| .includedirs                         | | Ordered list with include paths. Defaulted to ``["include"]``                                         |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .libdirs                             | | Ordered list with lib paths. Defaulted to ``["lib"]``                                                 |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .resdirs                             | | Ordered list of resource (data) paths. Defaulted to ``["res"]``                                       |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .bindirs                             | | Ordered list with paths to binaries (executables, dynamic libraries,...).                             |
|                                      | | Defaulted to ``["bin"]``                                                                              |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .builddirs                           | | Ordered list with build scripts directory paths. Defaulted to ``[]`` (empty)                          |
|                                      | | CMakeDeps generator will search in these dirs for files like *findXXX.cmake*                          |
|                                      | | or *include("XXX.cmake")*                                                                             |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .libs                                | | Ordered list with the library names, Defaulted to ``[]`` (empty)                                      |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .defines                             | | Preprocessor definitions. Defaulted to ``[]`` (empty)                                                 |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .cflags                              | | Ordered list with pure C flags. Defaulted to ``[]`` (empty)                                           |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .cxxflags                            | | Ordered list with C++ flags. Defaulted to ``[]`` (empty)                                              |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .sharedlinkflags                     | | Ordered list with linker flags (shared libs). Defaulted to ``[]`` (empty)                             |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .exelinkflags                        | | Ordered list with linker flags (executables). Defaulted to ``[]`` (empty)                             |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .frameworks                          | | Ordered list with the framework names (OSX), Defaulted to ``[]`` (empty)                              |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .frameworkdirs                       | | Ordered list with frameworks search paths (OSX). Defaulted to ``["Frameworks"]``                      |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .system_libs                         | | Ordered list with the system library names. Defaulted to ``[]`` (empty)                               |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .components                          | | Dictionary with different components a package may have: libraries,                                   |
|                                      | | executables... See docs below.                                                                        |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .requires                            | | List of components to consume from requirements (it applies only to                                   |
|                                      | | generators that implements components feature).                                                       |
|                                      | | **Warning**: If declared, only the components listed here will used by the                            |
|                                      | | linker and consumers.                                                                                 |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| .objects                             | | List of object libraries (*.obj* or *.o*). Defaulted to ``[]`` (empty)                                |
|                                      | | Only supported by :ref:`CMakeDeps<conan_tools_cmake>` generator                                       |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+

**Simplified accessors to libdirs, bindirs, includedirs:** you can access
``cpp_info.libdirs[0]``, ``cpp_info.bindirs[0]`` and ``cpp_info.includedirs[0]`` using
``cpp_info.libdir``, ``cpp_info.bindir`` and ``cpp_info.includedir``

Properties
^^^^^^^^^^

Any CppInfo object can declare "properties" that can be read by the generators.
The value of a property can be of any type. Check each generator reference to see the properties used on it.

.. code-block:: python

    def set_property(self, property_name, value)
    def get_property(self, property_name):

Example:

.. code-block:: python

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")


Components
^^^^^^^^^^

If your package is composed by more than one library, it is possible to declare components that allow to define a
``CppInfo`` object per each of those libraries and also requirements between them and to components of other packages
(the following case is not a real example):

.. code-block:: python

    def package_info(self):
        self.cpp_info.components["crypto"].set_property("cmake_file_name", "Crypto")
        self.cpp_info.components["crypto"].libs = ["libcrypto"]
        self.cpp_info.components["crypto"].defines = ["DEFINE_CRYPTO=1"]
        self.cpp_info.components["crypto"].requires = ["zlib::zlib"]  # Depends on all components in zlib package

        self.cpp_info.components["ssl"].set_property("cmake_file_name", "SSL")
        self.cpp_info.components["ssl"].includedirs = ["include/headers_ssl"]
        self.cpp_info.components["ssl"].libs = ["libssl"]
        self.cpp_info.components["ssl"].requires = ["crypto",
                                                    "boost::headers"]  # Depends on headers component in boost package

        obj_ext = "obj" if platform.system() == "Windows" else "o"
        self.cpp_info.components["ssl-objs"].objects = [os.path.join("lib", "ssl-object.{}".format(obj_ext))]


Dependencies among components and to components of other requirements can be defined using the ``requires`` attribute and the name
of the component. The dependency graph for components will be calculated and values will be aggregated in the correct order for each field.
