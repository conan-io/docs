.. _yocto_integration:


|yocto_logo| Yocto
__________________

The `Yocto Project`_ is an open-source project that delivers a set of tools that create operating system images for embedded Linux systems.
The Yocto Project tools are based on the `OpenEmbedded`_ project, which uses the BitBake build tool, to construct complete Linux images.

Brief introduction to Yocto
===========================

With these, the Yocto Project covers the needs of both system and application developers. When the Yocto Project is used as an integration
environment for bootloaders, the Linux kernel, and user space applications, we refer to it as system development.
For application development, the Yocto Project builds SDKs that enable the development of applications independently of the Yocto build
system.

Yocto supports several Linux host distributions and it also provides a way to install the correct version of these tools by either
downloading a buildtools-tarball or building one on a supported machine. This allows virtually any Linux distribution to be able to run
Yocto, and also makes sure that it will be possible to replicate your Yocto build system in the future. The Yocto Project build system also
isolates itself from the host distribution's C library, which makes it possible to share build caches between different distributions and
also helps in future-proofing the build system.

Creating Conan packages with Yocto's SDK toolchain
==================================================

Yocto SDKs are completely self-contained. The binaries are linked against their own copy of `libc`, which results in no dependencies on the
target system.

If you are using CMake, then you will have to patch this file in order to avoid linking with other dependencies inside the Yocto SDK, and
force it to use the Conan packages instead:

`sdk/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake`


```
set( CMAKE_FIND_ROOT_PATH $ENV{OECORE_TARGET_SYSROOT} $ENV{OECORE_NATIVE_SYSROOT} )
set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER )
# set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY )
# set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY )
# set( CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY )
```

`OE_CMAKE_TOOLCHAIN_FILE`

Then, you can start creating Conan packages setting up the environment of the Yocto SDK and running a :command:`conan create` command
with a suitable profile with the specific architecture of the toolchain.

For example, creating packages for `armv5`:

The profile will be:

.. code-block:: text
   :caption: *armv8*

    [settings]
    os_build=Linux
    arch_build=x86_64
    os=Linux
    arch=armv8
    compiler=gcc
    compiler.version=8
    compiler.libcxx=libstdc++11
    build_type=Release

And just activate the SDK environment and execute the create command.

.. code-block:: bash

    $ source oe-activate-environment <NAME>
    $ conan create . user/channel --profile armv8

This will generate the packages using the Yocto toolchain. Now you can upload the binaries

.. important::

    We strongly recommend to use the Yocto's SDK toolchain to create packages as they will be built with the optimization flags suitable to
    be deployed later to an image generated in a Yocto build.

.. seealso::

    You can `create your own Yocto SDKs <https://www.yoctoproject.org/docs/2.6/sdk-manual/sdk-manual.html#sdk-building-an-sdk-installer>`_
    or download and use
    `the prebuilt ones <http://downloads.yoctoproject.org/releases/yocto/yocto-2.6.2/toolchain/x86_64/>`_.

Using the Yocto SDK as a build requirement
******************************************

There is also a recipe available to apply the prebuilt Yocto toolchains as a build requirement in this repository <REPO>.

The recipe basically downloads the suitable SDK for your architecture and sets the environment for the toolchain to be applied and used in
the build of the packages.

(INFORMATION ABOUT THE TOOLCHAIN)

Architecture conversion table
+++++++++++++++++++++++++++++

We have decided to map the most common Yocto architectures and machines to the existing ones in Conan. We know that this mapping is not
complete and that some of the binaries generated with the Yocto toolchains will have specific optimization flags for the specific
architectures. However, we think that this mapping is good enough to get started with the Yocto builds.

+---------------+-------------------+------------------------+
| **Yocto SDK** | **Yocto Machine** | **Conan arch setting** |
+===============+===================+========================+
| aarch64       | qemuarm64         | armv8                  |
+---------------+-------------------+------------------------+
| armv5e        | qemuarmv5         | armv5el                |
+---------------+-------------------+------------------------+
| core2-64      | qemux86_64        | x86_64                 |
+---------------+-------------------+------------------------+
| cortexa8hf    | quemuarm          | armv7hf                |
+---------------+-------------------+------------------------+
| i586          | qemux86           | x86                    |
+---------------+-------------------+------------------------+
| mips32r2      | qemumips          | mips                   |
+---------------+-------------------+------------------------+
| mips64        | qemumips64        | mips64                 |
+---------------+-------------------+------------------------+
| ppc7400       | qemuppc           | ppc32                  |
+---------------+-------------------+------------------------+

.. seealso::

    - Prebuilt Yocto's SDKs: http://downloads.yoctoproject.org/releases/yocto/yocto-2.6/toolchain/x86_64/
    - Yocto Machine configurations: https://git.yoctoproject.org/cgit.cgi/poky/tree/meta/conf/machine
    - Conan Architectures in :ref:`settings_yml`.

Deploying Conan packages to a Yocto image
=========================================

Once you have created and and uploaded the Conan packages to a remote in Artifactory, you can deploy them in a Yocto build.

We have created a Yocto layer that includes all the configuration, the Conan client and a generic BitBake recipe so deploying the Conan
packages is as easy as:

.. code-block:: text
   :caption: *conan-mosquitto_1.4.15.bb*

    inherit conan

    DESCRIPTION = "An open source MQTT broker"
    LICENSE = "EPL-1.0"

    CONAN_PKG = "mosquitto/1.4.15@bincrafters/stable"
    CONAN_REMOTE = "ARTIFACTORY_CONAN_REPOSITORY_URL"

You will have to place this recipe inside your own layer and additionally add the configuration of your credentials to the *local.conf* file
of your build folder.

.. code-block:: text
   :caption: *local.conf*

    IMAGE_INSTALL_append = " conan-mosquitto"

    CONAN_USER = "REPO_USER"
    CONAN_PASSWORD = "REPO_PASSWORD"

Now you can build this recipe to test that the packages are correctly deployed:

.. code-block:: bash

    $ bitbake conan-mosquitto
    (ADDD OUTPUT)

After that, you can build your image with the Conan packages:

.. code-block:: bash

    $ bitbake core-image-minimal


.. |yocto_logo| image:: ../../images/yocto/conan_yocto.png
                 :width: 180px

.. _`Yocto Project`: https://www.yoctoproject.org/

.. _`OpenEmbedded`: http://www.openembedded.org/wiki/Main_Page