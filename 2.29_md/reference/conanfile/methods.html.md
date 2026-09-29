<a id="reference-conanfile-methods"></a>

# Methods

What follows is a list of methods that you can define in your recipes to customize the package creation & consumption processes:

- [build()](https://docs.conan.io/2//reference/conanfile/methods/build.html.md): Contains the build instructions to build a package from source
- [build_id()](https://docs.conan.io/2//reference/conanfile/methods/build_id.html.md): Allows reusing the same build to create different package binaries
- [build_requirements()](https://docs.conan.io/2//reference/conanfile/methods/build_requirements.html.md): Defines `tool_requires` and `test_requires`
- [compatibility()](https://docs.conan.io/2//reference/conanfile/methods/compatibility.html.md): Defines binary compatibility at the recipe level
- [configure()](https://docs.conan.io/2//reference/conanfile/methods/configure.html.md): Allows configuring settings and options while computing dependencies
- [config_options()](https://docs.conan.io/2//reference/conanfile/methods/config_options.html.md): Configure options while computing dependency graph
- [deploy()](https://docs.conan.io/2//reference/conanfile/methods/deploy.html.md): Deploys (copy from package to user folder) the desired artifacts
- [export()](https://docs.conan.io/2//reference/conanfile/methods/export.html.md): Copies files that are part of the recipe
- [export_sources()](https://docs.conan.io/2//reference/conanfile/methods/export_sources.html.md): Copies files that are part of the recipe sources
- [finalize()](https://docs.conan.io/2//reference/conanfile/methods/finalize.html.md): Customizes the package for using it in the running machine without affecting the original package
- [generate()](https://docs.conan.io/2//reference/conanfile/methods/generate.html.md): Generates the files that are necessary for building the package
- [init()](https://docs.conan.io/2//reference/conanfile/methods/init.html.md): Special initialization of recipe when extending from `python_requires`
- [layout()](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md): Defines the relative project layout, source folders, build folders, etc.
- [package()](https://docs.conan.io/2//reference/conanfile/methods/package.html.md): Copies files from build folder to the package folder.
- [package_id()](https://docs.conan.io/2//reference/conanfile/methods/package_id.html.md): Defines special logic for computing the binary `package_id` identifier
- [package_info()](https://docs.conan.io/2//reference/conanfile/methods/package_info.html.md): Provide information for consumers of this package about libraries, folders, etc.
- [requirements()](https://docs.conan.io/2//reference/conanfile/methods/requirements.html.md): Define the dependencies of the package
- [set_name()](https://docs.conan.io/2//reference/conanfile/methods/set_name.html.md): Dynamically define the name of a package
- [set_version()](https://docs.conan.io/2//reference/conanfile/methods/set_version.html.md): Dynamically define the version of a package.
- [source()](https://docs.conan.io/2//reference/conanfile/methods/source.html.md): Contains the commands to obtain the source code used to build
- [system_requirements()](https://docs.conan.io/2//reference/conanfile/methods/system_requirements.html.md): Call system package managers like Apt to install system packages
- [test()](https://docs.conan.io/2//reference/conanfile/methods/test.html.md): Run some simple package test (exclusive of `test_package`)
- [validate()](https://docs.conan.io/2//reference/conanfile/methods/validate.html.md): Define if the current package is invalid (cannot work) with the current configuration.
- [validate_build()](https://docs.conan.io/2//reference/conanfile/methods/validate_build.html.md): Define if the current package cannot be created with the current configuration.
