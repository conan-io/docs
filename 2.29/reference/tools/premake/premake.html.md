<a id="conan-tools-premake-premake"></a>

# Premake

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `Premake` build helper is a wrapper around the command line invocation of Premake. It will abstract the
project configuration and build command.

The helper is intended to be used in the *conanfile.py* `build()` method, to call Premake commands automatically
when a package is being built directly by Conan (create, install)

**Usage Example:**

```python
from conan.tools.premake import Premake

class Pkg(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    # The PremakeToolchain generator is always needed to use premake helper
    generators = "PremakeToolchain"

    def build(self):
        p = Premake(self)

        # Set the main Lua configuration file (default: premake5.lua)
        p.luafile = "myproject.lua"

        # Pass custom arguments to Premake (translates to --{key}={value})
        p.arguments["myarg"] = "myvalue"

        # Automatically determines the correct action:
        # - For MSVC, selects vs<version> based on the compiler version
        # - Defaults to "gmake" for other compilers
        # p.configure() will run: premake5 --file=myproject.lua <action> --{key}={value} ...
        p.configure()
        # p.build() will invoke proper compiler depending on action (automatically detected by profile)
        p.build("HelloWorld.sln")
```

## Reference

### *class* Premake(conanfile)

This class calls Premake commands when a package is being built. Notice that
this one should be used together with the `PremakeToolchain` generator.

This premake generator is only compatible with `premake5`.

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.

#### luafile

Path to the root premake5 lua file (default is `premake5.lua`)

#### arguments

Key value pairs. Will translate to “–{key}={value}”

#### configure()

Runs `premake5 <action> [FILE]` which will generate respective build scripts depending on the `action`.

#### build(workspace, targets=None, configuration=None, msbuild_platform=None)

Depending on the action, this method will run either `msbuild` or `make` with `N_JOBS`.
You can specify `N_JOBS` through the configuration line `tools.build:jobs=N_JOBS`
in your profile `[conf]` section.

* **Parameters:**
  * **workspace** – `str` Specifies the solution to be compiled (only used by `MSBuild`).
  * **targets** – `List[str]` Declare the projects to be built (None to build all projects).
  * **configuration** – `str` Specify the configuration build type, default to build_type (“Release” or “Debug”),
    but this allow setting custom configuration type.
  * **msbuild_platform** – `str` Specify the platform for the internal MSBuild generator (only used by `MSBuild`).

## conf

The `Premake` build helper is affected by these `[conf]` variables:

- `tools.build:verbosity` which accepts one of `quiet` or `verbose` and sets the `--quiet` flag in `Premake.configure()`
- `tools.compilation:verbosity` which accepts one of `quiet` or `verbose` and sets the `--verbose` flag in `Premake.build()`

## Extra configuration

By default, typical Premake configurations are `Release` and `Debug`.
This configurations could vary depending on the used Premake script.

For example,

```lua
workspace "MyProject"
    configurations { "Debug", "Release", "DebugDLL", "ReleaseDLL" }
```

If you wish to use a different configuration than `Release` or `Debug`, you can override the configuration from the `Premake` generator.

If the project also have dependencies, you will also need to override the
`configuration` property of the `PremakeDeps` generator accordingly, with the same value.

```python
class MyRecipe(Conanfile):
    ...
    def _premake_configuration(self):
        return str(self.settings.build_type) + ("DLL" if self.options.shared else "")

    def generate(self):
        deps = PremakeDeps(self)
        deps.configuration = self._premake_configuration
        deps.generate()
        tc = PremakeToolchain(self)
        tc.generate()

    def build(self):
        premake = Premake(self)
        premake.configure()
        premake.build(workspace="MyProject", configuration=self._premake_configuration)
```
