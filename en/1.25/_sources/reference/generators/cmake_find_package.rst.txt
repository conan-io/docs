.. _cmake_cmake_find_package_generator_reference:


cmake_find_package
==================

.. container:: out_reference_box

    This is the reference page for ``cmake_find_package`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.


The ``cmake_find_package`` generator creates a file for each requirement specified in the conanfile.

The name of the files follow the pattern ``Find<PKG-NAME>.cmake``. So for the ``asio/1.14.0`` package,
a ``Findasio.cmake`` file will be generated.

Variables in Find<PKG-NAME>.cmake
---------------------------------

Being ``<PKG-NAME>`` the package name used in the reference (by default) or the one declared in ``cpp_info.name`` or in
``cpp_info.names["cmake_find_package"]`` if specified:

+------------------------------------+-----------------------------------------------------------------------------------------------------+
| NAME                               | VALUE                                                                                               |
+====================================+=====================================================================================================+
| <PKG-NAME>_FOUND                   | Set to 1                                                                                            |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_VERSION                 | Package version                                                                                     |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_INCLUDE_DIRS            | Containing all the include directories of the package                                               |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_INCLUDES                | Same as the XXX_INCLUDE_DIRS                                                                        |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_DEFINITIONS             | Definitions of the library                                                                          |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_LIBS                    | Library paths to link                                                                               |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_LIBRARIES               | Same as <PKG-NAME>_LIBS                                                                             |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_BUILD_MODULES           | List of CMake module files with functionalities for consumers                                       |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_SYSTEM_LIBS             | System libraries to link                                                                            |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_FRAMEWORKS              | Framework names to do a `find_library()`                                                            |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_FRAMEWORKS_FOUND        | Found frameworks to link with after `find_library()`                                                |
+------------------------------------+-----------------------------------------------------------------------------------------------------+
| <PKG-NAME>_FRAMEWORK_DIRS          | Framework directories to perform the `find_library()` of <PKG-NAME>_FRAMEWORKS                      |
+------------------------------------+-----------------------------------------------------------------------------------------------------+

This file uses `<PKG-NAME>_BUILD_MODULES` values to include the files using the `include(...)` CMake directive. This makes functions or
utilities exported by the package available for consumers just by setting `find_package(<PKG-NAME>)` in the *CMakeLists.txt*.

Moreover, this also adjusts `CMAKE_MODULE_PATH` and `CMAKE_PREFIX_PATH` to the values declared by the package in ``cpp_info.buildirs``, so
modules in those directories can be found.

Target in Find<PKG-NAME>.cmake
------------------------------

A target named ``<PKG-NAME>::<PKG-NAME>`` target is generated with the following properties adjusted:

- ``INTERFACE_INCLUDE_DIRECTORIES``: Containing all the include directories of the package.
- ``INTERFACE_LINK_LIBRARIES``: Library paths to link.
- ``INTERFACE_COMPILE_DEFINITIONS``: Definitions of the library.

The targets are transitive. So, if your project depends on a packages ``A`` and ``B``, and at the same time
``A`` depends on ``C``, the ``A`` target will contain automatically the properties of the ``C`` dependency, so
in your `CMakeLists.txt` file you only need to ``find_package(A)`` and ``find_package(B)``.
