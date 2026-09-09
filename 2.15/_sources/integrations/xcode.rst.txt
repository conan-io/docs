.. _integrations_xcode:

|xcode_logo| Xcode
==================

Conan provides different tools to integrate with Xcode IDE, providing all the necessary
information about the dependencies, build options and also to build projects created with
Xcode in recipes. They can be imported from ``conan.tools.apple``. The most relevant tools are:

- `XcodeDeps`: the dependency information generator for Xcode. It will generate multiple
  `.xcconfig` configuration files, that can be used by consumers using xcodebuild in the
  command line or adding them to the Xcode IDE.

- `XcodeToolchain`: the toolchain generator for Xcode. It will generate .xcconfig
  configuration files that can be added to Xcode projects. This generator translates the
  current package configuration, settings, and options, into Xcode .xcconfig files syntax.

- `XcodeBuild` build helper is a wrapper around the command line invocation of Xcode. It
  will abstract the calls like ``xcodebuild -project app.xcodeproj -configuration <config>
  -arch <arch> ...``


For the full list of tools under ``conan.tools.apple`` please check the :ref:`reference
<conan_tools_apple>` section. 

.. seealso::

    - Reference for :ref:`XcodeDeps<conan_tools_apple_xcodedeps>`, :ref:`XcodeToolchain
      <conan_tools_apple_xcodetoolchain>` and :ref:`XcodeBuild build helper
      <conan_tools_apple_xcodebuild>`


.. |xcode_logo| image:: ../images/integrations/conan-xcode-logo.jpg
