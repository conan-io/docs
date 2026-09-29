# conan lock update

```text
$ conan lock update -h
usage: conan lock update [-h] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF] [--requires REQUIRES]
                         [--build-requires BUILD_REQUIRES]
                         [--python-requires PYTHON_REQUIRES]
                         [--config-requires CONFIG_REQUIRES]
                         [--lockfile-out LOCKFILE_OUT] [--lockfile LOCKFILE]

Update requires, build-requires or python-requires from an existing lockfile.
References that matches the arguments package names will be replaced by the
arguments. References can be supplied with and without revisions like "--
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
  --requires REQUIRES   Update references to lockfile.
  --build-requires BUILD_REQUIRES
                        Update build-requires from lockfile
  --python-requires PYTHON_REQUIRES
                        Update python-requires from lockfile
  --config-requires CONFIG_REQUIRES
                        Update config-requires from lockfile
  --lockfile-out LOCKFILE_OUT
                        Filename of the created lockfile
  --lockfile LOCKFILE   Filename of the input lockfile

```

The `conan lock update` command is able to update `requires`, `build_requires`, `python_requires` or `config_requires` items from an existing lockfile.

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

The `conan lock update` command:

```bash
$ conan lock update --requires=math/1.1 --build-requires=cmake/1.1
```

Will result in the following `conan.lock`:

```bash
$ cat conan.lock
{
    "version": "0.5",
    "requires": [
        "math/1.1",
        "engine/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ],
    "build_requires": [
        "cmake/1.1",
        "ninja/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ],
    "python_requires": [
        "mytool/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
        "othertool/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
    ]
}
```

The command will replace existing locked references that matches the same package name with the provided argument values.
If the provided references does not exist in the lockfile, they will be added (same as `conan lock add` command).

This command is similar to do a `conan lock remove` followed by a `conan lock add` command.
