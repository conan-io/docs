.. spelling::

  PropertyManager

.. _visualstudiolegacy_generator:

visual_studio_legacy
====================

Generates a file named *conanbuildinfo.vsprops* containing an XML that can be imported to your *Visual Studio 2008* project. Note that the
format of this file is different and incompatible with the *conanbuildinfo.props* file generated with the ``visual_studio`` generator for
newer versions.

Generated XML structure:

.. code-block:: xml

  <?xml version="1.0" encoding="Windows-1252"?>
  <VisualStudioPropertySheet
      ProjectType="Visual C++"
      Version="8.00"
      Name="conanbuildinfo"
      >
      <Tool
          Name="VCCLCompilerTool"
          AdditionalOptions="{compiler_flags}"
          AdditionalIncludeDirectories="{include_dirs}"
          PreprocessorDefinitions="{definitions}"
      />
      <Tool
          Name="VCLinkerTool"
          AdditionalOptions="{linker_flags}"
          AdditionalDependencies="{libs}"
          AdditionalLibraryDirectories="{lib_dirs}"
      />
  </VisualStudioPropertySheet>

This file can be loaded from the Menu->View->PropertyManager window, selecting "Add Existing Property Sheet" for the desired configuration.

.. image::  ../../images/conan-vc2008_props.png

Note that for single-configuration packages (which is the most typical), Conan installs Debug and Release packages separately. So a
different property sheet will be generated for each configuration. The process could be:

Given for example a recipe like:

.. code-block:: text
   :caption: *conanfile.txt*

    [requires]
    Pkg/0.1@user/channel

    [generators]
    visual_studio_legacy

And assuming that binary packages exist for ``Pkg/0.1@user/channel``, we could do:

.. code-block:: bash

    $ mkdir debug && cd debug
    $ conan install .. -s compiler="Visual Studio" -s compiler.version=9 -s arch=x86 -s build_type=Debug
    $ cd ..
    $ mkdir release && cd release
    $ conan install .. -s compiler="Visual Studio" -s compiler.version=9 -s arch=x86 -s build_type=Release
    # Now go to VS 2008 Property Manager, load the respective sheet into each configuration

The above process can be simplified using profiles (assuming you have created a *vs9release* profile) and you can also specify the
generators in the command line:

.. code-block:: bash

    $ conan install .. -pr=vs9release -g visual_studio_legacy
