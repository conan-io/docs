.. _conan_tools_meson_meson:

Meson
======

The ``Meson()`` build helper is intended to be used in the ``build()`` and ``package()`` methods, to call Meson commands automatically.

.. code:: python

    from conan import ConanFile
    from conan.tools.meson import Meson

    class PkgConan(ConanFile):

        def build(self):
            meson = Meson(self)
            meson.configure()
            meson.build()

        def package(self):
            meson = Meson(self)
            meson.install()


Reference
---------

.. currentmodule:: conan.tools.meson

.. autoclass:: Meson
    :members:


conf
----

The ``Meson`` build helper is affected by these ``[conf]`` variables:

- ``tools.meson.mesontoolchain:extra_machine_files=[<FILENAME>]`` configuration to add
  your machine files at the end of the command using the correct parameter depending on
  native or cross builds. See `this Meson reference
  <https://mesonbuild.com/Machine-files.html#loading-multiple-machine-files>`_ for more
  information.

- ``tools.compilation:verbosity`` which accepts one of ``quiet`` or ``verbose`` and sets the ``--verbose`` flag in ``Meson.build()``

- ``tools.build:verbosity`` which accepts one of ``quiet`` or ``verbose`` and sets the ``--quiet`` flag in ``Meson.install()``
