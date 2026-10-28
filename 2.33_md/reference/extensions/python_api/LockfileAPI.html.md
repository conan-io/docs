# Lockfile API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* LockfileAPI(conan_api)

Loads and saves Lockfiles from disk, modifies and manipulates them.

At the moment Lockfile objects are “opaque” objects, they are not intended to be used
independently, only to be retrieved from this API and passed as arguments to methods
of the API.

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

#### check_lockfile_config(lockfile: Lockfile)

Verify that installed configurations are aligned with lockfile config_requires.

* **Parameters:**
  **lockfile** – The lockfile to check, can be None

#### update_lockfile_export(lockfile, conanfile, ref, is_build_require=False) → Lockfile

Update the lockfile or create a new one with the information resulting from a
conan export operation, so the recently exported version and revision can be locked and
prioritized.

* **Parameters:**
  * **lockfile** – The lockfile to update. Can be None and a new lockfile will be created
  * **conanfile** – The exported conanfile
  * **ref** – The reference of the exported conanfile, including its recipe revision
  * **is_build_require** – If True, the exported conanfile is for a tool used as tool_requires
* **Returns:**
  The updated lockfile

#### *static* update_lockfile(lockfile, graph, lock_packages=False, clean=False) → Lockfile

Update the lockfile with information from the dependency graph

* **Parameters:**
  * **lockfile** – The lockfile to update. It can be None, and a new lockfile will be created.
  * **graph** – The dependency graph
  * **lock_packages** – Unused, do not use or define it.
  * **clean** – If true, completely clean the lockfile, computing a new lockfile from graph

#### *static* merge_lockfiles(lockfiles) → Lockfile

Merge multiple lockfiles into a single lockfile.

* **Parameters:**
  **lockfiles** – list of lockfiles to merge
* **Returns:**
  the merged lockfile

#### *static* add_lockfile(lockfile=None, requires=None, build_requires=None, python_requires=None, config_requires=None) → Lockfile

Add requires to a lockfile. If the lockfile doesn’t exist, it will be created

* **Parameters:**
  * **lockfile** – The lockfile to add to. Can be `None`.
  * **requires** – The list of requirements to add. Can be `None`.
  * **build_requires** – The list of build requirements to add. Can be `None`.
  * **python_requires** – The list of Python requirements to add. Can be `None`.
  * **config_requires** – The list of configuration requirements to add. Can be `None`.
* **Returns:**
  The lockfile with the added information.

#### *static* remove_lockfile(lockfile: Lockfile, requires=None, build_requires=None, python_requires=None, config_requires=None) → Lockfile

Remove entries from lockfile

* **Parameters:**
  * **lockfile** – The lockfile to remove entries. It will be mutated in place.
  * **requires** – The list of requires to remove
  * **build_requires** – The list of build requires to remove
  * **python_requires** – The list of python_requires to remove
  * **config_requires** – The list of config_requires to remove
* **Returns:**
  The modified lockfile

#### *static* save_lockfile(lockfile: Lockfile, lockfile_out, path=None)

Save lockfile to disk

* **Parameters:**
  * **lockfile** – The lockfile object to save. If None, nothing will be saved
  * **lockfile_out** – The output lockfile filename
  * **path** – The path of the output lockfile, if None, it will be cwd
