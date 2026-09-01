<a id="integrations-premake"></a>

# ![premake_logo](images/integrations/conan-premake-logo.png) Premake

Conan provides different tools to help manage your projects using Premake. They can be
imported from `conan.tools.premake`. The most relevant tools are:

- `PremakeDeps`: the dependencies generator for Premake, to allow consuming dependencies from Premake projects.
- `PremakeToolchain`: the toolchain generator for Premake. It will create a
  wrapper over premake scripts allowing premake workspace and projects
  customization.
- `Premake`: the Premake build helper. It’s simply a wrapper around the command line invocation of Premake.

#### SEE ALSO
- Reference for [PremakeDeps](https://docs.conan.io/2//reference/tools/premake/premakedeps.html.md#conan-tools-premake-premakedeps).
- Reference for [PremakeToolchain](https://docs.conan.io/2//reference/tools/premake/premaketoolchain.html.md#conan-tools-premake-premaketoolchain).
- Reference for [Premake](https://docs.conan.io/2//reference/tools/premake/premake.html.md#conan-tools-premake-premake).
