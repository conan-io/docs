.. _security_sanitizers:

Sanitizers
==========

.. warning::

   Do not use sanitizers for production builds, especially for binaries with elevated privileges (e.g., SUID).
   Sanitizer runtimes rely on environment variables and can enable privilege escalation.
   Use only in development and testing.

Sanitizers are powerful runtime instrumentation tools that detect issues such as:

* Buffer overflows (stack/heap), use-after-free, double-free
* Data races in multithreaded code
* Memory leaks
* Use of uninitialized memory
* A wide range of undefined behaviors

Compilers such as GCC, Clang, and MSVC support sanitizers via compiler and linker flags.

This page explains recommended approaches for integrating compiler sanitizers into your workflow with Conan.

Compiler Sanitizer Support Comparison
-------------------------------------

.. important::

   Always rebuild all dependencies from source when enabling sanitizers to ensure consistent instrumentation
   and to avoid false positives (particularly critical for MemorySanitizer).

Each compiler has different levels of support for various sanitizers, Clang being the most comprehensive so far.
To help you choose the right sanitizer for your needs and compiler, here is a summary of the most common ones:

+----------------------------------------+-----+-------+------+-----------------------------------------+
| Sanitizer                              | GCC | Clang | MSVC | Notes                                   |
+========================================+=====+=======+======+=========================================+
| **AddressSanitizer (ASan)**            | ✅  | ✅    | ✅   | MSVC: Not supported for 32-bit targets  |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **ThreadSanitizer (TSan)**             | ✅  | ✅    | ❌   | Detects data races                      |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **MemorySanitizer (MSan)**             | ❌  | ✅    | ❌   | Clang-only, requires `-O1`              |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **UndefinedBehaviorSanitizer (UBSan)** | ✅  | ✅    | ❌   | Wide range of undefined behavior checks |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **LeakSanitizer (LSan)**               | ✅  | ✅    | ❌   | Often integrated with ASan              |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **HardwareAddressSanitizer (HWASan)**  | ❌  | ✅    | ❌   | ARM64 only, lower overhead than ASan    |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **KernelAddressSanitizer (KASan)**     | ✅  | ✅    | ✅   | MSVC: Requires Windows 11               |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **DataFlowSanitizer (DFSan)**          | ❌  | ✅    | ❌   | Dynamic data flow analysis              |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **Control Flow Integrity (CFI)**       | ❌  | ✅    | ✅   | MSVC: `/guard:cf`                       |
+----------------------------------------+-----+-------+------+-----------------------------------------+

Besides MSVC having more limited support for sanitizers, it encourages the community to vote for new features
at `Developer Community <https://developercommunity.visualstudio.com/cpp>`_.

Also, you can consider the typical use cases for each sanitizer:

* **AddressSanitizer (ASan)**: Great default for memory errors; often combined with UBSan for broader coverage.
* **ThreadSanitizer (TSan)**: Find data races in multithreaded code.
* **MemorySanitizer (MSan)**: Detects uninitialized memory reads (Clang-only). Requires all dependencies to be instrumented.
* **LeakSanitizer (LSan)**: Often included with ASan on Clang/GCC, can be enabled explicitly. Typically used to find memory leaks.
* **UndefinedBehaviorSanitizer (UBSan)**: Catches many undefined behaviors; often combined with ASan.

Common Sanitizer Combinations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The sanitizers can often be combined to provide more comprehensive coverage, but not all combinations are supported by every compiler.
Here are some common combinations and their compatibility mostly used with GCC and Clang:

+-------------------+-----+-------+------+-----------------------------------------+
| Combination       | GCC | Clang | MSVC | Compatibility                           |
+===================+=====+=======+======+=========================================+
| **ASan + UBSan**  | ✅  | ✅    | ❌   | Most common combination                 |
+-------------------+-----+-------+------+-----------------------------------------+
| **TSan + UBSan**  | ✅  | ✅    | ❌   | Good for multithreaded code             |
+-------------------+-----+-------+------+-----------------------------------------+
| **ASan + LSan**   | ✅  | ✅    | ❌   | LSan often enabled by default with ASan |
+-------------------+-----+-------+------+-----------------------------------------+
| **MSan + UBSan**  | ❌  | ✅    | ❌   | Requires careful dependency management  |
+-------------------+-----+-------+------+-----------------------------------------+

**Notes on combinations**:

* AddressSanitizer (ASan), ThreadSanitizer (TSan), and MemorySanitizer (MSan) **are mutually exclusive with one another**.
* MemorySanitizer often requires special flags such as ``-O1``, ``-fno-omit-frame-pointer`` and fully-instrumented dependencies;
  mixing with non-instrumented code leads to crashes/false positives.

