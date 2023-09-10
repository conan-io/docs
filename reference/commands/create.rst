conan create
============

.. code-block:: text

    $ conan create -h
    usage: conan create [-h] [-v [V]] [-f FORMAT] [--name NAME]
                        [--version VERSION] [--user USER] [--channel CHANNEL]
                        [-l LOCKFILE] [--lockfile-partial]
                        [--lockfile-out LOCKFILE_OUT] [--lockfile-packages]
                        [--lockfile-clean]
                        [--lockfile-overrides LOCKFILE_OVERRIDES] [-b BUILD]
                        [-r REMOTE | -nr] [-u] [-o OPTIONS_HOST]
                        [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                        [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                        [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                        [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST] [-c CONF_HOST]
                        [-c:b CONF_BUILD] [-c:h CONF_HOST] [--build-require]
                        [-tf TEST_FOLDER] [-bt BUILD_TEST]
                        path

    Create a package.

    positional arguments:
    path                  Path to a folder containing a recipe (conanfile.py)

    optional arguments:
    -h, --help            show this help message and exit
    -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
    -f FORMAT, --format FORMAT
                            Select the output format: json
    --name NAME           Provide a package name if not specified in conanfile
    --version VERSION     Provide a package version if not specified in
                            conanfile
    --user USER           Provide a user if not specified in conanfile
    --channel CHANNEL     Provide a channel if not specified in conanfile
    -l LOCKFILE, --lockfile LOCKFILE
                            Path to a lockfile. Use --lockfile="" to avoid
                            automatic use of existing 'conan.lock' file
    --lockfile-partial    Do not raise an error if some dependency is not found
                            in lockfile
    --lockfile-out LOCKFILE_OUT
                            Filename of the updated lockfile
    --lockfile-packages   Lock package-id and package-revision information
    --lockfile-clean      Remove unused entries from the lockfile
    --lockfile-overrides LOCKFILE_OVERRIDES
                            Overwrite lockfile overrides
    -b BUILD, --build BUILD
                            Optional, specify which packages to build from source.
                            Combining multiple '--build' options on one command
                            line is allowed. Possible values: --build="*" Force
                            build from source for all packages. --build=never
                            Disallow build for all packages, use binary packages
                            or fail if a binary package is not found, it cannot be
                            combined with other '--build' options. --build=missing
                            Build packages from source whose binary package is not
                            found. --build=cascade Build packages from source that
                            have at least one dependency being built from source.
                            --build=[pattern] Build packages from source whose
                            package reference matches the pattern. The pattern
                            uses 'fnmatch' style wildcards. --build=~[pattern]
                            Excluded packages, which will not be built from the
                            source, whose package reference matches the pattern.
                            The pattern uses 'fnmatch' style wildcards.
                            --build=missing:[pattern] Build from source if a
                            compatible binary does not exist, only for packages
                            matching pattern.
    -r REMOTE, --remote REMOTE
                            Look in the specified remote or remotes server
    -nr, --no-remote      Do not use remote, resolve exclusively in the cache
    -u, --update          Will check the remote and in case a newer version
                            and/or revision of the dependencies exists there, it
                            will install those in the local cache. When using
                            version ranges, it will install the latest version
                            that satisfies the range. Also, if using revisions, it
                            will update to the latest revision for the resolved
                            version range.
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
    -c CONF_HOST, --conf CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c
                            tools.cmake.cmaketoolchain:generator=Xcode
    -c:b CONF_BUILD, --conf:build CONF_BUILD
                            Configuration to build the package, overwriting the
                            defaults (build machine). e.g.: -c:b
                            tools.cmake.cmaketoolchain:generator=Xcode
    -c:h CONF_HOST, --conf:host CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c:h
                            tools.cmake.cmaketoolchain:generator=Xcode
    --build-require       Whether the package being created is a build-require
                            (to be used as tool_requires() by other packages)
    -tf TEST_FOLDER, --test-folder TEST_FOLDER
                            Alternative test folder name. By default it is
                            "test_package". Use "" to skip the test stage
    -bt BUILD_TEST, --build-test BUILD_TEST
                            Same as '--build' but only for the test_package
                            requires. By default if not specified it will take the
                            '--build' value if specified


The ``conan create`` command creates a package from the recipe specified in ``path``.

This command will first :command:`export` the recipe to the local cache and then build
and create the package. If a ``test_package`` folder (you can change the folder name with
the ``-tf`` argument) is found, the command will run the consumer project to ensure that
the package has been created correctly. Check :ref:`testing Conan packages
<tutorial_creating_test>` section to know more about how to test your Conan packages.

.. tip::

    Sometimes you want to **skip/disable the test stage**. In that case you can skip/disable
    the test package stage by passing an empty value as the ``-tf`` argument:

    .. code-block:: bash

        $ conan create . --test-folder=


Using conan create with build requirements
------------------------------------------

The ``--build-require`` argument allows to create the package using the configuration and
settings of the "build" context, as it was a ``build_require``. This feature allows to
create packages in a way that is consistent with the way they will be used later. 

.. code-block:: bash

    $ conan create . --name=cmake --version=3.23.1 --build-require  


Conan create output
-------------------

The ``conan create ... --format=json`` creates a json output containing the full dependency graph information.
This json is the same as the one created with ``conan graph info`` (see the :ref:`graph info json format<reference_commands_graph_info_json_format>`)
with extended information about the binaries, like a more complete ``cpp_info`` field.
This resulting json is the dependency graph of the package recipe being created, excluding all the ``test_package`` and other possible dependencies of the ``test_package/conanfile.py``. These dependencies only exist in the ``test_package`` functionality, and as such, are not part of the "main" product or package. If you are interested in capturing the dependency graph including the ``test_package`` (most likely not necessary in most cases), then you can do it running the ``conan test`` command separately.

The same happens for lockfiles created with ``--lockfile-out`` argument. The lockfile will only contain the created package and its transitive dependencies versions, but it will not contain the ``test_package`` or the transitive dependencies of the ``test_package/conanfile.py``. It is possible to capture a lockfile which includes those with the ``conan test`` command (though again, this might not be really necessary)

.. note::

  **Best practice**

  In general, having ``test_package/conanfile.py`` with dependencies other than the tested
  one should be avoided. The ``test_package`` functionality should serve as a simple check
  to ensure the package is correctly created. Adding extra dependencies to
  ``test_package`` might indicate that the check is not straightforward or that its
  functionality is being misused. If, for any reason, your ``test_package`` has additional
  dependencies, you can control their build using the ``--build-test`` argument.


.. seealso::

    - Read more about creating packages in the :ref:`dedicated
      tutorial<tutorial_creating_packages>`
