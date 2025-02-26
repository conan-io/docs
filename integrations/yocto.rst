.. _integrations_yocto:


|yocto_logo| Yocto
__________________

The `Yocto Project`_ is an open-source project that delivers a set of tools that create operating system images for embedded Linux systems.
The Yocto Project tools are based on the `OpenEmbedded`_ project, which uses the BitBake build tool, to construct complete Linux images.

Yocto supports several Linux host distributions and it also provides a way to install the correct version of these tools by either
downloading a buildtools-tarball or building one on a supported machine. This allows virtually any Linux distribution to be able to run
Yocto, and also makes sure that it will be possible to replicate your Yocto build system in the future. The Yocto Project build system also
isolates itself from the host distribution's C library, which makes it possible to share build caches between different distributions and
also helps in future-proofing the build system.

Integration with Conan
======================

You can create Conan packages building with the Yocto SDK as any other package for other configuration. Those packages can be integrated
into a Yocto build installing them from a remote and without compiling them again.

Three stages can be differentiated in the proposed flow:

1. Developers can create an application with the native tools in their desktop platform of choice using their usual IDE, compiler or
debugger and test the application.

   .. image:: /images/yocto/conan-yocto_development.png
       :height: 600 px
       :width: 600 px
       :align: center

2. Packages can be cross-built for the target device using the Yocto SDK and uploaded to Artifactory, even automated in a CI process.

   .. image:: /images/yocto/conan-yocto_cross-build.png
       :height: 600 px
       :width: 600 px
       :align: center

3. Once the cross-built packages are available in Artifactory, the application can be directly deployed to the Yocto image without building
   it from sources again.

   .. image:: /images/yocto/conan-yocto_deploy.png
       :height: 450 px
       :width: 450 px
       :align: center

Creating Conan packages with Yocto's SDK
========================================

Prepare your recipes
--------------------

First of all, the recipe of the application to be deployed to the final image should have a
:ref:`deploy() method <reference_conanfile_methods_deploy>`. There you can specify the files of the application
needed in the image as well as any other from its dependencies (like shared libraries or assets):

.. code-block:: shell

   conan install
   :caption: *conanfile.py*
   :emphasize-lines: 28-31

    from conan import ConanFile
    from conan.tools.files import copy
    import os


    class FoobarConan(ConanFile):
        name = "foobar"
        ...

    def package(self):
        copy(self, "*.h", dst=os.path.join(self.package_folder, "include"), src="hello")
        copy(self, "*.so", dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.a", dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "foobar", dst=os.path.join(self.package_folder, "bin"), keep_path=False)

    def deploy(self):
        # Deploy everything from this eclipse/mosquitto package
        copy(self, "*", src=self.package_folder, dst=self.deploy_folder)

Another option is using the :ref:`deployers<reference_extensions_deployers>`,
 which will copy all artifacts, including package dependencies to your installation folder.


Setting up a Yocto SDK
----------------------

Yocto SDKs are completely self-contained, there is no dependency on libraries of the build machine or tools installed in it. The SDK is a
cross-building toolchain matching the target and it is generated from that specific configuration. This means that you will have to use a
different SDK toolchain to build for a different target architecture or that some SDK's may have specific settings to enable some system
dependency of the final target and those libraries will be available in the SDK.

You can `create your own Yocto SDKs <https://docs.yoctoproject.org/sdk-manual/appendix-obtain.html#building-an-sdk-installer>`_
or download and use `the prebuilt ones <http://downloads.yoctoproject.org/releases/yocto/yocto-5.1.2/toolchain/x86_64/>`_.

**In the case that you are using CMake** to create the Conan packages, Yocto injects a toolchain that configures CMake to only search for
libraries in the rootpath of the SDK with ``CMAKE_FIND_ROOT_PATH``. This is
something that has to be patched to allow CMake to find libraries in the Conan cache as well:

.. code-block:: cmake
   :caption: *sdk/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake*

    set( CMAKE_FIND_ROOT_PATH $ENV{OECORE_TARGET_SYSROOT} $ENV{OECORE_NATIVE_SYSROOT} )
    set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER )
    # COMMENT THIS: set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY )
    # COMMENT THIS: set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY )
    # COMMENT THIS: set( CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY )

You can read more about those variables here:

  - `CMAKE_FIND_ROOT_PATH_MODE_LIBRARY <https://cmake.org/cmake/help/v3.31/variable/CMAKE_FIND_ROOT_PATH_MODE_LIBRARY.html>`_
  - `CMAKE_FIND_ROOT_PATH_MODE_INCLUDE <https://cmake.org/cmake/help/v3.31/variable/CMAKE_FIND_ROOT_PATH_MODE_INCLUDE.html>`_
  - `CMAKE_FIND_ROOT_PATH_MODE_PACKAGE <https://cmake.org/cmake/help/v3.31/variable/CMAKE_FIND_ROOT_PATH_MODE_PACKAGE.html>`_

Cross-building Conan packages with the SDK toolchain
----------------------------------------------------

After setting up your desired SDK, you can start creating Conan packages setting up the environment of the Yocto SDK and running a
:command:`conan create` command with a suitable profile with the specific architecture of the toolchain.

For example, creating packages for `arch=armv8`:

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

Activate the SDK environment and execute the create command if you have a specific recipe:

.. code-block:: bash

    $ source oe-environment-setup-aarch64-poky-linux
    $ conan create --profile armv8 .

However, if you wish an official Conan package from Conan Center, you can install it directly:

