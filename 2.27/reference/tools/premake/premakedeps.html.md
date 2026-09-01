<a id="conan-tools-premake-premakedeps"></a>

# PremakeDeps

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `PremakeDeps` is the dependencies generator for Premake.
The generator can be used by name in conanfiles:

```python
class Pkg(ConanFile):
    generators = "PremakeDeps"
```

```text
[generators]
PremakeDeps
```

And it can also be fully instantiated in the conanfile `generate()` method:

```python
from conan import ConanFile
from conan.tools.premake import PremakeDeps

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    requires = "zlib/1.3.1"

    def generate(self):
        deps = PremakeDeps(self)
        deps.generate()
```

#### IMPORTANT
The `PremakeDeps` generator must be used in conjunction with the
[PremakeToolchain](https://docs.conan.io/2//reference/tools/premake/premaketoolchain.html.md#conan-tools-premake-premaketoolchain) generator, as it will
generate a `include('conandeps.premake5.lua')` that will be automatically
included by the toolchain.

## Generated files

`PremakeDeps` will generate a `conandeps.premake5.lua` script file which
will be injected later by the toolchain and the following files per dependency in the `conanfile.generators_folder`:

- `conan_<pkg>.premake5.lua`: will be including the proper script depending on the `build_type` and architecture.
- `conan_<pkg>_vars_<config>.premake5.lua`: will contain essentially the following information for the specific dependency, architecture and build_type:
  > - `includedirs`
  > - `libdirs`
  > - `bindirs`
  > - `sysincludedirs`
  > - `frameworkdirs`
  > - `frameworks`
  > - `libs`
  > - `syslibs`
  > - `defines`
  > - `cxxflags`
  > - `cflags`
  > - `sharedlinkflags`
  > - `exelinkflags`

All this information will be loaded in the `conandeps.premake5.lua` script
and injected later to the main premake script, allowing a transparent and easy to use dependency management with conan.