Compiler-Specific Flags
^^^^^^^^^^^^^^^^^^^^^^^

Each compiler requires specific flags to enable the desired sanitizers. Here is a summary of the most common
sanitizers and their corresponding flags for GCC, Clang, and MSVC:

+-----------------------+------------------------+------------------------+----------------------+
| Sanitizer             | GCC Flag               | Clang Flag             | MSVC Flag            |
+=======================+========================+========================+======================+
| **AddressSanitizer**  | `-fsanitize=address`   | `-fsanitize=address`   | `/fsanitize=address` |
+-----------------------+------------------------+------------------------+----------------------+
| **ThreadSanitizer**   | `-fsanitize=thread`    | `-fsanitize=thread`    | N/A                  |
+-----------------------+------------------------+------------------------+----------------------+
| **MemorySanitizer**   | N/A                    | `-fsanitize=memory`    | N/A                  |
+-----------------------+------------------------+------------------------+----------------------+
| **UndefinedBehavior** | `-fsanitize=undefined` | `-fsanitize=undefined` | N/A                  |
+-----------------------+------------------------+------------------------+----------------------+
| **LeakSanitizer**     | `-fsanitize=leak`      | `-fsanitize=leak`      | N/A                  |
+-----------------------+------------------------+------------------------+----------------------+

It may seem like a large number of options, but for Clang, these are only a portion. To obtain the complete list,
please refer to the official documentation for each compiler:

* Clang: `AddressSanitizer <https://clang.llvm.org/docs/AddressSanitizer.html>`_,
  `ThreadSanitizer <https://clang.llvm.org/docs/ThreadSanitizer.html>`_,
  `MemorySanitizer <https://clang.llvm.org/docs/MemorySanitizer.html>`_,
  `UndefinedBehaviorSanitizer <https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html>`_.
* GCC: `Instrumentation Options <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_.
* MSVC: `MSVC Sanitizers <https://learn.microsoft.com/en-us/cpp/sanitizers/>`_.

Binary Compatibility
--------------------

How sanitizers affect your binaries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sanitizers instrument your code at compile time, adding runtime checks and metadata.
This changes your binary's **Application Binary Interface (ABI)**, making instrumented code incompatible with non-instrumented code.

**Key changes sanitizers make:**

- **Memory layout**: Sanitizers add shadow memory, guard zones, or tracking metadata around your data
- **Function calls**: Standard library functions (``malloc``, ``free``, etc.) are wrapped or intercepted
- **Runtime dependencies**: Instrumented code requires sanitizer runtime libraries (``libasan``, ``libtsan``, etc.)
- **Linking**: Mixing instrumented and non-instrumented code can cause crashes, false positives, or undefined behavior

Handling external code
^^^^^^^^^^^^^^^^^^^^^^

When using sanitizers, you must consider how to handle third-party dependencies.
As mixing instrumented and non-instrumented code can lead to issues, here are some strategies:

**Always require full instrumentation:**

- **MemorySanitizer (MSan)**: Changes function ABIs to pass shadow state.
- **DataFlowSanitizer (DFSan)**: Explicitly modifies the ABI by appending label parameters to functions.
- **ThreadSanitizer (TSan)**: Changes memory layout and intercepts synchronization primitives.
  Some code may not be instrumented by ThreadSanitizer, but not recommended.

**Usually require full instrumentation:**

- **AddressSanitizer (ASan)**: Adds redzones and shadow memory; Works with non-instrumented code, but not recommended.
- **HardwareAddressSanitizer (HWASan)**: Similar to ASan but uses hardware tagging. Mixing is possible but not recommended.

**Can often mix with non-instrumented code:**

- **UndefinedBehaviorSanitizer (UBSan)**: Adds runtime checks for undefined behavior; Minimal ABI changes, safer to mix.
- **LeakSanitizer (LSan)**: Detects memory leaks at program exit; When standalone, has minimal ABI impact.

For reliable results, **always** rebuild your entire dependency tree with the same sanitizer configuration.

Enabling Sanitizers
-------------------

Conan cannot infer sanitizer flags from settings automatically.
You have to pass the appropriate compiler and linker flags (e.g., ``-fsanitize=`` or ``/fsanitize=address``) via profiles or toolchains.
Conan toolchains (e.g., ``CMakeToolchain``, ``MesonToolchain``) will propagate flags defined in ``[conf]`` sections.

