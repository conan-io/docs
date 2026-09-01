.. _conan_tools_qbs_helper:

Qbs
=====
The ``Qbs`` build helper is a wrapper around the command line invocation of the Qbs build tool.
It will abstract the calls like ``qbs resolve``, ``qbs build`` and ``qbs install`` into Python
method calls.

The helper is intended to be used in the ``build()`` and ``package()`` methods, to call Qbs
commands automatically when a package is being built directly by Conan (create, install).

.. code-block:: python

    from conan import ConanFile
    from conan.tools.qbs import Qbs, QbsDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        exports_sources = "*.h", "*.cpp", "*.qbs",
        requires = "hello/0.1"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def generate(self):
            deps = QbsDeps(self)
            deps.generate()

        def build(self):
            qbs = Qbs(self)
            qbs.resolve()
            qbs.build()

        def package(self):
            qbs = Qbs(self)
            qbs.install()

Reference
---------

.. currentmodule:: conan.tools.qbs.qbs

.. autoclass:: Qbs
    :members:

