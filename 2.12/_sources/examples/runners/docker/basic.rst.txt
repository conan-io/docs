.. _examples_runners_docker_basic:

Creating a Conan package using a Docker runner
==============================================

.. include:: ../../../common/experimental_warning.inc

First of all you need to have the Docker daemon installed and running, plus Conan and the ``docker`` Python package. This tutorial assumes that you are running Conan inside a Python virtual environment, skip the first line if you already have the ``docker`` Python package installed in your virtual environment.

.. code-block:: bash

    # install docker in your virtual environment if you don't have it already installed
    $ pip install conan docker
    $ docker ps
    $ CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES


Now we are going to create create simple ``cmake_lib`` Conan template to later run inside Docker using the runner feature. Let’s create the Conan package and a Dockerfile inside our project folder.

.. code-block:: bash

    $ cd </my/runner/folder>
    $ mkdir mylib
    $ cd mylib
    $ conan new cmake_lib -d name=mylib -d version=0.1
    $ tree
    .
    ├── CMakeLists.txt
    ├── conanfile.py
    ├── include
    │   └── mylib.h
    ├── src
    │   └── mylib.cpp
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── src
            └── example.cpp

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

.. code-block:: bash

    $ cd </my/runner/folder>/mylib
    $ tree
    .
    ...
    ├── Dockerfile
    ...

Now, we need to define two new profiles inside the conan ``profiles`` folder. Replace ``</my/runner/folder>`` with your real project folder path.

``docker_example_host`` profile

.. code-block:: text

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
    dockerfile=</my/runner/folder>/mylib
    cache=copy
    remove=true

``docker_example_build`` profile

.. code-block:: bash

    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux

We are going to start from a totally clean environment, without any containers, images or conan package.

.. code-block:: bash

    $ conan list "*:*"
    Found 0 pkg/version recipes matching * in local cache


.. code-block:: bash

    $ docker ps --all
    CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES


.. code-block:: bash

    $ docker images
    REPOSITORY   TAG       IMAGE ID   CREATED   SIZE

Now, it's time to create our library ``mylib`` using our new runner definition.

.. code-block:: bash

    $ conan create . --version 0.1 -pr:h docker_example_host -pr:b docker_example_build

If we split and analyze the command output, we can see what is happening and where the commands are being executed.

**1.** Standard conan execution.

.. code-block:: bash

    ======== Exporting recipe to the cache ========
    mylib/0.1: Exporting package recipe: </my/runner/folder>/mylib/conanfile.py
    mylib/0.1: Copied 1 '.py' file: conanfile.py
    mylib/0.1: Copied 1 '.txt' file: CMakeLists.txt
    mylib/0.1: Copied 1 '.h' file: mylib.h
    mylib/0.1: Copied 1 '.cpp' file: mylib.cpp
    mylib/0.1: Exported to cache folder: /Users/davidsanfal/.conan2/p/mylib4abd06a04bdaa/e
    mylib/0.1: Exported: mylib/0.1#8760bf5a311f01cc26f3b95428203210 (2024-07-08 12:22:01 UTC)

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

**2.** Build docker image

.. code-block:: bash

    **********************************************
    * Building the Docker image: my-conan-runner *
    **********************************************

    Dockerfile path: '</my/runner/folder>/mylib/Dockerfile'
    Docker build context: '</my/runner/folder>/mylib'

    Step 1/4 : FROM ubuntu:22.04

    ...

    ---> 2bcf70201cce
    Successfully built 2bcf70201cce
    Successfully tagged conan-runner-default:latest

**3.** Save the local cache running ``conan cache save``.

.. code-block:: bash

    ***********************************************************************************
    * Save host cache in: </my/runner/folder>/mylib/.conanrunner/local_cache_save.tgz *
    ***********************************************************************************

    Found 1 pkg/version recipes matching * in local cache
    Saving mylib/0.1: mylib4abd06a04bdaa

**4.** Create and initialize the docker container.

.. code-block:: bash

    *********************************
    * Creating the docker container *
    *********************************

    *****************************************
    * Container conan-runner-docker running *
    *****************************************

**5.** Check if the container has a conan version with the runner feature.

.. code-block:: bash

    *******************************************
    * Running in container: "conan --version" *
    *******************************************

    Conan version 2.5.0

**6.** Initialize the container conan cache using the host copy running ``conan cache restore``.

.. code-block:: bash

    ***********************************************************************************************************
    * Running in container: "conan cache restore "/root/conanrunner/mylib/.conanrunner/local_cache_save.tgz"" *
    ***********************************************************************************************************

    Restore: mylib/0.1 in mylib4abd06a04bdaa
    Local Cache
    mylib
        mylib/0.1
        revisions
            8760bf5a311f01cc26f3b95428203210 (2024-07-08 12:22:19 UTC)
            packages
            recipe_folder: mylib4abd06a04bdaa