Modeling and applying sanitizers using settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to model sanitizer options so that the package ID is affected by them, you can
:ref:`customize new compiler sub-settings <reference_config_files_customizing_settings>`. You should not need
to modify ``settings.yml`` directly; instead add :ref:`the settings_user.yml <examples_config_files_settings_user>`.

This approach is preferred because enabling a sanitizer alters the package ID, allowing you to build and use
the same binary package with or without sanitizers. This is ideal for development and debugging workflows.

Configuring sanitizers as part of settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you typically use a specific set of sanitizers or combinations for your builds, you can specify
a sub-setting as a list of values in your ``settings_user.yml``. For example, for Clang:

.. code-block:: yaml
   :caption: settings_user.yml
   :emphasize-lines: 3

   compiler:
     clang:
       sanitizer: [null, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]

This example defines a few common sanitizers. You can add any sanitizer your compiler supports.
The ``null`` value represents a build without sanitizers. The above models the use of ``-fsanitize=address``,
``-fsanitize=thread``, ``-fsanitize=memory``, ``-fsanitize=leak``, ``-fsanitize=undefined``, ``-fsanitize=hwaddress``,
``-fsanitize=kernel-address``, as well as combinations like ``-fsanitize=address,undefined`` and ``-fsanitize=thread,undefined``.

As the ``sanitizer`` setting is a list, it can be choose by one single value at time.
As an workaround to support mutiple sanitizers at same time, you can define combinations like
``AddressUndefinedBehavior`` and ``ThreadUndefinedBehavior``, as listed above.
There is no limitation on the number of combinations you can define, but keep in mind that these are only tags
to help you manage your builds. You still need to pass the appropriate flags to the compiler and linker accordingly.

Adding sanitizers as part of the profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another option is to add the sanitizer values as part of a profile. This way, you can easily switch between
different configurations by using dedicated profiles.

.. code-block:: ini
   :caption: compiler_sanitizers/profiles/asan

   include(default)

   [settings]
   build_type=Debug
   compiler.sanitizer=Address

   [conf]
   tools.build:cflags+=["-fsanitize=address", "-fno-omit-frame-pointer"]
   tools.build:cxxflags+=["-fsanitize=address", "-fno-omit-frame-pointer"]
   tools.build:exelinkflags+=["-fsanitize=address"]
   tools.build:sharedlinkflags+=["-fsanitize=address"]

   [runenv]
   ASAN_OPTIONS="halt_on_error=1:detect_leaks=1"

For Visual Studio (MSVC) we can obtain an equivalent profile for AddressSanitizer:

.. code-block:: ini
   :caption: ~/.conan/profiles/asan

   include(default)

   [settings]
   build_type=Debug
   compiler.sanitizer=Address

   [conf]
   tools.build:cxxflags+=["/fsanitize=address", "/Zi"]
   tools.build:exelinkflags+=["/fsanitize=address"]

The Conan client is not capable of deducing the necessary flags from the settings and applying them automatically
during the build process. It is necessary to pass the expected sanitizer flags according to the
``compiler.sanitizer`` value as part of the compiler and linker flags.
Conan's built-in toolchains (like ``CMakeToolchain`` and ``MesonToolchain``) will automatically
pick up the flags defined in the ``[conf]`` section and apply them to the build.

Managing sanitizers with a CMake toolchain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Besides using Conan profiles to manage sanitizer settings, you can also use other approaches.

If you already have a :ref:`custom CMake toolchain file <conan_cmake_user_toolchain>` to manage compiler
and build options, you can pass the necessary flags to enable sanitizers there instead of profiles.

.. code-block:: cmake
   :caption: cmake/my_toolchain.cmake

   # Apply to all targets; consider per-target options for finer control
   set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=address,undefined -fno-omit-frame-pointer")
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address,undefined -fno-omit-frame-pointer")
   set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address,undefined")
   set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -fsanitize=address,undefined")

Then, specify this toolchain file as part of your Conan profile:

.. code-block:: ini
   :caption: profiles/asan_ubsan

   include(default)

   [settings]
   build_type=Debug
   compiler.sanitizer=AddressUndefinedBehavior

   [conf]
   tools.cmake.cmaketoolchain:user_toolchain=cmake/my_toolchain.cmake

This way, you can keep your existing CMake toolchain file and still leverage Conan profiles to manage other settings.

Building Examples Using Sanitizers
----------------------------------

To better illustrate this, first, please clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

   git clone https://github.com/conan-io/examples2.git
   cd examples2/examples/dev_flow/sanitizers/compiler_sanitizers

In this example we will see how to prepare Conan to use sanitizers in different ways.

To show how to use sanitizers in your builds, let's consider two examples.

