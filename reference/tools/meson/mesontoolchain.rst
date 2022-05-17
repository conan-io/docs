.. _conan_tools_meson_mesontoolchain:

MesonToolchain
==============

The ``MesonToolchain`` is the toolchain generator for Meson and it can be used in the ``generate()`` method
as follows:


.. code:: python

    from conan import ConanFile
    from conan.tools.meson import MesonToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False]}
        default_options = {"shared": False}

        def generate(self):
            tc = MesonToolchain(self)
            tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
            tc.generate()


.. important::

    The ``MesonToolchain`` only works with the ``PkgConfigDeps`` generator.
    Please, do not use other generators, as they can have overlapping definitions that can conflict.


Generated files
-----------------

This will generate the following files after a :command:`conan install` (or when building the package
in the cache) with the information provided in the ``generate()`` method as well as information
translated from the current ``settings``, ``conf``, etc.:

-  *conan_meson_native.ini*: if doing a native build.
-  *conan_meson_cross.ini*: if doing a cross-build (:ref:`conan_tools_build`).

conan_meson_native.ini
+++++++++++++++++++++++++

This file contains the definitions of all the Meson properties related to the Conan options
and settings for the current package, platform, etc. This includes but is not limited to the following:

* Detection of ``default_library`` from Conan settings.

    * Based on existance/value of a option named ``shared``.

* Detection of ``buildtype`` from Conan settings.

* Definition of the C++ standard as necessary.

* The Visual Studio runtime (``b_vscrt``), obtained from Conan input settings.


conan_meson_cross.ini
++++++++++++++++++++++++

This file will contain the same information as the previous *conan_meson_native.ini*,
but with additional information to describe host, target, and build machines (such as the processor architecture).


Check out the meson documentation for more details on native and cross files:

* `Machine files <https://mesonbuild.com/Machine-files.html>`_
* `Native environments <https://mesonbuild.com/Native-environments.html>`_
* `Cross compilation <https://mesonbuild.com/Cross-compilation.html>`_


Customization
---------------

Attributes
+++++++++++++

definitions
^^^^^^^^^^^^

This attribute allows defining Meson project options:

.. code:: python

    def generate(self):
        tc = MesonToolchain(self)
        tc.definitions["MYVAR"] = "MyValue"
        tc.generate()

This will be translated to:

- One project options definition for ``MYVAR`` in ``conan_meson_native.init`` or ``conan_meson_cross.ini`` file.

preprocessor_definitions
^^^^^^^^^^^^^^^^^^^^^^^^

This attribute allows defining compiler preprocessor definitions, for multiple configurations (Debug, Release, etc).

.. code:: python

    def generate(self):
        tc = MesonToolchain(self)
        tc.preprocessor_definitions["MYDEF"] = "MyValue"
        tc.generate()

This will be translated to:

- One preprocessor definition for ``MYDEF`` in ``conan_meson_native.ini`` or ``conan_meson_cross.ini`` file.

.. note::

    You can have a look at the rest of the public attributes in the
    :ref:`MesonToolchain class Reference<MesonToolchain Reference>`

conf
++++++

``MesonToolchain`` is affected by these ``[conf]`` variables:

- ``tools.meson.mesontoolchain:backend``. the meson `backend
  <https://mesonbuild.com/Configuring-a-build-directory.html>`_ to use. Possible values:
  ``ninja``, ``vs``, ``vs2010``, ``vs2015``, ``vs2017``, ``vs2019``, ``xcode``.
- ``tools.apple:sdk_path`` argument for SDK path in case of Apple cross-compilation. It will be used as value
  of the flag ``-isysroot``.
- ``tools.android:ndk_path`` argument for NDK path in case of Android cross-compilation. It will be used to get
  some binaries like ``c``, ``cpp`` and ``ar`` used in ``[binaries]`` section from *conan_meson_cross.ini*.
- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``cpp_args``.
- ``tools.build:cflags`` list of extra of pure C flags that will be used by ``c_args``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``c_link_args`` and ``cpp_link_args``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by ``c_link_args`` and ``cpp_link_args``.


Extending and advanced customization
------------------------------------

Using the toolchain in developer flow
+++++++++++++++++++++++++++++++++++++

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


Cross-building for Apple and Android
+++++++++++++++++++++++++++++++++++++

 The ``MesonToolchain`` automatically adds all the flags needed
to cross-compile for Apple (MacOS M1, iOS, etc.) and Android.

**Apple**

It adds link flags ``-arch XXX``, ``-isysroot [SDK_PATH]`` and the minimum deployment target flag, e.g., ``-mios-version-min=8.0``
into Meson ``c_args``, ``c_link_args``, ``cpp_args`` and ``cpp_link_args`` built-in options.

**Android**

It initializes the ``c``, ``cpp`` and ``ar`` variables which are needed to cross-compile for Android. For instance:

* ``c == $TOOLCHAIN/bin/llvm-ar``
* ``cpp == $TOOLCHAIN/bin/$TARGET$API-clang``
* ``ar == $TOOLCHAIN/bin/$TARGET$API-clang++``

Where:

* ``$TOOLCHAIN``: ``[NDK_PATH]/toolchains/llvm/prebuilt/[OS_BUILD]-x86_64/bin``.
* ``$TARGET``: target triple, e.g., for ``armv8`` will be ``aarch64-linux-android``.
* ``$API``: Android API version.

Besides that, you'll always be able to change any of these variables before being applied thanks
to the ``MesonToolchain`` class interface. For instance:

.. code:: python

    from conan import ConanFile
    from conan.tools.meson import MesonToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False]}
        default_options = {"shared": False}

        def generate(self):
            tc = MesonToolchain(self)
            tc.cpp = "/path/to/other/compiler"
            tc.generate()

.. _MesonToolchain Reference:

Reference
---------

.. currentmodule:: conan.tools.meson

.. autoclass:: MesonToolchain
    :members:
