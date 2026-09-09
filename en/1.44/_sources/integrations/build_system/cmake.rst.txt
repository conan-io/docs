.. _cmake:

|cmake_logo| CMake
==================

.. note::

   The new, experimental integration with CMake can be found in :ref:`conan_tools_cmake`. This is the integration that will
   become the standard one in Conan 2.0, and the below generators and integrations will be deprecated and removed.


Conan can be integrated with CMake using different generators, build helpers and custom *findXXX.cmake* files:


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