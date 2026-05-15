<a id="reference-commands-build"></a>

# conan build

```text
$ conan build -h
usage: conan build [-h] [-f FORMAT] [--out-file OUT_FILE]
                   [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                   [-cc CORE_CONF] [--name NAME] [--version VERSION]
                   [--user USER] [--channel CHANNEL] [-g GENERATOR]
                   [-of OUTPUT_FOLDER] [-d DEPLOYER]
                   [--deployer-folder DEPLOYER_FOLDER] [--build-require]
                   [--envs-generation {false}] [-b BUILD] [-r REMOTE | -nr]
                   [-u [UPDATE]] [-pr PROFILE] [-pr:b PROFILE_BUILD]
                   [-pr:h PROFILE_HOST] [-pr:a PROFILE_ALL] [-o OPTIONS]
                   [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST] [-o:a OPTIONS_ALL]
                   [-s SETTINGS] [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                   [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                   [-c:h CONF_HOST] [-c:a CONF_ALL] [-l LOCKFILE]
                   [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                   [--lockfile-clean]
                   [--lockfile-overrides LOCKFILE_OVERRIDES]
                   [path]

Install dependencies and call the build() method.

positional arguments:
  path                  Path to a python-based recipe file or a folder
                        containing a conanfile.py recipe. conanfile.txt cannot
                        be used with conan build. Defaults to current
                        directory

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Select the output format: json
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True
  -g GENERATOR, --generator GENERATOR
                        Generators to use
  -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        The root output folder for generated and build files
  -d DEPLOYER, --deployer DEPLOYER
                        Deploy using the provided deployer to the output
                        folder. Built-in deployers: 'full_deploy',
                        'direct_deploy', 'runtime_deploy'
  --deployer-folder DEPLOYER_FOLDER
                        Deployer output folder, base build folder by default
                        if not set
  --build-require       Whether the provided path is a build-require
  --envs-generation {false}
                        Generation strategy for virtual environment files for
                        the root
  -b BUILD, --build BUILD
                        Optional, specify which packages to build from source.
                        Combining multiple '--build' options on one command
                        line is allowed. Possible values: --build=never
                        Disallow build for all packages, use binary packages
                        or fail if a binary package is not found, it cannot be
                        combined with other '--build' options. --build=missing
                        Build packages from source whose binary package is not
                        found. --build=cascade Build packages from source that
                        have at least one dependency being built from source.
                        --build=[pattern] Build packages from source whose
                        package reference matches the pattern. The pattern
                        uses 'fnmatch' style wildcards, so '--build="*"' will
                        build everything from source. --build=~[pattern]
                        Excluded packages, which will not be built from the
                        source, whose package reference matches the pattern.
                        The pattern uses 'fnmatch' style wildcards.
                        --build=missing:[pattern] Build from source if a
                        compatible binary does not exist, only for packages
                        matching pattern. --build=compatible:[pattern]
                        (Experimental) Build from source if a compatible
                        binary does not exist, and the requested package is
                        invalid, the closest package binary following the
                        defined compatibility policies (method and
                        compatibility.py)

reference arguments:
  --name NAME           Provide a package name if not specified in conanfile
  --version VERSION     Provide a package version if not specified in
                        conanfile
  --user USER           Provide a user if not specified in conanfile
  --channel CHANNEL     Provide a channel if not specified in conanfile

remote arguments:
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -u [UPDATE], --update [UPDATE]
                        Will install newer versions and/or revisions in the
                        local cache for the given reference name, or all
                        references in the graph if no argument is supplied.
                        When using version ranges, it will install the latest
                        version that satisfies the range. It will update to
                        the latest revision for the resolved version range.

profile arguments:
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
                        both contexts at once. Example:
                        -o="pkg/*:with_qt=True"
  -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
  -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
  -o:a OPTIONS_ALL, --options:all OPTIONS_ALL
  -s SETTINGS, --settings SETTINGS
                        Apply the specified settings. By default, or if
                        specifying -s:h (--settings:host), it applies to the
                        host context. Use -s:b (--settings:build) to specify
                        the build context, or -s:a (--settings:all) to specify
                        both contexts at once. Example: -s="compiler=gcc"
  -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
  -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
  -s:a SETTINGS_ALL, --settings:all SETTINGS_ALL
  -c CONF, --conf CONF  Apply the specified conf. By default, or if specifying
                        -c:h (--conf:host), it applies to the host context.
                        Use -c:b (--conf:build) to specify the build context,
                        or -c:a (--conf:all) to specify both contexts at once.
                        Example:
                        -c="tools.cmake.cmaketoolchain:generator=Xcode"
  -c:b CONF_BUILD, --conf:build CONF_BUILD
  -c:h CONF_HOST, --conf:host CONF_HOST
  -c:a CONF_ALL, --conf:all CONF_ALL

lockfile arguments:
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile. Use --lockfile="" to avoid
                        automatic use of existing 'conan.lock' file
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile
  --lockfile-out LOCKFILE_OUT
                        Filename of the updated lockfile
  --lockfile-clean      Remove unused entries from the lockfile
  --lockfile-overrides LOCKFILE_OVERRIDES
                        Overwrite lockfile overrides

```

The `conan build` command installs the recipe specified in `path` and calls its `build()` method.

#### SEE ALSO
- Read the tutorial about the [local package development flow](https://docs.conan.io/2//tutorial/developing_packages/local_package_development_flow.html.md#local-package-development-flow).
