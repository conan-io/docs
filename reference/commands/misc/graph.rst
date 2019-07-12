.. _conan_graph:

conan graph
===========

.. code-block:: bash

    $ conan graph [-h] {update-lock,build-order,clean-modified,lock} ...

Generates and manipulates lock files.

.. code-block:: text

    positional arguments:
      {update-lock,build-order,clean-modified,lock}
                            sub-command help
        update-lock         merge two lockfiles
        build-order         Returns build-order
        clean-modified      Clean modified
        lock                create a lockfile

    optional arguments:
      -h, --help            show this help message and exit



conan graph update-lock
-----------------------

.. code-block:: bash

    $ conan graph update-lock [-h] old_lockfile new_lockfile

Updates the *old_lockfile* file with the contents of the *new_lockfiles*.

.. code-block:: text

  positional arguments:
    old_lockfile  path to previous lockfile
    new_lockfile  path to modified lockfile

  optional arguments:
    -h, --help    show this help message and exit


Only the packages in *new_lockfile* marked as "modified" will be processed.
If a node in *old_lockfile* is already modified and an incompatible (different
binary ID, different revision) updated is attempted, it will raise an error.
The updated nodes will keep the "modified" flag when updated in *old_lockfile*

This command is useful for distributed or concurrent builds of different packages
in the same dependency graph locked by the same lockfile. When one package is rebuilt
it will modify the package reference, and will be marked as "modified". The way
of integrating the information of package builds into the main lockfile is this command.

Example:

Integrate the information of building a "pkgb" package using a lockfile (and modified
in the folder pkgb_temp) in the main lockfile:

.. code-block:: bash

    $ conan graph update-lock release/conan.lock pkgb_temp/release/conan.lock


conan graph clean-modified
--------------------------

.. code-block:: bash

    $ conan graph clean-modified [-h] lockfile

Cleans all "modified" flags from the given lockfile.

.. code-block:: text

  positional arguments:
    lockfile    lockfile folder

  optional arguments:
    -h, --help  show this help message and exit

When a package of a dependency graph is going to be re-built, using a given lockfile,
it is desired to finish the build knowing which packages of the graph have been
actually rebuilt as a result of the last command. This command will clean all the
previously existing "modified" flags before such build, so after the build 
the "modified" are only those that have been built now.

conan graph build-order
-----------------------

.. code-block:: bash

  $ conan graph build-order [-h] [-b [BUILD]] [--json JSON] lockfile


Given a lockfile, compute which packages and in which order they should be built,
as mandated by the binary ID (``package_id()``) definitions and the ``--build`` argument,
which is the same as :command:`conan create|install`

.. code-block:: text

  positional arguments:
    lockfile              lockfile folder

  optional arguments:
    -h, --help            show this help message and exit
    -b [BUILD], --build [BUILD]
                          nodes to build
    --json JSON           generate output file in json format


The result is a list of lists, containing tuples. Each tuple contains 2 elements, the
first is a UUID of the node of the graph. It is unique and ensures a way to address
exactly one node, even if there are nodes with the same reference (it is possible for
example to have different build_requires with the same name and version, but different
configuration)


conan graph lock
----------------

.. code-block:: bash

    conan graph lock [-h] [-l LOCKFILE] [-b [BUILD]] [-e ENV] [-o OPTIONS]
                            [-pr PROFILE] [-r REMOTE] [-s SETTINGS] [-u]
                            path_or_reference

.. code-block:: text

    positional arguments:
      path_or_reference     Path to a folder containing a recipe (conanfile.py or
                            conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt. It could also be a
                            reference

    optional arguments:
      -h, --help            show this help message and exit
      -l LOCKFILE, --lockfile LOCKFILE
                            Path to lockfile to be created. If not specified
                            'conan.lock' will be created in current folder
      -b [BUILD], --build [BUILD]
                            Packages to build from source
      -e ENV, --env ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      -o OPTIONS, --options OPTIONS
                            Define options values, e.g., -o Pkg:with_qt=true
      -pr PROFILE, --profile PROFILE
                            Apply the specified profile to the install command
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -s SETTINGS, --settings SETTINGS
                            Settings to build the package, overwriting the
                            defaults. e.g., -s compiler=gcc
      -u, --update          Check updates exist from upstream remotes


This command is similar to :command:`conan install` or :command:`conan info`, but
with a few differences:

- It doesn't need to retrieve binaries, it will only compute what is necessary to do, according to the ``--build`` argument and rules
- Even when ``--build`` values are specified, packages will not be built from sources. It will just compute, as a "dry-run" what would happen in an equivalent :command:`conan install`
