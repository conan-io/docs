.. _docker_conan:

How to run Conan with Docker
============================

With Docker, you can run different virtual Linux operating systems in a Linux, Mac OSX or Windows machine.
It is useful to reproduce build environments, for example to automate CI processes. You can have
different images with different compilers or toolchains and run containers every time is needed.

We provide :ref:`list of pre-built images<available_docker_images>` with common
build tools and compilers and of course, with Conan installed.


Using conan inside a container
------------------------------

.. code-block:: bash

    docker run -it --rm lasote/conangcc7 /bin/bash

The previous code will run a shell in container. We have specified:

- ``-it``: Keep STDIN open and allocate a pseudo-tty, in other words, we want to type in the container because we are opening a bash.
- ``--rm``: Once the container exits, remove the container. Helps to keep clean or hard drive.
- ``lasote/conangcc7``: Image name, check the :ref:`available docker images<available_docker_images>`.
- ``/bin/bash``: The command to run


Now we are running on the conangcc7 container we can use Conan normally. It is always recommended
to upgrade conan from pip first:

.. code-block:: bash

    $ sudo pip install conan --upgrade
    $ git clone https://github.com/conan-community/conan-openssl
    $ cd conan-openssl
    $ conan create . user/channel


Sharing a local folder with a docker container
----------------------------------------------

You can share a local folder with your container, for example a project:

.. code-block:: bash

    $ git clone https://github.com/conan-community/conan-openssl
    $ cd conan-openssl
    $ docker run -it -v$(pwd):/home/conan/project --rm lasote/conangcc7 /bin/bash


- ``v$(pwd):/home/conan/project``: We are mapping the current directory (conan-openssl) to the container
  ``/home/conan/project`` directory, so anything we change in this shared folder, will be really changed
  in our host machine.

.. code-block:: bash

    # Now we are running on the conangcc7 container
    $ sudo pip install conan --upgrade
    $ cd project
    $ conan create . user/channel --build missing
    $ conan remote add myremote http://some.remote.url
    $ conan upload "*" -r myremote --all


Using the images to cross-build packages
----------------------------------------

You can use the :ref:`images<available_docker_images>` ``-i386``, ``-armv7`` and ``-armv7gh`` to cross build
conan packages.

The ``armv7`` images have a cross toolchain for linux ARM installed, and declared as main compiler with the
environment variables ``CC`` and ``CXX``. Also, the default Conan profile (``~/.conan/profiles/default``)
is adjusted to declare the correct arch (``armv7`` / ``armv7hf``).


.. code-block:: bash

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

We can cross build a package and all the missing dependencies for ``Linux/armv7hf`` and
finally uploading the built packages to a repository:

.. code-block:: bash

    $ git clone https://github.com/conan-community/conan-openssl
    $ cd conan-openssl
    $ docker run -it -v$(pwd):/home/conan/project --rm lasote/conangcc49-armv7hf /bin/bash

    # Now we are running on the conangcc49-armv7hf container
    $ sudo pip install conan --upgrade
    $ cd project

    $ conan create . user/channel --build missing
    $ conan remote add myremoteARMV7 http://some.remote.url
    $ conan upload "*" -r myremoteARMV7 --all


.. _available_docker_images:

Available docker images
-----------------------

**GCC** images

+--------------------------------------------------------------------------------------------+----------------+
| **Version**                                                                                | **Target Arch**|
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc49: gcc 4.9 <https://hub.docker.com/r/lasote/conangcc49/>`_                | x86_64         |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc49-i386: gcc 4.9 <https://hub.docker.com/r/lasote/conangcc49-i386/>`_      | x86            |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc49-armv7: gcc 4.9 <https://hub.docker.com/r/lasote/conangcc49-armv7/>`_    | armv7          |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc49-armv7hf: gcc 4.9 <https://hub.docker.com/r/lasote/conangcc49-armv7hf/>`_| armv7hf        |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc5-armv7: gcc 5 <https://hub.docker.com/r/lasote/conangcc5-armv7/>`_        | armv7          |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc5-armv7hf: gcc 5 <https://hub.docker.com/r/lasote/conangcc5-armv7hf/>`_    | armv7hf        |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc5: gcc 5 <https://hub.docker.com/r/lasote/conangcc5/>`_                    | x86_64         |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc5-i386: gcc 5 <https://hub.docker.com/r/lasote/conangcc5-i386/>`_          | x86            |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc5-armv7: gcc 5 <https://hub.docker.com/r/lasote/conangcc5-armv7/>`_        | armv7          |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc5-armv7hf: gcc 5 <https://hub.docker.com/r/lasote/conangcc5-armv7hf/>`_    | armv7hf        |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc6: gcc 6 <https://hub.docker.com/r/lasote/conangcc6/>`_                    | x86_64         |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc6-i386: gcc 6 <https://hub.docker.com/r/lasote/conangcc6-i386/>`_          | x86            |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc6-armv7: gcc 6 <https://hub.docker.com/r/lasote/conangcc6-armv7/>`_        | armv7          |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc6-armv7hf: gcc 6 <https://hub.docker.com/r/lasote/conangcc6-armv7hf/>`_    | armv7hf        |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc7-i386: gcc 7 <https://hub.docker.com/r/lasote/conangcc7-i386/>`_          | x86            |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc7: gcc 7 <https://hub.docker.com/r/lasote/conangcc7/>`_                    | x86_64         |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc7-armv7: gcc 7 <https://hub.docker.com/r/lasote/conangcc7-armv7/>`_        | armv7          |
+--------------------------------------------------------------------------------------------+----------------+
| `lasote/conangcc7-armv7hf: gcc 7 <https://hub.docker.com/r/lasote/conangcc7-armv7hf/>`_    | armv7hf        |
+--------------------------------------------------------------------------------------------+----------------+


**Clang images**

+--------------------------------------------------------------------------------------------+-------------+
| Version                                                                                    | Target Arch |
+--------------------------------------------------------------------------------------------+-------------+
| `lasote/conanclang38: clang 3.8 <https://hub.docker.com/r/lasote/conanclang38/>`_          | x86_64      |
+--------------------------------------------------------------------------------------------+-------------+
| `lasote/conanclang39-i386: clang 3.9 <https://hub.docker.com/r/lasote/conanclang39-i386/>`_| x86         |
+--------------------------------------------------------------------------------------------+-------------+
| `lasote/conanclang39: clang 3.9 <https://hub.docker.com/r/lasote/conanclang39/>`_          | x86_64      |
+--------------------------------------------------------------------------------------------+-------------+
| `lasote/conanclang40-i386: clang 4.0 <https://hub.docker.com/r/lasote/conanclang40/-i386>`_| x86         |
+--------------------------------------------------------------------------------------------+-------------+
| `lasote/conanclang40: clang 4.0 <https://hub.docker.com/r/lasote/conanclang40/>`_          | x86_64      |
+--------------------------------------------------------------------------------------------+-------------+
| `lasote/conanclang50-i386: clang 5.0 <https://hub.docker.com/r/lasote/conanclang50-i386/>`_| x86         |
+--------------------------------------------------------------------------------------------+-------------+
| `lasote/conanclang50: clang 5.0 <https://hub.docker.com/r/lasote/conanclang50/>`_          | x86_64      |
+--------------------------------------------------------------------------------------------+-------------+


The Dockerfiles for all these images can be found `here <https://github.com/conan-io/conan-docker-tools>`_.