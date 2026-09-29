.. _examples_tools_meson_create_first_package:

Create your first Conan package with Meson
==========================================

In the :ref:`Create your first Conan package tutorial<creating_packages_create_your_first_conan_package>`
CMake was used as the build system. If you haven't read that section, read it first to familiarize
yourself with the ``conanfile.py`` and ``test_package`` concepts, then come back to read
about the specifics of the ``Meson`` package creation.

Use the :command:`conan new` command to create a "Hello World" C++ library example project:

.. code-block:: bash

    $ conan new meson_lib -d name=hello -d version=1.0


This will create a Conan package project with the following structure.

.. code-block:: text

  ├── conanfile.py
  ├── meson.build
  ├── hello.vcxproj
  ├── src
  │   ├── hello.h
  │   └── hello.cpp
  └── test_package
      ├── conanfile.py
      ├── meson.build
      └── src
          └── example.cpp


The structure and files are very similar to the previous CMake example:

- **conanfile.py**: On the root folder, there is a *conanfile.py* which is the main recipe
  file, responsible for defining how the package is built and consumed.
- **meson.build**: A Meson build script. This script doesn't need to contain anything Conan-specific,
  it is completely agnostic of Conan, because the integration is transparent.
- **src** folder: the folder that contains the simple C++ "hello" library.
- **test_package** folder: contains an *example* application that will require
  and link with the created package. In this case the ``test_package`` also contains a
  ``meson.build``, but it is possible to have the ``test_package`` using
  other build system as CMake if desired. It is not mandatory that the test_package is using
  the same build system as the package.

Let's have a look at the package recipe *conanfile.py* (only the relevant new parts):

.. code-block:: python

    exports_sources = "meson.build", "src/*"

    def layout(self):
        basic_layout(self)

    def generate(self):
        tc = MesonToolchain(self)
        tc.generate()

    def build(self):
        meson = Meson(self)
        meson.configure()
        meson.build()

    def package(self):
        meson = Meson(self)
        meson.install()

Let's explain the different sections of the recipe briefly:

- The ``layout()`` defines a ``basic_layout()``, this is less flexible than a CMake one, so it
  doesn't allow any parametrization.
- The ``generate()`` method calls ``MesonToolchain`` that can generate ``conan_meson_native.ini``
  and ``conan_meson_cross.ini`` Meson toolchain files for cross builds. If the project had dependencies
  with Conan ``requires``, it should add ``PkgConfigDeps`` too
- The ``build()`` method uses the ``Meson()`` helper to drive the build
- The ``package()`` method uses the ``Meson`` install functionality to define and copy to the package 
  folder the final artifacts.


The **test_package** folder also contains a ``meson.build`` file that declares a dependency to
the tested package, and links an application, to verify the package was correctly created and contains
that library:

.. code-block:: 
  :caption: test_package/meson.build

  project('Testhello', 'cpp')
  hello = dependency('hello', version : '>=0.1')
  executable('example', 'src/example.cpp', dependencies: hello)


Note the ``test_package/conanfile.py`` contains also a ``generators = "PkgConfigDeps", "MesonToolchain"``,
because the ``test_package`` has the "hello" package as dependency, and ``PkgConfigDeps`` is necessary to
locate it.

.. note:: 

  This example assumes Meson, Ninja and PkgConfig are installed in the system, which might not always be the case.
  If they are not, you can create a profile ``myprofile`` with:

  .. code-block::

    include(default)
    
    [tool_requires]
    meson/[*]
    pkgconf/[*]

We added `Meson` and `pkg-config` as :ref:`tool requirements to the profile <reference_config_files_profiles_tool_requires>`. By executing ``conan create . -pr=myprofile``, those tools will be installed and made available during the package's build process.


Let's build the package from sources with the current default configuration, and then let
the ``test_package`` folder test the package:

.. code-block:: bash

    $ conan create .
    
    ...
    ======== Testing the package: Executing test ========
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: .\example
    hello/1.0: Hello World Release!
      hello/1.0: _M_X64 defined
      hello/1.0: MSVC runtime: MultiThreadedDLL
      hello/1.0: _MSC_VER1939
      hello/1.0: _MSVC_LANG201402
      hello/1.0: __cplusplus201402
    hello/1.0 test_package


We can now validate that the recipe and the package binary are in the cache:


.. code-block:: bash

    $ conan list "hello/1.0:*"
    Local Cache:
      hello
        hello/1.0
          revisions
            856c535669f78da11502a119b7d8a6c9 (2024-03-04 17:52:39 UTC)
              packages
                c13a22a41ecd72caf9e556f68b406569547e0861
                  info
                    settings
                      arch: x86_64                  
                      build_type: Release           
                      compiler: msvc                
                      compiler.cppstd: 14           
                      compiler.runtime: dynamic     
                      compiler.runtime_type: Release
                      compiler.version: 193         
                      os: Windows                   
         

.. seealso::

    - :ref:`Meson built-in integrations reference<conan_tools_meson>`.
    - :ref:`PkgConfigDeps built-in integrations reference<conan_tools_gnu_pkgconfigdeps>`.
