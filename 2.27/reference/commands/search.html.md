<a id="reference-commands-search"></a>

# conan search

Search existing recipes in remotes.
This command is equivalent to `conan list <query> -r=*`, and is provided for simpler UX.

```text
$ conan search -h
usage: conan search [-h] [-f FORMAT] [--out-file OUT_FILE]
                    [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                    [-cc CORE_CONF] [-r REMOTE]
                    reference

Search for package recipes in all the remotes (by default), or a remote.

positional arguments:
  reference             Recipe reference to search for. It can contain * as
                        wildcard at any reference field.

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
  -r REMOTE, --remote REMOTE
                        Remote names. Accepts wildcards. If not specified it
                        searches in all the remotes

```

```text
$ conan search zlib
conancenter
  zlib
    zlib/1.2.8
    zlib/1.3.1
    zlib/1.2.12
    zlib/1.2.13

$ conan search zlib -r=conancenter
conancenter
  zlib
    zlib/1.2.8
    zlib/1.3.1
    zlib/1.2.12
    zlib/1.2.13

$ conan search zlib/1.2.1* -r=conancenter
conancenter
  zlib
    zlib/1.3.1
    zlib/1.2.12
    zlib/1.2.13

$ conan search zlib/1.2.1* -r=conancenter --format=json
{
    "conancenter": {
        "zlib/1.3.1": {},
        "zlib/1.2.12": {},
        "zlib/1.2.13": {}
    }
}
```
