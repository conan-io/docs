.. _conan_create_command:

conan create
============

.. code-block:: bash

    $ conan create [-h] [-ne] [-tf TEST_FOLDER] [-k] [-kb] [-m [MANIFESTS]]
                   [-mi [MANIFESTS_INTERACTIVE]] [-v [VERIFY]] [-u]
                   [-pr PROFILE] [-r REMOTE] [-o OPTIONS] [-s SETTINGS]
                   [-e ENV] [-b [BUILD [BUILD ...]]]
                   path reference

Builds a binary package for recipe (conanfile.py) located in current dir. Uses
the specified configuration in a profile or in -s settings, -o options etc. If
a 'test_package' folder (the name can be configured with -tf) is found, the
command will run the consumer project to ensure that the package has been
created correctly. Check the 'conan test' command to know more about the
'test_folder' project.

.. code-block:: bash

    positional arguments:
      path                  path to a folder containing a recipe (conanfile.py) or
                            to a recipe file, e.g., conan package
                            folder/conanfile.py
      reference             user/channel, or a full package reference
                            (Pkg/version@user/channel), if name and version are
                            not declared in the recipe (conanfile.py)

    optional arguments:
      -h, --help            show this help message and exit
      -ne, --not-export     Do not export the conanfile
      -tf TEST_FOLDER, --test-folder TEST_FOLDER
                            alternative test folder name, by default is
                            "test_package". "None" if test stage needs to be
                            disabled
      -k, --keep-source     Optional. Do not remove the source folder in local
                            cache. Use for testing purposes only
      -kb, --keep-build     Optional. Do not remove the build folder in local
                            cache. Use for testing purposes only
      -j JSON, --json JSON  Path to a json file where the install information will
                            be written
      -m [MANIFESTS], --manifests [MANIFESTS]
                            Install dependencies manifests in folder for later
                            verify. Default folder is .conan_manifests, but can be
                            changed
      -mi [MANIFESTS_INTERACTIVE], --manifests-interactive [MANIFESTS_INTERACTIVE]
                            Install dependencies manifests in folder for later
                            verify, asking user for confirmation. Default folder
                            is .conan_manifests, but can be changed
      -v [VERIFY], --verify [VERIFY]
                            Verify dependencies manifests against stored ones
      -u, --update          check updates exist from upstream remotes
      -pr PROFILE, --profile PROFILE
                            Apply the specified profile to the install command
      -r REMOTE, --remote REMOTE
                            look in the specified remote server
      -o OPTIONS, --options OPTIONS
                            Define options values, e.g., -o Pkg:with_qt=true
      -s SETTINGS, --settings SETTINGS
                            Settings to build the package, overwriting the
                            defaults. e.g., -s compiler=gcc
      -e ENV, --env ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      -b [BUILD [BUILD ...]], --build [BUILD [BUILD ...]]
                            Optional, use it to choose if you want to build from
                            sources: --build Build all from sources, do not use
                            binary packages. --build=never Never build, use binary
                            packages or fail if a binary package is not found.
                            --build=missing Build from code if a binary package is
                            not found. --build=outdated Build from code if the
                            binary is not built with the current recipe or when
                            missing binary package. --build=[pattern] Build always
                            these packages from source, but never build the
                            others. Allows multiple --build parameters. "pattern"
                            is a fnmatch file pattern of a package name. Default
                            behavior: If you dont specify anything, it will be
                            similar to --build=never, but package recipes can
                            override it and decide to build with "build_policy"

This is the recommended way to create packages.

:command:`conan create . demo/testing` is equivalent to:

.. code-block:: bash

    $ conan export . demo/testing
    $ conan install Hello/0.1@demo/testing --build=Hello
    # package is created now, use test to test it
    $ cd test_package
    $ conan test . Hello/0.1@demo/testing


.. tip::

    Sometimes you need to **skip/disable test stage** to avoid a failure while creating the package,
    i.e: when you are cross compiling libraries and target code cannot be executed in current host platform.
    In that case you can skip/disable the test package stage:

    .. code-block:: bash

        $ conan create . demo/testing --test-folder=None

:command:`conan create` executes methods of a *conanfile.py* in the following order:

1. ``config_options()``
2. ``configure()``
3. ``requirements()``
4. ``package_id()``
5. ``build_requirements()``
6. ``build_id()``
7. ``system_requirements()``
8. ``source()``
9. ``imports()``
10. ``build()``
11. ``package()``
12. ``package_info()``

In case of installing a pre-built binary, steps from 5 to 11 will be skipped. Note ``package_info()`` is used for consumers, it should not
be fired if there is no *test_package*. Note also that ``deploy()`` method is only used in :command:`conan install`.

