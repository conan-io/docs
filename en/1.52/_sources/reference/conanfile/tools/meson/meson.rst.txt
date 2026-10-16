.. _conan-meson-helper:


Meson
-----

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

Available since: `1.33.0 <https://github.com/conan-io/conan/releases/tag/1.33.0>`_

The ``Meson()`` build helper that works with the ``MesonToolchain`` is also experimental,
and subject to breaking change in the future. It will evolve to adapt and complement the
toolchain functionality.

The helper is intended to be used in the ``build()`` method, to call Meson commands automatically
when a package is being built directly by Conan (create, install)

.. code:: python

    from conan.tools.meson import Meson

    def build(self):
        meson = Meson(self)
        meson.configure()
        meson.build()


It supports the following methods:


constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.

configure()
+++++++++++

.. code:: python

    def configure(self):

Calls :command:`meson`, with the given generator and passing either :command:`--native-file conan_meson_native.ini`
(native builds) or :command:`--cross-file conan_meson_cross.ini` (cross builds).


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

- ``tools.build:jobs=10`` argument for the ``--jobs`` parameter when running Ninja.
