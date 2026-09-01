.. _conan-meson-toolchain:

MesonToolchain
==============

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


The ``MesonToolchain`` can be used in the ``generate()`` method:


.. code:: python

    from conans import ConanFile
    from conan.tools.meson import MesonToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False]}
        default_options = {"shared": False}

        def generate(self):
            tc = MesonToolchain(self)
            tc.generate()


The ``MesonToolchain`` will generate the following file during ``conan install``
command (or before calling the ``build()`` method when the package is being
built in the cache): ``conan_meson_native.ini``

``conan_meson_native.ini`` will contain the definitions of all the Meson properties
related to the Conan options and settings for the current package, platform,
etc. This includes but is not limited to the following:

* Detection of ``default_library`` from Conan settings

  * Based on existance/value of a option named ``shared``

* Detection of ``buildtype`` from Conan settings

* Definition of the C++ standard as necessary

* The Visual Studio runtime (``b_vscrt``), obtained from Conan input settings

Generators
----------

The ``MesonToolchain`` only works with the ``pkg_config`` generator.
Please, do not use other generators, as they can have overlapping definitions that can conflict.


Using the toolchain in developer flow
-------------------------------------

One of the advantages of using Conan toolchains is that they can help to achieve the exact same build
with local development flows, than when the package is created in the cache.

With the ``MesonToolchain`` it is possible to do:

.. code:: bash

    # Lets start in the folder containing the conanfile.py
    $ mkdir build && cd build
    # Install both debug and release deps and create the toolchain
    $ conan install ..
    # the build type Release is encoded in the toolchain already.
    # This conan_meson_native.iniis specific for release
    $ meson setup --native-file conan_meson_native.ini build .
    $ meson compile -C build
