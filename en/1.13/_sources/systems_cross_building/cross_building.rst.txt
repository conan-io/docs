.. _cross_building:

Cross building
==============

Cross building is compiling a library or executable in one platform to be used in a different one.

Cross-compilation is used to build software for embedded devices where you don't have an operating system
nor a compiler available. Also for building software for not too fast devices, like an Android machine, a Raspberry PI etc.

To cross build code you need the right toolchain.
A toolchain is basically a compiler with a set of libraries matching the ``host`` platform.


GNU triplet convention
----------------------

According to the GNU convention, there are three platforms involved in the software building:

- **Build platform:** The platform on which the compilation tools are executed
- **Host platform:** The platform on which the code will run
- **Target platform:** Only when building a compiler, this is the platform that the compiler will
  generate code for


When you are building code for your own machine it's called **native building**, where the ``build``
and the ``host`` platforms are the same. The ``target`` platform is not defined in this situation.

When you are building code for a different platform, it's called **cross building**, where the ``build``
platform is different from the ``host`` platform. The ``target`` platform is not defined in this situation.

The use of the ``target`` platform is rarely needed, only makes sense when you are building a compiler. For instance,
when you are building in your Linux machine a GCC compiler that will run on Windows, to generate code for Android.
Here, the ``build`` is your Linux computer, the ``host`` is the Windows computer and the ``target`` is Android.


Conan settings
--------------

From version 1.0, Conan introduces new settings to model the GNU convention triplet:

``build`` platform settings:

    - **os_build**: Operating system of the ``build`` system.
    - **arch_build**: Architecture system of the ``build`` system.

    These settings are detected the first time you run Conan with the same values than the ``host`` settings,
    so by default, we are doing **native building**. Probably you will never need to change the value
    of this settings because they describe where are you running Conan.


``host`` platform settings:

    - **os**: Operating system of the ``host`` system.
    - **arch**: Architecture of the ``host`` system.
    - **compiler**: Compiler of the ``host`` system (to declare compatibility of libs in the host platform)
    - ... (all the regular settings)

    These settings are the regular Conan settings, already present before supporting the GNU triplet convention.
    If you are cross building you have to change them according to the ``host`` platform.


``target`` platform:

    - **os_target**: Operating system of the ``target`` system.
    - **arch_target**: Architecture of the ``target`` system.

    If you are building a compiler, specify with these settings where the compiled code will run.


Cross building with Conan
-------------------------

If you want to cross-build a Conan package, for example, in your Linux machine, build the `zlib`
Conan package for Windows, you need to indicate to Conan where to find your cross-compiler/toolchain.

There are two approaches:

- Install the toolchain in your computer and use a ``profile`` to declare the settings and
  point to the needed tools/libraries in the toolchain using the ``[env]`` section to declare, at least,
  the ``CC`` and ``CXX`` environment variables.

- Package the toolchain as a Conan package and include it as a ``build_require``.


Using profiles
++++++++++++++

Create a profile with:

- A **[settings]** section containing the needed settings: ``os_build``, ``arch_build`` and the regular
  settings ``os``, ``arch``, ``compiler``, ``build_type`` and so on.

- An **[env]** section with a PATH variable pointing to your installed toolchain. Also any other variable
  that the toolchain expects (read the docs of your compiler). Some build systems need a variable ``SYSROOT`` to locate
  where the host system libraries and tools are.


Linux to Windows
................

- Install the needed toolchain, in ubuntu:

    ``sudo apt-get install g++-mingw-w64 gcc-mingw-w64``

- Create a file named **linux_to_win64** with the contents:

.. code-block:: text

    $toolchain=/usr/x86_64-w64-mingw32 # Adjust this path
    target_host=x86_64-w64-mingw32
    cc_compiler=gcc
    cxx_compiler=g++

    [env]
    CONAN_CMAKE_FIND_ROOT_PATH=$toolchain
    CHOST=$target_host
    AR=$target_host-ar
    AS=$target_host-as
    RANLIB=$target_host-ranlib
    CC=$target_host-$cc_compiler
    CXX=$target_host-$cxx_compiler
    STRIP=$target_host-strip
    RC=$target_host-windres

    [settings]
    # We are building in Ubuntu Linux
    os_build=Linux
    arch_build=x86_64

    # We are cross building to Windows
    os=Windows
    arch=x86_64
    compiler=gcc

    # Adjust to the gcc version of your MinGW package
    compiler.version=7.3
    compiler.libcxx=libstdc++11
    build_type=Release

