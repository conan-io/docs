.. _consuming_packages_tool_requires:

Using build tools as Conan packages
===================================

.. important::

    In this example, we will retrieve the CMake Conan package from a Conan repository with
    packages compatible with Conan 2.0. To run this example successfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``

In the previous example, we built our CMake project and used Conan to install and locate
the **Zlib** library. Conan used the CMake version found in the system path to build this
example. But, what happens if you don’t have CMake installed in your build environment or
want to build your project with a specific CMake version different from the one you have
already installed system-wide? In this case, you can declare this dependency in Conan
using a type of requirement named ``tool_requires``. Let’s see an example of how to add a
``tool_requires`` to our project, and use a different CMake version to build it.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/consuming_packages/tool_requires

The structure of the project is the same as the one of the previous example:

.. code-block:: text

    .
    ├── conanfile.txt
    ├── CMakeLists.txt
    └── src
        └── main.c


The main difference is the addition of the **[tool_requires]** section in the
**conanfile.txt** file. In this section, we declare that we want to build our application
using CMake **v3.19.8**.

.. code-block:: ini
    :caption: **conanfile.txt**
    :emphasize-lines: 4,5

    [requires]
    zlib/1.2.11

    [tool_requires]
    cmake/3.19.8

    [generators]
    CMakeDeps
    CMakeToolchain

We also added a message to the *CMakeLists.txt* to output the CMake version:

.. code-block:: cmake
    :caption: **CMakeLists.txt**
    :emphasize-lines: 6

    cmake_minimum_required(VERSION 3.15)
    project(compressor C)

    find_package(ZLIB REQUIRED)

    message("Building with CMake version: ${CMAKE_VERSION}")
    
    add_executable(${PROJECT_NAME} src/main.c)
    target_link_libraries(${PROJECT_NAME} ZLIB::ZLIB)

Now, as in the previous example, we will use Conan to install **Zlib** and **CMake
3.19.8** and generate the files to find both of them. We will generate those
files the folder *build*. To do that, just run:

.. code-block:: bash

    $ conan install . --output-folder=build --build=missing

You can check the output:

.. code-block:: bash

    -------- Computing dependency graph ----------
    cmake/3.19.8: Not found in local cache, looking in remotes...
    cmake/3.19.8: Checking remote: conanv2
    cmake/3.19.8: Trying with 'conanv2'...
    Downloading conanmanifest.txt
    Downloading conanfile.py
    cmake/3.19.8: Downloaded recipe revision 3e3d8f3a848b2a60afafbe7a0955085a
    Graph root
        conanfile.txt: /Users/carlosz/Documents/developer/conan/examples2/tutorial/consuming_packages/tool_requires/conanfile.txt
    Requirements
        zlib/1.2.11#f1fadf0d3b196dc0332750354ad8ab7b - Cache
    Build requirements
        cmake/3.19.8#3e3d8f3a848b2a60afafbe7a0955085a - Downloaded (conanv2)

    -------- Computing necessary packages ----------
    Requirements
        zlib/1.2.11#f1fadf0d3b196dc0332750354ad8ab7b:2a823fda5c9d8b4f682cb27c30caf4124c5726c8#48bc7191ec1ee467f1e951033d7d41b2 - Cache
    Build requirements
        cmake/3.19.8#3e3d8f3a848b2a60afafbe7a0955085a:f2f48d9745706caf77ea883a5855538256e7f2d4#6c519070f013da19afd56b52c465b596 - Download (conanv2)

    -------- Installing packages ----------

    Installing (downloading, building) binaries...
    cmake/3.19.8: Retrieving package f2f48d9745706caf77ea883a5855538256e7f2d4 from remote 'conanv2' 
    Downloading conanmanifest.txt
    Downloading conaninfo.txt
    Downloading conan_package.tgz
    Decompressing conan_package.tgz
    cmake/3.19.8: Package installed f2f48d9745706caf77ea883a5855538256e7f2d4
    cmake/3.19.8: Downloaded package revision 6c519070f013da19afd56b52c465b596
    zlib/1.2.11: Already installed!

    -------- Finalizing install (deploy, generators) ----------
    conanfile.txt: Generator 'CMakeToolchain' calling 'generate()'
    conanfile.txt: Generator 'CMakeDeps' calling 'generate()'
    conanfile.txt: Aggregating env generators

Now, if you check the folder you will see that Conan generated a new
file called ``conanbuild.sh/bat``. This is the result of automatically invoking a
``VirtualBuildEnv`` generator when we declared the ``tool_requires`` in the
**conanfile.txt**. This file sets some environment variables like a new ``PATH`` that
we can use to inject to our environment the location of CMake v3.19.8.

Activate the virtual environment, and run ``cmake --version`` to check that you
have installed the new CMake version in the path.

.. code-block:: bash
    :caption: Windows

    $ cd build
    $ conanbuild.bat

.. code-block:: bash
    :caption: Linux, macOS
    
    $ cd build
    $ source conanbuild.sh
    Capturing current environment in deactivate_conanbuildenv-release-x86_64.sh
    Configuring environment variables

Run ``cmake`` and check the version:

.. code-block:: bash
    
    $ cmake --version
    cmake version 3.19.8
    ...

As you can see, after activating the environment, the CMake v3.19.8 binary folder was
added to the path and is the currently active version now. Now you can build your project as
you previously did, but this time Conan will use CMake 3.19.8 to build it:

.. code-block:: bash
    :caption: Windows

    # assuming Visual Studio 15 2017 is your VS version and that it matches your default profile
    $ cmake .. -G "Visual Studio 15 2017" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build . --config Release
    ...
    Building with CMake version: 3.19.8
    ...
    [100%] Built target compressor
    $ Release\compressor.exe
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11

.. code-block:: bash
    :caption: Linux, macOS
    
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .
    ...
    Building with CMake version: 3.19.8
    ...
    [100%] Built target compressor
    $ ./compressor
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11


Note that when we activated the environment, a new file named
``deactivate_conanbuild.sh/bat`` was created in the same folder. If you source this file
you can restore the environment as it was before.

.. code-block:: bash
    :caption: Windows
    
    $ deactivate_conanbuild.bat

.. code-block:: bash
    :caption: Linux, macOS
    
    $ source deactivate_conanbuild.sh
    Restoring environment


Run ``cmake`` and check the version, it will be the version that was installed previous to
the environment activation:

.. code-block:: bash
    
    $ cmake --version
    cmake version 3.22.0
    ...


Read more
---------

- Using MinGW as tool_requires
- Using tool_requires in profiles
- Using conf to set a toolchain from a tool requires
- Creating recipes for tool_requires: packaging build tools
