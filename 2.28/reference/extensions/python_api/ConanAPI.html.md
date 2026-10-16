<a id="reference-python-api-conan-api"></a>

# Conan API Reference

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

### *class* ConanAPI(cache_folder=None)

This is the main object to interact with the Conan API. It provides all the subapis to work with
recipes, packages, remotes, etc., which are exposed as attributes of this class, and should
not be created directly.

* **Parameters:**
  **cache_folder** – Conan cache/home folder. It will have less priority than the
  `"home_folder"` defined in a Workspace.

#### config *: [ConfigAPI](https://docs.conan.io/2//reference/extensions/python_api/ConfigAPI.html.md#conan.api.subapi.config.ConfigAPI)*

Used to interact with the local Conan configuration

#### remotes *: [RemotesAPI](https://docs.conan.io/2//reference/extensions/python_api/RemotesAPI.html.md#conan.api.subapi.remotes.RemotesAPI)*

Used to interact with remotes

#### command *: [CommandAPI](https://docs.conan.io/2//reference/extensions/python_api/CommandAPI.html.md#conan.api.subapi.command.CommandAPI)*

Used to call other commands

#### list *: [ListAPI](https://docs.conan.io/2//reference/extensions/python_api/ListAPI.html.md#conan.api.subapi.list.ListAPI)*

Used to get latest refs and list refs of recipes and packages

#### profiles *: [ProfilesAPI](https://docs.conan.io/2//reference/extensions/python_api/ProfilesAPI.html.md#conan.api.subapi.profiles.ProfilesAPI)*

Used to process and load Conan profiles

#### install *: [InstallAPI](https://docs.conan.io/2//reference/extensions/python_api/InstallAPI.html.md#conan.api.subapi.install.InstallAPI)*

Used to install binaries, sources, deploy packages and more

#### export *: [ExportAPI](https://docs.conan.io/2//reference/extensions/python_api/ExportAPI.html.md#conan.api.subapi.export.ExportAPI)*

Used to export recipes and pre-compiled package binaries to the Conan cache

#### upload *: [UploadAPI](https://docs.conan.io/2//reference/extensions/python_api/UploadAPI.html.md#conan.api.subapi.upload.UploadAPI)*

Used to upload recipes and packages to remotes

#### download *: [DownloadAPI](https://docs.conan.io/2//reference/extensions/python_api/DownloadAPI.html.md#conan.api.subapi.download.DownloadAPI)*

Used to download recipes and packages from remotes

#### cache *: [CacheAPI](https://docs.conan.io/2//reference/extensions/python_api/CacheAPI.html.md#conan.api.subapi.cache.CacheAPI)*

Used to interact wit the packages storage cache

#### lockfile *: [LockfileAPI](https://docs.conan.io/2//reference/extensions/python_api/LockfileAPI.html.md#conan.api.subapi.lockfile.LockfileAPI)*

Used to read and manage lockfile files

#### local *: [LocalAPI](https://docs.conan.io/2//reference/extensions/python_api/LocalAPI.html.md#conan.api.subapi.local.LocalAPI)*

Local flow helpers for developer “source”, “build”, “editable” commands

#### audit *: [AuditAPI](https://docs.conan.io/2//reference/extensions/python_api/AuditAPI.html.md#conan.api.subapi.audit.AuditAPI)*

Used to check vulnerabilities of dependencies

#### workspace *: WorkspaceAPI*

Used to manage workspaces

#### *property* home_folder *: str*

Where the Conan user home is located. Read only.
Can be modified by the `CONAN_HOME` environment variable or by the
`.conanrc` file in the current directory or any parent directory
when Conan is called.

#### reinit()

Reinitialize the Conan API. This is useful when the configuration changes.

#### SEE ALSO
- [Creating Conan custom commands](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#reference-commands-custom-commands)
