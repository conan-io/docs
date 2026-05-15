# List classes

### *class* PackagesList

A collection of recipes, revisions and packages.

#### split()

Returns a list of PackageList, split one per reference.
This can be useful to parallelize things like upload, parallelizing per-reference

#### only_recipes() → None

Filter out all the packages and package revisions, keep only the recipes and
recipe revisions in self._data.

#### add_ref(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference)) → None

Adds a new RecipeReference to a package list

#### add_pref(pref: PkgReference, pkg_info: dict = None) → None

Add a PkgReference to an already existing RecipeReference inside a package list

#### items() → Iterable[Tuple[[RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference), Dict[PkgReference, Dict]]]

Iterate over the contents of the package list.

Yields tuples containing a recipe reference and a dictionary of its
associated package references content.

Returns:
: An iterable of tuples where:
  <br/>
  - The first element is a `RecipeReference` (representing the recipe revision).
  - The second element is a dictionary mapping a `PkgReference` to a nested dictionary of
    its specific attributes (e.g., settings, options).

Warning:
: **Missing Revisions Behavior:**
  This method filters out results that lack revision information.
  <br/>
  - It will ONLY yield items if they contain at least a **recipe revision**.
  - The nested package dictionary will be empty unless it contains a **package revision**.
  <br/>
  **When to use serialize instead:**
  If you perform a general search that does not fetch revisions (e.g., running
  `conan list *`), this method will yield nothing because no artifact references
  are created. In these cases, use the `serialize()` method to access the results.
  <br/>
  To successfully use `items()`, your query must explicitly request revisions
  (e.g., running `conan list pkg/version#*:*#*`).

#### recipe_dict(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference))

Gives read/write access to the dictionary containing a specific RecipeReference
information.

#### package_dict(pref: PkgReference)

Gives read/write access to the dictionary containing a specific PkgReference
information

#### serialize()

Serialize the instance to a dictionary.

#### *static* deserialize(data)

Loads the data from a serialized dictionary.

### *class* MultiPackagesList

A collection of PackagesList by remote name.

#### serialize()

Serialize object to a dictionary.

#### *static* load(file)

Create an instance of the class from a serialized JSON file path pointed by `file`.

#### *static* load_graph(graphfile, graph_recipes=None, graph_binaries=None, context=None)

Create an instance of the class from a graph file path, which is
the json format returned by a few commands
like `conan graph info` or `conan create/install.`

* **Parameters:**
  * **graphfile** (*str*) – Path to the graph file
  * **graph_recipes** (*list* *[**str* *]*) – List for kinds of recipes to return.
    For example `"cache"` will return only recipes in the local cache,
    `"download"` will return only recipes that have been downloaded,
    and passing `"*"` will return all recipes.
  * **graph_binaries** (*list* *[**str* *]*) – List for kinds of binaries to return.
    For example `"cache"` will return only binaries in the local cache,
    `"download"` will return only binaries that have been downloaded,
    `"build"` will return only binaries that are built,
    `"missing"` will return only binaries that are missing,
    `"invalid"` will return only binaries that are invalid,
    and passing `"*"` will return all binaries.
  * **context** (*str*) – Context to filter the graph,
    can be `"host"`, `"build"`, `"host-only"` or `"build-only"`

### *class* ListPattern(expression, rrev='latest', package_id=None, prev='latest', only_recipe=False)

Object holding a pattern that matches recipes, revisions and packages.

* **Parameters:**
  * **expression** – The pattern to match, e.g. `"name/*:*"`
  * **rrev** – The recipe revision to match, defaults to `"latest"`,
    can also be `"!latest"` or `"~latest"` to match all but the latest revision,
    a pattern like `"1234*"` to match a specific revision,
    or a specific revision like `"1234"`.
  * **package_id** – The package ID to match, defaults to `None`, which matches all package IDs.
  * **prev** – The package revision to match, defaults to `"latest"`,
    can also be `"!latest"` or `"~latest"` to match all but the latest revision,
    a pattern like `"1234*"` to match a specific revision,
    or a specific revision like `"1234"`.
  * **only_recipe** – If `True`, only the recipe part of the expression is parsed,
    ignoring `package_id` and `prev`. This is useful for commands that
    only operate on recipes, like `conan search`.
