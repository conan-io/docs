.. _cross_building:

Cross building
==============

Cross building (or cross compilation) is the process of generating binaries for a platform that is not the one
where the compiling process is running.

Cross compilation is mostly used to build software for an alien device, such as an embedded device where you don't have an operating system
nor a compiler available. It's also used to build software for slower devices, like an Android machine or a Raspberry Pi where running
the native compilation will take too much time.

In order to cross build a codebase the right toolchain is needed, with a proper compiler (cross compiler), a linker
and the set of libraries matching the ``host`` platform.


GNU triplet convention
----------------------

According to the GNU convention, there are three platforms involved in the software building:

- **Build platform:** The platform on which the compilation tools are being executed.
- **Host platform:** The platform on which the generated binaries will run.
- **Target platform:** Only when building a cross compiler, it is the platform it will generate binaries for.


Depending on the values of these platforms, there are different scenarios:

* **Native building**: when the ``build`` and the ``host`` platforms are the same, it means
  that the platform where the compiler is running is the same one where the generated binaries will run.
  This is the most common scenario.
* **Cross building**: when the ``build`` and the ``host`` platform are different, it requires
  a cross compiler running in the build platform that generates binaries for the host platform.


The ``target`` platform plays and important role when compiling a cross compiler, in that scenario
the ``target`` is the platform the compiler will generate binaries for: in order to be a cross compiler
the ``host`` platform (where the cross compiler will run) has to be different from the ``target`` platform.
If the ``build`` platform is also different, it is called **Canadian Cross**.

Let's illustrate these scenarios with some examples:

* The Android NDK is a cross compiler to Android: it can be executed in Linux (the ``build`` platform)
  to generate binaries for Android (the ``host`` platform).
* The Android NDK was once compiled, during that compilation a different compiler was used running in
  a ``build`` platform (maybe Windows) to generate the actual Android NDK that will run in the ``host``
  platform Linux, and as we saw before, that Android NDK cross compiler will generate binaries for 
  a ``target`` platform which is Android.

The values of the ``build``, ``host`` and ``target`` platforms are not absolute, and
they depend on the process we are talking about. The ``host`` when compiling a cross compiler turns
into the ``build`` when using that same cross compiler, or the ``target`` of the cross compiler is
the ``host`` platform of the binaries generated with it.


.. seealso::

    One way to avoid this complexity is to run the compilation in the host platform, so both ``build`` and
    ``host`` will take the same value and it will be a *native compilation*. Docker is a very successful
    tool that can help you with this, read more about it in :ref:`this section <use_docker_to_crossbuild>`.


Cross building with Conan
-------------------------

If you want to cross build a Conan package (for example using your Linux machine) to build the ``zlib``
Conan package for Windows, you need to tell Conan where to find your toolchain/cross compiler.

There are two approaches:

- Install the toolchain in your computer and use a ``profile`` to declare the settings and
  point to the needed tools/libraries in the toolchain using the ``[env]`` section to declare, at least,
  the ``CC`` and ``CXX`` environment variables.

- Package the toolchain as a Conan package and include it as a ``build_requires``.


Using a profile
+++++++++++++++

Using a Conan profile we can declare not only the ``settings`` that will identify our binary, but also
all the environment variables needed to use a toolchain or cross compiler. The profile needs the following
sections:

- A **[settings]** section containing the regular settings: ``os``, ``arch``, ``compiler`` and ``build_type``
  depending on your library. These settings will identify your binary.

- An **[env]** section with a PATH variable pointing to your installed toolchain. Also any other variable
  that the toolchain expects (read the docs of your compiler). Some build systems need a variable ``SYSROOT`` to locate
  where the host system libraries and tools are.

For example, in the following profile we declare the ``host`` platform to be Windows x86_64 with the
compiler, version and other settings be are using. And we add the **[env]** section with all the variables
needed to use an installed toolchain:

.. code-block:: ini

    toolchain=/usr/x86_64-w64-mingw32 # Adjust this path
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
    # We are cross-building to Windows
    os=Windows
    arch=x86_64
    compiler=gcc

    # Adjust to the gcc version of your MinGW package
    compiler.version=7.3
    compiler.libcxx=libstdc++11
    build_type=Release

