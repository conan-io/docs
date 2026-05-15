# Export API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* ExportAPI(conan_api, helpers)

This API provides methods to export artifacts, both recipes and pre-compiled package
binaries from user folders to the Conan cache, as Conan recipes and Conan package binaries

#### export(path, name: str = None, version: str = None, user: str = None, channel: str = None, lockfile=None, remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)] = None) → Tuple[[RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference), ConanFile]

Exports a `conanfile.py` recipe, together with its associated files to the Conan cache.
A “recipe-revision” will be computed and assigned.

* **Parameters:**
  * **path** – Path to the conanfile to be exported
  * **name** – Optional package name. Typically not necessary as it is defined by the recipe
    attribute or dynamically with the `set_name()` method.
    If it is defined in recipe and as an argument, but they don’t match, an error will be raised.
  * **version** – Optional version. It can be defined in the recipe with the version
    attribute or dynamically with the ‘set_version()’ method.
    If it is defined in recipe and as an argument, but they don’t match, an error will be raised.
  * **user** – Optional user. Can be defined by recipe attribute.
    If it is defined in recipe and as an argument, but they don’t match, an error will be raised.
  * **channel** – Optional channel. Can be defined by recipe attribute.
    If it is defined in recipe and as an argument, but they don’t match, an error will be raised.
  * **lockfile** – Optional, only relevant if the recipe has ‘python-requires’ to be locked
  * **remotes** – Optional, only relevant to resolve ‘python-requires’ in remotes
* **Returns:**
  A tuple of the exported RecipeReference and a ConanFile object

#### export_pkg_graph(path, ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference), profile_host, profile_build, remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)], lockfile=None, is_build_require=False, skip_binaries=False, output_folder=None)

Computes a dependency graph for a given configuration, for an already existing (previously
exported) recipe in the Conan cache. This method computes the full dependency graph, using
the profiles, lockfile and remotes information as any other install/graph/create command.
This is necessary in order to compute the “package_id” of the binary being exported
into the Conan cache.
The resulting dependency graph can be passed to `export_pkg()` method

* **Parameters:**
  * **path** – Path to the conanfile.py in the user folder
  * **ref** – full RecipeReference, including recipe-revision
  * **profile_host** – Profile for the host context
  * **profile_build** – Profile for the build context
  * **lockfile** – Optional lockfile
  * **remotes** – List of Remotes
  * **is_build_require** – In case a package intended to be used as a tool-requires
  * **skip_binaries** – 
  * **output_folder** – The folder containing output files, like potential environment scripts
* **Returns:**
  A Graph object that can be passed to `export_pkg()` method

#### export_pkg(graph, output_folder=None) → None

Executes the `package()` method of the exported recipe in order to copy the artifacts
from user folder to the Conan cache package folder

* **Parameters:**
  * **graph** – A Graph object
  * **output_folder** – Optional folder where generated files like environment scripts
    of dependencies have been installed