- Clone an example recipe or use your own recipe:

.. code-block:: bash

    git clone https://github.com/memsharded/conan-hello.git

- Call :command:`conan create` using the created **linux_to_win64**

.. code-block:: bash

    $ cd conan-hello && conan create . conan/testing --profile ../linux_to_win64
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/example.cpp.obj
    [100%] Linking CXX executable bin/example.exe
    [100%] Built target example

A *bin/example.exe* for Win64 platform has been built.

Windows to Raspberry PI (Linux/ARM)
...................................

- Install the toolchain: http://gnutoolchains.com/raspberry/
  You can choose different versions of the GCC cross compiler, choose one and adjust the following
  settings in the profile accordingly.

- Create a file named **win_to_rpi** with the contents:

.. code-block:: text

    target_host=arm-linux-gnueabihf
    standalone_toolchain=C:/sysgcc/raspberry
    cc_compiler=gcc
    cxx_compiler=g++

    [settings]
    os_build=Windows
    arch_build=x86_64
    os=Linux
    arch=armv7 # Change to armv6 if you are using Raspberry 1
    compiler=gcc
    compiler.version=6
    compiler.libcxx=libstdc++11
    build_type=Release

    [env]
    CONAN_CMAKE_FIND_ROOT_PATH=$standalone_toolchain/$target_host/sysroot
    PATH=[$standalone_toolchain/bin]
    CHOST=$target_host
    AR=$target_host-ar
    AS=$target_host-as
    RANLIB=$target_host-ranlib
    LD=$target_host-ld
    STRIP=$target_host-strip
    CC=$target_host-$cc_compiler
    CXX=$target_host-$cxx_compiler
    CXXFLAGS=-I"$standalone_toolchain/$target_host/lib/include"

The profiles to target Linux are all very similar, probably you just need to adjust the variables
declared in the top of the profile:

    - **target_host**: All the executables in the toolchain starts with this prefix.
    - **standalone_toolchain**: Path to the toolchain installation.
    - **cc_compiler/cxx_compiler**: In this case ``gcc``/``g++``, but could be ``clang``/``clang++``.


- Clone an example recipe or use your own recipe:

.. code-block:: bash

    git clone https://github.com/memsharded/conan-hello.git

- Call :command:`conan create` using the created profile.

.. code-block:: bash

    $ cd conan-hello && conan create . conan/testing --profile=../win_to_rpi
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/example.cpp.obj
    [100%] Linking CXX executable bin/example
    [100%] Built target example

A *bin/example* for Raspberry PI (Linux/armv7hf) platform has been built.

.. _cross_building_android:

Linux/Windows/macOS to Android
..............................

Cross building a library for Android is very similar to the previous examples, except the complexity of managing different
architectures (armeabi, armeabi-v7a, x86, arm64-v8a) and the Android API levels.

Download the Android NDK `here <https://developer.android.com/ndk/downloads>`_ and unzip it.

.. note::

    If you are in Windows the process will be almost the same, but unzip the file in the root folder of your hard disk (``C:\``) to avoid issues with path lengths.

Now you have to build a `standalone toolchain <https://developer.android.com/ndk/guides/standalone_toolchain>`_,
we are going to target "arm" architecture and the Android API level 21, change the ``--install-dir`` to any other place that works
for you:

.. code-block:: bash

   $ cd build/tools
   $ python make_standalone_toolchain.py --arch=arm --api=21 --stl=libc++ --install-dir=/myfolder/arm_21_toolchain


.. note::

    You can generate the standalone toolchain with several different options to target different architectures, api levels etc.

    Check the Android docs: `standalone toolchain <https://developer.android.com/ndk/guides/standalone_toolchain>`_


To use the ``clang`` compiler, create a profile ``android_21_arm_clang``. Once again, the profile is very similar to the
RPI one:

