<a id="reference-commands-cache"></a>

# conan cache

Perform file operations in the local cache (of recipes and/or packages).

## conan cache path

```text
$ conan cache path -h
usage: conan cache path [-h] [-f FORMAT] [--out-file OUT_FILE]
                        [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                        [-cc CORE_CONF]
                        [--folder {export_source,source,build,metadata}]
                        reference

Show the path to the Conan cache for a given reference.

positional arguments:
  reference             Recipe reference or Package reference

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
  --folder {export_source,source,build,metadata}
                        Path to show. The 'build' requires a package
                        reference. If the argument is not passed, it shows
                        'exports' path for recipe references and 'package'
                        folder for package references.

```

The `conan cache path` returns the path in the cache of a given reference. Depending on the reference, it
could return the path of a recipe, or the path to a package binary.

Let’s say that we have created a package in our current cache with:

```text
$ conan new cmake_lib -d name=pkg -d version=0.1
$ conan create .
...
Requirements
    pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77 - Cache

Requirements
    pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77:2401fa1d188d289bb25c37cfa3317e13e377a351 - Build
```

And now we are interested in obtaining the path where our `pkg/0.1` recipe `conanfile.py` has been exported:

```text
$ conan cache path pkg/0.1
<path to conan cache>/p/5cb229164ec1d245/e

$ ls <path to conan cache>/p/5cb229164ec1d245/e
conanfile.py  conanmanifest.txt
```

By default, if the recipe revision is not specified, it means the “latest” revision in the cache. This can
also be made explicit by the literal `#latest`, and also any recipe revision can be explicitly defined,
these commands are equivalent to the above:

```text
$ conan cache path pkg/0.1#latest
<path to conan cache>/p/5cb229164ec1d245/e

# The recipe revision might be different in your case.
# Check the "conan create" output to get yours
$ conan cache path pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77
<path to conan cache>/p/5cb229164ec1d245/e
```

Together with the recipe folder, there are a two other folders that are common to all the binaries
produced with this recipe: the “export_source” folder and the “source” folder. Both can be
obtained with:

```text
$ conan cache path pkg/0.1 --folder=export_source
<path to conan cache>/p/5cb229164ec1d245/es

$ ls <path to conan cache>/p/5cb229164ec1d245/es
CMakeLists.txt  include/  src/

$ conan cache path pkg/0.1 --folder=source
<path to conan cache>/p/5cb229164ec1d245/s

$ ls <path to conan cache>/p/5cb229164ec1d245/s
CMakeLists.txt  include/  src/
```

In this case the contents of the “source” folder are identical to the ones of the “export_source” folder
because the recipe did not implement any `source()` method that could retrieve code or do any other operation
over the code, like applying patches.

The recipe revision by default will be `#latest`, this follows the same rules as above.

Note that these two folders will not exist if the package has not been built from source, like when a precompiled
binary is retrieve from a server.

It is also possible to obtain the folders of the binary packages providing the `package_id`:

```text
# Your package_id might be different, it depends on the platform
# Check the "conan create" output to obtain yours
$ conan cache path pkg/0.1:2401fa1d188d289bb25c37cfa3317e13e377a351
<path to conan cache>/p/1cae77d6250c23b7/p

$ ls <path to conan cache>/p/1cae77d6250c23b7/p
conaninfo.txt  conanmanifest.txt  include/  lib/
```

As above, by default it will resolve to the “latest” recipe revision and package revision.
The command above is equal to explicitly defining `#latest` or the exact revisions.
All the commands below are equivalent to the above one:

```text
$ conan cache path pkg/0.1#latest:2401fa1d188d289bb25c37cfa3317e13e377a351
<path to conan cache>/p/1cae77d6250c23b7/p

$ conan cache path pkg/0.1#latest:2401fa1d188d289bb25c37cfa3317e13e377a351#latest
<path to conan cache>/p/1cae77d6250c23b7/p

$ conan cache path pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77:2401fa1d188d289bb25c37cfa3317e13e377a351
<path to conan cache>/p/1cae77d6250c23b7/p
```

It is possible to access the “build” folder with all the temporary build artifacts:

```text
$ conan cache path pkg/0.1:2401fa1d188d289bb25c37cfa3317e13e377a351 --folder=build
<path to conan cache>/p/1cae77d6250c23b7/b

ls -al <path to conan cache>/p/1cae77d6250c23b7/b
build/  CMakeLists.txt  CMakeUserPresets.json  conaninfo.txt  include/  src/
```

