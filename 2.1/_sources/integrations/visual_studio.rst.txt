.. _integrations_visual_studio:

|visual_studio_logo| Visual Studio
==================================

Conan provides several tools to help manage your projects using Microsoft Visual Studio.
These tools can be imported from ``conan.tools.microsoft`` and allow for native
integration with Microsoft Visual Studio, without the need to use CMake and instead
directly using Visual Studio solutions, projects, and property files. The most relevant
tools are:

- `MSBuildDeps`: the dependency information generator for Microsoft MSBuild build system.
  It will generate multiple ``xxxx.props`` properties files, one per dependency of a
  package, to be used by consumers using MSBuild or Visual Studio, just by adding the
  generated properties files to the solution and projects.

- `MSBuildToolchain`: the toolchain generator for MSBuild. It will generate MSBuild
  properties files that can be added to the Visual Studio solution projects. This
  generator translates the current package configuration, settings, and options, into
  MSBuild properties files syntax.

- `MSBuild` build helper is a wrapper around the command line invocation of MSBuild. It
  will abstract the calls like ``msbuild "MyProject.sln" /p:Configuration=<conf>
  /p:Platform=<platform>`` into Python method calls.

For the full list of tools under ``conan.tools.microsoft`` please check the
:ref:`reference <conan_tools_microsoft>` section.


.. seealso::

    - Reference for :ref:`MSBuildDeps<conan_tools_microsoft_msbuilddeps>`,
      :ref:`MSBuildToolchain<conan_tools_microsoft_msbuildtoolchain>` and
      :ref:`MSBuild<conan_tools_microsoft_msbuild>`.

.. |visual_studio_logo| image:: ../images/integrations/conan-visual_studio-logo.png
