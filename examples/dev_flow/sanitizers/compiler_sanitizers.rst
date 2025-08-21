.. _examples_dev_flow_sanitizers_compiler_sanitizers:

Compiler sanitizers
===================

.. warning::

    Using sanitizers in production with suid binaries is dangerous, as the libsanitizer runtime
    relies on environment variables that could enable privilege escalation attacks.
    Use sanitizers only in development and testing environments.

Sanitizers are powerful tools for detecting runtime bugs like buffer overflows, memory leaks,
dangling pointers, and various types of undefined behavior.

Compilers such as GCC, Clang and MSVC support these tools through specific compiler and linker flags.

This example explains a recommended approach for integrating compiler sanitizers into your Conan 2.x workflow.

Modeling and Applying Sanitizers using Settings
------------------------------------------------

If you want to model the sanitizer options so that the package id is affected by them, you have to
:ref:`customize new compiler sub-settings<reference_config_files_customizing_settings>`. You should not need
modify ``settings.yml`` directly, but adding :ref:`the settings_user.yml <examples_config_files_settings_user>`
instead.

This approach is preferred because it ensures that enabling a sanitizer alters the package ID, allowing you to use the same
binary package with or without sanitizers, which is ideal for development and debugging workflows.

To better illustrate this, please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/dev_flow/sanitizers/compiler_sanitizers

In this example we are going to see how to prepare Conan to use sanitizers in different ways.


Configuring Sanitizers as Part of Settings
##########################################

If you typically use a specific set of sanitizers or combinations for your builds, you can specify
them as a list of values. For example, with Clang, you might do the following:

.. code-block:: yaml
    :caption: *settings_user.yml*
    :emphasize-lines: 3

    compiler:
      clang:
        sanitizer: [None, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]

Here you have modeled the use of ``-fsanitize=address``, ``-fsanitize=thread``,
``-fsanitize=memory``, ``-fsanitize=leak``, ``-fsanitize=undefined``, ``-fsanitize=hwaddress``, ``-fsanitize=kernel-address``, the combination of ``-fsanitize=address`` with
``-fsanitize=undefined`` and ``-fsanitize=thread`` with ``-fsanitize=undefined``.

It seems be a large number of options, but for Clang, these are only a portion.
To obtain the complete list of available sanitizers, you can refer to the `Clang documentation <https://clang.llvm.org/docs/>`_.
The GCC supports a similar number of sanitizers, and you can find the complete list in the `GCC documentation <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_.
For MSVC, the available sanitizers are more limited, and you can find the complete list in the `MSVC documentation <https://learn.microsoft.com/en-us/cpp/sanitizers/>`_.

Note that not all sanitizer combinations are possible, for example, with Clang, you cannot use more than one of the Address, Thread, or Memory sanitizers in the same program.

Be aware once ``setting_user.yml`` is present in your Conan home, it will affect all your projects using Conan, asking for the setting ``compiler.sanitizer`` always.
In order to disable it, just remove the ``settings_user.yml`` file from your Conan home.

Adding Sanitizers as Part of the Profile
########################################

An option would be to add the sanitizer values as part of the profile.
This way, you can easily switch between different sanitizer configurations by using different dedicated profiles.

.. code-block:: ini
    :caption: *~/.conan/profiles/asan*
    :emphasize-lines: 7

    include(default)

    [settings]
    compiler.sanitizer=Address

    [conf]
    tools.build:cflags=['-fsanitize=address']
    tools.build:cxxflags=['-fsanitize=address']
    tools.build:exelinkflags=['-fsanitize=address']

The Conan client is not capable to deduce the necessary flags from the settings and apply them during the build process.
It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value.

Building Examples Using Sanitizers
----------------------------------

To show how to use sanitizers in your builds, let's consider a couple of examples.

Address Sanitizer: Index Out of Bounds
######################################

In this example, we will build a simple C++ program that intentionally accesses an out-of-bounds
index in an array, which should trigger the Address Sanitizer when running the program.

The following code demonstrates this:

.. code-block:: cpp
    :caption: *index_out_of_bounds/main.cpp*
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

The definition ``__SANITIZE_ADDRESS__`` is used to check if the Address Sanitizer is enabled when
running the produced application. It's supported by GCC, Clang and MSVC compilers.

