<a id="tutorial-creating-packages"></a>

# Creating packages

This section shows how to create Conan packages using a Conan recipe. We begin by creating
a basic Conan recipe to package a simple C++ library that you can scaffold using the
**conan new** command. Then, we will explain the different methods that you can
define inside a Conan recipe and the things you can do inside them:

* Using the `source()` method to retrieve sources from external repositories and apply
  patches to those sources.
* Add requirements to your Conan packages inside the `requirements()` method.
* Use the `generate()` method to prepare the package build, and customize the toolchain.
* Configure settings and options in the `configure()` and `config_options()`
  methods and how they affect the packages’ binary compatibility.
* Use the `build()` method to customize the build process and launch the tests for the
  library you are packaging.
* Select which files will be included in the Conan package using the `package()` method.
* Define the package information in the `package_info()` method so that consumers
  of this package can use it.
* Use a *test_package* to test that the Conan package can be consumed correctly.

After this walkthrough around some Conan recipe methods, we will explain some
peculiarities of different types of Conan packages like, for example, header-only
libraries, packages for pre-built binaries, packaging tools for building other packages or
packaging your own applications.

# Table of contents

* [Create your first Conan package](https://docs.conan.io/2//tutorial/creating_packages/create_your_first_package.html.md)
  * [A note about the Conan cache](https://docs.conan.io/2//tutorial/creating_packages/create_your_first_package.html.md#a-note-about-the-conan-cache)
* [Handle sources in packages](https://docs.conan.io/2//tutorial/creating_packages/handle_sources_in_packages.html.md)
  * [Sources from a *zip* file stored in a remote repository](https://docs.conan.io/2//tutorial/creating_packages/handle_sources_in_packages.html.md#sources-from-a-zip-file-stored-in-a-remote-repository)
  * [Sources from a branch in a *git* repository](https://docs.conan.io/2//tutorial/creating_packages/handle_sources_in_packages.html.md#sources-from-a-branch-in-a-git-repository)
  * [Using the conandata.yml file](https://docs.conan.io/2//tutorial/creating_packages/handle_sources_in_packages.html.md#using-the-conandata-yml-file)
* [Add dependencies to packages](https://docs.conan.io/2//tutorial/creating_packages/add_dependencies_to_packages.html.md)
  * [Headers transitivity](https://docs.conan.io/2//tutorial/creating_packages/add_dependencies_to_packages.html.md#headers-transitivity)
* [Preparing the build](https://docs.conan.io/2//tutorial/creating_packages/preparing_the_build.html.md)
* [Configure settings and options in recipes](https://docs.conan.io/2//tutorial/creating_packages/configure_options_settings.html.md)
  * [Conan packages binary compatibility: the **package ID**](https://docs.conan.io/2//tutorial/creating_packages/configure_options_settings.html.md#conan-packages-binary-compatibility-the-package-id)
* [Build packages: the build() method](https://docs.conan.io/2//tutorial/creating_packages/build_packages.html.md)
  * [Build and run tests for your project](https://docs.conan.io/2//tutorial/creating_packages/build_packages.html.md#build-and-run-tests-for-your-project)
  * [Conditionally patching the source code](https://docs.conan.io/2//tutorial/creating_packages/build_packages.html.md#conditionally-patching-the-source-code)
  * [Conditionally select your build system](https://docs.conan.io/2//tutorial/creating_packages/build_packages.html.md#conditionally-select-your-build-system)
* [Package files: the package() method](https://docs.conan.io/2//tutorial/creating_packages/package_method.html.md)
  * [Using CMake install step in the package() method](https://docs.conan.io/2//tutorial/creating_packages/package_method.html.md#using-cmake-install-step-in-the-package-method)
  * [Use conan.tools.files.copy() in the package() method and packaging licenses](https://docs.conan.io/2//tutorial/creating_packages/package_method.html.md#use-conan-tools-files-copy-in-the-package-method-and-packaging-licenses)
  * [Managing symlinks in the package() method](https://docs.conan.io/2//tutorial/creating_packages/package_method.html.md#managing-symlinks-in-the-package-method)
* [Define information for consumers: the package_info() method](https://docs.conan.io/2//tutorial/creating_packages/define_package_information.html.md)
  * [Setting information in the package_info() method](https://docs.conan.io/2//tutorial/creating_packages/define_package_information.html.md#setting-information-in-the-package-info-method)
  * [Define information for consumers depending on settings or options](https://docs.conan.io/2//tutorial/creating_packages/define_package_information.html.md#define-information-for-consumers-depending-on-settings-or-options)
  * [Properties model: setting information for specific generators](https://docs.conan.io/2//tutorial/creating_packages/define_package_information.html.md#properties-model-setting-information-for-specific-generators)
  * [Propagating environment or configuration information to consumers](https://docs.conan.io/2//tutorial/creating_packages/define_package_information.html.md#propagating-environment-or-configuration-information-to-consumers)
  * [Define components for Conan packages that provide multiple libraries](https://docs.conan.io/2//tutorial/creating_packages/define_package_information.html.md#define-components-for-conan-packages-that-provide-multiple-libraries)
* [Testing Conan packages](https://docs.conan.io/2//tutorial/creating_packages/test_conan_packages.html.md)
* [Other types of packages](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages.html.md)
  * [Header-only packages](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/header_only_packages.html.md)
  * [Package prebuilt binaries](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html.md)
  * [Tool requires packages](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/tool_requires_packages.html.md)

#### NOTE
The Conan 2 Essentials training course is available for free at the JFrog Academy,
which covers the same topics as this documentation but in a more interactive way.
You can access it [here](https://academy.jfrog.com/path/conan-cc-package-manager?utm_source=Conan+Docs).
