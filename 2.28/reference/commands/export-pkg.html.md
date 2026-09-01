<a id="reference-commands-export-pkg"></a>

# conan export-pkg

```text
$ conan export-pkg -h
usage: conan export-pkg [-h] [-f FORMAT] [--out-file OUT_FILE]
                        [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                        [-cc CORE_CONF] [-of OUTPUT_FOLDER] [--build-require]
                        [-tf TEST_FOLDER] [-sb] [-r REMOTE | -nr]
                        [--name NAME] [--version VERSION] [--user USER]
                        [--channel CHANNEL] [-l LOCKFILE] [--lockfile-partial]
                        [--lockfile-out LOCKFILE_OUT] [--lockfile-clean]
                        [--lockfile-overrides LOCKFILE_OVERRIDES]
                        [-pr PROFILE] [-pr:b PROFILE_BUILD]
                        [-pr:h PROFILE_HOST] [-pr:a PROFILE_ALL] [-o OPTIONS]
                        [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                        [-o:a OPTIONS_ALL] [-s SETTINGS] [-s:b SETTINGS_BUILD]
                        [-s:h SETTINGS_HOST] [-s:a SETTINGS_ALL] [-c CONF]
                        [-c:b CONF_BUILD] [-c:h CONF_HOST] [-c:a CONF_ALL]
                        [path]

Create a package directly from pre-compiled binaries.

positional arguments:
  path                  Path to a folder containing a recipe (conanfile.py).
                        Defaults to current directory

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
  -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        The root output folder for generated and build files
  --build-require       Whether the provided reference is a build-require
  -tf TEST_FOLDER, --test-folder TEST_FOLDER
                        Alternative test folder name. By default it is
                        "test_package". Use "" to skip the test stage
  -sb, --skip-binaries  Skip installing dependencies binaries
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache

reference arguments:
  --name NAME           Provide a package name if not specified in conanfile
  --version VERSION     Provide a package version if not specified in
                        conanfile
  --user USER           Provide a user if not specified in conanfile
  --channel CHANNEL     Provide a channel if not specified in conanfile

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

```

The `conan export-pkg` command creates a package binary directly from pre-compiled binaries in a user folder. This command can be useful in different cases:

- When creating a package for some closed source or pre-compiled binaries provided by a vendor. In this case, it is not necessary that the `conanfile.py` recipe contains a `build()` method, and providing the `package()` and `package_info()` method are enough to package those pre-compiled binaries. In this case the `build_policy = "never"` could make sense to indicate it is not possible to `conan install --build=this_pkg`, as it doesn’t know how to build from sources when it is a dependency.
- When testing some recipe locally in the [local development flow](https://docs.conan.io/2//tutorial/developing_packages/local_package_development_flow.html.md#local-package-development-flow), it can be used to quickly put the locally built binaries in the cache to make them available to other packages for testing, without needing to go through a full `conan create` that would be slower.

In general, it is expected that when `conan export-pkg` executes, the possible Conan dependencies that were necessary to build this package had already been installed via `conan install`, so it is not necessary to download dependencies at `export-pkg` time. But if for some reason this is not the case, the command defines `--remote` and `--no-remote` arguments, similar to other commands, as well as the `--skip-binaries` optimization that could save some time installing dependencies binaries if they are not strictly necessary for the current `export-pkg`. But this is the responsibility of the user, as it is possible that such binaries are actually necessary, for example, if a `tool_requires = "cmake/x.y"` is used and the `package()` method implements a `cmake.install()` call, this will definitely need the binaries for the dependencies installed in the current machine to execute.

The `conan export-pkg` is a package creation command, it will create both a new recipe and a new package binary, in the same way that the `conan create` command does.
Similarly, it will run after the creation of the package any “test-package” functionality. If there is a `test_package` folder besides the `conanfile.py`, or a different test-package folder is defined via the `--test-folder/-tf` argument or in the recipe `test_package_folder` attribute, then, such test-package will be triggered to test and validate that the created package is usable by the simple consumer project in the test-package folder.

#### SEE ALSO
- Check the [JSON format output](https://docs.conan.io/2//reference/commands/formatters/graph_info_json_formatter.html.md#reference-commands-graph-info-json-format) for this command.
- Read the tutorial about the [local package development flow](https://docs.conan.io/2//tutorial/developing_packages/local_package_development_flow.html.md#local-package-development-flow).
