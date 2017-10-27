
conan test
============

.. code-block:: bash

	$ conan test [-h] [--update] [--scope SCOPE] [--profile PROFILE]
               [-r REMOTE] [--options OPTIONS] [--settings SETTINGS]
               [--env ENV] [--build [BUILD [BUILD ...]]]
               path [reference]

Runs a test_folder/conanfile.py to test an existing package. The package to be
tested must exist in the local cache or any configured remote. To create and
test a binary package for a local directory conanfile.py use the ``conan
create`` command.

.. code-block:: bash

    positional arguments:
      path                  path to a recipe (conanfile.py), e.g., conan test
                            pkg/version@user/channel
      reference             a full package reference pkg/version@user/channel, or
                            just the package name "pkg" if the test_package
                            conanfile is requiring more than one reference. Empty
                            if the conanfile has onlyone require

    optional arguments:
      -h, --help            show this help message and exit
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


This command is util for testing existing packages, that have been previously built (with ``conan create``, for example).
``conan create`` will automatically run this test if a ``test_package`` folder is found besides the conanfile.py, or if
the ``--test-folder`` argument is provided to ``conan create``.


**Examples**:



.. code-block:: bash

	$ conan new Hello/0.1 -s -t
  $ mv test_package test_package2
  $ conan create user/testing
  # doesn't automatically run test, it has been renamed
  # now run test
  $ conan test test_package2 Hello/0.1@user/testing

The test package folder, could be elsewhere, or could be even applied to different versions of the package.