.. code-block:: text

    standalone_toolchain=/myfolder/arm_21_toolchain # Adjust this path
    target_host=arm-linux-androideabi
    cc_compiler=clang
    cxx_compiler=clang++

    [settings]
    compiler=clang
    compiler.version=5.0
    compiler.libcxx=libc++
    os=Android
    os.api_level=21
    arch=armv7
    build_type=Release

    [env]
    CONAN_CMAKE_FIND_ROOT_PATH=$standalone_toolchain/sysroot
    PATH=[$standalone_toolchain/bin]
    CHOST=$target_host
    AR=$target_host-ar
    AS=$target_host-as
    RANLIB=$target_host-ranlib
    CC=$target_host-$cc_compiler
    CXX=$target_host-$cxx_compiler
    LD=$target_host-ld
    STRIP=$target_host-strip
    CFLAGS= -fPIE -fPIC -I$standalone_toolchain/include/c++/4.9.x
    CXXFLAGS= -fPIE -fPIC -I$standalone_toolchain/include/c++/4.9.x
    LDFLAGS= -pie


You could also use ``gcc`` using this profile ``arm_21_toolchain_gcc``, changing the ``cc_compiler`` and
``cxx_compiler`` variables, removing ``-fPIE`` flag and, of course, changing the ``[settings]`` to
match the gcc toolchain compiler:


.. code-block:: text

    standalone_toolchain=/myfolder/arm_21_toolchain
    target_host=arm-linux-androideabi
    cc_compiler=gcc
    cxx_compiler=g++

    [settings]
    compiler=gcc
    compiler.version=4.9
    compiler.libcxx=libstdc++
    os=Android
    os.api_level=21
    arch=armv7
    build_type=Release

    [env]
    CONAN_CMAKE_FIND_ROOT_PATH=$standalone_toolchain/sysroot
    PATH=[$standalone_toolchain/bin]
    CHOST=$target_host
    AR=$target_host-ar
    AS=$target_host-as
    RANLIB=$target_host-ranlib
    CC=$target_host-$cc_compiler
    CXX=$target_host-$cxx_compiler
    LD=$target_host-ld
    STRIP=$target_host-strip
    CFLAGS= -fPIC -I$standalone_toolchain/include/c++/4.9.x
    CXXFLAGS= -fPIC -I$standalone_toolchain/include/c++/4.9.x
    LDFLAGS=

- Clone, for example, the zlib library to try to build it to Android

.. code-block:: bash

    git clone https://github.com/conan-community/conan-zlib.git

- Call :command:`conan create` using the created profile.

.. code-block:: bash

    $ cd conan-zlib && conan create . conan/testing --profile=../android_21_arm_clang

    ...
    -- Build files have been written to: /tmp/conan-zlib/test_package/build/ba0b9dbae0576b9a23ce7005180b00e4fdef1198
    Scanning dependencies of target enough
    [ 50%] Building C object CMakeFiles/enough.dir/enough.c.o
    [100%] Linking C executable bin/enough
    [100%] Built target enough
    zlib/1.2.11@conan/testing (test package): Running test()

A **bin/enough** for Android ARM platform has been built.

Using build requires
++++++++++++++++++++

Instead of downloading manually the toolchain and creating a profile, you can create a Conan package
with it. The toolchain Conan package needs to fill the ``env_info`` object
in the :ref:`package_info()<method_package_info>` method with the same variables we've specified in the examples
above in the ``[env]`` section of profiles.

A layout of a Conan package for a toolchain could looks like this:


.. code-block:: python

   from conans import ConanFile
   import os


   class MyToolchainXXXConan(ConanFile):
       name = "my_toolchain"
       version = "0.1"
       settings = "os_build", "arch_build"

       def build(self):
           # Typically download the toolchain for the 'build' host
           url = "http://fake_url.com/installers/%s/%s/toolchain.tgz" % (os_build, os_arch)
           tools.download(url, "toolchain.tgz")
           tools.unzip("toolchain.tgz")

       def package(self):
           # Copy all the
           self.copy("*", dst="", src="toolchain")

       def package_info(self):
           bin_folder = os.path.join(self.package_folder, "bin")
           self.env_info.path.append(bin_folder)
           self.env_info.CC = os.path.join(bin_folder, "mycompiler-cc")
           self.env_info.CXX = os.path.join(bin_folder, "mycompiler-cxx")
           self.env_info.SYSROOT = self.package_folder