You can find working examples at the :ref:`bottom of this section <cross_building_examples_profiles>`.


.. _cross_building_build_requires:

Using build requires
++++++++++++++++++++

Instead of manually downloading the toolchain and creating a profile, you can create a Conan package
with it. Starting with Conan v1.24 and the command line arguments ``--profile:host`` and ``--profile:build``
this should be a regular recipe, for older versions some more work is needed.


Conan v1.24 and newer
.....................

A recipe with a toolchain is like any other recipe with a binary executable:

.. code-block:: python

    import os
    from conans import ConanFile

    class MyToolchainXXXConan(ConanFile):
        name = "my_toolchain"
        version = "0.1"
        settings = "os", "arch", "compiler", "build_type"

        # Implement source() and build() as usual

        def package(self):
            # Copy all the required files for your toolchain
            self.copy("*", dst="", src="toolchain")

        def package_info(self):
            bin_folder = os.path.join(self.package_folder, "bin")
            self.env_info.CC = os.path.join(bin_folder, "mycompiler-cc")
            self.env_info.CXX = os.path.join(bin_folder, "mycompiler-cxx")
            self.env_info.SYSROOT = self.package_folder


The Conan package with the toolchain needs to fill the ``env_info`` object
in the :ref:`package_info()<method_package_info>` method with the same variables we've specified in the examples
above in the ``[env]`` section of profiles.

Then you will need to consume this recipe as any regular :ref:`build requires <build_requires>` that belongs to the
``build`` context: you need to use the ``--profile:build`` argument in the command line while creating your library:

.. code-block:: bash

    conan create path/to/conanfile.py --profile:build=profile_build --profile:host=profile_host


.. image:: ../images/xbuild/conan-my_toolchain.png
   :width: 400 px
   :align: center


The profile ``profile_build`` will contain just the settings related to your ``build`` platform, where you are
running the command, and the ``profile_host`` will list the settings for the ``host`` platform (and eventually
the ``my_toolchain/0.1`` as ``build_requires`` if it is not listed in the recipe itself).

Conan will apply the appropiate profile to each recipe, and will inject the environment of all the build requirements
that belong to the ``build`` context before running the ``build()`` method of the libraries being compiled.
That way, the environment variables ``CC``, ``CXX`` and ``SYSROOT`` from ``my_toolchain/0.1`` will be available
and also the path to the ``bindirs`` directory from that package.

The above means that **Conan is able to compile the full graph in a single execution**, it will compile
the build requires using the ``profile_build`` and then it will compile the libraries using the ``host_profile``
settings applying the environment of the former ones.


Conan older than v1.24
......................

.. warning::

    We ask you to use the previous approach for Conan 1.24 and newer, and avoid any specific modification
    of your recipes to make them work as build requirements in a cross building scenario.


With this approach, only one profile is provided in the command line (the ``--profile:host`` or just ``--profile``)
and it has to define the ``os_build`` and ``arch_build`` settings too. The recipe of this build requires
has to be modified to take into account these settings and the ``compiler`` and
``build_type`` settings have to be removed because their values for the ``build`` platform are not defined
in the profile:


.. code-block:: python

    from conans import ConanFile
    import os


    class MyToolchainXXXConan(ConanFile):
        name = "my_toolchain"
        version = "0.1"
        settings = "os_build", "arch_build"

        # As typically, this recipe doesn't declare 'compiler' and 'build_type',
        #   the source() and build() methods need a custom implementation
        def build(self):
            # Typically download the toolchain for the 'build' platform
            url = "http://fake_url.com/installers/%s/%s/toolchain.tgz" % (os_build, os_arch)
            tools.download(url, "toolchain.tgz")
            tools.unzip("toolchain.tgz")

        def package(self):
            # Copy all the required files for your toolchain
            self.copy("*", dst="", src="toolchain")

        def package_info(self):
            bin_folder = os.path.join(self.package_folder, "bin")
            self.env_info.PATH.append(bin_folder)
            self.env_info.CC = os.path.join(bin_folder, "mycompiler-cc")
            self.env_info.CXX = os.path.join(bin_folder, "mycompiler-cxx")
            self.env_info.SYSROOT = self.package_folder


