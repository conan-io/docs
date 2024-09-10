.. _example_cross_build_tricore:


Building packages for TriCore
=======================================

.. include:: ../../common/experimental_warning.inc


TriCore is an embedded microcontroller architecture used in multiple domains such as automotive.
There are multiple compilers for TriCore, some of which can be found `here
<https://www.infineon.com/cms/en/tools/aurix-tools/Compilers/>`__. There are also ``gcc``
implementations for TriCore; this is what we will be using in the examples on this page.

Since Conan 2.7 there is some built-in support for this architecture:

- The default ``settings.yml`` contains architectures: ``'tc131', 'tc16', 'tc161', 'tc162', 'tc18'``
- ``CMakeToolchain`` defines ``CMAKE_SYSTEM_NAME=Generic-ELF`` and ``CMAKE_SYSTEM_PROCESSOR=tricore`` for these architectures
- The compiler flags ``-m<architecture>"`` are injected as compiler and linker flags in ``CMakeToolchain`` and ``AutotoolsToolchain``

That means that it is possible to define a profile like:

.. code-block::
    :caption: tricore.profile

    [settings]
    os=baremetal
    arch=tc162
    compiler=gcc
    compiler.version=11
    compiler.cppstd=20
    compiler.libcxx=libstdc++11

    [options]
    *:fPIC=False
    *:shared=False

    [conf]
    tools.build:compiler_executables={"c":"tricore-elf-gcc","cpp":"tricore-elf-g++"}


This assumes the compiler is installed in the system path, and its executables are called ``tricore-elf-gcc`` and ``tricore-elf-g++``.
And then, cross-build and create a package for TriCore using this profile, for example the default ``cmake_lib``:

.. code-block:: bash

    $ conan new cmake_lib -d name=mypkg -d version=0.1
    $ conan create . -pr=tricore.profile


.. note::

    - This support is new and experimental. Please create a ticket in https://github.com/conan-io/conan/issues for any feedback or issues
    - Linking applications (like if using ``conan new cmake_exe``) requires a specific linker script, definition of entry-points, etc.
      Trying to build it as above will produce linking errors. We will try to add further examples for this case.
