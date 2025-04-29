AutotoolsGen
============

.. warning::

    These tools are **experimental** and subject to breaking changes.


The ``AutotoolsGen`` is a complete generator for the whole autotools system. It aggregates the
functionality of ``AutotoolsDeps``, ``AutotoolsToolchain`` and ``VirtualEnv`` into a single generator.

It will generate shell scripts containing environment variable definitions that the autotools build system can understand.

The ``AutotoolsGen`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "AutotoolsGen"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    AutotoolsGen

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsGen

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsGen(self)
            tc.generate()


Its implementation is straightforward:

.. code:: python

    class AutotoolsGen:
        def __init__(self, conanfile):
            self.toolchain = AutotoolsToolchain(conanfile)
            self.deps = AutotoolsDeps(conanfile)
            self.env = VirtualEnv(conanfile)

And it will output the same files as ``VirtualEnv``:

- *conanbuildenv* .bat or .sh scripts, that are automatically loaded if existing by the ``self.run()`` recipes methods
- *conanrunenv* .bat or .sh scripts, that can be explicitly opted-in in ``self.run()`` recipes methods with ``self.run(..., env=["conanrunenv"])``

These files will contain the necessary accumulated information from all the 3 internal generators.
