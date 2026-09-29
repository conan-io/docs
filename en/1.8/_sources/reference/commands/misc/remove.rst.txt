
.. _conan_remove:

conan remove
============

.. code-block:: bash

    $ conan remove [-h] [-b [BUILDS [BUILDS ...]]] [-f] [-o]
                   [-p [PACKAGES [PACKAGES ...]]] [-q QUERY] [-r REMOTE] [-s]
                   [-l]
                   [pattern_or_reference]

Removes packages or binaries matching pattern from local cache or remote. It
can also be used to remove temporary source or build folders in the local
conan cache. If no remote is specified, the removal will be done by default in
the local conan cache.

.. code-block:: text

    positional arguments:
      pattern_or_reference  Pattern or package recipe reference, e.g.,
                            'MyPackage/1.2@user/channel', 'boost/*'

    optional arguments:
      -h, --help            show this help message and exit
      -b [BUILDS [BUILDS ...]], --builds [BUILDS [BUILDS ...]]
                            By default, remove all the build folders or select
                            one, specifying the package ID
      -f, --force           Remove without requesting a confirmation
      -o, --outdated        Remove only outdated from recipe packages. This flag
                            can only be used with a reference
      -p [PACKAGES [PACKAGES ...]], --packages [PACKAGES [PACKAGES ...]]
                            Select package to remove specifying the package ID
      -q QUERY, --query QUERY
                            Packages query: 'os=Windows AND (arch=x86 OR
                            compiler=gcc)'. The 'pattern_or_reference' parameter
                            has to be a reference: MyPackage/1.2@user/channel
      -r REMOTE, --remote REMOTE
                            Will remove from the specified remote
      -s, --src             Remove source folders
      -l, --locks           Remove locks


The ``-q`` parameter can't be used along with ``-p`` nor ``-b`` parameters.

**Examples**:

- Remove from the local cache the binary packages (the package recipes will not be removed)
  from all the recipes matching ``OpenSSL/*`` pattern:

  .. code-block:: bash

      $ conan remove OpenSSL/* --packages

- Remove the temporary build folders from all the recipes matching ``OpenSSL/*`` pattern without
  requesting confirmation:

  .. code-block:: bash

      $ conan remove OpenSSL/* --builds --force

- Remove the recipe and the binary packages from a specific remote:

  .. code-block:: bash

      $ conan remove OpenSSL/1.0.2@lasote/stable -r myremote

- Remove only Windows OpenSSL packages from local cache:

  .. code-block:: bash

      $ conan remove OpenSSL/1.0.2@lasote/stable -q "os=Windows"
