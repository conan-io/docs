.. _examples_dev_flow_sanitizers_compiler_sanitizers:

Compiler sanitizers
===================

.. warning::

   Using sanitizers in production, particularly with SUID binaries, is dangerous. The libsanitizer
   runtimes rely on environment variables that could enable privilege escalation attacks.
   Use sanitizers only in development and testing environments.

Sanitizers are powerful tools for detecting runtime bugs like buffer overflows, data races, memory leaks,
dangling pointers, use-of-uninitialized memory, and various types of undefined behavior. Compilers such as
GCC, Clang, and MSVC support these tools through specific compiler and linker flags.

This document explains recommended approaches for integrating compiler sanitizers into your Conan 2.x workflow.

Modeling and applying sanitizers using settings
-----------------------------------------------

If you want to model sanitizer options so that the package ID is affected by them, you can
:ref:`customize new compiler sub-settings <reference_config_files_customizing_settings>`. You should not need
to modify ``settings.yml`` directly; instead add :ref:`the settings_user.yml <examples_config_files_settings_user>`.

This approach is preferred because enabling a sanitizer alters the package ID, allowing you to build and use
the same binary package with or without sanitizers. This is ideal for development and debugging workflows.

To better illustrate this, please clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

   git clone https://github.com/conan-io/examples2.git
   cd examples2/examples/dev_flow/sanitizers/compiler_sanitizers

In this example we will see how to prepare Conan to use sanitizers in different ways.

Configuring sanitizers as part of settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

It may seem like a large number of options, but for Clang, these are only a portion. To obtain the complete list,
refer to:

* Clang: `AddressSanitizer <https://clang.llvm.org/docs/AddressSanitizer.html>`_,
  `ThreadSanitizer <https://clang.llvm.org/docs/ThreadSanitizer.html>`_,
  `MemorySanitizer <https://clang.llvm.org/docs/MemorySanitizer.html>`_,
  `UndefinedBehaviorSanitizer <https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html>`_.
* GCC: `Instrumentation Options <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_.
* MSVC: `MSVC Sanitizers <https://learn.microsoft.com/en-us/cpp/sanitizers/>`_.

**Notes on combinations**:

* AddressSanitizer (ASan), ThreadSanitizer (TSan), and MemorySanitizer (MSan) are mutually exclusive with one another.
* Address + UndefinedBehavior (UBSan) is a common and supported combination.
* Thread + UndefinedBehavior is also supported.
* MemorySanitizer often requires special flags such as ``-O1``, ``-fno-omit-frame-pointer`` and fully-instrumented dependencies.

Adding sanitizers as part of the profile
----------------------------------------

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


Building examples using sanitizers
----------------------------------

To show how to use sanitizers in your builds, let's consider two examples.

.. note::

   To build your project with a sanitizer, simply use the corresponding profile.
   It is crucial to **rebuild all dependencies from source** to ensure they are also instrumented,
   which prevents false positives and other issues.

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
The define ``__SANITIZE_ADDRESS__`` is present when ASan is active;

**To build and run this example using Conan:**

.. code-block:: bash

   conan export index_out_of_bounds/
   conan install --requires=index_out_of_bounds/0.1.0 -pr profiles/asan -of index_out_of_bounds/install --build=missing
   # Activate run environment to ensure sanitizer runtime and paths are set
   source index_out_of_bounds/install/conanrun.sh
   index_out_of_bounds

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
   conan install --requires=signed_integer_overflow/0.1.0 -pr profiles/asan_ubsan -of signed_integer_overflow/install --build=missing
   source signed_integer_overflow/install/conanrun.sh
   signed_integer_overflow

**Expected output (abbreviated):**

.. code-block:: text

   Address sanitizer enabled
   .../main.cpp:16:9: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'

Passing the information to the compiler or build system
-------------------------------------------------------

Besides using Conan profiles to manage sanitizer settings, you can also use other approaches.

Managing sanitizers with a CMake toolchain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Managing sanitizers with Conan hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another approach is using :ref:`Conan hooks <reference_extensions_hooks>`. With hooks, you can inject compiler
flags on-the-fly during the build process, allowing for dynamic configurations without modifying the original
build files.

For instance, add a ``pre_generate`` hook to append the necessary sanitizer flags based on the
``compiler.sanitizer`` setting:

.. code-block:: python
   :caption: ~/.conan2/extensions/hooks/hook_sanitizer_flags.py

   def pre_generate(conanfile):
       sani = conanfile.settings.get_safe("compiler.sanitizer")
       if not sani or sani == "null":
           return
       mapping = {
           "Address": "address",
           "Leak": "leak",
           "Thread": "thread",
           "Memory": "memory",
           "UndefinedBehavior": "undefined",
           "HardwareAssistanceAddress": "hwaddress",
           "KernelAddress": "kernel-address",
           "AddressUndefinedBehavior": "address,undefined",
           "ThreadUndefinedBehavior": "thread,undefined",
       }
       fs = mapping.get(sani)
       if not fs:
           return
       flag = f"-fsanitize={fs}"
       for k in ("tools.build:cflags", "tools.build:cxxflags",
                 "tools.build:exelinkflags", "tools.build:sharedlinkflags"):
           conanfile.conf.append(k, flag)
       # Optional: better stack traces
       conanfile.conf.append("tools.build:cxxflags", "-fno-omit-frame-pointer")

The ``pre_generate`` hook is executed before Conan generates toolchain files, so it can contribute to the final
configuration for compiler and linker flags. This approach is flexible, but can increase maintenance complexity
as it moves logic out of profile management.

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
