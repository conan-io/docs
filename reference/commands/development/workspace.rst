
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

    $ conan workspace install [-h] [-b [BUILD]] [-e ENV] [-o OPTIONS]
                              [-pr PROFILE] [-r REMOTE] [-s SETTINGS] [-u]
                              [-if INSTALL_FOLDER]
                              path

.. code-block:: text

  positional arguments:
    path                  path to workspace definition file (it will look for a
                          "conanws.yml" inside if a directory is given)

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
    -e ENV, --env ENV     Environment variables that will be set during the
                          package build, -e CXX=/usr/bin/clang++
    -o OPTIONS, --options OPTIONS
                          Define options values, e.g., -o Pkg:with_qt=True
    -pr PROFILE, --profile PROFILE
                          Apply the specified profile to the install command
    -r REMOTE, --remote REMOTE
                          Look in the specified remote server
    -s SETTINGS, --settings SETTINGS
                          Settings to build the package, overwriting the
                          defaults. e.g., -s compiler=gcc
    -u, --update          Check updates exist from upstream remotes
    -l [LOCKFILE], --lockfile [LOCKFILE]
                          Path to a lockfile or folder containing 'conan.lock'
                          file. Lockfile can be updated if packages change
    -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                          Folder where the workspace files will be created
                          (default to current working directory)


Note that these arguments, like ``settings`` and ``options`` mostly apply to the dependencies,
but those packages that are defined as editable in the workspace are in the user space.
Those packages won't be built by the command (even with ``--build`` arguments), as they are
built locally. It is the responsibility of the editables layout to match the settings (typically
parameterizing the layout with ``settings`` and ``options``)
