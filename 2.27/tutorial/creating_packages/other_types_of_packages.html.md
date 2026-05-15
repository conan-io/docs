# Other types of packages

In the previous sections, we saw how to create a new recipe for a classic C++ library but
there are other types of packages apart from libraries.

In this section, we will review how to create a recipe for *header-only* libraries, how
to package already *built libraries*, and how to create recipes for *tool requires*
and *applications*.

# Table of contents

* [Header-only packages](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/header_only_packages.html.md)
  * [Header-only library with tests](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/header_only_packages.html.md#header-only-library-with-tests)
* [Package prebuilt binaries](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html.md)
  * [Locally building binaries](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html.md#locally-building-binaries)
  * [Packaging already pre-built binaries](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html.md#packaging-already-pre-built-binaries)
  * [Downloading and Packaging Pre-built Binaries](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html.md#downloading-and-packaging-pre-built-binaries)
* [Tool requires packages](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/tool_requires_packages.html.md)
  * [A simple tool require recipe](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/tool_requires_packages.html.md#a-simple-tool-require-recipe)
  * [Removing settings in package_id()](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/tool_requires_packages.html.md#removing-settings-in-package-id)