With this approach we also need to add the path to the binaries to the ``PATH`` environment variable. The
one and only profile has to include a ``[build_requires]`` section with the reference to our new packaged toolchain and
it will also contain a ``[settings]`` section with the regular settings plus the ``os_build`` and ``arch_build`` ones.

This approach requires a special profile, and it needs a modified recipe without the ``compiler`` and ``build_type`` settings,
Conan can still compile it from sources but it won't be able to identify the binary properly and it can be really to tackle
if the build requirements has other Conan dependencies.


Settings ``*_build`` and ``*_target``
+++++++++++++++++++++++++++++++++++++

.. warning::

    **These settings are being reviewed and might be deprecated in the future**, we encourage you to try not to use
    them. If you need help with your use case, please `open an issue in the Conan repository <https://github.com/conan-io/conan/issues>`_
    and we will help you.


Before Conan v1.24 the recommended way to deal with cross building was to use some extra settings like
``os_build``, ``arch_build`` and ``os_target`` and ``arch_target``. These settings have a special meaning
for some Conan tools and build helpers, but they also need to be listed in the recipes themselves creating
a dedicated set of recipes for *installers* and *tools* in general. This approach should be superseeded with
the introduction in Conan 1.24 of the command line arguments ``--profile:host`` and ``--profile:build``
that allow to declare two different profiles with all the information needed for the corresponding platforms.

The meaning of those settings is the following:

* The settings ``os_build`` and ``arch_build`` identify the ``build`` platform according to the GNU convention
  triplet. These settings are detected the first time you run Conan with the same values than the ``host`` settings,
  so by default, we are doing **native building**. You will probably never need to change the value
  of this setting because they describe where are you running Conan.
* The settings ``os_target`` and ``arch_target`` identify the ``target`` platform. If you are building
  a cross compiler, these settings specify where the compiled code will run.

The rest of settings, as we already know, identify the ``host`` platform.


Preparing recipes to be cross-compiled
++++++++++++++++++++++++++++++++++++++

If you use the build helpers :ref:`AutoToolsBuildEnvironment<autotools_reference>` or :ref:`CMake<cmake_reference>`
together with ``os_build`` and ``arch_build`` settings, Conan will adjust the configuration accordingly to the specified settings.

If not, you can always check the regular settings ``os``, ``arch``,... (matching the ``host`` platform) and
inject the needed flags to your build system script.

Also, you can use this tool to check if you are cross-building:

- :ref:`tools.cross_building(self.settings)<cross_building_reference>` (returns True or False)


.. note::

    In the following releases, this build helpers and tools will take into account the values of the
    command line arguments ``--profile:host`` and ``--profile:build`` to implement the proper
    cross building behavior.


ARM architecture reference
--------------------------

Remember that the Conan settings are intended to unify the different names for operating systems, compilers,
architectures etc.

Conan has different architecture settings for ARM: ``armv6``, ``armv7``, ``armv7hf``, ``armv8``.
The "problem" with ARM architecture is that it's frequently named in different ways, so maybe you are wondering what setting
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


Examples
--------


.. _cross_building_examples_profiles:

Examples using profiles
+++++++++++++++++++++++

Linux to Windows
................

- Install the needed toolchain, in Ubuntu:

  .. code-block:: bash

      sudo apt-get install g++-mingw-w64 gcc-mingw-w64


- Create a file named **linux_to_win64** with the contents:

  .. code-block:: text

      toolchain=/usr/x86_64-w64-mingw32 # Adjust this path
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
      # We are cross-building to Windows
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

Windows to Raspberry Pi (Linux/ARM)
...................................

- Install the toolchain: https://gnutoolchains.com/raspberry/
  You can choose different versions of the GCC cross compiler. Choose one and adjust the following
  settings in the profile accordingly.

- Create a file named **win_to_rpi** with the contents:

  .. code-block:: text

      target_host=arm-linux-gnueabihf
      standalone_toolchain=C:/sysgcc/raspberry
      cc_compiler=gcc
      cxx_compiler=g++

      [settings]
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

The profiles to target Linux are all very similar. You probably just need to adjust the variables
declared at the top of the profile:

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

.. _cross_building_windows_ce:

