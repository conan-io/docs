.. _examples_tools_microsoft_create_first_package:

Create your first Conan package with Visual Studio/MSBuild
==========================================================

In the :ref:`Create your first Conan package tutorial<creating_packages_create_your_first_conan_package>`
CMake was used as the build system. If you haven't read that section, read it first to familiarize
yourself with the ``conanfile.py`` and ``test_package`` concepts, then come back to read
about the specifics of the ``Visual Studio`` package creation.

Use the :command:`conan new` command to create a "Hello World" C++ library example project:

.. code-block:: bash

    $ conan new msbuild_lib -d name=hello -d version=1.0


This will create a Conan package project with the following structure.

.. code-block:: text

  .
  ├── conanfile.py
  ├── hello.sln
  ├── hello.vcxproj
  ├── include
  │   └── hello.h
  ├── src
  │   └── hello.cpp
  └── test_package
      ├── conanfile.py
      ├── test_hello.sln
      ├── test_hello.vcxproj
      └── src
          └── test_hello.cpp

The structure and files are very similar to the previous CMake example:

- **conanfile.py**: On the root folder, there is a *conanfile.py* which is the main recipe
  file, responsible for defining how the package is built and consumed.
- **hello.sln**: A Visual Studio solution file that can be opened with the IDE.
- **hello.vcxproj**: A Visual Studio C/C++ project, part of the solution above.
- **src** and **include** folders: the folders that contains the simple C++ "hello" library.
- **test_package** folder: contains an *example* application that will require
  and link with the created package. In this case the ``test_package`` also contains a
  Visual Studio solution and project, but it is possible to have the ``test_package`` using
  other build system as CMake if desired. It is not mandatory that the test_package is using
  the same build system as the package.

Let's have a look at the package recipe *conanfile.py* (only the relevant new parts):

.. code-block:: python

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "hello.sln", "hello.vcxproj", "src/*", "include/*"

    def layout(self):
        vs_layout(self)

    def generate(self):
        tc = MSBuildToolchain(self)
        tc.generate()

    def build(self):
        msbuild = MSBuild(self)
        msbuild.build("hello.sln")

    def package(self):
        copy(self, "*.h", os.path.join(self.source_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))
        copy(self, "*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"),
             keep_path=False)


Let's explain the different sections of the recipe briefly:

- Note there are no ``options`` like the ``shared`` option in this recipe. The current project
  always builds a static library, so it is not optional.
- The ``layout()`` defines a typical VS layout, this is less flexible than a CMake one, so it
  doesn't allow any parametrization.
- The ``generate()`` method calls ``MSBuildToolchain`` to generate a ``conantoolchain.props`` 
  file, that the project must add to its properties. If the project had dependencies with Conan
  ``requires``, it should add ``MSBuildDeps`` too and add the relevant generated files property
  sheets.
- The ``build()`` method uses the ``MSBuild()`` helper to drive the build of the solution
- As the project doesn't have any "install" functionality in the build scripts, the ``package()``
  method can manually define which files must be copied.

The ``hello.vcxproj`` project file adds the generated property sheets like ``conantoolchain.props``
to the project, so the build can receive the Conan input ``settings`` and act accordingly.

.. code-block:: xml
   :caption: hello.vcxproj

    <ImportGroup Label="PropertySheets">
      <Import Project="conan\conantoolchain.props" />
    </ImportGroup>

If the project had dependencies, it should add the dependencies generated ``.props`` files too.


The **test_package** folder also contains a ``test_hello.vcxproj`` file, that includes both the
toolchain and the dependencies property sheets:

.. code-block:: xml
  :caption: test_package/test_hello.vcxproj

  <ImportGroup Label="PropertySheets">
      <Import Project="conan\conantoolchain.props" />
      <Import Project="conan\conandeps.props" />
  </ImportGroup>


Note the ``test_package/conanfile.py`` contains also a ``generators="MSBuildDeps"``.

Let's build the package from sources with the current default configuration, and then let
the ``test_package`` folder test the package:

.. code-block:: bash

    $ conan create .
    
    ...
    ======== Testing the package: Executing test ========
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: x64\Release\test_hello
    hello/1.0: Hello World Release!
      hello/1.0: _M_X64 defined
      hello/1.0: MSVC runtime: MultiThreadedDLL
      hello/1.0: _MSC_VER1939
      hello/1.0: _MSVC_LANG201402
      hello/1.0: __cplusplus199711
    hello/1.0 test_package


We can now validate that the recipe and the package binary are in the cache:


.. code-block:: bash

    $ conan list hello/1.0:*
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

    - :ref:`MSBuild built-in integrations reference<conan_tools_microsoft>`.

