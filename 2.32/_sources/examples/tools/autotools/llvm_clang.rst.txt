.. _examples-tools-autotools-llvm-clang:

AutoTools: Using LLVM/Clang Windows compiler
============================================

The Clang compiler in Windows can come from 2 different installations or distributions:

- The LLVM/Clang compiler, that uses the MSVC runtime
- The Msys2 Clang compiler that uses the Msys2 runtime (libstdc++6.dll)

This example explains the LLVM/Clang with the MSVC runtime. This Clang distribution can in turn
be used in two different ways:

- Using the LLVM/Clang downloaded compiler (it still uses the MSVC runtime), via the GNU-like frontend ``clang``
- Using the LLVM/Clang downloaded compiler (it still uses the MSVC runtime), via the MSVC-like frontend ``clang-cl``


Let's start from a simple ``autotools_exe`` template:

.. code-block:: bash

    $ conan new autotools_exe -d name=mypkg -d version=0.1

This creates a simple Autotools based project and Conan package recipe that uses ``AutotoolsToolchain``.


Autotools: LLVM/Clang with ``clang`` GNU-like frontend
------------------------------------------------------

To build this configuration we will use the following profile:

.. code-block:: ini
    :caption: llvm_clang

    [settings]
    os=Windows
    arch=x86_64
    build_type=Release
    compiler=clang
    compiler.version=18
    compiler.cppstd=14
    compiler.runtime=dynamic
    compiler.runtime_type=Release
    compiler.runtime_version=v144

    [buildenv]
    PATH=+(path)C:\ws\LLVM\18.1\bin

    [conf]
    tools.compilation:verbosity=verbose
    tools.build:compiler_executables = {"c": "clang", "cpp": "clang++"}
    tools.microsoft.bash:subsystem=msys2
    tools.microsoft.bash:path=C:\ws\msys64\usr\bin\bash.exe


Quick explanation of the profile:

- The ``compiler.runtime`` definition is the important differentiator to distinguish between Msys2-Clang and LLVM/Clang
  with the MSVC runtime. The LLVM/Clang defines this ``compiler.runtime``, while the Msys2-Clang doesn't.
- The MSVC runtime can be either dynamic or static. It is important also to define the runtime version (toolset version ``v144``)
  of this runtime, as it is possible to use different ones.
- The ``[buildenv]`` allows to point to the LLVM/Clang compiler, in case it is not already in the path. **Note** the ``PATH=+(path)``
  syntax, to **prepend** that path, so it has higher priority
- While defining ``tools.microsoft.bash:path``, the full path to the ``msys2`` ``bash.exe`` has been used. Otherwise, it is possible that
  it can find another ``bash.exe`` in the Windows system that will not be valid.


Let's build it:

.. code-block:: bash

    $ conan build . -pr=llvm_clang
    ...
    conanfile.py (mypkg/0.1): Calling build()
    conanfile.py (mypkg/0.1): RUN: autoreconf --force --install
    conanfile.py (mypkg/0.1): RUN: "/c/projectpath/clang/configure" --prefix=/ --bindir=${prefix}/bin --sbindir=${prefix}/bin --libdir=${prefix}/lib --includedir=${prefix}/include --oldincludedir=${prefix}/include
    conanfile.py (mypkg/0.1): RUN: make -j8
    ...
    clang++ -DPACKAGE_NAME=\"mypkg\" -DPACKAGE_TARNAME=\"mypkg\" -DPACKAGE_VERSION=\"0.1\" -DPACKAGE_STRING=\"mypkg\ 0.1\" -DPACKAGE_BUGREPORT=\"\" -DPACKAGE_URL=\"\" -DPACKAGE=\"mypkg\" -DVERSION=\"0.1\" -I. -I/c/projectpath/clang/src   -DNDEBUG  -std=c++14 -D_DLL -D_MT -Xclang --dependent-lib=msvcrt -O3 -c -o main.o /c/projectpath/clang/src/main.cpp
    source='/c/projectpath/clang/src/mypkg.cpp' object='mypkg.o' libtool=no \
    DEPDIR=.deps depmode=none /bin/sh /c/projectpath/clang/depcomp \
    clang++ -DPACKAGE_NAME=\"mypkg\" -DPACKAGE_TARNAME=\"mypkg\" -DPACKAGE_VERSION=\"0.1\" -DPACKAGE_STRING=\"mypkg\ 0.1\" -DPACKAGE_BUGREPORT=\"\" -DPACKAGE_URL=\"\" -DPACKAGE=\"mypkg\" -DVERSION=\"0.1\" -I. -I/c/projectpath/clang/src   -DNDEBUG  -std=c++14 -D_DLL -D_MT -Xclang --dependent-lib=msvcrt -O3 -c -o mypkg.o /c/projectpath/clang/src/mypkg.cpp
    clang++  -std=c++14 -D_DLL -D_MT -Xclang --dependent-lib=msvcrt -O3  -fuse-ld=lld-link -o mypkg.exe main.o mypkg.o

