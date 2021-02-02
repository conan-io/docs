
.. _conan_copy:

conan copy
==========

.. code-block:: bash

    $ conan copy [-h] [-p PACKAGE] [--all] [--force] reference user_channel

Copies conan recipes and packages to another user/channel. Useful to promote
packages (e.g. from "beta" to "stable") or transfer them from one user to
another.

.. code-block:: text

    positional arguments:
      reference             package reference. e.g., MyPackage/1.2@user/channel
      user_channel          Destination user/channel. e.g., lasote/testing

    optional arguments:
      -h, --help            show this help message and exit
      -p PACKAGE, --package PACKAGE
                            copy specified package ID
      --all                 Copy all packages from the specified package recipe
      --force               Override destination packages and the package recipe


**Examples**

- Promote a package to **stable** from **beta**:

  .. code-block:: bash

      $ conan copy OpenSSL/1.0.2i@lasote/beta lasote/stable


- Change a package's username:

  .. code-block:: bash

      $ conan copy OpenSSL/1.0.2i@lasote/beta foo/beta
