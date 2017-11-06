.. _conan_create_command:

conan create
============

.. code-block:: bash

	$  conan create [-h] [--cwd CWD] [--file FILE] [-ne] [-tf TEST_FOLDER]
                        [--keep-source] [--werror] [--manifests [MANIFESTS]]
                        [--manifests-interactive [MANIFESTS_INTERACTIVE]]
                        [--verify [VERIFY]] [--update] [--scope SCOPE]
                        [--profile PROFILE] [-r REMOTE] [--options OPTIONS]
                        [--settings SETTINGS] [--env ENV]
                        [--build [BUILD [BUILD ...]]]
                        reference


Builds a binary package for recipe (conanfile.py) located in current dir. Uses
the specified configuration in a profile or in -s settings, -o options etc. If
a 'test_package' folder (the name can be configured with -tf) is found, the
command will run the consumer project to ensure that the package has been
created correctly. Check the 'conan test' command to know more about the
'test_folder' project.


.. code-block:: bash

    positional arguments:
      reference             user/channel, or a full package reference
                            (Pkg/version@user/channel), if name and version are
                            not declared in the recipe

    optional arguments:
      -h, --help            show this help message and exit
      --cwd CWD, -c CWD     Optional. Folder with a conanfile.py. Default current
                            directory.
      --file FILE, -f FILE  specify conanfile filename
      -ne, --not-export     Do not export the conanfile
      -tf TEST_FOLDER, --test-folder TEST_FOLDER, --test_folder TEST_FOLDER
                            alternative test folder name, by default is
                            "test_package"
      --keep-source, -k     Optional. Do not remove the source folder in local
                            cache. Use for testing purposes only
      --werror              Error instead of warnings for graph inconsistencies
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
                            Define options values, e.g., -o Pkg:with_qt=true
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
                            --build parameters. 'pattern' is a fnmatch file
                            pattern of a package name.



This is the recommended way to create packages.

``conan create demo/testing`` is equivalent to:

.. code-block:: bash

    $ conan export demo/testing
    $ conan install Hello/0.1@demo/testing --build=Hello
    # package is created now, use test to test it
    $ cd test_package
    $ conan test . Hello/0.1@demo/testing