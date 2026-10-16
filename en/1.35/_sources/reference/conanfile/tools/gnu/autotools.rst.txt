Autotools
=========

.. warning::

    These tools are **experimental** and subject to breaking changes.


The ``Autotools`` build helper is a wrapper around the command line invocation of autotools. It will abstract the
calls like ``./configure`` or ``make`` into Python method calls.

The ``Autotools`` helper can be used like:

.. code:: python

    from conans import conanfile
    from conan.tools.gnu import Autotools

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            autotools = Autotools(self)
            autotools.configure()
            autotools.make()


The current support is limited:
- It does not support cross-building or --target, --host, --build definitions
- It does not handle install functionality