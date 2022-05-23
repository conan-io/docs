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
