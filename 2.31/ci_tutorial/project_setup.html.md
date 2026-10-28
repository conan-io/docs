# Project setup

The code necessary for this tutorial is found in the `examples2` repo, clone it and
move to the folder:

```bash
$ git clone https://github.com/conan-io/examples2.git
$ cd examples2/ci/game
```

## Server repositories setup

We need 3 different repositories in the same server. Make sure to have an Artifactory running and available. You can download the free  [Artifactory CE](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes/artifactory/artifactory_ce_cpp.html.md#artifactory-ce-cpp) from the [downloads page](https://conan.io/downloads.html) and run it in your own computer, or you can use docker:

```bash
$ docker run --name artifactory -d -p 8081:8081 -p 8082:8082 releases-docker.jfrog.io/jfrog/artifactory-cpp-ce:7.63.12
# Can be stopped with "docker stop artifactory"
```

When you launch it, you can go to [http://localhost:8082/](http://localhost:8082/) to check it (user: “admin”, password: “password”).
If you have another available Artifactory, it can be used too if you can create new repositories there.

As a first step, log into the web UI and **create 3 different local repositories** called `develop`, `packages` and `products`.

Then according to the `project_setup.py` file, these are the necessary environment variables to configure the server. Please define `ARTIFACTORY_URL`, `ARTIFACTORY_USER` and/or `ARTIFACTORY_PASSWORD` if necessary to adapt to your setup:

```python
# TODO: This must be configured by users
SERVER_URL = os.environ.get("ARTIFACTORY_URL", "http://localhost:8081/artifactory/api/conan")
USER = os.environ.get("ARTIFACTORY_USER", "admin")
PASSWORD = os.environ.get("ARTIFACTORY_PASSWORD", "password")
```

## Initial dependency graph

#### WARNING
- The initialization of the project will remove the contents of the 3 `develop`, `products` and `packages` repositories in the server.
- The `examples2/ci/game` folder contains a `.conanrc` file that defines a local cache, so commands executed in this tutorial do not pollute or alter your main Conan cache.

```bash
$ python project_setup.py
```

This will do several tasks, clean the server repos, create initial `Debug` and `Release` binaries for the dependency graph and upload them to the `develop` repo, then clean the local cache. Note in this example we are using `Debug` and `Release` as our different configurations for convenience, but in real cases these would be different configurations such as Windows/X86_64, Linux/x86_64, Linux/armv8, etc., running
in different computers.

After the setup, it can be checked that the 3 remotes are defined, but only `develop` remote is enabled, and there are no packages in the local cache:

```bash
$ conan remote list
products: http://localhost:8081/artifactory/api/conan/products [Verify SSL: True, Enabled: False]
develop: http://localhost:8081/artifactory/api/conan/develop [Verify SSL: True, Enabled: True]
packages: http://localhost:8081/artifactory/api/conan/packages [Verify SSL: True, Enabled: False]

$ conan list *
Found 0 pkg/version recipes matching * in local cache
Local Cache
WARN: There are no matching recipe references
```

#### IMPORTANT
The order of the remotes is important. If the `products` repository is enabled, it will have higher priority than
the `develop` one, so if it contains new versions, they will be picked from there.

This dependency graph of packages in the `develop` repo is the starting point for our tutorial, assumed as a functional and stable “develop” state of the project that developers can `conan install` to work in any of the different packages.
