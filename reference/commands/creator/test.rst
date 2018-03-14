
conan test
============

.. code-block:: bash

    $ conan test [-h] [-u] [-pr PROFILE] [-r REMOTE] [-o OPTIONS]
                 [-s SETTINGS] [-e ENV] [-b [BUILD [BUILD ...]]]
                 path reference

Runs a test_folder/conanfile.py to test an existing package. The package to be
tested must exist in the local cache or any configured remote. To create and
test a binary package for a local directory conanfile.py use the ``conan
create`` command.

.. code-block:: bash

    positional arguments:
      path                  path to the "testing" folder containing a recipe
                            (conanfile.py) with a test() method or to a recipe
                            file, e.g. conan test_package/conanfile.py
                            pkg/version@user/channel
      reference             a full package reference pkg/version@user/channel, of
                            the package to be tested

    optional arguments:
      -h, --help            show this help message and exit
      -tbf TEST_BUILD_FOLDER, --test-build-folder TEST_BUILD_FOLDER
                            Optional. Working directory of the build process.
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

This command is util for testing existing packages, that have been previously built (with :command:`conan create`, for example).
:command:`conan create` will automatically run this test if a *test_package* folder is found besides the *conanfile.py*, or if the
:command:`--test-folder` argument is provided to :command:`conan create`.

**Example**:

.. code-block:: bash

    $ conan new Hello/0.1 -s -t
    $ mv test_package test_package2
    $ conan create . user/testing
    # doesn't automatically run test, it has been renamed
    # now run test
    $ conan test test_package2 Hello/0.1@user/testing

The test package folder, could be elsewhere, or could be even applied to different versions of the
package.
