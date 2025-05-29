.. _cmake_paths_generator_reference:


cmake_paths
===========

.. warning::

    This is a **deprecated** feature. Please refer to the :ref:`Migration Guidelines<conan2_migration_guide>`
    to find the feature that replaced this one.

    The new, **under development** integration with CMake can be found in :ref:`conan_tools_cmake`. This is the integration that will
    become the standard one in Conan 2.0, and the below generators and integrations will be deprecated and removed. While they are
    recommended and usable and we will try not to break them in future releases, some breaking
    changes might still happen if necessary to prepare for the *Conan 2.0 release*.

.. container:: out_reference_box

    This is the reference page for ``cmake_paths`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.

It generates a file named ``conan_paths.cmake`` and declares these variables:

.. _conan_paths_cmake_variables:

Variables in *conan_paths.cmake*
--------------------------------

+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| NAME                  | VALUE                                                                                                                                                          |
+=======================+================================================================================================================================================================+
| CMAKE_MODULE_PATH     | Containing all requires root folders, any declared :ref:`self.cpp_info.builddirs <cpp_info_attributes_reference>` and the current directory of this file       |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CMAKE_PREFIX_PATH     | Containing all requires root folders, any declared :ref:`self.cpp_info.builddirs <cpp_info_attributes_reference>` and the current directory of this file       |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CONAN_<PKG-NAME>_ROOT | For each dep, the root folder, being XXX the dep name uppercase. Useful when a *.cmake* is patched with :ref:`cmake.patch_config_paths()<patch_config_paths>`  |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+

Where ``<PKG-NAME>`` is the placeholder for the name of the require in uppercase (``ZLIB`` for ``zlib/1.2.11``) or the one declared in ``cpp_info.names["cmake_paths"]`` if specified.
