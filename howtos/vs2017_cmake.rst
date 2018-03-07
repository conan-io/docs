.. _visual2017_cmake_howto:


Using Visual Studio 2017 - CMake integration
=============================================

.. code-block:: cpp

    #include <iostream>
    #include "hello.h"

    int main() {
        hello();
        std::cin.ignore();
    }

.. code-block::

    [requires]
    Hello/0.1@user/testing

    [generators]
    cmake

    [imports]
    bin, *.dll  -> bin

.. code-block:: cmake

    project(Example CXX)
    cmake_minimum_required(VERSION 2.8.12)

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

    add_executable(example example.cpp)
    target_link_libraries(example ${CONAN_LIBS})

It will error with:

.. code-block:: bash

    1> Command line: C:\PROGRAM FILES (X86)\MICROSOFT VISUAL STUDIO\2017\COMMUNITY\COMMON7\IDE\COMMONEXTENSIONS\MICROSOFT\CMAKE\CMake\bin\cmake.exe  -G "Ninja" -DCMAKE_INSTALL_PREFIX:PATH="C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\install\x64-Debug"  -DCMAKE_CXX_COMPILER="C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.12.25827/bin/HostX64/x64/cl.exe"  -DCMAKE_C_COMPILER="C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.12.25827/bin/HostX64/x64/cl.exe"  -DCMAKE_BUILD_TYPE="Debug" -DCMAKE_MAKE_PROGRAM="C:\PROGRAM FILES (X86)\MICROSOFT VISUAL STUDIO\2017\COMMUNITY\COMMON7\IDE\COMMONEXTENSIONS\MICROSOFT\CMAKE\Ninja\ninja.exe" "C:\Users\user\conanws\visual-cmake"
    1> Working directory: C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\build\x64-Debug
    1> -- The CXX compiler identification is MSVC 19.12.25831.0
    1> -- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.12.25827/bin/HostX64/x64/cl.exe
    1> -- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.12.25827/bin/HostX64/x64/cl.exe -- works
    1> -- Detecting CXX compiler ABI info
    1> -- Detecting CXX compiler ABI info - done
    1> -- Detecting CXX compile features
    1> -- Detecting CXX compile features - done
    1> CMake Error at CMakeLists.txt:4 (include):
    1>   include could not find load file:
    1> 
    1>     C:/Users/user/CMakeBuilds/df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab/build/x64-Debug/conanbuildinfo.cmake


.. code-block:: bash

    $ conan install . -s build_type=Debug -if=C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\build\x64-Debug

.. code-block:: bash

    $ conan install . -if=C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\build\x64-Release



Using cmake-conan
------------------

.. code-block:: cmake

    project(Example CXX)
    cmake_minimum_required(VERSION 2.8.12)

    # Download automatically, you can also just copy the conan.cmake file
    if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
        file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/v0.9/conan.cmake"
                    "${CMAKE_BINARY_DIR}/conan.cmake")
    endif()
    
    include(${CMAKE_BINARY_DIR}/conan.cmake)

    conan_cmake_run(CONANFILE conanfile.txt
                    BASIC_SETUP)

    add_executable(example example.cpp)
    target_link_libraries(example ${CONAN_LIBS})


.. code-block:: json

    {
      "name": "x64-Release",
      "generator": "Ninja",
      "configurationType": "Release",
      "inheritEnvironments": [ "msvc_x64_x64" ],
      "buildRoot": "${env.USERPROFILE}\\CMakeBuilds\\${workspaceHash}\\build\\${name}",
      "installRoot": "${env.USERPROFILE}\\CMakeBuilds\\${workspaceHash}\\install\\${name}",
      "cmakeCommandArgs": "",
      "buildCommandArgs": "-v",
      "ctestCommandArgs": ""
    },