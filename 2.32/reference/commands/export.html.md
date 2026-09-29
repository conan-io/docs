# conan export

```text
$ conan export -h
usage: conan export [-h] [-f FORMAT] [--out-file OUT_FILE]
                    [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                    [-cc CORE_CONF] [--name NAME] [--version VERSION]
                    [--user USER] [--channel CHANNEL] [-r REMOTE | -nr]
                    [-l LOCKFILE] [--lockfile-out LOCKFILE_OUT]
                    [--lockfile-partial] [--build-require]
                    [path]

Export a recipe to the Conan package cache.

positional arguments:
  path                  Path to a folder containing a recipe (conanfile.py).
                        Defaults to current directory

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Select the output format: json, pkglist
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
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile.
  --lockfile-out LOCKFILE_OUT
                        Filename of the updated lockfile
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile
  --build-require       Whether the provided reference is a build-require

reference arguments:
  --name NAME           Provide a package name if not specified in conanfile
  --version VERSION     Provide a package version if not specified in
                        conanfile
  --user USER           Provide a user if not specified in conanfile
  --channel CHANNEL     Provide a channel if not specified in conanfile

```

The `conan export` command exports the recipe specified in `path` to the Conan package cache.

## Output Formats

The **conan export** command accepts two types of formats for the `--format` argument:

* `json`: Creates a JSON file containing the information of the exported recipe reference.
* `pkglist`: Generates a JSON file in the [pkglist](https://docs.conan.io/2//tutorial/other_features.html.md#other-important-features-pkglist)
  format, which can be utilized as input for various commands such as **upload**,
  **download**, and **remove**.
