
.. _conan_download:

conan download
==============

.. code-block:: bash

    $ conan download [-h] [-p PACKAGE] [-r REMOTE] [-re] reference

Downloads recipe and binaries to the local cache, without using settings.

It works specifying the recipe reference and package ID to be
installed. Not transitive, requirements of the specified reference will
NOT be retrieved. Useful together with 'conan copy' to automate the
promotion of packages to a different user/channel. Only if a reference
is specified, it will download all packages from the specified remote.
If no remote is specified, it will use the default remote.

.. code-block:: text

    positional arguments:
      reference             pkg/version@user/channel

    optional arguments:
      -h, --help            show this help message and exit
      -p PACKAGE, --package PACKAGE
                            Force install specified package ID (ignore
                            settings/options) [DEPRECATED: use full reference
                            instead]
      -r REMOTE, --remote REMOTE
                            look in the specified remote server
      -re, --recipe         Downloads only the recipe


**Examples**

- Download all **OpenSSL/1.0.2i@conan/stable** binary packages from the remote **foo**:

  .. code-block:: bash

      $ conan download OpenSSL/1.0.2i@conan/stable -r foo

- Download a single binary package of **OpenSSL/1.0.2i@conan/stable** from the remote **foo**:

  .. code-block:: bash

      $ conan download OpenSSL/1.0.2i@conan/stable:8018a4df6e7d2b4630a814fa40c81b85b9182d2 -r foo

- Download only the recipe of package **OpenSSL/1.0.2i@conan/stable** from the remote **foo**:

  .. code-block:: bash

      $ conan download OpenSSL/1.0.2i@conan/stable -r foo -re
