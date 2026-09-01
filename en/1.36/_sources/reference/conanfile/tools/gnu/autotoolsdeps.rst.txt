AutotoolsDeps
=============

.. warning::

    These tools are **experimental** and subject to breaking changes.


The ``AutotoolsDeps`` is the dependencies generator for Autotools. It will generate shell scripts containing
environment variable definitions that the autotools build system can understand.

The ``AutotoolsDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "AutotoolsDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    AutotoolsDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsDeps(self)
            tc.generate()

The ``AutotoolsDeps`` will generate after a ``conan install`` command the *conanautotoolsdeps.sh* or *conanautotoolsdeps.bat* files:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ source conanautotoolsdeps.sh
    # or in Windows
    $ conanautotoolsdeps.bat

This generator will define aggregated variables ``CPPFLAGS``, ``LIBS``, ``LDFLAGS``, ``CXXFLAGS``, ``CFLAGS`` that
accumulate all dependencies information, including transitive dependencies, with flags like ``-I<path>``, ``-L<path>``, etc.

At this moment, only the ``requires`` information is generated, the ``build_requires`` one is not managed by this generator yet.
