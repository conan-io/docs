<a id="integrations-makefile"></a>

# ![gnu_make_logo](images/integrations/conan-autotools-logo.png) Makefile

Conan provides different tools to help manage your projects using Make. They can be
imported from `conan.tools.gnu`. Besides the most popular variant, GNU Make, Conan also
supports other variants like BSD Make. The most relevant tools are:

- MakeDeps: the dependencies generator for Make, which generates a Makefile containing
  definitions that the Make build tool can understand.

Currently, there is no `MakeToolchain` generator, it should be added in the future.

For the full list of tools under `conan.tools.gnu` please check the [reference](https://docs.conan.io/2//reference/tools/gnu.html.md#conan-tools-gnu) section.

#### SEE ALSO
- Reference for [MakeDeps](https://docs.conan.io/2//reference/tools/gnu/makedeps.html.md#conan-tools-gnu-makedeps).
