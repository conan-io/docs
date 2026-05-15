<a id="reference-commands-source"></a>

# conan source

```text
$ conan source -h
usage: conan source [-h] [--out-file OUT_FILE]
                    [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                    [-cc CORE_CONF] [--name NAME] [--version VERSION]
                    [--user USER] [--channel CHANNEL]
                    [path]

Call the source() method.

positional arguments:
  path                  Path to a folder containing a conanfile.py. Defaults
                        to current directory

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

reference arguments:
  --name NAME           Provide a package name if not specified in conanfile
  --version VERSION     Provide a package version if not specified in
                        conanfile
  --user USER           Provide a user if not specified in conanfile
  --channel CHANNEL     Provide a channel if not specified in conanfile

```

#### SEE ALSO
- Read the tutorial about the [local package development flow](https://docs.conan.io/2//tutorial/developing_packages/local_package_development_flow.html.md#local-package-development-flow).
