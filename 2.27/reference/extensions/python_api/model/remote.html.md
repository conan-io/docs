# Remote model

<a id="conan-api-model-remote"></a>

### *class* Remote(name, url, verify_ssl=True, disabled=False, allowed_packages=None, remote_type=None, recipes_only=False)

The `Remote` class represents a remote registry of packages.

A Remote object can be constructed to be passed as an argument to
RemotesAPI methods. When possible, it is better to use Remote objects returned by the API,
but for the `RemotesAPI.add()` method, for which a new constructed object is necessary.
It is recommended to use named arguments like `Remote(..., verify_ssl=False)` in
the constructor.
:param name: The name of the remote.
:param url: The URL of the remote repository (or local folder for “local-recipes-index”).
:param verify_ssl: Enable SSL Certificate validation.
:param disabled: Disable the remote repository.
:param allowed_packages: List of patterns of allowed packages from this remote
:param remote_type: Type of the remote repository, use “local-recipes-index” or `None`
:param recipes_only: If True, binaries form this remote will be ignored and never used

#### invalidate_cache()

If external operations might have modified the remote since it was instantiated,
this method can be called to invalidate the cache.
Note that this is done automatically when the remote is used in any operation by Conan,
such as uploading packages, so this method is not usually needed when only interacting
with the Conan API
