.. _docker_conan:

How to use Docker to create and cross-build C and C++ Conan packages
====================================================================

With Docker, you can run different virtual Linux operating systems in a Linux, Mac OSX or Windows machine.
It is useful to reproduce build environments, for example to automate CI processes. You can have
different images with different compilers or toolchains and run containers every time is needed.

In this section you will find a :ref:`list of pre-built images<available_docker_images>` with common
build tools and compilers as well as Conan installed.


Using Conan inside a container
------------------------------

.. code-block:: bash

    $ docker run -it --rm conanio/gcc7 /bin/bash


.. note::

    Use ``sudo`` when needed to run ``docker``.

The previous code will run a shell in container. We have specified:

- :command:`-it`: Keep STDIN open and allocate a pseudo-tty, in other words, we want to type in the container because we are opening a bash.
- :command:`--rm`: Once the container exits, remove the container. Helps to keep clean or hard drive.
- :command:`conanio/gcc7`: Image name, check the :ref:`available Docker images<available_docker_images>`.
- :command:`/bin/bash`: The command to run


Now we are running on the conangcc7 container we can use Conan normally. In the following example we are
creating a package from the recipe by cloning the repository, for OpenSSL.
It is always recommended to upgrade Conan from pip first:

.. code-block:: bash

    $ sudo pip install conan --upgrade # We make sure we are running the latest Conan version
    $ git clone https://github.com/conan-community/conan-openssl
    $ cd conan-openssl
    $ conan create . user/channel


Sharing a local folder with a Docker container
----------------------------------------------

You can share a local folder with your container, for example a project:

.. code-block:: bash

    $ git clone https://github.com/conan-community/conan-openssl
    $ cd conan-openssl
    $ docker run -it -v$(pwd):/home/conan/project --rm conanio/gcc7 /bin/bash


- ``v$(pwd):/home/conan/project``: We are mapping the current directory (conan-openssl) to the container
  ``/home/conan/project`` directory, so anything we change in this shared folder, will be reflected
  in our host machine.

.. code-block:: bash

    # Now we are running on the conangcc7 container
    $ sudo pip install conan --upgrade # We make sure we are running the latest Conan version
    $ cd project
    $ conan create . user/channel --build missing
    $ conan remote add myremote http://some.remote.url
    $ conan upload "*" -r myremote --all


Using the images to cross-build packages
----------------------------------------

You can use the :ref:`images<available_docker_images>` ``-i386``, ``-armv7`` and ``-armv7gh`` to cross-build
Conan packages.

The ``armv7`` images have a cross toolchain for linux ARM installed, and declared as main compiler with the
environment variables ``CC`` and ``CXX``. Also, the default Conan profile (``~/.conan/profiles/default``)
is adjusted to declare the correct arch (``armv7`` / ``armv7hf``).

Cross-building and uploading a package along with all its missing dependencies for ``Linux/armv7hf`` is done in few steps:

.. code-block:: bash

    $ git clone https://github.com/conan-community/conan-openssl
    $ cd conan-openssl
    $ docker run -it -v$(pwd):/home/conan/project --rm conanio/gcc49-armv7hf /bin/bash

    # Now we are running on the conangcc49-armv7hf container
    # The default profile is automatically adjusted to armv7hf
    $ cat ~/.conan/profiles/default

    [settings]
    os=Linux
    os_build=Linux
    arch=armv7hf
    arch_build=x86_64
    compiler=gcc
    compiler.version=4.9
    compiler.libcxx=libstdc++
    build_type=Release
    [options]
    [build_requires]
    [env]

    $ sudo pip install conan --upgrade # We make sure we are running the latest Conan version
    $ cd project

    $ conan create . user/channel --build missing
    $ conan remote add myremoteARMV7 http://some.remote.url
    $ conan upload "*" -r myremoteARMV7 --all


.. _available_docker_images:

Available Docker images
-----------------------

We provide a set of images with the most common compilers installed that can be used to generate Conan packages for different profiles.
Their dockerfiles can be found in the `Conan Docker Tools <https://github.com/conan-io/conan-docker-tools>`_ repository.

