# Upload API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* UploadAPI(conan_api, api_helpers)

This API is used to upload recipes and packages to a remote server.

#### check_upstream(package_list: [PackagesList](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList), remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote), enabled_remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)], force=False)

Checks `remote` for the existence of the recipes and packages in `package_list`.
An `upload` key will be added to each entry, with the value `True` for the items
that are not present in the remote and need to be uploaded, and `False` otherwise.

If the recipe has an upload policy of `skip`, its packages will be discarded from the
upload list, and only the recipe will be considered.

* **Parameters:**
  * **package_list** – A `PackagesList` object with the recipes and packages to check.
  * **remote** – Remote to check.
  * **enabled_remotes** – List of enabled remotes. This is used to possibly load
    python_requires from the listed recipes if necessary.
  * **force** – If `True`, the items already present in the remote will also be
    marked to be uploaded, adding a `force_upload` key with the value `True` to
    their entries.

#### prepare(package_list: [PackagesList](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList), enabled_remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)], metadata: List[str] = None)

Compress the recipes and packages and fill the `package_list` entries
with the complete information of the files to upload. It doesn’t perform the upload
nor checks upstream to see if the recipe is still there

* **Parameters:**
  * **package_list** – A PackagesList object with the recipes and packages to upload.
  * **enabled_remotes** – A list of remotes that are enabled in the client.
    Recipe sources will attempt to be fetched from these remotes.
  * **metadata** – A list of patterns of metadata that should be uploaded.
    Default `None` means all metadata will be uploaded together with the package artifacts.
    If metadata contains an empty string (`""`),
    it means that no metadata files should be uploaded.

#### upload_full(package_list: [PackagesList](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList), remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote), enabled_remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)], check_integrity=False, force=False, metadata: List[str] = None, dry_run=False, is_prepared=False)

Does the whole process of uploading, including the possibility of parallelizing
per recipe based on the `core.upload:parallel` conf.

The steps that this method performs are:
: - if `check_integrity` is `True`, calls `conan_api.cache.check_integrity` to
    ensure the packages are not corrupted
  - checks the upload policy of the recipes
    : - (if it is `"skip"`, it will not upload the binaries, but will still upload
        the recipe)
  - checks which revisions already exist in the server so that it can skip the upload
  - prepares the artifacts to upload (compresses the conan_package.tgz)
  - executes the actual upload
  - uploads associated sources backups if any

* **Parameters:**
  * **package_list** – A PackagesList object with the recipes and packages to upload.
  * **remote** – The remote to upload the packages to.
  * **enabled_remotes** – A list of remotes that are enabled in the client.
    Recipe sources will attempt to be fetched from these remotes,
    and to possibly load python_requires from the listed recipes if necessary.
  * **check_integrity** – If `True`, it will check the integrity of the cache packages
    before uploading them. This is useful to ensure that the packages are not corrupted.
  * **force** – If `True`, it will force the upload of the recipes and packages,
    even if they already exist in the remote. Note that this might update the timestamps
  * **metadata** – A list of patterns of metadata that should be uploaded.
    Default `None` means all metadata will be uploaded together with the package artifacts.
    If metadata contains an empty string (`""`),
    it means that no metadata files should be uploaded.
  * **dry_run** – If `True`, it will not perform the actual upload,
    but will still prepare the artifacts and check the upstream.

#### upload_backup_sources(files: List) → None

Upload to the server the backup sources files, that have been typically gathered by
CacheAPI.get_backup_sources()

* **Parameters:**
  **files** – The list of files that must be uploaded
