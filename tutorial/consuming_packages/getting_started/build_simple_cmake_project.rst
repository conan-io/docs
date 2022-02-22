.. _consuming_packages_getting_started_build_simple_cmake_project:

Build a simple CMake project using Conan
========================================

Let's get started with an example: We are going to create a string compressor application
that uses one of the most popular C++ libraries: `Zlib <https://zlib.net/>`__.

.. important::

    In this example, we will retreive the zlib Conan package from a Conan repository with
    packages compatible for Conan 2.0. To run this example succesfully you should add this
    remote to your Conan configuration doing:
    ``conan remote add conanv2 https://conanv2.jfrog.io/artifactory/api/conan/conan --index 0``

We'll use CMake as build system in this case but keep in mind that Conan **works with any
build system** and is not limited to using CMake. You can check more examples with other
build systems in the :ref:`Read More
section<consuming_packages_getting_started_read_more>`.

.. note::

    The source files to recreate this project are available in the `examples2.0 repository
    <https://github.com/conan-io/examples2>`_ in GitHub. You can skip the manual
    creation of the folder and sources with this command:

    .. code-block:: bash

        $ git clone https://github.com/conan-io/examples2.git
        $ cd tutorial/consumer/getting_started

1. We start from a very simple C language project with this structure:

.. code-block:: text

    .
    ├── CMakeLists.txt
    └── src
        └── main.c

This project contains a basic *CMakeLists.txt* including the **zlib** dependency and the
source code for the string compressor program in *main.c*.

Let's have a look at the *main.c* file:

.. code-block:: cpp
    :caption: **main.c**

    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>

    #include <zlib.h>

    int main(void) {
        char buffer_in [32] = {"Conan Package Manager"};
        char buffer_out [32] = {0};

        z_stream defstream;
        defstream.zalloc = Z_NULL;
        defstream.zfree = Z_NULL;
        defstream.opaque = Z_NULL;
        defstream.avail_in = (uInt) strlen(buffer_in);
        defstream.next_in = (Bytef *) buffer_in;
        defstream.avail_out = (uInt) sizeof(buffer_out);
        defstream.next_out = (Bytef *) buffer_out;

        deflateInit(&defstream, Z_BEST_COMPRESSION);
        deflate(&defstream, Z_FINISH);
        deflateEnd(&defstream);

        printf("Compressed size is: %lu\n", strlen(buffer_in));
        printf("Compressed string is: %s\n", buffer_in);
        printf("Compressed size is: %lu\n", strlen(buffer_out));
        printf("Compressed string is: %s\n", buffer_out);

        printf("ZLIB VERSION: %s\n", zlibVersion());

        return EXIT_SUCCESS;
    }

Also, the contents of *CMakeLists.txt* are:

.. code-block:: cmake
    :caption: **CMakeLists.txt**

    cmake_minimum_required(VERSION 3.15)
    project(compressor C)

    find_package(ZLIB REQUIRED)

    add_executable(${PROJECT_NAME} main.c)
    target_link_libraries(${PROJECT_NAME} ZLIB::ZLIB)

Our application relies on the **Zlib** library. Conan, by default, tries to install
libraries from a remote server called `Conan Center Index <https://conan.io/center/>`_.
You can search there for libraries and also check the available versions. In our case, 
after checking the available versions for `Zlib <https://conan.io/center/zlib>`__ we
choose to use the latest available version: **zlib/1.2.11**.

3. The easiest way to install the **Zlib** library and find it from our project with Conan is
   using a *conanfile.txt* file. Let's create one with the following content:

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    zlib/1.2.11

    [generators]
    CMakeDeps
    CMakeToolchain

As you can see we added two sections to this file with a syntax similar to an *INI* file.

    * **[requires]** section is where we declare the libraries we want to use in the
      project, in this case **zlib/1.2.11**.

    * **[generators]** section tells Conan to generate the files that the compilers
      or build systems will use to find the dependencies and build the project. In this
      case, as our project is based in *CMake*, we will use *CMakeDeps* to generate information
      about where the **Zlib** library files are installed and *CMakeToolchain* to pass build
      information to *CMake* using a *CMake* toolchain file.

