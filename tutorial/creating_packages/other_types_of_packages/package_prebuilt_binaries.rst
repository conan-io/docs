.. _creating_packages_other_prebuilt:

Package prebuilt binaries
=========================

There are specific scenarios in which it is necessary to create packages from existing binaries, for example from 3rd
parties or binaries previously built by another process or team that is not using Conan. Under these circumstances,
building from sources is not what you want.

You can package the local files in the following scenarios:

 1. When you are developing your package locally and you want to quickly create a package with the built artifacts, but as you don't want to rebuild again (clean copy) your artifacts, you don't want to call
    :command:`conan create`. This method will keep your local project build if you are using an IDE.
 2. When you cannot build the packages from sources (when only pre-built binaries are available) and you have them
    in a local directory.
 3. Same as 2 but you have the precompiled libraries in a remote repository.


Locally building binaries
-------------------------

Use the :command:`conan new` command to create a "Hello World" C++ library example project:

.. code-block:: bash

    $ conan new cmake_lib -d name=hello -d version=1.0


This will create a Conan package project with the following structure.

.. code-block:: text

  .
  ├── CMakeLists.txt
  ├── conanfile.py
  ├── include
  │   └── hello.h
  ├── src
  │   └── hello.cpp
  └── test_package
      ├── CMakeLists.txt
      ├── conanfile.py
      └── src
          └── example.cpp


We have a ``CMakeLists.txt`` file in the root, an ``src`` folder with the ``cpp`` files and, an ``include``
folder for the headers.

They also have a ``test_package/`` folder to test that the exported package is working correctly.

Now, for every different configuration (different compilers, architectures, build_type...):

1. We call :command:`conan install` to generate the ``conan_toolchain.cmake`` file and the ``CMakeUserPresets.json``
   that can be used in our IDE or calling CMake (only >= 3.23).

   .. code-block:: bash

       $ conan install . -s build_type=Release

2. We build our project calling CMake, our IDE, ... etc:

   .. code-block:: bash
       :caption: Linux, macOS

       $ mkdir -p build/Release
       $ cd build/Release
       $ cmake ../.. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=../Release/generators/conan_toolchain.cmake
       $ cmake --build .


   .. code-block:: bash
       :caption: Windows

       $ mkdir -p build
       $ cd build
       $ cmake ..  -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake
       $ cmake --build . --config Release


   .. note::

         As we are directly using our IDE or CMake to build the library, the ``build()`` method of the recipe
         is never called and could be removed.

3. We call :command:`conan export-pkg` to package the built artifacts.

   .. code-block:: bash

       $ cd ../..
       $ conan export-pkg . -s build_type=Release
       ...
       hello/0.1: Calling package()
       hello/0.1 package(): Packaged 1 '.h' file: hello.h
       hello/0.1 package(): Packaged 1 '.a' file: libhello.a
       ...
       hello/0.1: Package '54a3ab9b777a90a13e500dd311d9cd70316e9d55' created


   Let's deep a bit more in the package method. The generated ``package()`` method is using ``cmake.install()`` to copy
   the artifacts from our local folders to the Conan package.

   There is an alternative and generic ``package()`` method that could be used for any build system:

   .. code-block:: python

         def package(self):
             local_include_folder = os.path.join(self.source_folder, self.cpp.source.includedirs[0])
             local_lib_folder = os.path.join(self.build_folder, self.cpp.build.libdirs[0])
             copy(self, "*.h", local_include_folder, os.path.join(self.package_folder, "include"), keep_path=False)
             copy(self, "*.lib", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=False)
             copy(self, "*.a", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=False)

   This  ``package()`` method is copying artifacts from the following directories that, thanks to the layout(), will always
   point to the correct places:

   - **os.path.join(self.source_folder, self.cpp.source.includedirs[0])** will always point to our local include folder.
   - **os.path.join(self.build_folder, self.cpp.build.libdirs[0])** will always point to the location of the libraries when
     they are built, no matter if using a single-config CMake Generator or a multi-config one.

