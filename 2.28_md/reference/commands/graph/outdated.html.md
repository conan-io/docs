<a id="reference-graph-outdated"></a>

# conan graph outdated

```text
$ conan graph outdated -h
usage: conan graph outdated [-h] [-f FORMAT] [--out-file OUT_FILE]
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
                            [path]

List the dependencies in the graph and it's newer versions in the remote

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

The `conan graph outdated` command provides details on libraries for which a newer version is available in a remote
repository. This command helps users in identifying outdated libraries by displaying the latest version available in
the remote repository and indicating which specific remote repository it was found in. Additionally, it presents
information on the versions currently stored in the local cache and specifies the version ranges for each library.

It will display the information for every library on the dependency graph it is run on. For example if running
the command with an older version of `libcurl` it will display:

```bash
$ conan graph outdated --requires=libcurl/[*]
```

```text
======== Computing dependency graph ========
Graph root
    cli
Requirements
    libcurl/8.5.0#95279f20d2443016907657f081a79261 - Cache
    openssl/3.2.1#edbeabd3bfc383d2cca3858aa2a78a0d - Cache
    zlib/1.3.1#f52e03ae3d251dec704634230cd806a2 - Cache
Build requirements
    nasm/2.15.05#058c93b2214a49ca1cfe9f8f26205568 - Cache
    strawberryperl/5.32.1.1#8f83d05a60363a422f9033e52d106b47 - Cache
Resolved version ranges
    libcurl/[*]: libcurl/8.5.0
    openssl/[>=1.1 <4]: openssl/3.2.1
    zlib/[>=1.2.11 <2]: zlib/1.3.1

======== Checking remotes ========
Found 35 pkg/version recipes matching libcurl in conancenter
Found 46 pkg/version recipes matching openssl in conancenter
Found 6 pkg/version recipes matching zlib in conancenter
Found 5 pkg/version recipes matching nasm in conancenter
Found 3 pkg/version recipes matching strawberryperl in conancenter
======== Outdated dependencies ========
libcurl
    Current versions:  libcurl/8.5.0
    Latest in remote(s):  libcurl/8.6.0 - conancenter
    Version ranges: libcurl/[*]
nasm
    Current versions:  nasm/2.15.05
    Latest in remote(s):  nasm/2.16.01 - conancenter
```
