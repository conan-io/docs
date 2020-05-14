
conan copy
==========

.. code-block:: bash

   $ conan copy [-h] [--package PACKAGE] [--all] [--force]
                reference user_channel

Copies conan recipes and packages to another user/channel. Useful to promote
packages (e.g. from "beta" to "stable"). Also for moving packages from one
user to another.

.. code-block:: bash

    positional arguments:
      reference             package recipe referencee.g.,
                            MyPackage/1.2@user/channel
      user_channel          Destination user/channele.g., lasote/testing

    optional arguments:
      -h, --help            show this help message and exit
      --package PACKAGE, -p PACKAGE
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