Finally, when you want to cross-build a library, the profile to be used, will include a ``[build_requires]``
section with the reference to our new packaged toolchain. Also will contain a ``[settings]`` section
with the same settings of the examples above.


.. _darwin_toolchain:

Example: Darwin Toolchain
.........................

Check the `Darwin Toolchain <https://github.com/theodelrieu/conan-darwin-toolchain>`_  package in conan-center.
You can use a profile like the following to cross build your packages for ``iOS``,  ``watchOS`` and ``tvOS``:

.. code-block:: text
    :caption: ios_profile

    include(default)

    [settings]
    os=iOS
    os.version=9.0
    arch=armv7

    [build_requires]
    darwin-toolchain/1.0@theodelrieu/stable


.. code-block:: bash

    $ conan install . --profile ios_profile

.. seealso::

    - Check the :ref:`Creating conan packages to install dev tools<create_installer_packages>` to learn
      more about how to create Conan packages for tools.

    - Check the `mingw-installer <https://github.com/conan-community/conan-mingw-installer/blob/master/conanfile.py>`_ build require recipe as an example of packaging a compiler.


Using Docker images
+++++++++++++++++++

You can use some :ref:`available docker images with Conan preinstalled images<available_docker_images>` to cross build conan packages.
Currently there are ``i386``, ``armv7`` and ``armv7hf`` images with the needed packages and toolchains installed to cross build.

**Example**: Cross-building and uploading a package along with all its missing dependencies for ``Linux/armv7hf`` is done in few steps:

.. code-block:: bash

    $ git clone https://github.com/conan-community/conan-openssl
    $ cd conan-openssl
    $ docker run -it -v$(pwd):/home/conan/project --rm conanio/gcc49-armv7hf /bin/bash

    # Now we are running on the conangcc49-armv7hf container
    $ sudo pip install conan --upgrade
    $ cd project

    $ conan create . user/channel --build missing
    $ conan remote add myremoteARMV7 http://some.remote.url
    $ conan upload "*" -r myremoteARMV7 --all


Check the section: :ref:`How to run Conan with Docker<docker_conan>` to know more.


Preparing recipes to be cross-compiled
++++++++++++++++++++++++++++++++++++++

If you use the build helpers :ref:`AutoToolsBuildEnvironment<autotools_reference>` or :ref:`CMake<cmake_reference>`,
Conan will adjust the configuration accordingly to the specified settings.

If don't, you can always check the ``self.settings.os``, ``self.settings.build_os``,
``self.settings.arch`` and ``self.settings.build_arch`` settings values and inject the needed flags to your
build system script.

You can use this tool to check if you are cross building:

- :ref:`tools.cross_building(self.settings)<cross_building_reference>` (returns True or False)


ARM architecture reference
--------------------------

Remember that the conan settings are intended to unify the different names for operating systems, compilers,
architectures etc.

Conan has different architecture settings for ARM: ``armv6``, ``armv7``, ``armv7hf``, ``armv8``.
The "problem" with ARM architecture is that frequently are named in different ways, so maybe you are wondering what setting
do you need to specify in your case.

Here is a table with some typical ARM platforms:

+--------------------------------+------------------------------------------------------------------------------------------------+
| Platform                       | Conan setting                                                                                  |
+================================+================================================================================================+
| Raspberry PI 1                 | ``armv6``                                                                                      |
+--------------------------------+------------------------------------------------------------------------------------------------+
| Raspberry PI 2                 | ``armv7`` or ``armv7hf`` if we want to use the float point hard support                        |
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

    - https://developer.arm.com/docs/100066/0604/compiling-c-and-c-code/specifying-a-target-architecture-processor-and-instruction-set
    - https://developer.arm.com/docs/dui0472/latest/compiler-command-line-options

    **ANDROID**

    - https://developer.android.com/ndk/guides/standalone_toolchain

    **VISUAL STUDIO**

    - https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild-command-line-reference?view=vs-2017


.. seealso::

    - See :ref:`conan.conf file<conan_conf>` and :ref:`Environment variables <env_vars>` sections to know more.
    - See :ref:`AutoToolsBuildEnvironment build helper<autotools_reference>` reference.
    - See :ref:`CMake build helper<cmake_reference>` reference.
    - See `CMake cross building wiki <https://vtk.org/Wiki/CMake_Cross_Compiling>`_ to know more about cross building with CMake.