4. Besides the *conanfile.txt*, we need a **Conan profile** to build our project. Conan
   profiles allows users to define a configuration set for things like compiler, build
   configuration, architecture, shared or static libraries, etc. Conan, by default, will
   not try to detect a profile automatically, so we need to create one. To let Conan try
   to guess the profile, based on the current operating system and installed tools, please
   run:

.. code-block:: bash

    conan profile detect --force

This will detect the operating system, build architecture and compiler settings based on
the environent. It will also set the build configuration as *Release* by default. The
generated profile will be stored in the Conan home folder with name *default* and will be
used by Conan in all commands by default unless other profile is specified via the command
line. After executing the command you should see some output similar to this but for your
configuration:

.. code-block:: ini

    $ conan profile detect --force
    Found apple-clang 13.0    
    Detected profile:
    [settings]
    os=Macos
    arch=x86_64
    compiler=apple-clang
    compiler.version=13.0
    compiler.libcxx=libc++
    compiler.cppstd=gnu98
    build_type=Release
    [options]
    [tool_requires]
    [env]
    ...

5. Now, we will use Conan to install **Zlib** and generate the files that CMake needs to find
   this library and build our project. We will generate those files in the folder
   *cmake-build-release*. To do that, just run:

.. code-block:: bash

    $ conan install . --output-folder cmake-build-release

You will get something similar to this as output of that command:

.. code-block:: bash

    $ conan install . --output-folder cmake-build-release
    ...
    -------- Computing dependency graph ----------
    zlib/1.2.11: Not found in local cache, looking in remotes...
    zlib/1.2.11: Checking remote: conanv2
    zlib/1.2.11: Trying with 'conanv2'...
    Downloading conanmanifest.txt
    Downloading conanfile.py
    Downloading conan_export.tgz
    Decompressing conan_export.tgz
    zlib/1.2.11: Downloaded recipe revision 25fd8350c227f2d6b5c5ca74c4009074
    Graph root
        conanfile.txt: /Users/conan-docs/Documents/developer/conan/examples2.0/tutorial/consumer/getting_started/conanfile.txt
    Requirements
        zlib/1.2.11#25fd8350c227f2d6b5c5ca74c4009074 - Downloaded (conanv2)

    -------- Computing necessary packages ----------
    Requirements
        zlib/1.2.11#25fd8350c227f2d6b5c5ca74c4009074:2a823fda5c9d8b4f682cb27c30caf4124c5726c8#2d46b6fb6c2b74296cf021fa332cd1da - Download (conanv2)

    -------- Installing packages ----------

    Installing (downloading, building) binaries...
    zlib/1.2.11: Retrieving package 2a823fda5c9d8b4f682cb27c30caf4124c5726c8 from remote 'conanv2' 
    Downloading conanmanifest.txt
    Downloading conaninfo.txt
    Downloading conan_package.tgz
    Decompressing conan_package.tgz
    zlib/1.2.11: Package installed 2a823fda5c9d8b4f682cb27c30caf4124c5726c8
    zlib/1.2.11: Downloaded package revision 2d46b6fb6c2b74296cf021fa332cd1da

    -------- Finalizing install (generators) ----------
    conanfile.txt: Generator 'CMakeDeps' calling 'generate()'
    conanfile.txt: Generator 'CMakeToolchain' calling 'generate()'
    conanfile.txt: Aggregating env generators


As you can see in the output, Conan installed the *Zlib* library from the remote server we
configured at the beginning of the tutorial. This server does not only store the Conan
recipes, that tell Conan how to build the libraries and what information to pass to the
projects that use this libraries but also prebuilt binaries that can be reused so we don't
have to build from sources everytime.


.. _consuming_packages_getting_started_read_more:

Read more
---------

- Getting started with Autotools
- Getting started with Meson
- ...