4. We can test the built package calling :command:`conan test`:

   .. code-block:: bash

       $ conan test test_package/conanfile.py hello/0.1 -s build_type=Release

       -------- Testing the package: Running test() ----------
       hello/0.1 (test package): Running test()
       hello/0.1 (test package): RUN: ./example
       hello/0.1: Hello World Release!
         hello/0.1: __x86_64__ defined
         hello/0.1: __cplusplus199711
         hello/0.1: __GNUC__4
         hello/0.1: __GNUC_MINOR__2
         hello/0.1: __clang_major__13
         hello/0.1: __clang_minor__1
         hello/0.1: __apple_build_version__13160021


Now you can try to generate a binary package for ``build_type=Debug`` running the same steps but changing the ``build_type``.
You can repeat this process any number of times for different configurations.


Packaging already Pre-built Binaries
------------------------------------

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/other_packages/prebuilt_binaries

This is an example of scenario 2 explained in the introduction. If you have a local folder containing the binaries
for different configurations you can package them using the following approach.


These are the files of our example, (be aware that the library files are only empty files so not valid libraries):

.. code-block:: text

    .
    ├── conanfile.py
    └── vendor_hello_library
        ├── linux
        │   ├── armv8
        │   │   ├── include
        │   │   │   └── hello.h
        │   │   └── libhello.a
        │   └── x86_64
        │       ├── include
        │       │   └── hello.h
        │       └── libhello.a
        ├── macos
        │   ├── armv8
        │   │   ├── include
        │   │   │   └── hello.h
        │   │   └── libhello.a
        │   └── x86_64
        │       ├── include
        │       │   └── hello.h
        │       └── libhello.a
        └── windows
            ├── armv8
            │   ├── hello.lib
            │   └── include
            │       └── hello.h
            └── x86_64
                ├── hello.lib
                └── include
                    └── hello.h


We have folders with ``os`` and subfolders with ``arch``. This the recipe of our example:


.. code-block:: python

      import os
      from conan import ConanFile
      from conan.tools.files import copy


      class helloRecipe(ConanFile):
          name = "hello"
          version = "0.1"
          settings = "os", "arch"

          def layout(self):
              _os = str(self.settings.os).lower()
              _arch = str(self.settings.arch).lower()
              self.folders.build = os.path.join("vendor_hello_library", _os, _arch)
              self.folders.source = self.folders.build
              self.cpp.source.includedirs = ["include"]
              self.cpp.build.libdirs = ["."]

          def package(self):
              local_include_folder = os.path.join(self.source_folder, self.cpp.source.includedirs[0])
              local_lib_folder = os.path.join(self.build_folder, self.cpp.build.libdirs[0])
              copy(self, "*.h", local_include_folder, os.path.join(self.package_folder, "include"), keep_path=False)
              copy(self, "*.lib", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=False)
              copy(self, "*.a", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=False)

          def package_info(self):
              self.cpp_info.libs = ["hello"]



- We are not building anything, so the ``build`` method is not useful here.
- We can keep the same ``package`` method from the previous example because the location of the artifacts is
  declared by the ``layout()``.
- Both the source folder (with headers) and the build folder (with libraries) are in the same location, in a path that follows:

        ``vendor_hello_library/{os}/{arch}``

- The headers are in the ``include`` subfolder of the ``self.source_folder`` (we declare it in ``self.cpp.source.includedirs``).
- The libraries are in the root of the ``self.build_folder`` folder (we declare ``self.cpp.build.libdirs = ["."]``).
- We removed the ``compiler`` and the ``build_type`` because we only have different libraries depending on the operating
  system and the architecture (it might be a pure C library).


Now, for each different configuration we call :command:`conan export-pkg` command, later we can list the binaries
so we can check we have one package for each precompiled library:

    .. code-block:: bash

        $ conan export-pkg . -s os="Linux" -s arch="x86_64"
        $ conan export-pkg . -s os="Linux" -s arch="armv8"
        $ conan export-pkg . -s os="Macos" -s arch="x86_64"
        $ conan export-pkg . -s os="Macos" -s arch="armv8"
        $ conan export-pkg . -s os="Windows" -s arch="x86_64"
        $ conan export-pkg . -s os="Windows" -s arch="armv8"

        $ conan list "hello/0.1#:*"
        Local Cache
          hello
            hello/0.1
              revisions
                9c7634dfe0369907f569c4e583f9bc50 (2024-05-10 08:28:31 UTC)
                  packages
                    522dcea5982a3f8a5b624c16477e47195da2f84f
                      info
                        settings
                          arch: x86_64
                          os: Windows
                    63fead0844576fc02943e16909f08fcdddd6f44b
                      info
                        settings
                          arch: x86_64
                          os: Linux
                    82339cc4d6db7990c1830d274cd12e7c91ab18a1
                      info
                        settings
                          arch: x86_64
                          os: Macos
                    a0cd51c51fe9010370187244af885b0efcc5b69b
                      info
                        settings
                          arch: armv8
                          os: Windows
                    c93719558cf197f1df5a7f1d071093e26f0e44a0
                      info
                        settings
                          arch: armv8
                          os: Linux
                    dcf68e932572755309a5f69f3cee1bede410e907
                      info
                        settings
                          arch: armv8
                          os: Macos


