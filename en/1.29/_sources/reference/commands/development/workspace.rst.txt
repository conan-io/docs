
.. _conan_workspace:

conan workspace
===============

.. code-block:: bash

    $ conan workspace [-h] {install} ...

Manages a workspace (a set of packages consumed from the user workspace that
belongs to the same project).

Use this command to manage a Conan workspace, use the subcommand 'install' to
create the workspace from a file.

.. code-block:: text

    positional arguments:
      {install}   sub-command help
        install   same as a "conan install" command but using the workspace data
                  from the file. If no file is provided, it will look for a file
                  named "conanws.yml"

    optional arguments:
      -h, --help  show this help message and exit


.. _conan_workspace_install:

conan workspace install
-----------------------

.. code-block:: bash

    $ conan workspace install [-h] [-b [BUILD]] [-r REMOTE] [-u] [-l [LOCKFILE]]
                              [-e ENV_HOST] [-e:b ENV_BUILD] [-e:h ENV_HOST]
                              [-o OPTIONS_HOST] [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                              [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                              [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                              [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                              [-if INSTALL_FOLDER]
                              path

.. code-block:: text

    positional arguments:
      path                  path to workspace definition file (it will look for a "conanws.yml"
                            inside if a directory is given)

    optional arguments:
      -h, --help            show this help message and exit
      -b [BUILD], --build [BUILD]
                            Optional, use it to choose if you want to build from sources:
                            --build Build all from sources, do not use binary packages.
                            --build=never Never build, use binary packages or fail if a binary
                            package is not found. --build=missing Build from code if a binary
                            package is not found. --build=cascade Will build from code all the
                            nodes with some dependency being built (for any reason). Can be
                            used together with any other build policy. Useful to make sure that
                            any new change introduced in a dependency is incorporated by
                            building again the package. --build=outdated Build from code if the
                            binary is not built with the current recipe or when missing a
                            binary package. --build=[pattern] Build always these packages from
                            source, but never build the others. Allows multiple --build
                            parameters. 'pattern' is a fnmatch file pattern of a package
                            reference. Default behavior: If you don't specify anything, it will
                            be similar to '--build=never', but package recipes can override it
                            with their 'build_policy' attribute in the conanfile.py.
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -u, --update          Will check the remote and in case a newer version
                            and/or revision of the dependencies exists there, it
                            will install those in the local cache. When using
                            version ranges, it will install the latest version
                            that satisfies the range. Also, if using revisions, it
                            will update to the latest revision for the resolved
                            version range.
      -l [LOCKFILE], --lockfile [LOCKFILE]
                            Path to a lockfile or folder containing 'conan.lock' file. Lockfile
                            can be updated if packages change
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
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Folder where the workspace files will be created (default to
                            current working directory)


Note that these arguments, like ``settings`` and ``options`` mostly apply to the dependencies,
but those packages that are defined as editable in the workspace are in the user space.
Those packages won't be built by the command (even with ``--build`` arguments), as they are
built locally. It is the responsibility of the editables layout to match the settings (typically
parameterizing the layout with ``settings`` and ``options``)
