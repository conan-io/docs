.. _example_cross_build_linux_to_windows_mingw:


Cross-compiling from Linux to Windows with MinGW
================================================

It is possible to cross-build from Linux to Windows using the MinGW cross-compiler.
Note that such a compiler won't be using the MSVC runtime, but the MinGW one, which
uses the ``libstdc++6.dll`` runtime.

This `blog post about Clang in Windows <https://blog.conan.io/2022/10/13/Different-flavors-Clang-compiler-Windows.html>`_
describes the different runtimes for the different Windows subsystems, which is equally applicable to MinGW.

The first step would be to install the compiler. In Debian based systems:

.. code-block:: bash

    $ sudo apt install gcc-mingw-w64-x86-64-posix
    $ sudo apt install g++-mingw-w64-x86-64-posix

If the compiler is installed in the system path, then we could write a profile like:

.. code-block:: text
    :caption: mingw

    [settings]
    os=Windows
    compiler=gcc
    compiler.version=10
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    arch=x86_64
    build_type=Release

    [buildenv]
    CC=x86_64-w64-mingw32-gcc-posix
    CXX=x86_64-w64-mingw32-g++-posix


Then, let's say that we have a basic CMake project, which we can create with the ``conan new``:

.. code-block:: bash

    $ conan new cmake_lib -d name=mypkg -d version=0.1
    $ conan create . -pr=mingw

    ...
    -- Using Conan toolchain: .../conan_toolchain.cmake
    -- Conan toolchain: Defining architecture flag: -m64
    -- Conan toolchain: C++ Standard 17 with extensions ON
    -- The CXX compiler identification is GNU 10.0.0
    -- Check for working CXX compiler: /usr/bin/x86_64-w64-mingw32-g++-posix - skipped

    mypkg/0.1 (test package): Running CMake.build()
    mypkg/0.1 (test package): RUN: cmake --build ...
    gcc-10-x86_64-gnu17-release" -- -j8
    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.obj
    [100%] Linking CXX executable example.exe
    [100%] Built target example

The example.exe will not be executed in the Linux machine, because the ``test_package`` contains 
a ``if can_run(self)`` branch to not run it in cross-build scenarios.

We can now take the ``example.exe`` and run it in a Windows machine:

.. code-block:: bash

  mypkg/0.1: Hello World Release!
  mypkg/0.1: _M_X64 defined
  mypkg/0.1: __x86_64__ defined
  mypkg/0.1: _GLIBCXX_USE_CXX11_ABI 1
  mypkg/0.1: MSVC runtime: MultiThreadedDLL
  mypkg/0.1: __cplusplus201402
  mypkg/0.1: __GNUC__10
  mypkg/0.1: __MINGW32__1
  mypkg/0.1: __MINGW64__1


.. note::

    - It is very possible that some recipes in ConanCenter are not prepared to be cross-built from Linux
      to Windows. The recommended way to build ConanCenter recipes is to build them with MSVC in
      Windows, as there might be limitations for the specific build-systems of the recipes, and MinGW
      support is not guaranteed.
    - Trying to run the executables with some emulators like ``wine`` might require extra effort, because
      the runtime environment is intended to be Windows, and as such a ``conanrun.bat`` environment file
      will be created, but that cannot be executed in Linux. Using configurations like ``-c tools.build.cross_building:can_run=True -c tools.microsoft.bash:subsystem=mingw -c tools.microsoft.bash:active=True``
      can allow to force the generation and execution of ``conanrun.sh``.
