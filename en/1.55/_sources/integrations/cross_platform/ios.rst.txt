.. _iOS:

iOS, tvOS, watchOS
____________________________

.. _darwin_toolchain:

Using Darwin toolchain package (tool require)
=============================================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

One example of a tool requires implementing a toolchain to cross-compile to iOS, tvOS or watchOS, is
the `Darwin Toolchain <https://github.com/theodelrieu/conan-darwin-toolchain>`_  package. Although
this package is not in Conan Center Index you can check it to see an example of how to use a
toolchain for cross-compilation by using a tool requires. You can use a profile like the following
to cross-build your packages for ``iOS``,  ``watchOS`` and ``tvOS``:

.. code-block:: text
    :caption: ios_profile

    include(default)

    [settings]
    os=iOS
    os.version=9.0
    arch=armv7

    [tool_requires]
    darwin-toolchain/1.0@theodelrieu/stable


.. code-block:: bash

    $ conan install . --profile ios_profile

.. _conan-cmake-toolchain-ios:

Use built-in Conan toolchain
============================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

Conan will generate a toolchain for iOS if the recipe is using a :ref:`conan-cmake-toolchain`. This
toolchain provides a minimal implementation supporting only the CMake XCode generator. It will be
extended in the future but at the current version (1.31.0) is just for testing purpouses.

For using it, create a regular profile for the *host* context:

.. code-block:: ini
   :caption: **profile_host_ios**

   [settings]
    os=iOS
    os.version=12.0
    arch=armv8
    compiler=apple-clang
    compiler.version=12.0
    compiler.libcxx=libc++
    build_type=Release

Together with the files created by the generators that make it possible to find and link the
requirements, :command:`conan install` command will generate a toolchain file like the following one:

.. code-block:: cmake
   :caption: **conan_toolchain.cmake** (some parts are stripped)

    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)

    # set cmake vars
    set(CMAKE_SYSTEM_NAME iOS)
    set(CMAKE_SYSTEM_VERSION 12.0)
    set(DEPLOYMENT_TARGET ${CONAN_SETTINGS_HOST_MIN_OS_VERSION})
    # Set the architectures for which to build.
    set(CMAKE_OSX_ARCHITECTURES arm64)
    # Setting CMAKE_OSX_SYSROOT SDK, when using Xcode generator the name is enough
    # but full path is necessary for others
    set(CMAKE_OSX_SYSROOT iphoneos)

    


With this toolchain file you can execute CMake's command to generate the binaries:

.. code-block:: bash

   conan install <conanfile> --profile:host=profile_host_ios --profile:build=default
   cmake . -GXcode -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
   cmake --build . --config Release