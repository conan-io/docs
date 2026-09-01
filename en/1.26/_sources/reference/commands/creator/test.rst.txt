
.. _conan_test:

conan test
==========

.. code-block:: bash

    $ conan test [-h] [-tbf TEST_BUILD_FOLDER] [-b [BUILD]] [-r REMOTE] [-u]
                 [-l [LOCKFILE]] [-e ENV_HOST] [-e:b ENV_BUILD]
                 [-e:h ENV_HOST] [-o OPTIONS_HOST] [-o:b OPTIONS_BUILD]
                 [-o:h OPTIONS_HOST] [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                 [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                 [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                 path reference

Tests a package consuming it from a conanfile.py with a test() method.

This command installs the conanfile dependencies (including the tested
package), calls a 'conan build' to build test apps and finally executes
the test() method. The testing recipe does not require name or version,
neither definition of package() or package_info() methods. The package
to be tested must exist in the local cache or any configured remote.

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
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -u, --update          Check updates exist from upstream remotes
      -l [LOCKFILE], --lockfile [LOCKFILE]
                            Path to a lockfile or folder containing 'conan.lock'
                            file. Lockfile can be updated if packages change
      -e ENV_HOST, --env ENV_HOST
                            Environment variables that will be set during the
                            package build (host machine). e.g.: -e
                            CXX=/usr/bin/clang++
      -e:b ENV_BUILD, --env:build ENV_BUILD
                            Environment variables that will be set during the
                            package build (build machine). e.g.: -e:b
                            CXX=/usr/bin/clang++
      -e:h ENV_HOST, --env:host ENV_HOST
                            Environment variables that will be set during the
                            package build (host machine). e.g.: -e:h
                            CXX=/usr/bin/clang++
      -o OPTIONS_HOST, --options OPTIONS_HOST
                            Define options values (host machine), e.g.: -o
                            Pkg:with_qt=true
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                            Define options values (build machine), e.g.: -o:b
                            Pkg:with_qt=true
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                            Define options values (host machine), e.g.: -o:h
                            Pkg:with_qt=true
      -pr PROFILE_HOST, --profile PROFILE_HOST
                            Apply the specified profile to the host machine
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                            Apply the specified profile to the build machine
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                            Apply the specified profile to the host machine
      -s SETTINGS_HOST, --settings SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s compiler=gcc
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                            Settings to build the package, overwriting the
                            defaults (build machine). e.g.: -s:b compiler=gcc
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s:h compiler=gcc


This command is util for testing existing packages, that have been previously built (with :command:`conan create`, for example).
:command:`conan create` will automatically run this test if a *test_package* folder is found besides the *conanfile.py*, or if the
:command:`--test-folder` argument is provided to :command:`conan create`.

**Example**:

.. code-block:: bash

    $ conan new hello/0.1 -s -t
    $ mv test_package test_package2
    $ conan create . user/testing
    # doesn't automatically run test, it has been renamed
    # now run test
    $ conan test test_package2 hello/0.1@user/testing

The test package folder, could be elsewhere, or could be even applied to different versions of the
package.
