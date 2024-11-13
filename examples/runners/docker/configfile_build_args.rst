.. _examples_runners_docker_configfile_build_args:

Using a docker runner configfile to parameterize a Dockerfile
=============================================================

.. include:: ../../../common/experimental_warning.inc

If you need more control over the build and execution of the container, you can define more parameters inside a configfile yaml.

For example, you can add arguments in the build step or environment variables when you launch the container.

To use it, you just need to add it in the host profile.

.. code-block:: text

    [settings]
    ...
    [runner]
    type=docker
    configfile=</my/runner/folder>/configfile
    cache=copy
    remove=false

**How to use**

Let’s create a Dockerfile inside your project folder, a cmake_lib ``myparamlib`` like the :ref:`"Creating a Conan package using a Docker runner"<examples_runners_docker_basic>` example and two profiles. 

.. code-block:: bash

    $ cd </my/runner/folder>
    $ mkdir myparamlib
    $ cd myparamlib
    $ conan new cmake_lib -d name=myparamlib -d version=0.1
    $ cd </my/runner/folder>
    $ tree
    .
    ├── CMakeLists.txt
    ├── conanfile.py
    ├── include
    │   └── myparamlib.h
    ├── src
    │   └── myparamlib.cpp
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── src
            └── example.cpp

.. code-block:: docker

    ARG BASE_IMAGE
    FROM $BASE_IMAGE
    RUN apt-get update \
        && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            build-essential \
            cmake \
            python3 \
            python3-pip \
            python3-venv \
        && rm -rf /var/lib/apt/lists/*
    RUN pip install conan

``configfile``

.. code-block:: yaml

    image: my-conan-runner-image
    build:
        dockerfile: </my/runner/folder>
        build_context: </my/runner/folder>
        build_args:
            BASE_IMAGE: ubuntu:22.04
    run:
        name: my-conan-runner-container

.. code-block:: bash

    $ cd </my/runner/folder>/myparamlib
    $ tree
    .
    ...
    ├── Dockerfile
    ...
    ├── configfile
    ...

``docker_param_example_host`` profile

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
    configfile=</my/runner/folder>/myparamlib/configfile
    cache=copy
    remove=false

``docker_param_example_build`` profile

.. code-block:: text

    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu17
    compiler.libcxx=libstdc++11
    compiler.version=11
    os=Linux

Now it's time to create our new library.

.. code-block:: bash

    $ conan create . --version 0.1 -pr:h docker_param_example_host -pr:b docker_param_example_build

    ...

    ****************************************************
    * Building the Docker image: my-conan-runner-image *
    ****************************************************

    Dockerfile path: '</my/runner/folder>/myparamlib/Dockerfile'
    Docker build context: '</my/runner/folder>/myparamlib'

    Step 1/5 : ARG BASE_IMAGE

    Step 2/5 : FROM $BASE_IMAGE

    ...

    Successfully built caa8071cdff7
    Successfully tagged my-conan-runner-image:latest

    ...

    **************************************************************************************************************************************************************************
    * Running in container: "conan create /root/conanrunner/myparamlib --version 0.1 -pr:h docker_param_example_host -pr:b docker_param_example_build -f json > create.json" *
    **************************************************************************************************************************************************************************

    ...

    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example

    ======== Testing the package: Executing test ========
    myparamlib/0.1 (test package): Running test()
    myparamlib/0.1 (test package): RUN: ./example
    myparamlib/0.1: Hello World Release!
    myparamlib/0.1: __x86_64__ defined
    myparamlib/0.1: _GLIBCXX_USE_CXX11_ABI 1
    myparamlib/0.1: __cplusplus201703
    myparamlib/0.1: __GNUC__11
    myparamlib/0.1: __GNUC_MINOR__4
    myparamlib/0.1 test_package


    **********************************************************************************************
    * Restore host cache from: </my/runner/folder>/myparamlib/.conanrunner/docker_cache_save.tgz *
    **********************************************************************************************

    Saving myparamlib/0.1: mypar36e44205a36b9
    Saving myparamlib/0.1:8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe: b/mypare0dc449d4125d/p
    Saving myparamlib/0.1:8631cf963dbbb4d7a378a64a6fd1dc57558bc2fe metadata: b/mypare0dc449d4125d/d/metadata

If we now check the status of our conan cache, we will see the new ``myparamlib`` pacakge.

.. code-block:: bash

    $ conan list "*:*"
    Found 1 pkg/version recipes matching * in local cache
    Local Cache
    myparamlib
        myparamlib/0.1
        revisions
            11cb359a0526fe9ce3cfefb59c5d1953 (2024-07-08 12:47:21 UTC)
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