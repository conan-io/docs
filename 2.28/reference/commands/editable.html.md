<a id="reference-commands-editable"></a>

# conan editable

Allow working with a package that resides in user folder.

## conan editable add

```text
$ conan editable add -h
usage: conan editable add [-h] [--out-file OUT_FILE]
                          [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                          [-cc CORE_CONF] [--name NAME] [--version VERSION]
                          [--user USER] [--channel CHANNEL]
                          [-of OUTPUT_FOLDER] [-r REMOTE | -nr]
                          [path]

Define the given <path> location as the package <reference>, so when this
package is required, it is used from this <path> location instead of the
cache.

positional arguments:
  path                  Path to the package folder in the user workspace

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
  -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        The root output folder for generated and build files
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache

reference arguments:
  --name NAME           Provide a package name if not specified in conanfile
  --version VERSION     Provide a package version if not specified in
                        conanfile
  --user USER           Provide a user if not specified in conanfile
  --channel CHANNEL     Provide a channel if not specified in conanfile

```

## conan editable remove

```text
$ conan editable remove -h
usage: conan editable remove [-h] [--out-file OUT_FILE]
                             [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                             [-cc CORE_CONF] [-r REFS]
                             [path]

Remove the "editable" mode for this reference.

positional arguments:
  path                  Path to a folder containing a recipe conanfile.py or
                        to a recipe file. e.g., ./my_project/conanfile.py.

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
  -r REFS, --refs REFS  Directly provide reference patterns

```

## conan editable list

```text
$ conan editable list -h
usage: conan editable list [-h] [-f FORMAT] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF]

List all the packages in editable mode.

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

```

#### SEE ALSO
- Read the tutorial about editable packages [editable package](https://docs.conan.io/2//tutorial/developing_packages/editable_packages.html.md#editable-packages).
