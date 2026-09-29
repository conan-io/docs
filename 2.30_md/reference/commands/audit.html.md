<a id="reference-commands-audit"></a>

# conan audit

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

*New feature in Conan 2.14.0*

The `conan audit` command is used to check for known vulnerabilities in your Conan packages.

See [the audit devops page](https://docs.conan.io/2//devops/audit.html.md#devops-audit) to see examples on how to use the `conan audit` command.

## conan audit scan

```text
$ conan audit scan -h
usage: conan audit scan [-h] [-f FORMAT] [--out-file OUT_FILE]
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
                        [--lockfile-overrides LOCKFILE_OVERRIDES]
                        [--build-require] [-sl SEVERITY_LEVEL]
                        [--context {host,build}] [-p PROVIDER]
                        [path]

Scan a given recipe for vulnerabilities in its dependencies.

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
  --build-require       Whether the provided reference is a build-require
  -sl SEVERITY_LEVEL, --severity-level SEVERITY_LEVEL
                        Set threshold for severity level to raise an error. By
                        default raises an error for any critical CVSS (9.0 or
                        higher). Use 100.0 to disable it.
  --context {host,build}
                        Context to scan, by default both contexts are scanned
                        if not specified
  -p PROVIDER, --provider PROVIDER
                        Provider to use for scanning

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

The `conan audit scan` command checks for vulnerabilities in the given references and their transitive dependencies.
This command receives configuration arguments such as profiles and settings, to control the expansion of the graph.

## conan audit list

```text
$ conan audit list -h
usage: conan audit list [-h] [-f FORMAT] [--out-file OUT_FILE]
                        [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                        [-cc CORE_CONF] [-l LIST] [-s SBOM] [-lock LOCKFILE]
                        [-r REMOTE] [-p PROVIDER]
                        [reference]

List the vulnerabilities of the given reference.

positional arguments:
  reference             Reference to list vulnerabilities for

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
  -l LIST, --list LIST  Package list file to list vulnerabilities for
  -s SBOM, --sbom SBOM  SBOM file to list vulnerabilities for
  -lock LOCKFILE, --lockfile LOCKFILE
                        Path to the lockfile to check for vulnerabilities
  -r REMOTE, --remote REMOTE
                        Remote to use for listing
  -p PROVIDER, --provider PROVIDER
                        Provider to use for scanning

```

The `conan audit list` command lists vulnerabilities for the given references, without checking their transitive dependencies.
You can pass a single reference, a pkglist file with multiple references,
a cyclonedx SBOM file generated with the [conan.tools.sbom](https://docs.conan.io/2//reference/tools/sbom.html.md#conan-tools-sbom) module, or a Conan lockfile.

## conan audit provider

```text
$ conan audit provider -h
usage: conan audit provider [-h] [-f FORMAT] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF] [--url URL]
                            [--type {conan-center-proxy,private}]
                            [--token TOKEN]
                            {add,list,auth,remove} [name]

Manage security providers for the 'conan audit' command.

positional arguments:
  {add,list,auth,remove}
                        Action to perform from 'add', 'list' , 'remove' or
                        'auth'
  name                  Provider name

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
  --url URL             Provider URL
  --type {conan-center-proxy,private}
                        Provider type
  --token TOKEN         Provider token

```

The `conan audit provider` command manages the list of providers used to check for vulnerabilities.

By default the `conan audit` subcommands use the ConanCenter provider, but you can add your own providers to the list.
For now, besides the default ConanCenter provider, only private JFrog Security providers are supported, see [the audit devops page](https://docs.conan.io/2//devops/audit.html.md#devops-audit-private-providers) for more information.

There are 3 subcommands:

- `conan audit provider auth`: Authenticates a provider with a token.
- `conan audit provider add`: Adds a provider to the list.
- `conan audit provider remove`: Removes a provider from the list.

#### SEE ALSO
- Read more in the dedicated [blog post](https://blog.conan.io/introducing-conan-audit-command/).
