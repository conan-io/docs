<a id="reference-python-api"></a>

# Python API

#### WARNING
The full Python API is **experimental**.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The Python API is a set of Python classes that allow you to interact with Conan programmatically.
It’s designed to be used as part of the custom commands extension point,
or in Python scripts or applications, providing a more flexible and powerful way to work with Conan than the command line interface.

It is organized in submodules, each one providing a specific set of functionalities.

Note that only the **documented** public members of these classes are guaranteed to be stable,
and the rest of the members are considered private and can change without notice.

* [Conan API Reference](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md)
* [Audit API](https://docs.conan.io/2//reference/extensions/python_api/AuditAPI.html.md)
* [Cache API](https://docs.conan.io/2//reference/extensions/python_api/CacheAPI.html.md)
* [Command API](https://docs.conan.io/2//reference/extensions/python_api/CommandAPI.html.md)
* [Config API](https://docs.conan.io/2//reference/extensions/python_api/ConfigAPI.html.md)
* [Download API](https://docs.conan.io/2//reference/extensions/python_api/DownloadAPI.html.md)
* [Export API](https://docs.conan.io/2//reference/extensions/python_api/ExportAPI.html.md)
* [Graph API](https://docs.conan.io/2//reference/extensions/python_api/GraphAPI.html.md)
* [Install API](https://docs.conan.io/2//reference/extensions/python_api/InstallAPI.html.md)
* [List API](https://docs.conan.io/2//reference/extensions/python_api/ListAPI.html.md)
* [Local API](https://docs.conan.io/2//reference/extensions/python_api/LocalAPI.html.md)
* [Lockfile API](https://docs.conan.io/2//reference/extensions/python_api/LockfileAPI.html.md)
* [New API](https://docs.conan.io/2//reference/extensions/python_api/NewAPI.html.md)
* [Profiles API](https://docs.conan.io/2//reference/extensions/python_api/ProfilesAPI.html.md)
* [Remotes API](https://docs.conan.io/2//reference/extensions/python_api/RemotesAPI.html.md)
* [Remove API](https://docs.conan.io/2//reference/extensions/python_api/RemoveAPI.html.md)
* [Report API](https://docs.conan.io/2//reference/extensions/python_api/ReportAPI.html.md)
* [Upload API](https://docs.conan.io/2//reference/extensions/python_api/UploadAPI.html.md)

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

There are also some model classes that represent the data structures used in the API.
Note that as with the API, only the **documented** public members are guaranteed to be stable,
and the rest of the members are considered private and can change without notice.

* [Models](https://docs.conan.io/2//reference/extensions/python_api/model.html.md)
  * [Remote model](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md)
    * [`Remote`](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)
  * [List classes](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md)
    * [`PackagesList`](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.PackagesList)
    * [`MultiPackagesList`](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.MultiPackagesList)
    * [`ListPattern`](https://docs.conan.io/2//reference/extensions/python_api/model/list.html.md#conan.api.model.ListPattern)
  * [Reference models](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md)
    * [`RecipeReference`](https://docs.conan.io/2//reference/extensions/python_api/model/references.html.md#conan.api.model.RecipeReference)
