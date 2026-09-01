<a id="conan-tools-qbs-helper"></a>

# Qbs

The `Qbs` build helper is a wrapper around the command line invocation of the Qbs build tool.
It will abstract the calls like `qbs resolve`, `qbs build` and `qbs install` into Python
method calls.

The helper is intended to be used in the `build()` and `package()` methods, to call Qbs
commands automatically when a package is being built directly by Conan (create, install).

```python
from conan import ConanFile
from conan.tools.qbs import Qbs, QbsProfile, QbsDeps

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = "*.h", "*.cpp", "*.qbs",
    requires = "hello/0.1"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def generate(self):
        profile = QbsProfile(self)
        profile.generate()
        deps = QbsDeps(self)
        deps.generate()

    def build(self):
        qbs = Qbs(self)
        qbs.resolve()
        qbs.build()

    def package(self):
        qbs = Qbs(self)
        qbs.install()
```

## Reference

### *class* Qbs(conanfile, project_file=None)

Qbs helper to use together with the QbsDeps feature.
This class provides helper methods that wraps calls to the Qbs tool.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **project_file** – The name to the main project file. If not set, Qbs will try to
    autodetect the project file.

#### add_configuration(name, values)

Adds a build configuration for the multi-configuration build.
This Qbs feature is rarely needed since each conan package can contain only one
configuration, however might be useful when creating multiple versions of the same product
that should be put in the same Conan package.

* **Parameters:**
  * **name** – the name of the configuration. This corresponds to the `config` parameter
    of `qbs resolve`, `qbs build` and `qbs install` commands.
  * **values** – the dict containing Qbs properties and their values for this configuration.

#### resolve(parallel=True)

Wraps the `qbs resolve` call.
If QbsDeps generator is used, this will also set the necessary properites of the Qbs
“conan” module provider automatically adding dependencies to the project.
:param parallel: Whether to use multi-threaded resolving. Defaults to `True`.

#### build(products=None)

Wraps the `qbs build` call.

* **Parameters:**
  **products** – The list of product names to build. If not set, builds all products that
  have builtByDefault set to true. This parameter corresponds to the `--products`
  option of the `qbs build` command.

The resolve() method should be called before calling this method.

#### build_all()

Wraps the `qbs build --all-products` call.
This method builds all products, even if their builtByDefault property is false.
The resolve() method should be called before calling this method.

#### install()

Wraps the `qbs install` call.
Perfoms the installation of files marked as installable in the Qbs project.
The build() or build_all() methods should be called before calling this method.
