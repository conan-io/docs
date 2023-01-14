.. _android:

|android_logo| Android
____________________________

There are several ways to cross-compile packages for `Android <https://www.android.com>`__ platform via conan.

.. warning::

    Always use :ref:`build context <build_requires_context>` when cross building.

Using android-ndk package (tool require)
========================================

The easiest way so far is to use `android-ndk <https://conan.io/center/android-ndk>`_ conan package (which is in ``conancenter`` repository).

Using the ``android-ndk`` package as a tool requirement will do the following steps:

- Download the appropriate `Android NDK <https://developer.android.com/ndk>`_ archive.

- Set up required environment variables, such as ``CC``, ``CXX``, ``RANLIB`` and so on to the appropriate tools from the NDK.

- In case of using CMake, it will inject the appropriate `toolchain file <https://developer.android.com/ndk/guides/cmake#file>`_ and set up the necessary CMake `variables <https://developer.android.com/ndk/guides/cmake#variables>`_.

For instance, in order to cross-compile for ``ARMv8``, the following conan profile might be used:

.. code-block:: ini

  include(default)
  [settings]
  arch=armv8
  build_type=Release
  compiler=clang
  compiler.libcxx=libc++
  compiler.version=14
  os=Android
  os.api_level=21
  [tool_requires]
  android-ndk/r25
  [options]
  [env]

.. note::

   In addition to the above, Windows users may need to specify ``CONAN_MAKE_PROGRAM``,
   for instance from the existing MinGW installation (e.g. ``C:\MinGW\bin\mingw32-make.exe``), or use make from the ``mingw_installer/1.0@conan/stable``.

Similar profile might be used to cross-compile for ``ARMv7`` (notice the ``arch`` change):

.. code-block:: ini

  include(default)
  [settings]
  arch=armv7
  build_type=Release
  compiler=clang
  compiler.libcxx=libc++
  compiler.version=14
  os=Android
  os.api_level=21
  [tool_requires]
  android-ndk/r25
  [options]
  [env]

By adjusting ``arch`` setting, you may cross-compile for ``x86`` and ``x86_64`` Android as well (e.g. if you need to run code in a simulator).

.. note::

  ``os.api_level`` is an important setting which affects compatibility - it defines the **minimum** Android version supported.
  In other words, it is the same meaning as `minSdkVersion <https://developer.android.com/guide/topics/manifest/uses-sdk-element>`_.

Also, do not forget to use build context when cross building to Android:

.. code-block:: bash

  conan install conanfile.txt -pr:b=default -pr:h=android

Where ``android`` is one of the profiles listed above.

.. _conan-cmake-toolchain-android:

Use built-in Conan toolchain
============================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

Conan will generate a toolchain for Android if the recipe is using a :ref:`conan-cmake-toolchain`. In
that case all you need is to provide the path to the Android NDK and :ref:`working profiles <build_requires_context>`.
This approach can also use the Android NDK package referenced in the previous section.

Use a regular profile for the *host* context:

.. code-block:: ini
   :caption: **profile_host**

   [settings]
   os=Android
   os.api_level=23
   arch=x86_64
   compiler=clang
   compiler.version=14
   compiler.libcxx=c++_shared
   build_type=Release

   [conf]
   tools.android:ndk_path=<path/to/myandroid/ndk>


Together with the files created by the generators that make it possible to find and link the
requirements, :command:`conan install` command will generate a toolchain file like the following one:

.. code-block:: cmake
   :caption: **conan_toolchain.cmake** (some parts are stripped)

    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)

    set(CMAKE_SYSTEM_NAME Android)
    set(CMAKE_SYSTEM_VERSION 23)
    set(CMAKE_ANDROID_ARCH_ABI x86_64)
    set(CMAKE_ANDROID_STL_TYPE c++_shared)
    set(CMAKE_ANDROID_NDK <path/to/myandroid/ndk>)


With this toolchain file you can execute CMake's command to generate the binaries:

