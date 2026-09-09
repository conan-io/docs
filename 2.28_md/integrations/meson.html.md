<a id="integrations-meson"></a>

# ![meson_logo](images/integrations/conan-meson-logo.png) Meson

Conan provides different tools to help manage your projects using Meson. They can be
imported from `conan.tools.meson`. The most relevant tools are:

- MesonToolchain: generates the .ini files for Meson with the definitions of all the
  Meson properties related to the Conan options and settings for the current package,
  platform, etc. MesonToolchain normally works together with
  [PkgConfigDeps](https://docs.conan.io/2//reference/tools/gnu/pkgconfigdeps.html.md#conan-tools-gnu-pkgconfigdeps) to manage all the dependencies.
- Meson build helper, a wrapper around the command line invocation of Meson.

#### SEE ALSO
- Reference for [MesonToolchain](https://docs.conan.io/2//reference/tools/meson/mesontoolchain.html.md#conan-tools-meson-mesontoolchain) and
  [Meson](https://docs.conan.io/2//reference/tools/meson/meson.html.md#conan-tools-meson-meson).
- Build a simple Meson project using Conan
  [example](https://docs.conan.io/2//examples/tools/meson/build_simple_meson_project.html.md#examples-tools-meson-toolchain-build-simple-meson-project)

Build a simple Meson project using Conan
