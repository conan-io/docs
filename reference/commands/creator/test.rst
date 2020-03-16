
.. _conan_test:

conan test
==========

.. code-block:: bash

    $ conan test [-h] [-tbf TEST_BUILD_FOLDER] [-b [BUILD]] [-e ENV]
                 [-o OPTIONS] [-pr PROFILE] [-r REMOTE] [-s SETTINGS] [-u]
                 [-l [LOCKFILE]]
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
