<a id="conan-tools-microsoft-msbuild"></a>

# MSBuild

The `MSBuild` build helper is a wrapper around the command line invocation of MSBuild. It abstracts the
calls like `msbuild "MyProject.sln" /p:Configuration=<conf> /p:Platform=<platform>` into Python method ones.

This helper can be used like:

```python
from conan import ConanFile
from conan.tools.microsoft import MSBuild

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def build(self):
        msbuild = MSBuild(self)
        msbuild.build("MyProject.sln")
```

The `MSBuild.build()` method internally implements a call to `msbuild` like:

```bash
$ <vcvars-cmd> && msbuild "MyProject.sln" /p:Configuration=<configuration> /p:Platform=<platform>
```

Where:

- `<vcvars-cmd>` calls the Visual Studio prompt that matches the current recipe `settings`.
- `configuration`, typically Release, Debug, which will be obtained from `settings.build_type`
  but this can be customized with the `build_type` attribute.
- `<platform>` is the architecture, a mapping from the `settings.arch` to the common ‘x86’, ‘x64’, ‘ARM’, ‘ARM64’, ‘ARM64EC’.
  This can be customized with the `platform` attribute.

## Customization

### attributes

You can customize the following attributes in case you need to change them:

- **build_type** (default `settings.build_type`): Value for the `/p:Configuration`.
- **platform** (default based on `settings.arch` to select one of these values: (`'x86', 'x64', 'ARM', 'ARM64', 'ARM64EC'`):
  Value for the `/p:Platform`.

Example:

```python
from conan import ConanFile
from conan.tools.microsoft import MSBuild
class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    def build(self):
        msbuild = MSBuild(self)
        msbuild.build_type = "MyRelease"
        msbuild.platform = "MyPlatform"
        msbuild.build("MyProject.sln")
```

### conf

`MSBuild` is affected by these `[conf]` variables:

- `tools.build:verbosity` accepts one of `quiet` or `verbose` to be passed
  to the `MSBuild.build()` call as `msbuild .... /verbosity:{Quiet,Detailed}`.
- `tools.microsoft.msbuild:max_cpu_count` maximum number of CPUs to be passed to the `MSBuild.build()`
  call as `msbuild .... /m:N`. If `max_cpu_count=0`, then it will use `/m` without arguments, which means use all available cpus.

## Reference

### *class* MSBuild(conanfile)

MSBuild build helper class

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.

#### command(sln, targets=None)

Gets the `msbuild` command line. For instance,
**msbuild.exe "MyProject.sln" -p:Configuration=<conf> -p:Platform=<platform>**.

* **Parameters:**
  * **sln** – `str` name of Visual Studio `*.sln` file
  * **targets** – `targets` is an optional argument, defaults to `None`, and otherwise it is a list of targets to build
* **Returns:**
  `str` msbuild command line.

#### build(sln, targets=None)

Runs the `msbuild` command line obtained from `self.command(sln)`.

* **Parameters:**
  * **sln** – `str` name of Visual Studio `*.sln` file
  * **targets** – `targets` is an optional argument, defaults to `None`, and otherwise it is a list of targets to build
