.. _cmake_cmake_find_package_generator_reference:


`cmake_find_package`
====================

.. container:: out_reference_box

    This is the reference page for ``cmake_find_package`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.


The ``cmake_find_package`` generator creates a file for each requirement specified in the conanfile.

The name of the files follow the pattern ``Find<package_name>.cmake``. So for the ``zlib/1.2.11@conan/stable`` package,
a ``Findzlib.cmake`` file will be generated.


Variables in Find{name}.cmake
-------------------------------------

Being {name} the package name:

+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| NAME                           | VALUE                                                                                                                                              |
+================================+====================================================================================================================================================+
| {name}_FOUND                   | Set to 1                                                                                                                                           |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| {name}_INCLUDE_DIRS            | Containing all the include directories of the package                                                                                              |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| {name}_INCLUDES                | Same as the XXX_INCLUDE_DIRS                                                                                                                       |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| {name}_DEFINITIONS             | Definitions of the library                                                                                                                         |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| {name}_LIBRARIES               | Library paths to link                                                                                                                              |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| {name}_LIBS                    | Same as XXX_LIBRARIES                                                                                                                              |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+


Target in Find<package_name>.cmake
----------------------------------

A target named ``{name}:{name}`` target is generated with the following properties adjusted:

- ``INTERFACE_INCLUDE_DIRECTORIES``: Containing all the include directories of the package.
- ``INTERFACE_LINK_LIBRARIES``: Library paths to link.
- ``INTERFACE_COMPILE_DEFINITIONS``: Definitions of the library.

The targets are transitive. So, if your project depends on a packages ``A`` and ``B``, and at the same time
``A`` depends on ``C``, the ``A`` target will contain automatically the properties of the ``C`` dependency, so
in your `CMakeLists.txt` file you only need to ``find_package(A)`` and ``find_package(B)``.