.. code-block:: bash

   conan install <conanfile> --profile:host=profile_host --profile:build=default
   cd build/Release
   cmake ../.. -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
   cmake --build .


Using Docker images
===================

If you're using `Docker <https://www.docker.com>`_ for builds, you may consider using docker images from the
`Conan Docker Tools <https://github.com/conan-io/conan-docker-tools>`_ repository.

Currently, Conan Docker Tools provide the following Android images:

- conanio/android-clang14
- conanio/android-clang14-x86
- conanio/android-clang14-armv7
- conanio/android-clang14-armv8

All above mentioned images have corresponding `Android NDK <https://developer.android.com/ndk>`_ installed as Conan package.
For more information how to build Android docker images, visit `Docker build section <https://github.com/conan-io/conan-docker-tools#build-test-and-deploy>`_.
Once you have a docker image installed property, you can run directly on your machine and cross-compile to Android:

.. code-block:: bash

  % docker run --rm -ti -v${PWD}:/home/conan/project conanio/android-clang14-armv8
  # running into docker container
  $ conan install project/conanfile.txt -pr:b=default -pr:h=android --build

.. note::

  If you are running on Mac M1, you need to pass ``--platform=linux/amd64`` as command argument to :command:`docker run`.

Using existing NDK
==================

It's also possible to use an existing `Android NDK <https://developer.android.com/ndk>`_ installation with conan.
For instance, if you're using `Android Studio <https://developer.android.com/studio/>`_ IDE, you may already have an NDK at ``~/Library/Android/sdk/ndk``.

You have to specify different environment variables in the Conan profile for make-based projects. For instance:

.. code-block:: text

  include(default)
  target_host=aarch64-linux-android
  android_ndk=/home/conan/Library/Android/sdk/ndk/20.0.5594570
  api_level=21
  [settings]
  arch=armv8
  build_type=Release
  compiler=clang
  compiler.libcxx=libc++
  compiler.version=8
  os=Android
  os.api_level=$api_level
  [tool_requires]
  [options]
  [env]
  PATH=[$android_ndk/toolchains/llvm/prebuilt/darwin-x86_64/bin]
  CHOST=$target_host
  AR=$target_host-ar
  AS=$target_host-as
  RANLIB=$target_host-ranlib
  CC=$target_host$api_level-clang
  CXX=$target_host$api_level-clang++
  LD=$target_host-ld
  STRIP=$target_host-strip

However, when building CMake projects, there are several approaches available, and it's not always clear which one to follow.

Using toolchain from Android NDK
--------------------------------

.. warning::

   This method is deprecated. Use the one above using ``CMakeToolchain``, the generated ``conan_toolchain.cmake``
   and the conf ``tools.android:ndk_path=<path/to/myandroid/ndk>``


For this, you will need a small CMake toolchain file:

.. code-block:: text

  set(ANDROID_PLATFORM 21)
  set(ANDROID_ABI arm64-v8a)
  include($ENV{HOME}/Library/Android/sdk/ndk/20.0.5594570/build/cmake/android.toolchain.cmake)

This toolchain file only sets up the required CMake `variables <https://developer.android.com/ndk/guides/cmake#variables>`_,
and then includes the default `toolchain file <https://developer.android.com/ndk/guides/cmake#file>`_ supplied with Android NDK.

And then, you may use the following profile:

.. code-block:: text

  include(default)
  [settings]
  arch=armv8
  build_type=Release
  compiler=clang
  compiler.libcxx=libc++
  compiler.version=8
  os=Android
  os.api_level=21
  [tool_requires]
  [options]
  [env]
  CONAN_CMAKE_TOOLCHAIN_FILE=/home/conan/my_android_toolchain.cmake

In the profile, ``CONAN_CMAKE_TOOLCHAIN_FILE`` points to the CMake toolchain file listed above.


.. |android_logo| image:: ../../images/android_logo.png
                  :width: 180px
