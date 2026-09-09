<a id="conan-tools-ros-rosenv"></a>

# ROSEnv

The `ROSEnv` generator is an environment generator that, in conjunction with [CMakeDeps](https://docs.conan.io/2//reference/tools/cmake/cmakedeps.html.md#conan-tools-cmakedeps)
and [CMakeToolchain](https://docs.conan.io/2//reference/tools/cmake/cmaketoolchain.html.md#conan-tools-cmaketoolchain), allows to consume Conan packages from a ROS package.

```text
[requires]
fmt/11.0.2

[generators]
CMakeDeps
CMakeToolchain
ROSEnv
```

This generator will create a conanrosenv.sh script with the required environment variables that allow CMake and Colcon
to locate the packages installed by Conan.

This script needs to be *sourced* before the **colcon build** command:

```bash
$ cd workspace
$ conan install ...
$ source conanrosenv.sh
$ colcon build
```

## Reference

### *class* ROSEnv(conanfile)

Generator to serve as integration for Robot Operating System 2 development workspaces.

IMPORTANT: This generator should be used together with CMakeDeps and CMakeToolchain generators.

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.

#### generate()

Creates a `conanrosenv.sh` with the environment variables that are needed to build and
execute ROS packages with Conan dependencies.
