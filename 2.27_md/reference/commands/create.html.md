<a id="reference-commands-create"></a>

# conan create

```text
$ conan create -h
usage: conan create [-h] [-f FORMAT] [--out-file OUT_FILE]
                    [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                    [-cc CORE_CONF] [--name NAME] [--version VERSION]
                    [--user USER] [--channel CHANNEL] [-l LOCKFILE]
                    [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                    [--lockfile-clean]
                    [--lockfile-overrides LOCKFILE_OVERRIDES] [-b BUILD]
                    [-r REMOTE | -nr] [-u [UPDATE]] [-pr PROFILE]
                    [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                    [-pr:a PROFILE_ALL] [-o OPTIONS] [-o:b OPTIONS_BUILD]
                    [-o:h OPTIONS_HOST] [-o:a OPTIONS_ALL] [-s SETTINGS]
                    [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                    [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                    [-c:h CONF_HOST] [-c:a CONF_ALL] [--build-require]
                    [-tf TEST_FOLDER] [-tm] [-bt BUILD_TEST]
                    [path]

Create a package.

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
  --build-require       Whether the package being created is a build-require
                        (to be used as tool_requires() by other packages)
  -tf TEST_FOLDER, --test-folder TEST_FOLDER
                        Alternative test folder name. By default it is
                        "test_package". Use "" to skip the test stage
  -tm, --test-missing   Run the test_package checks only if the package is
                        built from source but not if it already existed (using
                        --build=missing)
  -bt BUILD_TEST, --build-test BUILD_TEST
                        Same as '--build' but only for the test_package
                        requires. By default if not specified it will take the
                        '--build' value if specified

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

```

The `conan create` command creates a package from the recipe specified in `path`.

