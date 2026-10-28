<a id="conanfile-reference"></a>

# conanfile.py

The `conanfile.py` is the recipe file of a package, responsible for defining how to build it and consume it.

> ```python
> from conan import ConanFile

> class HelloConan(ConanFile):
>     ...
> ```

#### IMPORTANT
*conanfile.py* recipes use a variety of attributes and methods to operate. In order to avoid
collisions and conflicts, follow these rules:

- Public attributes and methods, like `build()`, `self.package_folder`, are reserved for Conan.
  Don’t use public members for custom fields or methods in the recipes.
- Use “protected” access for your own members, like `self._my_data` or `def _my_helper(self):`.
  Conan only reserves “protected” members starting with `_conan`.

Contents:

* [Attributes](https://docs.conan.io/2//reference/conanfile/attributes.html.md)
  * [Package reference](https://docs.conan.io/2//reference/conanfile/attributes.html.md#package-reference)
  * [Metadata](https://docs.conan.io/2//reference/conanfile/attributes.html.md#metadata)
  * [Requirements](https://docs.conan.io/2//reference/conanfile/attributes.html.md#requirements)
  * [Sources](https://docs.conan.io/2//reference/conanfile/attributes.html.md#sources)
  * [Binary model](https://docs.conan.io/2//reference/conanfile/attributes.html.md#binary-model)
  * [Build](https://docs.conan.io/2//reference/conanfile/attributes.html.md#build)
  * [Folders and layout](https://docs.conan.io/2//reference/conanfile/attributes.html.md#folders-and-layout)
  * [Layout](https://docs.conan.io/2//reference/conanfile/attributes.html.md#layout)
  * [Package information for consumers](https://docs.conan.io/2//reference/conanfile/attributes.html.md#package-information-for-consumers)
  * [Other](https://docs.conan.io/2//reference/conanfile/attributes.html.md#other)
* [Methods](https://docs.conan.io/2//reference/conanfile/methods.html.md)
* [Running and output](https://docs.conan.io/2//reference/conanfile/running_and_output.html.md)
  * [Output text from recipes](https://docs.conan.io/2//reference/conanfile/running_and_output.html.md#output-text-from-recipes)
  * [Running commands](https://docs.conan.io/2//reference/conanfile/running_and_output.html.md#running-commands)
