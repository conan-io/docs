<a id="reference-commands-install"></a>

# conan install

```text
$ conan install -h
usage: conan install [-h] [-f FORMAT] [--out-file OUT_FILE]
                     [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                     [-cc CORE_CONF] [-b BUILD] [-r REMOTE | -nr]
                     [-u [UPDATE]] [-pr PROFILE] [-pr:b PROFILE_BUILD]
                     [-pr:h PROFILE_HOST] [-pr:a PROFILE_ALL] [-o OPTIONS]
                     [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                     [-o:a OPTIONS_ALL] [-s SETTINGS] [-s:b SETTINGS_BUILD]
                     [-s:h SETTINGS_HOST] [-s:a SETTINGS_ALL] [-c CONF]
                     [-c:b CONF_BUILD] [-c:h CONF_HOST] [-c:a CONF_ALL]
                     [--requires REQUIRES] [--tool-requires TOOL_REQUIRES]
                     [--name NAME] [--version VERSION] [--user USER]
                     [--channel CHANNEL] [-l LOCKFILE] [--lockfile-partial]
                     [--lockfile-out LOCKFILE_OUT] [--lockfile-clean]
                     [--lockfile-overrides LOCKFILE_OVERRIDES] [-g GENERATOR]
                     [-of OUTPUT_FOLDER] [-d DEPLOYER]
                     [--deployer-folder DEPLOYER_FOLDER]
                     [--deployer-package DEPLOYER_PACKAGE] [--build-require]
                     [--envs-generation {false}]
                     [path]

Install the requirements specified in a recipe (conanfile.py or conanfile.txt).

It can also be used to install packages without a conanfile, using the
--requires and --tool-requires arguments.

If any requirement is not found in the local cache, it will iterate the remotes
looking for it. When the full dependency graph is computed, and all dependencies
recipes have been found, it will look for binary packages matching the current settings.
If no binary package is found for some or several dependencies, it will error,
unless the '--build' argument is used to build it from source.

After installation of packages, the generators and deployers will be called.

positional arguments:
  path                  Path to a folder containing a recipe (conanfile.py or
                        conanfile.txt) or to a recipe file. e.g.,
                        ./my_project/conanfile.txt. Defaults to the current
                        directory when no --requires or --tool-requires is
                        given

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
  --requires REQUIRES   Directly provide requires instead of a conanfile
  --tool-requires TOOL_REQUIRES
                        Directly provide tool-requires instead of a conanfile
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
  --deployer-package DEPLOYER_PACKAGE
                        Execute the deploy() method of the packages matching
                        the provided patterns
  --build-require       Whether the provided path is a build-require
  --envs-generation {false}
                        Generation strategy for virtual environment files for
                        the root

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

```

The `conan install` command is one of the main Conan commands, and it is used to resolve and install dependencies.

This command does the following:

- Compute the whole dependency graph, for the current configuration defined by settings, options, profiles and configuration.
  It resolves version ranges, transitive dependencies, conditional requirements, etc, to build the dependency graph.
- Evaluate the existence of binaries for every package in the graph, whether or not there are precompiled binaries to download, or if
  they should be built from sources (as directed by the `--build` argument). If binaries are missing, it will not recompute
  the dependency graph to try to fallback to previous versions that contain binaries for that configuration. If a certain
  dependency version is desired, it should be explicitly required.
- Download precompiled binaries, or build binaries from sources in the local cache, in the right order for the dependency graph.
- Create the necessary files as requested by the “generators”, so build systems and other tools can locate the locally installed dependencies
- Optionally, execute the desired `deployers`.

