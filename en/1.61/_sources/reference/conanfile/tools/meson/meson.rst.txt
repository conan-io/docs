.. _conan-meson-helper:


Meson
-----

.. important::

    This feature is still **under development**, while it is recommended and usable and we will try not to break them in future releases,
    some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.

Available since: `1.33.0 <https://github.com/conan-io/conan/releases/tag/1.33.0>`_

This helper is intended to be used in the ``build()`` method, to call Meson commands automatically
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

    def configure(self, reconfigure=False):

Calls :command:`meson`, with the given generator and passing either :command:`--native-file conan_meson_native.ini`
(native builds) or :command:`--cross-file conan_meson_cross.ini` (cross builds). Use ``tools.meson.mesontoolchain:extra_machine_files=[<FILENAME>]``
configuration to add your machine files at the end of the command using the correct parameter depending on native or cross builds.
See `this Meson reference <https://mesonbuild.com/Machine-files.html#loading-multiple-machine-files>`_ for more information.

Parameters:
    - **reconfigure** (Optional, Defaulted to ``False``): Adds the ``--reconfigure`` parameter to the ``meson setup`` command if ``True``.


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

Runs project's tests. Equivalent to running :command:`meson test -v -C .` in the build folder. Use ``tools.build:skip_test=False``
to avoid execute this command and skip the tests.


conf
++++

- ``tools.build:jobs=10`` (integer) argument for the ``--jobs`` parameter when running Ninja.
- ``tools.build:skip_test=<bool>``(boolean) if ``True`` running ``meson test``.
- ``tools.meson.mesontoolchain:extra_machine_files=["<FILENAME>"]`` (list of strings) adds your own extra machine files in
  ``meson setup`` command, e.g., ``meson setup --native-file "conan_meson_native.ini" --native-file "<FILENAME>"``.
