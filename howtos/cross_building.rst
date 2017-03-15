.. _cross_building:

Cross building
==============

Cross building is compile a library or executable for a platform other than the one on which the compiler is running.

Cross compilation is a specially useful if you are building software for embedded devices where you don't have an operating system
nor a compiler available. Also for building software for not too fast devices, like an Android machine, a Raspberry PI etc.

The only thing that you need to cross compile some code is have the right toolchain installed in your system.
A toolchain is just a compiler with some libraries matching the target platform.

Some toochains examples:

+------------+---------------+--------------------------------------------------------------------------+
| Running on | Target        | Toolchain                                                                |
+============+===============+==========================================================================+
| Linux      | RaspberryPI   | ARM hf compiler (apt-get install g++-arm-linux-gnueabihf)                |
+------------+---------------+--------------------------------------------------------------------------+
| Linux      | Windows x64   | Mingw compiler for linux (apt-get install g++-mingw-w64)                 |
+------------+---------------+--------------------------------------------------------------------------+
| Windows    | RaspberryPI   | SysProgs toolchain http://gnutoolchains.com/raspberry/                   |
+------------+---------------+--------------------------------------------------------------------------+

Once you have the toolchain installed conan can help you to build your conan package with the :ref:`profiles<profiles>`
feature.

Conan profiles contains a predefined set of ``settings``, ``options``, ``environment variables`` and ``scopes``.
That way you can organize your target buildings adjusting the OS and the compiler of the target and setting CC and CXX environment
variables pointing to the compiler of the toolchain.

First create an example **Hello World** conan package with the :ref:`conan new command<conan_new>`:

.. code-block:: bash

    conan new mylib/1.0@lasote/stable -t


We can try to build the hello world example for our own architecture with the ``test_package`` command:


.. code-block:: bash

    $ conan test_package

    ...

    > Hello World!
    *** Running example, will fail by default, implement yours! ***
    ERROR: Error 65280 while executing ./example

The test_package command fails because it's only a template and it's asking us to override the default example.
So it's all ok, we've built a Hello World conan package for our own architecture.

From Linux to Windows
---------------------

- Install the needed toolchain (for ubuntu should be ``sudo apt-get install g++-mingw-w64``)

- Create a file named **linux_to_win64** with the contents:

.. code-block:: text

    [env]
    CC=/usr/bin/x86_64-w64-mingw32-gcc
    CXX=/usr/bin/x86_64-w64-mingw32-g++
    CONAN_CMAKE_GENERATOR=Unix Makefiles

    [settings]
    os=Windows
    compiler=gcc
    compiler.version=6.2


``CC`` and ``CXX`` are standard environment variables to declare the C/C++ compiler to use respectively.
``CONAN_MAKE_GENERATOR`` overrides the CMake generator auto-detected by the ``CMake`` conan helper.


- Call ``conan test_package`` using the created profile.

.. code-block:: bash

    $ conan test_package --profile /path/to/linux_to_win64
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/example.cpp.obj
    [100%] Linking CXX executable bin/example.exe
    [100%] Built target example

A **bin/example.exe** for Win64 platform has been built.



From Windows to Raspberry PI
----------------------------

- Install the toolchain: http://gnutoolchains.com/raspberry/

- Create a file named **win_to_rpi** with the contents:

.. code-block:: text

    [settings]
        os: Linux
        compiler: gcc
        compiler.version: 4.6
        compiler.libcxx: libstdc++
        build_type: Debug
        arch: armv6
    [env]
        CC=arm-linux-gnueabihf-gcc
        CXX=arm-linux-gnueabihf-g++


- Call ``conan test_package`` using the created profile.

.. code-block:: bash

    $ conan test_package --profile /path/to/win_to_rpi
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/example.cpp.obj
    [100%] Linking CXX executable bin/example
    [100%] Built target example

A **bin/example** for Raspberry PI (Arm hf) platform has been built.


Cross build your project and the requirements
---------------------------------------------

Remember that the ``test_package`` command is just a wrapper that export the recipe. It installs the requirements and builds an
example against the exported package to ensure that a package can be reused correctly.

If you want to cross compile your project's dependencies you can also run:

.. code-block:: bash

    $ conan install . --profile /path/to/win_to_rpi --build missing

If you have your project building automated with conan you can then just call ``conan build`` to crossbuild your project too:


.. code-block:: bash

    $ conan build


So, now you can commit your profile files to a repository and use them for cross-build your projects.
