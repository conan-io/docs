.. _consuming_packages_getting_started:

Getting started: building your project using a Conan package
============================================================

Let's get started with an example: We are going to create a string compressor application
that uses one of the most popular C++ libraries: `Zlib <https://zlib.net/>`_.

We'll use CMake as build system in this case but keep in mind that Conan **works with any
build system** and is not limited to using CMake. You can check more examples with other
build systems in the :ref:`Read More
section<consuming_packages_getting_started_read_more>`.

.. note::

    The source files to recreate this project are available in the `examples2.0 repository
    <https://github.com/conan-io/examples2.0>`_ in GitHub. You can skip the manual
    creation of the folder and sources with this command:

    .. code-block:: bash

        $ git clone https://github.com/conan-io/examples2.0.git && cd tutorial/consumer/getting_started


Building a CMake project consuming Zlib with Conan
--------------------------------------------------

#. We start from a very simple C language project with this structure:

.. code-block:: text

    .
    ├── CMakeLists.txt
    └── src
        └── main.c

This project contains a basic *CMakeLists.txt* including the *Zlib* dependency and the
source code of the string compressor in *main.c*.

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

#. Our application relies on the Zlib library. Conan, by default, tries to install
   libraries from a remote server called `Conan Center Index <https://conan.io/center/>`_.
   You can search there for libraries and also check the available versions. In our case, 
   after checking the available versions for `Zlib <hhttps://conan.io/center/zlib>`_ we
   choose to use the latest available version: **zlib/1.2.11**.

#. The easiest way to install the Zlib library and find it from our project with Conan is
   using a *conanfile.txt* file. Let's create one with the following content:

    .. code-block:: txt
       :caption: **conanfile.txt**

        [requires]
        zlib/1.2.11

        [generators]
        CMakeDeps
        CMakeToolchain

As you can see we added two sections to this file with a syntax similar to an *INI* file.

    * **[requires]** section is where we declare the libraries we want to use in the
      project, in this case zlib/1.2.11.

    * **[generators]** section tells Conan to generate the files that the compilers
      or build systems will use to find the dependencies and build the project. In this
      case, as our project is *CMake* based we will use *CMakeDeps* to generate information
      about where the *Zlib* library files are installed and *CMakeToolchain* to pass build
      information to CMake through a CMake toolchain file.



conan install . --output-folder conan

cmake . -DCMAKE_TOOLCHAIN_FILE=conan/conan_toolchain.cmake

cmake --build .

./compressor


.. _consuming_packages_getting_started_read_more:

Read more
=========

- Getting started with Autotools
- Getting started with Meson
- ...
