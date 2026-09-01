.. _cmake_paths_generator:

``cmake_paths`` generator
=========================

This generator is especially useful if you are using ``CMake`` based only on the ``find_package``
feature to locate the dependencies.

The ``cmake_paths`` generator creates a file named ``conan_paths.cmake`` declaring:

- ``CMAKE_MODULE_PATH`` with the folders of the required packages, to allow CMake to locate the included cmake scripts and ``FindXXX.cmake``
  files. The folder containing the *conan_paths.cmake* (`self.install_folder` when used in a recipe) is also included, so any custom file
  will be located too. Check :ref:`cmake_find_package_generator` generator.
- ``CMAKE_PREFIX_PATH`` used by ``find_library()`` to locate library files (*.a*, *.lib*, *.so*, *.dll*) in your packages and ``find_dependency()`` to locate
  the transitive dependencies.

.. code-block:: text
   :caption: conanfile.txt

    [requires]
    zlib/1.2.11
    ...

    [generators]
    cmake_paths

.. code-block:: cmake
   :emphasize-lines: 4
   :caption: CMakeList.txt

    cmake_minimum_required(VERSION 3.0)
    project(helloworld)
    add_executable(helloworld hello.c)
    find_package(Zlib)
    if(ZLIB_FOUND)
       include_directories(${ZLIB_INCLUDE_DIRS})
       target_link_libraries (helloworld ${ZLIB_LIBRARIES})
    endif()

In the example above, the ``zlib/1.2.11`` package is not packaging a custom ``FindZLIB.cmake`` file, but the ``FindZLIB.cmake``
included in the CMake installation directory (`/Modules`) will locate the zlib library from the Conan package because of the
``CMAKE_PREFIX_PATH`` used by the ``find_library()``.

If the ``zlib/1.2.11`` would have included a custom ``FindZLIB.cmake`` in the package root folder or any declared
:ref:`self.cpp_info.builddirs <cpp_info_attributes_reference>`, it would have been located because of the ``CMAKE_MODULE_PATH`` variable.

Included as a toolchain
-----------------------

You can use the *conan_paths.cmake* as a toolchain without modifying your *CMakeLists.txt* file:

.. code-block:: bash
   :emphasize-lines: 3

    $ mkdir build && cd build
    $ conan install ..
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .

Included using the ``CMAKE_PROJECT_<PROJECT-NAME>_INCLUDE``
-----------------------------------------------------------

With ``CMAKE_PROJECT_<PROJECT-NAME>_INCLUDE`` you can specify a file to be included by the ``project()`` command.
If you already have a toolchain file you can use this variable to include the ``conan_paths.cmake`` and insert your toolchain with the
``CMAKE_TOOLCHAIN_FILE``.

.. code-block:: bash

    $ mkdir build && cd build
    $ conan install ..
    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_PROJECT_helloworld_INCLUDE=build/conan_paths.cmake
    $ cmake --build .

Included in your *CMakeLists.txt*
---------------------------------

.. code-block:: cmake
   :emphasize-lines: 3
   :caption: CMakeList.txt

    cmake_minimum_required(VERSION 3.0)
    project(helloworld)

    include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

    add_executable(helloworld hello.c)

    find_package(zlib)

    if(ZLIB_FOUND)
       include_directories(${ZLIB_INCLUDE_DIRS})
       target_link_libraries (helloworld ${ZLIB_LIBRARIES})
    endif()

.. code-block:: bash

    $ mkdir build && cd build
    $ conan install ..
    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .

.. seealso::

    Check the section :ref:`cmake_paths_generator_reference` to read more about this generator.

.. note::

    The ``CMAKE_MODULE_PATH`` and ``CMAKE_PREFIX_PATH`` contain the paths to the ``builddirs`` of every required package. By default the
    root package folder is the only declared ``builddirs`` directory. Check :ref:`cpp_info_attributes_reference`.
