.. _conan_lock:

conan lock
===========

.. code-block:: bash

    $ conan lock [-h] {update,build-order,clean-modified,create} ...

Generates and manipulates lock files.

.. code-block:: text

    positional arguments:
        {update,build-order,clean-modified,create}
                            sub-command help
        update              Complete missing information in the first lockfile with information defined in the second lockfile. Both lockfiles must represent the same graph,
                            and have the same topology with the same identifiers, i.e. the second lockfile must be an evolution based on the first one
        build-order         Returns build-order
        clean-modified      Clean modified flags
        create              Create a lockfile from a conanfile or a reference

    optional arguments:
        -h, --help            show this help message and exit



.. seealso::

    read about lockfiles in :ref:`versioning_lockfiles`



conan lock create
-----------------
.. code-block:: bash

    $ conan lock create [-h] [--name NAME] [--version VERSION] [--user USER] [--channel CHANNEL] [--reference REFERENCE] [-l LOCKFILE] [--base]
                         [--lockfile-out LOCKFILE_OUT] [-b [BUILD]] [-r REMOTE] [-u] [-e ENV_HOST] [-e:b ENV_BUILD] [-e:h ENV_HOST] [-o OPTIONS_HOST] [-o:b OPTIONS_BUILD]
                         [-o:h OPTIONS_HOST] [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST] [-s SETTINGS_HOST] [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                         [path]


.. code-block:: text

    positional arguments:
      path                  Path to a conanfile

    optional arguments:
      -h, --help            show this help message and exit
      --name NAME           Provide a package name if not specified in conanfile
      --version VERSION     Provide a package version if not specified in conanfile
      --user USER           Provide a user
      --channel CHANNEL     Provide a channel
      --reference REFERENCE
                            Provide a package reference instead of a conanfile
      -l LOCKFILE, --lockfile LOCKFILE
                            Path to lockfile to be used as a base
      --base                Lock only recipe versions and revisions
      --lockfile-out LOCKFILE_OUT
                            Filename of the created lockfile
      -b [BUILD], --build [BUILD]
                            Packages to build from source
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -u, --update          Will check the remote and in case a newer version and/or revision of the dependencies exists there, it will install those in the local cache. When
                            using version ranges, it will install the latest version that satisfies the range. Also, if using revisions, it will update to the latest revision
                            for the resolved version range.
      -e ENV_HOST, --env ENV_HOST
                            Environment variables that will be set during the package build (host machine). e.g.: -e CXX=/usr/bin/clang++
      -e:b ENV_BUILD, --env:build ENV_BUILD
                            Environment variables that will be set during the package build (build machine). e.g.: -e:b CXX=/usr/bin/clang++
      -e:h ENV_HOST, --env:host ENV_HOST
                            Environment variables that will be set during the package build (host machine). e.g.: -e:h CXX=/usr/bin/clang++
      -o OPTIONS_HOST, --options OPTIONS_HOST
                            Define options values (host machine), e.g.: -o Pkg:with_qt=true
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                            Define options values (build machine), e.g.: -o:b Pkg:with_qt=true
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                            Define options values (host machine), e.g.: -o:h Pkg:with_qt=true
      -pr PROFILE_HOST, --profile PROFILE_HOST
                            Apply the specified profile to the host machine
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                            Apply the specified profile to the build machine
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                            Apply the specified profile to the host machine
      -s SETTINGS_HOST, --settings SETTINGS_HOST
                            Settings to build the package, overwriting the defaults (host machine). e.g.: -s compiler=gcc
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                            Settings to build the package, overwriting the defaults (build machine). e.g.: -s:b compiler=gcc
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                            Settings to build the package, overwriting the defaults (host machine). e.g.: -s:h compiler=gcc


conan lock update
-----------------

.. code-block:: bash

    $ conan lock update [-h] old_lockfile new_lockfile

.. code-block:: text

    positional arguments:
        old_lockfile  Path to lockfile to be updated
        new_lockfile  Path to lockfile containing the new information that is going to be updated into the first lockfile

    optional arguments:
        -h, --help    show this help message and exit



conan lock build-order
----------------------

.. code-block:: bash

    $ conan lock build-order [-h] [--json JSON] lockfile

.. code-block:: text

    positional arguments:
        lockfile     lockfile file

    optional arguments:
        -h, --help   show this help message and exit
        --json JSON  generate output file in json format


conan lock clean-modified
-------------------------

.. code-block:: bash

    $ conan lock clean-modified [-h] lockfile

.. code-block:: text

    positional arguments:
        lockfile    Path to the lockfile

    optional arguments:
        -h, --help  show this help message and exit