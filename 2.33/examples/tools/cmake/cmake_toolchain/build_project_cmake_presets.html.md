<a id="examples-tools-cmake-toolchain-build-project-presets"></a>

# CMakeToolchain: Building your project using CMakePresets

In this example we are going to see how to use `CMakeToolchain`, predefined layouts like `cmake_layout` and the
`CMakePresets` CMake feature.

Let’s create a basic project based on the template `cmake_exe` as an example of a C++ project:

```bash
$ conan new cmake_exe -d name=foo -d version=1.0
```

## Generating the toolchain

The recipe from our project declares the generator “CMakeToolchain”.

We can call **conan install** to install both `Release` and `Debug`
configurations. Conan will generate a `conan_toolchain.cmake` at the corresponding
*generators* folder:

```bash
$ conan install .
$ conan install . -s build_type=Debug
```

## Building the project using `CMakePresets`

A `CMakeUserPresets.json` file is generated in the same folder of your `CMakeLists.txt` file,
so you can use the `--preset` argument from `cmake >= 3.23` or use an IDE that supports it.

The `CMakeUserPresets.json` is including the `CMakePresets.json` files located at the
corresponding *generators* folder.

The `CMakePresets.json` contain information about the `conan_toolchain.cmake` location
and even the `binaryDir` set with the output directory.

#### NOTE
We use CMake presets in this example. This requires CMake >= 3.23 because the
“include” from `CMakeUserPresets.json` to `CMakePresets.json` is only supported
since that version. If you prefer not to use presets you can use something like:

```bash
cmake <path> -G <CMake generator> -DCMAKE_TOOLCHAIN_FILE=<path to
conan_toolchain.cmake> -DCMAKE_BUILD_TYPE=Release
```

Conan will show the exact CMake command everytime you run `conan install` in case
you can’t use the presets feature.

If you are using a multi-configuration generator:

```bash
$ cmake --preset conan-default
$ cmake --build --preset conan-debug
$ build\Debug\foo.exe
foo/1.0: Hello World Debug!

$ cmake --build --preset conan-release
$ build\Release\foo.exe
foo/1.0: Hello World Release!
```

If you are using a single-configuration generator:

```bash
$ cmake --preset conan-debug
$ cmake --build --preset conan-debug
$ ./build/Debug/foo
foo/1.0: Hello World Debug!


$ cmake --preset conan-release
$ cmake --build --preset conan-release
$ ./build/Release/foo
foo/1.0: Hello World Release!
```

Note that we didn’t need to create the `build/Release` or `build/Debug` folders, as we did [in the
tutorial](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#consuming-packages-flexibility-of-conanfile-py-use-layout). The output directory
is declared by the `cmake_layout()` and automatically managed by the CMake Presets feature.

This behavior is also managed automatically by Conan (with CMake >= 3.15) when you build a package in the Conan
cache (with **conan create** command). The CMake >= 3.23 is not required.

Read More:

- `cmake_layout()` [reference](https://docs.conan.io/2//reference/tools/cmake/cmake_layout.html.md#cmake-layout)
- Conanfile [layout() method reference](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md#reference-conanfile-methods-layout)
- Package layout tutorial [tutorial](https://docs.conan.io/2//tutorial/developing_packages/package_layout.html.md#developing-packages-layout)
- Understanding [Conan package layouts](https://docs.conan.io/2//tutorial/developing_packages/package_layout.html.md#tutorial-package-layout)
