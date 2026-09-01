
.. _conan_test:

conan test
==========

.. code-block:: bash

    $ conan test [-h] [-tbf TEST_BUILD_FOLDER] [-b [BUILD]] [-e ENV]
                 [-o OPTIONS] [-pr PROFILE] [-r REMOTE] [-s SETTINGS] [-u]
                 path reference

Tests a package consuming it from a conanfile.py with a test() method.

This command installs the conanfile dependencies (including the tested
package), calls a 'conan build' to build test apps and finally executes
the test() method. The testing recipe does not require name or version,
neither definition of package() or package_info() methods. The package
to be tested must exist in the local cache or in any configured remote.

.. code-block:: text

    positional arguments:
      path                  Path to the "testing" folder containing a conanfile.py
                            or to a recipe file with test() methode.g. conan
                            test_package/conanfile.py pkg/version@user/channel
      reference             pkg/version@user/channel of the package to be tested

    optional arguments:
      -h, --help            show this help message and exit
      -tbf TEST_BUILD_FOLDER, --test-build-folder TEST_BUILD_FOLDER
                            Working directory of the build process.
      -b [BUILD], --build [BUILD]
                            Optional, use it to choose if you want to build from
                            sources: --build Build all from sources, do not use
                            binary packages. --build=never Never build, use binary
                            packages or fail if a binary package is not found.
                            --build=missing Build from code if a binary package is
                            not found. --build=cascade Will build from code all
                            the nodes with some dependency being built (for any
                            reason). Can be used together with any other build
                            policy. Useful to make sure that any new change
                            introduced in a dependency is incorporated by building
                            again the package. --build=outdated Build from code if
                            the binary is not built with the current recipe or
                            when missing binary package. --build=[pattern] Build
                            always these packages from source, but never build the
                            others. Allows multiple --build parameters. 'pattern'
                            is a fnmatch file pattern of a package reference.
                            Default behavior: If you don't specify anything, it
                            will be similar to '--build=never', but package
                            recipes can override it with their 'build_policy'
                            attribute in the conanfile.py.
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
