
.. _conan_workspace:

conan workspace
===============

.. code-block:: bash

    $ conan workspace [-h] {install} ...

Command to manage workspaces

.. code-block:: text

    positional arguments:
    {install}   sub-command help
        install   same as a "conan install" command but using the workspace data
                from the file

    optional arguments:
    -h, --help  show this help message and exit


.. _conan_workspace_install:

conan workspace install
-----------------------

.. code-block:: bash

    $ conan workspace install [-h] [-b [BUILD]] [-e ENV] [-o OPTIONS]
                               [-pr PROFILE] [-r REMOTE] [-s SETTINGS] [-u]
                               path

.. code-block:: text

    positional arguments:
    path                  path to workspace definition file

    optional arguments:
    -h, --help            show this help message and exit
    -b [BUILD], --build [BUILD]
                            Optional, use it to choose if you want to build from
                            sources: --build Build all from sources, do not use
                            binary packages. --build=never Never build, use binary
                            packages or fail if a binary package is not found.
                            --build=missing Build from code if a binary package is
                            not found. --build=outdated Build from code if the
                            binary is not built with the current recipe or when
                            missing binary package. --build=[pattern] Build always
                            these packages from source, but never build the
                            others. Allows multiple --build parameters. 'pattern'
                            is a fnmatch file pattern of a package name. Default
                            behavior: If you don't specify anything, it will be
                            similar to '--build=never', but package recipes can
                            override it with their 'build_policy' attribute in the
                            conanfile.py.
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


Note that these arguments, like ``settings`` and ``options`` mostly apply to the dependencies,
but those packages that are defined as editable in the workspace are in the user space.
Those packages won't be built by the command (even with ``--build`` arguments), as they are
built locally. It is the responsibility of the editables layout to match the settings (typically
parameterizing the layout with ``settings`` and ``options``)