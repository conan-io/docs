# Local API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* LocalAPI(conan_api, helpers)

This `LocalAPI` contains several helpers related to the local development flow, i.e.,
locally calling `source()` or `build()` methods, or adding and removing editable packages

#### *static* get_conanfile_path(path, cwd, py)

Obtain the full path to a conanfile file, either .txt or .py, from the current
working directory.

If both `conanfile.py` and a `conanfile.txt` are present, it will raise an error.

* **Parameters:**
  * **path** – Relative path to look for the file. Can be a folder or a file.
  * **cwd** – The current working directory.
  * **py** – If True, a conanfile.py must exist, a .txt is not valid in this case

#### editable_add(path, name=None, version=None, user=None, channel=None, cwd=None, output_folder=None, remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)] = None) → [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference)

Add the conanfile in the given path as an editable package

Note that for automation over editables it might be recommended to use the `WorkspacesAPI`
instead of this API.

* **Parameters:**
  * **path** – Relative path to look for it. Can be a folder or a file.
  * **name** – The name of the package. If not defined, it is taken from conanfile
  * **version** – The version of the package. If not defined, it is taken from conanfile
  * **user** – The user of the package. If not defined, it is taken from conanfile
  * **channel** – The channel of the package. If not defined, it is taken from conanfile
  * **cwd** – The current working directory
  * **output_folder** – The output folder. If not defined, the recipe layout will be used.
  * **remotes** – The remotes to resolve possible `python-requires` for this recipe if needed.
* **Returns:**
  RecipeReference of the added package

#### editable_remove(path=None, requires=None, cwd=None)

Remove an editable package from the given path

Note that for automation over editables it might be recommended to use the `WorkspacesAPI`
instead of this API.

* **Parameters:**
  * **path** – Relative path to look for it. Can be a folder or a file.
  * **requires** – Remove these requirements from editables (instead of by path)
  * **cwd** – The current working directory
* **Returns:**
  RecipeReference of the added package

#### source(path, name=None, version=None, user=None, channel=None, remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)] = None)

Calls the `source()` method of the current (user folder) `conanfile.py`

This method does not require computing a dependency graph, because the `source()`
method is assumed to be invariant with respect to settings, options and dependencies.

* **Parameters:**
  * **path** – Relative path to look for the conanfile. Can be a folder or a file.
  * **name** – The name of the package. If not defined, it is taken from conanfile
  * **version** – The version of the package. If not defined, it is taken from conanfile
  * **user** – The user of the package. If not defined, it is taken from conanfile
  * **channel** – The channel of the package. If not defined, it is taken from conanfile
  * **remotes** – The remotes to resolve possible `python-requires` for this recipe if needed.

#### build(conanfile) → None

Calls the `build()` method of the current (user folder) `conanfile.py`

This method does require computing a dependency graph, because the `build()` method
needs all dependencies and transitive dependencies. Then, the `conanfile` argument
must be the one obtaind from a full dependency graph install operation, including both
the graph comptutation and the binary installation.

* **Parameters:**
  **conanfile** – `Conanfile` object representing the “root” node in the dependency graph,
  corresponding to a `conanfile.py` in the user folder, containing the `build()` method to
  be called. This `conanfile` object must have all of its dependencies computed and
  installed in the current Conan package cache to work.

#### *static* test(conanfile) → None

Calls the `test()` method of the current (user folder) `test_package/conanfile.py`

This method does require computing a dependency graph, because the `test()` method
needs all dependencies and transitive dependencies. Then, the `conanfile` argument
must be the one obtaind from a full dependency graph install operation, including both
the graph comptutation and the binary installation.

Typically called after a `build()` one.

* **Parameters:**
  **conanfile** – `Conanfile` object representing the “root” node in the dependency graph,
  corresponding to a conanfile.py in the user “test_package” folder, containing the `test()`
  method to be called. This `conanfile` object must have all of its dependencies computed
  and installed in the current Conan package cache to work.
