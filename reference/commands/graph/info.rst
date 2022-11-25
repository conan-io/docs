conan graph info
================

.. code-block:: bash
        
    conan graph info -h
    usage: conan graph info [-h] [-f FORMAT] [-v [V]] [--logger] [--name NAME] [--version VERSION]
                            [--user USER] [--channel CHANNEL] [--requires REQUIRES]
                            [--tool-requires TOOL_REQUIRES] [-b [BUILD]] [-r REMOTE] [-u]
                            [-o OPTIONS_HOST] [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                            [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                            [-s SETTINGS_HOST] [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                            [-c CONF_HOST] [-c:b CONF_BUILD] [-c:h CONF_HOST] [-l LOCKFILE]
                            [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                            [--lockfile-packages] [--lockfile-clean] [--check-updates]
                            [--filter FILTER] [--package-filter PACKAGE_FILTER] [--deploy DEPLOY]
                            [path]

    Computes the dependency graph and shows information about it

    positional arguments:
    path                  Path to a folder containing a recipe (conanfile.py or conanfile.txt) or
                            to a recipe file. e.g., ./my_project/conanfile.txt.

    optional arguments:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Select the output format: html, json, dot
    -v [V]                Level of detail of the output. Valid options from less verbose to more
                            verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or
                            -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.
    --name NAME           Provide a package name if not specified in conanfile
    --version VERSION     Provide a package version if not specified in conanfile
    --user USER           Provide a user if not specified in conanfile
    --channel CHANNEL     Provide a channel if not specified in conanfil
    --requires REQUIRES   Directly provide requires instead of a conanfile
    --tool-requires TOOL_REQUIRES
                            Directly provide tool-requires instead of a conanfile
    -b [BUILD], --build [BUILD]
                            Optional, specify which packages to build from source. Combining
                            multiple '--build' options on one command line is allowed. For
                            dependencies, the optional 'build_policy' attribute in their
                            conanfile.py takes precedence over the command line parameter. Possible
                            parameters: --build="*" Force build for all packages, do not use binary
                            packages. --build=never Disallow build for all packages, use binary
                            packages or fail if a binary package is not found. Cannot be combined
                            with other '--build' options. --build=missing Build packages from
                            source whose binary package is not found. --build=cascade Build
                            packages from source that have at least one dependency being built from
                            source. --build=[pattern] Build packages from source whose package
                            reference matches the pattern. The pattern uses 'fnmatch' style
                            wildcards. --build=![pattern] Excluded packages, which will not be
                            built from the source, whose package reference matches the pattern. The
                            pattern uses 'fnmatch' style wildcards. Default behavior: If you omit
                            the '--build' option, the 'build_policy' attribute in conanfile.py will
                            be used if it exists, otherwise the behavior is like '--build=never'.
    -r REMOTE, --remote REMOTE
                            Look in the specified remote or remotes server
    -u, --update          Will check the remote and in case a newer version and/or revision of
                            the dependencies exists there, it will install those in the local
                            cache. When using version ranges, it will install the latest version
                            that satisfies the range. Also, if using revisions, it will update to
                            the latest revision for the resolved version range.
    -o OPTIONS_HOST, --options OPTIONS_HOST
                            Define options values (host machine), e.g.: -o Pkg:with_qt=true
    -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                            Define options values (build machine), e.g.: -o:b Pkg:with_qt=true
    -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                            Define options values (host machine), e.g.: -o:h Pkg:with_qt=true
    -pr PROFILE_HOST, --profile PROFILE_HOST
                            Apply the specified profile to the host machine
    -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                            Apply the specified profile to the build machine
    -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                            Apply the specified profile to the host machine
    -s SETTINGS_HOST, --settings SETTINGS_HOST
                            Settings to build the package, overwriting the defaults (host machine).
                            e.g.: -s compiler=gcc
    -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                            Settings to build the package, overwriting the defaults (build
                            machine). e.g.: -s:b compiler=gcc
    -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                            Settings to build the package, overwriting the defaults (host machine).
                            e.g.: -s:h compiler=gcc
    -c CONF_HOST, --conf CONF_HOST
                            Configuration to build the package, overwriting the defaults (host
                            machine). e.g.: -c tools.cmake.cmaketoolchain:generator=Xcode
    -c:b CONF_BUILD, --conf:build CONF_BUILD
                            Configuration to build the package, overwriting the defaults (build
                            machine). e.g.: -c:b tools.cmake.cmaketoolchain:generator=Xcode
    -c:h CONF_HOST, --conf:host CONF_HOST
                            Configuration to build the package, overwriting the defaults (host
                            machine). e.g.: -c:h tools.cmake.cmaketoolchain:generator=Xcode
    -l LOCKFILE, --lockfile LOCKFILE
                            Path to a lockfile.
    --lockfile-partial    Do not raise an error if some dependency is not found in lockfile
    --lockfile-out LOCKFILE_OUT
                            Filename of the updated lockfile
    --lockfile-packages   Lock package-id and package-revision information
    --lockfile-clean      remove unused
    --check-updates
    --filter FILTER       Show only the specified fields
    --package-filter PACKAGE_FILTER
                            Print information only for packages that match the patterns
    --deploy DEPLOY       Deploy using the provided deployer to the output folder
