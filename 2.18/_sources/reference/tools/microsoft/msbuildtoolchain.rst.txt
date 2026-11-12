.. _conan_tools_microsoft_msbuildtoolchain:


MSBuildToolchain
=================

The ``MSBuildToolchain`` is the toolchain generator for MSBuild. It will generate MSBuild properties files
that can be added to the Visual Studio solution projects. This generator translates the current package configuration,
settings, and options, into MSBuild properties files syntax.

This generator can be used by name in conanfiles:

.. code-block:: python
    :caption: **conanfile.py**

    class Pkg(ConanFile):
        generators = "MSBuildToolchain"

.. code-block:: text
    :caption: **conanfile.txt**

    [generators]
    MSBuildToolchain


And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import MSBuildToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = MSBuildToolchain(self)
            tc.generate()


The ``MSBuildToolchain`` will generate three files after a ``conan install`` command:

.. code-block:: bash

    $ conan install . # default is Release
    $ conan install . -s build_type=Debug


- The main *conantoolchain.props* file, to be added to the project.
- A *conantoolchain_<config>.props* file, that will be conditionally included from the previous
  *conantoolchain.props* file based on the configuration and platform, e.g., *conantoolchain_release_x86.props*.
- A *conanvcvars.bat* file with the ``vcvars`` invocation to define the build environment from the command line,
  or any other automated tools (might not be required if opening the IDE). This file will be automatically called
  by the ``MSBuild.build()`` method.

Every invocation with different configuration creates a new properties ``.props`` file, that is also conditionally
included. That allows to install different configurations, then switch among them directly from the Visual Studio IDE.

The MSBuildToolchain files can configure:

- The Visual Studio runtime (*MT/MD/MTd/MDd*), obtained from Conan input settings.
- The C++ standard, obtained from Conan input settings.

One of the advantages of using toolchains is that they help to achieve the exact same build with local development flows,
than when the package is created in the cache.


Customization
---------------

conf
++++

``MSBuildToolchain`` is affected by these ``[conf]`` variables:

- ``tools.microsoft.msbuildtoolchain:compile_options`` dict-like object of extra compile options to be added to ``<ClCompile>`` section.
  The dict will be translated as follows: ``<[KEY]>[VALUE]</[KEY]>``.
- ``tools.microsoft:winsdk_version`` value will define the ``<WindowsTargetPlatformVersion>`` element in the toolchain file.
- ``tools.build:cxxflags`` list of extra C++ flags that will be appended to ``<AdditionalOptions>`` section from ``<ClCompile>`` and ``<ResourceCompile>`` one.
- ``tools.build:cflags`` list of extra of pure C flags that will be appended to ``<AdditionalOptions>`` section from ``<ClCompile>`` and ``<ResourceCompile>`` one.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be appended to ``<AdditionalOptions>`` section from ``<Link>`` one.
- ``tools.build:exelinkflags`` list of extra linker flags that will be appended to ``<AdditionalOptions>`` section from ``<Link>`` one.
- ``tools.build:defines`` list of preprocessor definitions that will be appended to ``<PreprocessorDefinitions>`` section from ``<ResourceCompile>`` one.


Reference
---------

.. currentmodule:: conan.tools.microsoft

.. autoclass:: MSBuildToolchain
    :members: generate

Attributes
++++++++++

* **properties**: Additional properties added to the generated ``.props`` files. You can
  define the properties in a key-value syntax like:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import MSBuildToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            msbuild = MSBuildToolchain(self)
            msbuild.properties["IncludeExternals"] = "true"
            msbuild.generate()

Then, the generated *conantoolchain_<config>.props* file will contain the defined property
in its contents:


.. code-block:: xml
    :emphasize-lines: 8

    <?xml version="1.0" encoding="utf-8"?>
    <Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
    <ItemDefinitionGroup>
    ...
    </ItemDefinitionGroup>
    <PropertyGroup Label="Configuration">
        ...
        <IncludeExternals>true</IncludeExternals>
        ...
    </PropertyGroup>
    </Project>
