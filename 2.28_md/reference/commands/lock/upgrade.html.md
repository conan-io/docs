# conan lock upgrade

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

```text
$ conan lock upgrade -h
usage: conan lock upgrade [-h] [--out-file OUT_FILE]
                          [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                          [-cc CORE_CONF] [-b BUILD] [-r REMOTE | -nr]
                          [-u [UPDATE]] [-pr PROFILE] [-pr:b PROFILE_BUILD]
                          [-pr:h PROFILE_HOST] [-pr:a PROFILE_ALL]
                          [-o OPTIONS] [-o:b OPTIONS_BUILD]
                          [-o:h OPTIONS_HOST] [-o:a OPTIONS_ALL] [-s SETTINGS]
                          [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                          [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                          [-c:h CONF_HOST] [-c:a CONF_ALL]
                          [--requires REQUIRES]
                          [--tool-requires TOOL_REQUIRES] [--name NAME]
                          [--version VERSION] [--user USER]
                          [--channel CHANNEL] [-l LOCKFILE]
                          [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                          [--lockfile-clean]
                          [--lockfile-overrides LOCKFILE_OVERRIDES]
                          [-ur UPDATE_REQUIRES] [-ubr UPDATE_BUILD_REQUIRES]
                          [-upr UPDATE_PYTHON_REQUIRES] [--build-require]
                          [path]

(Experimental) Upgrade requires, build-requires or python-requires from an
existing lockfile given a conanfile or a reference.

positional arguments:
  path                  Path to a folder containing a recipe (conanfile.py or
                        conanfile.txt) or to a recipe file. e.g.,
                        ./my_project/conanfile.txt. Defaults to the current
                        directory when no --requires or --tool-requires is
                        given

options:
  -h, --help            show this help message and exit
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
  -ur UPDATE_REQUIRES, --update-requires UPDATE_REQUIRES
                        Update requires from lockfile
  -ubr UPDATE_BUILD_REQUIRES, --update-build-requires UPDATE_BUILD_REQUIRES
                        Update build-requires from lockfile
  -upr UPDATE_PYTHON_REQUIRES, --update-python-requires UPDATE_PYTHON_REQUIRES
                        Update python-requires from lockfile
  --build-require       Whether the provided reference is a build-require

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

The `conan lock upgrade` command is able to upgrade `requires`, `build_requires`, `python_requires` items from an existing lockfile.

For example, if we have the following `conan.lock`:

```bash
$ cat conan.lock
{
    "version": "0.5",
    "requires": [
        "package/1.0#b0546195fd5bf19a0e6742510fff8855%1740472377.653885"
    ],
    "build_requires": [
        "cmake/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
    ]
}
```

And these packages available in the cache:

```bash
$ conan list "*" --format=compact

Found 9 pkg/version recipes matching * in local cache
Local Cache
  package/1.0
  package/1.9
  cmake/3.29.0
  cmake/3.30.5
```

Using the `conan lock upgrade` command with the appropiate `--update-**` arguments:

```bash
$ conan lock upgrade --requires=package/[>=1.0 <2] --update-requires=package/[*]
```

Will result in the following `conan.lock`:

```bash
$ cat conan.lock
{
    "version": "0.5",
    "requires": [
        "package/1.9#b0546195fd5bf19a0e6742510fff8855%1740484122.108484"
    ],
    "build_requires": [
        "cmake/3.29.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
    ]
}
```

The same can be done for `build_requires` and `python_requires`.

The command will upgrade existing locked references that match the same
package name with versions that match the version ranges provided by required
arguments.

The `conan lock upgrade` command may also be able to upgrade `requires`, `build_requires`, `python_requires` from a conanfile.
This use case enhances the functionality of version ranges.

Let’s consider the following conanfile:

```python
from conan import ConanFile
class HelloConan(ConanFile):
    requires = ("math/[>=1.0 <2]")
    tool_requires = "ninja/[>=1.0]"
```

```bash
$ conan list "*" --format=compact

Found 9 pkg/version recipes matching * in local cache
Local Cache
  math/1.0
  math/2.0
  ninja/1.0
  ninja/1.1
```

Starting from the same environment and `conan.lock` file from previous example.
Running the following command:

```bash
$ conan lock upgrade . --update-requires=math/1.0 --update-build-requires=ninja/[*]
```

Will result in the following `conan.lock`:

```bash
{
    "version": "0.5",
    "requires": [
        "math/1.0#b0546195fd5bf19a0e6742510fff8855%1740488410.356828"
    ],
    "build_requires": [
        "ninja/1.1#dc77a17d3e566df710241e3b1f380b8c%1740488410.371875"
    ]
}
```

`math` package have not been updated due to the version range specified in
the conanfile, but `ninja` has been updated to the latest version available
in the cache.

If a dependency is updated and in the new revision, a transitive dependency is
added, the `lock upgrade` command will reflect the new transitive dependency
in the lockfile. E.g.

- `liba/1.0` depends on `libb/1.0`
- `libb/1.0` depends on `libc/1.0`

If `libb/2.0` depends also on `libd/1.0`:

```bash
$ conan lock upgrade --requires=libb/[>=2] --update-requires=libb/*
```

The resulting lockfile will contain both `libc/1.0` and `libd/1.0`.

#### NOTE
Updating transitive dependencies is not supported yet. This is an experimental feature and it may change in the future.
