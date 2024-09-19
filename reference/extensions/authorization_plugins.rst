.. _reference_extensions_authorization_plugin:

Authorization plugins
---------------------

Regarding authorization, we have two plugins: one focused on remote Conan servers authorization, ``auth_remote.py``, and another
focused on authorization for source file servers, ``auth_source.py``.

The idea behind these plugins is to create custom integrations with each user's secrets managers.

Auth remote plugin
+++++++++++++++++++
This first plugin is a Python script that receives a ``remote`` object and two optional parameters: ``user`` and
``password``. The output should be a tuple of the username and password that we want to use for that remote,
or ``None`` if no credentials are specified for that remote and we want Conan to follow the normal login flow.

This plugin is located at the path ``<CONAN_HOME>/extensions/plugins/auth_remote.py`` and must be manually created with the name
``auth_remote.py``, containing a function named ``auth_remote_plugin(remote, user=None, password=None)``.

Here we can see an example of a plugin implementation.

.. code-block:: python

    def auth_remote_plugin(remote, user=None, password=None):
        if remote.url == "https://www.my-custom-remote.com":
            return "admin", "password"


Auth source plugin
+++++++++++++++++++
This one is a Python script that receives an ``url`` as a parameter and outputs a dictionary with the credentials or
access token. It can also return None to indicate that Conan should proceed with its normal login flow.

This plugin is located at the path ``extensions/plugins/auth_source.py`` and must be manually created with the name
``auth_source.py``, containing a function like ``auth_source_plugin(url)``.

Here we can see an example of a plugin implementation.

.. code-block:: python

    def auth_source_plugin(url):
        if url == "https://www.my-custom-login-sources.com":
            return {'user': 'my-user', 'password': 'my-password'}
        elif url == "https://www.my-custom-token-sources.com":
            return {'token': 'my-secure-token'}


