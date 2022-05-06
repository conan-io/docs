
.. _examples-tools-cmake-toolchain-build-project:

CMakeToolchain: Building your project
=====================================

In this example we are going to see how to use ``CMakeToolchain`` and predefined layouts like ``cmake_layout``
to ease the way we build our project locally (calling CMake directly).

Let's create a basic project based on the template ``cmake_exe`` as an example of a C++ project:

.. code:: bash

    $ conan new -d name=foo -d version=1.0 cmake_exe


Generating the toolchain
------------------------

The recipe from our project declares the generator "CMakeToolchain".

We can call :command:`conan install` to install both ``Release`` and ``Debug`` configurations without taking care
of the output folder of the generated files, (avoiding ``--output-folder`` argument), the
toolchain will be always at the same place.

The ``conan_toolchain.cmake`` is common for both configurations and located at *build/generators* folder:

.. code:: bash

    $ conan install .
    $ conan install . -s build_type=Debug



.. note::

    The `build/generators` location is declared by the ``cmake_layout()`` in the ``layout()`` method.


Building the project
--------------------


If you are using a multi-configuration generator:

.. code:: bash

    $ cd build
    $ cmake .. -G "Visual Studio 15" -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake
    # Now you can open the IDE, select Debug or Release config and build
    # or, in the command line
    $ cmake --build . --config Release
    $ Release\foo.exe
      foo/1.0: Hello World Release!

    $ cmake --build . --config Debug
    $ Debug\foo.exe
      foo/1.0: Hello World Debug!


**NOTE**: The platform (Win64), is already encoded in the toolchain. The command line shouldn't pass it, so using
``-G "Visual Studio 15"`` instead of the ``-G "Visual Studio 15 Win64"``


If you are using a single-configuration generator:

.. code:: bash

    $ mkdir cmake-build-release && cmake-build-release
    $ cmake ..  -DCMAKE_TOOLCHAIN_FILE=../build/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .
    $ ./foo
    foo/1.0: Hello World Release!

    $ mkdir cmake-build-debug && cmake-build-debug
    $ cmake ..  -DCMAKE_TOOLCHAIN_FILE=../build/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Debug
    $ cmake --build .
    $ ./foo
    foo/1.0: Hello World Debug!
