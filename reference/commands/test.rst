.. _reference_commands_test:

conan test
===========

.. code-block:: text

    $ conan test -h
    usage: conan test [-h] [-v [V]] [-f FORMAT] [-b BUILD] [-r REMOTE | -nr] [-u]
                      [-pr PROFILE] [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                      [-pr:a PROFILE_ALL] [-o OPTIONS] [-o:b OPTIONS_BUILD]
                      [-o:h OPTIONS_HOST] [-o:a OPTIONS_ALL] [-s SETTINGS]
                      [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                      [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                      [-c:h CONF_HOST] [-c:a CONF_ALL] [-l LOCKFILE]
                      [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                      [--lockfile-packages] [--lockfile-clean]
                      [--lockfile-overrides LOCKFILE_OVERRIDES]
                      path reference

    Test a package from a test_package folder.

    positional arguments:
      path                  Path to a test_package folder containing a
                            conanfile.py
      reference             Provide a package reference to test

    options:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      -f FORMAT, --format FORMAT
                            Select the output format: json
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


The ``conan test`` command uses the *test_package* folder specified in ``path`` to tests the package reference specified in ``reference``.

.. seealso::

    - Read the tutorial about :ref:`testing Conan packages <tutorial_creating_test>`.
