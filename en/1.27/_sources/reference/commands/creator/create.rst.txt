.. spelling::

  tf


.. _conan_create:

conan create
============

.. code-block:: bash

    $ conan create [-h] [-j JSON] [-k] [-kb] [-ne] [-tbf TEST_BUILD_FOLDER]
                   [-tf TEST_FOLDER] [--ignore-dirty] [-m [MANIFESTS]]
                   [-mi [MANIFESTS_INTERACTIVE]] [-v [VERIFY]] [-b [BUILD]]
                   [-r REMOTE] [-u] [-l [LOCKFILE]] [-e ENV_HOST]
                   [-e:b ENV_BUILD] [-e:h ENV_HOST] [-o OPTIONS_HOST]
                   [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                   [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                   [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                   [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                   path [reference]

Builds a binary package for a recipe (conanfile.py).

Uses the specified configuration in a profile or in -s settings, -o
options, etc. If a 'test_package' folder (the name can be configured
with -tf) is found, the command will run the consumer project to ensure
that the package has been created correctly. Check 'conan test' command
to know more about 'test_folder' project.

.. code-block:: text

    positional arguments:
      path                  Path to a folder containing a conanfile.py or to a
                            recipe file e.g., my_folder/conanfile.py
      reference             user/channel, version@user/channel or
                            pkg/version@user/channel (if name or version declared
                            in conanfile.py, they should match)

    optional arguments:
      -h, --help            show this help message and exit
      -j JSON, --json JSON  json file path where the install information will be
                            written to
      -k, -ks, --keep-source
                            Do not remove the source folder in the local cache,
                            even if the recipe changed. Use this for testing
                            purposes only
      -kb, --keep-build     Do not remove the build folder in local cache. Implies
                            --keep-source. Use this for testing purposes only
      -ne, --not-export     Do not export the conanfile.py
      -tbf TEST_BUILD_FOLDER, --test-build-folder TEST_BUILD_FOLDER
                            Working directory for the build of the test project.
      -tf TEST_FOLDER, --test-folder TEST_FOLDER
                            Alternative test folder name. By default it is
                            "test_package". Use "None" to skip the test stage
      --ignore-dirty        When using the "scm" feature with "auto" values,
                            capture the revision and url even if there are
                            uncommitted changes
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
                            build=package name'.
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


:command:`conan create . demo/testing` is equivalent to:

.. code-block:: bash

    $ conan export . demo/testing
    $ conan install hello/0.1@demo/testing --build=hello
    # package is created now, use test to test it
    $ cd test_package
    $ conan test . hello/0.1@demo/testing


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

In case of installing a pre-built binary, steps from 5 to 11 will be skipped. Note that ``deploy()`` method is only used in
:command:`conan install`.

.. note::

  Installation of binaries can be accelerated setting up parallel downloads with the ``general.parallel_download``
  **experimental** configuration in :ref:`conan_conf`.