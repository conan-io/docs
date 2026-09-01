<a id="reference-commands-pkglist"></a>

# conan pkglist

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

Perform different operations over package lists:

- Merge multiple package lists (deep merge) into a single one: `conan pkglist merge`
- Find in which remotes packages from the cache can be found: `conan pkglist find-remote`

## conan pkglist merge

```text
$ conan pkglist merge -h
usage: conan pkglist merge [-h] [-f FORMAT] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF] [-l LIST]

(Experimental) Merge several package lists into a single one

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
  -l LIST, --list LIST  Package list file

```

The `conan pkglist merge` command can merge multiple package lists into a single one:

```bash
$ conan pkglist merge --list=list1.json --list=list2.json --format=json > result.json
```

The merge will be a deep merge, different versions can be added, and within versions multiple
revisions can be added, and for every recipe revision multiple package_ids can be also accumulated.

## conan pkglist find-remote

```text
$ conan pkglist find-remote -h
usage: conan pkglist find-remote [-h] [-f FORMAT] [--out-file OUT_FILE]
                                 [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                                 [-cc CORE_CONF] [-r REMOTE]
                                 list

(Experimental) Find the remotes of a list of packages in the cache

positional arguments:
  list                  Input package list

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
  -r REMOTE, --remote REMOTE
                        Remote names. Accepts wildcards ('*' means all the
                        remotes available)

```

The `conan pkglist find-remote` command will take a package list of packages in the cache
(key `"Local Cache"`) and look for them in the defined remotes. For every exact occurrence in a remote
matching the recipe, version, recipe-revision, etc, an entry in the resulting “package lists”
will be added for that specific remote.

#### SEE ALSO
- [Read the “package lists” example usages](https://docs.conan.io/2//examples/commands/pkglists.html.md#examples-commands-pkglists)
