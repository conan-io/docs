# Remotes API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* RemotesAPI(conan_api, api_helpers)

The `RemotesAPI` manages the definition of remotes, contained in the “remotes.json” file
in the Conan home, supporting addition, removal, update, rename, enable, disable of remotes.
These operations do not contact the servers or check their existence at all. If they are not
available, they will fail later when used.

The `user_xxx` methods perform authentication related tasks, and some of them will contact
the servers to perform such authentication

#### list(pattern=None, only_enabled=True)

Obtain a list of [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) objects matching the pattern.

* **Parameters:**
  * **pattern** – `None`, single `str` or list of `str`. If it is `None`,
    all remotes will be returned (equivalent to `pattern="*"`).
  * **only_enabled** – boolean, by default return only enabled remotes
* **Returns:**
  A list of [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) objects

#### disable(pattern)

Disable all remotes matching `pattern`

* **Parameters:**
  **pattern** – single `str` or list of `str`. If the pattern is an exact name without
  wildcards like “\*” and no remote is found matching that exact name, it will raise an error.
* **Returns:**
  the list of disabled [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) objects  (even if they
  were already disabled)

#### enable(pattern)

Enable all remotes matching `pattern`.

* **Parameters:**
  **pattern** – single `str` or list of `str`. If the pattern is an exact name without
  wildcards like “\*” and no remote is found matching that exact name, it will raise an error.
* **Returns:**
  the list of enabled [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) objects (even if they
  were already enabled)

#### get(remote_name)

Obtain a [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) object

* **Parameters:**
  **remote_name** – the exact name of the remote to be returned
* **Returns:**
  the [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) object, or raise an Exception if the
  remote does not exist.

#### add(remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote), force=False, index=None)

Add a new [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) object to the existing ones

* **Parameters:**
  * **remote** – a [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) object to be added
  * **force** – do not fail if the remote already exist (but default it fails)
  * **index** – if not defined, the new remote will be last one. Pass an integer to insert
    the remote in that position instead of the last one

#### remove(pattern)

Remove the remotes matching the `pattern`

* **Parameters:**
  **pattern** – single `str` or list of `str`. If the pattern is an exact name without
  wildcards like “\*” and no remote is found matching that exact name, it will raise an error.
* **Returns:**
  The list of removed [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) objects

#### update(remote_name: str, url=None, secure=None, disabled=None, index=None, allowed_packages=None, recipes_only=None)

Update an existing remote

* **Parameters:**
  * **remote_name** – The name of the remote to update, must exist
  * **url** – optional url to update, if not defined it will not be updated
  * **secure** – optional ssl secure connection to update
  * **disabled** – optional disabled state
  * **index** – optional integer to change the order of the remote
  * **allowed_packages** – optional list of packages allowed from this remote
  * **recipes_only** – optional boolean to only allow recipe downloads from this remote,
    never package binaries

#### rename(remote_name: str, new_name: str)

Change the name of an existing remote

* **Parameters:**
  * **remote_name** – The previous existing name
  * **new_name** – The new name

#### user_login(remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote), username: str, password: str)

Perform user authentication against the given remote with the provided username and password

* **Parameters:**
  * **remote** – a [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) object
  * **username** – the user login as `str`
  * **password** – password `str`

#### user_logout(remote: [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan.api.model.Remote))

Logout from the given [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote)

* **Parameters:**
  **remote** – The [Remote](https://docs.conan.io/2//reference/extensions/python_api/model/remote.html.md#conan-api-model-remote) object to logout
