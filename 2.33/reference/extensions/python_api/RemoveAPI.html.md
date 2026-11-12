# Remove API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* RemoveAPI(conan_api, api_helpers)

This API is used to remove artifacts from either remotes or the Conan cache.
It can either remove specific package references, or whole recipe references with all
its associated packages

#### recipe(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference), remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote) | None = None)

Removes the specified recipe reference alongside all its associated packages.

If `remote` is specified, the recipe will be removed from the remote,
otherwise they will be removed from the local cache.

* **Parameters:**
  * **ref** – Recipe reference to remove
  * **remote** – Optional remote to remove references from

#### recipes(refs: List[[RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference)], remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote) | None = None)

Removes the specified recipe reference alongside all its associated packages.

If `remote` is specified, the packages will be removed from the remote,
otherwise they will be removed from the local cache.

Warning:
: This method is not atomic wit respect to each of the given references

* **Parameters:**
  * **refs** – List of recipe references to delete, must contain recipe revisions
  * **remote** – Optional remote to remove references from

#### package(pref: PkgReference, remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote) | None = None)

Removes the specified package reference.

If `remote` is specified, the packages will be removed from the remote,
otherwise they will be removed from the local cache.

* **Parameters:**
  * **pref** – Package reference to remove
  * **remote** – Optional remote to remove references from

#### packages(prefs: List[PkgReference], remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote) | None = None)

Removes all the specified package references.

If `remote` is specified, the packages will be removed from the remote,
otherwise they will be removed from the local cache.

Warning:
: This method is not atomic when performed in the local cache
  with respect to each of the given references,
  nor are remotes guaranteed to implement this call atomically either.

* **Parameters:**
  * **prefs** – List of package references to delete, must contain package revisions
  * **remote** – Optional remote to remove references from
