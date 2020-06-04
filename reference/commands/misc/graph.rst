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


.. _conan_graph_clean_modified:

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

.. _conan_graph_build_order:

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
                          Optional, specify which packages to build from source.
                          Combining multiple '--build' options on one command
                          line is allowed. For dependencies, the optional
                          'build_policy' attribute in their conanfile.py takes
                          precedence over the command line parameter. Possible
                          parameters: --build Force build for all packages, do
                          not use binary packages. --build=never Disallow build
                          for all packages, use binary packages or fail if a
                          binary package is not found. Cannot be combined with
                          other '--build' options. --build=missing Build
                          packages from source whose binary package is not
                          found. --build=outdated Build packages from source
                          whose binary package was not generated from the latest
                          recipe or is not found. --build=cascade Build packages
                          from source that have at least one dependency being
                          built from source. --build=[pattern] Build packages
                          from source whose package reference matches the
                          pattern. The pattern uses 'fnmatch' style wildcards.
                          Default behavior: If you omit the '--build' option,
                          the 'build_policy' attribute in conanfile.py will be
                          used if it exists, otherwise the behavior is like '--
                          build=never'.
    --json JSON           generate output file in json format


The result is a list of lists, containing tuples. Each tuple contains 2 elements, the
first is a UUID of the node of the graph. It is unique and ensures a way to address
exactly one node, even if there are nodes with the same reference (it is possible for
example to have different build_requires with the same name and version, but different
configuration)


conan graph lock
----------------

.. code-block:: bash

    conan graph lock [-h] [-l LOCKFILE] [-b [BUILD]] [-r REMOTE] [-u] [-e ENV_HOST]
                     [-e:b ENV_BUILD] [-e:h ENV_HOST] [-o OPTIONS_HOST]
                     [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST] [-pr PROFILE_HOST]
                     [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                     [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                     path_or_reference

.. code-block:: text

    positional arguments:
      path_or_reference     Path to a folder containing a recipe (conanfile.py or
                            conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt. It could also be a reference

    optional arguments:
      -h, --help            show this help message and exit
      -l LOCKFILE, --lockfile LOCKFILE
                            Path to lockfile to be created. If not specified 'conan.lock' will
                            be created in current folder
      -b [BUILD], --build [BUILD]
                            Packages to build from source
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -u, --update          Check updates exist from upstream remotes
      -e ENV_HOST, --env ENV_HOST
                            Environment variables that will be set during the package build
                            (host machine). e.g.: -e CXX=/usr/bin/clang++
      -e:b ENV_BUILD, --env:build ENV_BUILD
                            Environment variables that will be set during the package build
                            (build machine). e.g.: -e CXX=/usr/bin/clang++
      -e:h ENV_HOST, --env:host ENV_HOST
                            Environment variables that will be set during the package build
                            (host machine). e.g.: -e CXX=/usr/bin/clang++
      -o OPTIONS_HOST, --options OPTIONS_HOST
                            Define options values (host machine), e.g.: -o Pkg:with_qt=true
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                            Define options values (build machine), e.g.: -o Pkg:with_qt=true
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                            Define options values (host machine), e.g.: -o Pkg:with_qt=true
      -pr PROFILE_HOST, --profile PROFILE_HOST
                            Apply the specified profile to the host machine
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                            Apply the specified profile to the build machine
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                            Apply the specified profile to the host machine
      -s SETTINGS_HOST, --settings SETTINGS_HOST
                            Settings to build the package, overwriting the defaults (host
                            machine). e.g.: -s compiler=gcc
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                            Settings to build the package, overwriting the defaults (build
                            machine). e.g.: -s compiler=gcc
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                            Settings to build the package, overwriting the defaults (host
                            machine). e.g.: -s compiler=gcc



This command is similar to :command:`conan install` or :command:`conan info`, but
with a few differences:

- It doesn't need to retrieve binaries, it will only compute what is necessary to do, according to the ``--build`` argument and rules
- Even when ``--build`` values are specified, packages will not be built from sources. It will just compute, as a "dry-run" what would happen in an equivalent :command:`conan install`
