<a id="examples-conanfile-layout-multiple-subprojects"></a>

# Declaring the layout when we have multiple subprojects

Please, first clone the sources to recreate this project. You can find them in the
[examples2 repository](https://github.com/conan-io/examples2) in GitHub:

```bash
$ git clone https://github.com/conan-io/examples2.git
$ cd examples2/examples/conanfile/layout/multiple_subprojects
```

Let’s say that we have a project that contains two subprojects: *hello* and *bye*, that need to
access some information that is at their same level (sibling folders). Each subproject
would be a Conan package. The structure could be something similar to this:

```text
.
├── bye
│   ├── CMakeLists.txt
│   ├── bye.cpp        # contains an #include "../common/myheader.h"
│   └── conanfile.py   # contains include(../common/myutils.cmake)
├── common
│   ├── myheader.h
│   └── myutils.cmake
└── hello
    ├── CMakeLists.txt # contains include(../common/myutils.cmake)
    ├── conanfile.py
    └── hello.cpp      # contains an #include "../common/myheader.h"
```

Both *hello* and *bye* subprojects needs to use some of the files located inside the
`common` folder (that might be used and shared by other subprojects too), and it
references them by their relative location. Note that `common` is not intended to be a
Conan package. It is just some common code that will be copied into the different
subproject packages.

We can use the `self.folders.root = ".."` layout specifier to locate the root of the
project, then use the `self.folders.subproject = "subprojectfolder"` to relocate back
most of the layout to the current subproject folder, as it would be the one containing the
build scripts, sources code, etc., so other helpers like `cmake_layout()` keep working.
Let’s see how the *conanfile.py* of *hello* could look like:

```python
import os
from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMake
from conan.tools.files import copy


class hello(ConanFile):
    name = "hello"
    version = "1.0"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain"

    def layout(self):
        self.folders.root = ".."
        self.folders.subproject = "hello"
        cmake_layout(self)

    def export_sources(self):
        source_folder = os.path.join(self.recipe_folder, "..")
        copy(self, "hello/conanfile.py", source_folder, self.export_sources_folder)
        copy(self, "hello/CMakeLists.txt", source_folder, self.export_sources_folder)
        copy(self, "hello/hello.cpp", source_folder, self.export_sources_folder)
        copy(self, "common*", source_folder, self.export_sources_folder)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.run(os.path.join(self.cpp.build.bindirs[0], "hello"))
```

Let’s build *hello* and check that it’s building correctly, using the contents of the
common folder.

```bash
$ conan install hello
$ conan build hello
...
[100%] Built target hello
conanfile.py (hello/1.0): RUN: ./hello
hello WORLD
```

You can also run a **conan create** and check that it works fine too:

```bash
$ conan create hello
...
[100%] Built target hello
conanfile.py (hello/1.0): RUN: ./hello
hello WORLD
```

#### NOTE
Note the importance of the `export_sources()` method, which is able to maintain the
same relative layout of the `hello` and `common` folders, both in the local developer
flow in the current folder, but also when those sources are copied to the Conan cache, to
be built there with `conan create` or `conan install --build=hello`. This is one of the
design principles of the `layout()`, the relative location of things must be consistent
in the user folder and in the cache.

#### SEE ALSO
- Read more about the [layout method](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md#reference-conanfile-methods-layout) and [how the
  package layout works](https://docs.conan.io/2//tutorial/developing_packages/package_layout.html.md#tutorial-package-layout).
