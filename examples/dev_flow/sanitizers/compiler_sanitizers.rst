.. _examples_dev_flow_sanitizers_compiler_sanitizers:

Compiler sanitizers
===================

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
    :emphasize-lines: 6

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


Passing the information to the compiler or build system
-------------------------------------------------------

Here again, we have multiple choices to pass sanitizers information to the compiler or build system.

Using from custom profiles
##########################

It is possible to have different custom profiles defining the compiler sanitizer setting and
environment variables to inject that information to the compiler, and then passing those profiles to
Conan commands. An example of this would be a profile like:

.. code-block:: text
   :caption: *address_sanitizer_profile*
   :emphasize-lines: 10,12,13,14

    [settings]
    os=Macos
    os_build=Macos
    arch=x86_64
    arch_build=x86_64
    compiler=apple-clang
    compiler.version=10.0
    compiler.libcxx=libc++
    build_type=Release
    compiler.sanitizer=Address
    [env]
    CFLAGS=-fsanitize=address
    CXXFLAGS=-fsanitize=address
    LDFLAGS=-fsanitize=address

Then calling :command:`conan create . -pr address_sanitizer_profile` would inject
``-fsanitize=address`` to the build through the ``CFLAGS``, ``CXXFLAGS``, and ``LDFLAGS`` environment variables.

Managing sanitizer settings with the build system
#################################################

Another option is to make use of the information that is propagated to the *conan generator*. For
example, if we are using CMake we could use the information from the *CMakeLists.txt* to append
the flags to the compiler settings like this:

.. code-block:: cmake
   :caption: *CMakeLists.txt*

    cmake_minimum_required(VERSION 3.2)
    project(SanitizerExample)
    set (CMAKE_CXX_STANDARD 11)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
    set(SANITIZER ${CONAN_SETTINGS_COMPILER_SANITIZER})
    if(SANITIZER)
        if(SANITIZER MATCHES "(Address)")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address" )
        endif()
    endif()
    add_executable(sanit_example src/main.cpp)


The sanitizer setting is propagated to CMake as the ``CONAN_SETTINGS_COMPILER_SANITIZER`` variable
with a value equals to ``"Address"`` and we can set the behavior in CMake depending on the value of
the variable.


Using conan Hooks to set compiler environment variables
#######################################################

.. warning::

    This way of adding sanitizers is recommended just for testing purposes. In general, it's not a
    good practice to inject this in the environment using a Conan hook. It's much better explicitly
    defining this in the profiles.

.. important::

    Take into account that the package ID doesn't encode information about the environment,
    so different binaries due to different `CXX_FLAGS` would be considered by Conan as the same package.


If you are not interested in modelling the settings in the Conan package you can use a
Hook to modify the environment variable and apply the sanitizer
flags to the build. It could be something like:

.. code-block:: python
    :caption: *sanitizer_hook.py*

    import os


    class SanitizerHook(object):
        def __init__(self):
            self._old_cxx_flags = None

        def set_sanitize_address_flag(self):
            self._old_cxx_flags = os.environ.get("CXXFLAGS")
            flags_str = self._old_cxx_flags or ""
            os.environ["CXXFLAGS"] = flags_str + " -fsanitize=address"

        def reset_sanitize_address_flag(self):
            if self._old_cxx_flags is None:
                del os.environ["CXXFLAGS"]
            else:
                os.environ["CXXFLAGS"] = self._old_cxx_flags


    sanitizer = SanitizerHook()


    def pre_build(output, conanfile, **kwargs):
        sanitizer.set_sanitize_address_flag()


    def post_build(output, conanfile, **kwargs):
        sanitizer.reset_sanitize_address_flag()
