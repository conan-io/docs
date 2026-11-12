.. _conan_tools_microsoft_vcvars:


VCVars
=======

Generates a file called ``conanvcvars.bat`` that activates the Visual Studio developer command prompt according
to the current settings by wrapping the `vcvarsall <https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=vs-2017>`_
Microsoft bash script.


The ``VCVars`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "VCVars"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    VCVars

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.microsoft import VCVars

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = VCVars(self)
            ms.generate()



Customization
---------------

conf
++++

``VCVars`` is affected by these ``[conf]`` variables:

- ``tools.microsoft.msbuild:installation_path`` indicates the path to Visual Studio installation folder.
  For instance: ``C:\Program Files (x86)\Microsoft Visual Studio\2019\Community``, ``C:\Program Files (x86)\Microsoft Visual Studio 14.0``, etc.
- ``tools.microsoft:winsdk_version`` defines the specific winsdk version in the vcvars command line.

Reference
-----------

.. currentmodule:: conan.tools.microsoft

.. autoclass:: VCVars
    :members: generate
