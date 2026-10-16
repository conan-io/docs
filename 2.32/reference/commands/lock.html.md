# conan lock

The `conan lock` command contains several subcommands.
In addition to these commands, most of the Conan commands that compute a graph, like `create`, `install`,
`graph`, can both receive lockfiles as input and produce lockfiles as output.

- [conan lock add](https://docs.conan.io/2//reference/commands/lock/add.html.md): Manually add items to a lockfile
- [conan lock remove](https://docs.conan.io/2//reference/commands/lock/remove.html.md): Manually remove items from a lockfile
- [conan lock create](https://docs.conan.io/2//reference/commands/lock/create.html.md): Evaluates a dependency graph and save a lockfile
- [conan lock merge](https://docs.conan.io/2//reference/commands/lock/merge.html.md): Merge several existing lockfiles into one
- [conan lock update](https://docs.conan.io/2//reference/commands/lock/update.html.md): Manually update items from a lockfile
- [conan lock upgrade](https://docs.conan.io/2//reference/commands/lock/upgrade.html.md): (Experimental) Upgrade items from a lockfile
- [conan lock upgrade-config](https://docs.conan.io/2//reference/commands/lock/upgrade_config.html.md): (Experimental) Upgrade configuration packages from a lockfile

```text
$ conan lock -h
usage: conan lock [-h] [--out-file OUT_FILE]
                  [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                  [-cc CORE_CONF]
                  {add,create,merge,remove,update,upgrade,upgrade-config} ...

Create or manage lockfiles.

positional arguments:
  {add,create,merge,remove,update,upgrade,upgrade-config}
                        sub-command help
    add                 Add requires, build-requires or python-requires to an
                        existing or new lockfile. The resulting lockfile will
                        be ordered, newer versions/revisions first. References
                        can be supplied with and without revisions like "--
                        requires=pkg/version", but they must be recipe
                        references, including at least the version, and they
                        cannot contain a version range.
    create              Create a lockfile from a conanfile or a reference.
    merge               Merge 2 or more lockfiles.
    remove              Remove requires, build-requires or python-requires
                        from an existing lockfile. References can be supplied
                        with and without revisions like "--
                        requires=pkg/version",
    update              Update requires, build-requires or python-requires
                        from an existing lockfile. References that matches the
                        arguments package names will be replaced by the
                        arguments. References can be supplied with and without
                        revisions like "--requires=pkg/version",
    upgrade             (Experimental) Upgrade requires, build-requires or
                        python-requires from an existing lockfile given a
                        conanfile or a reference.
    upgrade-config      (Experimental) Upgrade config requires in a lockfile

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

```
