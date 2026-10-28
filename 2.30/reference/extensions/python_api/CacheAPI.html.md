# Cache API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* CacheAPI(conan_api, api_helpers)

This CacheAPI is used to interact with the packages storage cache

Note that the Conan packages cache is exclusively **read-only** for user code. Only Conan
can write or modify the folders and files in the Conan cache. In general, when a method
returns a folder, it is mostly for debugging purposes and read-only access, but never to
modify the contents of the cache.

#### export_path(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference))

Returns the path of the recipe conanfile and exported files in the Conan cache

This folder is exclusively for **read-only** access, typically for debugging purposes,
it is completely forbidden to modify any of its contents.

* **Parameters:**
  **ref** – RecipeReference. If it includes recipe revision, that exact revision will be
  returned, if it doesn’t include recipe revision, it will return the latest revision one.
* **Returns:**
  path to the folder, as a string
* **Raises:**
  ConanExcepcion if the folder doesn’t exist

#### recipe_metadata_path(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference))

Returns the path of the recipe metadata files in the Conan cache

Exceptionally, adding or modifying the files within this folder is allowed, as
the metadata files are not taken into account into the computation of the recipe hash
(recipe revision).

* **Parameters:**
  **ref** – RecipeReference. If it includes recipe revision, that exact revision will be
  returned, if it doesn’t include recipe revision, it will return the latest revision one.
* **Returns:**
  path to the folder, as a string
* **Raises:**
  ConanExcepcion if the folder doesn’t exist

#### export_source_path(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference))

Returns the path of the exported sources in the Conan cache

Note that the exported sources only exist in the cache when the package has been created
locally or built from source.

This folder is exclusively for **read-only** access, typically for debugging purposes,
it is completely forbidden to modify any of its contents.

* **Parameters:**
  **ref** – RecipeReference. If it includes recipe revision, that exact revision will be
  returned, if it doesn’t include recipe revision, it will return the latest revision one.
* **Returns:**
  path to the folder, as a string
* **Raises:**
  ConanExcepcion if the folder doesn’t exist

#### source_path(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference))

Returns the path of the temporary source folder in the Conan cache

Note that the source folder only exist in the cache when the package has been created
locally or built from source.

This folder is exclusively for **read-only** access, typically for debugging purposes,
it is completely forbidden to modify any of its contents.

* **Parameters:**
  **ref** – RecipeReference. If it includes recipe revision, that exact revision will be
  returned, if it doesn’t include recipe revision, it will return the latest revision one.
* **Returns:**
  path to the folder, as a string
* **Raises:**
  ConanExcepcion if the folder doesn’t exist

#### build_path(pref: PkgReference)

Returns the path of the temporary build folder in the Conan cache

Note that the build folder only exist in the cache when the package has been created
locally or built from source.

This folder is exclusively for **read-only** access, typically for debugging purposes,
it is completely forbidden to modify any of its contents.

* **Parameters:**
  **pref** – PkgReference. If it includes recipe revision, that exact revision will be
  returned, if it doesn’t include recipe revision, it will return the latest revision one.
  Exactly same behavior for the package revision.
* **Returns:**
  path to the folder, as a string
* **Raises:**
  ConanExcepcion if the folder doesn’t exist

#### package_metadata_path(pref: PkgReference)

Returns the path of the package metadata folder in the Conan cache

> Exceptionally, adding or modifying the files within this folder is allowed, as
> the metadata files are not taken into account into the computation of the package hash
> (package revision).
* **Parameters:**
  **pref** – PkgReference. If it includes recipe revision, that exact revision will be
  returned, if it doesn’t include recipe revision, it will return the latest revision one.
  Exactly same behavior for the package revision.
* **Returns:**
  path to the folder, as a string
* **Raises:**
  ConanExcepcion if the folder doesn’t exist

#### package_path(pref: PkgReference)

Returns the path of the package folder in the Conan cache

This folder is exclusively for **read-only** access, typically for debugging purposes,
it is completely forbidden to modify any of its contents.

* **Parameters:**
  **pref** – PkgReference. If it includes recipe revision, that exact revision will be
  returned, if it doesn’t include recipe revision, it will return the latest revision one.
  Exactly same behavior for the package revision.
* **Returns:**
  path to the folder, as a string
* **Raises:**
  ConanExcepcion if the folder doesn’t exist

#### check_integrity(package_list, return_pkg_list=False)

Check if the recipes and packages are corrupted

* **Parameters:**
  * **package_list** – PackagesList to check
  * **return_pkg_list** – If True, return a PackagesList with corrupted artifacts
* **Returns:**
  PackagesList with corrupted artifacts if return_pkg_list is True
* **Raises:**
  ConanExcepcion if there are corrupted artifacts and return_pkg_list is False

#### sign(package_list)

Sign packages with the package signing plugin

#### verify(package_list)

Verify packages with the package signing plugin

#### clean(package_list, source=True, build=True, download=True, temp=True, backup_sources=False) → None

Remove non critical folders from the cache, like source, build and download (.tgz store)
folders.

* **Parameters:**
  * **package_list** – the package lists that should be cleaned
  * **source** – boolean, remove the “source” folder if True
  * **build** – boolean, remove the “build” folder if True
  * **download** – boolean, remove the “download (.tgz)” folder if True
  * **temp** – boolean, remove the temporary folders
  * **backup_sources** – boolean, remove the “source” folder if True
* **Returns:**

#### save(package_list: [PackagesList](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList), path, no_source=False) → None

Create a compressed archive with recipes and packages from the Conan cache that
can be later restored in another cache.

Do not manipulate the contents of the resulting archive, as it also contains metadata,
and modifying the contents would be equivalent to modify the Conan package cache, which
is forbidden.

* **Parameters:**
  * **package_list** – PackagesList containing the recipes and packages to add
    to the compressed archive
  * **path** – The archive file to generate. Based on the extension of the file, different
    compression formats can be used (.tgz, .txz and .tzst, the latter only for Python>=3.14).
  * **no_source** – If True, the source folders in the cache will not be added to the archive.
* **Returns:**

#### restore(path) → [PackagesList](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList)

Restore a compressed archive with recipes and packages previously saved from another
Conan cache into the currently active Conan cache.

* **Parameters:**
  **path** – The archive file to restore. Based on the extension of the file, different
  compression formats can be used (.tgz, .txz and .tzst, the latter only for Python>=3.14).
* **Returns:**
  a PackageLists with the recipes and packages that have been restored to the cache

#### get_backup_sources(package_list=None, exclude=True, only_upload=True)

Get list of backup source files currently present in the cache,
either all of them if no argument, or filtered by those belonging to the references
in the package_list

* **Parameters:**
  * **package_list** – a PackagesList object to filter backup files from (The files should
    have been downloaded form any of the references in the package_list)
  * **exclude** – if True, exclude the sources that come from URLs present the
    core.sources:exclude_urls global conf
  * **only_upload** – if True, only return the files for packages that are set to be uploaded
* **Returns:**
  A list of files that need to be uploaded
