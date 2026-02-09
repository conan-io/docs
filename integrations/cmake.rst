.. _integrations_cmake:

|cmake_logo| CMake
==================

Conan provides different tools to integrate with CMake in a transparent way. Using these
tools, the consuming ``CMakeLists.txt`` file does not need to be aware of Conan at all. The
CMake tools also provide better IDE integration via cmake-presets.

To learn how to integrate Conan with your current CMake project you can follow the
:ref:`Conan tutorial <tutorial>` that uses CMake along all the sections.

Please also check the reference for the CMakeDeps, CMakeToolchain, and CMake tools:

- ``CMakeDeps``: responsible for generating the CMake config files for all the required
  dependencies of a package.

- ``CMakeConfigDeps``: A modern and better alternative to ``CMakeDeps``, released in Conan 2.25
  that has several improvements and fixes.

- ``CMakeToolchain``: generates all the information needed for CMake to build the packages
  according to the information passed to Conan about things like the operating system, the
  compiler to use, architecture, etc. in a ``conan_toolchain.cmake`` toolchain file.
  It will also generate `cmake-presets` files for easy
  integration with some IDEs that support this CMake feature off-the-shelf.

- ``CMake`` build helper is the tool used by Conan ``conanfile.py`` recipes to run CMake and will pass all the
  arguments that CMake needs to build successfully, such as the toolchain file, build type
  file, and all the CMake definitions set in the recipe.


The ``CMakeDeps`` and ``CMakeConfigDeps``, together with ``CMakeToolchain`` follow for the classic
consumption flow described along the tutorial and many other sections in this documentation:

.. code-block:: bash

  $ conan install ...
  $ cmake --preset conan-xxxx
  # or use the -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake

This flow is important, the ``conan install`` command generates CMake presets and ``conan_toolchain.cmake``
toolchain files that helps locating the dependencies, besides trying to align as best as possible with the profile 
information. This is the recommended flow for most cases.

In extraordinary and exceptional scenarios, it might be desired that it is the ``CMake`` execution that 
calls ``conan install`` to simplify the flow, for example for some IDE integrations like the CLion one, so
the users don't need to call ``conan install`` themselves.

For this purpose, the  `cmake-conan integration <https://github.com/conan-io/cmake-conan>`_ exists.
It uses the CMake "dependency providers" to intercept the first ``find_package()`` and do a call
to ``conan install`` to fetch the dependencies at that point.

This ``cmake-conan`` project stability is not guaranteed, and it has some known issues and limitations.
refer to the Github repository for more details. And note that calling ``conan install`` explicitly before
calling ``cmake`` is still the preferred and most recommended flow for most cases.


.. seealso::

    - Check the :ref:`Building your project using CMakePresets
      <examples-tools-cmake-toolchain-build-project-presets>` example
    - Reference for :ref:`CMakeDeps <conan_tools_cmakedeps>`, :ref:`CMakeConfigDeps generator<conan_tools_cmakeconfigdeps>`,
      :ref:`CMakeToolchain <conan_tools_cmaketoolchain>` and :ref:`CMake build helper
      <conan_tools_cmake_helper>`
    - :ref:`Conan tutorial <tutorial>`


.. |cmake_logo| image:: ../images/integrations/conan-cmake-logo.png