.. code-block:: bash

    $ source oe-environment-setup-aarch64-poky-linux
    $ conan install --requires=mosquitto/2.0.14 -p:b default -p:h armv8 -d runtime_deploy --deployer-folder=deploy


This will generate the packages using the Yocto toolchain from the environment variables such as ``CC``, ``CXX``, ``LD``... Now you can
:ref:`upload the binaries <uploading_packages>` to an Artifactory server to share and reuse in your Yocto builds.

.. code-block:: bash

    $ conan upload -r my_repo mosquitto/2.0.14

.. important::

    We strongly recommend using the Yocto's SDK toolchain to create packages as they will be built with the optimization flags suitable to
    be deployed later to an image generated in a Yocto build.

Deploying an application to a Yocto image
=========================================

Now that you have your cross-built Conan packages in Artifactory, you can deploy them in a Yocto build.

Set up the Conan layer
----------------------

We have created a `meta-conan <https://github.com/conan-io/meta-conan>`_ layer that includes all the configuration, the Conan client and a
generic BitBake recipe. To add the layer you will have to clone the repository and the dependency layers of ``meta-openembedded``:

.. code-block:: bash

    $ cd poky/
    $ git clone --branch conan2/scarthgap https://github.com/conan-io/meta-conan.git
    $ git clone --branch scarthgap https://github.com/openembedded/meta-openembedded.git

You would also have to activate the layers in the *bblayers.conf* file of your build folder:

.. code-block:: text
   :caption: *conf/bblayers.conf*

    POKY_BBLAYERS_CONF_VERSION = "2"

    BBPATH = "${TOPDIR}"
    BBFILES ?= ""

    BBLAYERS ?= " \
    /home/username/poky/meta \
    /home/username/poky/meta-poky \
    /home/username/poky/meta-yocto-bsp \
    /home/username/poky/meta-openembedded/meta-oe \
    /home/username/poky/meta-openembedded/meta-python \
    /home/username/poky/meta-conan \
    "

Or, if you are not confident editing the configuration file or just to automate all process, you can use bitbake commands:

.. code-block:: bash

    $ cd build/
    $ bitbake-layers add-layer ${PWD}/../poky/meta-openembedded/meta-oe
    $ bitbake-layers add-layer ${PWD}/../poky/meta-openembedded/meta-python
    $ bitbake-layers add-layer ${PWD}/../poky/meta-conan

.. note::

    Please report any question, feature request or issue related to the ``meta-conan`` layer in its
    `GitHub issue tracker <https://github.com/conan-io/meta-conan/issues>`_.

Write the Bitbake recipe for the Conan package
----------------------------------------------

With the ``meta-conan`` layer, a Conan recipe to deploy a Conan package should look as easy as this recipe:

.. code-block:: text
   :caption: *conan-mosquitto_2.0.18.bb*

    inherit conan

    DESCRIPTION = "An open source MQTT broker"
    LICENSE = "EPL-1.0"

    CONAN_PKG = "mosquitto/2.0.18@"

This recipe will be placed inside your application layer that should be also added to the *conf/bblayers.conf* file.

Configure Conan variables for the build
---------------------------------------

Additionally to the recipe, you will need to provide the information about the credentials for Artifactory or the profile to be used to
retrieve the packages in the *local.conf* file of your build folder.

.. code-block:: text
   :caption: *poky_build_folder/conf/local.conf*

    IMAGE_INSTALL:append = " conan-mosquitto"

    # Artifactory repository - In case not used, will point to ConanCenter
    CONAN_REMOTE_URL = "https://localhost:8081/artifactory/api/conan/<repository>"
    # Artifactory Credentials
    CONAN_USER = "REPO_USER"
    CONAN_PASSWORD = "REPO_PASSWORD"

The host profile will be detected on the fly, based on the active Yocto SDK environment. The same will be stored in the build folder automatically,
but can be overridden with the ``CONAN_PROFILE_HOST_PATH`` variable. The same applies for ``CONAN_PROFILE_BUILD_PATH``.

Finally, the Artifactory repository URL where you want to retrieve the packages from and its credentials.

You can also use ``CONAN_CONFIG_URL`` with a custom Conan configuration to be used with :command:`conan config install` command. For instance:

.. code-block:: text
   :caption: *poky_build_folder/conf/local.conf*

    IMAGE_INSTALL:append = " conan-mosquitto"

    CONAN_CONFIG_URL = "https://github.com/<your-organization>/conan-config.git"
    CONAN_REMOTE_NAME = "my_repo"
    CONAN_USER = "REPO_USER"
    CONAN_PASSWORD = "REPO_PASSWORD"

In this case, the custom remote will be used to retrieve the packages and the configuration will be installed from the given URL.

Deploy the application and its dependencies to the final image
--------------------------------------------------------------

You can build the recipe to test that the packages are correctly deployed:

.. code-block:: bash

    $ bitbake -c compile conan-mosquitto
    $ bitbake -c install conan-mosquitto

Packages will be built and installed with the profile indicated and installed with its dependencies only from the remote specified.

Finally, you can build your image with the Conan packages:

.. code-block:: bash

    $ bitbake core-image-minimal

The binaries of **the Conan packages will be deployed** to the */bin* folder of the image once it is created.


.. |yocto_logo| image:: ../images/yocto/conan-yocto-logo.png
                 :width: 180px

.. _`Yocto Project`: https://www.yoctoproject.org/

.. _`OpenEmbedded`: http://www.openembedded.org/wiki/Main_Page
