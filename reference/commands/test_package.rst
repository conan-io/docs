.. _conan_test_package_command:

conan test_package
==================

.. code-block:: bash

	$  conan test_package [-h] [-ne] [-tf TEST_FOLDER] [--keep-source]
                          [--test-only] [--cwd CWD] [--manifests [MANIFESTS]]
                          [--manifests-interactive [MANIFESTS_INTERACTIVE]]
                          [--verify [VERIFY]] [--update] [--scope SCOPE]
                          [--profile PROFILE] [-r REMOTE] [--options OPTIONS]
                          [--settings SETTINGS] [--env ENV]
                          [--build [BUILD [BUILD ...]]]
                          [reference]


.. note::

    The ``test_package`` command was the preferred way to create packages. Now this has been superseded by the ``conan create``
    command. ``test_package`` will keep backwards compatibility for a while, but the recommended usage from now would be to use
    for pure testing, with ``conan test_package user/channel --test-only``


The ``test_package`` command looks for a **test_package subfolder** in the current directory, and builds the
project that is in it. It will typically be a project with a single requirement, pointing to
the ``conanfile.py`` being developed in the current directory.

This was mainly intended to do a test of the package, not to run unit or integrations tests on the package
being created. Those tests could be launched if desired in the ``build()`` method.
But it can be used for that purpose if desired, there are no real technical constraints.

The command line arguments are exactly the same as the settings, options, and build parameters
for the ``install`` command, with one small difference:

In conan test_package, by default, the ``--build=CurrentPackage`` pattern is automatically appended for the
currently tested package. You can always manually specify other build options, like ``--build=never``,
if you just want to check that the current existing package works for the test subproject, without
re-building it.

You can use the ``conan new`` command with the ``-t`` option to generate a ``test_package`` skeleton.


.. code-block:: bash

    positional arguments:
      reference         a full package reference Pkg/version@user/channel, or
                        just the user/channel if package and version are
                        defined in recipe

    optional arguments:
          -h, --help            show this help message and exit
          -ne, --not-export     Do not export the conanfile before test execution
          -tf TEST_FOLDER, --test_folder TEST_FOLDER
                                alternative test folder name, by default is
                                "test_package"
          --keep-source, -k     Optional. Do not remove the source folder in local
                                cache. Use for testing purposes only
          --test-only, -t       Just run the test, without exporting or building the
                                package
          --cwd CWD, -c CWD     Use this directory as the current directory
          --manifests [MANIFESTS], -m [MANIFESTS]
                                Install dependencies manifests in folder for later
                                verify. Default folder is .conan_manifests, but can be
                                changed
          --manifests-interactive [MANIFESTS_INTERACTIVE], -mi [MANIFESTS_INTERACTIVE]
                                Install dependencies manifests in folder for later
                                verify, asking user for confirmation. Default folder
                                is .conan_manifests, but can be changed
          --verify [VERIFY], -v [VERIFY]
                                Verify dependencies manifests against stored ones
          --update, -u          check updates exist from upstream remotes
          --scope SCOPE, -sc SCOPE
                                Use the specified scope in the install command
          --profile PROFILE, -pr PROFILE
                                Apply the specified profile to the install command
          -r REMOTE, --remote REMOTE
                                look in the specified remote server
          --options OPTIONS, -o OPTIONS
                                Options to build the package, overwriting the
                                defaults. e.g., -o with_qt=true
          --settings SETTINGS, -s SETTINGS
                                Settings to build the package, overwriting the
                                defaults. e.g., -s compiler=gcc
          --env ENV, -e ENV     Environment variables that will be set during the
                                package build, -e CXX=/usr/bin/clang++
          --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]
                                Optional, use it to choose if you want to build from
                                sources: --build Build all from sources, do not use
                                binary packages. --build=never Default option. Never
                                build, use binary packages or fail if a binary package
                                is not found. --build=missing Build from code if a
                                binary package is not found. --build=outdated Build
                                from code if the binary is not built with the current
                                recipe or when missing binary package.
                                --build=[pattern] Build always these packages from
                                source, but never build the others. Allows multiple
                                --build parameters.




If you want to use a different folder name than **test_package**, just use it and pass it to the ``-f folder``
command line option

.. code-block:: bash

    $ conan test_package --tf my_test_folder


This command will run the equivalent to ``conan export <user>/<channel>`` where ``user`` and ``channel``
will be deduced from the values of the requirement in the ``conanfile.py`` inside the test subfolder.
This is very convenient, as if you are running a package test it is extremely likely that you have
just edited the package recipe. If the package recipe is locally modified, it has to be exported again,
otherwise, the package will be tested with the old recipe. If you want to inhibit this ``export``,
you can use the ``-ne, --no-export`` parameter.

