.. _examples_cross_build_emscripten:

Cross-building with Emscripten - WebAssembly and asm.js
=======================================================

This example demonstrates how to cross-build a simple C++ project using Emscripten and Conan.

Conan supports building for both `asm.js <http://asmjs.org>`_ and `WASM
<https://webassembly.org>`_, giving you the flexibility to target different
JavaScript/WebAssembly runtimes in the browser.

We recommend creating separate Conan profiles for each target. Below are
recommended profiles and instructions on how to build with them.

What’s the difference between asm.js and WASM?
----------------------------------------------

- **asm.js** is a subset of JavaScript optimized for speed. It is fully supported by all browsers (even older ones) and compiles to a large ``.js`` file.
- **WebAssembly (WASM)** is a binary format that is smaller and faster to load and execute. Most modern browsers support it, and it is generally recommended for new projects. **WASM** is also easier to integrate with native browser APIs compared to **asm.js**.

Setting up Conan profiles
-------------------------

**For asm.js (JavaScript-based output):**

.. code-block:: text

   [settings]
   arch=asm.js
   build_type=Release
   compiler=emcc
   compiler.cppstd=<cppstd>
   compiler.libcxx=<libcxx>
   compiler.threads=<threads>
   compiler.version=<version>
   os=Emscripten

   [tool_requires]
   emsdk/[*]

   [conf]
   # Optional settings to enable memory allocation
   tools.build:exelinkflags=['-sALLOW_MEMORY_GROWTH=1', '-sMAXIMUM_MEMORY=2GB', '-sINITIAL_MEMORY=64MB']
   tools.build:sharedlinkflags=['-sALLOW_MEMORY_GROWTH=1', '-sMAXIMUM_MEMORY=2GB', '-sINITIAL_MEMORY=64MB']

**For WebAssembly (WASM):**

.. code-block:: text

   [settings]
   arch=wasm
   build_type=Release
   compiler=emcc
   compiler.cppstd=<cppstd>
   compiler.libcxx=<libcxx>
   compiler.threads=<threads>
   compiler.version=<version>
   os=Emscripten

   [tool_requires]
   emsdk/[*]

   [conf]
   # Optional settings to enable memory allocation
   tools.build:exelinkflags=['-sALLOW_MEMORY_GROWTH=1', '-sMAXIMUM_MEMORY=4GB', '-sINITIAL_MEMORY=64MB']
   tools.build:sharedlinkflags=['-sALLOW_MEMORY_GROWTH=1', '-sMAXIMUM_MEMORY=4GB', '-sINITIAL_MEMORY=64MB']


Even though Emscripten is not a true runtime environment (like Linux or
Windows), it is part of a toolchain ecosystem that compiles C/C++ to
WebAssembly (WASM) and asm.js.

Conan uses Emscripten to:

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

.. note::

   The profiles above use the ``emsdk`` package from `Conan Center Index repository <https://conan.io/center/recipes/emsdk>`_, which provides the Emscripten SDK, including ``emcc``, ``em++``, and tools like ``emrun`` and ``node``.
   
   If you prefer to use your system-installed Emscripten instead of the Conan-provided one, ``tool_requires`` could be replaced by custom ``compiler_executables`` and ``buildenv``:
   
   .. code-block:: text

      [conf]
      tools.build:compiler_executables={'c':'/path/to/emcc', 'cpp':'/path/to/em++'}
      # Add native Emscripten toolchain
      # tools.cmake.cmaketoolchain:user_toolchain=["/path/to/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake"]

      [buildenv]
      CC=emcc
      CXX=em++
      AR=emar
      NM=emnm
      RANLIB=emranlib
      STRIP=emstrip


   This way conan could configure `emsdk` local installation to be used from `CMake`, `Meson`, `Autotools` or other build systems.


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

   Also, when requiring ``emsdk`` package as a tool, it is recommended to use it this way:

   .. code-block:: python

       self.tool_requires("emsdk/[*]", package_id_mode="patch_mode")


   This will ensure that the package ID is generated based on the Emscripten
   version, allowing Conan to detect changes in the Emscripten toolchain and
   rebuild the project accordingly.
