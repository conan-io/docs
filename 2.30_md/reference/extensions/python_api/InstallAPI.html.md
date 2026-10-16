# Install API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* InstallAPI(conan_api, helpers)

This is the InstallAPI.

It provides methods to install binaries, sources,
prepare the consumer folder with generators and deploy, etc., all of them
based on an already resolved dependency graph.

#### install_binaries(deps_graph, remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)] = None, return_install_error=False)

Install binaries of a dependency graph.

This is the equivalent to the `conan install` command, but working with an already
resolved dependency graph, usually obtained from the corresponding `GraphAPI` methods.

It will download the available packages from the given remotes,
and then build the ones that were marked for build from source.

System requirements will be installed as well, taking into account the
`tools.system.package_manager:mode` conf to determine whether to install, check or skip them.

* **Parameters:**
  * **deps_graph** – Dependency graph to install packages for
  * **remotes** – List of remotes to fetch packages from if necessary.
  * **return_install_error** – If `True`, do not raise an exception, but return it

#### install_system_requires(graph, only_info=False)

Install only the system requirements of a dependency graph.

This is a subset of `install_binaries` which only deals with system requirements
of an already resolved dependency graph,
usually obtained from the corresponding `GraphAPI` methods.

The `tools.system.package_manager:mode` conf will be taken into account to
determine whether to install, check or skip system requirements.

* **Parameters:**
  * **graph** – Dependency graph to install system requirements for
  * **only_info** – If `True`, only reporting and checking of whether the system requirements are installed is performed.

#### install_sources(graph, remotes: List[[Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote)])

Download sources in the given dependency graph.

If the `tools.build:download_source` conf is `True`, sources will be downloaded for
every package in the graph, otherwise only the packages marked for build from source will
have their sources downloaded.

`tools.build:download_source=True` is useful when users want to inspect the source code
of all dependencies, even the ones that are not built from source.

After this method, the `conanfile.source_folder` on each node of the dependency graph
for which the sources have been downloaded will be set to the folder where sources have been downloaded.

* **Parameters:**
  * **remotes** – List of remotes where the `exports_sources` of the packages might be located
  * **graph** – Dependency graph to download sources from

#### install_consumer(deps_graph, generators: List[str] = None, source_folder=None, output_folder=None, deploy=False, deploy_package: List[str] = None, deploy_folder=None, envs_generation=None)

Prepare the folder of the root consumer of a dependency graph after installation
of the dependencies.

This ensures that the requested generators are created in the consumer folder,
and also handles deployment if requested.

* **Parameters:**
  * **deps_graph** – Dependency graph whose root is the consumer we want to prepare
  * **generators** – List of generators to be used in addition to the ones defined in the root conanfile, if any
  * **source_folder** – Source folder of the consumer
  * **output_folder** – Output folder of the consumer
  * **deploy** – Deployer or list of deployers to be used for deployment
  * **deploy_package** – Only deploy the packages matching these patterns (`None` or empty for all)
  * **deploy_folder** – Folder where to deploy, by default the build folder
  * **envs_generation** – Anything other than `None` will activate the generation of virtual environment files for the root conanfile

#### deploy(graph, deployer: List[str], deploy_package: List[str] = None, deploy_folder=None) → None

Run the given deployer in the dependency graph.

No checks are performed in the graph, it is assumed to be already resolved
and in a valid state to be deployed from.

* **Parameters:**
  * **graph** – The dependency graph to deploy
  * **deployer** – List of deployers to be used
  * **deploy_package** – Only deploy the packages matching these patterns (`None` or empty for all)
  * **deploy_folder** – Folder where to deploy, by default the build folder
