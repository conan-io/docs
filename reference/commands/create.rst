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
                        [-r REMOTE | -nr] [-u] [-pr PROFILE] [-pr:b PROFILE_BUILD]
                        [-pr:h PROFILE_HOST] [-pr:a PROFILE_ALL] [-o OPTIONS]
                        [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                        [-o:a OPTIONS_ALL] [-s SETTINGS] [-s:b SETTINGS_BUILD]
                        [-s:h SETTINGS_HOST] [-s:a SETTINGS_ALL] [-c CONF]
                        [-c:b CONF_BUILD] [-c:h CONF_HOST] [-c:a CONF_ALL]
                        [--build-require] [-tf TEST_FOLDER] [-bt BUILD_TEST]
                        path

    Create a package.

    positional arguments:
      path                  Path to a folder containing a recipe (conanfile.py)

    options:
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
      -pr PROFILE, --profile PROFILE
                            Apply the specified profile. By default, or if
                            specifying -pr:h (--profile:host), it applies to the
                            host context. Use -pr:b (--profile:build) to specify
                            the build context, or -pr:a (--profile:all) to specify
                            both contexts at once
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
      -pr:a PROFILE_ALL, --profile:all PROFILE_ALL
      -o OPTIONS, --options OPTIONS
                            Apply the specified options. By default, or if
                            specifying -o:h (--options:host), it applies to the
                            host context. Use -o:b (--options:build) to specify
                            the build context, or -o:a (--options:all) to specify
                            both contexts at once. Example: -o pkg:with_qt=true
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
      -o:a OPTIONS_ALL, --options:all OPTIONS_ALL
      -s SETTINGS, --settings SETTINGS
                            Apply the specified settings. By default, or if
                            specifying -s:h (--settings:host), it applies to the
                            host context. Use -s:b (--settings:build) to specify
                            the build context, or -s:a (--settings:all) to specify
                            both contexts at once. Example: -s compiler=gcc
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
      -s:a SETTINGS_ALL, --settings:all SETTINGS_ALL
      -c CONF, --conf CONF  Apply the specified conf. By default, or if specifying
                            -c:h (--conf:host), it applies to the host context.
                            Use -c:b (--conf:build) to specify the build context,
                            or -c:a (--conf:all) to specify both contexts at once.
                            Example: -c tools.cmake.cmaketoolchain:generator=Xcode
      -c:b CONF_BUILD, --conf:build CONF_BUILD
      -c:h CONF_HOST, --conf:host CONF_HOST
      -c:a CONF_ALL, --conf:all CONF_ALL
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
