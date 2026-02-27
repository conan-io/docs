.. _conan-meson-toolchain:

MesonToolchain
--------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


Available since: `1.33.0 <https://github.com/conan-io/conan/releases/tag/1.33.0>`_


The ``MesonToolchain`` can be used in the ``generate()`` method:


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


The ``MesonToolchain`` will generate a file:
-  *conan_meson_native.ini*: if doing a native build.
-  *conan_meson_cross.ini*: if doing a cross-build (:ref:`cross_building_reference`).

.. important::

    This class will require very soon to define both the "host" and "build" profiles. It is very recommended to
    start defining both profiles immediately to avoid future breaking. Furthermore, some features, like trying to
    cross-compile might not work at all if the "build" profile is not provided.


``conan_meson_native.ini`` will contain the definitions of all the Meson properties
related to the Conan options and settings for the current package, platform,
etc. This includes but is not limited to the following:

* Detection of ``default_library`` from Conan settings

  * Based on existance/value of a option named ``shared``

* Detection of ``buildtype`` from Conan settings

* Definition of the C++ standard as necessary

* The Visual Studio runtime (``b_vscrt``), obtained from Conan input settings

*conan_meson_cross.ini* contains the same information as *conan_meson_native.ini*,
but with additional information to describe host, target, and build machines (such
as the processor architecture).

Check out the meson documentation for more details on native and cross files:

* `Machine files <https://mesonbuild.com/Machine-files.html>`_
* `Native environments <https://mesonbuild.com/Native-environments.html>`_
* `Cross compilation <https://mesonbuild.com/Cross-compilation.html>`_

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, backend=None):

Most of the arguments are optional and will be deduced from the current ``settings``, and not
necessary to define them.

- ``conanfile``: the current recipe object. Always use ``self``.
- ``backend``: the meson `backend <https://mesonbuild.com/Configuring-a-build-directory.html>`_ to use. By default, ``ninja`` is used. Possible values: ninja, vs, vs2010, vs2015, vs2017, vs2019, xcode.

definitions
+++++++++++

This attribute allows defining Meson project options:

.. code:: python

    def generate(self):
        tc = MesonToolchain(self)
        tc.definitions["MYVAR"] = "MyValue"
        tc.generate()

- One project options definition for ``MYVAR`` in ``conan_meson_native.init`` or ``conan_meson_cross.ini`` file.

preprocessor_definitions
++++++++++++++++++++++++

This attribute allows defining compiler preprocessor definitions, for multiple configurations (Debug, Release, etc).

.. code:: python

    def generate(self):
        tc = MesonToolchain(self)
        tc.preprocessor_definitions["MYDEF"] = "MyValue"
        tc.generate()

This will be translated to:

- One preprocessor definition for ``MYDEF`` in ``conan_meson_native.ini`` or ``conan_meson_cross.ini`` file.

Generators
++++++++++

The ``MesonToolchain`` only works with the ``PkgConfigDeps`` generator.
Please, do not use other generators, as they can have overlapping definitions that can conflict.


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


conf
++++

``MesonToolchain`` is affected by these :ref:`[conf]<global_conf>` variables:

- ``tools.meson.mesontoolchain:backend``. the meson `backend
  <https://mesonbuild.com/Configuring-a-build-directory.html>`_ to use. Possible values:
  ``ninja``, ``vs``, ``vs2010``, ``vs2015``, ``vs2017``, ``vs2019``, ``xcode``.
- ``tools.apple:sdk_path`` argument for SDK path in case of Apple cross-compilation. It will be used as value
  of the flag ``-isysroot``.
- ``tools.android:ndk_path`` argument for NDK path in case of Android cross-compilation. It will be used to get
  some binaries like ``c``, ``cpp`` and ``ar`` used in ``[binaries]`` section from *conan_meson_cross.ini*.

Apart from that, since Conan 1.47, you can inject extra flags thanks to these ones:

- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``cpp_args``.
- ``tools.build:cflags`` list of extra of pure C flags that will be used by ``c_args``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``c_link_args`` and ``cpp_link_args``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by by ``c_link_args`` and ``cpp_link_args``.


Cross-building for Apple and Android
+++++++++++++++++++++++++++++++++++++

It deserves a special mention because ``MesonToolchain`` is automatically adding all the flags needed
to cross-compile for Apple (MacOS M1, iOS, etc.) and Android.

**Apple**

It'll add link flags like ``-arch XXX``, ``-isysroot [SDK_PATH]`` and the minimum deployment target flag, e.g., ``-mios-version-min=8.0``
into Meson ``c_args``, ``c_link_args``, ``cpp_args`` and ``cpp_link_args`` built-in options.

**Android**

It'll initialize the ``c``, ``cpp`` and ``ar`` variables which are needed to cross-compile for Android. For instance:

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
