``cmake_multi`` generator
=========================


``cmake_multi`` generator is intended for CMake multi-configuration environments, like Visual Studio and XCode IDEs that do not configure for a specific
``build_type``, like Debug or Release, but rather can be used for both and switch among Debug andRelease configurations with a combo box or similar control.
The project configuration for cmake is different, in multi-configuration environments, the flow would be:

.. code-block:: bash

    $ cmake .. -G "Visual Studio 14 Win64"
    # Now open the IDE (.sln file) or
    $ cmake --build . --config Release

While in single-configuration environments (Unix Makefiles, etc):

.. code-block:: bash

    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
    # Build from your IDE, launching make, or
    $ cmake --build .

The ``CMAKE_BUILD_TYPE`` default, if not specified is ``Debug``.

With the regular conan ``cmake`` generator, only 1 configuration at a time can be managed. Then,
it is a universal, homogeneous solution for all environments.
This is the recommended way, using the regular ``cmake`` generator, and just go to the command line and
switch among configurations:

.. code-block:: bash

    $ conan install -s build_type=Release ...
    # Work in release, then, to switch to Debug dependencies
    $ conan install -s build_type=Debug ...


However, end consumers with heavy usage of the IDE, might want a multi-configuration build. The
``cmake_multi`` **experimental** generator is able to do that. First, both Debug and Release
dependencies have to be installed:

.. code-block:: bash

    $ conan install -g cmake_multi -s build_type=Release ...
    $ conan install -g cmake_multi -s build_type=Debug  ...

These commands will generate 3 files: ``conanbuildinfo_release.cmake``, ``conanbuildinfo_debug.cmake``,
and ``conanbuildinfo_multi.cmake``, which includes the other two, and enables its use.


Global variables approach
----------------------------

The consumer project might write a ``CMakeLists.txt`` like:

.. code-block:: cmake

    project(MyHello)
    cmake_minimum_required(VERSION 2.8.12)

    include(${CMAKE_BINARY_DIR}/conanbuildinfo_multi.cmake)
    conan_basic_setup()

    add_executable(say_hello main.cpp)
    foreach(_LIB ${CONAN_LIBS_RELEASE})
        target_link_libraries(say_hello optimized ${_LIB})
    endforeach()
    foreach(_LIB ${CONAN_LIBS_DEBUG})
        target_link_libraries(say_hello debug ${_LIB})
    endforeach()


Targets approach
-----------------

Or, if using the modern cmake syntax with targets:

.. code-block:: cmake

    project(MyHello)
    cmake_minimum_required(VERSION 2.8.12)

    include(${CMAKE_BINARY_DIR}/conanbuildinfo_multi.cmake)
    conan_basic_setup(TARGETS)

    add_executable(say_hello main.cpp)
    target_link_libraries(say_hello CONAN_PKG::Hello1)

There's also a convenient macro for linking to all libraries:

.. code-block:: cmake

    project(MyHello)
    cmake_minimum_required(VERSION 2.8.12)

    include(${CMAKE_BINARY_DIR}/conanbuildinfo_multi.cmake)
    conan_basic_setup()

    add_executable(say_hello main.cpp)
    conan_target_link_libraries(say_hello)


With this approach, the end user can open the generated IDE project and switch among both
configurations, building the project, or from the command line:

.. code-block:: bash

    $ cmake --build . --config Release
    # And without having to conan install again, or do anything else
    $ cmake --build . --config Debug



.. seealso:: Check the section :ref:`Reference/Generators/cmake <cmakemulti_generator>` to read more about this generator.

