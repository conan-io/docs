.. _conan_alias:

conan alias
============

.. code-block:: bash

    $ conan alias [-h] reference target

Uploads a recipe and binary packages to a remote. If you use the --force
variable, it won't check the package date. It will override the remote with
the local package. If you use a pattern instead of a conan recipe reference
you can use the -c or --confirm option to upload all the matching recipes. If
you use the --retry option you can specify how many times should conan try to
upload the packages in case of failure. The default is 2. With --retry_wait
you can specify the seconds to wait between upload attempts. If no remote is
specified, the first configured remote (by default conan.io, use 'conan remote
list' to list the remotes) will be used.

.. code-block:: bash

    positional arguments:
      reference   Alias reference. e.j: mylib/1.X@user/channel
      target      Target reference. e.j: mylib/1.12@user/channel

    optional arguments:
      -h, --help  show this help message and exit

The command:

.. code-block:: bash

    $ conan alias Hello/0.X@user/testing Hello/0.1@user/testing

Creates and exports a package recipe for ``Hello/0.X@user/testing`` with the following content:

.. code-block:: python

    from conans import ConanFile

    class AliasConanfile(ConanFile):
        alias = "Hello/0.1@user/testing"

Such package recipe acts as a "proxy" for the aliased reference. Users depending on
``Hello/0.X@user/testing`` will actually use version ``Hello/0.1@user/testing``. The alias package
reference will not appear in the dependency graph at all. It is useful to define symbolic names, or
behaviors like "always depend on the latest minor", but defined upstream instead of being defined
downstream with ``version-ranges``.

The "alias" package should be uploaded to servers in the same way as regular package recipes, in
order to enable usage from servers.