Again, the “build” folder will only exist if the package was built from source.

#### NOTE
**Best practices**

- This `conan cache path` command is intended for eventual inspection of the cache, but the cache
  package storage must be considered **read-only**. Do not modify, change, remove or add files from the cache.
- If you are using this command to obtain the path to artifacts and then copying them, consider the usage of a `deployer`
  instead. In the general case, extracting artifacts from the cache manually is discouraged.
- Developers can use the `conan list ... --format=compact` to get the full references in a compact way that can
  be copied and pasted into the `conan cache path` command

## conan cache clean

```text
$ conan cache clean -h
usage: conan cache clean [-h] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF] [-l LIST] [-s] [-b] [-d] [-t] [-bs]
                         [-p PACKAGE_QUERY]
                         [pattern]

Remove non-critical folders from the cache, like source, build and/or download
(.tgz store) ones.

positional arguments:
  pattern               Selection pattern for references to clean

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
  -l LIST, --list LIST  Package list of packages to clean
  -s, --source          Clean source folders
  -b, --build           Clean build folders
  -d, --download        Clean download and metadata folders
  -t, --temp            Clean temporary folders
  -bs, --backup-sources
                        Clean backup sources
  -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                        Remove only the packages matching a specific query,
                        e.g., os=Windows AND (arch=x86 OR compiler=gcc)

```

This command will remove all temporary folders, along with the source, build and download folder
that Conan generates in its execution. It will do so for every matching reference passed in *pattern*,
or the contents of the pkglist file if the `--list` option is used.
It’s possible to limit the cleaning to certain kinds of folders with different flags.

**Examples**:

- Remove all non-critical files:
  ```text
  $ conan cache clean "*"
  ```
- Remove all temporary files:
  ```text
  $ conan cache clean "*" --temp
  ```
- Remove the download folders for the `zlib` recipe:
  ```text
  $ conan cache clean "zlib/*" --download
  ```
- Remove everything but the download folder for the `zlib` recipe:
  ```text
  $ conan cache clean "zlib/*" --source --build --temp
  ```
- Get a list of packages to remove temp files from, then remove them:
  > ```text
  > $ conan list "zlib/*" -f=json > pkglist.json
  > $ conan cache clean --list pkglist.json
  > ```

## conan cache check-integrity

```text
$ conan cache check-integrity -h
usage: conan cache check-integrity [-h] [-f FORMAT] [--out-file OUT_FILE]
                                   [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                                   [-cc CORE_CONF] [-l LIST]
                                   [-p PACKAGE_QUERY]
                                   [pattern]

Check the integrity of the local cache for the given references

positional arguments:
  pattern               Selection pattern for references to check integrity
                        for

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
  -l LIST, --list LIST  Package list of packages to check integrity for
  -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                        Only the packages matching a specific query, e.g.,
                        os=Windows AND (arch=x86 OR compiler=gcc)

```

The `conan cache check-integrity` command checks the integrity of Conan packages in the
local cache that match the given *pattern*, or the contents of the pkglist file if the `--list` option is used.
This means that it will throw an error if any file included in the
`conanmanifest.txt` is missing or does not match the declared checksum in that file.

For example, to verify the integrity of the whole Conan local cache, do:

```text
$ conan cache check-integrity "*"
mypkg/1.0: Integrity checked: ok
mypkg/1.0:454923cd42d0da27b9b1294ebc3e4ecc84020747: Integrity checked: ok
mypkg/1.0:454923cd42d0da27b9b1294ebc3e4ecc84020747: Integrity checked: ok
zlib/1.3.1: Integrity checked: ok
zlib/1.3.1:6fe7fa69f760aee504e0be85c12b2327c716f9e7: Integrity checked: ok
```

This command can also return a pkglist when the `--format=json` option is used.
This returns the packages the are corrupted, which is useful for generating a list of packages that can later be used, for example,
to remove all potentially corrupted packages in a single operation:

```text
$ conan cache check-integrity "*" --format=json --out-file pkglist.json
$ conan remove --list pkglist.json
```

## conan cache backup-upload

