.. _cmake_cmake_find_package_multi_generator_reference:


`cmake_find_package_multi`
==========================

.. container:: out_reference_box

    This is the reference page for ``cmake_find_package_multi`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.



Generated files
---------------

For each conan package in your graph, it will generate 1 file and 1 more per different ``build_type``.
Being {name} the package name and

+--------------------------------+--------------------------------------------------------------------------------------+
| NAME                           | CONTENTS                                                                             |
+================================+======================================================================================+
| Find{name}.cmake               | It include the following files and aggregates all the information                    |
+--------------------------------+--------------------------------------------------------------------------------------+
| Find{name}-Release.cmake       | Specific information for the Release configuration                                   |
+--------------------------------+--------------------------------------------------------------------------------------+
| Find{name}-Debug.cmake         | Specific information for the Debug configuration                                     |
+--------------------------------+--------------------------------------------------------------------------------------+


Global Variables
-----------------

Being {name} the package name:

+--------------------------------+--------------------------------------------------------------------------------------+
| NAME                           | VALUE                                                                                |
+================================+======================================================================================+
| {name}_FOUND                   | Set to 1                                                                             |
+--------------------------------+--------------------------------------------------------------------------------------+
| {name}_VERSION                 | Package version                                                                      |
+--------------------------------+--------------------------------------------------------------------------------------+
| {name}_INCLUDE_DIRS            | Containing both the directories for the Debug and the Release                        |
+--------------------------------+--------------------------------------------------------------------------------------+
| {name}_LIBRARIES               | Libraries for the Debug or Release configuration, depending on the current config    |
+--------------------------------+--------------------------------------------------------------------------------------+
| {name}_LIBS                    | Same as {name}_LIBRARIES                                                             |
+--------------------------------+--------------------------------------------------------------------------------------+
| {name}_LIBRARY                 | Same as {name}_LIBRARIES. Required by "select_library_configurations" cmake function |
+--------------------------------+--------------------------------------------------------------------------------------+


Release Variables
-----------------

Being {name} the package name:

+-----------------------------------+--------------------------------------------------------------------------------------+
| NAME                              | VALUE                                                                                |
+===================================+======================================================================================+
| {name}_INCLUDE_DIRS_RELEASE       | Include directories for Release.                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------+
| {name}_DEFINITIONS_RELEASE        | Definitions of the library for Release.                                              |
+-----------------------------------+--------------------------------------------------------------------------------------+
| {name}_LIBRARIES_RELEASE          | Library paths to link for Release.                                                   |
+-----------------------------------+--------------------------------------------------------------------------------------+
| {name}_LIBS_RELEASE               | Same as {name}_LIBRARIES_RELEASE                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------+
| {name}_LIBRARY_RELEASE            | Same as {name}_LIBRARIES_RELEASE.                                                    |
+-----------------------------------+--------------------------------------------------------------------------------------+
| {name}_LINKER_FLAGS_RELEASE       | Linker flags for Release.                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------+
| {name}_COMPILE_DEFINITIONS_RELEASE| Compile definitions for Release.                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------+
| {name}_COMPILE_OPTIONS_RELEASE    | Compiler options for Release.                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------+

Debug Variables
---------------

Same as ``Release`` but with the ``_DEBUG`` suffix instead of ``_RELEASE``

Targets
-------

A target named ``{name}::{name}`` target is generated with the following properties adjusted:

- ``INTERFACE_INCLUDE_DIRECTORIES``: Containing all the include directories of the package.
- ``INTERFACE_LINK_LIBRARIES``: Library paths to link.
- ``INTERFACE_COMPILE_DEFINITIONS``: Definitions of the library.

The targets contains multi-configuration properties, for example, the compile options property
is declared like this:

.. code-block:: cmake

        set_property(TARGET {name}::{name}
                 PROPERTY INTERFACE_COMPILE_OPTIONS
                     $<$<CONFIG:Release>:${{{name}_COMPILE_OPTIONS_RELEASE_LIST}}>
                     $<$<CONFIG:RelWithDebInfo>:${{{name}_COMPILE_OPTIONS_RELEASE_LIST}}>
                     $<$<CONFIG:MinSizeRel>:${{{name}_COMPILE_OPTIONS_RELEASE_LIST}}>
                     $<$<CONFIG:Debug>:${{{name}_COMPILE_OPTIONS_DEBUG_LIST}}>)

The targets are also transitive. So, if your project depends on a packages ``A`` and ``B``, and at the same time
``A`` depends on ``C``, the ``A`` target will contain automatically the properties of the ``C`` dependency, so
in your `CMakeLists.txt` file you only need to ``find_package(A)`` and ``find_package(B)``.


