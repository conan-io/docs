
.. _conan_user:

conan user
==========

.. code-block:: bash

    $ conan user [-h] [-c] [-p [PASSWORD]] [-r REMOTE] [-j JSON] [-s] [name]

Authenticates against a remote with user/pass, caching the auth token.

Useful to avoid the user and password being requested later. e.g. while
you're uploading a package.  You can have one user for each remote.
Changing the user, or introducing the password is only necessary to
perform changes in remote packages.

.. code-block:: text

    positional arguments:
      name                  Username you want to use. If no name is provided it
                            will show the current user

    optional arguments:
      -h, --help            show this help message and exit
      -c, --clean           Remove user and tokens for all remotes
      -p [PASSWORD], --password [PASSWORD]
                            User password. Use double quotes if password with
                            spacing, and escape quotes if existing. If empty, the
                            password is requested interactively (not exposed)
      -r REMOTE, --remote REMOTE
                            Use the specified remote server
      -j JSON, --json JSON  json file path where the user list will be written to
      -s, --skip-auth       Skips the authentication with the server if there are
                            local stored credentials. It doesn't check if the
                            current credentials are valid or not


**Examples**:

- List my user for each remote:

  .. code-block:: bash

      $ conan user
      Current user of remote 'conan-center' set to: 'danimtb' [Authenticated]
      Current user of remote 'bincrafters' set to: 'None' (anonymous)
      Current user of remote 'upload_repo' set to: 'danimtb' [Authenticated]
      Current user of remote 'conan-community' set to: 'danimtb' [Authenticated]
      Current user of remote 'the_remote' set to: 'None' (anonymous)

- Change **bar** remote user to **foo**:

  .. code-block:: bash

      $ conan user foo -r bar
      Changed user of remote 'bar' from 'None' (anonymous) to 'foo'

- Change **bar** remote user to **foo**, authenticating against the remote and storing the
  user and authentication token locally, so a later upload won't require entering credentials:

  .. code-block:: bash

      $ conan user foo -r bar -p mypassword


- Authenticate against the remote only if we don't have credentials stored locally. It will not check
  if the credentials are valid or not:

  .. code-block:: bash

      $ conan user foo -r bar -p mypassword --skip-auth

- Clean all local users and tokens:

  .. code-block:: bash

      $ conan user --clean

- Change **bar** remote user to **foo**, **asking user password** to authenticate against the
  remote and storing the user and authentication token locally, so a later upload won't require entering credentials:

  .. code-block:: text

      $ conan user foo -r bar -p
      Please enter a password for "foo" account:
      Change 'bar' user from None (anonymous) to foo

.. note::

    The password is not stored in the client computer at any moment. Conan uses
    `JWT <https://en.wikipedia.org/wiki/JSON_Web_Token>`_, so it gets a token (expirable by the
    server) checking the password against the remote credentials. If the password is correct, an
    authentication token will be obtained, and that token is the information cached locally. For
    any subsequent interaction with the remotes, the Conan client will only use that JWT token.

Using environment variables
---------------------------

The :ref:`CONAN_LOGIN_USERNAME <env_vars_conan_login_username>` and :ref:`CONAN_PASSWORD <env_vars_conan_password>` environment variables allow
defining the user and the password in the environment.
If those environment variables are defined, the user input will no be necessary whenever the user or
password are requested. Values for user and password will be automatically taken from the
environment variables without any interactive input.

This applies also to the ``conan user`` command, if you want to force the authentication in some
scripts, without requiring to put the password in plain text, the following can be done:


.. code-block:: bash    

      $ conan user --clean  # remove previous auth tokens
      $ export CONAN_PASSWORD=mypassword
      $ conan user mysyusername -p -r=myremote 
      Please enter a password for "mysusername" account: Got password '******' from environment
      Changed user of remote 'myremote' from 'None' (anonymous) to 'mysusername'
      $ conan upload zlib* -r=myremote --all --confirm

In this example, :command:`conan user mysyusername -p -r=myremote` will interactively request a password
if ``CONAN_PASSWORD`` is not defined.

The environment variable :ref:`env_vars_non_interactive` (or ``general.non_interactive`` in *conan.conf*)
can be defined to guarantee that an error will be raise if user input is required, to avoid stalls in CI
builds.

Note that defining ``CONAN_LOGIN_USERNAME`` and/or ``CONAN_PASSWORD`` do not perform in any case an
authentication request against the server. Only when the server request credentials 
(or a explicit :command:`conan user -p` is done), they will be used as an alternative source rather than interactive user input. This means that for servers like Artifactory that allow enabling *"Hide Existence of Unauthorized Resource"* modes, it will be necessary to explicitly call :command:`conan user -p` before downloading or uploading anything from the server, otherwise, Artifactory will return 404 errors instead of requesting authentication.
