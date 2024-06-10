
.. _examples-tools-use-different-toolchain-generator:

Using CMakeToolchain with Different Generators: Ninja Example
=============================================================

This guide demonstrates how to use ``CMakeToolchain`` with predefined generators like ``Ninja`` and how to configure it to use different generators.

Creating a Basic Project
-------------------------
We will create a basic project based on the ``cmake_exe`` template as an example of a C++ project:

.. code-block:: bash

    $ conan new -d name=foo -d version=0.1.0 cmake_exe

Understanding CMake Generators
------------------------------
CMake offers a variety of `generators <https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html>`_ to create build system files. If you want to use a generator other than the default chosen by CMake, you can configure ``tools.cmake.cmaketoolchain:generator``.

To see which generators are available on your system, run:

.. code-block:: bash

    $ cmake --help

You can set this configuration in your profile, directly in the command line, or even in your global configuration.

Generating the Toolchain File with the Ninja Generator
------------------------------------------------------
The project's recipe declares the "CMakeToolchain" generator.

1. **Default Build**: To build the recipe using the default generator chosen by CMake, run:

    .. code-block:: bash

        $ conan create .

2. **Specifying the Ninja Generator**: If you prefer to use the Ninja generator, specify it in the command line:

    .. code-block:: bash

        $ conan create . -c tools.cmake.cmaketoolchain:generator=Ninja

    This configuration will be passed to the ``conan_toolchain.cmake`` file, and the Ninja generator will be used. You should see the following output snippet indicating the Ninja generator is being used:

    .. code-block:: bash

        Profile host:
        [settings]
        ...
        [conf]
        tools.cmake.cmaketoolchain:generator=Ninja

        ...
        foo/0.1.0: Calling build()
        foo/0.1.0: Running CMake.configure()
        foo/0.1.0: RUN: cmake -G "Ninja" ...

Using the Ninja Generator by Default in a Profile
-------------------------------------------------

To set the Ninja generator as the default in a profile,
add the entry ``[conf]`` to your profile with the generator value:

.. code-block:: text

    [settings]
    os=Linux
    arch=x86_64
    compiler=gcc
    compiler.version=13
    compiler.libcxx=libstdc++11
    compiler.cppstd=20
    build_type=Release

    [conf]
    *:tools.cmake.cmaketoolchain:generator=Ninja

Now, you can build your project without specifying the generator in the command line:

.. code-block:: bash

    $ conan create .

The Ninja generator will be used by default when running CMake with this profile.

Setting the Ninja Generator Globally
------------------------------------
To set the Ninja generator as the default globally, add the following to your global configuration file located at ``~/.conan2/global.conf``. If the file does not exist, create it:

.. code-block:: text

    *:tools.cmake.cmaketoolchain:generator=Ninja

With this setting, any profile will use the Ninja generator as the default when running CMake.

Conclusion
----------
This guide showed you how to configure `CMakeToolchain` to use different generators, specifically the Ninja generator, through the command line, profile configuration, and global settings. For more details, refer to the following resources:

- ``CMakeToolchain`` :ref:`reference <conan_tools_cmaketoolchain>`
- Configuration pattern :ref:`reference <reference_config_files_global_conf_patterns>`
- Configuration in profiles :ref:`reference <reference_config_files_profiles_conf>`
