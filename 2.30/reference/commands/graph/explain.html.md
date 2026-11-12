<a id="reference-graph-explain"></a>

# conan graph explain

```text
$ conan graph explain -h
usage: conan graph explain [-h] [-f FORMAT] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF] [-b BUILD] [-r REMOTE | -nr]
                           [-u [UPDATE]] [-pr PROFILE] [-pr:b PROFILE_BUILD]
                           [-pr:h PROFILE_HOST] [-pr:a PROFILE_ALL]
                           [-o OPTIONS] [-o:b OPTIONS_BUILD]
                           [-o:h OPTIONS_HOST] [-o:a OPTIONS_ALL]
                           [-s SETTINGS] [-s:b SETTINGS_BUILD]
                           [-s:h SETTINGS_HOST] [-s:a SETTINGS_ALL] [-c CONF]
                           [-c:b CONF_BUILD] [-c:h CONF_HOST] [-c:a CONF_ALL]
                           [--requires REQUIRES]
                           [--tool-requires TOOL_REQUIRES] [--name NAME]
                           [--version VERSION] [--user USER]
                           [--channel CHANNEL] [-l LOCKFILE]
                           [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                           [--lockfile-clean]
                           [--lockfile-overrides LOCKFILE_OVERRIDES]
                           [--check-updates] [--build-require]
                           [--missing [MISSING]]
                           [path]

Explain what is wrong with the dependency graph, like report missing binaries
closest alternatives, trying to explain why the existing binaries do not match

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
  --check-updates       Check if there are recipe updates
  --build-require       Whether the provided reference is a build-require
  --missing [MISSING]   A pattern in the form
                        'pkg/version#revision:package_id#revision', e.g:
                        "zlib/1.2.13:*" means all binaries for zlib/1.2.13. If
                        revision is not specified, it is assumed latest one.

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

The `conan graph explain` tries to give a more detailed explanation for a package that might be missing with the configuration provided and show the differences between the expected binary package and the available ones.
It helps to understand what is missing from the package requested, whether it is different options, different settings or different dependencies.

**Example**:

Imagine that we want to install the lib/1.0.0 that depends on dep/2.0.0 but we don’t have a binary yet, as the latest CI run only generated a binary for lib/1.0.0 using the previous version of dep.
When we try to install the refere lib/1.0.0 it says:

```text
$ conan install --requires=lib/1.0.0
...
ERROR: Missing prebuilt package for 'lib/1.0.0'
```

Now we can try to find a explanation for this:

```text
$ conan graph explain --requires=lib/1.0.0
requires: dep/1.Y.Z
diff
  dependencies
    expected: dep/2.Y.Z
    existing: dep/1.Y.Z
    explanation: This binary has same settings and options, but different dependencies
```

In the same way, it can report when a package has a different option value and the output is also available in JSON format:

```text
$conan graph explain --requires=lib/1.0.0 -o lib/*:shared=True --format=json
...
{
    "closest_binaries": {
        "lib/1.0.0": {
            "revisions": {
                "dc0e384f0551386cd76dc29cc964c95e": {
                    "timestamp": 1692672717.68,
                    "packages": {
                        "b647c43bfefae3f830561ca202b6cfd935b56205": {
                            "info": {
                                "settings": {
                                    "arch": "x86_64",
                                    "build_type": "Release",
                                    "compiler": "gcc",
                                    "compiler.version": "11",
                                    "os": "Linux"
                                },
                                "options": {
                                    "shared": "False"
                                }
                            },
                            "diff": {
                                "platform": {},
                                "options": {
                                    "expected": [
                                        "shared=True"
                                    ],
                                    "existing": [
                                        "shared=False"
                                    ]
                                },
                                "settings": {},
                                "dependencies": {},
                                "explanation": "This binary was built with same settings but different options."
                            },
                            "remote": "conancenter"
                        }
                    }
                }
            }
        }
    }
}
```
