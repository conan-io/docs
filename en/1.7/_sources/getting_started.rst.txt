.. _getting_started:

Getting Started
===============

Let's get started with an example using one of the most popular C++ libraries: POCO_. We'll use CMake as our sample build system. Keep in
mind that Conan **works with any build system** and is not limited to using CMake.

.. _POCO: https://pocoproject.org/

A Timer Using POCO Libraries
----------------------------

1. Let's create a folder for our project:

.. code-block:: bash

    $ mkdir mytimer
    $ cd mytimer

.. note::

    If your code is in a GitHub repository, simply clone the project instead of creating this folder by using the following command:

    .. code-block:: bash

        $ git clone https://github.com/memsharded/example-poco-timer.git mytimer

2. Create the following source files inside this folder:

.. code-block:: cpp
   :caption: **timer.cpp**

    // $Id: //poco/1.4/Foundation/samples/Timer/src/Timer.cpp#1 $
    // This sample demonstrates the Timer and Stopwatch classes.
    // Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
    // and Contributors.
    // SPDX-License-Identifier:    BSL-1.0

    #include "Poco/Timer.h"
    #include "Poco/Thread.h"
    #include "Poco/Stopwatch.h"
    #include <iostream>

    using Poco::Timer;
    using Poco::TimerCallback;
    using Poco::Thread;
    using Poco::Stopwatch;

    class TimerExample{
    public:
        TimerExample(){ _sw.start();}

        void onTimer(Timer& timer){
            std::cout << "Callback called after " << _sw.elapsed()/1000 << " milliseconds." << std::endl;
        }
    private:
        Stopwatch _sw;
    };

    int main(int argc, char** argv){
        TimerExample example;
        Timer timer(250, 500);
        timer.start(TimerCallback<TimerExample>(example, &TimerExample::onTimer));

        Thread::sleep(5000);
        timer.stop();
        return 0;
    }

3. Create a *conanfile.txt* inside this folder with the following content:

.. code-block:: text
   :caption: **conanfile.txt**

    [requires]
    Poco/1.9.0@pocoproject/stable

    [generators]
    cmake

In this example, we use CMake to build the project, which is why the ``cmake`` generator is specified. This generator creates a
*conanbuildinfo.cmake* file that defines CMake variables including paths and library names that can be used in our build.

.. note:::

    If you are not a CMake user, change the ``[generators]`` section of your *conanfile.txt* to ``gcc`` or to the more generic ``txt`` in
    order to handle requirements for any build system. Learn more in :ref:`Using packages<using_packages>`.

To do so, include the generated file and add these variables to our *CMakeLists.txt*:

.. code-block:: cmake
   :caption: **CMakeLists.txt**

    project(FoundationTimer)
    cmake_minimum_required(VERSION 2.8.12)
    add_definitions("-std=c++11")

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

    add_executable(timer timer.cpp)
    target_link_libraries(timer ${CONAN_LIBS})

Installing Dependencies
-----------------------

To improve visibility, if you have a terminal with bright colors, like the default GNOME terminal in Ubuntu, set ``CONAN_COLOR_DARK=1`` to
increase the contrast. Then create a build folder for temporary build files, and install the requirements (pointing to the parent directory,
where the *conanfile.txt* is located):

.. code-block:: bash

    $ mkdir build && cd build
    $ conan install ..

.. attention::

    - It is strongly recommended to review the generated default profile and adjust the settings to accurately describe your system as
      described in the following section :ref:`getting_started_other_configurations`.

    - When a GCC **compiler >= 5.1** is detected, the setting modeling for the c++ standard library is set as follows: The
      ``compiler.libcxx`` is set to ``libstdc++`` that represents the old ABI compatibility for better compatibility. Your compiler default
      is most likely to be set to the new ABI, so you might want to change it to ``libstdc++11`` to use the new ABI compliant with CXX11
      directives and run :command:`conan install ..` again to install the right binaries. Read more in :ref:`manage_gcc_abi`.

This :command:`conan install` command downloads the binary package required for your configuration (detected the first time you ran the
command), **together with other (transitively required by Poco) libraries, like OpenSSL and Zlib**. It will also create the
*conanbuildinfo.cmake* file in the current directory, in which you can see the CMake variables, and a *conaninfo.txt* in which the settings,
requirements and optional information is saved.

It is very important to understand the installation process. When the :command:`conan install` command runs, settings specified on the
command line or taken from the defaults in *<userhome>/.conan/profiles/default* file are applied.

.. image:: images/install_flow.png
   :height: 400 px
   :width: 500 px
   :align: center

For example, the command :command:`conan install . -s os="Linux" -s compiler="gcc"`, performs these steps:

- Checks if the package recipe (for ``Poco/1.9.0@pocoproject/stable`` package) exists in the local cache. If we are just starting, the
  cache is empty.
