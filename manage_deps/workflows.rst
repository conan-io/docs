.. _workflows:


Workflows
=========

This section summarizes some possible layouts and workflows while using conan together with other
tools as an end-user, i.e. installing and consuming existing packages. For creating your own
packages, have a look at the :ref:`Packaging section <packaging>`.


In both cases, the recommended approach is to have a conanfile (either .py or .txt) at the root of
your project.

Single configuration (one conf at a time)
-----------------------------------------
The single configuration is simple. It is the one that has been used so far for the examples and
tutorials. In :ref:`Getting started<getting_started>`, we ran the ``conan install`` command in the project root folder,
and the ``conaninfo.txt`` and ``conanbuildinfo.cmake`` files were generated there.

But out-of-source builds are also supported. Let's make a simple example:

.. code-block:: bash
   
      $ git clone https://github.com/memsharded/example-hello.git
      $ mkdir example-hello-build && cd example-hello-build
      $ conan install ../example-hello --build=missing
      
So the layout will be:
      
::

   example-hello-build
      conaninfo.txt
      conanbuildinfo.cmake
   example-hello
      conanfile.txt
      CMakeLists.txt  # If using cmake, but can be Makefile, sln...
      main.cpp


Now you are ready to build:

.. code-block:: bash
   
      $ cmake ../example-hello -G ...
      $ cmake --build . --config Release
      
In effect, with this setup, we have created a separate configuration of the project, without
affecting at all the original source directory. The benefit is that we can experiment freely, and even erase it and
create a new build with a new configuration with different settings, if needed:

.. code-block:: bash<
   
      $ cd example-hello-build
      $ rm -rf *
      $ conan install ../example-hello -s compiler="change compiler" --build=missing
      $ cmake ../example-hello -G ...
      $ cmake --build . --config Release

      

Multi configuration
-------------------
You can also manage different configurations, in-source or out of source, and you can switch
between them without taking the extra step of re-issuing the ``conan install`` command (even
though this is not an speed related issue, since the second time ``conan install`` is executed
with the same parameters, it will run very fast. Packages are installed in the cache, not inside
the project).

.. code-block:: bash
   
      $ git clone https://github.com/memsharded/example-hello.git
      $ mkdir example-hello-build && cd example-hello-build
      $ mkdir debug && cd debug
      $ conan install ../../example-hello -s build_type=Debug --build=missing
      $ cmake ../../example-hello -G "Visual Studio 14 Win64"
      $ cd .. && mkdir release && cd release
      $ conan install ../../example-hello -s build_type=Release --build=missing
      $ cmake ../../example-hello -G "Visual Studio 14 Win64"
      
      
      
So the layout will be:
      
::

   example-hello-build
      debug
          conaninfo.txt
          conanbuildinfo.cmake
          CMakeCache.txt # and other cmake files
      release
          conaninfo.txt
          conanbuildinfo.cmake
          CMakeCache.txt # and other cmake files
   example-hello
      conanfile.txt
      CMakeLists.txt  # If using cmake, but can be Makefile, sln...
      main.cpp

Now you can switch between your build configurations in exactly the same way you do for
CMake or other build systems, moving to the folder in which the build configuration lives, because
the conan configuration files for that build configuration will also be there.

.. code-block:: bash
   
      $ cd example-hello-build/debug
      $ cmake --build . --config Debug
      $ cd ../release
      $ cmake --build . --config Release
      
Note that the CMake ``INCLUDE()`` of your project must be prefixed with the current cmake binary
directory, otherwise it will not find the necessary file:

.. code-block:: cmake

   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup()
