# Lockfile API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* LockfileAPI(conan_api)

#### *static* get_lockfile(lockfile=None, conanfile_path=None, cwd=None, partial=False, overrides=None) → Lockfile

obtain a lockfile, following this logic:

If lockfile is explicitly defined, it would be either absolute or relative to cwd and
the lockfile file must exist. If lockfile=”” (empty string) the default “conan.lock”
lockfile will not be automatically used even if it is present.

If lockfile is not defined, it will still look for a default conan.lock:

> - if conanfile_path is defined, it will be besides it
> - if conanfile_path is not defined, the default conan.lock should be in cwd
> - if the default conan.lock cannot be found, it is not an error
* **Parameters:**
  * **partial** – If the obtained lockfile will allow partial resolving
  * **cwd** – the current working dir, if None, os.getcwd() will be used
  * **conanfile_path** – The full path to the conanfile, if existing
  * **lockfile** – the name of the lockfile file
  * **overrides** – Dictionary of overrides {overriden: [new_ref1, new_ref2]}

#### check_lockfile_config(lockfile)

Verify that installed configurations are aligned with lockfile config_requires.
