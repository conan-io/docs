<a id="conan-tools-microsoft-vcvars"></a>

# VCVars

Generates a file called `conanvcvars.bat` that activates the Visual Studio developer command prompt according
to the current settings by wrapping the [vcvarsall](https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=vs-2017)
Microsoft bash script.

The `VCVars` generator can be used by name in conanfiles:

```python
class Pkg(ConanFile):
    generators = "VCVars"
```

```text
[generators]
VCVars
```

And it can also be fully instantiated in the conanfile `generate()` method:

```python
from conan import ConanFile
from conan.tools.microsoft import VCVars

class Pkg(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    requires = "zlib/1.3.1", "bzip2/1.0.8"

    def generate(self):
        ms = VCVars(self)
        ms.generate()
```

## Customization

### conf

`VCVars` is affected by these `[conf]` variables:

- `tools.microsoft.msbuild:installation_path` indicates the path to Visual Studio installation folder.
  For instance: `C:\Program Files (x86)\Microsoft Visual Studio\2019\Community`, `C:\Program Files (x86)\Microsoft Visual Studio 14.0`, etc.
- `tools.microsoft:winsdk_version` defines the specific winsdk version in the vcvars command line.
- `tools.env.virtualenv:powershell` generates an additional `conanvcvars.ps1` so it can be run from the Powershell console.

## Reference

### *class* VCVars(conanfile)

VCVars class generator to generate a `conanvcvars.bat` script that activates the correct
Visual Studio prompt.

This generator will be automatically called by other generators such as `CMakeToolchain`
when considered necessary, for example if building with Visual Studio compiler using the
CMake `Ninja` generator, which needs an active Visual Studio prompt.
Then, it is not necessary to explicitly instantiate this generator in most cases.

* **Parameters:**
  **conanfile** – `ConanFile object` The current recipe object. Always use `self`.

#### generate(scope='build')

Creates a `conanvcvars.bat` file that calls Visual `vcvars` with the necessary
args to activate the correct Visual Studio prompt matching the Conan settings.

* **Parameters:**
  **scope** – `str` activation scope, by default “build”. It means it will add a
  call to this `conanvcvars.bat` from the aggregating general
  `conanbuild.bat`, which is the script that will be called by default
  in `self.run()` calls and build helpers such as `cmake.configure()`
  and `cmake.build()`.
