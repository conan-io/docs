.. _consuming_packages_cross_building_with_conan:

How to cross-compile your applications using Conan: host and build contexts
===========================================================================

.. important::

    In this example, we will retrieve Conan packages from a Conan repository with
    packages compatible with Conan 2.0. To run this example successfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/consuming_packages/cross_building


In the previous examples, we learned how to use a *conanfile.py* or *conanfile.txt* to
build an application that compresses strings using the *Zlib* and *CMake* Conan packages.
Also, we explained that you can set information like the operating system, compiler or
build configuration in a file called the Conan profile. You can use that profile to call
the ``conan install`` command with the ``--profile`` argument. We also explained that not
specifying that profile is equivalent to using the ``--profile=default`` argument.

For all these examples we used the same platform for building and running the application.
But, what if you want to build the application in your machine running Ubuntu Linux but you would
like that application to run in other platform like, for example, a Raspberry Pi? Conan
can model that case by using two different profiles, one for the machine that **builds**
the application (Ubuntu Linux) and another one for the machine that **runs** the application
(Raspberry Pi). We will explain this "two profiles" approach in the section that follows.

Conan two profiles model: build and host profiles
-------------------------------------------------

Although you can specify only one ``--profile`` argument, Conan will internally use two
profiles. One for the machine that is **building** the binaries (called the **build** profile) and
another for the machine that will **run** those binaries (called the **host** profile). So calling
this command:

.. code-block:: bash

    $ conan install . --build=missing --profile=someprofile

Would be equivalent to:

.. code-block:: bash

    $ conan install . --build=missing --profile:host=someprofile --profile:build=someprofile


As you can see we used two new arguments:

* ``profile:host``: This is the profile that is applied for all the dependencies where the
  built binary is meant to run. For our compressor example, this profile would be the one
  applied for the *Zlib* library that will run in a Raspberry Pi.
* ``profile:build``: This is the profile that is applied for all the dependencies we may
  need for building the binary. For our compressor example this profile would be the one
  applied to the *CMake* tool that will run on the Ubuntu Linux machine.

So, if we want to build the compressor application in the Ubuntu Linux machine but run it in a
Raspberry Pi, we could define two different profiles. The profile for our **build** machine
could look like this:

.. code-block:: bash
    :caption: <conan home>/profiles/ubuntu

    [settings]
    os=Linux
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.cppstd=gnu14
    compiler.libcxx=libstdc++11
    compiler.version=9

And the profile for the Raspberry Pi that is the **host** machine could look like this:

.. code-block:: bash
    :caption: <conan home>/profiles/raspberry

    [settings]
    os=Linux
    arch=armv7hf
    compiler=gcc
    build_type=Release
    compiler.cppstd=gnu14
    compiler.libcxx=libstdc++11
    compiler.version=9
    [buildenv]
    CC=arm-linux-gnueabihf-gcc-9
    CXX=arm-linux-gnueabihf-g++-9
    LD=arm-linux-gnueabihf-ld




Read more
---------

- Using Conan to build for Android
- Using Conan to build for iOS
- Using Conan to build for Raspberry Pi
