.. _security_sanitizers:

C, C++ Compiler Sanitizers
==========================

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

   Always rebuild all dependencies when using MemorySanitizer (MSan) and generally for ThreadSanitizer (TSan)
   to avoid false positives/negatives. For AddressSanitizer, UBSan, and LeakSanitizer, mixing instrumented
   code with prebuilt libraries is typically safe, but may miss bugs inside those libraries.

Each compiler has different levels of support for various sanitizers, Clang being the most comprehensive so far.
To help you choose the right sanitizer for your needs and compiler, here is a summary of the most common ones:

+----------------------------------------+-----+-------+------+-----------------------------------------+
| Sanitizer                              | GCC | Clang | MSVC | Notes                                   |
+========================================+=====+=======+======+=========================================+
| **AddressSanitizer (ASan)**            | YES | YES   | YES  | MSVC: Supports x86, x64 and ARM64       |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **ThreadSanitizer (TSan)**             | YES | YES   | NO   | Detects data races                      |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **MemorySanitizer (MSan)**             | NO  | YES   | NO   | Clang-only, requires `-O1`              |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **UndefinedBehaviorSanitizer (UBSan)** | YES | YES   | NO   | Wide range of undefined behavior checks |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **LeakSanitizer (LSan)**               | YES | YES   | NO   | Often integrated with ASan              |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **HardwareAddressSanitizer (HWASan)**  | NO  | YES   | NO   | ARM64 only, lower overhead than ASan    |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **KernelAddressSanitizer (KASan)**     | YES | YES   | YES  | MSVC: Requires Windows 11               |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **DataFlowSanitizer (DFSan)**          | NO  | YES   | NO   | Dynamic data flow analysis              |
+----------------------------------------+-----+-------+------+-----------------------------------------+
| **Control Flow Integrity (CFI)**       | NO  | YES   | YES  | MSVC: `/guard:cf`                       |
+----------------------------------------+-----+-------+------+-----------------------------------------+

Besides MSVC having more limited support for sanitizers, it encourages the community to vote for new features
at `Developer Community <https://developercommunity.visualstudio.com/cpp>`_. Very recently Visual Studio 2026 added
support for AddressSanitizer on ARM64 architecture. This support should be straightforward when using Conan with MSVC.

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
| **ASan + UBSan**  | YES | YES   | NO   | Most common combination                 |
+-------------------+-----+-------+------+-----------------------------------------+
| **TSan + UBSan**  | YES | YES   | NO   | Good for multithreaded code             |
+-------------------+-----+-------+------+-----------------------------------------+
| **ASan + LSan**   | YES | YES   | NO   | LSan often enabled by default with ASan |
+-------------------+-----+-------+------+-----------------------------------------+
| **MSan + UBSan**  | NO  | YES   | NO   | Requires careful dependency management  |
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
a sub-setting as a list of values in your ``settings_user.yml``. For example, for Clang, GCC and MSVC:

.. code-block:: yaml
   :caption: settings_user.yml
   :emphasize-lines: 3

   compiler:
      clang:
        sanitizer: [null, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]
      gcc:
        sanitizer: [null, Address, Leak, Thread, UndefinedBehavior, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]
      msvc:
        sanitizer: [null, Address, KernelAddress]

This example defines a few common sanitizers. You can add any sanitizer your compiler supports.
The ``null`` value represents a build without sanitizers. The above models for Clang the use of ``-fsanitize=address``,
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
   :caption: compiler_sanitizers/profiles/gcc_asan

   [settings]
   arch=x86_64
   os=Linux
   build_type=Debug
   compiler=gcc
   compiler.cppstd=gnu20
   compiler.libcxx=libstdc++11
   compiler.version=15
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
   :caption: compiler_sanitizers/profiles/msvc_asan

   [settings]
   arch=x86_64
   os=Windows
   build_type=Debug
   compiler=msvc
   compiler.version=194
   compiler.runtime=dynamic
   compiler.runtime_type=Release
   compiler.sanitizer=Address

   [conf]
   tools.build:cxxflags+=["/fsanitize=address", "/Zi"]
   tools.build:exelinkflags+=["/fsanitize=address"]

The Conan client is not capable of deducing the necessary flags from the settings and applying them automatically
during the build process. It is necessary to pass the expected sanitizer flags according to the
``compiler.sanitizer`` value as part of the compiler and linker flags.
Conan's built-in toolchains (like ``CMakeToolchain`` and ``MesonToolchain``) will automatically
pick up the flags defined in the ``[conf]`` section and apply them to the build.

Managing sanitizers with a custom CMake toolchain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
   :caption: profiles/gcc_asan_ubsan

   [settings]
   arch=x86_64
   os=Linux
   build_type=Debug
   compiler=gcc
   compiler.cppstd=gnu20
   compiler.libcxx=libstdc++11
   compiler.version=15
   compiler.sanitizer=AddressUndefinedBehavior

   [conf]
   tools.cmake.cmaketoolchain:user_toolchain=["<path_to>/cmake/my_toolchain.cmake"]

This way, you can keep your existing CMake toolchain file and still leverage Conan profiles to manage other settings.