To build this example, you can use Conan to invoke CMake and perform the build.

.. code-block:: bash

    conan export index_out_of_bounds/
    conan install --requires=index_out_of_bounds/0.1.0 -pr profiles/asan -of index_out_of_bounds/install --build=missing


Here we are using Conan to export the recipe and build the project.
The profile file `profiles/asan` was demonstrated already and will merge with the default profile
from your configuration. The resulting build will produce an executable in a specific package folder,
in order to access it, you can use the script produced by the ``VirtualRunEnv`` generator,
then run the executable:

.. code-block:: text

    source index_out_of_bounds/install/conanrun.sh
    index_out_of_bounds

    Address sanitizer enabled
    =================================================================
    ==32018==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffbe04a6d0 at pc 0x5dad4506e2eb bp 0x7fffbe04a500 sp 0x7fffbe04a4f0
    WRITE of size 4 at 0x7fffbe04a6d0 thread T0
        #0 0x5dad4506e2ea in main (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x12ea)
        #1 0x731331629d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
        #2 0x731331629e3f in __libc_start_main_impl ../csu/libc-start.c:392
        #3 0x5dad4506e3d4 in _start (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x13d4)

    Address 0x7fffbe04a6d0 is located in stack of thread T0 at offset 448 in frame
        #0 0x5dad4506e1ef in main (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x11ef)

    This frame has 1 object(s):
        [48, 448) 'foo' (line 11) <== Memory access at offset 448 overflows this variable
    HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
        (longjmp and C++ exceptions *are* supported)
    SUMMARY: AddressSanitizer: stack-buffer-overflow (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x12ea) in main

Once running the example, you should see an error message from the Address Sanitizer indicating the
out-of-bounds. The message is simplified here, but it provides useful information about the error,
including the expected index of bounds error.


Undefined Sanitizer: Signed Integer Overflow
############################################

This example demonstrates how to use the Undefined Behavior Sanitizer to detect signed integer overflow.
It combines the usage of two sanitizers at same time: Address Sanitizer and Undefined Behavior Sanitizer.
For this example, we will be using the following Conan profile:

.. code-block:: ini
    :caption: *~/.conan/profiles/asan_ubsan*
    :emphasize-lines: 7

    include(default)

    [settings]
    compiler.sanitizer=AddressUndefinedBehavior

    [conf]
    tools.build:cflags=['-fsanitize=address,undefined']
    tools.build:cxxflags=['-fsanitize=address,undefined']
    tools.build:exelinkflags=['-fsanitize=address,undefined']

It's important to mention it only works for GCC and Clang compilers,
as MSVC does not support the Undefined Behavior Sanitizer yet.

The source code for this example is as follows:

.. code-block:: cpp
    :caption: *signed_integer_overflow/main.cpp*
    :emphasize-lines: 12

    #include <iostream>
    #include <cstdlib>
    #include <cstdint>

    int main(int argc, char* argv[]) {
        #ifdef __SANITIZE_ADDRESS__
            std::cout << "Address sanitizer enabled\n";
        #else
            std::cout << "Address sanitizer not enabled\n";
        #endif

        int foo = 0x7fffffff;
        foo += argc; // Signed integer overflow

        return EXIT_SUCCESS;
    }

In this example, it's intentionally causing a signed integer overflow by adding the command line argument count to a large integer value.

As next step, the code can be built using Conan and CMake, similar to the previous example:

.. code-block:: bash

    conan export signed_integer_overflow/
    conan install --requires=signed_integer_overflow/0.1.0 -pr profiles/asan -of signed_integer_overflow/install --build=missing


Once the project built successfully, you can run the example with the sanitizers enabled:

.. code-block:: bash

    conan build signed_integer_overflow/install
    ./build/signed_integer_overflow

This should trigger the Address and Undefined Behavior Sanitizers, and you should see output indicating any detected issues.z

Passing the information to the compiler or build system
-------------------------------------------------------

Besides using Conan profiles to manage sanitizer settings, you can also use different approaches.

Managing Sanitizer with CMake Toolchain
#######################################

**TODO**


Mananaging Sanitizer with Conan Hooks
#####################################

**TODO**