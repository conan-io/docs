.. _integrations_ros:

|ros_logo| ROS
==============

.. include:: ../common/experimental_warning.inc

Conan provides integration for your Robot Operating System (ROS) C/C++ based projects.
This will allow you to consume Conan packages inside your ROS package projects.
The Conan packages can be installed and used in CMake with the help of the :ref:`ROSEnv generator <conan_tools_ros_rosenv>` created
for the purpose.

It provides a clean integration that requires no Conan-specific modifications in your *CMakeLists.txt*.

.. important::

    This integration supports **ROS2**, it has been developed using its **Humble version** and the aim is to **support newer versions going forward**.
    If you have any issues with other ROS versions, please let us know by opening an issue in our GitHub repository.

.. note::

    **Pre-requisites to run the example:**

    1. In order to run the example, it is expected that you have an Ubuntu environment (22.04 LTS preferred) with `ROS2 Humble version installed <https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html>`_. For convenience, you can also use this Docker File instead:

       .. code-block:: docker

           FROM osrf/ros:humble-desktop
           RUN apt-get update && apt-get install -y \
           curl \
           python3-pip \
           git \
           ros-humble-nav2-msgs \
           && rm -rf /var/lib/apt/lists/*
           RUN pip3 install --upgrade pip && pip3 install conan==2.*
           RUN conan profile detect
           CMD ["bash"]


    Simply copy the Dockerfile, build your image with ``docker build -t conanio/ros-humble .``, and finally run it with ``docker run -it conanio/ros-humble``.

    2. The files for this example can be found at `our examples repository <https://github.com/conan-io/examples2/tree/main/examples/tools/ros/rosenv/workspace>`_.
       Clone it like so to get started:

       .. code-block:: bash

           $ git clone https://github.com/conan-io/examples2.git
           $ cd examples2/examples/tools/ros/rosenv






Consuming Conan packages using the ROSEnv generator
---------------------------------------------------

Imagine we have a ROS C++ package called `str_printer` that uses some functionality from the 
third party string formatting library `fmt <https://conan.io/center/recipes/fmt>`_ to print fancy strings.

We have the following project structure:

.. code-block:: bash

    $  tree /f
    workspace
    ├───str_printer
    │   │   CMakeLists.txt
    │   │   conanfile.txt
    │   │   package.xml
    │   ├───include
    │   │   └──str_printer
    │   │         str_printer.h
    │   └───src
    │          str_printer.cpp
    └───consumer
        │   CMakeLists.txt
        │   package.xml
        └───src
               main.cpp

Where:

- The `str_printer` is a ROS package that implements a function and **depends on the fmt Conan package**.
- The `consumer` is also a ROS package that depends on the `str_printer` ROS package and uses its functionality in a **final executable**.

The only difference in the `str_printer` package with respect to a normal ROS package is that it includes a *conanfile.txt* file.
This is the file used by Conan to install the required dependencies and generate the files needed to perform the build.

.. code-block:: text
   :caption: str_printer/conanfile.txt

    [requires]
    fmt/11.0.2

    [generators]
    CMakeDeps
    CMakeToolchain
    ROSEnv

In this case, we will install the 11.0.2 version of `fmt` and Conan will generate files for CMake and ROS so we can build the `str_printer` package later.

To install the `fmt` library using Conan we should do the following:

.. code-block:: bash

    $ cd workspace
    $ conan install str_printer/conanfile.txt --build missing --output-folder install/conan
    ======== Computing dependency graph ========
    fmt/11.0.2: Not found in local cache, looking in remotes...
    fmt/11.0.2: Checking remote: conancenter
    fmt/11.0.2: Downloaded recipe revision 5c7438ef4d5d69ab106a41e460ce11f3
    Graph root
        conanfile.txt: /home/user/examples2/examples/tools/ros/rosenv/workspace/str_printer/conanfile.txt
    Requirements
        fmt/11.0.2#5c7438ef4d5d69ab106a41e460ce11f3 - Downloaded (conancenter)

    ======== Computing necessary packages ========
    Requirements
        fmt/11.0.2#5c7438ef4d5d69ab106a41e460ce11f3:29da3f322a17cc9826b294a7ab191c2f298a9f49#d8d27fde7061f89f7992c671d98ead71 - Download (conancenter)

    ======== Installing packages ========

    -------- Downloading 1 package --------
    fmt/11.0.2: Retrieving package 29da3f322a17cc9826b294a7ab191c2f298a9f49 from remote 'conancenter'
    fmt/11.0.2: Package installed 29da3f322a17cc9826b294a7ab191c2f298a9f49
    fmt/11.0.2: Downloaded package revision d8d27fde7061f89f7992c671d98ead71

    ======== Finalizing install (deploy, generators) ========
    conanfile.txt: Writing generators to /home/user/examples2/examples/tools/ros/rosenv/workspace/install/conan
    conanfile.txt: Generator 'CMakeDeps' calling 'generate()'
    conanfile.txt: CMakeDeps necessary find_package() and targets for your CMakeLists.txt
        find_package(fmt)
        target_link_libraries(... fmt::fmt)
    conanfile.txt: Generator 'CMakeToolchain' calling 'generate()'
    conanfile.txt: CMakeToolchain generated: conan_toolchain.cmake
    conanfile.txt: Preset 'conan-release' added to CMakePresets.json. Invoke it manually using 'cmake --preset conan-release' if using CMake>=3.23
    conanfile.txt: If your CMake version is not compatible with CMakePresets (<3.23) call cmake like: 'cmake <path> -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=/home/danimtb/examples2/examples/tools/ros/rosenv/workspace/install/conan/conan_toolchain.cmake -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release'
    conanfile.txt: CMakeToolchain generated: CMakePresets.json
    conanfile.txt: CMakeToolchain generated: ../../str_printer/CMakeUserPresets.json
    conanfile.txt: Generator 'ROSEnv' calling 'generate()'
    conanfile.txt: Generated ROSEnv Conan file: conanrosenv.sh
    Use 'source /home/user/examples2/examples/tools/ros/rosenv/workspace/install/conan/conanrosenv.sh' to set the ROSEnv Conan before 'colcon build'
    conanfile.txt: Generating aggregated env files
    conanfile.txt: Generated aggregated env files: ['conanrosenv.sh']
    Install finished successfully

This will download the `fmt` Conan package to the local cache and generate the CMake and ROS environment files
in the `conan` subfolder of the `install` directory.

Now we can source our ROS environment, then **source the Conan ROSEnv environment**, so the conan-installed package are found by CMake, and then
we can build the `str_printer` package as usual with Colcon.

.. code-block:: bash

    $ source /opt/ros/humble/setup.bash
    $ source install/conan/conanrosenv.sh
    $ colcon build --packages-select str_printer
    Starting >>> str_printer
    Finished <<< str_printer [10.8s]

    Summary: 1 package finished [12.4s]


Bridging the Conan-provided transitive dependencies to another ROS package
--------------------------------------------------------------------------

As the `consumer` ROS package depends on `str_printer`, the targets of transitive dependencies should be exported.
This is done as usual in the `str_printers`'s *CMakeLists.txt* using `ament_export_dependencies()`:

.. code-block:: text
   :caption: str_printer/CMakeLists.txt
   :emphasize-lines: 10,22

    cmake_minimum_required(VERSION 3.8)
    project(str_printer)

    if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
    endif()

    # find dependencies
    find_package(ament_cmake REQUIRED)
    find_package(fmt REQUIRED)  # Retrieved with Conan C/C++ Package Manager

    add_library(str_printer src/str_printer.cpp)

    target_include_directories(str_printer PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/str_printer>
    $<INSTALL_INTERFACE:include>)

    target_compile_features(str_printer PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
    ament_target_dependencies(str_printer fmt)

    ament_export_targets(str_printerTargets HAS_LIBRARY_TARGET)
    ament_export_dependencies(fmt)

    install(
    DIRECTORY include/
    DESTINATION include
    )

    install(
    TARGETS str_printer
    EXPORT str_printerTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
    )

    ament_package()

To build the `consumer` ROS package, you can proceed as usual (make sure
that you have both the ROS environment and the Conan ROSEnv environment *sourced* before building as in previous step):

.. code-block:: bash

    $ colcon build --packages-select consumer
    Starting >>> consumer
    Finished <<< consumer [7.9s]

    Summary: 1 package finished [9.4s]

And after this, our `consumer` application should be ready to run with just:

.. code-block:: bash

    $ source install/setup.bash
    $ ros2 run consumer main
    Hi there! I am using fmt library fetched with Conan C/C++ Package Manager

.. seealso::

    - Reference for :ref:`ROSEnv generator<conan_tools_ros_rosenv>`.

.. |ros_logo| image:: ../images/integrations/conan-ros-logo.png
