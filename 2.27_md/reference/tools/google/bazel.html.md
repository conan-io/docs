<a id="conan-tools-google-bazel"></a>

# Bazel

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `Bazel` build helper is a wrapper around the command line invocation of bazel. It will abstract the
calls like `bazel <rcpaths> build <configs> <targets>` into Python method calls.

The helper is intended to be used in the *conanfile.py* `build()` method, to call Bazel commands automatically
when a package is being built directly by Conan (create, install)

```python
from conan import ConanFile
from conan.tools.google import Bazel

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def build(self):
        bz = Bazel(self)
        bz.build(target="//main:hello-world")
```

## Reference

### *class* Bazel(conanfile)

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.

#### build(args=None, target='//...', clean=True)

Runs “bazel <rcpaths> build <configs> <args> <targets>” command where:

* `rcpaths`: adds `--bazelrc=xxxx` per rc-file path. It listens to `BazelToolchain`
  (`--bazelrc=conan_bzl.rc`), and `tools.google.bazel:bazelrc_path` conf.
* `configs`: adds `--config=xxxx` per bazel-build configuration.
  It listens to `BazelToolchain` (`--config=conan-config`), and
  `tools.google.bazel:configs` conf.
* `args`: they are any extra arguments to add to the `bazel build` execution.
* `targets`: all the target labels.

* **Parameters:**
  * **target** – It is the target label. By default, it’s “//…” which runs all the targets.
  * **args** – list of extra arguments to pass to the CLI.
  * **clean** – boolean that indicates to run a “bazel clean” before running the “bazel build”.
    Notice that this is important to ensure a fresh bazel cache every

#### test(target=None)

Runs “bazel test <targets>” command.

### Properties

The following properties affect the `Bazel` build helper:

- `tools.build:skip_test=<bool>` (boolean) if `True`, it runs the `bazel test <target>`.

### conf

`Bazel` is affected by these [[conf]](https://docs.conan.io/2//reference/config_files/global_conf.html.md#reference-config-files-global-conf) variables:

- `tools.google.bazel:bazelrc_path`: List of paths to other bazelrc files to be used as **bazel --bazelrc=rcpath1 ... build**.
- `tools.google.bazel:configs`: List of Bazel configurations to be used as **bazel build --config=config1 ...**.

#### SEE ALSO
- [Build a simple Bazel project using Conan](https://docs.conan.io/2//examples/tools/google/bazeltoolchain/build_simple_bazel_project.html.md#examples-tools-bazel-toolchain-build-simple-bazel-project)
- [Build a simple Bazel 7.x project using Conan](https://docs.conan.io/2//examples/tools/google/bazeltoolchain/build_simple_bazel_7x_project.html.md#examples-tools-bazel-7x-toolchain-build-simple-bazel-project)
