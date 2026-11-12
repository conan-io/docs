.. _reference_extensions_authorization_plugin:

Authorization plugins
=====================

.. include:: ../../common/experimental_warning.inc

Regarding authorization, we have two plugins: one focused on remote  :ref:`Conan servers <setting_up_conan_remotes>`
authorization, ``auth_remote.py``, and another focused on authorization for source file servers, ``auth_source.py``.

The idea behind these plugins is to create custom integrations with each user's secrets managers.

Auth remote plugin
+++++++++++++++++++
This first plugin is a Python script that receives a ``remote`` object and an optional parameter: ``user``. If the user
is provided, the expected output is the credentials that use that username. The output should be a tuple of the
username that we want to use for that remote, or ``None`` if no credentials are specified for that remote and we want
Conan to follow the normal login flow.

This plugin is located at the path ``<CONAN_HOME>/extensions/plugins/auth_remote.py`` and must be manually created with
the name ``auth_remote.py``, containing a function named ``auth_remote_plugin(remote, user=None, **kwargs)``.

The order for retrieving credentials is as follows:

* First, an attempt is made to obtain the credentials from the ``auth_remote_plugin``.
* If it doesn't exist or returns ``None``, the next step is to check ``credentials.json``.
* After that, the environment variables are searched.
* Finally, the credentials are obtained through an interactive prompt.

Here we can see an example of a plugin implementation.

.. code-block:: python

    def auth_remote_plugin(remote, user=None, **kwargs):
        if remote.url.startswith("https://artifactory.my-org/"):
            return "admin", "password"


Auth source plugin
+++++++++++++++++++
This one is a Python script that receives an ``url`` as a parameter and outputs a dictionary with the credentials or
access token. It can also return ``None`` to indicate that Conan should proceed with its normal login flow.

This plugin is located at the path ``<CONAN_HOME>/extensions/plugins/auth_source.py`` and must be manually created with the name
``auth_source.py``, containing a function named ``auth_source_plugin(url, **kwargs)``.

The order for retrieving the credentials is as follows:

* First, an attempt is made to obtain the credentials from the ``auth_source_plugin``.
* If it doesn't exist or returns ``None``, an attempt is made to retrieve them from ``source_credentials.json``.

Here we can see an example of a plugin implementation.

.. code-block:: python

    def auth_source_plugin(url, **kwargs):
        if url.startswith("https://my-sources-user-password.my-org/"):
            return {'user': 'my-user', 'password': 'my-password'}
        elif url.startswith("https://my-private-token-sources.my-org/"):
            return {'token': 'my-secure-token'}


.. note::

    These plugins can be shared and installed using ``conan config install`` or ``conan config install-pkg``

    **Important:** Ensure that your plugins and configurations do **not** contain hardcoded secrets or sensitive data.
    Instead, passwords should be retrieved using your implementation with a secret manager.
