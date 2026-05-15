# List API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* ListAPI(conan_api, api_helpers)

Get references from the recipes and packages in the cache or a remote

#### latest_recipe_revision(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference), remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote) = None)

For a given recipe reference, return the latest revision of the recipe in the remote,
or in the local cache if no remote is specified, or `None` if the recipe does not exist.

#### recipe_revisions(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference), remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote) = None)

For a given recipe reference, return all the revisions of the recipe in the remote,
or in the local cache if no remote is specified

#### select(pattern: [ListPattern](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.ListPattern), package_query=None, remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote) = None, lru=None, profile=None) → [PackagesList](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList)

For a given pattern, return a list of recipes and packages matching the provided filters.

* **Parameters:**
  * **pattern** ([*ListPattern*](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.ListPattern)) – Search criteria
  * **package_query** (*str*) – When returning packages, expression of the form
    `"os=Windows AND (arch=x86 OR compiler=gcc)"` to filter packages by.
    If `None`, all packages will be returned if requested.
  * **remote** ([*Remote*](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)) – Remote to search in,
    if `None`, it will search in the local cache.
  * **lru** (*str*) – If set, it will filter the results to only include
    packages/binaries that have been used in the last ‘lru’ time.
    It can be a string like `"2d"` (2 days) or `"3h"` (3 hours).
  * **profile** (*Profile*) – Profile to filter the packages by settings and options.

#### explain_missing_binaries(ref, conaninfo, remotes)

(Experimental) Explain why a binary is missing in the cache

#### find_remotes(package_list, remotes)

(Experimental) Find the remotes where the current package lists can be found
