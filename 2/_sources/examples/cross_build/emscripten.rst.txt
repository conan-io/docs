.. _examples_cross_build_emscripten:

Cross-building with Emscripten - WebAssembly and asm.js
=======================================================

This example demonstrates how to cross-build a simple C++ project using Emscripten and Conan.

Conan supports `WASM <https://webassembly.org>`_ cross compilation, giving you the flexibility to target different
JavaScript/WebAssembly runtimes in the browser.

We recommend creating separate Conan profiles for each target. Below are
recommended profiles and instructions on how to build with them.


Setting up Conan profile for WebAssembly (WASM)
-----------------------------------------------

.. code-block:: text

   [settings]
   arch=wasm
   build_type=Release
   compiler=emcc
   compiler.cppstd=17
   compiler.libcxx=libc++
   # Optional settings to enable multithreading (see note below)
   # compiler.threads=posix
   compiler.version=4.0.10
   os=Emscripten

   [tool_requires]
   emsdk/4.0.10

   [conf]
   # Optional settings to enable memory allocation
   tools.build:exelinkflags=['-sALLOW_MEMORY_GROWTH=1', '-sMAXIMUM_MEMORY=4GB', '-sINITIAL_MEMORY=64MB']
   tools.build:sharedlinkflags=['-sALLOW_MEMORY_GROWTH=1', '-sMAXIMUM_MEMORY=4GB', '-sINITIAL_MEMORY=64MB']


.. note::
    
    Conan also supports building for `asm.js <http://asmjs.org>`_ targets, which is a nowadays considered deprecated.

    What’s the difference between asm.js and WASM?

    - **asm.js** is a subset of JavaScript optimized for speed. It is fully supported by all browsers (even older ones) and compiles to a large ``.js`` file.
    - **WebAssembly (WASM)** is a binary format that is smaller and faster to load and execute. Most modern browsers support it, and it is generally recommended for new projects. **WASM** is also easier to integrate with native browser APIs compared to **asm.js**.


Even though Emscripten is not a true runtime environment (like Linux or
Windows), it is part of a toolchain ecosystem that compiles C/C++ to
WebAssembly (WASM) and asm.js.

Conan uses ``os=Emscripten`` to:

- Align with the toolchain: Emscripten integrates the compiler, runtime glue, and JavaScript environment, making it practical to treat as an "OS-like" target.

- Support backward compatibility: Many recipes in Conan Center Index use ``os=Emscripten`` to enable or disable features and dependencies that specifically target Emscripten.

- Maintain stability: Changing this setting would break recipes that rely on it, and would complicate compatibility with alternative WASM toolchains.


.. note::

   ``wasm`` arch refers to ``WASM 32-bit`` target architecture, which is the
   default. If you wish to target ``WASM64``, set ``arch=wasm64`` in your profile.
   **Note that WASM64 is still experimental** and requires Node.js v20+ and a browser that supports it.

.. important::

    According to `emscripten documentation <https://emscripten.org/docs/api_reference/wasm_workers.html>`_ Emscripten supports two multithreading APIs:

    - POSIX Threads API (``posix`` in conan profile)
    - Wasm Workers API (``wasm_workers`` in conan profile)

    These two APIs are incompatible with each other and incompatibles with binaries compiled without threading support.
    This incompatibility necessitates the modeling of threading usage within
    the compiler's binary model, allowing conan to distinguish between binaries
    compiled with threading and those compiled without it.

    Conan will automatically set compiler and linker flags to enable threading if configured in the profile.


The profiles above use the ``emsdk`` package from `Conan Center Index repository <https://conan.io/center/recipes/emsdk>`_, which provides the Emscripten SDK, including ``emcc``, ``em++``, and tools like ``emrun`` and ``node``.

If you prefer to use your system-installed Emscripten instead of the Conan-provided one, ``tool_requires`` could be replaced by custom ``compiler_executables`` and ``buildenv``:

.. code-block:: text

  [conf]
  tools.build:compiler_executables={'c':'/path/to/emcc', 'cpp':'/path/to/em++'}

  [buildenv]
  CC=emcc
  CXX=em++
  AR=emar
  NM=emnm
  RANLIB=emranlib
  STRIP=emstrip


This way conan could configure `emsdk` local installation to be used from `CMake`, `Meson`, `Autotools` or other build systems.

In some cases, you might also need the ``Emscripten.cmake`` toolchain file
for advanced scenarios. This toolchais is already added in our packaged
`emsdk` but if you are using your own Emscripten installation, you can
specify it in the profile by using
:ref:`tools.cmake.cmaketoolchain:user_toolchain<conan_cmake_user_toolchain>`
and providing the absolute path to your toolchain file.

.. note::

   The ``tools.build:exelinkflags`` and ``tools.build:sharedlinkflags`` in
   previous profiles are recomendations but users can modify them or define
   their values in the CMakeLists.txt file using the
   ``set_target_properties()`` command.

   - By enabling ``ALLOW_MEMORY_GROWTH`` we allow the runtime to grow its
     memory dynamically at runtime by calling ``emscripten_resize_heap()``. Without
     this flag, memory is allocated at startup and cannot grow.

   - The ``MAXIMUM_MEMORY`` and ``INITIAL_MEMORY`` values specifies the maximum
     and initial memory size for the Emscripten runtime. These values can be
     adjusted based on your application's needs. 

     Take into account that ``arch=wasm64`` has a theorical exabytes maximum
     memory size, but runtime currently limits it to 16GB, while ``arch=wasm32``
     has a maximum memory size of 4GB and ``arch=asm.js`` has a maximum memory size of 2GB.
    

.. important::

   ``emcc`` compiler does not guarantee any ABI compatibility between different versions (patches included)
   To ensure a new ``package_id`` is generated when the Emscripten version
   changes, it is recommended to update the ``compiler.version`` setting in your profile accordingly.

   This will ensure that the package ID is generated based on the Emscripten
   version, allowing Conan to detect changes in the Emscripten toolchain and
   rebuild the project accordingly.
