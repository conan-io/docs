.. _buildroot_integration:


|buildroot_logo| Buildroot
__________________________

The `Buildroot Project`_ is a tool for automating the creation of Embedded Linux distributions. It
builds the code for the architecture of the board so it was set up, all through an overview of
Makefiles. In addition to being open-source, it is licensed under `GPL-2.0-or-later`_.

Integration with Conan
======================

Let's create a new file called **pkg-conan.mk** in the `package/` directory. At the same time, we
need to add it in `package/Makefile.in` file in order to Buildroot be able to list it.

.. code-block:: bash

    echo 'include package/pkg-conan.mk' >> package/Makefile.in

For this development we will break it down into a few steps. Because it is a large file, we will
only portray parts of it in this post, but the full version can be found in `pkg-conan.mk`_.

Buildroot defines its settings, including processor, compiler version, and build type through
variables. However, these variables do not have directly valid values for Conan, so we need to
parse most of them. Let's start with the compiler version, by default Buildroot uses a GCC-based
toolchain, so we will only filter on its possible versions:

.. code-block:: makefile

    CONAN_SETTING_COMPILER_VERSION  ?=
    ifeq ($(BR2_GCC_VERSION_8_X),y)
    CONAN_SETTING_COMPILER_VERSION = 8
    else ifeq ($(BR2_GCC_VERSION_7_X),y)
    CONAN_SETTING_COMPILER_VERSION = 7
    else ifeq ($(BR2_GCC_VERSION_6_X),y)
    CONAN_SETTING_COMPILER_VERSION = 6
    else ifeq ($(BR2_GCC_VERSION_5_X),y)
    CONAN_SETTING_COMPILER_VERSION = 5
    else ifeq ($(BR2_GCC_VERSION_4_9_X),y)
    CONAN_SETTING_COMPILER_VERSION = 4.9
    endif

This same process should be repeated for build_type, arch, and so on.
For the Conan package installation step we will have the following routine:

.. code-block:: makefile

    define $(2)_BUILD_CMDS
        $$(TARGET_MAKE_ENV) $$(CONAN_ENV) $$($$(PKG)_CONAN_ENV) \
            CC=$$(TARGET_CC) CXX=$$(TARGET_CXX) \
            $$(CONAN) install $$(CONAN_OPTS) $$($$(PKG)_CONAN_OPTS) \
            $$($$(PKG)_REFERENCE) \
            -s build_type=$$(CONAN_SETTING_BUILD_TYPE) \
            -s arch=$$(CONAN_SETTING_ARCH) \
            -s compiler=$$(CONAN_SETTING_COMPILER) \
            -s compiler.version=$$(CONAN_SETTING_COMPILER_VERSION) \
            -g deploy \
            --build $$(CONAN_BUILD_POLICY)
    endef

The :command:`conan install` command will be executed as usual, but the settings and options are configured
through what was previously collected from Buildroot, and accept new ones through the Buildroot
package recipe. Because it was a scenario where previously all sources were compiled in the first
moment, we will set Conan build policy to ``missing``, so any package will be built if not available.

Also, note that we are using the generator :ref:`deploy <deploy_generator>`, as we will need to copy all the artifacts into
the Buildroot internal structure. Once built, we will copy the libraries, binaries and headers
through the following routine:

.. code-block:: makefile

    define $(2)_INSTALL_CMDS
        cp -f -a $$($$(PKG)_BUILDDIR)/bin/. /usr/bin 2>/dev/null || :
        cp -f -a $$($$(PKG)_BUILDDIR)/lib/. /usr/lib 2>/dev/null || :
        cp -f -a $$($$(PKG)_BUILDDIR)/include/. /usr/include 2>/dev/null || :
    endef


With this script we will be able to install the vast majority of Conan packages, using only simpler
information for each Buildroot recipe.

Creating Conan packages with Buildroot
======================================

Installing Conan Zlib
---------------------

Once we have our script for installing Conan packages, now let's install a fairly simple and
well-known project: `zlib <https://www.zlib.net>`_.
For this case we will create a new recipe in the package directory. Let's start with the package
configuration file:

.. code-block:: bash

    mkdir package/conan-zlib
    touch package/conan-zlib/Config.in
    touch package/conan-zlib/conan-zlib.mk

The contents of the file *Config.in* should be as follows:

.. code-block:: text

   config BR2_PACKAGE_CONAN_ZLIB
    bool "conan-zlib"
    help
      Standard (de)compression library. Used by things like
      gzip and libpng.

      http://www.zlib.net

Now let's go to the *conan-zlib.mk* that contains the Zlib data:

.. code-block:: makefile

    # conan-zlib.mk
    CONAN_ZLIB_VERSION = 1.2.11
    CONAN_ZLIB_LICENSE = Zlib
    CONAN_ZLIB_LICENSE_FILES = licenses/LICENSE
    CONAN_ZLIB_SITE = $(call github,conan-community,conan-zlib,92d34d0024d64a8f307237f211e43ab9952ef0a1)
    CONAN_ZLIB_REFERENCE = zlib/$(CONAN_ZLIB_VERSION)@conan/stable

    $(eval $(conan-package))

