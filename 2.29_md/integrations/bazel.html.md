<a id="integrations-bazel"></a>

# ![bazel_logo](images/integrations/conan-bazel-logo.png) Bazel

Conan provides different tools to help manage your projects using Bazel. They can be
imported from `conan.tools.google`. The most relevant tools are:

- `BazelDeps`: the dependencies generator for Bazel, which generates a  *[DEPENDENCY]/BUILD.bazel* file for each dependency
  and a *dependencies.bzl* file containing a Bazel function to load all those ones. That function must be loaded by your
  *WORKSPACE* file.
- `BazelToolchain`: the toolchain generator for Bazel, which generates a `conan_bzl.rc` file that contains
  a build configuration `conan-config` to inject all the parameters into the **bazel build** command.
- `Bazel`: the Bazel build helper. It’s simply a wrapper around the command line invocation of Bazel.

#### SEE ALSO
- Reference for [BazelDeps](https://docs.conan.io/2//reference/tools/google/bazeldeps.html.md#conan-tools-google-bazeldeps).
- Reference for [BazelToolchain](https://docs.conan.io/2//reference/tools/google/bazeltoolchain.html.md#conan-tools-google-bazeltoolchain).
- Reference for [Bazel](https://docs.conan.io/2//reference/tools/google/bazel.html.md#conan-tools-google-bazel).
- [Build a simple Bazel project using Conan](https://docs.conan.io/2//examples/tools/google/bazeltoolchain/build_simple_bazel_project.html.md#examples-tools-bazel-toolchain-build-simple-bazel-project)
- [Build a simple Bazel 7.x project using Conan](https://docs.conan.io/2//examples/tools/google/bazeltoolchain/build_simple_bazel_7x_project.html.md#examples-tools-bazel-7x-toolchain-build-simple-bazel-project)
