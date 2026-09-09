<a id="reference-conanfile-methods-deploy"></a>

# deploy()

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `deploy()` method is intended to deploy (copy) artifacts from the current package.
It only executes at `conan install` time, when the `--deployer-package` argument is provided, otherwise `deploy()` is ignored.

Artifacts should be deployed to the `self.deploy_folder`, by default the current folder. A custom destination can be defined with `--deployer-folder`.
A basic `deploy()` method would copy all files from the package folder to the deploy folder:

```python
from conan import ConanFile
from conan.tools.files import copy

class Pkg(ConanFile):

    def deploy(self):
        copy(self, "*", src=self.package_folder, dst=self.deploy_folder)
```

Refer to the documentation of the [conan install command](https://docs.conan.io/2//reference/commands/install.html.md#reference-commands-install-generators-deployers) for more information.

If you need to run binaries from your build dependencies, the recommended approach is
to apply the env from a `VirtualBuildEnv`, such as:

```python
def deploy(self):
    venv = VirtualBuildEnv(self)
    with venv.vars().apply():
        self.run("mytool")
```

#### NOTE
**Best practices**

- Only “binary” package artifacts can be deployed, copying from the `self.package_folder`. It is recommended to copy only from the package folder, not other folders.
- The `deploy()` method is intended for final production deployments or the installation of binaries on the machine, as it extracts the files from the Conan cache. It is not intended for normal development operations, nor to build Conan packages against deployed binaries. The recommendation is to build against packages in the Conan cache.
- The `self.deploy_folder` should only be used from within the `deploy()` method.