Windows to Windows CE
.....................
The Windows CE (WinCE) operating system is supported for CMake and MSBuild. Since WinCE depends on the
MSVC compiler, Visual Studio and the according Windows CE platform SDK for the WinCE device have to be installed
on the build host.

The ``os.platform`` defines the WinCE Platform SDK and is equal to the ``Platform`` in Visual Studio.

Some examples for Windows CE platforms:

- ``SDK_AM335X_SK_WEC2013_V310``
- ``STANDARDSDK_500 (ARMV4I)``
- ``Windows Mobile 5.0 Pocket PC SDK (ARMV4I)``
- ``Toradex_CE800 (ARMV7)``

The ``os.version`` defines the WinCE version and must be ``"5.0"``, ``"6.0"`` or ``"7.0"``.

CMake supports Visual Studio 2008 (``compiler.version=9``) and Visual Studio 2012 (``compiler.version=11``).

Example of an Windows CE conan profile:

.. code-block:: text

    [settings]
    os=WindowsCE
    os.version=8.0
    os.platform=Toradex_CE800 (ARMV7)
    arch=armv7
    compiler=Visual Studio
    compiler.version=11

    # Release configuration
    build_type=Release
    compiler.runtime=MD

.. note::

    Further information about CMake and WinCE can be found in the CMake documentation:

    `CMake - Cross Compiling for Windows CE
    <https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html#cross-compiling-for-windows-ce>`_

.. _cross_building_android:

Linux/Windows/macOS to Android
..............................

Cross-building a library for Android is very similar to the previous examples, except the complexity of managing different
architectures (armeabi, armeabi-v7a, x86, arm64-v8a) and the Android API levels.

Download the Android NDK `here <https://developer.android.com/ndk/downloads>`_ and unzip it.

.. note::

    If you are in Windows the process will be almost the same, but unzip the file in the root folder of your hard disk (``C:\``) to avoid issues with path lengths.

Now you have to build a `standalone toolchain <https://developer.android.com/ndk/guides/standalone_toolchain>`_.
We are going to target the "arm" architecture and the Android API level 21. Change the ``--install-dir`` to any other place that works
for you:

.. code-block:: bash

   $ cd build/tools
   $ python make_standalone_toolchain.py --arch=arm --api=21 --stl=libc++ --install-dir=/myfolder/arm_21_toolchain


.. note::

    You can generate the standalone toolchain with several different options to target different architectures, API levels etc.

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

    $ cd conan-zlib && conan create . --profile=../android_21_arm_clang

    ...
    -- Build files have been written to: /tmp/conan-zlib/test_package/build/ba0b9dbae0576b9a23ce7005180b00e4fdef1198
    Scanning dependencies of target enough
    [ 50%] Building C object CMakeFiles/enough.dir/enough.c.o
    [100%] Linking C executable bin/enough
    [100%] Built target enough
    zlib/1.2.11 (test package): Running test()

A **bin/enough** for Android ARM platform has been built.


.. _cross_building_examples_build_requires:

Examples using build requires
+++++++++++++++++++++++++++++

.. _darwin_toolchain:

Example: Darwin Toolchain
.........................

Check the `Darwin Toolchain <https://github.com/theodelrieu/conan-darwin-toolchain>`_  package in conan-center.
You can use a profile like the following to cross-build your packages for ``iOS``,  ``watchOS`` and ``tvOS``:

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




---


.. seealso:: Reference links

    **ARM**

    - https://developer.arm.com/docs/dui0773/latest/compiling-c-and-c-code/specifying-a-target-architecture-processor-and-instruction-set
    - https://developer.arm.com/docs/dui0472/latest/compiler-command-line-options

    **ANDROID**

    - https://developer.android.com/ndk/guides/standalone_toolchain

    **VISUAL STUDIO**

    - https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild-command-line-reference?view=vs-2017


.. seealso::

    - See :ref:`conan.conf file<conan_conf>` and :ref:`Environment variables <env_vars>` sections to know more.
    - See :ref:`AutoToolsBuildEnvironment build helper<autotools_reference>` reference.
    - See :ref:`CMake build helper<cmake_reference>` reference.
    - See `CMake cross-building wiki <https://vtk.org/Wiki/CMake_Cross_Compiling>`_ to know more about cross-building with CMake.
