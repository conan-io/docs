<a id="conan-tools-layout"></a>

# conan.tools.layout

<a id="conan-tools-layout-predefined-layouts"></a>

## Predefined layouts

There are some pre-defined common [layouts](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md#reference-conanfile-methods-layout), ready to be simply used in recipes:

- `cmake_layout()`: [a layout for a typical CMake project](https://docs.conan.io/2//reference/tools/cmake/cmake_layout.html.md#cmake-layout)
- `vs_layout()`: a layout for a typical Visual Studio project
- `basic_layout()`: [a very basic layout for a generic project](#conan-tools-basic-layout)

The pre-defined layouts define the Conanfile `.folders` and `.cpp` attributes with
typical values. To check which values are set by these pre-defined layouts please
check the reference for the [layout()](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md#reference-conanfile-methods-layout) method. For example in the
`cmake_layout()` the source folder is set to `"."`, meaning that Conan will expect
the sources in the same directory where the conanfile is (most likely the project root,
where a `CMakeLists.txt` file will be typically found). If you have a different folder
where the `CMakeLists.txt` is located, you can use the `src_folder` argument:

```python
from conan.tools.cmake import cmake_layout

def layout(self):
    cmake_layout(self, src_folder="mysrcfolder")
```

Even if this pre-defined layout doesn’t suit your specific projects layout, checking how
they implement their logic shows how you could implement your own logic (and probably put
it in a common `python_require` if you are going to use it in multiple packages).

To learn more about the layouts and how to use them while developing packages, please
check the Conan package layout [tutorial](https://docs.conan.io/2//tutorial/developing_packages/package_layout.html.md#developing-packages-layout).

<a id="conan-tools-basic-layout"></a>

## basic_layout

Usage:

```python
from conan.tools.layout import basic_layout

def layout(self):
    basic_layout(self)
```

The current layout implementation is very simple, basically sets a different build folder for different build_types
and sets the generators output folder inside the build folder. This way we avoid to clutter our project
while working locally. If you prefer, you can define the build_folder to take control over the destination folder,
so the temporary build files do not pollute the source tree.

```python
def basic_layout(conanfile, src_folder=".", build_folder=None):
    subproject = conanfile.folders.subproject

    conanfile.folders.source = src_folder if not subproject else os.path.join(subproject, src_folder)
    if build_folder:
        conanfile.folders.build = build_folder if not subproject else os.path.join(subproject, build_folder)
    else:
        conanfile.folders.build = "build" if not subproject else os.path.join(subproject, "build")
        if conanfile.settings.get_safe("build_type"):
            conanfile.folders.build += "-{}".format(str(conanfile.settings.build_type).lower())
    conanfile.folders.generators = os.path.join(conanfile.folders.build, "conan")
    conanfile.cpp.build.bindirs = ["."]
    conanfile.cpp.build.libdirs = ["."]

    if not conanfile.cpp.source.includedirs:
        conanfile.cpp.source.includedirs = ["include"]
```
