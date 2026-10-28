<a id="integrations-cmake"></a>

# ![cmake_logo](images/integrations/conan-cmake-logo.png) CMake

Conan provides different tools to integrate with CMake in a transparent way. Using these
tools, the consuming `CMakeLists.txt` file does not need to be aware of Conan at all. The
CMake tools also provide better IDE integration via cmake-presets.

To learn how to integrate Conan with your current CMake project you can follow the
[Conan tutorial](https://docs.conan.io/2//tutorial.html.md#tutorial) that uses CMake along all the sections.

Please also check the reference for the CMakeDeps, CMakeToolchain, and CMake tools:

- `CMakeDeps`: responsible for generating the CMake config files for all the required
  dependencies of a package.
- `CMakeConfigDeps`: A modern and better alternative to `CMakeDeps`, released in Conan 2.25
  that has several improvements and fixes.
- `CMakeToolchain`: generates all the information needed for CMake to build the packages
  according to the information passed to Conan about things like the operating system, the
  compiler to use, architecture, etc. in a `conan_toolchain.cmake` toolchain file.
  It will also generate cmake-presets files for easy
  integration with some IDEs that support this CMake feature off-the-shelf.
- `CMake` build helper is the tool used by Conan `conanfile.py` recipes to run CMake and will pass all the
  arguments that CMake needs to build successfully, such as the toolchain file, build type
  file, and all the CMake definitions set in the recipe.

The `CMakeDeps` and `CMakeConfigDeps`, together with `CMakeToolchain` follow for the classic
consumption flow described along the tutorial and many other sections in this documentation:

```bash
$ conan install ...
$ cmake --preset conan-xxxx
# or use the -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
```

This flow is important, the `conan install` command generates CMake presets and `conan_toolchain.cmake`
toolchain files that helps locating the dependencies, besides trying to align as best as possible with the profile
information. This is the recommended flow for most cases.

In extraordinary and exceptional scenarios, it might be desired for the `CMake` execution to
call `conan install` to simplify the flow, for example for some IDE integrations like the CLion one, so
the users don’t need to call `conan install` themselves.

For this purpose, the  [cmake-conan integration](https://github.com/conan-io/cmake-conan) exists.
It uses the CMake “dependency providers” feature to intercept the first `find_package()` and do a call
to `conan install` to fetch the dependencies at that point.

This `cmake-conan` project stability is not guaranteed, and it has some known issues and limitations.
Refer to the Github repository for more details. And note that calling `conan install` explicitly before
calling `cmake` is still the preferred and most recommended flow for most cases.

#### SEE ALSO
- Check the [Building your project using CMakePresets](https://docs.conan.io/2//examples/tools/cmake/cmake_toolchain/build_project_cmake_presets.html.md#examples-tools-cmake-toolchain-build-project-presets) example
- Reference for [CMakeDeps](https://docs.conan.io/2//reference/tools/cmake/cmakedeps.html.md#conan-tools-cmakedeps), [CMakeConfigDeps generator](https://docs.conan.io/2//reference/tools/cmake/cmakeconfigdeps.html.md#conan-tools-cmakeconfigdeps),
  [CMakeToolchain](https://docs.conan.io/2//reference/tools/cmake/cmaketoolchain.html.md#conan-tools-cmaketoolchain) and [CMake build helper](https://docs.conan.io/2//reference/tools/cmake/cmake.html.md#conan-tools-cmake-helper)
- [Conan tutorial](https://docs.conan.io/2//tutorial.html.md#tutorial)
