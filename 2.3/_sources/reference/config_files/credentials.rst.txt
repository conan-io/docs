.. _reference_config_files_credentials:

credentials.json
================

.. include:: ../../common/experimental_warning.inc


Conan can authenticate against its Conan remote servers with the following:

- Interactive command line, when some server launches an unauthorized error, the Conan client will ask for user/password interactively and retry.
- With the ``conan remote login`` command, authentication can be done with argument passing, or interactively.
- With the environment variables ``CONAN_LOGIN_USERNAME`` for all remotes (``CONAN_LOGIN_USERNAME_{REMOTE}`` for an individual remote) and ``CONAN_PASSWORD`` (``CONAN_PASSWORD_{REMOTE}`` for an individual remote), Conan will not request interactively in the command line when necessary, but will take the values from the environment variables as if they were provided by the user.
- With a ``credentials.json`` file put in the Conan cache.

This section describes the usage of ``credentials.json`` file.


This file has the following format, in which every ``credentials`` entry should have a ``remote`` name, matching the name defined in ``conan remote list``.
Then, the ``user`` and ``password`` fields.

.. code-block:: json

    {
        "credentials": [
            {
                "remote": "default", 
                "user": "admin", 
                "password": "password"
            }
        ]
    }

Conan will be able to extract the credentials from this file automatically when necessary and requested by the server.

.. note::

    Conan does not pre-emptively use the credentials to force a login automatically in every remote defined at every Conan command.
    By default Conan uses the previously stored tokens or anonymous usage, until an explicit ``conan remote login`` command is done, 
    or until a remote server launches an authentication error. When that happens, authentication against that server will be done,
    using the ``credentials.json`` file, the environment variables or the user interactive inputs.

The priority of credentials origins is as follows:

- If the ``credentials.json`` file exist, it has higher priority, if an entry for the remote exists,
  it will be used. If it doesn't work, it will be an error.
- If an entry in the ``credentials.json`` for that remote does not exist, it will look for defined environment variables
- If environment variables don't exist, it will request interactively the credentials. If ``core:non_interactive=True``, it will error.

The ``credentials.json`` file is jinja-rendered with injected ``platform`` and ``os`` imports, so it allows to use jinja syntax. 
For example it could do something like the following to get the credentials from environment variables:


.. code-block:: jinja
    
    {% set myuser = os.getenv('myuser') %}
    {% set mytk = os.getenv('mytoken') %}
    {
        "credentials": [
            {
                "remote": "myremote", 
                "user": "{{myuser}}"
                "password": "{{mytk}}"
            }
        ]
    }
