<a id="reference-commands-version"></a>

# conan version

#### NOTE
This feature is in **preview**. It means that it is very unlikely to be removed and unlikely to have
breaking changes. Maintainers will try as much as possible to not break it, and only do it if
very necessary.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

```text
$ conan version -h
usage: conan version [-h] [-f FORMAT] [--out-file OUT_FILE]
                     [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                     [-cc CORE_CONF]

Give information about the Conan client version.

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

The **conan version** command shows information about the system and Python environment,
including Conan version, Python version, system platform, architecture, release, CPU, and more:

* **version**: The Conan version.
* **conan_path**: The path to the Conan script.
* *python*: A sub-dictionary containing information about the Python environment, including:
  : * **version**: The version of Python being used.
    * **sys_version**: The full Python system version.
    * **sys_executable**: The path to the Python executable.
    * **is_frozen**: An indicator of whether the Python script is being run as a frozen file (e.g., using py2exe or PyInstaller).
    * **architecture**: The architecture detected by Python.
* *system*: A sub-dictionary containing information about the operating system, including:
  : * **version**: The version of the operating system.
    * **platform**: The platform of the system.
    * **system**: The name of the operating system.
    * **release**: The release version of the operating system.
    * **cpu**: Information about the system’s CPU.

```text
$ conan version
version: 2.0.6
conan_path: /conan/venv/bin/conan
python
  version: 3.10.4
  sys_version: 3.10.4 (main, May 17 2022, 10:53:07) [Clang 13.1.6 (clang-1316.0.21.2.3)]
  sys_executable: /conan/venv/bin/python
  is_frozen: False
  architecture: arm64
system
  version: Darwin Kernel Version 23.4.0: Fri Mar 15 00:12:37 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T6031
  platform: macOS-14.4.1-arm64-arm-64bit
  system: Darwin
  release: 23.4.0
  cpu: arm
```

The **conan version --format=json** returns a JSON output format in `stdout` (which can be redirected to a file) with the following structure:

```text
$ conan version --format=json
{
    "version": "2.0.6",
    "conan_path": "/Users/myUser/Documents/GitHub/conan/venv/bin/conan",
    "python": {
        "version": "3.10.4",
        "sys_version": "3.10.4 (main, May 17 2022, 10:53:07) [Clang 13.1.6 (clang-1316.0.21.2.3)]",
        "sys_executable": "/conan/venv/bin/python",
        "is_frozen": false,
        "architecture": "arm64"
    },
    "system": {
        "version": "Darwin Kernel Version 23.4.0: Fri Mar 15 00:12:37 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T6031",
        "platform": "macOS-14.4.1-arm64-arm-64bit",
        "system": "Darwin",
        "release": "23.4.0",
        "cpu": "arm"
    }
}
```