.. warning::

    The images listed below are intended for generating open-source library packages and we cannot guarantee any kind of stability.
    We strongly recommend using your own generated images for production environments taking these dockerfiles as a reference.

**GCC** images

+--------------------------------------------------------------------------------------+----------------+
| **Version**                                                                          | **Target Arch**|
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc49 (GCC 4.9) <https://hub.docker.com/r/conanio/gcc49/>`_                 | x86_64         |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc49-i386 (GCC 4.9) <https://hub.docker.com/r/conanio/gcc49-i386/>`_       | x86            |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc49-armv7 (GCC 4.9) <https://hub.docker.com/r/conanio/gcc49-armv7/>`_     | armv7          |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc49-armv7hf (GCC 4.9) <https://hub.docker.com/r/conanio/gcc49-armv7hf/>`_ | armv7hf        |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc5-armv7 (GCC 5) <https://hub.docker.com/r/conanio/gcc5-armv7/>`_         | armv7          |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc5-armv7hf (GCC 5) <https://hub.docker.com/r/conanio/gcc5-armv7hf/>`_     | armv7hf        |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc5 (GCC 5) <https://hub.docker.com/r/conanio/gcc5/>`_                     | x86_64         |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc5-i386 (GCC 5)  <https://hub.docker.com/r/conanio/gcc5-i386/>`_          | x86            |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc5-armv7 (GCC 5) <https://hub.docker.com/r/conanio/gcc5-armv7/>`_         | armv7          |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc5-armv7hf (GCC 5)  <https://hub.docker.com/r/conanio/gcc5-armv7hf/>`_    | armv7hf        |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc6 (GCC 6) <https://hub.docker.com/r/conanio/gcc6/>`_                     | x86_64         |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc6-i386 (GCC 6)  <https://hub.docker.com/r/conanio/gcc6-i386/>`_          | x86            |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc6-armv7 (GCC 6)  <https://hub.docker.com/r/conanio/gcc6-armv7/>`_        | armv7          |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc6-armv7hf: (GCC 6)  <https://hub.docker.com/r/conanio/gcc6-armv7hf/>`_   | armv7hf        |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc7-i386 (GCC 7) <https://hub.docker.com/r/conanio/gcc7-i386/>`_           | x86            |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc7 (GCC 7) <https://hub.docker.com/r/conanio/gcc7/>`_                     | x86_64         |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc7-armv7 (GCC 7) <https://hub.docker.com/r/conanio/gcc7-armv7/>`_         | armv7          |
+--------------------------------------------------------------------------------------+----------------+
| `conanio/gcc7-armv7hf (GCC 7) <https://hub.docker.com/r/conanio/gcc7-armv7hf/>`_     | armv7hf        |
+--------------------------------------------------------------------------------------+----------------+


**Clang** images

+--------------------------------------------------------------------------------------+------------------+
| Version                                                                              | **Target Arch**  |
+--------------------------------------------------------------------------------------+------------------+
| `conanio/clang38 (Clang 3.8) <https://hub.docker.com/r/conanio/clang38/>`_           | x86_64           |
+--------------------------------------------------------------------------------------+------------------+
| `conanio/clang39-i386 (Clang 3.9) <https://hub.docker.com/r/conanio/clang39-i386/>`_ | x86              |
+--------------------------------------------------------------------------------------+------------------+
| `conanio/clang39 (Clang 3.9) <https://hub.docker.com/r/conanio/clang39/>`_           | x86_64           |
+--------------------------------------------------------------------------------------+------------------+
| `conanio/clang40-i386 (Clang 4) <https://hub.docker.com/r/conanio/clang40/-i386>`_   | x86              |
+--------------------------------------------------------------------------------------+------------------+
| `conanio/clang40 (Clang 4) <https://hub.docker.com/r/conanio/clang40/>`_             | x86_64           |
+--------------------------------------------------------------------------------------+------------------+
| `conanio/clang50-i386 (Clang 5) <https://hub.docker.com/r/conanio/clang50-i386/>`_   | x86              |
+--------------------------------------------------------------------------------------+------------------+
| `conanio/clang50 (Clang 5) <https://hub.docker.com/r/conanio/clang50/>`_             | x86_64           |
+--------------------------------------------------------------------------------------+------------------+
