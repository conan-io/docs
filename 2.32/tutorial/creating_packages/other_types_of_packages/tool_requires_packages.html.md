<a id="tutorial-other-tool-requires-packages"></a>

# Tool requires packages

In the “[Using build tools as Conan packages](https://docs.conan.io/2//tutorial/consuming_packages/use_tools_as_conan_packages.html.md#consuming-packages-tool-requires)” section, we learned how to use
a tool require to build (or help building) our project or Conan package.
In this section, we are going to learn how to create a recipe for a tool require.

#### NOTE
**Best practice**

`tool_requires` and tool packages are intended for executable applications, like `cmake` or `ninja` that
can be used as `tool_requires("cmake/[>=3.25]")` by other packages to put those executables in their path. They
are not intended for library-like dependencies (use `requires` for them), for test frameworks (use `test_requires`)
or in general for anything that belongs to the “host” context of the final application. Do not abuse `tool_requires`
for other purposes.

Please, first clone the sources to recreate this project. You can find them in the
[examples2 repository](https://github.com/conan-io/examples2) on GitHub:

```bash
$ git clone https://github.com/conan-io/examples2.git
$ cd examples2/tutorial/creating_packages/other_packages/tool_requires/tool
```

## A simple tool require recipe

This is a recipe for a (fake) application that receiving a path returns 0 if the path is secure.
We can check how the following simple recipe covers most of the `tool-require` use-cases:

```python
import os
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import copy


class secure_scannerRecipe(ConanFile):
    name = "secure_scanner"
    version = "1.0"
    package_type = "application"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        extension = ".exe" if self.settings_build.os == "Windows" else ""
        copy(self, "*secure_scanner{}".format(extension),
             self.build_folder, os.path.join(self.package_folder, "bin"), keep_path=False)

    def package_info(self):
        self.buildenv_info.define("MY_VAR", "23")
```

There are a few relevant things in this recipe:

1. It declares `package_type = "application"`. This is optional but convenient, and will indicate to Conan that the current
   package doesn’t contain headers or libraries to be linked. Consumers will know that this package is an application.
2. The `package()` method is packaging the executable into the `bin/` folder, that is declared by default as a bindir:
   `self.cpp_info.bindirs = ["bin"]`.
3. In the `package_info()` method, we are using `self.buildenv_info` to define an environment variable `MY_VAR`
   that will also be available to consumers.

Let’s create a binary package for the `tool_require`:

```bash
$ conan create . --build-require
...
secure_scanner/1.0: Calling package()
secure_scanner/1.0: Copied 1 file: secure_scanner
secure_scanner/1.0 package(): Packaged 1 file: secure_scanner
...
Security Scanner: The path 'mypath' is secure!
```

#### IMPORTANT
Use `--build-require` argument.

The `conan create` command by default creates packages for the “host” context, using
the “host” profile. But if the package we are creating is intended to be used as a tool with
`tool_requires`, then it needs to be built for the “build” context.

The `--build-require` argument specifies this. When this argument is provided, the
current recipe binary will be built for the “build” context.
Because the `secure_scanner/1.0` package is a package which executables run in the
current “build” machine, not necessarily in the final “host” machine, that could be
different to the build one, for example in the case of a cross-build.

The `--build-require` argument is necessary to build the `secure_scanner` package correctly
as a build tool.

Let’s review the `test_package/conanfile.py`:

```python
from conan import ConanFile


class secure_scannerTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def test(self):
        extension = ".exe" if self.settings_build.os == "Windows" else ""
        self.run("secure_scanner{} mypath".format(extension))
```

We are requiring the `secure_scanner` package as `tool_require` doing `self.tool_requires(self.tested_reference_str)`.
In the `test()` method, we are running the application because it is available in the PATH. In the
next example, we are going to see why the executables from a `tool_require` are available to consumers.

Let’s create a consumer recipe to test if we can run the `secure_scanner` application of the `tool_require` and
read the environment variable. Go to the examples2/tutorial/creating_packages/other_packages/tool_requires/consumer
folder:

```python
from conan import ConanFile

class MyConsumer(ConanFile):
    name = "my_consumer"
    version = "1.0"
    settings = "os", "arch", "compiler", "build_type"
    tool_requires = "secure_scanner/1.0"

    def build(self):
        extension = ".exe" if self.settings_build.os == "Windows" else ""
        self.run("secure_scanner{} {}".format(extension, self.build_folder))
        if self.settings_build.os != "Windows":
            self.run("echo MY_VAR=$MY_VAR")
        else:
            self.run("set MY_VAR")
```

In this simple recipe we are declaring a `tool_require` to `secure_scanner/1.0` and we are calling directly the packaged
application `secure_scanner` in the `build()` method, also printing the value of the `MY_VAR` env variable.

If we build the consumer:

```bash
$ conan build .

-------- Installing (downloading, building) binaries... --------
secure_scanner/1.0: Already installed!

-------- Finalizing install (deploy, generators) --------
...
conanfile.py (my_consumer/1.0): RUN: secure_scanner /Users/luism/workspace/examples2/tutorial/creating_packages/other_packages/tool_requires/consumer
...
Security Scanner: The path '/Users/luism/workspace/examples2/tutorial/creating_packages/other_packages/tool_requires/consumer' is secure!
...
MY_VAR=23
```

We can see that the executable returned 0 (because our folder is secure) and it printed `Security Scanner: The path is secure!` message.
It also printed the “23” value assigned to `MY_VAR` but, why are these automatically available?

- The generators `VirtualBuildEnv` and `VirtualRunEnv` are automatically used.
- The `VirtualRunEnv` is reading the `tool-requires` and is creating a launcher like `conanbuildenv-release-x86_64.sh` appending
  all `cpp_info.bindirs` to the `PATH`, all the `cpp_info.libdirs` to the `LD_LIBRARY_PATH` environment variable and
  declaring each variable of `self.buildenv_info`.
- Every time conan executes `self.run`, it, by default, activates the `conanbuild.sh` file before calling any command.
  The `conanbuild.sh` is including the `conanbuildenv-release-x86_64.sh`, so the application is in the PATH
  and the environment variable “MYVAR” has the value declared in the `tool-require`.

## Removing settings in package_id()

With the previous recipe, if we call **conan create** with different settings like different compiler versions, we will get
different binary packages with a different `package ID`. This might be convenient to, for example, keep better traceability of
our tools. In this case, the [compatibility.py](https://docs.conan.io/2//reference/extensions/binary_compatibility.html.md#reference-extensions-binary-compatibility) plugin can help to locate the best matching binary in case Conan doesn’t find the
binary for our specific compiler version.

But in some cases we might want to just generate a binary taking into account only the `os`, `arch` or at most
adding the `build_type` to know if the application is built for Debug or Release. We can add a `package_id()` method
to remove them:

```python
import os
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import copy


class secure_scannerRecipe(ConanFile):
    name = "secure_scanner"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    ...

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type
```

So, if we call **conan create** with different `build_type` we will get exactly the same `package_id`.

```bash
$ conan create .
...
Package '82339cc4d6db7990c1830d274cd12e7c91ab18a1' created

$ conan create . -s build_type=Debug
...
Package '82339cc4d6db7990c1830d274cd12e7c91ab18a1' created
```

We got the same binary `package_id`. The second command `conan create . -s build_type=Debug` created and overwrote the previous Release binary
(it created a newer package revision), because they have the same `package_id` identifier.
It is typical to create only the `Release` one, and if for any reason managing both Debug and Release binaries is intended,
then the approach would be not removing the `del self.info.settings.build_type`.

#### SEE ALSO
- [JFrog Academy Conan 2 Essentials Module 3, Lesson 16: Creating Tool Require Packages](https://academy.jfrog.com/path/conan-cc-package-manager/conan-2-essentials-module-3-advanced-package-creation-scenarios?utm_source=Conan+Docs)
- [Using the same requirement as a requires and as a tool_requires](https://docs.conan.io/2//examples/graph/tool_requires/using_protobuf.html.md#examples-graph-tool-requires-protobuf)
- Toolchains (compilers)
- [Usage of runenv_info](https://docs.conan.io/2//reference/conanfile/methods/package_info.html.md#reference-conanfile-methods-package-info-runenv-info)
- [More info on settings_target](https://docs.conan.io/2//reference/binary_model/extending.html.md#binary-model-extending-cross-build-target-settings)
