.. _examples_runners_docker_basic:

Creating a Conan package using a Docker runner
==============================================

.. include:: ../../../common/experimental_warning.inc

In this example we are going to see how to create the ``zlib/1.3.1`` Conan packge inside Docker using a runner. Let’s create two profiles and a Dockerfile inside our project folder.

.. code-block:: bash

    $ cd </my/runner/folder>
    $ tree
    .
    ├── Dockerfile
    ├── docker_example_build
    └── docker_example_host

``docker_example_host`` profile

..  code-block:: text

    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux
    [runner]
    type=docker
    dockerfile=</my/runner/folder>
    cache=copy
    remove=true

``docker_example_build`` profile

..  code-block:: text

    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux

``Dockerfile``

..  code-block:: docker

    FROM ubuntu:22.04
    RUN apt-get update \
        && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            build-essential \
            cmake \
            python3 \
            python3-pip \
            python3-venv \
        && rm -rf /var/lib/apt/lists/*
    RUN pip install conan

In this example we are going to start from a totally clean docker, without containers or images. In addition, we are going to have the conan cache also completely empty.

.. code-block:: bash

    $ conan list "*:*"
    Found 0 pkg/version recipes matching * in local cache

    $ docker ps --all
    CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

    $ docker images  
    REPOSITORY   TAG       IMAGE ID   CREATED   SIZE


Now, we are going to clone and build zlib from conan-center-index and create it using our new runner definition.

.. code-block:: bash
    
    $ git clone https://github.com/conan-io/conan-center-index.git --depth=1
    $ conan create ./conan-center-index/recipes/zlib/all --version 1.3.1 -pr:h </my/runner/folder>/docker_example_host -pr:b </my/runner/folder>/docker_example_build

If we split and analyze the command output, we can see what is happening and where the commands are being executed.

1. Standard conan execution.

.. code-block:: bash

    ======== Exporting recipe to the cache ========
    zlib/1.3.1: Exporting package recipe: </my/runner/folder>/conan-center-index/recipes/zlib/all/conanfile.py
    zlib/1.3.1: exports: File 'conandata.yml' found. Exporting it...
    zlib/1.3.1: Calling export_sources()
    zlib/1.3.1: Copied 1 '.py' file: conanfile.py
    zlib/1.3.1: Copied 1 '.yml' file: conandata.yml
    zlib/1.3.1: Copied 1 '.patch' file: 0001-fix-cmake.patch
    zlib/1.3.1: Exported to cache folder: /Users/conan/.conan2/p/zlib95420566fc0dd/e
    zlib/1.3.1: Exported: zlib/1.3.1#e20364c96c45455608a72543f3a53133 (2024-04-29 17:03:44 UTC)

    ======== Input profiles ========
    Profile host:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux

    Profile build:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux

2. Build docker image

.. code-block:: bash

    **********************************************
    * Building the Docker image: my-conan-runner *
    **********************************************

    Dockerfile path: '</my/runner/folder>/Dockerfile'
    Docker build context: '</my/runner/folder>'

    Step 1/4 : FROM ubuntu:22.04

    ...

    ---> dba927bb0517
    Successfully built dba927bb0517
    Successfully tagged my-conan-runner:latest

3. Save the local cache running ``conan cache save``.

.. code-block:: bash

    ******************************************************************************************************************
    * Save host cache in: </my/runner/folder>/conan-center-index/recipes/zlib/all/.conanrunner/local_cache_save.tgz *
    ******************************************************************************************************************

    Found 1 pkg/version recipes matching * in local cache
    Saving zlib/1.3.1: p/zlib95420566fc0dd

4. Create and initialize the docker container.

.. code-block:: bash

    *********************************
    * Creating the docker container *
    *********************************

    *****************************************
    * Container conan-runner-docker running *
    *****************************************

5. Check if the container has a conan version with the runner feature.

.. code-block:: bash

    *******************************************
    * Running in container: "conan --version" *
    *******************************************

    Conan version 2.3.0

6. Initialize the container conan cache using the host copy running ``conan cache restore``.

.. code-block:: bash

    *********************************************************************************************************
    * Running in container: "conan cache restore "/root/conanrunner/all/.conanrunner/local_cache_save.tgz"" *
    *********************************************************************************************************

    Restore: zlib/1.3.1 in p/zlib95420566fc0dd
    Local Cache
    zlib
        zlib/1.3.1
        revisions
            e20364c96c45455608a72543f3a53133 (2024-04-29 17:19:32 UTC)
            packages
            recipe_folder: p/zlib95420566fc0dd

7. Run the ``conan create`` inside the container and build zlib.

.. code-block:: bash

    *****************************************************************************************************************************************************************************************************************************************************
    * Running in container: "conan create /root/conanrunner/all --version 1.3.1 -pr:h /root/conanrunner/all/.conanrunner/profiles/docker_example_host_1 -pr:b /root/conanrunner/all/.conanrunner/profiles/docker_example_build_0 -f json > create.json" *
    *****************************************************************************************************************************************************************************************************************************************************


    ======== Exporting recipe to the cache ========
    zlib/1.3.1: Exporting package recipe: /root/conanrunner/all/conanfile.py
    zlib/1.3.1: exports: File 'conandata.yml' found. Exporting it...
    zlib/1.3.1: Calling export_sources()
    zlib/1.3.1: Copied 1 '.yml' file: conandata.yml
    zlib/1.3.1: Copied 1 '.py' file: conanfile.py
    zlib/1.3.1: Copied 1 '.patch' file: 0001-fix-cmake.patch
    zlib/1.3.1: Exported to cache folder: /root/.conan2/p/zlib95420566fc0dd/e
    zlib/1.3.1: Exported: zlib/1.3.1#e20364c96c45455608a72543f3a53133 (2024-04-29 17:19:32 UTC)

    ======== Input profiles ========
    Profile host:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux

    Profile build:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux


    ======== Computing dependency graph ========
    Graph root
        cli
    Requirements
        zlib/1.3.1#e20364c96c45455608a72543f3a53133 - Cache

    ======== Computing necessary packages ========
    zlib/1.3.1: Forced build from source
    Requirements
        zlib/1.3.1#e20364c96c45455608a72543f3a53133:b647c43bfefae3f830561ca202b6cfd935b56205 - Build

    ======== Installing packages ========
    zlib/1.3.1: Calling source() in /root/.conan2/p/zlib95420566fc0dd/s/src

    -------- Installing package zlib/1.3.1 (1 of 1) --------
    zlib/1.3.1: Building from source
    zlib/1.3.1: Package zlib/1.3.1:b647c43bfefae3f830561ca202b6cfd935b56205
    zlib/1.3.1: Copying sources to build folder
    zlib/1.3.1: Building your package in /root/.conan2/p/b/zlib8dd8e27348e8c/b
    zlib/1.3.1: Calling generate()
    zlib/1.3.1: Generators folder: /root/.conan2/p/b/zlib8dd8e27348e8c/b/build/Release/generators
    zlib/1.3.1: CMakeToolchain generated: conan_toolchain.cmake
    zlib/1.3.1: CMakeToolchain generated: /root/.conan2/p/b/zlib8dd8e27348e8c/b/build/Release/generators/CMakePresets.json
    zlib/1.3.1: CMakeToolchain generated: /root/.conan2/p/b/zlib8dd8e27348e8c/b/src/CMakeUserPresets.json
    zlib/1.3.1: Generating aggregated env files
    zlib/1.3.1: Generated aggregated env files: ['conanbuild.sh', 'conanrun.sh']
    zlib/1.3.1: Calling build()
    zlib/1.3.1: Apply patch (conan): separate static/shared builds, disable debug suffix
    zlib/1.3.1: Running CMake.configure()
    zlib/1.3.1: RUN: cmake -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="/root/.conan2/p/b/zlib8dd8e27348e8c/p" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" -DCMAKE_BUILD_TYPE="Release" "/root/.conan2/p/b/zlib8dd8e27348e8c/b/src"
    -- Using Conan toolchain: /root/.conan2/p/b/zlib8dd8e27348e8c/b/build/Release/generators/conan_toolchain.cmake
    -- Conan toolchain: Setting CMAKE_POSITION_INDEPENDENT_CODE=ON (options.fPIC)
    -- Conan toolchain: Setting BUILD_SHARED_LIBS = OFF
    -- The C compiler identification is GNU 11.4.0
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Check for working C compiler: /usr/bin/cc - skipped
    -- Detecting C compile features
    -- Detecting C compile features - done
    -- Looking for sys/types.h
    -- Looking for sys/types.h - found
    -- Looking for stdint.h
    -- Looking for stdint.h - found
    -- Looking for stddef.h
    -- Looking for stddef.h - found
    -- Check size of off64_t
    -- Check size of off64_t - done
    -- Looking for fseeko
    -- Looking for fseeko - found
    -- Looking for unistd.h
    -- Looking for unistd.h - found
    -- Renaming
    --     /root/.conan2/p/b/zlib8dd8e27348e8c/b/src/zconf.h
    -- to 'zconf.h.included' because this file is included with zlib
    -- but CMake generates it automatically in the build directory.
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /root/.conan2/p/b/zlib8dd8e27348e8c/b/build/Release
    zlib/1.3.1: Running CMake.build()
    zlib/1.3.1: RUN: cmake --build "/root/.conan2/p/b/zlib8dd8e27348e8c/b/build/Release" -- -j16
    [ 12%] Building C object CMakeFiles/zlib.dir/adler32.c.o
    [ 12%] Building C object CMakeFiles/zlib.dir/compress.c.o
    [ 18%] Building C object CMakeFiles/zlib.dir/deflate.c.o
    [ 25%] Building C object CMakeFiles/zlib.dir/crc32.c.o
    [ 31%] Building C object CMakeFiles/zlib.dir/gzlib.c.o
    [ 37%] Building C object CMakeFiles/zlib.dir/gzread.c.o
    [ 43%] Building C object CMakeFiles/zlib.dir/gzclose.c.o
    [ 56%] Building C object CMakeFiles/zlib.dir/infback.c.o
    [ 56%] Building C object CMakeFiles/zlib.dir/gzwrite.c.o
    [ 62%] Building C object CMakeFiles/zlib.dir/inflate.c.o
    [ 68%] Building C object CMakeFiles/zlib.dir/inffast.c.o
    [ 75%] Building C object CMakeFiles/zlib.dir/trees.c.o
    [ 81%] Building C object CMakeFiles/zlib.dir/zutil.c.o
    [ 87%] Building C object CMakeFiles/zlib.dir/uncompr.c.o
    [ 93%] Building C object CMakeFiles/zlib.dir/inftrees.c.o
    [100%] Linking C static library libz.a
    [100%] Built target zlib
    zlib/1.3.1: Package 'b647c43bfefae3f830561ca202b6cfd935b56205' built
    zlib/1.3.1: Build folder /root/.conan2/p/b/zlib8dd8e27348e8c/b/build/Release
    zlib/1.3.1: Generating the package
    zlib/1.3.1: Packaging in folder /root/.conan2/p/b/zlib8dd8e27348e8c/p
    zlib/1.3.1: Calling package()
    zlib/1.3.1: Running CMake.install()
    zlib/1.3.1: RUN: cmake --install "/root/.conan2/p/b/zlib8dd8e27348e8c/b/build/Release" --prefix "/root/.conan2/p/b/zlib8dd8e27348e8c/p"
    -- Install configuration: "Release"
    -- Installing: /root/.conan2/p/b/zlib8dd8e27348e8c/p/lib/libz.a
    -- Installing: /root/.conan2/p/b/zlib8dd8e27348e8c/p/include/zconf.h
    -- Installing: /root/.conan2/p/b/zlib8dd8e27348e8c/p/include/zlib.h

    zlib/1.3.1: package(): Packaged 1 file: LICENSE
    zlib/1.3.1: package(): Packaged 2 '.h' files: zlib.h, zconf.h
    zlib/1.3.1: package(): Packaged 1 '.a' file: libz.a
    zlib/1.3.1: Created package revision fd85b1346d5377ae2465645768e62bf2
    zlib/1.3.1: Package 'b647c43bfefae3f830561ca202b6cfd935b56205' created
    zlib/1.3.1: Full package reference: zlib/1.3.1#e20364c96c45455608a72543f3a53133:b647c43bfefae3f830561ca202b6cfd935b56205#fd85b1346d5377ae2465645768e62bf2
    zlib/1.3.1: Package folder /root/.conan2/p/b/zlib8dd8e27348e8c/p
    WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
    WARN: deprecated:     'cpp_info.names' used in: zlib/1.3.1

    ======== Launching test_package ========

    ======== Computing dependency graph ========
    Graph root
        zlib/1.3.1 (test package): /root/conanrunner/all/test_package/conanfile.py
    Requirements
        zlib/1.3.1#e20364c96c45455608a72543f3a53133 - Cache

    ======== Computing necessary packages ========
    Requirements
        zlib/1.3.1#e20364c96c45455608a72543f3a53133:b647c43bfefae3f830561ca202b6cfd935b56205#fd85b1346d5377ae2465645768e62bf2 - Cache

    ======== Installing packages ========
    zlib/1.3.1: Already installed! (1 of 1)
    WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
    WARN: deprecated:     'cpp_info.names' used in: zlib/1.3.1

    ======== Testing the package ========
    Removing previously existing 'test_package' build folder: /root/conanrunner/all/test_package/build/gcc-11-x86_64-gnu17-release
    zlib/1.3.1 (test package): Test package build: build/gcc-11-x86_64-gnu17-release
    zlib/1.3.1 (test package): Test package build folder: /root/conanrunner/all/test_package/build/gcc-11-x86_64-gnu17-release
    zlib/1.3.1 (test package): Writing generators to /root/conanrunner/all/test_package/build/gcc-11-x86_64-gnu17-release/generators
    zlib/1.3.1 (test package): Generator 'CMakeToolchain' calling 'generate()'
    zlib/1.3.1 (test package): CMakeToolchain generated: conan_toolchain.cmake
    zlib/1.3.1 (test package): CMakeToolchain generated: /root/conanrunner/all/test_package/build/gcc-11-x86_64-gnu17-release/generators/CMakePresets.json
    zlib/1.3.1 (test package): CMakeToolchain generated: /root/conanrunner/all/test_package/CMakeUserPresets.json
    zlib/1.3.1 (test package): Generator 'CMakeDeps' calling 'generate()'
    zlib/1.3.1 (test package): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
        find_package(ZLIB)
        target_link_libraries(... ZLIB::ZLIB)
    zlib/1.3.1 (test package): Generator 'VirtualRunEnv' calling 'generate()'
    zlib/1.3.1 (test package): Generating aggregated env files
    zlib/1.3.1 (test package): Generated aggregated env files: ['conanrun.sh', 'conanbuild.sh']

    ======== Testing the package: Building ========
    zlib/1.3.1 (test package): Calling build()
    zlib/1.3.1 (test package): Running CMake.configure()
    zlib/1.3.1 (test package): RUN: cmake -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="/root/conanrunner/all/test_package" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" -DCMAKE_BUILD_TYPE="Release" "/root/conanrunner/all/test_package"
    -- Using Conan toolchain: /root/conanrunner/all/test_package/build/gcc-11-x86_64-gnu17-release/generators/conan_toolchain.cmake
    -- Conan toolchain: C++ Standard 17 with extensions ON
    -- The C compiler identification is GNU 11.4.0
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Check for working C compiler: /usr/bin/cc - skipped
    -- Detecting C compile features
    -- Detecting C compile features - done
    -- Conan: Target declared 'ZLIB::ZLIB'
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /root/conanrunner/all/test_package/build/gcc-11-x86_64-gnu17-release
    zlib/1.3.1 (test package): Running CMake.build()
    zlib/1.3.1 (test package): RUN: cmake --build "/root/conanrunner/all/test_package/build/gcc-11-x86_64-gnu17-release" -- -j16
    [ 50%] Building C object CMakeFiles/test_package.dir/test_package.c.o
    [100%] Linking C executable test_package
    [100%] Built target test_package

    ======== Testing the package: Executing test ========
    zlib/1.3.1 (test package): Running test()
    zlib/1.3.1 (test package): RUN: ./test_package
    Compressed size is: 21
    Compressed string is: Conan Package Manager
    Compressed size is: 22
    Compressed string is: xsKHLNLOUMRE
    ZLIB VERSION: 1.3.1

8. Copy just the package created inside the container using the ``pkglist.json`` info from the previous ``conan create``, restore this new package inside the host cache running a ``conan cache save`` and remove the container.

..  code-block:: bash

    **********************************************************************************************************************************
    * Running in container: "conan cache save --list=pkglist.json --file "/root/conanrunner/all"/.conanrunner/docker_cache_save.tgz" *
    **********************************************************************************************************************************

    Saving zlib/1.3.1: p/zlib95420566fc0dd
    Saving zlib/1.3.1:b647c43bfefae3f830561ca202b6cfd935b56205: p/b/zlib8dd8e27348e8c/p
    Saving zlib/1.3.1:b647c43bfefae3f830561ca202b6cfd935b56205 metadata: p/b/zlib8dd8e27348e8c/d/metadata
    Local Cache
    zlib
        zlib/1.3.1
        revisions
            e20364c96c45455608a72543f3a53133 (2024-04-29 17:19:32 UTC)
            packages
                b647c43bfefae3f830561ca202b6cfd935b56205
                revisions
                    fd85b1346d5377ae2465645768e62bf2
                    package_folder: p/b/zlib8dd8e27348e8c/p
                    metadata_folder: p/b/zlib8dd8e27348e8c/d/metadata
                info
                    settings
                    os: Linux
                    arch: x86_64
                    compiler: gcc
                    compiler.version: 11
                    build_type: Release
                    options
                    fPIC: True
                    shared: False
            recipe_folder: p/zlib95420566fc0dd


    ************************************************************************************************************************
    * Restore host cache from: </my/runner/folder>/conan-center-index/recipes/zlib/all/.conanrunner/docker_cache_save.tgz *
    ************************************************************************************************************************

    Restore: zlib/1.3.1 in p/zlib95420566fc0dd
    Restore: zlib/1.3.1:b647c43bfefae3f830561ca202b6cfd935b56205 in p/b/zlib8dd8e27348e8c/p
    Restore: zlib/1.3.1:b647c43bfefae3f830561ca202b6cfd935b56205 metadata in p/b/zlib8dd8e27348e8c/d/metadata

    **********************
    * Stopping container *
    **********************


    **********************
    * Removing container *
    **********************

If we now check the status of our conan and docker cache, we will see the new zlib package compile for Linux and the new docker image. We don't have any container because we define ``remove=true``

.. code-block:: bash

    $ conan list "*:*"
    Found 1 pkg/version recipes matching * in local cache
    Local Cache
      zlib
        zlib/1.3.1
        revisions
            e20364c96c45455608a72543f3a53133 (2024-04-29 17:18:07 UTC)
            packages
                b647c43bfefae3f830561ca202b6cfd935b56205
                info
                    settings
                    arch: x86_64
                    build_type: Release
                    compiler: gcc
                    compiler.version: 11
                    os: Linux
                    options
                    fPIC: True
                    shared: False

    $ docker ps --all
    CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

    $ docker images  
    REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
    my-conan-runner   latest    383b905f352e   22 minutes ago   531MB
    ubuntu            22.04     437ec753bef3   12 days ago      77.9MB
