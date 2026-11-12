<a id="conan-tools"></a>

# Recipe tools

Tools are all things that can be imported and used in Conan recipes.

The import path is always like:

```python
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
from conan.tools.microsoft import MSBuildToolchain, MSBuildDeps, MSBuild
```

The main guidelines are:

- Everything that recipes can import belong to `from conan.tools`. Any other thing is private implementation
  and shouldn’t be used in recipes.
- Only documented, public (not preceded by `_`) tools can be used in recipes.

Contents:

* [conan.tools.android](https://docs.conan.io/2//reference/tools/android.html.md)
  * [android_abi()](https://docs.conan.io/2//reference/tools/android.html.md#android-abi)
* [conan.tools.apple](https://docs.conan.io/2//reference/tools/apple.html.md)
  * [XcodeDeps](https://docs.conan.io/2//reference/tools/apple/xcodedeps.html.md)
  * [XcodeToolchain](https://docs.conan.io/2//reference/tools/apple/xcodetoolchain.html.md)
  * [XcodeBuild](https://docs.conan.io/2//reference/tools/apple/xcodebuild.html.md)
  * [conan.tools.apple.fix_apple_shared_install_name()](https://docs.conan.io/2//reference/tools/apple/other.html.md)
  * [conan.tools.apple.is_apple_os()](https://docs.conan.io/2//reference/tools/apple/other.html.md#conan-tools-apple-is-apple-os)
  * [conan.tools.apple.to_apple_arch()](https://docs.conan.io/2//reference/tools/apple/other.html.md#conan-tools-apple-to-apple-arch)
  * [conan.tools.apple.XCRun()](https://docs.conan.io/2//reference/tools/apple/other.html.md#conan-tools-apple-xcrun)
* [conan.tools.build](https://docs.conan.io/2//reference/tools/build.html.md)
  * [Building](https://docs.conan.io/2//reference/tools/build.html.md#building)
  * [Cppstd](https://docs.conan.io/2//reference/tools/build.html.md#cppstd)
  * [cstd](https://docs.conan.io/2//reference/tools/build.html.md#cstd)
  * [Compiler](https://docs.conan.io/2//reference/tools/build.html.md#compiler)
* [conan.tools.cmake](https://docs.conan.io/2//reference/tools/cmake.html.md)
  * [CMakeDeps](https://docs.conan.io/2//reference/tools/cmake/cmakedeps.html.md)
  * [CMakeConfigDeps](https://docs.conan.io/2//reference/tools/cmake/cmakeconfigdeps.html.md)
  * [CMakeToolchain](https://docs.conan.io/2//reference/tools/cmake/cmaketoolchain.html.md)
  * [CMake](https://docs.conan.io/2//reference/tools/cmake/cmake.html.md)
  * [cmake_layout](https://docs.conan.io/2//reference/tools/cmake/cmake_layout.html.md)
* [conan.tools.CppInfo](https://docs.conan.io/2//reference/tools/cpp_info.html.md)
  * [Aggregating information in custom generators](https://docs.conan.io/2//reference/tools/cpp_info.html.md#aggregating-information-in-custom-generators)
* [conan.tools.env](https://docs.conan.io/2//reference/tools/env.html.md)
  * [Environment](https://docs.conan.io/2//reference/tools/env/environment.html.md)
  * [EnvVars](https://docs.conan.io/2//reference/tools/env/envvars.html.md)
  * [VirtualBuildEnv](https://docs.conan.io/2//reference/tools/env/virtualbuildenv.html.md)
  * [VirtualRunEnv](https://docs.conan.io/2//reference/tools/env/virtualrunenv.html.md)
* [conan.tools.files](https://docs.conan.io/2//reference/tools/files.html.md)
  * [conan.tools.files basic operations](https://docs.conan.io/2//reference/tools/files/basic.html.md)
  * [conan.tools.files downloads](https://docs.conan.io/2//reference/tools/files/downloads.html.md)
  * [conan.tools.files patches](https://docs.conan.io/2//reference/tools/files/patches.html.md)
  * [conan.tools.files checksums](https://docs.conan.io/2//reference/tools/files/checksum.html.md)
  * [conan.tools.files.symlinks](https://docs.conan.io/2//reference/tools/files/symlinks.html.md)
* [conan.tools.gnu](https://docs.conan.io/2//reference/tools/gnu.html.md)
  * [AutotoolsDeps](https://docs.conan.io/2//reference/tools/gnu/autotoolsdeps.html.md)
  * [AutotoolsToolchain](https://docs.conan.io/2//reference/tools/gnu/autotoolstoolchain.html.md)
  * [Autotools](https://docs.conan.io/2//reference/tools/gnu/autotools.html.md)
  * [MakeDeps](https://docs.conan.io/2//reference/tools/gnu/makedeps.html.md)
  * [PkgConfigDeps](https://docs.conan.io/2//reference/tools/gnu/pkgconfigdeps.html.md)
  * [PkgConfig](https://docs.conan.io/2//reference/tools/gnu/pkgconfig.html.md)
* [conan.tools.google](https://docs.conan.io/2//reference/tools/google.html.md)
  * [Bazel](https://docs.conan.io/2//reference/tools/google/bazel.html.md)
  * [BazelDeps](https://docs.conan.io/2//reference/tools/google/bazeldeps.html.md)
  * [BazelToolchain](https://docs.conan.io/2//reference/tools/google/bazeltoolchain.html.md)
* [conan.tools.intel](https://docs.conan.io/2//reference/tools/intel.html.md)
  * [IntelCC](https://docs.conan.io/2//reference/tools/intel.html.md#intelcc)
  * [Reference](https://docs.conan.io/2//reference/tools/intel.html.md#reference)
* [conan.tools.layout](https://docs.conan.io/2//reference/tools/layout.html.md)
  * [Predefined layouts](https://docs.conan.io/2//reference/tools/layout.html.md#predefined-layouts)
  * [basic_layout](https://docs.conan.io/2//reference/tools/layout.html.md#basic-layout)
* [conan.tools.meson](https://docs.conan.io/2//reference/tools/meson.html.md)
  * [MesonToolchain](https://docs.conan.io/2//reference/tools/meson/mesontoolchain.html.md)
  * [Meson](https://docs.conan.io/2//reference/tools/meson/meson.html.md)
* [conan.tools.microsoft](https://docs.conan.io/2//reference/tools/microsoft.html.md)
  * [MSBuild](https://docs.conan.io/2//reference/tools/microsoft/msbuild.html.md)
  * [MSBuildDeps](https://docs.conan.io/2//reference/tools/microsoft/msbuilddeps.html.md)
  * [MSBuildToolchain](https://docs.conan.io/2//reference/tools/microsoft/msbuildtoolchain.html.md)
  * [VCVars](https://docs.conan.io/2//reference/tools/microsoft/vcvars.html.md)
  * [NMakeDeps](https://docs.conan.io/2//reference/tools/microsoft/nmake.html.md)
  * [NMakeToolchain](https://docs.conan.io/2//reference/tools/microsoft/nmake.html.md#nmaketoolchain)
  * [vs_layout](https://docs.conan.io/2//reference/tools/microsoft/visual_layout.html.md)
  * [check_min_vs](https://docs.conan.io/2//reference/tools/microsoft/helpers.html.md)
  * [msvc_runtime_flag](https://docs.conan.io/2//reference/tools/microsoft/helpers.html.md#msvc-runtime-flag)
  * [is_msvc](https://docs.conan.io/2//reference/tools/microsoft/helpers.html.md#is-msvc)
  * [is_msvc_static_runtime](https://docs.conan.io/2//reference/tools/microsoft/helpers.html.md#is-msvc-static-runtime)
  * [msvs_toolset](https://docs.conan.io/2//reference/tools/microsoft/helpers.html.md#msvs-toolset)
  * [unix_path](https://docs.conan.io/2//reference/tools/microsoft/helpers.html.md#unix-path)
* [conan.tools.qbs](https://docs.conan.io/2//reference/tools/qbs.html.md)
  * [Qbs](https://docs.conan.io/2//reference/tools/qbs/qbs.html.md)
  * [QbsDeps](https://docs.conan.io/2//reference/tools/qbs/qbsdeps.html.md)
  * [QbsProfile](https://docs.conan.io/2//reference/tools/qbs/qbsprofile.html.md)
* [conan.tools.ros](https://docs.conan.io/2//reference/tools/ros.html.md)
  * [ROSEnv](https://docs.conan.io/2//reference/tools/ros/rosenv.html.md)
* [conan.tools.sbom](https://docs.conan.io/2//reference/tools/sbom.html.md)
  * [CycloneDX](https://docs.conan.io/2//reference/tools/sbom.html.md#cyclonedx)
* [conan.tools.scm](https://docs.conan.io/2//reference/tools/scm.html.md)
  * [Git](https://docs.conan.io/2//reference/tools/scm/git.html.md)
  * [Version](https://docs.conan.io/2//reference/tools/scm/version.html.md)
* [conan.tools.scons](https://docs.conan.io/2//reference/tools/scons.html.md)
  * [SConsDeps](https://docs.conan.io/2//reference/tools/scons.html.md#sconsdeps)
* [conan.tools.premake](https://docs.conan.io/2//reference/tools/premake.html.md)
  * [PremakeDeps](https://docs.conan.io/2//reference/tools/premake/premakedeps.html.md)
  * [PremakeToolchain](https://docs.conan.io/2//reference/tools/premake/premaketoolchain.html.md)
  * [Premake](https://docs.conan.io/2//reference/tools/premake/premake.html.md)
* [conan.tools.system](https://docs.conan.io/2//reference/tools/system.html.md)
  * [conan.tools.system.package_manager](https://docs.conan.io/2//reference/tools/system/package_manager.html.md)
  * [PyEnv](https://docs.conan.io/2//reference/tools/system/pyenv.html.md)