**7.** Run the conan create inside the container and build "mylib".

.. code-block:: bash

    *********************************************************************************************************************************************************
    * Running in container: "conan create /root/conanrunner/mylib --version 0.1 -pr:h docker_example_host -pr:b docker_example_build -f json > create.json" *
    *********************************************************************************************************************************************************


    ======== Exporting recipe to the cache ========
    mylib/0.1: Exporting package recipe: /root/conanrunner/mylib/conanfile.py
    mylib/0.1: Copied 1 '.py' file: conanfile.py
    mylib/0.1: Copied 1 '.txt' file: CMakeLists.txt
    mylib/0.1: Copied 1 '.cpp' file: mylib.cpp
    mylib/0.1: Copied 1 '.h' file: mylib.h
    mylib/0.1: Exported to cache folder: /root/.conan2/p/mylib4abd06a04bdaa/e
    mylib/0.1: Exported: mylib/0.1#8760bf5a311f01cc26f3b95428203210 (2024-07-08 12:22:20 UTC)

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
        mylib/0.1#8760bf5a311f01cc26f3b95428203210 - Cache

    ======== Computing necessary packages ========
    mylib/0.1: Forced build from source
    Requirements
        mylib/0.1#8760bf5a311f01cc26f3b95428203210:8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe - Build

    ======== Installing packages ========

    -------- Installing package mylib/0.1 (1 of 1) --------


    ...

    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example


    ======== Testing the package: Executing test ========
    mylib/0.1 (test package): Running test()
    mylib/0.1 (test package): RUN: ./example
    mylib/0.1: Hello World Release!
    mylib/0.1: __x86_64__ defined
    mylib/0.1: _GLIBCXX_USE_CXX11_ABI 1
    mylib/0.1: __cplusplus201703
    mylib/0.1: __GNUC__11
    mylib/0.1: __GNUC_MINOR__4
    mylib/0.1 test_package

**8.** Copy just the package created inside the container using the ``pkglist.json`` info from the previous ``conan create``, restore this new package inside the host cache running a ``conan cache save`` and remove the container.

.. code-block:: bash

    ************************************************************************************************************************************
    * Running in container: "conan cache save --list=pkglist.json --file "/root/conanrunner/mylib"/.conanrunner/docker_cache_save.tgz" *
    ************************************************************************************************************************************

    Saving mylib/0.1: mylib4abd06a04bdaa
    Saving mylib/0.1:8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe: b/mylib503035e4ee8ae/p
    Saving mylib/0.1:8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe metadata: b/mylib503035e4ee8ae/d/metadata
    Local Cache
    mylib
        mylib/0.1
        revisions
            8760bf5a311f01cc26f3b95428203210 (2024-07-08 12:22:20 UTC)
            packages
                8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe
                revisions
                    ded6547554ff2306db5250451340fa43
                    package_folder: b/mylib503035e4ee8ae/p
                    metadata_folder: b/mylib503035e4ee8ae/d/metadata
                info
                    settings
                    os: Linux
                    arch: x86_64
                    compiler: gcc
                    compiler.cppstd: gnu17
                    compiler.libcxx: libstdc++11
                    compiler.version: 11
                    build_type: Release
                    options
                    fPIC: True
                    shared: False
            recipe_folder: mylib4abd06a04bdaa


    ******************************************************************************************
    * Restore host cache from: </my/runner/folder>/mylib/.conanrunner/docker_cache_save.tgz  *
    ******************************************************************************************

    Restore: mylib/0.1 in mylib4abd06a04bdaa
    Restore: mylib/0.1:8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe in b/mylib503035e4ee8ae/p
    Restore: mylib/0.1:8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe metadata in b/mylib503035e4ee8ae/d/metadata

    **********************
    * Stopping container *
    **********************


    **********************
    * Removing container *
    **********************

If we now check the status of our conan and docker cache, we will see the new mylib package compile for Linux and the new docker image but we don’t have any container because we define ``remove=true``

.. code-block:: bash

    $ conan list "*:*"
    Found 1 pkg/version recipes matching * in local cache
    Local Cache
    mylib
        mylib/0.1
        revisions
            8760bf5a311f01cc26f3b95428203210 (2024-07-08 12:33:28 UTC)
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

.. code-block:: bash

    $ docker ps --all
    CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

.. code-block:: bash

    $ docker images
    REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
    my-conan-runner   latest    2bcf70201cce   11 minutes ago   531MB

What we have just done is to compile a library from scratch inside a Docker container without running any Docker command and retrieve the generated packages in a totally transparent and easily debuggable way thanks to our terminal output.

In this way, we can work as we have always done regardless of whether it is on our machine or in a container, without several open terminals and having the result of each operation in the same cache, being able to reuse the compiled packages from a previous compilation in another container automatically and transparently.