<a id="reference-extensions"></a>

# Extensions

Conan can be extended in a few ways, with custom user code:

- `python_requires` allow to put common recipe code in a recipe package that can be
  reused by other recipes by declaring a `python_requires = "mypythoncode/version"`
- You can create your own custom Conan commands to solve self-needs thanks to Python and
  Conan public API powers altogether.
- It’s also possible to make your own custom Conan generators in case you are using build
  systems that are not supported by the built-in Conan tools. Those can be used from
  `python_requires` or installed globally.
- `hooks` are “pre” and “post” recipe methods (like `pre_build()` and `post_build()`)
  extensions that can be used to complement recipes
  with orthogonal functionality, like quality checks, binary analyzing, logging, etc.
- Binary compatibility `compatibility.py` extension allows to write custom rules for
  defining custom binary compatibility across different settings and options
- The `cmd_wrapper.py` extension allows to inject arbitrary command wrappers to any
  `self.run()` recipe command invocation, which can be useful to inject wrappers as
  parallelization tools
- The package signing extension allows to sign and verify packages at upload and install time
  respectively
- Deployers, a mechanism to facilitate copying files from one folder, usually the Conan cache, to user folders

#### NOTE
Besides the built-in Conan extensions listed in this document, there is a repository
that contains extensions for Conan, such as custom commands and deployers, useful for
different purposes like artifactory tasks, Conan Center Index, etc.

You can find more information on how to use those extensions in [the GitHub repository](https://github.com/conan-io/conan-extensions).

Contents:

* [Python requires](https://docs.conan.io/2//reference/extensions/python_requires.html.md)
  * [Introduction](https://docs.conan.io/2//reference/extensions/python_requires.html.md#introduction)
  * [Extending base classes](https://docs.conan.io/2//reference/extensions/python_requires.html.md#extending-base-classes)
  * [Reusing files](https://docs.conan.io/2//reference/extensions/python_requires.html.md#reusing-files)
  * [Testing python-requires](https://docs.conan.io/2//reference/extensions/python_requires.html.md#testing-python-requires)
  * [Effect in package_id](https://docs.conan.io/2//reference/extensions/python_requires.html.md#effect-in-package-id)
  * [Resolution of python_requires](https://docs.conan.io/2//reference/extensions/python_requires.html.md#resolution-of-python-requires)
* [Custom commands](https://docs.conan.io/2//reference/extensions/custom_commands.html.md)
  * [Location and naming](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#location-and-naming)
  * [Decorators](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#decorators)
  * [Argument definition and parsing](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#argument-definition-and-parsing)
  * [Formatters](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#formatters)
  * [Commands parameters](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#commands-parameters)
* [Custom Conan generators](https://docs.conan.io/2//reference/extensions/custom_generators.html.md)
  * [Custom generators as python_requires](https://docs.conan.io/2//reference/extensions/custom_generators.html.md#custom-generators-as-python-requires)
  * [Using global custom generators](https://docs.conan.io/2//reference/extensions/custom_generators.html.md#using-global-custom-generators)
  * [Generators from tool_requires](https://docs.conan.io/2//reference/extensions/custom_generators.html.md#generators-from-tool-requires)
* [Python API](https://docs.conan.io/2//reference/extensions/python_api.html.md)
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
  * [Models](https://docs.conan.io/2//reference/extensions/python_api/model.html.md)
* [Deployers](https://docs.conan.io/2//reference/extensions/deployers.html.md)
  * [Built-in deployers](https://docs.conan.io/2//reference/extensions/deployers.html.md#built-in-deployers)
  * [Custom deployers](https://docs.conan.io/2//reference/extensions/deployers.html.md#custom-deployers)
* [Hooks](https://docs.conan.io/2//reference/extensions/hooks.html.md)
  * [Hook structure](https://docs.conan.io/2//reference/extensions/hooks.html.md#hook-structure)
  * [Importing from a module](https://docs.conan.io/2//reference/extensions/hooks.html.md#importing-from-a-module)
  * [Hook interface](https://docs.conan.io/2//reference/extensions/hooks.html.md#hook-interface)
  * [Storage, activation and sharing](https://docs.conan.io/2//reference/extensions/hooks.html.md#storage-activation-and-sharing)
  * [Official Hooks](https://docs.conan.io/2//reference/extensions/hooks.html.md#official-hooks)
* [Binary compatibility](https://docs.conan.io/2//reference/extensions/binary_compatibility.html.md)
* [Profile plugin](https://docs.conan.io/2//reference/extensions/profile_plugin.html.md)
* [Authorization plugins](https://docs.conan.io/2//reference/extensions/authorization_plugins.html.md)
  * [Auth remote plugin](https://docs.conan.io/2//reference/extensions/authorization_plugins.html.md#auth-remote-plugin)
  * [Auth source plugin](https://docs.conan.io/2//reference/extensions/authorization_plugins.html.md#auth-source-plugin)
* [Command wrapper](https://docs.conan.io/2//reference/extensions/command_wrapper.html.md)
* [Package signing](https://docs.conan.io/2//reference/extensions/package_signing.html.md)
  * [Configuration](https://docs.conan.io/2//reference/extensions/package_signing.html.md#configuration)
  * [Implementation](https://docs.conan.io/2//reference/extensions/package_signing.html.md#implementation)
  * [Commands](https://docs.conan.io/2//reference/extensions/package_signing.html.md#commands)
  * [Plugin implementation examples](https://docs.conan.io/2//reference/extensions/package_signing.html.md#plugin-implementation-examples)
* [Compiler flags mapper plugin](https://docs.conan.io/2//reference/extensions/compiler_flags_plugin.html.md)
