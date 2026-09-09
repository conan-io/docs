# conan graph build-order

```text
$ conan graph build-order -h
usage: conan graph build-order [-h] [-f FORMAT] [--out-file OUT_FILE]
                               [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                               [-cc CORE_CONF] [-b BUILD] [-r REMOTE | -nr]
                               [-u [UPDATE]] [-pr PROFILE]
                               [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                               [-pr:a PROFILE_ALL] [-o OPTIONS]
                               [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                               [-o:a OPTIONS_ALL] [-s SETTINGS]
                               [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                               [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                               [-c:h CONF_HOST] [-c:a CONF_ALL]
                               [--requires REQUIRES]
                               [--tool-requires TOOL_REQUIRES] [--name NAME]
                               [--version VERSION] [--user USER]
                               [--channel CHANNEL] [-l LOCKFILE]
                               [--lockfile-partial]
                               [--lockfile-out LOCKFILE_OUT]
                               [--lockfile-clean]
                               [--lockfile-overrides LOCKFILE_OVERRIDES]
                               [--order-by {recipe,configuration}] [--reduce]
                               [path]

Compute the build order of a dependency graph.

positional arguments:
  path                  Path to a folder containing a recipe (conanfile.py or
                        conanfile.txt) or to a recipe file. e.g.,
                        ./my_project/conanfile.txt. Defaults to the current
                        directory when no --requires or --tool-requires is
                        given

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Select the output format: json, html
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
  --order-by {recipe,configuration}
                        Select how to order the output, "recipe" by default if
                        not set.
  --reduce              Reduce the build order, output only those to build.
                        Use this only if the result will not be merged later
                        with other build-order

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

The `conan graph build-order` command computes the build order of the dependency graph for the recipe specified in `path` or in `--requires/--tool-requires`.

There are 2 important arguments that affect how this build order is computed:

- The `--order-by` argument can take 2 values `recipe` and `configuration`, depending how we want to
  structure and parallelize our CI.
- The `--reduce` argument will strip all packages in the order that doesn’t need to be built from source.

By default, the `conan graph build-order` will return the order for the full dependency graph, and it will annotate
in each element what needs to be done, for example `"binary": "Cache"` if the binary is already in the Conan Cache
and it doesn’t need to be built from source, and `"binary": "Build"`, if it needs to be built from source.
Having the full order is necessary if we want to `conan graph build-order-merge` several build-orders into a single
one later, because having the full information allows to preserve the relative order that would otherwise be lost and
broken.
Consequently, the `--reduce` argument should only be used when we are directly going to use the result to do the
build, but not if we plan to later do a merge of the resulting build-order with other ones.

Let’s consider installing libpng and wanting to see the build order for this requirement ordered by recipe:

#### WARNING
Please be aware that starting with Conan 2.1.0, using the –order-by argument is
recommended, and its absence is deprecated. This argument will be removed in the near
future. It is maintained for backward compatibility. Note that the JSON output will
differ if you use the –order-by argument, changing from a simple list to a
dictionary with extended information.

```text
$ conan graph build-order --requires=libpng/1.5.30 --format=json --order-by=recipe
...
======== Computing the build order ========
{
    "order_by": "recipe",
    "reduced": false,
    "order": [
        [
            {
                "ref": "zlib/1.3#06023034579559bb64357db3a53f88a4",
                "depends": [],
                "packages": [
                    [
                        {
                            "package_id": "d62dff20d86436b9c58ddc0162499d197be9de1e",
                            "prev": "54b9c3efd9ddd25eb6a8cbf01860b499",
                            "context": "host",
                            "binary": "Cache",
                            "options": [],
                            "filenames": [],
                            "depends": [],
                            "overrides": {},
                            "build_args": null
                        }
                    ]
                ]
            }
        ],
        [
            {
                "ref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b",
                "depends": [
                    "zlib/1.3#06023034579559bb64357db3a53f88a4"
                ],
                "packages": [
                    [
                        {
                            "package_id": "60778dfa43503cdcda3636d15124c19bf6546ae3",
                            "prev": "ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                            "context": "host",
                            "binary": "Download",
                            "options": [],
                            "filenames": [],
                            "depends": [],
                            "overrides": {},
                            "build_args": null
                        }
                    ]
                ]
            }
        ]
    ],
    "profiles": {
        "self": {
            "args": ""
        }
    }
}
```

Firstly, we can see the `zlib` package, as `libpng` depends on it. The output is sorted by
recipes as we passed with the –order-by argument; however, we might prefer to see it
sorted by configurations instead. For that purpose use the –order-by argument with
value configuration.

At the end of the json, after the `order` field, we see a `profiles` field, which contains the profile related command line arguments for the current “build-order”. As in this case we didn’t provide any arguments, it is empty. But if we used something like `conan graph build-order ... -pr=default -s build_type=Debug > bo.json`, the `args` will contain those arguments (with json character escaping): `"args": "-pr:h=\"default\" -s:h=\"build_type=Debug\""`

Using `--order-by=configuration` we will get a different build-order format:

```text
$ conan graph build-order --requires=libpng/1.5.30 --format=json --order-by=configuration
...
======== Computing the build order ========
{
    "order_by": "configuration",
    "reduced": false,
    "order": [
        [
            {
                "ref": "zlib/1.3#06023034579559bb64357db3a53f88a4",
                "pref": "zlib/1.3#06023034579559bb64357db3a53f88a4:d62dff20d86436b9c58ddc0162499d197be9de1e#54b9c3efd9ddd25eb6a8cbf01860b499",
                "package_id": "d62dff20d86436b9c58ddc0162499d197be9de1e",
                "prev": "54b9c3efd9ddd25eb6a8cbf01860b499",
                "context": "host",
                "binary": "Cache",
                "options": [],
                "filenames": [],
                "depends": [],
                "overrides": {},
                "build_args": null
            }
        ],
        [
            {
                "ref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b",
                "pref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b:60778dfa43503cdcda3636d15124c19bf6546ae3#ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                "package_id": "60778dfa43503cdcda3636d15124c19bf6546ae3",
                "prev": "ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                "context": "host",
                "binary": "Download",
                "options": [],
                "filenames": [],
                "depends": [
                    "zlib/1.3#06023034579559bb64357db3a53f88a4:d62dff20d86436b9c58ddc0162499d197be9de1e#54b9c3efd9ddd25eb6a8cbf01860b499"
                ],
                "overrides": {},
                "build_args": null
            }
        ]
    ]
}
```

If we now apply the `--reduce`:

```text
$ conan graph build-order --requires=libpng/1.5.30 --reduce --format=json --order-by=configuration
...
======== Computing the build order ========
{
    "order_by": "configuration",
    "reduced": false,
    "order": []
}
```

As there are no binaries to build here, all binaries already exist. If we explicitly force to build some,
the result would be only those that are going to be built:

```text
$ conan graph build-order --requires=libpng/1.5.30 --build="libpng/*" --reduce --format=json --order-by=configuration
...
======== Computing the build order ========
{
    "order_by": "configuration",
    "reduced": false,
    "order": [
        [
            {
                "ref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b",
                "pref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b:60778dfa43503cdcda3636d15124c19bf6546ae3#ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                "package_id": "60778dfa43503cdcda3636d15124c19bf6546ae3",
                "prev": null,
                "context": "host",
                "binary": "Build",
                "options": [],
                "filenames": [],
                "depends": [],
                "overrides": {},
                "build_args": "--require=libpng/1.5.30 --build=libpng/1.5.30"
            }
        ]
    ]
}
```

Then it will contain exclusively the `binary=Build` nodes, but not the rest.
Note that it will also provide a `build_args` field with the arguments needed for a `conan install <args>` to fire the build of this package
in the CI agent.

**Getting a visual representation of the Build Order**

You can obtain a visual representation of the build order by using the HTML formatter. For example:

```text
$ conan graph build-order --requires=opencv/4.9.0 --order-by=recipe --build=missing --format=html > build-order.html
```

![image](images/conan-build-order-html.png)
