# Report API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* ReportAPI(conan_api, helpers)

Used to compute the differences (the “diff”) between two versions or revisions, for
both the recipe and source code.

#### diff(old_reference, new_reference, remotes, old_path=None, new_path=None, cwd=None)

Compare two recipes and return the differences.

* **Parameters:**
  * **old_reference** – The reference of the old recipe.
  * **new_reference** – The reference of the new recipe.
  * **remotes** – List of remotes to search for the recipes.
  * **old_path** – Optional path to the old recipe’s conanfile.py.
  * **new_path** – Optional path to the new recipe’s conanfile.py.
  * **cwd** – Current working directory, used to resolve paths.
* **Returns:**
  A dictionary with the differences between the two recipes.
