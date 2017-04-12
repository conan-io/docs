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
``CONAN_CMAKE_GENERATOR`` overrides the CMake generator auto-detected by the ``CMake`` conan helper.


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
        arch: armv7hf
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

Remember that the ``test_package`` command is just a wrapper that exports the recipe, installs the requirements and builds an
example against the exported package to ensure that a package can be reused correctly.

If you want to cross compile your project's dependencies you can also run:

.. code-block:: bash

    $ conan install . --profile /path/to/win_to_rpi --build missing

If you have your project building automated with conan you can then just call ``conan build`` to crossbuild your project too:


.. code-block:: bash

    $ conan build


So, now you can commit your profile files to a repository and use them for cross-build your projects.



.. _cross_building_android:


Android
-------


Cross bulding a library for Android is very similar to the previous examples, except the complexity of managing different
architectures (armeabi, armeabi-v7a, x86, arm64-v8a) and the Android api levels.

You can create an Android toolchain or point directly to the desired folders in the NDK and then use a conan profile to
declare the needed environment variables, something like:

.. code-block:: text

    [settings]
    compiler=clang
    compiler.version=3.9
    compiler.libcxx=libstdc++
    os=Android
    arch=armv8
    build_type=Release

    [env]
    CC=clang
    CXX=clang++
    CFLAGS=-fPIC -DPIC -march=armv8a --sysroot=/path/to/ndk/aarch64-api21/sysroot --target=aarch64-linux-android --gcc-toolchain=/path/to/ndk/aarch64-api21
    CXXFLAGS=--target=aarch64-linux-android -fPIC -DPIC -march=armv8a --sysroot=/path/to/ndk/aarch64-api21/sysroot--gcc-toolchain=/path/to/ndk/aarch64-api21
    LDFLAGS= --target=aarch64-linux-android --sysroot=/path/to/ndk/aarch64-api21/sysroot --gcc-toolchain=/path/to/ndk/aarch64-api21

And then call ``conan install`` using the profile:


.. code-block:: bash


    $ conan install --profile my_android_profile


But if you want to use different architectures or api levels, generate many profiles handling all the different flags
and different paths it will be error prone and very tedious task.


So we created a recipe ``android-toolchain/r13b@lasote/testing`` to be used as a :ref:`build requirement<build_requires>`.


It automatically builds an Android toolchain for your specified conan settings using the NDK already installed with your
:ref:`Android Studio<android_studio>` or will install a NDK by itself.

The ``android-toolchain/r13b@lasote/testing`` recipe will fill the ``env_info`` and ``cpp_info`` objects with
information about the toolchain. Information like compiler name, cflags, sysroot path etc. You can take a look to the
recipe in its `github repository <https://github.com/lasote/conan-android-toolchain/blob/master/conanfile.py>`_.

To cross build a conan package to Android:

1. Create a new :ref:`conan profile<profiles>` and specify your settings:


**~/.conan/profiles/my_android_profile**

.. code-block:: text

    [settings]
    os=Android
    compiler=clang
    compiler.version=3.8
    compiler.libcxx=libstdc++

    arch=armv7v # Adjust
    os.api_level=21 # Adjust

    [options]
    android-toolchain:ndk_path=~/Android/Sdk/ndk-bundle # If you have a NDK already installed

    [build_requires]
    android-toolchain/r13b@lasote/testing


2. You can use the ``test_package`` or ``install`` specifying the profile.

For example, uou can try to build ``libpng/1.6.23@lasote/testing`` for Android armv7v architecture, it will also
build the ``zlib/1.2.11@lasote/testing``.


.. code-block:: bash

    conan install libpng/1.6.23@lasote/testing --build missing --profile my_android_profile -u

For your conan package you could do:



.. code-block:: bash

    conan test_package --build missing --profile my_android_profile -u


.. seealso::

    - :ref:`Integrate Conan with Android Studio<android_studio>`
    - `Android NDF standalone toolchains <https://developer.android.com/ndk/guides/standalone_toolchain.html?hl=es>`_.



Toolchain packages as build requirements
----------------------------------------

The :ref:`Build requirements<build_requires>` feature allows to create packages that "inject" C/C++ flags
and environment variables through ``cpp_info`` and ``env_info`` objects.