- Looks for the package recipe in the defined remotes. Conan comes with `conan-center`_ Bintray remote as the default, but can be changed.
- If the recipe exists, the Conan client fetches and stores it in your local cache.
- With the package recipe and the input settings (Linux, GCC), the Conan client will validate that the corresponding binary is in the local
  cache. This test will not run when installing for the first time.
- The Conan client searches for the corresponding binary package in the remote. It will be fetched if it exists.
- The Conan client will then  generate the requested files specified in the ``[generators]`` section.

The Conan client will throw an error If the binary package required for specific settings doesn't exist. It is possible to try to build the
binary package from sources using the :command:`--build=missing` command line argument to install. A detailed description on how to build a
binary package is from sources is described in the below sections.

.. warning::

    In the Bintray repositories there are binaries for several mainstream compilers and versions, such as Visual Studio 12, 14, Linux GCC
    4.9 and Apple Clang 3.5. If you are using a different setup, running the command might fail because of the missing package. You could
    try to change your settings or build the package from source, using the :command:`--build=missing` option, instead of retrieving the
    binaries. Such a build might not have been tested and may eventually fail.

Building the Timer Example
--------------------------

Now you are ready to build and run your project:

.. code-block:: bash

    (win)
    $ cmake .. -G "Visual Studio 14 Win64"
    $ cmake --build . --config Release

    (linux, mac)
    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .
    ...
    [100%] Built target timer
    $ ./bin/timer
    Callback called after 250 milliseconds.
    ...

Inspecting Dependencies
-----------------------

The retrieved packages are installed to your local user cache (typically *.conan/data*), and can be reused from this location for other
projects. This allows to clean your current project and continue working even without network connection. To search for packages in the
local cache run:

.. code-block:: bash

    $ conan search

To inspect binary package details (for different installed binaries for a given package recipe) run:

.. code-block:: bash

    $ conan search Poco/1.9.0@pocoproject/stable

There is also the option to generate a table for all binaries from a given recipe with the :command:`--table` option, even in remotes:

.. code-block:: bash

    $ conan search zlib/1.2.11@conan/stable --table=file.html -r=conan-center
    $ file.html # or open the file, double-click

.. image:: /images/search_binary_table.png
    :height: 250 px
    :width: 300 px
    :align: center

Check the reference for more information on how to search in remotes, how to remove or clean packages from the local cache, and how to
define a custom cache directory per user or per project.

Inspect your current project's dependencies with the :command:`conan info` command, by pointing to the location of the *conanfile.txt*
folder:

.. code-block:: bash

    $ conan info ..

Generate a graph of your dependencies using Dot or HTML formats:

.. code-block:: bash

    $ conan info .. --graph=file.html
    $ file.html # or open the file, double-click

.. image:: /images/info_deps_html_graph.png
    :height: 150 px
    :width: 200 px
    :align: center

Searching Packages
------------------

The installed packages from the remote repository are configured by default in the Conan client in the "conan-center" located in Bintray. To
search for existing packages run:

.. code-block:: bash

    $ conan search "zlib*" -r=conan-center

There are additional community repositories that can be configured and used. For more information, see
:ref:`remotes`.

.. _getting_started_other_configurations:

Building with Other Configurations
----------------------------------

In this example, we have built our project using the default configuration detected by Conan. This configuration is known as the
:ref:`default profile<default_profile>`.

A profile needs to be available prior to running commands such as :command:`conan install`. When running the command, your settings are
automatically detected (compiler, architecture...) and stored as the default profile. You can edit these settings
*~/.conan/profiles/default* or create new profiles with your desired configuration.

For example, if we have a profile with a 32-bit GCC configuration in a profile called *gcc_x86*, we can run the following:

.. code-block:: bash

    $ conan install . -pr gcc_x86

.. tip::

    We strongly recommend using :ref:`profiles` and managing them with :ref:`conan_config_install`.

However, the user can always override the default profile settings in the :command:`conan install` command using the :command:`-s`
parameter. As an exercise, try building your timer project with a different configuration. For example, try building the 32-bit version:

.. code-block:: bash

    $ conan install . -s arch=x86

The above command installs a different package, using the :command:`-s arch=x86` setting, instead of the default used previously.

To use the 32-bit binaries, you will also have to change your project build:

- In Windows, change the CMake invocation to ``Visual Studio 14``.
- In Linux, you have to add the ``-m32`` flag to your ``CMakeLists.txt`` by running ``SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m32")``, and
  the same applies to ``CMAKE_C_FLAGS, CMAKE_SHARED_LINK_FLAGS and CMAKE_EXE_LINKER_FLAGS``. This can also be done more easily, by
  automatically using Conan, as we'll show later.
- In macOS, you need to add the definition ``-DCMAKE_OSX_ARCHITECTURES=i386``.

Got any doubts? Check out our :ref:`FAQ section <faq>` or |write_us|.

.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>

.. _`conan-center`: https://bintray.com/conan/conan-center
