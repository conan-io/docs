# Download API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* DownloadAPI(conan_api, api_helpers)

This API is used to download recipes and packages from a remote server.

#### recipe(ref: [RecipeReference](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference), remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote), metadata: List[str] | None = None)

Download the recipe specified in the ref from the remote.
If the recipe is already in the cache it will be skipped,
but the specified metadata will be downloaded.

#### package(pref: PkgReference, remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote), metadata: List[str] | None = None)

Download the package specified in the pref from the remote.
The recipe for this package binary must already exist in the cache.
If the package is already in the cache it will be skipped,
but the specified metadata will be downloaded.

#### download_full(package_list: [PackagesList](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList), remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote), metadata: List[str] | None = None)

Download the recipes and packages specified in the `package_list` from the remote,
parallelized based on `core.download:parallel`
