.. _visual2017_cmake_howto:


Using Visual Studio 2017 - CMake integration
=============================================

Visual Studio 2017 comes with a CMake integration that allows to just open a folder that contains a *CMakeLists.txt*
and Visual will use it to define the project build.

Conan can also be used in this setup to install dependencies. Let`s say that we are going to build an application, that depends
on an existing conan package called ``Hello/0.1@user/testing``. For the purpose of this example, you can quickly create
this package typing in your terminal:

.. code-block:: bash

    $ conan new Hello/0.1 -s
    $ conan create . user/testing # Default conan profile is Release
    $ conan create . user/testing -s build_type=Debug
  

The project we want to develop will be a simple application, with these 3 files in the same folder:

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
    Hello/0.1@user/testing

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

If we open Visual Studio 2017 (with CMake support installed), and in the Menu, select "Open Folder" and select the above folder,
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


As expected, our *CMakeLists.txt* is using a ``include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)``, and that file doesn't exist yet,
because conan has not installed the dependencies of this project yet. Visual Studio 2017 uses different build folders for each 
configuration. In this case, the default configuration at startup is ``x64-Debug``. This means that we need to install the
dependencies that match this configuration. Assuming that our default profile is using Visual Studio 2017 for x64 (it should typically be
the default one created by conan if VS2017 is present), then all we need to specify is the ``-s build_type=Debug`` setting:

.. code-block:: bash

    $ conan install . -s build_type=Debug -if=C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\build\x64-Debug

Now, you should be able to regenerate the CMake project from the IDE, Menu->CMake, build it, select the "example" executable to run, and run it.

Now, lets say that you want to build the Release application. You switch configuration from the IDE, and then the above error happens again.
The dependencies for Release mode need to be installed too:

.. code-block:: bash

    $ conan install . -if=C:\Users\user\CMakeBuilds\df6639d2-3ef2-bc32-abb3-2cd1bdb3c1ab\build\x64-Release

The process can be extended to x86 (passing ``-s arch=x86`` in the command line), or to other configurations. For production usage,
conan **profiles** are highly recommended.


Using cmake-conan
------------------

The **cmake-conan** project in https://github.com/conan-io/cmake-conan is a CMake script that runs an ``execute_process`` that automatically
launches ``conan install`` to install dependencies. The settings passed in the command line will be deduced from the current CMake
configuration, that will match the Visual Studio one. This script can be used to further automate the installation task:

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

This code will manage to download the **cmake-conan** CMake script, and use it automatically, calling a ``conan install`` automatically.


There could be an issue, though, for the ``Release`` configuration. Internally, the Visual Studio 2017 defines the ``configurationType`` As
``RelWithDebInfo`` for ``Release`` builds. But conan default settings (in the conan *settings.yml* file), only have ``Debug`` and ``Release``
defined. It is possible to modify the *settings.yml* file, and add those extra build types. Then you should create the ``Hello`` package 
for those settings. And most existing packages, specially in central repositories, are built only for Debug and Release modes.

An easier approach is to change the CMake configuration in Visual: go to the Menu -> CMake -> Change CMake Configuration. That should open
the *CMakeSettings.json* file, and there you can change the ``configurationType`` to ``Release``:


.. code-block:: text
  :emphasize-lines: 4

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
  }

Note that the above CMake code is only valid for consuming existing packages. If you are also creating a package, you
would need to make sure the right CMake code is executed, please check https://github.com/conan-io/cmake-conan/blob/master/README.md

Using tasks with tasks.vs.json
------------------------------
Another alternative is using file `tasks <https://docs.microsoft.com/en-us/cpp/ide/non-msbuild-projects#define-tasks-with-tasksvsjson>`_ feature of Visual Studio 2017. This way you can install dependencies by running conan install as task directly in the IDE.

All you need is to right click on your `conanfile.py`-> Configure Tasks (see the `link above <https://docs.microsoft.com/en-us/cpp/ide/non-msbuild-projects#define-tasks-with-tasksvsjson>`_) and add the following to your *tasks.vs.json*.

.. warning::
  The file *tasks.vs.json* is added to your local *.vs* folder so it is not supposed to be added to your version control system. There is also feature `request <https://visualstudio.uservoice.com/forums/121579-visual-studio-ide/suggestions/33814138-add-macro-buildroot-to-tasks-vs-json>`_ to improve this process.
    
.. code-block:: text
  :emphasize-lines: 7,9,16,18

      {
        "tasks": [
          {
            "taskName": "conan install debug",
            "appliesTo": "conanfile.py",
            "type": "launch",
            "command": "${env.COMSPEC}",
            "args": [
              "conan install ${file} -s build_type=Debug -if C:/Users/user/CMakeBuilds/4c2d87b9-ec5a-9a30-a47a-32ccb6cca172/build/x64-Debug/"
            ]
          },
          {
            "taskName": "conan install release",
            "appliesTo": "conanfile.py",
            "type": "launch",
            "command": "${env.COMSPEC}",
            "args": [
              "conan install ${file} -s build_type=Release -if C:/Users/user/CMakeBuilds/4c2d87b9-ec5a-9a30-a47a-32ccb6cca172/build/x64-Release/"
            ]
          }
        ],
        "version": "0.2.1"
      }

Then just right click on your *conanfile.py* and launch your ``conan install`` and regenerate your *CMakeLists.txt*.
