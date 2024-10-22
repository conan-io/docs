.. _examples_tools_autotools_create_first_package:

Create your first Conan package with Autotools
==============================================

.. warning::

  This example will only work for Linux and OSX environments and does not support Windows directly, including msys2/cygwin subsystems.
  However, Windows Subsystem for Linux (WSL) should work since it provides a Linux environment. While Conan offers `win_bash = True` 
  for some level of support in Windows environments with Autotools, it's not applicable in this tutorial.


In the :ref:`Create your first Conan package tutorial<creating_packages_create_your_first_conan_package>`
CMake was used as the build system. If you haven't read that section, read it first to familiarize
yourself with the ``conanfile.py`` and ``test_package`` concepts, then come back to read
about the specifics of the ``Autotools`` package creation.

Use the :command:`conan new` command to create a "Hello World" C++ library example project:

.. code-block:: bash

    $ conan new autotools_lib -d name=hello -d version=0.1


This will create a Conan package project with the following structure.

.. code-block:: text

  ├── conanfile.py
  ├── configure.ac
  ├── Makefile.am
  ├── src
  │   ├── hello.h
  │   ├── hello.cpp
  │   └── Makefile.am
  └── test_package
      ├── conanfile.py
      ├── configure.ac
      ├── mainc.pp
      └── Makefile.am


The structure and files are very similar to the previous CMake example:

- **conanfile.py**: On the root folder, there is a *conanfile.py* which is the main recipe
  file, responsible for defining how the package is built and consumed.
- **configure.ac**: An autotools configuration script, that contains the necessary macros
  and references the ``Makefiles`` it needs to configure.
- **Makefile.am**: A Makefile configuration file, defining only ``SUBDIRS = src``
- **src** folder: the folder that contains the simple C++ "hello" library.
- **src/Makefile.am**: Makefile configuration file containing the library definition and source files
  like ``libhello_la_SOURCES = hello.cpp hello.h``
- **test_package** folder: contains an *example* application that will require
  and link with the created package. In this case the ``test_package`` also contains an autotools
  project, but it is possible to have the ``test_package`` using
  other build system as CMake if desired. It is not mandatory that the test_package is using
  the same build system as the package.

Let's have a look at the package recipe *conanfile.py* (only the relevant new parts):

.. code-block:: python

    exports_sources = "configure.ac", "Makefile.am", "src/*"

    def layout(self):
        basic_layout(self)

    def generate(self):
        at_toolchain = AutotoolsToolchain(self)
        at_toolchain.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.autoreconf()
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()
        fix_apple_shared_install_name(self)

Let's explain the different sections of the recipe briefly:

- The ``layout()`` defines a ``basic_layout()``, this is less flexible than a CMake one, so it
  doesn't allow any parametrization.
- The ``generate()`` method calls ``AutotoolsToolchain`` that can generate a ``conanautotoolstoolchain``
  environment script defining environment variables like ``CXXFLAGS`` or ``LDFLAGS`` that will be used
  by the ``Makefiles`` to map the Conan input settings into compile flags. If the project had dependencies
  with Conan ``requires``, it should add ``PkgConfigDeps`` too
- The ``build()`` method uses the ``Autotools()`` helper to drive the build, calling the different configure
  and build steps.
- The ``package()`` method uses the ``Autotools`` install functionality to define and copy to the package 
  folder the final artifacts. Note the template also includes a call to ``fix_apple_shared_install_name()``
  that uses OSX *install_name_tool* utility to set ``@rpath``to fix the ``LC_ID_DYLIB`` and ``LC_LOAD_DYLIB``
  fields on Apple dylibs, because it is very unusual that autotools project will manage to do this (CMake can do it) .


Let's build the package from sources with the current default configuration, and then let
the ``test_package`` folder test the package:

.. code-block:: bash

    $ conan create .

    ...
    ======== Testing the package: Executing test ========
    hello/0.1 (test package): Running test()
    hello/0.1 (test package): RUN: ./main
    hello/0.1: Hello World Release!
      hello/0.1: __x86_64__ defined
      hello/0.1: _GLIBCXX_USE_CXX11_ABI 1
      hello/0.1: __cplusplus201703
      hello/0.1: __GNUC__11
      hello/0.1: __GNUC_MINOR__1
    hello/0.1 test_package


We can now validate that the recipe and the package binary are in the cache:


.. code-block:: bash

    $ conan list hello/1.0:*
    Local Cache:
      hello
        hello/1.0
          revisions
            5b151b3f08144bf25131266eb306ddff (2024-03-06 12:03:52 UTC)
              packages
                8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe
                  info
                    settings
                      arch: x86_64
                      build_type: Release
                      compiler: gcc
                      compiler.cppstd: gnu17
                      compiler.libcxx: libstdc++11
                      compiler.version: 11
                      os: Linux
                    options
                      fPIC: True
                      shared: False


.. seealso::

    - :ref:`GNU built-in integrations reference<conan_tools_gnu>`.