Note how the ``clang++`` compiler is used, the runtime is selected with ``-D_DLL -D_MT -Xclang --dependent-lib=msvcrt``.


We can run our executable, and see how the Clang compiler version and the MSVC runtime match the defined ones:

.. code-block:: bash

    $ build-release\src\mypkg.exe
    mypkg/0.1: Hello World Release!
        mypkg/0.1: _M_X64 defined
        mypkg/0.1: __x86_64__ defined
        mypkg/0.1: MSVC runtime: MultiThreadedDLL
        mypkg/0.1: _MSC_VER1943
        mypkg/0.1: _MSVC_LANG201402
        mypkg/0.1: __cplusplus201402
        mypkg/0.1: __clang_major__18
        mypkg/0.1: __clang_minor__1


Autotools: LLVM/Clang with ``clang-cl`` MSVC-like frontend
----------------------------------------------------------

To build this configuration we will use the following profile:

.. code-block:: ini
    :caption: llvm_clang_cl

    [settings]
    os=Windows
    arch=x86_64
    build_type=Release
    compiler=clang
    compiler.version=18
    compiler.cppstd=14
    compiler.runtime=dynamic
    compiler.runtime_type=Release
    compiler.runtime_version=v144

    [buildenv]
    PATH=+(path)C:/ws/LLVM/18.1/bin

    [conf]
    tools.compilation:verbosity=verbose
    tools.microsoft.bash:subsystem=msys2
    tools.build:compiler_executables = {"c": "clang-cl", "cpp": "clang-cl"}
    tools.microsoft.bash:path=C:\ws\msys64\usr\bin\bash.exe

The profile is almost identical to the above one, the main difference is the definition of ``tools.build:compiler_executables``,
defining the ``clang-cl`` compiler. 

.. note:: 

    The definition of ``tools.build:compiler_executables`` using the ``clang-cl`` compiler is what is used by Conan to differentiate
    among the frontends, also in other build systems. 
    This frontend is not a ``setting``, because the compiler is still the same, and the resulting binary should be binary compatible.


Let's build it:

.. code-block:: bash

    $ conan build . -pr=llvm_clang_cl
    ...
    clang-cl -DPACKAGE_NAME=\"mypkg\" -DPACKAGE_TARNAME=\"mypkg\" -DPACKAGE_VERSION=\"0.1\" -DPACKAGE_STRING=\"mypkg\ 0.1\" -DPACKAGE_BUGREPORT=\"\" -DPACKAGE_URL=\"\" -DPACKAGE=\"mypkg\" -DVERSION=\"0.1\" -I. -I/c/projectpath/clang/src   -DNDEBUG  -std:c++14 -MD -O2 -c -o main.obj `cygpath -w '/c/projectpath/clang/src/main.cpp'`
    source='/c/projectpath/clang/src/mypkg.cpp' object='mypkg.obj' libtool=no \
    DEPDIR=.deps depmode=msvc7msys /bin/sh /c/projectpath/clang/depcomp \
    clang-cl -DPACKAGE_NAME=\"mypkg\" -DPACKAGE_TARNAME=\"mypkg\" -DPACKAGE_VERSION=\"0.1\" -DPACKAGE_STRING=\"mypkg\ 0.1\" -DPACKAGE_BUGREPORT=\"\" -DPACKAGE_URL=\"\" -DPACKAGE=\"mypkg\" -DVERSION=\"0.1\" -I. -I/c/projectpath/clang/src   -DNDEBUG  -std:c++14 -MD -O2 -c -o mypkg.obj `cygpath -w '/c/projectpath/clang/src/mypkg.cpp'`
    clang-cl  -std:c++14 -MD -O2   -o mypkg.exe main.obj mypkg.obj
    ...


See how the desired ``clang-cl`` is used, and how the ``MSVC-like`` command line syntax is used, like ``-std:c++14``.
This MSVC-like syntax uses the ``-MD/-MT`` flags to differentiate across the dynamic/static MSVC runtimes.

We can run our executable, and see how the Clang compiler version and the MSVC runtime match the defined ones:

.. code-block:: bash

    $ build\Release\mypkg.exe
    mypkg/0.1: Hello World Release!
        mypkg/0.1: _M_X64 defined
        mypkg/0.1: __x86_64__ defined
        mypkg/0.1: MSVC runtime: MultiThreadedDLL
        mypkg/0.1: _MSC_VER1943
        mypkg/0.1: _MSVC_LANG201402
        mypkg/0.1: __cplusplus201402
        mypkg/0.1: __clang_major__18
        mypkg/0.1: __clang_minor__1

As expected, the output is identical to the previous one, as nothing changed except the compiler frontend.


.. note::

    It might be possible to build using the ``clang-cl`` distributed as a Visual Studio component for autotools-like projects.
    But it is necessary to provide the full path to that Clang component within the Visual Studio installed folder, so it can 
    be found, via ``[buildenv]`` and or ``tools.build:compiler_executables``, because it is basically an LLVM/Clang compiler,
    packaged and distributed by the Visual Studio installer.
