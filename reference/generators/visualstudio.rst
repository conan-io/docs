.. _visualstudio_generator:

visual_studio
=============

.. container:: out_reference_box

    This is the reference page for ``visual_studio`` generator.
    Go to :ref:`Integrations/Visual Studio<visual_studio>` if you want to learn how to integrate your project or recipes with Visual Studio.


Generates a file named ``conanbuildinfo.props`` containing an XML that can be imported to your *Visual Studio* project.

Generated xml structure:

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
      <ImportGroup Label="PropertySheets" />
      <PropertyGroup Label="UserMacros" />
      <PropertyGroup Label="Conan.RootDirs">
        <Conan.lib.Root>{ROOT DIRECTORY REQUIRE 1}</Conan.lib.Root>
        <Conan.lib.Root>{ROOT DIRECTORY REQUIRE 2}</Conan.lib.Root>
      </PropertyGroup>
      <PropertyGroup>
        <ExecutablePath>{BIN DIRECTORY REQUIRE 1};{BIN DIRECTORY REQUIRE 2};$(ExecutablePath)</ExecutablePath>
      </PropertyGroup>
      <PropertyGroup>
        <LocalDebuggerEnvironment>PATH=%PATH%;{BIN DIRECTORY REQUIRE 1};{BIN DIRECTORY REQUIRE 2};</LocalDebuggerEnvironment>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
      </PropertyGroup>
      <ItemDefinitionGroup>
        <ClCompile>
          <AdditionalIncludeDirectories>{INCLUDE DIRECTORY REQUIRE 1};{INCLUDE DIRECTORY REQUIRE 2};%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
          <PreprocessorDefinitions>%(PreprocessorDefinitions)</PreprocessorDefinitions>
          <AdditionalOptions> %(AdditionalOptions)</AdditionalOptions>
        </ClCompile>
        <Link>
          <AdditionalLibraryDirectories>{LIB DIRECTORY REQUIRE 1};{LIB DIRECTORY REQUIRE 2};%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
          <AdditionalDependencies>{LIB NAMES REQUIRE1} {LIB NAMES REQUIRE 2} %(AdditionalDependencies)</AdditionalDependencies>
          <AdditionalOptions> %(AdditionalOptions)</AdditionalOptions>
        </Link>
      </ItemDefinitionGroup>
      <ItemGroup />
    </Project>