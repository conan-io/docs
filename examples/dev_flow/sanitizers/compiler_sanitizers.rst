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
    :emphasize-lines: 6

    include(default)

    [settings]
    compiler.sanitizer=Address

    [conf]
    tools.build:cflags=['-fsanitize=address']
    tools.build:cxxflags=['-fsanitize=address']

The Conan client is capable to deduce the necessary flags from the profile and apply them during the build process.
It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value.

Building Examples Using Sanitizers
----------------------------------

Address Sanitizer: Index Out of Bounds
######################################

**TODO**

Undefined Sanitizer: Signed Integer Overflow
############################################

**TODO**

Passing the information to the compiler or build system
-------------------------------------------------------

Besides using Conan profiles to manage sanitizer settings, you can also use different approaches.

Managing Sanitizer with CMake Toolchain
#######################################

**TODO**


Mananaging Sanitizer with Conan Hooks
#####################################

**TODO**