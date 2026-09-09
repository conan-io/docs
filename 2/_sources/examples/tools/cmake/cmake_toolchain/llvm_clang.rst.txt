.. _examples-tools-cmake-toolchain-llvm-clang:

CMakeToolchain: Using LLVM/Clang Windows compiler
=================================================

The Clang compiler in Windows can come from 2 different installations or distributions:

- The LLVM/Clang compiler, that uses the MSVC runtime
- The Msys2 Clang compiler that uses the Msys2 runtime (libstdc++6.dll)

This example explains the LLVM/Clang with the MSVC runtime. This Clang distribution can in turn
be used in three different ways:

- Using the Clang component installed by Visual Studio installer as part of VS
- Using the LLVM/Clang downloaded compiler (it still uses the MSVC runtime), via the GNU-like frontend ``clang``
- Using the LLVM/Clang downloaded compiler (it still uses the MSVC runtime), via the MSVC-like frontend ``clang-cl``


Let's start from a simple ``cmake_exe`` template:

.. code-block:: bash

    $ conan new cmake_exe -d name=mypkg -d version=0.1

This creates a simple CMake based project and Conan package recipe that uses ``CMakeToolchain``.


LLVM/Clang with ``clang`` GNU-like frontend
-------------------------------------------

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
    PATH=+(path)C:/ws/LLVM/18.1/bin

    [conf]
    tools.cmake.cmaketoolchain:generator=Ninja
    tools.compilation:verbosity=verbose

    [tool_requires]
    ninja/[*]

Quick explanation of the profile:

- The ``compiler.runtime`` definition is the important differentiator to distinguish between Msys2-Clang and LLVM/Clang
  with the MSVC runtime. The LLVM/Clang defines this ``compiler.runtime``, while the Msys2-Clang doesn't.
- The MSVC runtime can be either dynamic or static. It is important also to define the runtime version (toolset version ``v144``)
  of this runtime, as it is possible to use different ones.
- The ``[buildenv]`` allows to point to the LLVM/Clang compiler, in case it is not already in the path. **Note** the ``PATH=+(path)``
  syntax, to **prepend** that path, so it has higher priority, otherwise it is possible that CMake would find and use the Clang
  component installed inside Visual Studio.
- We are using the ``Ninja`` CMake generator, and installing it from a ``[tool_requires]``, but this might not be necessary if Ninja
  is installed in your system.


Let's build it:

.. code-block:: bash

    $ conan build . -pr=llvm_clang
    ...
    -- The CXX compiler identification is Clang 18.1.8 with GNU-like command-line
    -- Check for working CXX compiler: C:/ws/LLVM/18.1/bin/clang++.exe - skipped
    ...
    [1/3] C:\ws\LLVM\18.1\bin\clang++.exe   -O3 -DNDEBUG -std=c++14 -D_DLL -D_MT -Xclang --dependent-lib=msvcrt -MD -MT CMakeFiles/mypkg.dir/src/main.cpp.obj -MF CMakeFiles\mypkg.dir\src\main.cpp.obj.d -o CMakeFiles/mypkg.dir/src/main.cpp.obj -c C:/Users/Diego/conanws/kk/clang/src/main.cpp
    [2/3] C:\ws\LLVM\18.1\bin\clang++.exe   -O3 -DNDEBUG -std=c++14 -D_DLL -D_MT -Xclang --dependent-lib=msvcrt -MD -MT CMakeFiles/mypkg.dir/src/mypkg.cpp.obj -MF CMakeFiles\mypkg.dir\src\mypkg.cpp.obj.d -o CMakeFiles/mypkg.dir/src/mypkg.cpp.obj -c C:/Users/Diego/conanws/kk/clang/src/mypkg.cpp
    [3/3] cmd.exe /C "cd . && C:\ws\LLVM\18.1\bin\clang++.exe -fuse-ld=lld-link -nostartfiles -nostdlib -O3 -DNDEBUG -D_DLL -D_MT -Xclang --dependent-lib=msvcrt -Xlinker /subsystem:console CMakeFiles/mypkg.dir/src/mypkg.cpp.obj CMakeFiles/mypkg.dir/src/main.cpp.obj -o mypkg.exe -Xlinker /MANIFEST:EMBED -Xlinker /implib:mypkg.lib -Xlinker /pdb:mypkg.pdb -Xlinker /version:0.0   -lkernel32 -luser32 -lgdi32 -lwinspool -lshell32 -lole32 -loleaut32 -luuid -lcomdlg32 -ladvapi32 -loldnames  && cd ."


See how the desired LLVM/Clang compiler installed in the ``C:/ws`` folder is used, and how the ``GNU-like`` command line syntax is used.
The GNU-like syntax requires the ``--dependent-lib=msvcrt`` (added automatically by CMake) compiler and linker flags to define linking against the dynamic MSVC runtime, as otherwise LLVM/Clang link it statically. Also note that the ``-MD -MT`` flags are not related to the <MSVC runtime, in the GNU-like frontend, they have a completely different meaning.

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


