# conan lock remove

```text
$ conan lock remove -h
usage: conan lock remove [-h] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF] [--requires REQUIRES]
                         [--build-requires BUILD_REQUIRES]
                         [--python-requires PYTHON_REQUIRES]
                         [--config-requires CONFIG_REQUIRES]
                         [--lockfile-out LOCKFILE_OUT] [--lockfile LOCKFILE]

Remove requires, build-requires or python-requires from an existing lockfile.
References can be supplied with and without revisions like "--
requires=pkg/version",

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
  --requires REQUIRES   Remove references to lockfile.
  --build-requires BUILD_REQUIRES
                        Remove build-requires from lockfile
  --python-requires PYTHON_REQUIRES
                        Remove python-requires from lockfile
  --config-requires CONFIG_REQUIRES
                        Remove config-requires from lockfile
  --lockfile-out LOCKFILE_OUT
                        Filename of the created lockfile
  --lockfile LOCKFILE   Filename of the input lockfile

```

The `conan lock remove` command is able to remove `requires`, `build_requires`, `python_requires` or `config_requires` items from an existing lockfile.

For example, if we have the following `conan.lock`:

```bash
$ cat conan.lock
{
    "version": "0.5",
    "requires": [
        "math/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
        "engine/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ],
    "build_requires": [
        "cmake/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
        "ninja/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ],
    "python_requires": [
        "mytool/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
        "othertool/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ]
}
```

The `conan lock remove` command:

```bash
$ conan lock remove --requires="math/*" --build-requires=cmake/1.0 --python-requires="*tool/*"
```

Will result in the following `conan.lock`:

```bash
$ cat conan.lock
{
    "version": "0.5",
    "requires": [
        "engine/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ],
    "build_requires": [
        "ninja/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ],
    "python_requires": [
    ]
}
```

It is possible to specify different patterns:

- Remove by version-ranges with expressions like `--requires="math/[>=1.0 <2]"`, and also
- Remove a specific revision: `--requires=math/1.0#revision`
- Remove locked dependencies for a given “team” user `--requires=*/*@team*`

The `conan lock remove` can be useful for:

- In combination with `conan lock add`, it can be used to force the downgrade of a locked version to an older one. As `conan lock add`
  always adds and sorts the order, resulting in newer versions with high priority, it is not possible to force going back to an older
  version with just `add`. But first using `conan lock remove`, then `conan lock add`, it is possible to do so.
- `conan lock remove` can unlock certain dependencies, resulting in an incomplete lockfile, that can be used with `--lockfile-partial`
  to resolve to the latest available versions for the unlocked dependencies, while keeping locked the rest.
