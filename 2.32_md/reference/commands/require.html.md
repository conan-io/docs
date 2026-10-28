<a id="reference-commands-require"></a>

# conan require

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

```text
$ conan require -h
usage: conan require [-h] [--out-file OUT_FILE]
                     [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                     [-cc CORE_CONF]
                     {add,remove} ...

Adds/removes requirements to/from your local conanfile.

positional arguments:
  {add,remove}          sub-command help
    add                 Add a new requirement to your local conanfile as a
                        version range. By default, it will look for the
                        requirement versions remotely.
    remove              Removes a requirement from your local conanfile.

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

The **conan require** command helps to add any requirement as a version range or remove it from your *conanfile.py*.

#### IMPORTANT
This command is only a UX utility. It’s not aimed at replacing editing the conanfile, and it’s not expected to cover
all the use cases, i.e., conditional requirements, requirements with different traits, etc. For all those mentioned
scenarios, we recommend editing the conanfile.py as usual.

## conan require add

```text
$ conan require add -h
usage: conan require add [-h] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF] [--folder FOLDER] [-tor TOOL]
                         [-ter TEST] [-r REMOTE | -nr]
                         [requires ...]

Add a new requirement to your local conanfile as a version range. By default,
it will look for the requirement versions remotely.

positional arguments:
  requires              Requirement name.

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
  --folder FOLDER       Path to a folder containing a recipe (conanfile.py).
                        Defaults to the current directory
  -tor TOOL, --tool TOOL
                        Tool requirement name.
  -ter TEST, --test TEST
                        Test requirement name.
  -r REMOTE, --remote REMOTE
                        Remote names. Accepts wildcards ('*' means all the
                        remotes available)
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache

```

Add a new requirement to your local *conanfile.py* as a version range.

By default, it looks for the recipe name in any of your remotes. When a remote contains any result for the recipe
required, the latest version is used and written as a version range between the version found and the next major one
(if possible, as versions based on commits do not have that major version):

```bash
$ conan require add fmt
Connecting to remote 'conancenter' anonymously
Found 21 pkg/version recipes matching fmt/* in conancenter
Added 'fmt/[>=12.1.0 <13]' as a new requires.
```

It admits several arguments as new requirements:

```bash
$ conan require add fmt zlib
Connecting to remote 'conancenter' anonymously
Found 21 pkg/version recipes matching fmt/* in conancenter
Found 5 pkg/version recipes matching zlib/* in conancenter
Added 'fmt/[>=12.1.0 <13]' as a new requires.
Added 'zlib/[>=1.3.1 <2]' as a new requires.
```

Or even, you can directly put the requirement version:

```bash
$ conan require add boost/1.89.0
Added 'boost/[>=1.89.0 <2]' as a new requires.
```

Tool and test requirements are also supported:

```bash
$ conan require add --tool cmake --test gtest
Connecting to remote 'conancenter' anonymously
Found 54 pkg/version recipes matching cmake/* in conancenter
Found 10 pkg/version recipes matching gtest/* in conancenter
Added 'cmake/[>=4.2.2 <5]' as a new tool_requires.
Added 'gtest/cci.20210126' as a new test_requires.
```

Use `--no-remote` to resolve versions only from the local cache:

```bash
$ conan require add boost --no-remote
Found 2 pkg/version recipes matching boost/* in local cache
Added 'boost/[>=1.89.0 <2]' as a new requires.
```

Use `--folder` to point to a different recipe location:

```text
$ conan require add fmt --folder=path/to/conanfile.py
```

## conan require remove

```text
$ conan require remove -h
usage: conan require remove [-h] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF] [--folder FOLDER] [-tor TOOL]
                            [-ter TEST]
                            [requires ...]

Removes a requirement from your local conanfile.

positional arguments:
  requires              Requirement name.

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
  --folder FOLDER       Path to a folder containing a recipe (conanfile.py).
                        Defaults to the current directory
  -tor TOOL, --tool TOOL
                        Tool requirement name.
  -ter TEST, --test TEST
                        Test requirement name.

```

Remove any requirement from your *conanfile.py*:

```bash
$ conan require remove fmt zlib
Removed fmt dependency as requires.
Removed zlib dependency as requires.
```

Tool and test requirements are also supported:

```bash
$ conan require remove --tool cmake --test gtest
Removed cmake dependency as tool_requires.
Removed gtest dependency as test_requires.
```

Use `--folder` to point to a different recipe location:

```text
$ conan require remove fmt --folder=path/to/conanfile.py
```
