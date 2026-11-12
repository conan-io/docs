<a id="conan-tools-premake-premaketoolchain"></a>

# PremakeToolchain

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### IMPORTANT
This class will generate files that are only compatible with Premake versions >= 5.0.0

The `PremakeToolchain` generator can be used by name in conanfiles:

```python
class Pkg(ConanFile):
    generators = "PremakeToolchain"
```

```text
[generators]
PremakeToolchain
```

And it can also be fully instantiated in the conanfile `generate()` method:

**Usage Example:**

```python
from conan.tools.premake import PremakeToolchain

class Pkg(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def generate(self):
        tc = PremakeToolchain(self)
        tc.extra_defines = ["VALUE=2"]                      # Add define to main premake workspace
        tc.extra_cflags = ["-Wextra"]                       # Add cflags to main premake workspace
        tc.extra_cxxflags = ["-Wall", "-Wextra"]            # Add cxxflags to main premake workspace
        tc.extra_ldflags = ["-lm"]                          # Add ldflags to main premake workspace
        tc.project("main").extra_defines = ["TEST=False"]   # Add define to "main" project (overriding possible value)
        tc.project("main").extra_cxxflags = ["-FS"]         # Add cxxflags to "main" project
        tc.project("test").disable = True                   # A way of disabling "test" project compilation
        tc.project("foo").kind = "StaticLib"                # Override library type of "foo"
        tc.generate()
```

## Generated files

The `PremakeToolchain` generates `conantoolchain.premake5.lua` file after a **conan install** (or when building the package
in the cache) with the information provided in the `generate()` method as well as information
translated from the current `settings`, `conf`, etc.

Premake does not expose any kind of API to interact inject/modify the build scripts.
Furthermore, premake does not have a concept of toolchain so following premake maintainers instructions, (see [premake discussion](https://github.com/premake/premake-core/discussions/2441))
as premake is built in top of Lua scripts, Conan generated file is a Lua script
that will override the original premake script adding the following
information:

* Detection of `buildtype` from Conan settings.
* Definition of the C++ standard as necessary.
* Definition of the C standard as necessary.
* Detection of the premake `action` based on conan profile and OS.
* Definition of the build folder in order to avoid default premake behavior of
  creating build folder and object files in the source repository (which goes
  against conan good practices).
* Definition of compiler and linker flags and defines based on user configuration values.
* Definition of proper target architecture when cross building.
* Definition of `fPIC` flag based on conan options.
* Based on `shared` conan option, `PremakeToolchain` will set the `kind` of the `workspace` to `SharedLib` or `StaticLib`.

#### NOTE
`PremakeToolchain` is not able to override the `kind` of a project if that project has already define the `kind` attribute (typical case).
It can only override top-level `workspace.kind`, which will only affect projects without a defined `kind`.

**Recomendation**: as premake does not offer any mechanism like CMake’s [BUILD_SHARED_LIBS](https://cmake.org/cmake/help/latest/variable/BUILD_SHARED_LIBS.html#variable:BUILD_SHARED_LIBS)
to externally manage the creation type of libraries, it is recommended while
using conan to **AVOID** defining the `kind` attribute on library project.

## Reference

### *class* PremakeToolchain(conanfile)

PremakeToolchain generator

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.

#### extra_cxxflags

List of extra `CXX` flags. Added to `buildoptions`.

#### extra_cflags

List of extra `C` flags. Added to `buildoptions`.

#### extra_ldflags

List of extra linker flags. Added to `linkoptions`.

#### extra_defines

List of extra preprocessor definitions. Added to `defines`.

#### project(project_name)

The returned object will also have the same properties as the workspace but will only affect
the project with the name.
:param project_name: The name of the project inside the workspace to be updated.
:return: `<PremakeProject>` object which allow to set project specific flags.

#### generate()

Creates a `conantoolchain.premake5.lua` file which will properly configure build paths,
binary paths, configuration settings and compiler/linker flags based on toolchain
configuration.
