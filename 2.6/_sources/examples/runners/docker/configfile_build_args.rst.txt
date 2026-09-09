.. _examples_runners_docker_configfile_build_args:

Using a docker runner configfile to parameterize a Dockerfile
=============================================================

.. include:: ../../../common/experimental_warning.inc

In this example we are going to see how to use a docker runner configfile to define our Dockerfile base image. Let’s create two profiles and a Dockerfile inside our project folder.

.. code-block:: bash

    $ cd </my/runner/folder>
    $ tree
    .
    ├── Dockerfile
    ├── configfile
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
    configfile=</my/runner/folder>/configfile
    cache=copy
    remove=false

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

``configfile``

..  code-block:: yaml

    image: my-conan-runner-image
    build:
        dockerfile: </my/runner/folder>
        build_context: </my/runner/folder>
        build_args:
            BASE_IMAGE: ubuntu:22.04
    run:
        name: my-conan-runner-container


..  code-block:: docker
    :caption: Dockerfile

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
    
    $ git clone https://github.com/conan-io/conan-center-index.git --depth 1
    $ conan create ./conan-center-index/recipes/zlib/all --version 1.3.1 -pr:h </my/runner/folder>/docker_example_host -pr:b </my/runner/folder>/docker_example_build

    ...

    ****************************************************
    * Building the Docker image: my-conan-runner-image *
    ****************************************************

    Dockerfile path: '</my/runner/folder>/Dockerfile'
    Docker build context: '</my/runner/folder>'

    Step 1/5 : ARG BASE_IMAGE

    Step 2/5 : FROM $BASE_IMAGE

    ...

    Successfully built 286df085400f
    Successfully tagged my-conan-runner-image:latest

    ...

    *********************************
    * Creating the docker container *
    *********************************


    *******************************************
    * Container my-conan-runner-image running *
    *******************************************


    *******************************************
    * Running in container: "conan --version" *
    *******************************************

    ************************************************************************************************************************
    * Restore host cache from: </my/runner/folder>/conan-center-index/recipes/zlib/all/.conanrunner/docker_cache_save.tgz *
    ************************************************************************************************************************

    Restore: zlib/1.3.1 in p/zlib95420566fc0dd
    Restore: zlib/1.3.1:b647c43bfefae3f830561ca202b6cfd935b56205 in p/zlibd59462fc4358e/p
    Restore: zlib/1.3.1:b647c43bfefae3f830561ca202b6cfd935b56205 metadata in p/zlibd59462fc4358e/d/metadata

    **********************
    * Stopping container *
    **********************

If we now check the status of our Conan and docker cache, we will see the zlib package compiled for Linux and the new docker image and container.

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
    CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS                       PORTS     NAMES
    1379072ae424   my-conan-runner-image   "/bin/bash -c 'while…"   17 seconds ago   Exited (137) 2 seconds ago             my-conan-runner-image

    $ docker images  
    REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
    my-conan-runner   latest    383b905f352e   22 minutes ago   531MB
    ubuntu            22.04     437ec753bef3   12 days ago      77.9MB

If we run the ``conan create`` command again we will see how Conan reuses the previous container because we have set ``remove=False``.

.. code-block:: bash
    
    $ conan create ./conan-center-index/recipes/zlib/all --version 1.3.1 -pr:h </my/runner/folder>/docker_example_host -pr:b </my/runner/folder>/docker_example_build

    ...

    *********************************
    * Starting the docker container *
    *********************************

    ...
