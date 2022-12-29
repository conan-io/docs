.. _cmake:

|cmake_logo| CMake
==================

Conan can be integrated with CMake using different generators, build helpers and custom *findXXX.cmake* files:

.. warning::

    This is a **deprecated** feature. Please refer to the :ref:`Migration Guidelines<conan2_migration_guide>`
    to find the feature that replaced this one.

    The new, **under development** integration with CMake can be found in :ref:`conan_tools_cmake`. This is the integration that will
    become the standard one in Conan 2.0, and the below generators and integrations will be deprecated and removed. While they are
    recommended and usable and we will try not to break them in future releases, some breaking
    changes might still happen if necessary to prepare for the *Conan 2.0 release*.


.. toctree::
   :maxdepth: 2

   cmake/cmake_generator
   cmake/cmake_multi_generator
   cmake/cmake_paths_generator
   cmake/cmake_find_package_generator
   cmake/cmake_find_package_multi_generator
   cmake/build_automation
   cmake/find_packages


Other resources:

- If you want to use the Visual Studio 2017 + CMake integration, :ref:`check this how-to<visual2017_cmake_howto>`



.. |cmake_logo| image:: ../../images/conan-cmake_logo.png