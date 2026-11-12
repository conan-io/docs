
.. _conan_alias:

conan alias
===========

.. code-block:: bash

    $ conan alias [-h] reference target

Creates and exports an 'alias package recipe'. An "alias" package is a
symbolic name (reference) for another package (target). When some package
depends on an alias, the target one will be retrieved and used instead, so the
alias reference, the symbolic name, does not appear in the final dependency
graph.

.. code-block:: text

    positional arguments:
      reference   Alias reference, e.g., mylib/1.X@user/channel
      target      Target reference, e.g., mylib/1.12@user/channel

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
