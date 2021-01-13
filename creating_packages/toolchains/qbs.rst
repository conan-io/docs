.. _conan-qbs-toolchain:

QbsToolchain
==============

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


The ``QbsToolchain`` can be used in the ``generate()`` method:


.. code:: python

    from conans import ConanFile
    from conan.tools.meson import QbsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False]}
        default_options = {"shared": False}

        def generate(self):
            tc = QbsToolchain(self)
            tc.generate()


The ``QbsToolchain`` will generate the following file during :command:`conan install`
command (or before calling the ``build()`` method when the package is being
built in the cache): *conan_toolchain.qbs*. This file will contain a qbs profile
named *conan_toolchain_profile*.


*conan_toolchain.qbs* will contain the definitions of all the Qbs properties
related to the Conan options and settings for the current package, platform,
etc. This includes the following:

* Detection of compiler

  * Based on the compiler set in environment variable ``CC``

  * Uses detected system compiler based on Conan setting ``compiler`` if environment variable ``CC`` is not set.

* Detection of compiler flags from environment (as defined at https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html):

  * ``ASFLAGS``

  * ``CFLAGS``

  * ``CPPFLAGS``

  * ``CXXFLAGS``

  * ``LDFLAGS``

* Detection of sysroot from environment.

* Detection of ``build_type`` from Conan settings.

* Detection of ``arch`` from Conan settings.

* Detection of ``compiler.cxxstd`` from Conan settings.

* Detection of ``fPIC`` based on the existence of such option in the recipe.