In this example, we don't have a ``test_package/`` folder but you can provide one to test the packages like in the
previous example.


Downloading and Packaging Pre-built Binaries
--------------------------------------------

This is an example of scenario 3 explained in the introduction. If we are not building the libraries we likely
have them somewhere in a remote repository. In this case, creating a complete Conan recipe, with the detailed
retrieval of the binaries could be the preferred method, because it is reproducible, and the original binaries might be traced.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/other_packages/prebuilt_remote_binaries


.. code-block:: python
   :caption: conanfile.py


      import os
      from conan.tools.files import get, copy
      from conan import ConanFile


      class HelloConan(ConanFile):
          name = "hello"
          version = "0.1"
          settings = "os", "arch"

          def build(self):
              base_url = "https://github.com/conan-io/libhello/releases/download/0.0.1/"

              _os = {"Windows": "win", "Linux": "linux", "Macos": "macos"}.get(str(self.settings.os))
              _arch = str(self.settings.arch).lower()
              url = "{}/{}_{}.tgz".format(base_url, _os, _arch)
              get(self, url)

          def package(self):
              copy(self, "*.h", self.build_folder, os.path.join(self.package_folder, "include"))
              copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))
              copy(self, "*.a", self.build_folder, os.path.join(self.package_folder, "lib"))

          def package_info(self):
              self.cpp_info.libs = ["hello"]


Typically, pre-compiled binaries come for different configurations, so the only task that the
``build()`` method has to implement is to map the ``settings`` to the different URLs.

We only need to call :command:`conan create` with different settings to generate the needed packages:


    .. code-block:: bash

        $ conan create . -s os="Linux" -s arch="x86_64"
        $ conan create . -s os="Linux" -s arch="armv8"
        $ conan create . -s os="Macos" -s arch="x86_64"
        $ conan create . -s os="Macos" -s arch="armv8"
        $ conan create . -s os="Windows" -s arch="x86_64"
        $ conan create . -s os="Windows" -s arch="armv8"

        $ conan list "hello/0.1#:*"
        Local Cache
          hello
            hello/0.1
              revisions
                d8e4debf31f0b7b5ec7ff910f76f1e2a (2024-05-10 09:13:16 UTC)
                  packages
                    522dcea5982a3f8a5b624c16477e47195da2f84f
                      info
                        settings
                          arch: x86_64
                          os: Windows
                    63fead0844576fc02943e16909f08fcdddd6f44b
                      info
                        settings
                          arch: x86_64
                          os: Linux
                    82339cc4d6db7990c1830d274cd12e7c91ab18a1
                      info
                        settings
                          arch: x86_64
                          os: Macos
                    a0cd51c51fe9010370187244af885b0efcc5b69b
                      info
                        settings
                          arch: armv8
                          os: Windows
                    c93719558cf197f1df5a7f1d071093e26f0e44a0
                      info
                        settings
                          arch: armv8
                          os: Linux
                    dcf68e932572755309a5f69f3cee1bede410e907
                      info
                        settings
                          arch: armv8
                          os: Macos

It is recommended to include also a small consuming project in a ``test_package`` folder to verify the package is correctly
built, and then upload it to a Conan remote with :command:`conan upload`.

The same building policies apply. Having a recipe fails if no Conan packages are
created, and the :command:`--build` argument is not defined. A typical approach for this kind of
package could be to define a :command:`build_policy="missing"`, especially if the URLs are also
under the team's control. If they are external (on the internet), it could be better to create the
packages and store them on your own Conan repository, so that the builds do not rely on third-party URLs
being available.
