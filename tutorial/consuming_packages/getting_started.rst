.. _consuming_packages_getting_started:

Getting started: building your project using a Conan package
============================================================

Let's get started with an example: We are going to create a string compressor application
that uses one of the most popular C++ libraries: Zlib_. The Zlib Conan package is already
stored in a the Conan Center Index repository and Conan will download it for you. In case
there are binaries available for the configuration you are running (os, compiler, etc.)
Conan will bring the needed binaries and link against then, otherwise it will tell you to
compile Zlib from sources and build it automatically.

We'll use CMake as build system in this case but keep in mind that Conan **works with any
build system** and is not limited to using CMake. You can check more examples with other
build systems in the :ref:`Read More
section<consuming_packages_getting_started_read_more>`.

.. note::

    The source files to recreate this project are available in the `examples2.0 repository`_ in GitHub.
    You can skip the manual creation of the folder and sources with this command:

    .. code-block:: bash

        $ git clone https://github.com/conan-io/examples2.0.git && cd tutorial/consumer/getting_started/string_compressor


Building a CMake project consuming Zlib with Conan
--------------------------------------------------



.. _consuming_packages_getting_started_read_more:

Read more
=========

- Getting started with Autotools
- Getting started with Meson
- ...



.. _`Zlib`: https://zlib.net/
.. _`examples2.0 repository`: https://github.com/conan-io/examples2.0