Note that this approach only works if all dependencies are built using CMake and the ``CMakeToolchain`` integration.
If you have dependencies using other build systems (e.g., Meson, Autotools), those dependencies will not receive the sanitizer flags
defined in your custom CMake toolchain file.

Managing sanitizers as a custom CMake Build Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another option, without using the custom ``compiler.sanitizer`` setting, is to define sanitizers as a custom CMake build type. In this approach, you select the sanitizer configuration by choosing the build type during the CMake configure step.
To achieve this, you can create a custom CMake toolchain file that maps build types to sanitizer flags. For example:

.. code-block:: cmake
   :caption: cmake/sanitizer_toolchain.cmake

   if(CMAKE_BUILD_TYPE STREQUAL "DebugASan")
       set(SANITIZER_FLAGS "-g -fsanitize=address -fno-omit-frame-pointer")
   elseif(CMAKE_BUILD_TYPE STREQUAL "DebugUBSan")
       set(SANITIZER_FLAGS "-g -fsanitize=undefined -fno-omit-frame-pointer")
   elseif(CMAKE_BUILD_TYPE STREQUAL "DebugASanUBSan")
       set(SANITIZER_FLAGS "-g -fsanitize=address,undefined -fno-omit-frame-pointer")
   else()
       set(SANITIZER_FLAGS "")
   endif()

   set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${SANITIZER_FLAGS}")
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${SANITIZER_FLAGS}")
   set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${SANITIZER_FLAGS}")
   set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} ${SANITIZER_FLAGS}")

Also, you will need to update your ``settings_user.yml`` to include the new build types:

.. code-block:: yaml
   :caption: settings_user.yml
   :emphasize-lines: 1

   build_type: [DebugASan, DebugUBSan, DebugASanUBSan]

Then, in your Conan profile, specify this toolchain file:

.. code-block:: ini
   :caption: profiles/gcc_asan_ubsan

   [settings]
   arch=x86_64
   os=Linux
   build_type=DebugASan
   compiler=gcc
   compiler.cppstd=gnu20
   compiler.libcxx=libstdc++11
   compiler.version=15

   [conf]
   tools.cmake.cmaketoolchain:user_toolchain=["<path_to>/sanitizer_toolchain.cmake"]

Be aware that this approach uses a custom build type, as a result, Conan will not automatically
apply the standard flags associated with the Debug build type. Therefore, in your custom toolchain file,
you need to also define the flags that correspond to the desired based build type, for example, that ``-g``
flag that matches the Debug ``build_type`` in gcc-like compilers.

Using this approach, you can easily switch between different sanitizer configurations and standard build types,
preserving the package ID differentiation based on the build type.

Practical Usage Examples
------------------------

For practical examples of using sanitizers with Conan, please refer to the
:ref:`Building Examples Using Sanitizers <examples_security_sanitizers>` section in the examples.

Additional recommendations
--------------------------

* Debug info and optimization:

  * For ASan/TSan and when using GCC or Clang, the compiler flags ``-O1`` or ``-O2`` generally works;
    for MSan, prefer ``-O1`` and avoid aggressive inlining.
  * ``-fno-omit-frame-pointer`` helps stack traces.

* Runtime symbolization:

  Some sanitizers can be configured to provide better stack traces and error reports.
  These features can be enabled via environment variables,
  such as ``ASAN_OPTIONS`` and ``UBSAN_OPTIONS`` for compilers like GCC and Clang.

  * Useful settings for CI:

    * ``ASAN_OPTIONS=halt_on_error=1:detect_leaks=1:log_path=asan``.

      This configuration makes AddressSanitizer stop execution on the first error,
      enables leak detection, and logs the output to a file named ``asan``.

    * ``UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1:log_path=ubsan``.

      This setup instructs UndefinedBehaviorSanitizer to print stack traces
      in a human-readable format, halt on the first error,
      and log the output to a file named ``ubsan``.

* Suppressions:

   If certain known issues are not relevant for your testing, you can create suppression files
   to filter them out from the sanitizer reports.

  * For ASan: ``ASAN_OPTIONS=suppressions=asan.supp``.

    Create a file named ``asan.supp`` with the following content:

    .. code-block:: text

       leak:FreeMyObject

    This example suppresses leak reports originating from ``FreeMyObject``.

  * For UBSan: ``UBSAN_OPTIONS=suppressions=ubsan.supp``.

      Create a file named ``ubsan.supp`` with the following content:

      .. code-block:: text

         signed-integer-overflow IncreaseCounter

      This example suppresses signed integer overflow reports from ``IncreaseCounter``.

* Third-party dependencies:

  * Mixed instrumented/uninstrumented code can lead to false positives or crashes, especially with MSan.
  * Prefer building dependencies with the same sanitizer or limit sanitizers to leaf applications.

* MSVC and Windows notes:

  * ASan with MSVC/Clang-cl uses ``/fsanitize=address`` and PDBs via ``/Zi``. Not supported for 32-bit targets.
  * KAsan requires Windows 11.
  * Some features are limited when using whole program optimization (``/GL``) or certain runtime libraries.
