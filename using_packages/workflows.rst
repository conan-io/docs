.. _workflows:

Workflows
=========

This section summarizes some possible layouts and workflows when using Conan together with other
tools as an end-user for installing and consuming existing packages. To create your own
packages, please refer to :ref:`Creating Packages <packaging>`.

Whether you are working on a single configuration or a multi configuration project, in both cases, the recommended approach is to have a conanfile (either .py or .txt) at the root of
your project.

Single configuration
--------------------

When working with a  single configuration, your conanfile will be quite simple as shown in the examples and tutorials we have used so far in this user guide. For example, in
:ref:`Getting started<getting_started>`, we showed how you can run the :command:`conan install ..` command inside the *build* folder resulting in the *conaninfo.txt* and
*conanbuildinfo.cmake* files being generated there too. Note that the build folder is temporary, so you should exclude it from version control to exclude these temporary files.

**Out-of-source builds** are also supported. Let's look at a simple example:

.. code-block:: bash

    $ git clone https://github.com/memsharded/example-hello.git
    $ conan install ./example-hello --build=missing --install-folder example-hello-build

This will result in the following layout:

.. code-block:: text

    example-hello-build
      conaninfo.txt
      conanbuildinfo.txt
      conanbuildinfo.cmake
    example-hello
      conanfile.txt
      CMakeLists.txt  # If using cmake, but can be Makefile, sln...
      main.cpp

Now you are ready to build:

.. code-block:: bash

    $ cmake ../example-hello -G "Visual Studio 14 Win64"  # or other generator
    $ cmake --build . --config Release
    $ ./bin/greet

We have created a separate build configuration of the project without affecting the original
source directory in any way. The benefit is that we can freely experiment with the configuration, and, if necessary, erase the build folder, and rerun the build with a new configuration with different settings:

.. code-block:: bash

    $ cd example-hello-build && rm -rf *
    $ conan install ../example-hello -s compiler="<other compiler>" --build=missing
    $ cmake ../example-hello -G "<other generator>"
    $ cmake --build . --config Release

Multi configuration
-------------------

You can also manage different configurations, whether in-source or out of source, and switch between
them without having to re-issue the :command:`conan install` command (Note however, that even if you did have to run :command:`conan install` again, since subsequent runs use the same parameters, they would be very fast since packages would already have been installed in the local cache rather than in the project)

.. code-block:: bash

    $ git clone https://github.com/memsharded/example-hello.git
    $ conan install ./example-hello -s build_type=Debug --build=missing -if example-hello-build/debug
    $ conan install ./example-hello -s build_type=Release --build=missing -if example-hello-build/release

    $ cd example-hello-build/debug && cmake ../../example-hello -G "Visual Studio 14 Win64" && cd ../..
    $ cd example-hello-build/release && cmake ../../example-hello -G "Visual Studio 14 Win64" && cd ../..

.. note::

    You can either use the ``--install-folder`` or ``-if`` flags to specify where to generate the output files, or
    manually create the output directory and navigate to it before executing the :command:`conan install` command.

So the layout will be:

.. code-block:: text

    example-hello-build
      debug
          conaninfo.txt
          conanbuildinfo.txt
          conanbuildinfo.cmake
          CMakeCache.txt # and other cmake files
      release
          conaninfo.txt
          conanbuildinfo.txt
          conanbuildinfo.cmake
          CMakeCache.txt # and other cmake files
    example-hello
      conanfile.txt
      CMakeLists.txt  # If using cmake, but can be Makefile, sln...
      main.cpp

Now you can switch between your build configurations in exactly the same way you do for CMake or
other build systems, by moving to the folder in which the build configuration is located, because the Conan
configuration files for that build configuration will also be there.

.. code-block:: bash

    $ cd example-hello-build/debug && cmake --build . --config Debug && cd ../..
    $ cd example-hello-build/release && cmake --build . --config Release && cd ../..

Note that the CMake ``INCLUDE()`` of your project must be prefixed with the current cmake binary
directory, otherwise it will not find the necessary file:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
