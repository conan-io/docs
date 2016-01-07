.. _boost_example:

Boost
=====

Boost doesn't need any intro. Let's go straight to build the typical regex example against Boost 1.60.
There are more than 60 pre-built binary packages in conan.io. Check them out at https://www.conan.io/source/Boost/1.60.0/lasote/stable


It is very easy to set up your own project, but here is a repository for convenience:


.. code-block:: bash

   $ git clone https://github.com/memsharded/example-boost.git


It contains a very simple ``CMakeLists.txt``, the ``main.cpp`` source file of the regex example
and a ``conanfile.txt`` with the following contents:

.. code-block:: text

   [requires]
   Boost/1.60.0@lasote/stable
   
   [generators]
   cmake
   
   [imports]
   bin, *.dll -> ./bin
   lib, *.dylib* -> ./bin


Install the requirements, configure the project with CMake, and build it:

.. code-block:: bash

   $ cd example-boost
   $ mkdir build && cd build
   $ conan install ..
   $ cmake .. -G "Visual Studio 14 Win64"
   $ cmake --build . --config Release
   $ cd bin
   $ regex

The above configuration assumes that your predefined settings are VS14, 64 bits, Release, MD runtime.
If your settings are different, just specify them while executing conan install, e.g.:

.. code-block:: bash

   $ conan install .. -s compiler="Visual Studio" -s compiler.version=12 -s arch=x86 -s build_type=Debug -s compiler.runtime=MDd
   $ cmake .. -G "Visual Studio 12"
   $ cmake --build . --config Debug

In the case above, it is important to specify the runtime ``MDd`` to be compatible with the ``Debug`` 
version we are requesting.

This is the project's ``CMakeLists.txt``:

.. code-block:: cmake

   project(MyRegex)
   cmake_minimum_required(VERSION 2.8)

   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup()

   # Just comment or uncomment the FindPackage line to use it or not
   find_package(Boost 1.60.0 COMPONENTS regex)
   if(Boost_FOUND)
      include_directories(${Boost_INCLUDE_DIRS})
      add_executable(regex main.cpp)
      target_link_libraries(regex ${Boost_LIBRARIES})
   else()
      add_executable(regex main.cpp)
      target_link_libraries(regex ${CONAN_LIBS})
   endif()

You can see that the traditional ``find_package()`` approach is supported. It is not strictly
necessary, as the ``conanbuildinfo.cmake`` already declares all the variables required to build
your application. But if your project's ``CMakeLists.txt`` already uses ``find_package()`` for Boost,
it is very easy to maintain the project with or without using conan.

Non CMake projects
------------------
Even if you are not using ``cmake`` in your project, it is possible to use conan. Put the
following ``conanfile.txt`` in your project root:

.. code-block:: text

   [requires]
   Boost/1.60.0@lasote/stable

   [generators]
   visual_studio

   [imports]
   bin, *.dll -> ./bin
   lib, *.dylib* -> ./bin


Install your requirements as above:

.. code-block:: bash

   $ conan install -s compiler="Visual Studio" -s compiler.version=14 -s arch=x86 -s build_type=Release

Then follow the instructions in :ref:`Visual Studio generator <visual_studio>` to load the generated
``conanbuildinfo.props`` into your project. Ensure that your project configuration matches the
installed requirements and build as usual. The above ``conanfile.txt`` assumes that the output
directory will be the ``bin`` one, and will put the boost dynamic libraries there, if needed. You
can either configure your Visual Studio project or your ``conanfile.txt`` to use the same output
directory for convenience when launching or debugging your application.


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
   