An important note here is the fact that ``CONAN_ZLIB_SITE`` is required even if not used for our
purpose. If it is not present, Buildroot will raise an error during its execution.
The other variables are simple, just expressing the package reference, name, version and license.
Note that in the end we are calling our script which should execute Conan.

Once created, we still need to add it to the Buildroot configuration list.
To do so, let's update the list with a new menu named *Conan*. In *package/Config.in* file,
let's add the following section:

.. code-block:: text

    menu "Conan"
        source "package/conan-zlib/Config.in"
    endmenu

Now just select the package through **menuconfig**: `Target Packages -> Conan -> conan-zlib`

|buildroot_menuconfig_conan|

Once configured and saved, simply run :command:`make` again to install the package.

As you can see, Conan is following the same profile used by Buildroot, which gives us the advantage
of not having to create a profile manually.

At the end of the installation it will be copied to the output directory.

Customizing Conan remote
========================

Let's say we have an :ref:`Artifatory <artifactory_ce>` instance where all packages are available
for download. How could we customize the remote used by Buildroot? We need to introduce a new
option, where we can write the remote name and Conan will be able to consume such variable. First
we need to create a new configuration file to insert new options in Conan's menu:

.. code-block:: bash

    mkdir package/conan
    touch package/conan/Config.in

The file *Config.in* should contain:

.. code-block:: text

    config CONAN_REMOTE_NAME
	    string "Conan remote name"
        help
	      Look in the specified remote server.

Also, we need to parse the option ``CONAN_REMOTE_NAME`` in *pkg-conan.mk* and add it to Conan
command line:

.. code-block:: makefile

    ifneq ($(CONAN_REMOTE_NAME),"")
    CONAN_REMOTE = -r $$(CONAN_REMOTE_NAME)
    endif

    define $(2)_BUILD_CMDS
        $$(TARGET_MAKE_ENV) $$(CONAN_ENV) $$($$(PKG)_CONAN_ENV) \
            CC=$$(TARGET_CC) CXX=$$(TARGET_CXX) \
            $$(CONAN) install $$(CONAN_OPTS) $$($$(PKG)_CONAN_OPTS) \
            $$($$(PKG)_REFERENCE) \
            -s build_type=$$(CONAN_SETTING_BUILD_TYPE) \
            -s arch=$$(CONAN_SETTING_ARCH) \
            -s compiler=$$(CONAN_SETTING_COMPILER) \
            -s compiler.version=$$(CONAN_SETTING_COMPILER_VERSION) \
            -g deploy \
            --build $$(CONAN_BUILD_POLICY) \
            $$(CONAN_REMOTE)
    endef


Now we are ready to set our specific remote name. We only need to run :command:`make menuconfig` and
follow the path: `Target Packages -> Libraries -> Conan -> Conan remote name`

And we will see:

|buildroot_custom_remote|

Now Conan is configured to search for packages in the remote named *artifactory*. But we need to
run :command:`make` again. Note that it will cost less time to build, since now we are using pre-built
packages provided by Conan.

If no errors have occurred during the process we will have the following output folder:

.. code-block:: bash

    ls output/images/
        bcm2710-rpi-3-b.dtb bcm2710-rpi-3-b-plus.dtb bcm2710-rpi-cm3.dtb boot.vfat rootfs.ext2 rootfs.ext4 rpi-firmware sdcard.img zImage

    ls -lh output/images/sdcard.img
        -rw-r--r-- 1 conan conan 153M ago  6 11:43 output/images/sdcard.img

These artifacts are the final compilation of everything that was generated during the build
process, here we will be interested in the *sdcard.img* file. This is the final image that we
will use on our *RaspberryPi3* and it is only 153MB. Compared to other embedded distributions like
*Raspbian*, it is much smaller.

If you are interested in knowing more, we have a complete `blog post`_ about Buildroot integration.


.. |buildroot_logo| image:: ../../images/buildroot/conan-buildroot_logo.png
                 :width: 180px

.. |buildroot_menuconfig_conan| image:: ../../images/buildroot/conan-buildroot_menuconfig_conan.png
                 :width: 800px

.. |buildroot_custom_remote| image:: ../../images/buildroot/conan-buildroot_custom_remote.png
                 :width: 500

.. _`Buildroot Project`: https://buildroot.org/
.. _`GPL-2.0-or-later`: https://spdx.org/licenses/GPL-2.0-or-later.html
.. _`blog post`: https://blog.conan.io/2019/08/27/Creating-small-Linux-images-with-Buildroot.html
.. _`pkg-conan.mk`: https://github.com/conan-community/buildroot/blob/feature/conan/package/pkg-conan.mk