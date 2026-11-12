.. _consuming_packages_build_simple_cmake_project:

Build a simple CMake project using Conan
========================================

Let's get started with an example: We are going to create a string compressor application
that uses one of the most popular C++ libraries: `Zlib <https://zlib.net/>`__.

We'll use CMake as build system in this case but keep in mind that Conan **works with any
build system** and is not limited to using CMake. You can check more examples with other
build systems in the :ref:`Read More
section<consuming_packages_read_more>`.


Please, first clone the sources to recreate this project, you can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/consuming_packages/simple_cmake_project


We start from a very simple C language project with this structure:

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

Also, the contents of *CMakeLists.txt* are:

.. code-block:: cmake
    :caption: **CMakeLists.txt**

    cmake_minimum_required(VERSION 3.15)
    project(compressor C)

    find_package(ZLIB REQUIRED)

    add_executable(${PROJECT_NAME} src/main.c)
    target_link_libraries(${PROJECT_NAME} ZLIB::ZLIB)

Our application relies on the **Zlib** library. Conan, by default, tries to install
libraries from a remote server called `ConanCenter <https://conan.io/center/>`_.
You can search there for libraries and also check the available versions. In our case, 
after checking the available versions for `Zlib <https://conan.io/center/zlib>`__ we
choose to use one of the latest versions: **zlib/1.2.11**.

The easiest way to install the **Zlib** library and find it from our project with Conan is
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
      project, in this case, **zlib/1.2.11**.

    * **[generators]** section tells Conan to generate the files that the compilers or
      build systems will use to find the dependencies and build the project. In this case,
      as our project is based in *CMake*, we will use :ref:`CMakeDeps<conan_tools_cmakedeps>` to
      generate information about where the **Zlib** library files are installed and
      :ref:`CMakeToolchain<conan_tools_cmaketoolchain>` to pass build information to *CMake*
      using a *CMake* toolchain file.

Besides the *conanfile.txt*, we need a **Conan profile** to build our project. Conan
profiles allow users to define a configuration set for things like the compiler, build
configuration, architecture, shared or static libraries, etc. Conan, by default, will
not try to detect a profile automatically, so we need to create one. To let Conan try
to guess the profile, based on the current operating system and installed tools, please
run:

.. code-block:: bash

    conan profile detect --force

This will detect the operating system, build architecture and compiler settings based on
the environment. It will also set the build configuration as *Release* by default. The
generated profile will be stored in the Conan home folder with name *default* and will be
used by Conan in all commands by default unless another profile is specified via the command
line. An example of the output of this command for MacOS would be:

.. code-block:: ini

    $ conan profile detect --force
    Found apple-clang 14.0
    apple-clang>=13, using the major as version
    Detected profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos

.. note:: **A note about the detected C++ standard by Conan**

    Conan will always set the default C++ standard as the one that the detected compiler
    version uses by default, except for the case of macOS using apple-clang. In this case,
    for apple-clang>=11, it sets ``compiler.cppstd=gnu17``. If you want to use a different
    C++ standard, you can edit the default profile file directly. First, get the location
    of the default profile using:

    .. code-block:: bash

        $ conan profile path default
        /Users/user/.conan2/profiles/default

    Then open and edit the file and set ``compiler.cppstd`` to the C++ standard you want
    to use.

.. note:: **Using a compiler other than the auto-detected one**

    If you want to change a Conan profile to use a compiler different from the default
    one, you need to change the ``compiler`` setting and also tell Conan explicitly where
    to find it using the :ref:`tools.build:compiler_executables
    configuration<conan-cmake-toolchain_conf>`.

We will use Conan to install **Zlib** and generate the files that CMake needs to
find this library and build our project. We will generate those files in the folder
*build*. To do that, run:

.. code-block:: bash

    $ conan install . --output-folder=build --build=missing


You will get something similar to this as the output of that command:

