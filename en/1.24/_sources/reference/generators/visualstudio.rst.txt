.. _visualstudio_generator:

visual_studio
=============

.. container:: out_reference_box

    This is the reference page for ``visual_studio`` generator.
    Go to :ref:`Integrations/Visual Studio<visual_studio>` if you want to learn how to integrate your project or recipes with Visual Studio.

Generates a file named *conanbuildinfo.props* containing an XML that can be imported to your Visual Studio project.

Generated xml structure:

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
      <ImportGroup Label="PropertySheets" />
      <PropertyGroup Label="UserMacros" />
      <PropertyGroup Label="Conan-RootDirs">
        <Conan-Lib1-Root>{PACKAGE LIB1 FOLDER}</Conan-Poco-Root>
        <Conan-Lib2-Root>{PACKAGE LIB2 FOLDER}</Conan-Poco-Root>
        ...
      </PropertyGroup>
      <PropertyGroup Label="ConanVariables">
        <ConanCompilerFlags>{compiler_flags}</ConanCompilerFlags>
        <ConanLinkerFlags>{linker_flags}</ConanLinkerFlags>
        <ConanPreprocessorDefinitions>{definitions}</ConanPreprocessorDefinitions>
        <ConanIncludeDirectories>{include_dirs}</ConanIncludeDirectories>
        <ConanResourceDirectories>{res_dirs}</ConanResourceDirectories>
        <ConanLibraryDirectories>{lib_dirs}</ConanLibraryDirectories>
        <ConanBinaryDirectories>{bin_dirs}</ConanBinaryDirectories>
        <ConanLibraries>{libs}</ConanLibraries>
        <ConanSystemDeps>{system_libs}</ConanSystemDeps>
      </PropertyGroup>
      <PropertyGroup>
        <LocalDebuggerEnvironment>PATH=%PATH%;{CONAN BINARY DIRECTORIES LIST}</LocalDebuggerEnvironment>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
      </PropertyGroup>
      <ItemDefinitionGroup>
        <ClCompile>
          <AdditionalIncludeDirectories>$(ConanIncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
          <PreprocessorDefinitions>$(ConanPreprocessorDefinitions)%(PreprocessorDefinitions)</PreprocessorDefinitions>
          <AdditionalOptions>$(ConanCompilerFlags) %(AdditionalOptions)</AdditionalOptions>
        </ClCompile>
        <Link>
          <AdditionalLibraryDirectories>$(ConanLibraryDirectories)%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
          <AdditionalDependencies>$(ConanLibraries)%(AdditionalDependencies)</AdditionalDependencies>
          <AdditionalDependencies>$(ConanSystemDeps)%(AdditionalDependencies)</AdditionalDependencies>
          <AdditionalOptions>$(ConanLinkerFlags) %(AdditionalOptions)</AdditionalOptions>
        </Link>
        <Midl>
          <AdditionalIncludeDirectories>$(ConanIncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
        </Midl>
        <ResourceCompile>
          <AdditionalIncludeDirectories>$(ConanIncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
          <PreprocessorDefinitions>$(ConanPreprocessorDefinitions)%(PreprocessorDefinitions)</PreprocessorDefinitions>
          <AdditionalOptions>$(ConanCompilerFlags) %(AdditionalOptions)</AdditionalOptions>
        </ResourceCompile>
      </ItemDefinitionGroup>
      <ItemGroup />
    </Project>

There are ``ConanVariables`` containing the information of the dependencies. Those variables are used later in the file, like in the ``<Link>`` task.

Note that for single-configuration packages, which is the most typical, Conan installs Debug/Release, 32/64bits, packages separately. So a different property sheet will be generated for each configuration. The process could be:

Given for example a ``conanfile.txt`` like:

.. code-block:: text
   :caption: *conanfile.txt*

    [requires]
    pkg/0.1@user/channel

    [generators]
    visual_studio

And assuming that binary packages exist for ``pkg/0.1@user/channel``, we could do:

.. code-block:: bash

    $ mkdir debug32 && cd debug32
    $ conan install .. -s compiler="Visual Studio" -s compiler.version=15 -s arch=x86 -s build_type=Debug
    $ cd ..
    $ mkdir debug64 && cd debug64
    $ conan install .. -s compiler="Visual Studio" -s compiler.version=15 -s arch=x86_64 -s build_type=Debug
    $ cd ..
    $ mkdir release32 && cd release32
    $ conan install .. -s compiler="Visual Studio" -s compiler.version=15 -s arch=x86 -s build_type=Release
    $ cd ..
    $ mkdir release64 && cd release64
    $ conan install .. -s compiler="Visual Studio" -s compiler.version=15 -s arch=x86_64 -s build_type=Release
    ...
    # Now go to VS 2017 Property Manager, load the respective sheet into each configuration

The above process can be simplified using profiles (assuming you have created the respective profiles), and you can also specify the
generators in the command line:

.. code-block:: bash

    $ conan install .. -pr=vs15release64 -g visual_studio
    ...
