<a id="reference-commands-test"></a>

# conan test

```text
$ conan test -h
usage: conan test [-h] [-f FORMAT] [--out-file OUT_FILE]
                  [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                  [-cc CORE_CONF] [-b BUILD] [-r REMOTE | -nr] [-u [UPDATE]]
                  [-pr PROFILE] [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                  [-pr:a PROFILE_ALL] [-o OPTIONS] [-o:b OPTIONS_BUILD]
                  [-o:h OPTIONS_HOST] [-o:a OPTIONS_ALL] [-s SETTINGS]
                  [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                  [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                  [-c:h CONF_HOST] [-c:a CONF_ALL] [-l LOCKFILE]
                  [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                  [--lockfile-clean] [--lockfile-overrides LOCKFILE_OVERRIDES]
                  [path] reference

Test a package from a test_package folder.

positional arguments:
  path                  Path to a test_package folder containing a
                        conanfile.py. Defaults to a 'test_package' folder in
                        the current directory
  reference             Provide a package reference to test

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

remote arguments:
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -u [UPDATE], --update [UPDATE]
                        Will install newer versions and/or revisions in the
                        local cache for the given references whose name
                        matches the given pattern, or all references in the
                        graph if no argument is supplied. When using version
                        ranges, it will install the latest version that
                        satisfies the range. It will update to the latest
                        revision for the resolved version range. The consumer
                        pattern (&) has no effect, and users should not
                        specify versions.

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

The `conan test` command uses the *test_package* folder specified in `path` to tests the package reference specified in `reference`.

When using the `cmake_layout()` functionality inside `test_package`, the conf `tools.cmake.cmake_layout:test_folder` can be used
to define the location of the build artifacts for the `test_package`. See [cmake_layout() docs](https://docs.conan.io/2//reference/tools/cmake/cmake_layout.html.md#cmake-layout).
Likewise, the full path to the build artifacts will be defined by the `self.folders.build_folder_vars` attribute.

- **tools.cmake.cmake_layout:test_folder** (*new since Conan 2.2.0*)(*experimental*) uses its value as the base folder of the `conanfile.folders.build`
  for test_package builds. If that value is `$TMP`, Conan will create and use a temporal folder.

#### SEE ALSO
- Read the tutorial about [testing Conan packages](https://docs.conan.io/2//tutorial/creating_packages/test_conan_packages.html.md#tutorial-creating-test).
