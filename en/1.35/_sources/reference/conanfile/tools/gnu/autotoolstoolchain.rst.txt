AutotoolsToolchain
==================

.. warning::

    These tools are **experimental** and subject to breaking changes.


The ``AutotoolsToolchain`` is the toolchain generator for Autotools. It will generate shell scripts containing
environment variable definitions that the autotools build system can understand.

The ``AutotooAutotoolsToolchainlsDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "AutotoolsToolchain"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    AutotoolsToolchain

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsToolchain(self)
            tc.generate()

The ``AutotoolsToolchain`` will generate after a ``conan install`` command the *conanautotoolstoolchain.sh* or *conanautotoolstoolchain.bat* files:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ source conanautotoolstoolchain.sh
    # or in Windows
    $ conanautotoolstoolchain.bat

This generator will define aggregated variables ``CPPFLAGS``, ``LDFLAGS``, ``CXXFLAGS``, ``CFLAGS`` that
accumulate all dependencies information, including transitive dependencies, with flags like ``-stdlib=libstdc++``, ``-std=gnu14``, architecture flags, etc.