AddressSanitizer: index out of bounds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, we will build a simple C++ program that intentionally accesses an out-of-bounds index
in an array, which should trigger ASan when running the program.

.. code-block:: cpp
   :caption: index_out_of_bounds/main.cpp
   :emphasize-lines: 11

   #include <iostream>
   #include <cstdlib>

   int main() {
   #ifdef __SANITIZE_ADDRESS__
     std::cout << "Address sanitizer enabled\n";
   #else
     std::cout << "Address sanitizer not enabled\n";
   #endif

     int foo[100];
     foo[100] = 42; // Out-of-bounds write

     return EXIT_SUCCESS;
   }

**Note:** The preprocessor check above is portable for GCC, Clang and MSVC.
The define ``__SANITIZE_ADDRESS__`` is present when **ASan** is active;

**To build and run this example using Conan:**

.. code-block:: bash

   conan export index_out_of_bounds/
   conan build index_out_of_bounds --version=0.1.0 -pr profiles/asan -of index_out_of_bounds/install --build=missing
   index_out_of_bounds/build/Debug/index_out_of_bounds

**Expected output (abbreviated):**

.. code-block:: text

   Address sanitizer enabled
   ==32018==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffbe04a6d0 ...
   WRITE of size 4 at 0x7fffbe04a6d0 thread T0
   #0 ... in main .../index_out_of_bounds+0x12ea
   ...
   SUMMARY: AddressSanitizer: stack-buffer-overflow ... in main
   This frame has 1 object(s):
   [48, 448) 'foo' (line 11) <== Memory access at offset 448 overflows this variable

UndefinedBehaviorSanitizer: signed integer overflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to use UBSan to detect signed integer overflow. It combines ASan and UBSan.
Create a dedicated profile:

.. code-block:: ini
   :caption: ~/.conan/profiles/asan_ubsan
   :emphasize-lines: 7

   include(default)

   [settings]
   build_type=Debug
   compiler.sanitizer=AddressUndefinedBehavior

   [conf]
   tools.build:cflags+=["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
   tools.build:cxxflags+=["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
   tools.build:exelinkflags+=["-fsanitize=address,undefined"]
   tools.build:sharedlinkflags+=["-fsanitize=address,undefined"]

It is supported by GCC and Clang. MSVC does not support UBSan.

**Source code:**

.. code-block:: cpp
   :caption: signed_integer_overflow/main.cpp
   :emphasize-lines: 14

   #include <iostream>
   #include <cstdlib>
   #include <climits>

   int main() {
   #ifdef __SANITIZE_ADDRESS__
     std::cout << "Address sanitizer enabled\n";
   #else
     std::cout << "Address sanitizer not enabled\n";
   #endif

     int x = INT_MAX;
     x += 42;                     // signed integer overflow

     return EXIT_SUCCESS;
   }

**Build and run:**

.. code-block:: bash

   conan export signed_integer_overflow/
   conan build signed_integer_overflow/ --version=0.1.0 -pr profiles/asan_ubsan -of signed_integer_overflow/install --build=missing
   signed_integer_overflow/build/Debug/signed_integer_overflow

**Expected output (abbreviated):**

.. code-block:: text

   Address sanitizer enabled
   .../main.cpp:16:9: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'

When executing the example application, UBSan detects the signed integer overflow and reports it as expected.

Additional recommendations
--------------------------

* Debug info and optimization:

  * For ASan/TSan, ``-O1`` or ``-O2`` generally works; for MSan, prefer ``-O1`` and avoid aggressive inlining.
  * ``-fno-omit-frame-pointer`` helps stack traces.

* Runtime symbolization:

  * Useful settings for CI:

    * ``ASAN_OPTIONS=halt_on_error=1:detect_leaks=1:log_path=asan``.
    * ``UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1:log_path=ubsan``.

* Suppressions:

  * For ASan: ``ASAN_OPTIONS=suppressions=asan.supp``.
  * For UBSan: ``UBSAN_OPTIONS=suppressions=ubsan.supp``.
  * Keep suppressions under version control and load them in CI jobs.

* Third-party dependencies:

  * Mixed instrumented/uninstrumented code can lead to false positives or crashes, especially with MSan.
  * Prefer building dependencies with the same sanitizer or limit sanitizers to leaf applications.

* MSVC and Windows notes:

  * ASan with MSVC/Clang-cl uses ``/fsanitize=address`` and PDBs via ``/Zi``. Not supported for 32-bit targets.
  * KAsan requires Windows 11.
  * Some features are limited when using whole program optimization (``/GL``) or certain runtime libraries.
