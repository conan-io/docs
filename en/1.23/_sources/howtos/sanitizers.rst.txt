.. _sanitizers:

Compiler sanitizers
===================

Sanitizers are tools that can detect bugs such as buffer overflows or accesses, dangling pointer or
different types of undefined behavior.

The two compilers that mainly support sanitizing options are gcc and clang. These options are
passed to the compiler as flags and, depending on if you are using
`clang <https://clang.llvm.org/docs/UsersManual.html#controlling-code-generation>`_ or
`gcc <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_, different sanitizers are
supported.

Here we explain different options on how to model and use sanitizers with your Conan packages.

Adding custom settings
----------------------

If you want to model the sanitizer options so that the package id is affected by them, you have to
introduce new settings in the *settings.yml* file (see :ref:`custom_settings` section for more
information).

Sanitizer options should be modeled as sub-settings of the compiler. Depending on how you want to
combine the sanitizers you have two choices.

Adding a list of commonly used values
######################################

If you have a fixed set of sanitizers or combinations of them that are the ones you usually set for
your builds you can add the sanitizers as a list of values. An example for *apple-clang* would be
like this:

.. code-block:: yaml
    :caption: *settings.yml*
    :emphasize-lines: 6
    
    apple-clang:
        version: ["5.0", "5.1", "6.0", "6.1", "7.0", "7.3", "8.0", "8.1", 
                  "9.0", "9.1", "10.0", "11.0"]
        libcxx: [libstdc++, libc++]
        cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20]
        sanitizer: [None, Address, Thread, Memory, UndefinedBehavior, AddressUndefinedBehavior]

Here you have modeled the use of ``-fsanitize=address``, ``-fsanitize=thread``,
``-fsanitize=memory``, ``-fsanitize=undefined`` and the combination of ``-fsanitize=address`` and
``-fsanitize=undefined``. Note that for example, for clang it is not possible to combine more than
one of the ``-fsanitize=address``, ``-fsanitize=thread``, and ``-fsanitize=memory`` checkers in the
same program.

Adding thread sanitizer for a :command:`conan install`, in this case, could be done by calling
:command:`conan install .. -s compiler.sanitizer=Thread`

Adding different values to combine
###################################

Another option would be to add the sanitizer values as multiple ``True`` or ``None`` fields so that
they can be freely combined later. An example of that for the previous sanitizer options would be as
follows:

.. code-block:: yaml
    :caption: *settings.yml*
    :emphasize-lines: 6,7,8

    apple-clang:
        version: ["5.0", "5.1", "6.0", "6.1", "7.0", "7.3", "8.0", 
                  "8.1", "9.0", "9.1", "10.0", "11.0"]
        libcxx: [libstdc++, libc++]
        cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20]
        address_sanitizer: [None, True]
        thread_sanitizer: [None, True]
        undefined_sanitizer: [None, True]

Then, you can add different sanitizers calling, for example, to :command:`conan install ..
-s compiler.address_sanitizer=True -s compiler.undefined_sanitizer=True`

A drawback of this approach is that not all the combinations will be valid or will make sense, but it
is up to the consumer to use it correctly.

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
   :emphasize-lines: 10,12,13

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
    CXXFLAGS=-fsanitize=address
    CFLAGS=-fsanitize=address

Then calling to :command:`conan create . -pr address_sanitizer_profile` would inject
``-fsanitize=address`` to the build through the ``CXXFLAGS`` environment variable.

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

.. important::

    Take into account that the package ID doesn't encode information about the environment,
    so different binaries due to different `CXX_FLAGS` would be considered by Conan as the same package.


If you are not interested in modelling the settings in the Conan package you can use a
:ref:`Hook <hooks_reference>` to modify the environment variable and apply the sanitizer
flags to the build. It could be something like:

.. code-block:: python
    :caption: *sanitizer_hook.py*

    def set_sanitize_address_flag(self):
        self._old_cxx_flags = os.environ.get("CXXFLAGS")
        os.environ["SOURCE_DATE_EPOCH"] = _old_flags + " -fsanitize=address"

    def reset_sanitize_address_flag(self):
        if self._old_cxx_flags is None:
            del os.environ["CXXFLAGS"]
        else:
            os.environ["CXXFLAGS"] = self._old_cxx_flags

And then calling those functions from a *pre_build* and a *post_build* hook:

.. code-block:: python
    :caption: *sanitizer_hook.py*

    def pre_build(output, conanfile, **kwargs):
        set_sanitize_address_flag()

    def post_build(output, conanfile, **kwargs):
        reset_sanitize_address_flag()
