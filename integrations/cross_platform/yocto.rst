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

Creating packages with Yocto's SDK toolchain
============================================

Yocto SDKs are completely self-contained. The binaries are linked against
their own copy of `libc`, which results in no dependencies on the target
system.

You can start creating Conan packages directly setting up the environment of the Yocto SDK and running a :command:`conan create` command
with a suitable profile with the architecture of the toolchain.

For example, creating packages for `armv5`:

The profile will be:

.. code-block:: text

    [settings]


.. code-block:: bash

    $ source oe-activate-environment <NAME>
    $ conan create . user/channel --profile <PROFILE>
    $ 

.. seealso::

    You can `create your own Yocto SDKs <https://www.yoctoproject.org/docs/2.6/sdk-manual/sdk-manual.html#sdk-building-an-sdk-installer>`_
    or download and use
    `the prebuilt ones <http://downloads.yoctoproject.org/releases/yocto/yocto-2.6.2/toolchain/x86_64/>`_.

Consuming Yocto packages
========================

Conversion table
****************

Use Conan packages in a Yocto build
===================================


.. |yocto_logo| image:: ../../images/yocto/conan_yocto.png
                 :width: 180px

.. _`Yocto Project`: https://www.yoctoproject.org/

.. _`OpenEmbedded`: http://www.openembedded.org/wiki/Main_Page