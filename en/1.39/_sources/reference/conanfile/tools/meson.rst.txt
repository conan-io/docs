.. _conan-meson-toolchain:

conan.tools.meson
=================

MesonToolchain
--------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

Available since: `1.33.0 <https://github.com/conan-io/conan/releases/tag/1.33.0>`_

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
            tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
            tc.generate()


The ``MesonToolchain`` will generate the following file during ``conan install``
command (or before calling the ``build()`` method when the package is being
built in the cache): *conan_meson_native.ini*, if doing a native build, or
*conan_meson_cross.ini*, if doing a cross-build (:ref:`cross_building_reference`).

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

    def __init__(self, conanfile, env=os.environ):

Most of the arguments are optional and will be deduced from the current ``settings``, and not
necessary to define them.

- ``conanfile``: the current recipe object. Always use ``self``.
- ``env``: the dictionary of the environment variables.

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

- One preprocessor definition for ``MYDEF`` in ``conan_meson_native.init`` or ``conan_meson_cross.ini`` file.

Generators
++++++++++

The ``MesonToolchain`` only works with the ``pkg_config`` generator.
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

Meson
-----

The ``Meson()`` build helper that works with the ``MesonToolchain`` is also experimental,
and subject to breaking change in the future. It will evolve to adapt and complement the
toolchain functionality.

The helper is intended to be used in the ``build()`` method, to call Meson commands automatically
when a package is being built directly by Conan (create, install)

.. code:: python

    from conan.tools.meson import Meson

    def build(self):
        meson = Meson(self)
        meson.configure(source_folder="src")
        meson.build()


It supports the following methods:


constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, build_folder='build'):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``build_folder``: Relative path to a folder to contain the temporary build files

configure()
+++++++++++

.. code:: python

    def configure(self, source_folder=None):

Calls :command:`meson`, with the given generator and passing either :command:`--native-file conan_meson_native.ini`
(native builds) or :command:`--cross-file conan_meson_cross.ini` (cross builds).

- ``source_folder``: Relative path to the folder containing the root *meson.build*

build()
+++++++

.. code:: python

    def build(self, target=None):

Calls the build system. Equivalent to :command:`meson compile -C .` in the build folder.

Parameters:
    - **target** (Optional, Defaulted to ``None``): Specifies the target to execute. The default *all* target will be built if ``None`` is specified.

install()
+++++++++

.. code:: python

    def install(self):

Installs development files (headers, libraries, etc.). Equivalent to run :command:`meson install -C .` in the build folder.

test()
++++++

.. code:: python

    def test(self):

Runs project's tests. Equivalent to running :command:`meson test -v -C .` in the build folder..

conf
++++

- ``tools.ninja:jobs`` argument for the ``--jobs`` parameter when running Ninja. (overrides
  the general ``tools.build:processes``).
