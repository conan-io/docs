# Graph API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* GraphAPI(conan_api, helpers)

#### load_root_test_conanfile(path, tested_reference, profile_host, profile_build, update=None, remotes=None, lockfile=None, tested_python_requires=None)

Create and initialize a root node from a test_package/conanfile.py consumer

* **Parameters:**
  * **tested_python_requires** – the reference of the `python_require` to be tested
  * **lockfile** – Might be good to lock python-requires, build-requires
  * **path** – The full path to the test_package/conanfile.py being used
  * **tested_reference** – The full RecipeReference of the tested package
  * **profile_host** – 
  * **profile_build** – 
  * **update** – 
  * **remotes** – 
* **Returns:**
  a graph Node, recipe=RECIPE_CONSUMER

#### load_graph(root_node, profile_host, profile_build, lockfile=None, remotes=None, update=None, check_update=False)

Compute the dependency graph, starting from a root package, evaluation the graph with
the provided configuration in profile_build, and profile_host. The resulting graph is a
graph of recipes, but packages are not computed yet (package_ids) will be empty in the
result. The result might have errors, like version or configuration conflicts, but it is
still possible to inspect it. Only trying to install such graph will fail

* **Parameters:**
  * **root_node** – the starting point, an already initialized Node structure, as
    returned by the “load_root_node” api
  * **profile_host** – The host profile
  * **profile_build** – The build profile
  * **lockfile** – A valid lockfile (None by default, means no locked)
  * **remotes** – list of remotes we want to check
  * **update** – (False by default), if Conan should look for newer versions or
    revisions for already existing recipes in the Conan cache
  * **check_update** – For “graph info” command, check if there are recipe updates

#### analyze_binaries(graph, build_mode=None, remotes=None, update=None, lockfile=None, build_modes_test=None, tested_graph=None)

Given a dependency graph, will compute the package_ids of all recipes in the graph, and
evaluate if they should be built from sources, downloaded from a remote server, of if the
packages are already in the local Conan cache

* **Parameters:**
  * **lockfile** – 
  * **graph** – a Conan dependency graph, as returned by “load_graph()”
  * **build_mode** – TODO: Discuss if this should be a BuildMode object or list of arguments
  * **remotes** – list of remotes
  * **update** – (`False` by default), if Conan should look for newer versions or
    revisions for already existing recipes in the Conan cache. It also accepts an array of
    reference patterns to limit the update to those references if any of the items match.
    Eg. `False`, `None` or `[]` *means no update*,
    `True` or `["*"]` *means update all*,
    and `["pkgA/*", "pkgB/1.0@user/channel"]` *means to update only specific packages*.
  * **build_modes_test** – the –build-test argument
  * **tested_graph** – In case of a “test_package”, the graph being tested

#### *static* find_first_missing_binary(graph, missing=None)

(Experimental) Given a dependency graph, will return the first node with a
missing binary package
