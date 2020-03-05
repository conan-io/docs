.. _android:

|android_logo| Android
____________________________

There are several ways to cross-compile packages for `Android <https://www.android.com/>`__ platform via conan.

Using android_ndk_installer package (build require)
=========================================================

The easiest way so far is to use `android_ndk_installer <https://github.com/bincrafters/conan-android_ndk_installer>`_ conan package (which is in ``conan-center`` repository).

Using the ``android_ndk_installer`` package as a build requirement will do the following steps:

- Download the appropriate `Android NDK <https://developer.android.com/ndk>`_ archive.

- Set up required environment variables, such as ``CC``, ``CXX``, ``RANLIB`` and so on to the appropriate tools from the NDK.

- In case of using CMake, it will inject the appropriate `toolchain file <https://developer.android.com/ndk/guides/cmake#the_cmake_toolchain_file>`_ and set up the necessary CMake `variables <https://developer.android.com/ndk/guides/cmake#variables>`_.

For instance, in order to cross-compile for ``ARMv8``, the following conan profile might be used:

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
  [build_requires]
  android_ndk_installer/r20@bincrafters/stable
  [options]
  [env]

.. note:: 

   In addition to the above, Windows users may need to specify ``CONAN_MAKE_PROGRAM``,
   for instance from the existing MinGW installation (e.g. ``C:\MinGW\bin\mingw32-make.exe``), or use make from the ``mingw_installer/1.0@conan/stable``.

Similar profile might be used to cross-compile for ``ARMv7`` (notice the ``arch`` change):

.. code-block:: text

  include(default)
  [settings]
  arch=armv7
  build_type=Release
  compiler=clang
  compiler.libcxx=libc++
  compiler.version=8
  os=Android
  os.api_level=21
  [build_requires]
  android_ndk_installer/r20@bincrafters/stable
  [options]
  [env]

By adjusting ``arch`` setting, you may cross-compile for ``x86`` and ``x86_64`` Android as well (e.g. if you need to run code in a simulator).

.. note:: 

  ``os.api_level`` is an important setting which affects compatibility - it defines the **minimum** Android version supported.
  In other words, it is the same meaning as `minSdkVersion <https://developer.android.com/guide/topics/manifest/uses-sdk-element>`_.

Using Docker images
===================

If you're using `Docker <https://www.docker.com/>`_ for builds, you may consider using docker images from the
`Conan Docker Tools <https://github.com/conan-io/conan-docker-tools>`_ repository.

Currently, Conan Docker Tools provide the following Android images:

- conanio/android-clang8
- conanio/android-clang8-x86
- conanio/android-clang8-armv7
- conanio/android-clang8-armv8

All above mentioned images have corresponding `Android NDK <https://developer.android.com/ndk>`_ installed, with required environment variables 
set and with default conan profile configured for android cross-building. Therefore, these images might be especially useful for CI systems.

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
  [build_requires]
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

This is the official way recommended by Android developers.

For this, you will need a small CMake toolchain file:

.. code-block:: text

  set(ANDROID_PLATFORM 21)
  set(ANDROID_ABI arm64-v8a)
  include($ENV{HOME}/Library/Android/sdk/ndk/20.0.5594570/build/cmake/android.toolchain.cmake)

This toolchain file only sets up the required CMake `variables <https://developer.android.com/ndk/guides/cmake#variables>`_,
and then includes the default `toolchain file <https://developer.android.com/ndk/guides/cmake#the_cmake_toolchain_file>`_ supplied with Android NDK.

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
  [build_requires]
  [options]
  [env]
  CONAN_CMAKE_TOOLCHAIN_FILE=/home/conan/my_android_toolchain.cmake

In the profile, ``CONAN_CMAKE_TOOLCHAIN_FILE`` points to the CMake toolchain file listed above.


Using CMake build-in Android NDK support
----------------------------------------

.. warning::

    This workflow is not supported by Android and is often broken with new NDK releases or when using older versions of CMake.
    This workflow is **strongly discouraged** and will not work with Gradle.

For this approach, you don't need to specify CMake toolchain file at all. It's enough to indicate ``os`` is Android
and Conan will automatically set up all required CMake
`variables <https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html#cross-compiling-for-android>`__ for you.

Therefore, the following conan profile could be used for ``ARMv8``:

.. code-block:: text

  include(default)
  [settings]
  arch=armv8
  build_type=Release
  compiler=clang
  compiler.libcxx=libc++
  compiler.version=7.0
  os=Android
  os.api_level=21
  [build_requires]
  [options]
  [env]
  ANDROID_NDK_ROOT=/home/conan/android-ndk-r18b

The only way you have to configure is ``ANDROID_NDK_ROOT`` which is a path to the Android NDK installation.

Once profile is configured, you should see the following output during the CMake build:

.. code-block:: text

  -- Android: Targeting API '21' with architecture 'arm64', ABI 'arm64-v8a', and processor 'aarch64'
  -- Android: Selected Clang toolchain 'aarch64-linux-android-clang' with GCC toolchain 'aarch64-linux-android-4.9'

It means native CMake integration has successfully found Android NDK and configured the build.

.. |android_logo| image:: ../../images/android_logo.png
                  :width: 180px
