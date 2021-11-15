.. _visual_cmake:

|visual_logo| CMake Integration
===============================

Visual Studio 2017 comes with a CMake integration that allows one to just open a folder that contains a *CMakeLists.txt*
and Visual will use it to define the project build.

Conan can also be used in this setup to install dependencies. Let`s say that we are going to build an application that depends
on an existing Conan package called ``hello/0.1@user/testing``. For the purpose of this example, you can quickly create this package by typing
in your terminal:

.. code-block:: bash

    $ conan new hello/0.1 -s
    $ conan create . user/testing # Default conan profile is Release
    $ conan create . user/testing -s build_type=Debug

The project we want to develop will be a simple application with these 3 files in the same folder:

.. code-block:: cpp
   :caption: **example.cpp**

    #include <iostream>
    #include "hello.h"

    int main() {
        hello();
        std::cin.ignore();
    }

.. code-block:: text
    :caption: **conanfile.txt**

    [requires]
    hello/0.1@user/testing

    [generators]
    cmake

.. code-block:: cmake
    :caption: **CMakeLists.txt**

    project(Example CXX)
    cmake_minimum_required(VERSION 2.8.12)

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

    add_executable(example example.cpp)
    target_link_libraries(example ${CONAN_LIBS})

If we open Visual Studio 2017 (with CMake support installed), and select "Open Folder" from the menu, and select the above folder,
we will see something like the following error:

.. code-block:: bash
    :emphasize-lines: 2,10-13

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

As expected, our *CMakeLists.txt* is using an ``include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)``, and that file doesn't exist yet,
because Conan has not yet installed the dependencies of this project. Visual Studio 2017 uses different build folders for each
configuration. In this case, the default configuration at startup is ``x64-Debug``. This means that we need to install the
dependencies that match this configuration. Assuming that our default profile is using Visual Studio 2017 for x64 (it should typically be
the default one created by Conan if VS2017 is present), then all we need to specify is the ``-s build_type=Debug`` setting:

.. code-block:: bash

    $ conan install . -s build_type=Debug -if=C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\build\x64-Debug

Now, you should be able to regenerate the CMake project from the IDE, Menu->CMake, build it, select the "example" executable to run, and run
it.

Now, let's say that you want to build the Release application. You switch configuration from the IDE, and then the above error happens
again. The dependencies for Release mode need to be installed too:

.. code-block:: bash

    $ conan install . -if=C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\build\x64-Release

The process can be extended to x86 (passing ``-s arch=x86`` in the command line), or to other configurations. For production usage,
Conan **profiles** are highly recommended.

.. _`CMake docs`: https://cmake.org/cmake/help/v3.0/manual/cmake-generators.7.html
.. |visual_logo| image:: ../../images/conan-visual-studio-logo.png
