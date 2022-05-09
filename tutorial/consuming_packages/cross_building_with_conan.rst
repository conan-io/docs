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
the :command:`conan install` command with the ``--profile`` argument. We also explained that not
specifying that profile is equivalent to using the ``--profile=default`` argument.

For all these examples we used the same platform for building and running the application.
But, what if you want to build the application in your machine running Ubuntu Linux but you would
like that application to run in other platform like, for example, a Raspberry Pi? Conan
can model that case by using two different profiles, one for the machine that **builds**
the application (Ubuntu Linux) and another one for the machine that **runs** the application
(Raspberry Pi). We will explain this "two profiles" approach in the section that follows.

Conan two profiles model: build and host profiles
-------------------------------------------------

Although for every conan command you can specify only one ``--profile`` argument, Conan
will internally use two profiles. One for the machine that is **building** the binaries
(called the **build** profile) and another for the machine that will **run** those
binaries (called the **host** profile). So calling this command:

.. code-block:: bash

    $ conan install . --build=missing --profile=someprofile

Would be equivalent to:

.. code-block:: bash

    $ conan install . --build=missing --profile:host=someprofile --profile:build=someprofile


As you can see we used two new arguments:

* ``profile:host``: This is the profile that is applied for all the dependencies where the
  built binary is meant to run. For our string compressor application this profile would
  be the one applied for the *Zlib* library that will run in a **Raspberry Pi**.
* ``profile:build``: This is the profile that is applied for all the dependencies we may
  need for building the binary. For our string compressor application this profile would
  be the one applied to the *CMake* tool that will run on the **Ubuntu Linux** machine.

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
    :emphasize-lines: 9-12

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

.. important::

    Please, take into account that in order to build this example successfully, you should
    have installed a toolchain that includes the compiler and all the tools to build the
    application for the proper architecture. In this case the host machine is a Raspberry Pi 3
    with *armv7hf* architecture and we already have installed in the Ubuntu machine the
    *arm-linux-gnueabihf* toolchain.

If you have a look at the *raspberry* profile, you will see a new section named
``[buildenv]``. This section is used to set the environment variables that are needed to
build the application. In this case we declare the ``CC``, ``CXX`` and ``LD`` variables
pointing to the cross-build toolchain compilers and linker, respectively. 

Now that we have our two profiles prepared, let's have a look at our *conanfile.py*:

.. code-block:: python
    :caption: **conanfile.py**

    from conan import ConanFile
    from conan.tools.cmake import cmake_layout

    class CompressorRecipe(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeToolchain", "CMakeDeps"

        def requirements(self):
            self.requires("zlib/1.2.11")
            self.tool_requires("cmake/3.19.8")

        def layout(self):
            cmake_layout(self)

As you can see we are using practically the same *conanfile.py* we used in the previous
example. We will require **zlib/1.2.11** as a regular dependency and **cmake/3.19.8** as a
tool needed for building the application. Also, we are using the pre-defined
``cmake_layout``.

We will need the application to be built for the Raspberry Pi with the cross-build
toolchain and also linking the **zlib/1.2.11** library built for the same platform. On the
other side we need the **cmake/3.19.8** binary to run in Ubuntu Linux. Conan manages this
internally in the dependency graph differentiating between what we call the "build
context" and the "host context":

* The **host context** is populated with the root package (the one specified in the
  :command:`conan install` or :command:`conan create` command) and all its requirements.
  In some cases it may also include tools that should run in the host machine (for example
  a test framework that will run in the host machine). In this case this includes the
  compressor application and the **zlib/1.2.11** dependency.

* The **build context** contains the rest of tool requirements and all of them in the
  profiles. This category typically includes all the developer tools like CMake,
  compilers, linkers,... In this case this includes the **cmake/3.19.8** tool.


In general, all the ``requires`` added to the dependency
graph should run in the **host** machine and hence, they will belong to the **host
context**. The ``tool_requires`` will run in the **build** machine and hence, they will
belong to the **host context**.



Read more
---------

- Cross-build using a tool_requires
- Using Conan to build for Android
- Using Conan to build for iOS