This command will first **export** the recipe to the local cache and then build
and create the package. If a `test_package` folder (you can change the folder name with
the `-tf` argument or with the `test_package_folder` recipe attribute) is found, the command will run the consumer project to ensure that
the package has been created correctly. Check [testing Conan packages](https://docs.conan.io/2//tutorial/creating_packages/test_conan_packages.html.md#tutorial-creating-test) section to know more about how to test your Conan packages.

## Using conan create with build requirements

The `--build-require` argument allows to create the package using the configuration and
settings of the “build” context, as it was a `build_require`. This feature allows to
create packages in a way that is consistent with the way they will be used later.

```bash
$ conan create . --name=cmake --version=3.23.1 --build-require
```

## Conan create output

The `conan create ... --format=json` creates a json output containing the full dependency graph information.
This json is the same as the one created with `conan graph info` (see the [graph info json format](https://docs.conan.io/2//reference/commands/formatters/graph_info_json_formatter.html.md#reference-commands-graph-info-json-format))
with extended information about the binaries, like a more complete `cpp_info` field.
This resulting json is the dependency graph of the package recipe being created, excluding all the `test_package` and other possible dependencies of the `test_package/conanfile.py`. These dependencies only exist in the `test_package` functionality, and as such, are not part of the “main” product or package. If you are interested in capturing the dependency graph including the `test_package` (most likely not necessary in most cases), then you can do it running the `conan test` command separately.

The same happens for lockfiles created with `--lockfile-out` argument. The lockfile will only contain the created package and its transitive dependencies versions, but it will not contain the `test_package` or the transitive dependencies of the `test_package/conanfile.py`. It is possible to capture a lockfile which includes those with the `conan test` command (though again, this might not be really necessary)

#### NOTE
**Best practice**

In general, having `test_package/conanfile.py` with dependencies other than the tested
one should be avoided. The `test_package` functionality should serve as a simple check
to ensure the package is correctly created. Adding extra dependencies to
`test_package` might indicate that the check is not straightforward or that its
functionality is being misused. If, for any reason, your `test_package` has additional
dependencies, you can control their build using the `--build-test` argument.

## Methods execution order

The `conan create` executes [methods](https://docs.conan.io/2//reference/conanfile/methods.html.md#reference-conanfile-methods) of a *conanfile.py* in the following order:

1. Export recipe to the cache
   : 1. `init()`
     2. `set_name()`
     3. `set_version()`
     4. `export()`
     5. `export_sources()`
2. Compute dependency graph
   : 1. `ìnit()`
     2. `config_options()`
     3. `configure()`
     4. `requirements()`
     5. `build_requirements()`
3. Compute necessary packages
   : 1. `validate_build()`
     2. `validate()`
     3. `package_id()`
     4. `layout()`
     5. `system_requirements()`
4. Install packages
   : 1. `source()`
     2. `build_id()`
     3. `generate()`
     4. `build()`
     5. `package()`
     6. `package_info()`

Steps `generate()`,  `build()`, `package()` from *Install packages* step will not be called if the package
is not being built from sources.

After that, if you have a folder named *test_package* in your project or you call the `conan create` command with the
`--test-folder` flag, the command will invoke the methods of the *conanfile.py* file inside the folder in the following order:

1. Launch test_package
   : 1. (test package) `init()`
     2. (test package) `set_name()`
     3. (test package) `set_version()`
2. Compute dependency graph
   : 1. (test package) `config_options()`
     2. (test package) `configure()`
     3. (test package) `requirements()`
     4. (test package) `build_requirements()`
     5. `ìnit()`
     6. `config_options()`
     7. `configure()`
     8. `requirements()`
     9. `build_requirements()`
3. Compute necessary packages
   : 1. `validate_build()`
     2. `validate()`
     3. `package_id()`
     4. `layout()`
     5. (test package) `validate_build()`
     6. (test package) `validate()`
     7. (test package) `package_id()`
     8. (test package) `layout()`
     9. `system_requirements()`
     10. (test package) `system_requirements()`
4. Install packages
   : 1. `build_id()`
     2. `generate()`
     3. `build()`
     4. `package_info()`
5. Test the package
   : 1. (test package) `build()`
     2. (test package) `test()`

The functions with  *(test package)* belong to the *conanfile.py* in the *test_package* folder. The steps
`build_id()`, `generate()`, `build()` inside the *Install packages* step will be skipped if the project is
already installed. Typically, it should be installed just as it was installed in the previous “install packages” step.

When using the `cmake_layout()` functionality inside `test_package`, the conf `tools.cmake.cmake_layout:test_folder` can be used
to define the location of the build artifacts for the `test_package`. See [cmake_layout() docs](https://docs.conan.io/2//reference/tools/cmake/cmake_layout.html.md#cmake-layout).
Likewise, the full path to the build artifacts will be defined by the `self.folders.build_folder_vars` attribute.

## Build modes

The `conan create --build=<xxxx>` build modes are very similar to the `conan install` ones documented in [Build Modes](https://docs.conan.io/2//reference/commands/install.html.md#reference-commands-build-modes),
with some differences.

By default, `conan create` defines the `--build=current_pkg/current_version` to force the build
from source for the current revision. This assumes that the source code (recipe, C/C++ code) was
changed and it will create a new revision. If that is not the case, then the `--build=missing:current_pkg/current_version`,
or `--build="missing:&"` would be recommended to avoid rebuilding from source an already existing binary.

When a `--build=xxx` argument is defined in the command line, then the automatically defined
`--build=current_pkg/current_version` is no longer passed, and it should be passed as a explicit argument too.

#### NOTE
**Best practices**

Having more than a `package_revision` for a given `recipe_revision` and `package_id` is discouraged
in most cases, as it implies unnecessarily rebuilding from sources binaries that were already existing. For that
reason, using `conan create` repeatedly over the same recipe without any source changes that would cause a
new `recipe_revision` is discouraged, and using `conan create . --build=missing:[pattern]` would be the
recommended approach.

#### SEE ALSO
- Read more about creating packages in the [dedicated
  tutorial](https://docs.conan.io/2//tutorial/creating_packages.html.md#tutorial-creating-packages)
- Read more about [testing Conan packages](https://docs.conan.io/2//tutorial/creating_packages/test_conan_packages.html.md#tutorial-creating-test)
