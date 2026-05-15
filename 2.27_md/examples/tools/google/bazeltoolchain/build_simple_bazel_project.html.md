<a id="examples-tools-bazel-toolchain-build-simple-bazel-project"></a>

# Build a simple Bazel project using Conan

#### WARNING
This example is Bazel 6.x compatible.

In this example, we are going to create a Hello World program
that uses one of the most popular C++ libraries: [fmt](https://fmt.dev/latest).

#### NOTE
This example is based on the main [Build a simple CMake project using Conan](https://docs.conan.io/2//tutorial/consuming_packages/build_simple_cmake_project.html.md#consuming-packages-build-simple-cmake-project)
tutorial. So we highly recommend reading it before trying out this one.

We’ll use Bazel as the build system and helper tool in this case, so you should get it installed
before going forward with this example. See [how to install Bazel](https://bazel.build/install).

Please, first clone the sources to recreate this project. You can find them in the
[examples2 repository](https://github.com/conan-io/examples2) in GitHub:

```bash
$ git clone https://github.com/conan-io/examples2.git
$ cd examples2/examples/tools/google/bazeltoolchain/6_x/string_formatter
```

We start from a very simple C++ language project with this structure:

```text
.
├── WORKSPACE
├── conanfile.txt
└── main
    ├── BUILD
    └── demo.cpp
```

This project contains a *WORKSPACE* file loading the Conan dependencies (in this case only `fmt`)
and a *main/BUILD* file which defines the *demo* bazel target and it’s in charge of using `fmt` to build a
simple Hello World program.

Let’s have a look at each file’s content:

```cpp
#include <cstdlib>
#include <fmt/core.h>

int main() {
    fmt::print("{} - The C++ Package Manager!\n", "Conan");
    return EXIT_SUCCESS;
}
```

```python
load("@//conan:dependencies.bzl", "load_conan_dependencies")
load_conan_dependencies()
```

```python
cc_binary(
    name = "demo",
    srcs = ["demo.cpp"],
    deps = [
        "@fmt//:fmt"
    ],
)
```

```ini
[requires]
fmt/10.1.1

[generators]
BazelDeps
BazelToolchain

[layout]
bazel_layout
```

Conan uses the [BazelToolchain](https://docs.conan.io/2//reference/tools/google/bazeltoolchain.html.md#conan-tools-google-bazeltoolchain) to generate a `conan_bzl.rc` file which defines the
`conan-config` bazel-build configuration. This file and the configuration are passed as parameters to the
`bazel build` command. Apart from that, Conan uses the [BazelDeps](https://docs.conan.io/2//reference/tools/google/bazeldeps.html.md#conan-tools-google-bazeldeps) generator
to create all the bazel files ( *[DEP]/BUILD.bazel* and *dependencies.bzl*) which define all the dependencies
as public bazel targets. The *WORKSPACE* above is already ready to load the *dependencies.bzl* which will tell the
*main/BUILD* all the information about the `@fmt//:fmt` bazel target.

As the first step, we should install all the dependencies listed in the `conanfile.txt`.
The command [conan install](https://docs.conan.io/2//reference/commands/install.html.md#reference-commands-install) does not only install the `fmt` package,
it also builds it from sources in case your profile does not match with a pre-built binary in your remotes.
Furthermore, it will save all the files created by the generators listed in the `conanfile.txt`
in a folder named *conan/* (default folder defined by the `bazel_layout`).

```bash
$ conan install . --build=missing
# ...
======== Finalizing install (deploy, generators) ========
conanfile.txt: Writing generators to /Users/user/develop/examples2/examples/tools/google/bazeltoolchain/6_x/string_formatter/conan
conanfile.txt: Generator 'BazelDeps' calling 'generate()'
conanfile.txt: Generator 'BazelToolchain' calling 'generate()'
conanfile.txt: Generating aggregated env files
conanfile.txt: Generated aggregated env files: ['conanbuild.sh', 'conanrun.sh']
Install finished successfully
```

Now we are ready to build and run our application:

```bash
$ bazel --bazelrc=./conan/conan_bzl.rc build --config=conan-config //main:demo
Starting local Bazel server and connecting to it...
INFO: Analyzed target //main:demo (38 packages loaded, 272 targets configured).
INFO: Found 1 target...
INFO: From Linking main/demo:
ld: warning: ignoring duplicate libraries: '-lc++'
Target //main:demo up-to-date:
  bazel-bin/main/demo
INFO: Elapsed time: 60.180s, Critical Path: 7.68s
INFO: 6 processes: 4 internal, 2 darwin-sandbox.
INFO: Build completed successfully, 6 total actions
```

```bash
$ ./bazel-bin/main/demo
Conan - The C++ Package Manager!
```
