<a id="integrations-autotools"></a>

# ![autotools_logo](images/integrations/conan-autotools-logo.png) Autotools

Conan provides different tools to help manage your projects using Autotools. They can be
imported from `conan.tools.gnu`. The most relevant tools are:

- AutotoolsDeps: the dependencies generator for Autotools, which generates shell scripts
  containing environment variable definitions that the Autotools build system can
  understand.
- AutotoolsToolchain: the toolchain generator for Autotools, which generates shell
  scripts containing environment variable definitions that the Autotools build system can
  understand.
- Autotools build helper, a wrapper around the command line invocation of autotools that
  abstracts calls like ./configure or make into Python method calls.
- PkgConfigDeps: the dependencies generator for pkg-config which generates
  pkg-config files for all the required dependencies of a package.

For the full list of tools under `conan.tools.gnu` please check the [reference](https://docs.conan.io/2//reference/tools/gnu.html.md#conan-tools-gnu) section.

#### SEE ALSO
- Reference for [AutotoolsDeps](https://docs.conan.io/2//reference/tools/gnu/autotoolsdeps.html.md#conan-tools-gnu-autotoolsdeps),
  [AutotoolsToolchain](https://docs.conan.io/2//reference/tools/gnu/autotoolstoolchain.html.md#conan-tools-gnu-autotoolstoolchain), [Autotools](https://docs.conan.io/2//reference/tools/gnu/autotools.html.md#conan-tools-gnu-build-helper) and
  [PkgConfigDeps](https://docs.conan.io/2//reference/tools/gnu/pkgconfigdeps.html.md#conan-tools-gnu-pkgconfigdeps).
