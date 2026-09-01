.. _docker_conan:

How to use Docker to create C and C++ Conan packages
====================================================================

With Docker, you can run different virtual Linux operating systems in a Linux, Mac OSX or Windows machine.
It is useful to reproduce build environments, for example to automate CI processes. You can have
different images with different compilers or toolchains and run containers every time is needed.

In this section you will find a :ref:`list of pre-built images<available_docker_images>` with common
build tools and compilers as well as Conan installed.


Using Conan inside a container
------------------------------

.. code-block:: bash

    $ docker run -it --rm --name conangcc11 conanio/gcc11-ubuntu16.04 /bin/bash


.. note::

    Use ``sudo`` when needed to run ``docker``.

The previous code will run a shell in container. We have specified:

- :command:`-it`: Keep STDIN open and allocate a pseudo-tty, in other words, we want to type in the container because we are opening a bash.
- :command:`--rm`: Once the container exits, remove the container. Helps to keep clean or hard drive.
- :command:`--name conangcc11``: The Docker container name
- :command:`conanio/gcc11-ubuntu16.04`: Image name, check the :ref:`available Docker images<available_docker_images>`.
- :command:`/bin/bash`: The command to run


Now we are running on the conangcc11 container we can use Conan normally. In the following example we are
creating a package from the recipe by cloning the repository, for OpenSSL.
It is always recommended to upgrade Conan from pip first:

.. code-block:: bash

    $ pip install conan --upgrade # We make sure we are running the latest Conan version
    $ git clone https://github.com/conan-io/conan-center-index
    $ cd conan-center-index/recipes/openssl/1.x.x
    $ conan create . 1.1.1n@


Sharing a local folder with a Docker container
----------------------------------------------

You can share a local folder with your container, for example a project:

.. code-block:: bash

    $ git clone https://github.com/conan-io/conan-center-index
    $ cd conan-center-index/recipes/openssl/1.x.x
    $ docker run -it -v$(pwd):/home/conan/project --rm conanio/gcc11-ubuntu16.04 /bin/bash


- ``v$(pwd):/home/conan/project``: We are mapping the current directory (conan-openssl) to the container
  ``/home/conan/project`` directory, so anything we change in this shared folder, will be reflected
  in our host machine.

.. code-block:: bash

    # Now we are running on the conangcc11 container
    $ pip install conan --upgrade # We make sure we are running the latest Conan version
    $ cd project
    $ conan create . user/channel --build missing
    $ conan remote add myremote http://some.remote.url
    $ conan upload "*" -r myremote --all

.. _available_docker_images:

Available Docker images
-----------------------

We provide a set of images with the most common compilers installed that can be used to generate Conan packages for different profiles.
Their dockerfiles can be found in the `Conan Docker Tools <https://github.com/conan-io/conan-docker-tools>`_ repository.

.. warning::

    The images listed below are intended for generating open-source library packages and we cannot guarantee any kind of stability.
    We strongly recommend using your own generated images for production environments taking these dockerfiles as a reference.

**GCC** images

+----------------------------------------------------------------------------------------------+----------------+
| **Version**                                                                                  | **Target Arch**|
+----------------------------------------------------------------------------------------------+----------------+
| `conanio/gcc5-ubuntu16.04 (GCC 5) <https://hub.docker.com/r/conanio/gcc5-ubuntu16.04/>`_     | x86_64         |
+----------------------------------------------------------------------------------------------+----------------+
| `conanio/gcc6-ubuntu16.04 (GCC 6) <https://hub.docker.com/r/conanio/gcc6-ubuntu16.04/>`_     | x86_64         |
+----------------------------------------------------------------------------------------------+----------------+
| `conanio/gcc7-ubuntu16.04 (GCC 7) <https://hub.docker.com/r/conanio/gcc7-ubuntu16.04/>`_     | x86_64         |
+----------------------------------------------------------------------------------------------+----------------+
| `conanio/gcc8-ubuntu16.04 (GCC 8) <https://hub.docker.com/r/conanio/gcc8-ubuntu16.04/>`_     | x86_64         |
+----------------------------------------------------------------------------------------------+----------------+
| `conanio/gcc9-ubuntu16.04 (GCC 9) <https://hub.docker.com/r/conanio/gcc9-ubuntu16.04/>`_     | x86_64         |
+----------------------------------------------------------------------------------------------+----------------+
| `conanio/gcc10-ubuntu16.04 (GCC 10) <https://hub.docker.com/r/conanio/gcc10-ubuntu16.04/>`_  | x86_64         |
+----------------------------------------------------------------------------------------------+----------------+
| `conanio/gcc11-ubuntu16.04 (GCC 11) <https://hub.docker.com/r/conanio/gcc11-ubuntu16.04/>`_  | x86_64         |
+----------------------------------------------------------------------------------------------+----------------+



**Clang** images

+-------------------------------------------------------------------------------------------------------+------------------+
| Version                                                                                               | **Target Arch**  |
+-------------------------------------------------------------------------------------------------------+------------------+
| `conanio/clang10-ubuntu16.04 (Clang 10) <https://hub.docker.com/r/conanio/clang10-ubuntu16.04/>`_     | x86_64           |
+-------------------------------------------------------------------------------------------------------+------------------+
| `conanio/clang11-ubuntu16.04 (Clang 11) <https://hub.docker.com/r/conanio/clang11-ubuntu16.04/>`_     | x86_64           |
+-------------------------------------------------------------------------------------------------------+------------------+
| `conanio/clang12-ubuntu16.04 (Clang 12) <https://hub.docker.com/r/conanio/clang12-ubuntu16.04/>`_     | x86_64           |
+-------------------------------------------------------------------------------------------------------+------------------+
| `conanio/clang13-ubuntu16.04 (Clang 13) <https://hub.docker.com/r/conanio/clang13-ubuntu16.04/>`_     | x86_64           |
+-------------------------------------------------------------------------------------------------------+------------------+
| `conanio/clang14-ubuntu16.04 (Clang 14) <https://hub.docker.com/r/conanio/clang14-ubuntu16.04/>`_     | x86_64           |
+-------------------------------------------------------------------------------------------------------+------------------+
