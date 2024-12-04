.. _integrations_cmake:

|cmake_logo| CMake
==================

Conan provides different tools to integrate with CMake in a transparent way. Using these
tools, the consuming ``CMakeLists.txt`` file does not need to be aware of Conan at all. The
CMake tools also provide better IDE integration via cmake-presets.

To learn how to integrate Conan with your current CMake project you can follow the
:ref:`Conan tutorial <tutorial>` that uses CMake along all the sections.

Please also check the reference for the CMakeDeps, CMakeToolchain, and CMake tools:

- `CMakeDeps`: responsible for generating the CMake config files for all the required
  dependencies of a package.

- `CMakeToolchain`: generates all the information needed for CMake to build the packages
  according to the information passed to Conan about things like the operating system, the
  compiler to use, architecture, etc. It will also generate `cmake-presets` files for easy
  integration with some IDEs that support this CMake feature off-the-shelf.

- `CMake` build helper is the tool used by Conan to run CMake and will pass all the
  arguments that CMake needs to build successfully, such as the toolchain file, build type
  file, and all the CMake definitions set in the recipe.


.. seealso::

    - Check the :ref:`Building your project using CMakePresets
      <examples-tools-cmake-toolchain-build-project-presets>` example
    - Reference for :ref:`CMakeDeps <conan_tools_cmakedeps>`, :ref:`CMakeToolchain
      <conan_tools_cmaketoolchain>` and :ref:`CMake build helper
      <conan_tools_cmake_helper>`
    - :ref:`Conan tutorial <tutorial>`


.. |cmake_logo| image:: ../images/integrations/conan-cmake-logo.png
