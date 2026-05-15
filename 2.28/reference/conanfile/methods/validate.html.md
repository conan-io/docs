<a id="reference-conanfile-methods-validate"></a>

# validate()

The `validate()` method can be used to mark a package binary as “invalid”, or not working for the current configuration. For example, if we have a header-only library that doesn’t work in Windows, we could have the
following `conanfile.py`:

```python
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration

class Pkg(ConanFile):
    name = "pkg"
    version = "1.0"
    package_type = "header-library"
    settings = "os"

    def validate(self):
        if self.settings.os == "Windows":
            raise ConanInvalidConfiguration("Windows not supported")

    def package_id(self):
        self.info.clear()  # header-only
```

If we try to create this package in Windows, it will fail, but if we do it in Linux, it will succeed:

```bash
$ conan create . -s os=Windows # FAILS
...
ERROR: There are invalid packages:
pkg/1.0: Invalid: Windows not supported
$ conan create . -s os=Linux # WORKS
```

And if we try to use it in Windows, it will fail again:

```bash
$ conan install --requires=pkg/1.0 -s os=Windows # FAILS
...
ERROR: There are invalid packages:
pkg/1.0: Invalid: Windows not supported
```

When the `ConanInvalidConfiguration` causes an error, Conan application exit code will be `6`

It is possible to check the validity of a given graph without raising errors with the `conan graph info` command:

```bash
$ conan graph info --requires=pkg/1.0 -s os=Windows --filter=binary
conanfile:
ref: conanfile
binary: None
pkg/1.0#cfc18fcc7a50ead278a7c1820be74e56:
ref: pkg/1.0#cfc18fcc7a50ead278a7c1820be74e56
binary: Invalid
```

The `validate()` method is evaluated after the whole graph has been computed. This means that it can use the `self.dependencies` information to raise errors:

```python
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration

class Pkg(ConanFile):
    requires = "dep/0.1"

    def validate(self):
        if self.dependencies["dep"].options.myoption == 2:
            raise ConanInvalidConfiguration("Option 2 of 'dep' not supported")
```

#### NOTE
**Best practices**

The `configure()` method evaluates before the graph is complete, so it doesn’t have the real values of the dependencies `options`. The `validate()` method is the one that should be checking those dependencies options values if necessary, not `configure()`.

#### SEE ALSO
- Follow the [tutorial about preparing build from source in recipes](https://docs.conan.io/2//tutorial/creating_packages/preparing_the_build.html.md#creating-packages-preparing-the-build).