LLVM/Clang with ``clang-cl`` MSVC-like frontend
-----------------------------------------------

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
    tools.cmake.cmaketoolchain:generator=Ninja
    tools.build:compiler_executables = {"c": "clang-cl", "cpp": "clang-cl"}
    tools.compilation:verbosity=verbose

    [tool_requires]
    ninja/[*]


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
    -- The CXX compiler identification is Clang 18.1.8 with MSVC-like command-line
    -- Check for working CXX compiler: C:/ws/LLVM/18.1/bin/clang-cl.exe - skipped
    ...
    [1/3] C:\ws\LLVM\18.1\bin\clang-cl.exe  /nologo -TP   /DWIN32 /D_WINDOWS /GR /EHsc /O2 /Ob2 /DNDEBUG -std:c++14 -MD /showIncludes /FoCMakeFiles\mypkg.dir\src\main.cpp.obj /FdCMakeFiles\mypkg.dir\ -c -- C:\project\src\main.cpp
    [2/3] C:\ws\LLVM\18.1\bin\clang-cl.exe  /nologo -TP   /DWIN32 /D_WINDOWS /GR /EHsc /O2 /Ob2 /DNDEBUG -std:c++14 -MD /showIncludes /FoCMakeFiles\mypkg.dir\src\mypkg.cpp.obj /FdCMakeFiles\mypkg.dir\ -c -- C:\project\src\mypkg.cpp
    [3/3] cmd.exe /C "cd . && C:\ws\cmake\cmake-3.27.9-windows-x86_64\bin\cmake.exe -E vs_link_exe --intdir=CMakeFiles\mypkg.dir --rc=C:\PROGRA~2\WI3CF2~1\10\bin\100226~1.0\x64\rc.exe --mt=C:\PROGRA~2\WI3CF2~1\10\bin\100226~1.0\x64\mt.exe --manifests  -- C:\ws\LLVM\18.1\bin\lld-link.exe /nologo CMakeFiles\mypkg.dir\src\mypkg.cpp.obj CMakeFiles\mypkg.dir\src\main.cpp.obj  /out:mypkg.exe /implib:mypkg.lib /pdb:mypkg.pdb /version:0.0 /machine:x64 /INCREMENTAL:NO /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."

See how the desired LLVM/Clang compiler installed in the ``C:/ws`` folder is used, and how the ``MSVC-like`` command line syntax is used.
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


MSVC Clang component (ClangCL Visual Studio toolset)
----------------------------------------------------

To build this configuration we will use the following profile:

.. code-block:: ini
    :caption: llvm_clang_vs

    [settings]
    os=Windows
    arch=x86_64
    build_type=Release
    compiler=clang
    compiler.version=19
    compiler.cppstd=14
    compiler.runtime=dynamic
    compiler.runtime_type=Release
    compiler.runtime_version=v144
    
    [conf]
    tools.cmake.cmaketoolchain:generator=Visual Studio 17
    tools.compilation:verbosity=verbose
    

This profile will use the CMake "Visual Studio" generator. This indicates that the Clang compiler will be the one
provided by Visual Studio, and installed as a component of Visual Studio via the Visual Studio installer. 
Note the ``compiler.version=19`` is a different version than the one used above, which was ``compiler.version=18``,
as the version inside Visual is defined automatically by its installer.

This setup will always use the MSVC-like ``clang-cl`` frontend, and the ``ClangCL`` toolset will be activated to
let Visual Studio that this is the compiler that it should use.
It is not necessary to define the ``tools.build:compiler_executable`` here.



Let's build it:

.. code-block:: bash

    $ conan build . -pr=llvm_clang_vs
    ...
    -- Conan toolchain: CMAKE_GENERATOR_TOOLSET=ClangCL
    -- The CXX compiler identification is Clang 19.1.1 with MSVC-like command-line
    ...
    ClCompile:
        C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\Llvm\x64\bin\clang-cl.exe /c /nologo /W1 /WX- /diagnostics:column /O2 /Ob2 /D _MBCS /D WIN
    32 /D _WINDOWS /D NDEBUG /D "CMAKE_INTDIR=\"Release\"" /EHsc /MD /GS /fp:precise /GR /std:c++14 /Fo"mypkg.dir\Release\\" /Gd /TP --target=amd64-pc-windows-
    msvc  C:\project\src\mypkg.cpp C:\project\src\main.cpp
    Link:
    C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\Llvm\x64\bin\lld-link.exe /OUT:"C:\project\build\Release\mypkg.exe" /
    INCREMENTAL:NO kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib /MANIFEST /MANIFESTUAC:
    "level='asInvoker' uiAccess='false'" /manifest:embed /PDB:"C:/Users/Diego/conanws/kk/clang/build/Release/mypkg.pdb" /SUBSYSTEM:CONSOLE /DYNAMICBASE /NXCOMP
    AT /IMPLIB:"C:/Users/Diego/conanws/kk/clang/build/Release/mypkg.lib"   /machine:x64 mypkg.dir\Release\mypkg.obj
    mypkg.dir\Release\main.obj
    mypkg.vcxproj -> C:\project\build\Release\mypkg.exe


The ``CMAKE_GENERATOR_TOOLSET=ClangCL`` is defined, and also the internal VS Clang component is used, and the ``19.1.1`` version is also displayed.
Then, the regular ``MSVC-like`` syntax, including the definition of the runtime via ``/MD`` flags is used.

We can run our executable, and see how the Clang compiler version (``19``) and the MSVC runtime match the defined ones:

.. code-block:: bash

    $ build\Release\mypkg.exe
    mypkg/0.1: Hello World Release!
        mypkg/0.1: _M_X64 defined
        mypkg/0.1: __x86_64__ defined
        mypkg/0.1: MSVC runtime: MultiThreadedDLL
        mypkg/0.1: _MSC_VER1943
        mypkg/0.1: _MSVC_LANG201402
        mypkg/0.1: __cplusplus201402
        mypkg/0.1: __clang_major__19
        mypkg/0.1: __clang_minor__1
