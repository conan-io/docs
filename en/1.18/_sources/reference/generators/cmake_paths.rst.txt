.. _cmake_paths_generator_reference:


`cmake_paths`
=============

.. container:: out_reference_box

    This is the reference page for ``cmake_paths`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.

It generates a file named ``conan_paths.cmake`` and declares two variables:

.. _conan_paths_cmake_variables:

Variables in *conan_paths.cmake*
--------------------------------

+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| NAME                | VALUE                                                                                                                                                          |
+=====================+================================================================================================================================================================+
| CMAKE_MODULE_PATH   | Containing all requires root folders, any declared :ref:`self.cpp_info.builddirs <cpp_info_attributes_reference>` and the current directory of this file       |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CMAKE_PREFIX_PATH   | Containing all requires root folders, any declared :ref:`self.cpp_info.builddirs <cpp_info_attributes_reference>` and the current directory of this file       |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CONAN_XXX_ROOT      | For each dep, the root folder, being XXX the dep name uppercase. Useful when a .cmake is patched with :ref:`cmake.patch_config_paths()<patch_config_paths>`    |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
