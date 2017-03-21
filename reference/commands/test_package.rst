.. _conan_test_package_command:

conan test_package
==================

.. code-block:: bash

	$ conan test_package [-h] [-ne] [-f FOLDER] [--scope SCOPE]
	                          [--keep-source] [--update] [--profile PROFILE]
	                          [-r REMOTE] [--options OPTIONS]
	                          [--settings SETTINGS] [--env ENV]
	                          [--build [BUILD [BUILD ...]]]
	                          [path]



The ``test_package`` (previously named **test**) command looks for a **test_package subfolder** in the current directory, and builds the
project that is in it. It will typically be a project with a single requirement, pointing to
the ``conanfile.py`` being developed in the current directory.

This was mainly intended to do a test of the package, not to run unit or integrations tests on the package
being created. Those tests could be launched if desired in the ``build()`` method.
But it can be used for that purpose if desired, there are no real technical constraints.

The command line arguments are exactly the same as the settings, options, and build parameters
for the ``install`` command, with one small difference:

In conan test, by default, the ``--build=CurrentPackage`` pattern is automatically appended for the
current tested package. You can always manually specify other build options, like ``--build=never``,
if you just want to check that the current existing package works for the test subproject, without
re-building it.

You can use the ``conan new`` command with the ``-t`` option to generate a ``test_package`` skeleton.


.. code-block:: bash

	positional arguments:
	  path                  path to conanfile file, e.g. /my_project/

	optional arguments:
	  -ne, --not-export     Do not export the conanfile before test execution
	  -f FOLDER, --folder FOLDER
	                        alternative test folder name
	  --scope SCOPE, -sc SCOPE
	                        Use the specified scope in the install command
	  --keep-source, -k     Optional. Do not remove the source folder in local cache.
                                Use for testing purposes only
	  --update, -u          update with new upstream packages, overwriting the local cache if needed.
	  --profile PROFILE, -pr PROFILE
	                        Apply the specified profile to the install command
	  -r REMOTE, --remote REMOTE
	                        look in the specified remote server
	  --options OPTIONS, -o OPTIONS
	                        Options to build the package, overwriting the defaults. e.g., -o with_qt=true
	  --settings SETTINGS, -s SETTINGS
	                        Settings to build the package, overwriting the defaults. e.g., -s compiler=gcc
	  --env ENV, -e ENV     Environment variables to set during the package build,
                                e.g. -e CXX=/usr/bin/clang++
	  --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]
	                        Optional, use it to choose if you want to build from sources:

	                        --build            Build all from sources, do not use binary packages.
	                        --build=never      Default option. Never build, use binary packages
                                                   or fail if a binary package is not found.
	                        --build=missing    Build from code if a binary package is not found.
	                        --build=outdated   Build from code if the binary is not built with the
                                                   current recipe or when missing binary package.
	                        --build=[pattern]  Build always these packages from source, but never build
                                                   the others. Allows multiple --build parameters.



If you want to use a different folder name than **test_package**, just use it and pass it to the ``-f folder``
command line option

.. code-block:: bash

    $ conan test_package --f my_test_folder


This command will run the equivalent to ``conan export <user>/<channel>`` where ``user`` and ``channel``
will be deduced from the values of the requirement in the ``conanfile.py`` inside the test subfolder.
This is very convenient, as if you are running a package test it is extremely likely that you have
just edited the package recipe. If the package recipe is locally modified, it has to be exported again,
otherwise, the package will be tested with the old recipe. If you want to inhibit this ``export``,
you can use the ``-ne, --no-export`` parameter.

