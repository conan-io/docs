.. _examples-tools-use-different-toolchain-generator:

CMakeToolchain: Use a different generator with CMake
====================================================

In this example we are going to see how to use ``CMakeToolchain``, predefined generator like ``Ninja`` and how
to configure it to use a different generator.

Let's create a basic project based on the template ``cmake_exe`` as an example of a C++ project:

.. code:: bash

    $ conan new -d name=foo -d version=0.1.0 cmake_exe

CMake generators
----------------

CMake has a lot of `generators <https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html>`_
to generate the build system files. In case you want to use a different generator, and not the default one
chosen by CMake, you can use the configuration ``tools.cmake.cmaketoolchain:generator``.

To check what generators are available in your system, you can run:

.. code:: bash

    $ cmake --help

The configuration can be defined in your profile or directly in the command line, or even in your global configuration.


Generating the toolchain file with Ninja generator
--------------------------------------------------

The recipe from our project declares the generator "CMakeToolchain".

We can call :command:`conan create` to build our recipe. It will build our example using the default generator
chosen by CMake. In this case, it will be the default generator for the platform.

.. code:: bash

    $ conan create .

The may not be what we want, so we can define the generator we want to use. In this case, we will use the Ninja generator.

Using the Ninja generator in the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the Ninja generator, we can define the configuration in the command line:

.. code:: bash

    $ conan create . -c:a tools.cmake.cmaketoolchain:generator=Ninja


This configuration configuration will be passed to the ``conan_toolchain.cmake`` file, and the Ninja generator will be used.
When running the command, we will be able to find the following part in the output:

.. code:: bash

    Profile host:
    [settings]
    ...
    [conf]
    tools.cmake.cmaketoolchain:generator=Ninja

    ...
    foo/0.1.0: Calling build()
    foo/0.1.0: Running CMake.configure()
    foo/0.1.0: RUN: cmake -G "Ninja" ...

The build system files will be generated using the Ninja generator, as we defined in the command line.

Using the Ninja generator for any project using the profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the Ninja generator as default generator when running CMake, we can define the configuration in the profile:

.. code:: text

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

Then, we can build our project without defining the generator in the command line:

.. code:: bash

    $ conan create .

Now, the Ninja generator will be used by default when running CMake with default profile.


Using the Ninja generator for any project using the global configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the Ninja generator as default generator when running CMake,
we can define the configuration in the global configuration. The global configuration is located in the
``~/.conan2/global.conf`` file. If the file does not exist, you can create it.

.. code:: text

    *:tools.cmake.cmaketoolchain:generator=Ninja

Then, any profile will use the Ninja generator as default generator when running CMake.


Read More:

- ``CMakeToolchain`` :ref:`reference <conan_tools_cmaketoolchain>`
- Configuration pattern :ref:`reference <reference_config_files_global_conf_patterns>`
- Configuration in profiles :ref:`reference <reference_config_files_profiles_conf>`
