.. _cmake_integration:

|cmake_logo| CMake
==================

Conan can be integrated with CMake using generators, build helpers and custom *findXXX.cmake* files:

However, beware of some current CMake limitations, such as not dealing well with find-packages, because CMake doesn't know how to handle finding both debug and release packages.

.. note::

    If you want to use the Visual Studio 2017 + CMake integration, :ref:`check this how-to<visual2017_cmake_howto>`


.. toctree::
   :maxdepth: 2

   cmake/cmake_generator
   cmake/cmake_multi_generator
   cmake/cmake_paths_generator
   cmake/cmake_find_package_generator
   cmake/cmake_find_package_multi_generator
   cmake/build_automation
   cmake/find_packages


.. |cmake_logo| image:: ../../images/conan-cmake_logo.png