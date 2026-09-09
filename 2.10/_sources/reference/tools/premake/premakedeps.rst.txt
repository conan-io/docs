.. _conan_tools_premake_premakedeps:

PremakeDeps
===========

.. include:: ../../../common/experimental_warning.inc

The ``PremakeDeps`` is the dependencies generator for Premake.

The ``PremakeDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "PremakeDeps"


.. code-block:: text
    :caption: conanfile.txt

    [generators]
    PremakeDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.premake import PremakeDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "zlib/1.2.11"

        def generate(self):
            bz = PremakeDeps(self)
            bz.generate()

Generated files
---------------

When the ``PremakeDeps`` generator is used, every invocation of ``conan install`` will
generate a ``include('conandeps.premake5.lua')`` that can be included and used in the project:


.. code-block:: lua

    -- premake5.lua

    include('conandeps.premake5.lua')

    workspace "HelloWorld"
        conan_setup()
        configurations { "Debug", "Release" }
        platforms { "x86_64" }