```text
$ conan cache backup-upload -h
usage: conan cache backup-upload [-h] [--out-file OUT_FILE]
                                 [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                                 [-cc CORE_CONF]

Upload all the source backups present in the cache

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

The `conan cache backup-upload` will upload all source backups present in the local cache to the backup server,
(excluding those which have been fetched from the excluded urls listed in the `core.sources:exclude_urls` conf),
regardless of which package they belong to, if any.

## conan cache save

```text
$ conan cache save -h
usage: conan cache save [-h] [-f FORMAT] [--out-file OUT_FILE]
                        [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                        [-cc CORE_CONF] [-l LIST] [--file FILE] [--no-source]
                        [pattern]

Get the artifacts from a package list and archive them

positional arguments:
  pattern               A pattern in the form
                        'pkg/version#revision:package_id#revision', e.g:
                        zlib/1.2.13:* means all binaries for zlib/1.2.13. If
                        revision is not specified, it is assumed latest one.

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
  -l LIST, --list LIST  Package list of packages to save
  --file FILE           Save to this file. Allowed extensions .tgz, .txz,
                        .tzst (.txz and .tzst experimental and .tzst requires
                        Python>=3.14)
  --no-source           Exclude the sources

```

Read more in [Save and restore packages from/to the cache](https://docs.conan.io/2//devops/save_restore.html.md#devops-save-restore).

## conan cache restore

```text
$ conan cache restore -h
usage: conan cache restore [-h] [-f FORMAT] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF]
                           file

Put the artifacts from an archive into the cache

positional arguments:
  file                  Path to archive to restore

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

Read more in [Save and restore packages from/to the cache](https://docs.conan.io/2//devops/save_restore.html.md#devops-save-restore).

## conan cache ref

```text
$ conan cache ref -h
usage: conan cache ref [-h] [--out-file OUT_FILE]
                       [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                       [-cc CORE_CONF]
                       path

Show the reference for a given Conan cache folder

positional arguments:
  path                  Path to a Conan cache folder

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

For a given cache folder, returns the Conan reference, that is, a recipe reference in the form `name/version#recipe_revision`, or a package reference in the form `name/version#recipe_revision:package_id#package_revision` (both could also have user/channel), depending on the contents of the folder.

This is a developer and debugging command, intended for occasional developer usage while debugging potential issues, but it is not recommended for any other use case.

#### NOTE
**Best practices**

Navigating the Conan cache is not an intended or supported use case. Using the `conan cache ref` command in any automation, CI or scripting
is strongly discouraged.
The `conan cache ref` is intended exclusively to be a helper command for developers while debugging.

## conan cache sign

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

```text
$ conan cache sign -h
usage: conan cache sign [-h] [-f FORMAT] [--out-file OUT_FILE]
                        [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                        [-cc CORE_CONF] [-l LIST] [-p PACKAGE_QUERY]
                        [pattern]

Sign packages with the Package Signing Plugin

positional arguments:
  pattern               Selection pattern for references to be signed

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
  -l LIST, --list LIST  Package list of packages to be signed
  -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                        Only the packages matching a specific query, e.g.,
                        os=Windows AND (arch=x86 OR compiler=gcc)

```

Signs the packages matching the pattern/reference or package list provided. For example:

```text
$ conan list zlib/1.3.1:* --format=json > list.json

$ conan cache sign --list=list.json
[Package sign] Results:

zlib/1.3.1
revisions
    bfceb3f8904b735f75c2b0df5713b1e6
    packages
        7bfde258ff4f62f75668d0896dbddedaa7480a0f

[Package sign] Summary: OK=1, FAILED=0
```

This command requires a configured package signing plugin, read more in [Package signing](https://docs.conan.io/2//reference/extensions/package_signing.html.md#reference-extensions-package-signing).

## conan cache verify

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

```text
$ conan cache verify -h
usage: conan cache verify [-h] [-f FORMAT] [--out-file OUT_FILE]
                          [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                          [-cc CORE_CONF] [-l LIST] [-p PACKAGE_QUERY]
                          [pattern]

Check the signature of packages with the Package Signing Plugin

positional arguments:
  pattern               Selection pattern for references to verify their
                        signature

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
  -l LIST, --list LIST  Package list of packages to verify their signature
  -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                        Only the packages matching a specific query, e.g.,
                        os=Windows AND (arch=x86 OR compiler=gcc)

```

Verifies the signatures of the packages matching the pattern/reference or a package list.

This command requires as configured package signing plugin, read more in [Package signing](https://docs.conan.io/2//reference/extensions/package_signing.html.md#reference-extensions-package-signing).
