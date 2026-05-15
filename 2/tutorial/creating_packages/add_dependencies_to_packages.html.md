<a id="creating-packages-add-dependencies-to-packages"></a>

# Add dependencies to packages

In the [previous tutorial section](https://docs.conan.io/2//tutorial/creating_packages.html.md#tutorial-creating-packages), we created a Conan
package for a “Hello World” C++ library. We used the
[conan.tools.scm.Git()](https://docs.conan.io/2//reference.html.md#reference) tool to retrieve the sources from a git
repository. So far, the package does not have any dependency on other Conan packages.
Let’s explain how to add a dependency to our package in a very similar way to how we did in
the [consuming packages section](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#consuming-packages-flexibility-of-conanfile-py). We
will add some fancy colour output to our “Hello World” library using the [fmt](https://conan.io/center/fmt) library.

Please, first clone the sources to recreate this project. You can find them in the
[examples2 repository](https://github.com/conan-io/examples2) on GitHub:

```bash
$ git clone https://github.com/conan-io/examples2.git
$ cd examples2/tutorial/creating_packages/add_requires
```

You will notice some changes in the conanfile.py file from the previous recipe.
Let’s check the relevant parts:

```python
...
from conan.tools.build import check_max_cppstd, check_min_cppstd
...

class helloRecipe(ConanFile):
    name = "hello"
    version = "1.0"

    ...
    generators = "CMakeDeps"
    ...

    def validate(self):
        check_min_cppstd(self, "11")
        check_max_cppstd(self, "20")

    def requirements(self):
        self.requires("fmt/8.1.1")

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/conan-io/libhello.git", target=".")
        # Please, be aware that using the head of the branch instead of an immutable tag
        # or commit is not a good practice in general
        git.checkout("require_fmt")
```

* First, we set the `generators` class attribute to make Conan invoke the
  [CMakeDeps](https://docs.conan.io/2//reference/tools/cmake/cmakedeps.html.md#conan-tools-cmakedeps) generator. This was not needed in the previous recipe as we
  did not have dependencies. `CMakeDeps` will generate all the config files that CMake needs
  to find the `fmt` library.
* Next, we use the [requires()](https://docs.conan.io/2//reference/conanfile/methods.html.md#reference-conanfile-methods) method to add the
  [fmt](https://conan.io/center/fmt)  dependency to our package.
* Note that we added an extra line in the [source()](https://docs.conan.io/2//reference/conanfile/methods.html.md#reference-conanfile-methods)
  method. We use the `Git().checkout()` method to checkout the source code in the
  [require_fmt](https://github.com/conan-io/libhello/tree/require_fmt) branch. This
  branch contains the changes in the source code to add colours to the library messages,
  and also in the `CMakeLists.txt` to declare that we are using the `fmt` library.
* Finally, note we added the [validate()](https://docs.conan.io/2//reference/conanfile/methods.html.md#reference-conanfile-methods) method to the
  recipe. We already used this method in the [consuming packages
  section](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#consuming-packages-flexibility-of-conanfile-py) to raise an error for
  non-supported configurations. Here, we call the functions
  [check_min_cppstd()](https://docs.conan.io/2//reference/tools/build.html.md#conan-tools-build-check-min-cppstd) and
  [check_max_cppstd()](https://docs.conan.io/2//reference/tools/build.html.md#conan-tools-build-check-max-cppstd) to verify that we are using at
  least C++11 and at most C++20 standards in our settings.

You can check the new sources using the fmt library in the
[require_fmt](https://github.com/conan-io/libhello/tree/require_fmt) branch. You will see that
the [hello.cpp](https://github.com/conan-io/libhello/blob/require_fmt/src/hello.cpp)
file adds colours to the output messages:

```cpp
#include <fmt/color.h>

#include "hello.h"

void hello(){
    #ifdef NDEBUG
    fmt::print(fg(fmt::color::crimson) | fmt::emphasis::bold, "hello/1.0: Hello World Release!\n");
    #else
    fmt::print(fg(fmt::color::crimson) | fmt::emphasis::bold, "hello/1.0: Hello World Debug!\n");
    #endif
    ...
```

Let’s build the package from sources with the current default configuration, and then let
the `test_package` folder test the package. You should see the output messages with
colour now:

```bash
$ conan create . --build=missing
-------- Exporting the recipe ----------
...
-------- Testing the package: Running test() ----------
hello/1.0 (test package): Running test()
hello/1.0 (test package): RUN: ./example
hello/1.0: Hello World Release!
  hello/1.0: __x86_64__ defined
  hello/1.0: __cplusplus 201103
  hello/1.0: __GNUC__ 4
  hello/1.0: __GNUC_MINOR__ 2
  hello/1.0: __clang_major__ 13
  hello/1.0: __clang_minor__ 1
  hello/1.0: __apple_build_version__ 13160021
```

<a id="tutorial-create-packages-headers-transitivity"></a>

## Headers transitivity

By default, Conan assumes that the required dependency headers are an implementation detail of the current package,
to promote good software engineering practices like low coupling and encapsulation. In the example above, `fmt`
is purely an implementation detail in the `hello/1.0` package. Consumers of `hello/1.0` will not know anything
about `fmt`, or has access to its headers, if a consumer of `hello/1.0` would try to add a `#include <fmt/color.h>`,
it will fail, not being able to find that headers.

But if the public headers of the `hello/1.0` package have the `#include` to `fmt` headers, that means that such
headers must be propagated down to allow consumers of `hello/1.0` to be compiled successfully. As this is not the
default expected behavior, recipes must declare it as:

```python
class helloRecipe(ConanFile):
    name = "hello"
    version = "1.0"

    def requirements(self):
        self.requires("fmt/8.1.1", transitive_headers=True)
```

That will propagate the necessary compilation flags and headers `includedirs` to the consumers of `hello/1.0`.

#### NOTE
**Best practices**

If a consumer of `hello/1.0` had a direct inclusion to `fmt` headers such as `#include <fmt/color.h>`, then,
such a consumer should declare its own `self.requires("fmt/8.1.1")` requirement, as that is a direct requirement.
In other words, even if the dependency to `hello/1.0` was removed from that consumer, it would still depend on `fmt`,
and consequently it cannot abuse the transitivity of the `fmt` headers from `hello`, but declare them explicitly.

#### SEE ALSO
- [JFrog Academy Conan 2 Essentials Module 2, Lesson 9: Dependencies, Generators And Building](https://academy.jfrog.com/path/conan-cc-package-manager/conan-2-essentials-module-2-package-creation-and-uploading?utm_source=Conan+Docs)
- [Reference for requirements() method](https://docs.conan.io/2//reference/conanfile/methods/requirements.html.md#reference-conanfile-methods-requirements).
- [Introduction to versioning](https://docs.conan.io/2//tutorial/consuming_packages/intro_to_versioning.html.md#consuming-packages-intro-versioning).
