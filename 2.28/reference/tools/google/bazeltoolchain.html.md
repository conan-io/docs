<a id="conan-tools-google-bazeltoolchain"></a>

# BazelToolchain

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `BazelToolchain` is the toolchain generator for Bazel. It will generate a `conan_bzl.rc` file that contains
a build configuration `conan-config` to inject all the parameters into the **bazel build** command.

The `BazelToolchain` generator can be used by name in conanfiles:

```python
class Pkg(ConanFile):
    generators = "BazelToolchain"
```

```text
[generators]
BazelToolchain
```

And it can also be fully instantiated in the conanfile `generate()` method:

```python
from conan import ConanFile
from conan.tools.google import BazelToolchain

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def generate(self):
        tc = BazelToolchain(self)
        tc.generate()
```

## Generated files

After running **conan install** command, the `BazelToolchain` generates the *conan_bzl.rc* file
that contains Bazel build parameters (it will depend on your current Conan settings and options from your *default* profile):

```text
# Automatic bazelrc file created by Conan

build:conan-config --cxxopt=-std=gnu++17

build:conan-config --dynamic_mode=off
build:conan-config --compilation_mode=opt
```

The [Bazel build helper](https://docs.conan.io/2//reference/tools/google/bazel.html.md#conan-tools-google-bazel) will use that `conan_bzl.rc` file to perform a call using this
configuration. The outcoming command will look like this **bazel --bazelrc=/path/to/conan_bzl.rc build --config=conan-config <target>**.

## Reference

### *class* BazelToolchain(conanfile)

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.

#### force_pic

Boolean used to add –force_pic=True. Depends on self.options.shared and
self.options.fPIC values

#### dynamic_mode

String used to add –dynamic_mode=[“fully”|”off”]. Depends on self.options.shared value.

#### cppstd

String used to add –cppstd=[FLAG]. Depends on your settings.

#### copt

List of flags used to add –copt=flag1 … –copt=flagN

#### conlyopt

List of flags used to add –conlyopt=flag1 … –conlyopt=flagN

#### cxxopt

List of flags used to add –cxxopt=flag1 … –cxxopt=flagN

#### linkopt

List of flags used to add –linkopt=flag1 … –linkopt=flagN

#### compilation_mode

String used to add –compilation_mode=[“opt”|”dbg”]. Depends on self.settings.build_type

#### compiler

String used to add –compiler=xxxx.

#### cpu

String used to add –cpu=xxxxx. At the moment, it’s only added if cross-building.

#### crosstool_top

String used to add –crosstool_top.

#### generate()

Creates a `conan_bzl.rc` file with some bazel-build configuration. This last mentioned
is put as `conan-config`.

### conf

`BazelToolchain` is affected by these [[conf]](https://docs.conan.io/2//reference/config_files/global_conf.html.md#reference-config-files-global-conf) variables:

- `tools.build:cxxflags` list of extra C++ flags that will be used by `cxxopt`.
- `tools.build:cflags` list of extra of pure C flags that will be used by `conlyopt`.
- `tools.build:sharedlinkflags` list of extra linker flags that will be used by `linkopt`.
- `tools.build:exelinkflags` list of extra linker flags that will be used by `linkopt`.
- `tools.build:linker_scripts` list of linker scripts, each of which will be prefixed with `-T` and added to `linkopt`.

#### SEE ALSO
- [Build a simple Bazel project using Conan](https://docs.conan.io/2//examples/tools/google/bazeltoolchain/build_simple_bazel_project.html.md#examples-tools-bazel-toolchain-build-simple-bazel-project)
- [Build a simple Bazel 7.x project using Conan](https://docs.conan.io/2//examples/tools/google/bazeltoolchain/build_simple_bazel_7x_project.html.md#examples-tools-bazel-7x-toolchain-build-simple-bazel-project)
