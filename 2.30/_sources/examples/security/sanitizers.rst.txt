.. _examples_security_sanitizers:

Using Compiler Sanitizers with Conan
====================================

To better illustrate the :ref:`sanitizers integration with Conan <security_sanitizers>`,
this section provides practical examples using AddressSanitizer (ASan) and
UndefinedBehaviorSanitizer (UBSan) with simple C++ programs.

As a first step, please clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

   git clone https://github.com/conan-io/examples2.git
   cd examples2/examples/security/sanitizers/compiler_sanitizers

In this example we will see how to prepare Conan to use sanitizers in different ways.

To show how to use sanitizers in your builds, let's consider two examples.

AddressSanitizer: index out of bounds
-------------------------------------

In this example, we will build a simple C++ program that intentionally accesses an out-of-bounds index
in an array, which should trigger ASan when running the program. We will be using a Conan profile to enable ASan:

.. code-block:: ini
   :caption: profiles/gcc_asan
   :emphasize-lines: 10

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
    tools.build:cflags=['-fsanitize=address']
    tools.build:cxxflags=['-fsanitize=address']
    tools.build:exelinkflags=['-fsanitize=address']
    tools.build:sharedlinkflags+=["-fsanitize=address"]

    [runenv]
    ASAN_OPTIONS=halt_on_error=1:detect_leaks=1

Note that in this profile we set the ``compiler.sanitizer=Address`` does not
define what compiler flags to use, but it is a settings to make explicit that
both ASan and UBSan are intended to be used.

And for further illustration, we also use environment variable
``ASAN_OPTIONS=halt_on_error=1:detect_leaks=1`` for runtime configuration,
to manage ASan to halt execution on the first error and to
detect memory leaks when the program exits.

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

   cd index_out_of_bounds/
   conan build . -pr ../profiles/gcc_asan
   build/Debug/index_out_of_bounds

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
---------------------------------------------------

This example demonstrates how to use UBSan to detect signed integer overflow. It combines ASan and UBSan.
Create a dedicated profile:

.. code-block:: ini
   :caption: profiles/gcc_asan_ubsan
   :emphasize-lines: 7

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

   cd signed_integer_overflow/
   conan build . -pr ../profiles/gcc_asan_ubsan
   build/Debug/signed_integer_overflow

**Expected output (abbreviated):**

.. code-block:: text

   Address sanitizer enabled
   .../main.cpp:16:9: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'

When executing the example application, UBSan detects the signed integer overflow and reports it as expected.