#### SEE ALSO
- Check the [JSON format output](https://docs.conan.io/2//reference/commands/formatters/graph_info_json_formatter.html.md#reference-commands-graph-info-json-format) for this command.

## Conanfile path or –requires

The `conan install` command can use 2 different origins for information. The first one is using a local `conanfile.py`
or `conanfile.txt`, containing definitions of the dependencies and generators to be used.

```text
$ conan install .  # there is a conanfile.txt or a conanfile.py in the cwd
$ conan install conanfile.py  # also works, direct reference file
$ conan install myconan.txt  # explicit custom name
$ conan install myfolder  # there is a conanfile in "myfolder" folder
```

Even if it is possible to use a custom name, in the general case, it is recommended to use the default `conanfile.py`
name, located in the repository root, so users can do a straightforward `git clone ... `` + ``conan install .`

The other possibility is to not have a `conanfile` at all, and define the requirements to be installed directly in the
command line:

```text
# Install the zlib/1.2.13 library
$ conan install --requires=zlib/1.2.13
# Install the zlib/1.2.13 and bzip2/1.0.8 libraries
$ conan install --requires=zlib/1.2.13 --requires=bzip2/1.0.8
# Install the cmake/3.23.5 and ninja/1.11.0 tools
$ conan install --tool-requires=cmake/3.23.5 --tool-requires=ninja/1.11.0
# Install the zlib/1.2.13 library and ninja/1.11.0 tool
$ conan install --requires=zlib/1.2.13 --tool-requires=ninja/1.11.0
```

In the general case, it is recommended to use a `conanfile` instead of defining things in the command line.

<a id="reference-commands-install-composition"></a>

## Profiles, Settings, Options, Conf

There are several arguments that are used to define the effective profiles that will be used, both for the “build”
and “host” contexts.

By default the arguments refer to the “host” context, so `--settings:host, -s:h` is totally equivalent to
`--settings, -s`. Also, by default, the `conan install` command will use the `default` profile both for the
“build” and “host” context. That means that if a profile with the “default” name has not been created, it will error.

Multiple definitions of profiles can be passed as arguments, and they will compound from left to right (right has the
highest priority)

```text
# The values of myprofile3 will have higher priority
$ conan install . -pr=myprofile1 -pr=myprofile2 -pr=myprofile3
```

#### NOTE
Profiles are searched for in a variety of locations, [see here for more information](https://docs.conan.io/2//reference/config_files/profiles.html.md#reference-config-files-profiles-using-profiles)

If values for any of `settings`, `options` and `conf` are provided in the command line, they create a profile that
is composed with the other provided `-pr` (or the “default” one if not specified) profiles, with higher priority,
not matter what the order of arguments is.

```text
# the final "host" profile will always be build_type=Debug, even if "myprofile"
# says "build_type=Release"
$ conan install . -pr=myprofile -s build_type=Debug
```

<a id="reference-commands-install-generators-deployers"></a>

## Generators and deployers

The `-g` argument allows to define in the command line the different built-in generators to be used:

```text
$ conan install --requires=zlib/1.2.13 -g CMakeDeps -g CMakeToolchain
```

Note that in the general case, the recommended approach is to have the `generators` defined in the `conanfile`,
and only for the `--requires` use case, it would be more necessary as command line argument.

Generators are intended to create files for the build systems to locate the dependencies, while the `deployers`
main use case is to copy files from the Conan cache to user space, and performing any other custom operations over the dependency graph,
like collecting licenses, generating reports, deploying binaries to the system, etc. The syntax for deployers is:

```text
# does a full copy of the dependencies binaries to the current user folder
$ conan install . --deployer=full_deploy
```

There are 3 built-in deployers:

- [full_deploy](https://docs.conan.io/2//reference/extensions/deployers.html.md#reference-extensions-deployer-full-deploy) does a complete copy of the dependencies binaries in the local folder, with a minimal folder
  structure to avoid conflicts between files and artifacts of different packages
- [direct_deploy](https://docs.conan.io/2//reference/extensions/deployers.html.md#reference-extensions-deployer-direct-deploy) does a copy of only the immediate direct dependencies, but does not include the transitive
  dependencies.
- [runtime_deploy](https://docs.conan.io/2//reference/extensions/deployers.html.md#reference-extensions-deployer-runtime-deploy) deploys all the shared libraries and the executables of the
  dependencies into a flat directory structure, preserving subdirectories as-is.

Some generators might have the capability of redefining the target “package folder”. That means that if some other
generator like `CMakeDeps` is used that is pointing to the packages, it will be pointing to the local deployed
copy, and not to the original packages in the Conan cache. See the full example in [Creating a Conan-agnostic deploy of dependencies for developer use](https://docs.conan.io/2//examples/extensions/deployers/dev/development_deploy.html.md#examples-extensions-builtin-deployers-development).

It is also possible, and it is a powerful extension point, to write custom user deployers.
Read more about custom deployers in [Deployers](https://docs.conan.io/2//reference/extensions/deployers.html.md#reference-extensions-deployers).

It is possible to also invoke the package recipes `deploy()` method with the `--deployer-package`:

```bash
# Execute deploy() method of every recipe that defines it
$ conan install --requires=pkg/0.1 --deployer-package="*"
# Execute deploy() method only for "pkg" (any version) recipes
$ conan install --requires=pkg/0.1 --deployer-package="pkg/*"
# Execute deploy() method for all packages except the "zlib" (transitive dep) one
$ conan install --requires=pkg/0.1 --deployer-package="*" --deployer-package="~zlib/*"
```

The `--deployer-package` argument is a pattern and accepts multiple values, all package references matching any of the defined patterns will execute its `deploy()` method.
This includes negated patterns, where for example `--deployer-package=~pkg/*` will execute the `deploy()` method for all packages except for that of the `pkg` recipe.
The `--deployer-folder` argument will also affect the output location of this deployment. See the [deploy() method](https://docs.conan.io/2//reference/conanfile/methods/deploy.html.md#reference-conanfile-methods-deploy).

If multiple deployed packages deploy to the same location, it is their responsibility to not mutually overwrite their binaries if they have the same filenames. For example if multiple packages `deploy()` a file called “License.txt”, each recipe is responsible for creating an intermediate folder with the package name and/or version that makes it unique, so other recipes `deploy()` method do not overwrite previously deployed “License.txt” files.

## Name, version, user, channel

The `conan install` command provides optional arguments for `--name, --version, --user, --channel`. These
arguments might not be necessary in the majority of cases. Never for `conanfile.txt` and for `conanfile.py`
only in the case that they are not defined in the recipe:

```python
from conan import ConanFile
from conan.tools.scm import Version

class Pkg(ConanFile):
    name = "mypkg"

    def requirements(self):
        if Version(self.version) >= "3.23":
            self.requires("...")
```

```text
# If we don't specify ``--version``, it will be None and it will fail
$ conan install . --version=3.24
```

## Lockfiles

The `conan install` command has several arguments to load and produce lockfiles.
By default, if a `conan.lock` file is located beside the recipe or in the current working directory
if no path is provided, will be used as an input lockfile.

Lockfiles are strict by default, that means that
if there is some `requires` and it cannot find a matching locked reference in the lockfile, it will error
and stop. For cases where it is expected that the lockfile will not be complete, as there might be new
dependencies, the `--lockfile-partial` argument can be used.

By default, `conan install` will not generate an output lockfile, but if the `--lockfile-out` argument
is provided, pointing to a filename, like `--lockfile-out=result.lock`, then a lockfile will be generated
from the current dependency graph. If `--lockfile-clean` argument is provided, all versions and revisions
not used in the current dependency graph will be dropped from the resulting lockfile.

Let’s say that we already have a `conan.lock` input lockfile, but we just added a new `requires = "newpkg/1.0"`
to a new dependency. We could resolve the dependencies, locking all the previously locked versions, while allowing
to resolve the new one, which was not previously present in the lockfile, and store it in a new location, or overwrite the existing lockfile:

```text
# --lockfile=conan.lock is the default, not necessary
$ conan install . --lockfile=conan.lock --lockfile-partial --lockfile-out=conan.lock
```

Also, it is likely that the majority of lockfile operations are better managed by the `conan lock` command.

#### SEE ALSO
- [Lockfiles](https://docs.conan.io/2//tutorial/consuming_packages/intro_to_versioning.html.md#tutorial-consuming-packages-versioning-lockfiles).
- Read the tutorial about the [local package development flow](https://docs.conan.io/2//tutorial/developing_packages/local_package_development_flow.html.md#local-package-development-flow).

## Update

The `conan install` command has an `--update` argument that will force the re-evaluation of the selected items of the dependency graph,
allowing for the update of the dependencies to the latest version if using version ranges, or to the latest revision of the same version,
when those versions are not locked in the given lockfile. Passing `--update` will check every package in the dependency graph,
but it is also possible to pass a package name to the `--update` argument (it can be added to the command more than once with different names),
to only update those packages, which avoids the re-evaluation of the whole graph.

```bash
$ conan install . --update  # Update all packages in the graph
$ conan install . --update=openssl  # Update only the openssl package
$ conan install . --update=openssl --update=boost  # Update both openssl and boost packages
```

Note that the `--update` argument will look into all the remotes specified in the command for possible newer versions,
and won’t stop at the first newer one found.

<a id="reference-commands-build-modes"></a>

## Build modes

The `conan install --build=<mode>` argument controls the behavior regarding building packages from source.
The default behavior is failing if there are no existing binaries, with the “missing binary” error message,
except for packages that define a `build_policy = "missing"` policy, but this can be changed with the
`--build` argument.

The possible values are:

```bash
--build=never      Disallow build for all packages, use binary packages or fail if a binary
                   package is not found, it cannot be combined with other '--build' options.
--build=missing    Build packages from source whose binary package is not found.
--build=cascade    Build packages from source that have at least one dependency being built from
                   source.
--build=[pattern]  Build packages from source whose package reference matches the pattern. The
                   pattern uses 'fnmatch' style wildcards, so '--build="*"' will build everything
                   from source.
--build=~[pattern] Excluded packages, which will not be built from the source, whose package
                   reference matches the pattern. The pattern uses 'fnmatch' style wildcards.
--build=missing:[pattern] Build from source if a compatible binary does not exist, only for
                          packages matching pattern.
--build=compatible:[pattern] (Experimental) Build from source if a compatible binary does not
                             exist, and the requested package is invalid, the closest package
                             binary following the defined compatibility policies (method and
                             compatibility.py)
```

The `--build=never` policy can be used to force never building from source, even for package recipes
that define the `build_policy = "missing"` policy.

The `--build=compatible:[pattern]` is an **experimental** new mode that allows building missing binaries
with a configuration different than the current one. For example if the current profile has
`compiler.cppstd=14`, but some package raises an “invalid” configuration error, because it needs at
least `compiler.cppstd=17`, and the binary compatibiliy (defined for example in `compatibility.py` plugin)
allows that as a compatible binary, then, Conan will build from source that dependency package applying
`compiler.cppstd=17`.

The `--build=[pattern]` uses a pattern, so it should use something like `--build="zlib/*"` to match any
version of the `zlib` package, as doing `--build=zlib` will not work.

The `--build=missing:[pattern]` form uses the same kind of package patterns as
in [Profile patterns](https://docs.conan.io/2//reference/config_files/profiles.html.md#reference-config-files-profile-patterns)
(`fnmatch`-style wildcards, references like `name/version@user/channel`,
etc.). Also, you can use the `&` syntax to match the **consumer** conanfile
(the root of the graph). That is useful with `conan create .` when you only
want to build the package being created if its binary is missing, without
retyping its name: `--build=missing:&` (equivalent to
`--build=missing:current_pkg/current_version` in the case of `conan create .`).

#### NOTE
**Best practices**

Forcing the rebuild of existing binaries with `--build="*"` or any other `--build="pkg/*"` or
similar pattern is not a recommended practice. If a binary is already existing there is no reason
to rebuild it from source. CI pipelines should be specially careful to not do this, and in general
the `--build=missing` and `--build=missing:[pattern]` are more recommended.

The `--build=cascade` mode is partly legacy, and shouldn’t be used in most cases. The `package_id`
computation should be the driver to decide what needs to be built. This mode has been left in Conan 2
only for exceptional cases, like recovering from broken systems, but it is not recommended for normal
production usage.
