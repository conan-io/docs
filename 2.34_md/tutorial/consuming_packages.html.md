<a id="tutorial-consuming-packages"></a>

# Consuming packages

This section shows how to build your projects using Conan to manage your dependencies. We
will begin with a basic example of a C project that uses CMake and depends on the **zlib**
library. This project will use a *conanfile.txt* file to declare its dependencies.

We will also cover how you can not only use ‘regular’ libraries with Conan but also manage
tools you may need to use while building: like CMake, msys2, MinGW, etc.

Then, we will explain different Conan concepts like settings and options and how you can
use them to build your projects for different configurations like Debug, Release, with
static or shared libraries, etc.

Also, we will explain how to transition from the *conanfile.txt* file we used in the first
example to a more powerful *conanfile.py*.

After that, we will introduce the concept of Conan build and host profiles and explain how
you can use them to cross-compile your application to different platforms.

Then, in the “Introduction to versioning” we will learn about using different versions,
defining requirements with version ranges, the concept of revisions and a brief introduction
to lockfiles to achieve reproducibility of the dependency graph.

# Table of contents

* [Build a simple CMake project using Conan](https://docs.conan.io/2//tutorial/consuming_packages/build_simple_cmake_project.html.md)
* [Using build tools as Conan packages](https://docs.conan.io/2//tutorial/consuming_packages/use_tools_as_conan_packages.html.md)
* [Building for multiple configurations: Release, Debug, Static and Shared](https://docs.conan.io/2//tutorial/consuming_packages/different_configurations.html.md)
  * [Modifying settings: use Debug configuration for the application and its dependencies](https://docs.conan.io/2//tutorial/consuming_packages/different_configurations.html.md#modifying-settings-use-debug-configuration-for-the-application-and-its-dependencies)
  * [Modifying options: linking the application dependencies as shared libraries](https://docs.conan.io/2//tutorial/consuming_packages/different_configurations.html.md#modifying-options-linking-the-application-dependencies-as-shared-libraries)
  * [Difference between settings and options](https://docs.conan.io/2//tutorial/consuming_packages/different_configurations.html.md#difference-between-settings-and-options)
  * [Introducing the concept of Package ID](https://docs.conan.io/2//tutorial/consuming_packages/different_configurations.html.md#introducing-the-concept-of-package-id)
* [Understanding the flexibility of using conanfile.py vs conanfile.txt](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md)
  * [Use the layout() method](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#use-the-layout-method)
  * [Use the validate() method to raise an error for non-supported configurations](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#use-the-validate-method-to-raise-an-error-for-non-supported-configurations)
  * [Conditional requirements using a conanfile.py](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#conditional-requirements-using-a-conanfile-py)
  * [Use the generate() method to copy resources from packages](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#use-the-generate-method-to-copy-resources-from-packages)
  * [Use the build() method and `conan build` command](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#use-the-build-method-and-conan-build-command)
* [How to cross-compile your applications using Conan: host and build contexts](https://docs.conan.io/2//tutorial/consuming_packages/cross_building_with_conan.html.md)
  * [Conan two profiles model: build and host profiles](https://docs.conan.io/2//tutorial/consuming_packages/cross_building_with_conan.html.md#conan-two-profiles-model-build-and-host-profiles)
* [Introduction to versioning](https://docs.conan.io/2//tutorial/consuming_packages/intro_to_versioning.html.md)
  * [Version ranges](https://docs.conan.io/2//tutorial/consuming_packages/intro_to_versioning.html.md#version-ranges)
  * [Revisions](https://docs.conan.io/2//tutorial/consuming_packages/intro_to_versioning.html.md#revisions)
  * [Lockfiles](https://docs.conan.io/2//tutorial/consuming_packages/intro_to_versioning.html.md#lockfiles)

#### NOTE
The Conan 2 Essentials training course is available for free at the JFrog Academy,
which covers the same topics as this documentation but in a more interactive way.
You can access it [here](https://academy.jfrog.com/path/conan-cc-package-manager?utm_source=Conan+Docs).
