.. _examples_tools_meson_toolchain_build_simple_meson_project:

Build a simple Meson project using Conan
========================================

In this example, we are going to create a string compressor application
that uses one of the most popular C++ libraries: `Zlib <https://zlib.net/>`__.

.. note::

    This example is based on the main :ref:`Build a simple CMake project using Conan<consuming_packages_build_simple_cmake_project>`
    tutorial. So we highly recommend reading it before trying out this one.

We'll use Meson as build system and pkg-config as helper tool in this case, so you should get them installed
before going forward with this example.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/tools/meson/mesontoolchain/simple_meson_project


We start from a very simple C language project with this structure:

.. code-block:: text

    .
    ├── meson.build
    └── src
        └── main.c

This project contains a basic *meson.build* including the **zlib** dependency and the
source code for the string compressor program in *main.c*.

Let's have a look at the *main.c* file:

.. code-block:: cpp
    :caption: **main.c**

    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>

    #include <zlib.h>

    int main(void) {
        char buffer_in [256] = {"Conan is a MIT-licensed, Open Source package manager for C and C++ development "
                                "for C and C++ development, allowing development teams to easily and efficiently "
                                "manage their packages and dependencies across platforms and build systems."};
        char buffer_out [256] = {0};

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

        printf("Uncompressed size is: %lu\n", strlen(buffer_in));
        printf("Compressed size is: %lu\n", strlen(buffer_out));

        printf("ZLIB VERSION: %s\n", zlibVersion());

        return EXIT_SUCCESS;
    }

Also, the contents of *meson.build* are:

.. code-block:: text
    :caption: **meson.build**

    project('tutorial', 'c')
    zlib = dependency('zlib', version : '1.2.11')
    executable('compressor', 'src/main.c', dependencies: zlib)


Let's create a *conanfile.txt* with the following content to install **Zlib**:

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    zlib/1.2.11

    [generators]
    PkgConfigDeps
    MesonToolchain

In this case, we will use :ref:`PkgConfigDeps<PkgConfigDeps>` to generate information about where the **Zlib** library
files are installed thanks to the `*.pc` files and :ref:`MesonToolchain<MesonToolchain>` to pass build information
to *Meson* using a `conan_meson_[native|cross].ini` file that describes the native/cross compilation environment, which in
this case is a `conan_meson_native.ini` one.

We will use Conan to install **Zlib** and generate the files that Meson needs to find this library and build our project.
We will generate those files in the folder *build*. To do that, run:

.. code-block:: bash

    $ conan install . --output-folder=build --build=missing

Now we are ready to build and run our **compressor** app:

.. code-block:: bash
    :caption: Windows

    $ cd build
    $ meson setup --native-file conan_meson_native.ini .. meson-src
    $ meson compile -C meson-src
    $ meson-src\compressor.exe
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11

.. code-block:: bash
    :caption: Linux, macOS

    $ cd build
    $ meson setup --native-file conan_meson_native.ini .. meson-src
    $ meson compile -C meson-src
    $ ./meson-src/compressor
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11
