.. _examples-tools-cmake-toolchain-build-project-presets:

CMakeToolchain: Building your project using CMakePresets
========================================================

In this example we are going to see how to use ``CMakeToolchain``, predefined layouts like ``cmake_layout`` and the
``CMakePresets`` CMake feature.

Let's create a basic project based on the template ``cmake_exe`` as an example of a C++ project:

.. code:: bash

    $ conan new cmake_exe -d name=foo -d version=1.0


Generating the toolchain
------------------------

The recipe from our project declares the generator "CMakeToolchain".

We can call :command:`conan install` to install both ``Release`` and ``Debug``
configurations. Conan will generate a ``conan_toolchain.cmake`` at the corresponding
*generators* folder:

.. code:: bash

    $ conan install .
    $ conan install . -s build_type=Debug


Building the project using ``CMakePresets``
-------------------------------------------

A ``CMakeUserPresets.json`` file is generated in the same folder of your ``CMakeLists.txt`` file,
so you can use the ``--preset`` argument from ``cmake >= 3.23`` or use an IDE that supports it.


The ``CMakeUserPresets.json`` is including the ``CMakePresets.json`` files located at the
corresponding *generators* folder.


The ``CMakePresets.json`` contain information about the ``conan_toolchain.cmake`` location
and even the ``binaryDir`` set with the output directory.


.. include:: ../../../../tutorial/cmake_presets_note.inc


If you are using a multi-configuration generator:

.. code:: bash

    $ cmake --preset conan-default
    $ cmake --build --preset conan-debug
    $ build\Debug\foo.exe
    foo/1.0: Hello World Release!

    $ cmake --build --preset conan-release
    $ build\Release\foo.exe
    foo/1.0: Hello World Release!


If you are using a single-configuration generator:

.. code:: bash

    $ cmake --preset conan-debug
    $ cmake --build --preset conan-debug
    $ ./build/Debug/foo
    foo/1.0: Hello World Debug!


    $ cmake --preset conan-release
    $ cmake --build --preset conan-release
    $ ./build/Release/foo
    foo/1.0: Hello World Release!


Note that we didn't need to create the ``build/Release`` or ``build/Debug`` folders, as we did :ref:`in the
tutorial<consuming_packages_flexibility_of_conanfile_py_use_layout>`. The output directory
is declared by the ``cmake_layout()`` and automatically managed by the CMake Presets feature.

This behavior is also managed automatically by Conan (with CMake >= 3.15) when you build a package in the Conan
cache (with :command:`conan create` command). The CMake >= 3.23 is not required.

Read More:

- ``cmake_layout()`` :ref:`reference <cmake_layout>`
- Conanfile :ref:`layout() method reference <reference_conanfile_methods_layout>`
- Package layout tutorial :ref:`tutorial <developing_packages_layout>`
- Understanding :ref:`Conan package layouts <tutorial_package_layout>`