.. code-block:: bash

    $ conan install . --output-folder=build --build=missing
    ...
    -------- Computing dependency graph ----------
    zlib/1.2.11: Not found in local cache, looking in remotes...
    zlib/1.2.11: Checking remote: conancenter
    zlib/1.2.11: Trying with 'conancenter'...
    Downloading conanmanifest.txt
    Downloading conanfile.py
    Downloading conan_export.tgz
    Decompressing conan_export.tgz
    zlib/1.2.11: Downloaded recipe revision f1fadf0d3b196dc0332750354ad8ab7b
    Graph root
        conanfile.txt: /home/conan/examples2/tutorial/consuming_packages/simple_cmake_project/conanfile.txt
    Requirements
        zlib/1.2.11#f1fadf0d3b196dc0332750354ad8ab7b - Downloaded (conancenter)

    -------- Computing necessary packages ----------
    Requirements
        zlib/1.2.11#f1fadf0d3b196dc0332750354ad8ab7b:cdc9a35e010a17fc90bb845108cf86cfcbce64bf#dd7bf2a1ab4eb5d1943598c09b616121 - Download (conancenter)

    -------- Installing packages ----------

    Installing (downloading, building) binaries...
    zlib/1.2.11: Retrieving package cdc9a35e010a17fc90bb845108cf86cfcbce64bf from remote 'conancenter'
    Downloading conanmanifest.txt
    Downloading conaninfo.txt
    Downloading conan_package.tgz
    Decompressing conan_package.tgz
    zlib/1.2.11: Package installed cdc9a35e010a17fc90bb845108cf86cfcbce64bf
    zlib/1.2.11: Downloaded package revision dd7bf2a1ab4eb5d1943598c09b616121

    -------- Finalizing install (deploy, generators) ----------
    conanfile.txt: Generator 'CMakeToolchain' calling 'generate()'
    conanfile.txt: Generator 'CMakeDeps' calling 'generate()'
    conanfile.txt: Generating aggregated env files


As you can see in the output, there are a couple of things that happened:

    * Conan installed the *Zlib* library from the remote server, which should be the Conan
      Center server by default if the library is available. This server stores both the Conan
      recipes, which are the files that define how libraries must be built, and the binaries
      that can be reused so we don't have to build from sources every time.
    * Conan generated several files under the **build** folder. Those files
      were generated by both the ``CMakeToolchain`` and ``CMakeDeps`` generators we set in
      the **conanfile.txt**. ``CMakeDeps`` generates files so that CMake finds the Zlib
      library we have just downloaded. On the other side, ``CMakeToolchain`` generates a
      toolchain file for CMake so that we can transparently build our project with CMake
      using the same settings that we detected for our default profile.


Now we are ready to build and run our **compressor** app:

.. code-block:: bash
    :caption: Windows

    $ cd build
    # assuming Visual Studio 15 2017 is your VS version and that it matches your default profile
    $ cmake .. -G "Visual Studio 15 2017" -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake"
    $ cmake --build . --config Release
    ...
    [100%] Built target compressor
    $ Release\compressor.exe
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11

.. code-block:: bash
    :caption: Linux, macOS
    
    $ cd build
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .
    ...
    [100%] Built target compressor
    $ ./compressor
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11


Note that ``CMakeToolchain`` might generate CMake **presets** files, that allows users with a modern CMake (``>=3.23``) to 
use them with ``cmake --preset`` instead of passing the toolchain file argument. 
See :ref:`Building with CMake presets<examples-tools-cmake-toolchain-build-project-presets>`


.. _consuming_packages_read_more:

.. seealso::

    - :ref:`Building with CMake presets<examples-tools-cmake-toolchain-build-project-presets>`
    - :ref:`Getting started with Autotools<examples_tools_autotools_autotools_toolchain_build_project_autotools_toolchain>`
    - :ref:`Getting started with Meson<examples_tools_meson_toolchain_build_simple_meson_project>`
    - :ref:`Getting started with Bazel<examples_tools_bazel_toolchain_build_simple_bazel_project>`
    - :ref:`Getting started with Bazel 7.x<examples_tools_bazel_7x_toolchain_build_simple_bazel_project>`