This is specially useful to create packages with toolchains for cross building because:

- The toolchain package can be specified in a profile and kept isolated from out library package.
  We won't need to change anything in the conan package of our library to cross build it for different targets.
  We can have different profiles using different ``build_requires`` to build our library for example, for Android,
  Windows, Raspberry PI etc.

- The toolchain package will manage all the complexity of the toolchain, just declaring the environment variables and
  C/C++ flags that we need to cross build a library. The toolchain package is able to read the specified user settings, so
  can 'inject' different flags for different user settings.

- The toolchain packages can be easily shared as any other conan package, using a conan server. Downloading and
  installing a toolchain and getting it work could be a difficult task.






ARM reference
-------------
Remember that the conan settings are intended to unify the different names for operating systems, compilers,
architectures etc.

Conan has different architecture settings for ARM: ``armv6``, ``armv7``, ``armv7hf``, ``armv8``.
The "problem" with ARM architecture is that frequently are named in different ways, so maybe you are wondering what setting
do you need to specify in your case.

Here is a table with some typical ARM platorms:

+--------------------------------+------------------------------------------------------------------------------------------------+
| Platform                       | Conan setting                                                                                  |
+================================+================================================================================================+
| Raspberry PI 1 and 2           | ``armv7`` or ``armv7hf`` if we want to use the float point hard support                        |
+--------------------------------+------------------------------------------------------------------------------------------------+
| Raspberry PI 3                 | ``armv8`` also known as armv64-v8a                                                             |
+--------------------------------+------------------------------------------------------------------------------------------------+
| Visual Studio                  | ``armv7`` currently Visual Studio builds ``armv7`` binaries when you select ARM.               |
+--------------------------------+------------------------------------------------------------------------------------------------+
| Android armbeabi-v7a           | ``armv7``                                                                                      |
+--------------------------------+------------------------------------------------------------------------------------------------+
| Android armv64-v8a             | ``armv8``                                                                                      |
+--------------------------------+------------------------------------------------------------------------------------------------+
| Android armeabi                | ``armv6`` (as a minimal compatible, will be compatible with v7 too)                            |
+--------------------------------+------------------------------------------------------------------------------------------------+



.. seealso:: Reference links

    **ARM**

    - https://developer.arm.com/docs/dui0773/latest/compiling-c-and-c-code/specifying-a-target-architecture-processor-and-instruction-set
    - https://developer.arm.com/docs/dui0774/latest/compiler-command-line-options/-target
    - https://developer.arm.com/docs/dui0774/latest/compiler-command-line-options/-march

    **ANDROID**

    - https://developer.android.com/ndk/guides/standalone_toolchain.html

    **VISUAL STUDIO**

    - https://msdn.microsoft.com/en-us/library/dn736986.aspx




Useful CMake configuration variables
------------------------------------

If you are using CMake to cross build your project you can adjust some Conan configuration variables, you can also
use environment variables:

+-----------------------------------+------------------------------------------------------------------------------------------------+
| conan.conf variable               | Environment variable                                                                           |
+===================================+================================================================================================+
| cmake_system_name                 |  CONAN_CMAKE_SYSTEM_NAME                                                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| cmake_system_version              |  CONAN_CMAKE_SYSTEM_VERSION                                                                    |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| cmake_system_processor            |  CONAN_CMAKE_SYSTEM_PROCESSOR                                                                  |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| cmake_find_root_path              |  CONAN_CMAKE_FIND_ROOT_PATH                                                                    |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| cmake_find_root_path_mode_program |  CONAN_CMAKE_FIND_ROOT_PATH_MODE_PROGRAM                                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| cmake_find_root_path_mode_library |  CONAN_CMAKE_FIND_ROOT_PATH_MODE_LIBRARY                                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| cmake_find_root_path_mode_include |  CONAN_CMAKE_FIND_ROOT_PATH_MODE_INCLUDE                                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------+


.. seealso::

    - See :ref:`conan.conf file<conan_conf>` and :ref:`Environment variables <env_vars>` sections to know more.
    - See `CMake cross building wiki <http://www.vtk.org/Wiki/CMake_Cross_Compiling>`_ to know more about cross building with CMake.


