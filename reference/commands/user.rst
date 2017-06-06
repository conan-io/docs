conan user
==========

.. code-block:: bash

	$ conan user [-h] [-p PASSWORD] [--remote REMOTE] [-c] [name]

Update your cached user name (and auth token) to avoid it being requested later, e.g. while you're uploading a package.
You can have more than one user (one per remote). Changing the user, or introducing the password is only necessary to upload
packages to a remote.

.. code-block:: bash

	positional arguments:
	  name                  Username you want to use. If no name is provided it
	                        will show the current user.

	optional arguments:
	  -h, --help            show this help message and exit
	  -p PASSWORD, --password PASSWORD
	                        User password. Use double quotes if password with
	                        spacing, and escape quotes if existing
	  --remote REMOTE, -r REMOTE
	                        look in the specified remote server
	  -c, --clean           Remove user and tokens for all remotes



**Examples**:

- List my user for each remote:

.. code-block:: bash

	$ conan user


- Change **conan.io** remote user to **foo**:

.. code-block:: bash

	$ conan user foo -r conan.io

- Change **conan.io** remote user to **foo**, authenticating against the remote and storing the
  user and authentication token locally, so a later upload won't require entering credentials:

.. code-block:: bash

	$ conan user foo -r conan.io -p mypassword

- Clean all local users and tokens

.. code-block:: bash

    $ conan user --clean


.. note::

	The password is not stored in the client computer at any moment. Conan uses `JWT <https://en.wikipedia.org/wiki/JSON_Web_Token>`: conan
	gets a token (expirable by the server) checking the password against the remote credentials.
	If the password is correct, an authentication token will be obtained, and that token is the
	information cached locally. For any subsequent interaction with the remotes, the conan client will only use that JWT token.

