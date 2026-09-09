.. _examples_cross_build_android_ndk:


Cross building to Android with the NDK
======================================

In this example, we are going to see how to cross-build a Conan package to Android.

First of all, download the Android NDK from `the download page <https://developer.android.com/ndk/downloads>`_
and unzip it. In MacOS you can also install it with ``brew install android-ndk``.

Then go to the ``profiles`` folder in the conan config home directory (check it running :command:`conan config home`)
and create a file named ``android`` with the following contents:

.. code-block:: text

    include(default)

    [settings]
    os=Android
    os.api_level=21
    arch=armv8
    compiler=clang
    compiler.version=12
    compiler.libcxx=c++_static
    compiler.cppstd=14

    [conf]
    tools.android:ndk_path=/usr/local/share/android-ndk

You might need to modify:

- ``compiler.version``: Check the NDK documentation or find a ``bin`` folder containing the compiler executables like
  ``x86_64-linux-android31-clang``. In a Macos installation it is found in the NDK path + ``toolchains/llvm/prebuilt/darwin-x86_64/bin``.
  Run ``./x86_64-linux-android31-clang --version`` to check the running ``clang`` version and adjust the profile.
- ``compiler.libcxx``: The supported values are ``c++_static`` and ``c++_shared``.
- ``compiler.cppstd``: The C++ standard version, adjust as your needs.
- ``os.api_level``: You can check `here <https://apilevels.com/>`_ the usage of each Android Version/API level and choose
  the one that fits better with your requirements. This is typically a balance between new features and more compatible applications.
- ``arch``: There are several architectures supported by Android: ``x86``, ``x86_64``, ``armv7``, and ``armv8``.
- ``tools.android:ndk_path`` conf: Write the location of the unzipped NDK.


Use the :command:`conan new` command to create a "Hello World" C++ library example project:

.. code-block:: bash

    $ conan new cmake_lib -d name=hello -d version=1.0


Then we can specify the ``android`` profile and our hello library will be built for Android:

.. code-block:: bash

    $ conan create . --profile android

    [ 50%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [100%] Linking CXX static library libhello.a
    [100%] Built target hello
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example

Both the library and the ``test_package`` executable are built for Android, so we cannot use them in our local computer.

Unless you have access to a `root` Android device, running the test application or using the built library is not possible
directly so it is more common to build an Android application that uses the ``hello`` library.

Read more
---------

- Check the example :ref:`Integrating Conan in Android Studio<examples_cross_build_android_studio>` to know how to use your
  c++ libraries in a native Android application.
- Check the tutorial :ref:`How to cross-compile your applications using Conan<consuming_packages_cross_building_with_conan>`.