<a id="conan-tools-gnu-autotoolsdeps"></a>

# AutotoolsDeps

The `AutotoolsDeps` is the dependencies generator for Autotools. It will generate shell scripts containing
environment variable definitions that the autotools build system can understand.

It can be used by name in conanfiles:

```python
class Pkg(ConanFile):
    generators = "AutotoolsDeps"
```

```text
[generators]
AutotoolsDeps
```

And it can also be fully instantiated in the conanfile `generate()` method:

```python
from conan import ConanFile
from conan.tools.gnu import AutotoolsDeps

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def generate(self):
        tc = AutotoolsDeps(self)
        tc.generate()
```

## Generated files

It will generate the file `conanautotoolsdeps.sh` or `conanautotoolsdeps.bat`:

```bash
$ conan install conanfile.py # default is Release
$ source conanautotoolsdeps.sh
# or in Windows
$ conanautotoolsdeps.bat
```

These launchers will define aggregated variables `CPPFLAGS`, `LIBS`, `LDFLAGS`, `CXXFLAGS`, `CFLAGS` that
accumulate all dependencies information, including transitive dependencies, with flags like `-I<path>`, `-L<path>`, etc.

At this moment, only the `requires` information is generated, the `tool_requires` one is not managed by this generator yet.

## Customization

To modify the computed values, you can access the `.environment` property that returns an
[Environment](https://docs.conan.io/2//reference/tools/env/environment.html.md#conan-tools-env-environment-model) class.

```python
from conan import ConanFile
from conan.tools.gnu import AutotoolsDeps

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def generate(self):
        tc = AutotoolsDeps(self)
        tc.environment.remove("CPPFLAGS", "undesired_value")
        tc.environment.append("CPPFLAGS", "var")
        tc.environment.define("OTHER", "cat")
        tc.environment.unset("LDFLAGS")
        tc.generate()
```

## Reference

### *class* AutotoolsDeps(conanfile)

#### *property* environment

* **Returns:**
  An `Environment` object containing the computed variables. If you need
  to modify some of the computed values you can access to the `environment` object.
