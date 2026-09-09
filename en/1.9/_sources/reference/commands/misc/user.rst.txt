
.. _conan_user:

conan user
==========

.. code-block:: bash

    $ conan user [-h] [-c] [-p [PASSWORD]] [-r REMOTE] [-j JSON] [name]

Authenticates against a remote with user/pass, caching the auth token. Useful
to avoid the user and password being requested later. e.g. while you're
uploading a package. You can have one user for each remote. Changing the user,
or introducing the password is only necessary to perform changes in remote
packages.

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
