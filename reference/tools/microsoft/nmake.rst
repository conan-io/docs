.. _conan_tools_microsoft_nmake:


NMakeDeps
=========

This generator can be used as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        requires = "mydep/1.0"
        # attribute declaration
        generators = "NMakeDeps"

        # OR explicit usage in the generate() method
        def generate(self):
            deps = NMakeDeps(self)
            deps.generate()

        def build(self):
            self.run(f"nmake /f makefile")

The generator will create a ``conannmakedeps.bat`` environment script that defines
``CL``, ``LIB`` and ``_LINK_`` environment variables, injecting necessary flags 
to locate and link the dependencies declared in ``requires``.
This generator should most likely be used together with ``NMakeToolchain`` one.


NMaketoolchain
==============

This generator can be used as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        # attribute declaration
        generators = "NMakeToolchain"

        # OR explicit usage in the generate() method
        def generate(self):
            toolchain = NMakeToolchain(self)
            toolchain.generate()

        def build(self):
            self.run(f"nmake /f makefile")

The generator will create a ``conannmaketoolchain.bat`` environment script that defines
``CL`` environment variable, injecting necessary flags deduced from the Conan settings 
like ``compiler.cppstd`` or the Visual Studio runtime.
It will also generate a ``conanvcvars.bat`` script that activates the correct VS prompt
matching the Conan settings ``compiler`` and ``compiler.version``.
