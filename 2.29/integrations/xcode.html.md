<a id="integrations-xcode"></a>

# ![xcode_logo](images/integrations/conan-xcode-logo.jpg) Xcode

Conan provides different tools to integrate with Xcode IDE, providing all the necessary
information about the dependencies, build options and also to build projects created with
Xcode in recipes. They can be imported from `conan.tools.apple`. The most relevant tools are:

- XcodeDeps: the dependency information generator for Xcode. It will generate multiple
  .xcconfig configuration files, that can be used by consumers using xcodebuild in the
  command line or adding them to the Xcode IDE.
- XcodeToolchain: the toolchain generator for Xcode. It will generate .xcconfig
  configuration files that can be added to Xcode projects. This generator translates the
  current package configuration, settings, and options, into Xcode .xcconfig files syntax.
- XcodeBuild build helper is a wrapper around the command line invocation of Xcode. It
  will abstract the calls like `xcodebuild -project app.xcodeproj -configuration <config>
  -arch <arch> ...`

For the full list of tools under `conan.tools.apple` please check the [reference](https://docs.conan.io/2//reference/tools/apple.html.md#conan-tools-apple) section.

#### SEE ALSO
- Reference for [XcodeDeps](https://docs.conan.io/2//reference/tools/apple/xcodedeps.html.md#conan-tools-apple-xcodedeps), [XcodeToolchain](https://docs.conan.io/2//reference/tools/apple/xcodetoolchain.html.md#conan-tools-apple-xcodetoolchain) and [XcodeBuild build helper](https://docs.conan.io/2//reference/tools/apple/xcodebuild.html.md#conan-tools-apple-xcodebuild)
