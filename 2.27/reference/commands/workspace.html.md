<a id="reference-commands-workspace"></a>

# conan workspace

#### WARNING
This feature is part of the new incubating features. This means that it is under development, and looking for user
testing and feedback. For more info see [Incubating section](https://docs.conan.io/2//incubating.html.md#incubating).

The `conan workspace` command allows to open, add, and remove packages from the current workspace. Check the
`conan workspace -h` help and the help of the subcommands to check their usage.

```text
$ conan workspace -h
usage: conan workspace [-h] [--out-file OUT_FILE]
                       [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                       [-cc CORE_CONF]
                       {add,build,clean,complete,create,info,init,install,open,remove,root,source,super-install}
                       ...

Manage Conan workspaces (group of packages in editable mode)

positional arguments:
  {add,build,clean,complete,create,info,init,install,open,remove,root,source,super-install}
                        sub-command help
    add                 Add packages to current workspace
    build               Call "conan build" for packages in the workspace, in
                        the right order
    clean               Clean the temporary build folders when possible
    complete            Complete the workspace, opening or adding intermediate
                        packages to it that have requirements to other
                        packages in the workspace.
    create              Call "conan create" for packages in the workspace, in
                        the correct order. Packages will be created in the
                        Conan cache, not locally
    info                Display info for current workspace
    init                Clean the temporary build folders when possible
    install             Call "conan install" for packages in the workspace, in
                        the right order
    open                Open specific references
    remove              Remove packages from the current workspace
    root                Return the folder containing the
                        conanws.py/conanws.yml workspace file
    source              Call the source() method of packages in the workspace
    super-install       Install the workspace as a monolith, installing only
                        external dependencies to the workspace, generating a
                        single result (generators, etc) for the whole
                        workspace.

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

## conan workspace init

```text
$ conan workspace init -h
usage: conan workspace init [-h] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF]
                            [path]

Clean the temporary build folders when possible

positional arguments:
  path                  Path to a folder where the workspace will be
                        initialized. Defaults to the current directory

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

The command `conan workspace init [path]` creates an empty `conanws.yml` file and a minimal `conanws.py` within that path
if they don’t exist yet. That path can be relative to your current working directory.

```bash
$ conan workspace init myfolder
Created empty conanws.yml in myfolder
Created minimal conanws.py in myfolder
```

## conan workspace [add | remove]

```text
$ conan workspace add -h
usage: conan workspace add [-h] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF] [--name NAME] [--version VERSION]
                           [--user USER] [--channel CHANNEL] [--ref REF]
                           [-of OUTPUT_FOLDER] [-r REMOTE | -nr]
                           [path]

Add packages to current workspace

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
  --ref REF             Open and add this reference
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

```text
$ conan workspace remove -h
usage: conan workspace remove [-h] [--out-file OUT_FILE]
                              [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                              [-cc CORE_CONF]
                              path

Remove packages from the current workspace

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

```

Use these commands to add or remove editable packages to the current workspace. The `conan workspace add <path>`
folder must contain a `conanfile.py`. That path can be relative to your current workspace.

The `conanws.py` has a default implementation, but it is possible to override the default behavior:

```python
import os
from conan import Workspace

class MyWorkspace(Workspace):
   def name(self):
      return "myws"

   def add(self, ref, path, *args, **kwargs):
      self.output.info(f"Adding {ref} at {path}")
      super().add(ref, path, *args, **kwargs)

   def remove(self, path, *args, **kwargs):
      self.output.info(f"Removing {path}")
      return super().remove(path, *args, **kwargs)
```

See [conan workspace complete](#workspace-complete-command) command to open/add multiple packages that are missing
in the package to connect different packages already existing in the workspace.

## conan workspace info

```text
$ conan workspace info -h
usage: conan workspace info [-h] [-f FORMAT] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF]

Display info for current workspace

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

Use this command to show information about the current workspace

```bash
$ cd myfolder
$ conan new workspace
$ conan workspace info
WARN: Workspace found
WARN: Workspace is a dev-only feature, exclusively for testing
name: myfolder
folder: /path/to/myfolder
packages
  - path: liba
    ref: liba/0.1
  - path: libb
    ref: libb/0.1
  - path: app1
    ref: app1/0.1
```

## conan workspace clean

```text
$ conan workspace clean -h
usage: conan workspace clean [-h] [--out-file OUT_FILE]
                             [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                             [-cc CORE_CONF]

Clean the temporary build folders when possible

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

The new `conan workspace clean` command removes by default the `output-folder` of every package in the workspace if it was defined.
If it is not defined, it won’t remove anything by default, as removing files in user space is dangerous, and could destroy user changes or files.
It would be recommended that users manage that cleaning with `git clean -xdf` or similar strategies.
It is also possible to define a custom clean logic by implementing the `clean()` method:

```python
class Ws(Workspace):
   def name(self):
      return "my_workspace"
   def clean(self):
      self.output.info("MY CLEAN!!!!")
```

## conan workspace open

```text
$ conan workspace open -h
usage: conan workspace open [-h] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF] [-r REMOTE | -nr]
                            reference

Open specific references

positional arguments:
  reference             Open this package source repository

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
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache

```

The new `conan workspace open` command implements a new concept. The packages containing an `scm` information in
the `conandata.yml` (with `git.coordinates_to_conandata()`) can be automatically cloned and checkout inside the
current workspace from their Conan recipe reference (including recipe revision).

See [conan workspace complete](#workspace-complete-command) command to open/add multiple packages that are missing
in the package to connect different packages already existing in the workspace.

## conan workspace root

```text
$ conan workspace root -h
usage: conan workspace root [-h] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF]

Return the folder containing the conanws.py/conanws.yml workspace file

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

Return the folder containing the conanws.py/conanws.yml workspace file.

## conan workspace source

```text
$ conan workspace source -h
usage: conan workspace source [-h] [--out-file OUT_FILE]
                              [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                              [-cc CORE_CONF] [--pkg PKG]

Call the source() method of packages in the workspace

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
  --pkg PKG             Define specific packages

```

The command `conan workspace source` performs the equivalent of `conan source <package-path>` for every `package`
defined within the workspace.

## conan workspace install

```text
$ conan workspace install -h
usage: conan workspace install [-h] [--out-file OUT_FILE]
                               [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                               [-cc CORE_CONF] [--pkg PKG] [-b BUILD]
                               [-r REMOTE | -nr] [-u [UPDATE]] [-pr PROFILE]
                               [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                               [-pr:a PROFILE_ALL] [-o OPTIONS]
                               [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                               [-o:a OPTIONS_ALL] [-s SETTINGS]
                               [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                               [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                               [-c:h CONF_HOST] [-c:a CONF_ALL] [-l LOCKFILE]
                               [--lockfile-partial]

Call "conan install" for packages in the workspace, in the right order

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
  --pkg PKG             Define specific packages
  -b BUILD, --build BUILD
                        Optional, specify which packages to build from source.
                        Combining multiple '--build' options on one command
                        line is allowed. Possible values: --build=never
                        Disallow build for all packages, use binary packages
                        or fail if a binary package is not found, it cannot be
                        combined with other '--build' options. --build=missing
                        Build packages from source whose binary package is not
                        found. --build=cascade Build packages from source that
                        have at least one dependency being built from source.
                        --build=[pattern] Build packages from source whose
                        package reference matches the pattern. The pattern
                        uses 'fnmatch' style wildcards, so '--build="*"' will
                        build everything from source. --build=~[pattern]
                        Excluded packages, which will not be built from the
                        source, whose package reference matches the pattern.
                        The pattern uses 'fnmatch' style wildcards.
                        --build=missing:[pattern] Build from source if a
                        compatible binary does not exist, only for packages
                        matching pattern. --build=compatible:[pattern]
                        (Experimental) Build from source if a compatible
                        binary does not exist, and the requested package is
                        invalid, the closest package binary following the
                        defined compatibility policies (method and
                        compatibility.py)

remote arguments:
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -u [UPDATE], --update [UPDATE]
                        Will install newer versions and/or revisions in the
                        local cache for the given reference name, or all
                        references in the graph if no argument is supplied.
                        When using version ranges, it will install the latest
                        version that satisfies the range. It will update to
                        the latest revision for the resolved version range.

profile arguments:
  -pr PROFILE, --profile PROFILE
                        Apply the specified profile. By default, or if
                        specifying -pr:h (--profile:host), it applies to the
                        host context. Use -pr:b (--profile:build) to specify
                        the build context, or -pr:a (--profile:all) to specify
                        both contexts at once
  -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
  -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
  -pr:a PROFILE_ALL, --profile:all PROFILE_ALL
  -o OPTIONS, --options OPTIONS
                        Apply the specified options. By default, or if
                        specifying -o:h (--options:host), it applies to the
                        host context. Use -o:b (--options:build) to specify
                        the build context, or -o:a (--options:all) to specify
                        both contexts at once. Example:
                        -o="pkg/*:with_qt=True"
  -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
  -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
  -o:a OPTIONS_ALL, --options:all OPTIONS_ALL
  -s SETTINGS, --settings SETTINGS
                        Apply the specified settings. By default, or if
                        specifying -s:h (--settings:host), it applies to the
                        host context. Use -s:b (--settings:build) to specify
                        the build context, or -s:a (--settings:all) to specify
                        both contexts at once. Example: -s="compiler=gcc"
  -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
  -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
  -s:a SETTINGS_ALL, --settings:all SETTINGS_ALL
  -c CONF, --conf CONF  Apply the specified conf. By default, or if specifying
                        -c:h (--conf:host), it applies to the host context.
                        Use -c:b (--conf:build) to specify the build context,
                        or -c:a (--conf:all) to specify both contexts at once.
                        Example:
                        -c="tools.cmake.cmaketoolchain:generator=Xcode"
  -c:b CONF_BUILD, --conf:build CONF_BUILD
  -c:h CONF_HOST, --conf:host CONF_HOST
  -c:a CONF_ALL, --conf:all CONF_ALL

lockfile arguments:
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile. Use --lockfile="" to avoid
                        automatic use of existing 'conan.lock' file
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile

```

The command `conan workspace install` performs the equivalent of `conan install <package-path>` for every `package`
defined within the workspace in the correct order.

## conan workspace build

```text
$ conan workspace build -h
usage: conan workspace build [-h] [--out-file OUT_FILE]
                             [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                             [-cc CORE_CONF] [--pkg PKG] [-b BUILD]
                             [-r REMOTE | -nr] [-u [UPDATE]] [-pr PROFILE]
                             [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                             [-pr:a PROFILE_ALL] [-o OPTIONS]
                             [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                             [-o:a OPTIONS_ALL] [-s SETTINGS]
                             [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                             [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                             [-c:h CONF_HOST] [-c:a CONF_ALL] [-l LOCKFILE]
                             [--lockfile-partial]

Call "conan build" for packages in the workspace, in the right order

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
  --pkg PKG             Define specific packages
  -b BUILD, --build BUILD
                        Optional, specify which packages to build from source.
                        Combining multiple '--build' options on one command
                        line is allowed. Possible values: --build=never
                        Disallow build for all packages, use binary packages
                        or fail if a binary package is not found, it cannot be
                        combined with other '--build' options. --build=missing
                        Build packages from source whose binary package is not
                        found. --build=cascade Build packages from source that
                        have at least one dependency being built from source.
                        --build=[pattern] Build packages from source whose
                        package reference matches the pattern. The pattern
                        uses 'fnmatch' style wildcards, so '--build="*"' will
                        build everything from source. --build=~[pattern]
                        Excluded packages, which will not be built from the
                        source, whose package reference matches the pattern.
                        The pattern uses 'fnmatch' style wildcards.
                        --build=missing:[pattern] Build from source if a
                        compatible binary does not exist, only for packages
                        matching pattern. --build=compatible:[pattern]
                        (Experimental) Build from source if a compatible
                        binary does not exist, and the requested package is
                        invalid, the closest package binary following the
                        defined compatibility policies (method and
                        compatibility.py)

remote arguments:
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -u [UPDATE], --update [UPDATE]
                        Will install newer versions and/or revisions in the
                        local cache for the given reference name, or all
                        references in the graph if no argument is supplied.
                        When using version ranges, it will install the latest
                        version that satisfies the range. It will update to
                        the latest revision for the resolved version range.

profile arguments:
  -pr PROFILE, --profile PROFILE
                        Apply the specified profile. By default, or if
                        specifying -pr:h (--profile:host), it applies to the
                        host context. Use -pr:b (--profile:build) to specify
                        the build context, or -pr:a (--profile:all) to specify
                        both contexts at once
  -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
  -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
  -pr:a PROFILE_ALL, --profile:all PROFILE_ALL
  -o OPTIONS, --options OPTIONS
                        Apply the specified options. By default, or if
                        specifying -o:h (--options:host), it applies to the
                        host context. Use -o:b (--options:build) to specify
                        the build context, or -o:a (--options:all) to specify
                        both contexts at once. Example:
                        -o="pkg/*:with_qt=True"
  -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
  -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
  -o:a OPTIONS_ALL, --options:all OPTIONS_ALL
  -s SETTINGS, --settings SETTINGS
                        Apply the specified settings. By default, or if
                        specifying -s:h (--settings:host), it applies to the
                        host context. Use -s:b (--settings:build) to specify
                        the build context, or -s:a (--settings:all) to specify
                        both contexts at once. Example: -s="compiler=gcc"
  -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
  -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
  -s:a SETTINGS_ALL, --settings:all SETTINGS_ALL
  -c CONF, --conf CONF  Apply the specified conf. By default, or if specifying
                        -c:h (--conf:host), it applies to the host context.
                        Use -c:b (--conf:build) to specify the build context,
                        or -c:a (--conf:all) to specify both contexts at once.
                        Example:
                        -c="tools.cmake.cmaketoolchain:generator=Xcode"
  -c:b CONF_BUILD, --conf:build CONF_BUILD
  -c:h CONF_HOST, --conf:host CONF_HOST
  -c:a CONF_ALL, --conf:all CONF_ALL

lockfile arguments:
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile. Use --lockfile="" to avoid
                        automatic use of existing 'conan.lock' file
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile

```

The command `conan workspace build` performs the equivalent of `conan build <package-path>` for every `package`
defined within the workspace in the correct order.

## conan workspace create

```text
$ conan workspace create -h
usage: conan workspace create [-h] [--out-file OUT_FILE]
                              [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                              [-cc CORE_CONF] [--pkg PKG] [-b BUILD]
                              [-r REMOTE | -nr] [-u [UPDATE]] [-pr PROFILE]
                              [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                              [-pr:a PROFILE_ALL] [-o OPTIONS]
                              [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                              [-o:a OPTIONS_ALL] [-s SETTINGS]
                              [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                              [-s:a SETTINGS_ALL] [-c CONF] [-c:b CONF_BUILD]
                              [-c:h CONF_HOST] [-c:a CONF_ALL] [-l LOCKFILE]
                              [--lockfile-partial]

Call "conan create" for packages in the workspace, in the correct order.
Packages will be created in the Conan cache, not locally

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
  --pkg PKG             Define specific packages
  -b BUILD, --build BUILD
                        Optional, specify which packages to build from source.
                        Combining multiple '--build' options on one command
                        line is allowed. Possible values: --build=never
                        Disallow build for all packages, use binary packages
                        or fail if a binary package is not found, it cannot be
                        combined with other '--build' options. --build=missing
                        Build packages from source whose binary package is not
                        found. --build=cascade Build packages from source that
                        have at least one dependency being built from source.
                        --build=[pattern] Build packages from source whose
                        package reference matches the pattern. The pattern
                        uses 'fnmatch' style wildcards, so '--build="*"' will
                        build everything from source. --build=~[pattern]
                        Excluded packages, which will not be built from the
                        source, whose package reference matches the pattern.
                        The pattern uses 'fnmatch' style wildcards.
                        --build=missing:[pattern] Build from source if a
                        compatible binary does not exist, only for packages
                        matching pattern. --build=compatible:[pattern]
                        (Experimental) Build from source if a compatible
                        binary does not exist, and the requested package is
                        invalid, the closest package binary following the
                        defined compatibility policies (method and
                        compatibility.py)

remote arguments:
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -u [UPDATE], --update [UPDATE]
                        Will install newer versions and/or revisions in the
                        local cache for the given reference name, or all
                        references in the graph if no argument is supplied.
                        When using version ranges, it will install the latest
                        version that satisfies the range. It will update to
                        the latest revision for the resolved version range.

profile arguments:
  -pr PROFILE, --profile PROFILE
                        Apply the specified profile. By default, or if
                        specifying -pr:h (--profile:host), it applies to the
                        host context. Use -pr:b (--profile:build) to specify
                        the build context, or -pr:a (--profile:all) to specify
                        both contexts at once
  -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
  -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
  -pr:a PROFILE_ALL, --profile:all PROFILE_ALL
  -o OPTIONS, --options OPTIONS
                        Apply the specified options. By default, or if
                        specifying -o:h (--options:host), it applies to the
                        host context. Use -o:b (--options:build) to specify
                        the build context, or -o:a (--options:all) to specify
                        both contexts at once. Example:
                        -o="pkg/*:with_qt=True"
  -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
  -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
  -o:a OPTIONS_ALL, --options:all OPTIONS_ALL
  -s SETTINGS, --settings SETTINGS
                        Apply the specified settings. By default, or if
                        specifying -s:h (--settings:host), it applies to the
                        host context. Use -s:b (--settings:build) to specify
                        the build context, or -s:a (--settings:all) to specify
                        both contexts at once. Example: -s="compiler=gcc"
  -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
  -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
  -s:a SETTINGS_ALL, --settings:all SETTINGS_ALL
  -c CONF, --conf CONF  Apply the specified conf. By default, or if specifying
                        -c:h (--conf:host), it applies to the host context.
                        Use -c:b (--conf:build) to specify the build context,
                        or -c:a (--conf:all) to specify both contexts at once.
                        Example:
                        -c="tools.cmake.cmaketoolchain:generator=Xcode"
  -c:b CONF_BUILD, --conf:build CONF_BUILD
  -c:h CONF_HOST, --conf:host CONF_HOST
  -c:a CONF_ALL, --conf:all CONF_ALL

lockfile arguments:
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile. Use --lockfile="" to avoid
                        automatic use of existing 'conan.lock' file
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile

```

The command `conan workspace create` performs the equivalent of `conan create <package-path>` for every `package`
defined within the workspace in the correct order. They will be created in the Conan cache, not locally.

## conan workspace super-install

```text
$ conan workspace super-install -h
usage: conan workspace super-install [-h] [-f FORMAT] [--out-file OUT_FILE]
                                     [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                                     [-cc CORE_CONF] [--pkg PKG]
                                     [-g GENERATOR] [-of OUTPUT_FOLDER]
                                     [-d DEPLOYER]
                                     [--deployer-folder DEPLOYER_FOLDER]
                                     [--deployer-package DEPLOYER_PACKAGE]
                                     [--envs-generation {false}] [-b BUILD]
                                     [-r REMOTE | -nr] [-u [UPDATE]]
                                     [-pr PROFILE] [-pr:b PROFILE_BUILD]
                                     [-pr:h PROFILE_HOST] [-pr:a PROFILE_ALL]
                                     [-o OPTIONS] [-o:b OPTIONS_BUILD]
                                     [-o:h OPTIONS_HOST] [-o:a OPTIONS_ALL]
                                     [-s SETTINGS] [-s:b SETTINGS_BUILD]
                                     [-s:h SETTINGS_HOST] [-s:a SETTINGS_ALL]
                                     [-c CONF] [-c:b CONF_BUILD]
                                     [-c:h CONF_HOST] [-c:a CONF_ALL]
                                     [-l LOCKFILE] [--lockfile-partial]
                                     [--lockfile-out LOCKFILE_OUT]
                                     [--lockfile-clean]
                                     [--lockfile-overrides LOCKFILE_OVERRIDES]

Install the workspace as a monolith, installing only external dependencies to
the workspace, generating a single result (generators, etc) for the whole
workspace.

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
  --pkg PKG             Define specific packages
  -g GENERATOR, --generator GENERATOR
                        Generators to use
  -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        The root output folder for generated and build files
  -d DEPLOYER, --deployer DEPLOYER
                        Deploy using the provided deployer to the output
                        folder. Built-in deployers: 'full_deploy',
                        'direct_deploy', 'runtime_deploy'
  --deployer-folder DEPLOYER_FOLDER
                        Deployer output folder, base build folder by default
                        if not set
  --deployer-package DEPLOYER_PACKAGE
                        Execute the deploy() method of the packages matching
                        the provided patterns
  --envs-generation {false}
                        Generation strategy for virtual environment files for
                        the root
  -b BUILD, --build BUILD
                        Optional, specify which packages to build from source.
                        Combining multiple '--build' options on one command
                        line is allowed. Possible values: --build=never
                        Disallow build for all packages, use binary packages
                        or fail if a binary package is not found, it cannot be
                        combined with other '--build' options. --build=missing
                        Build packages from source whose binary package is not
                        found. --build=cascade Build packages from source that
                        have at least one dependency being built from source.
                        --build=[pattern] Build packages from source whose
                        package reference matches the pattern. The pattern
                        uses 'fnmatch' style wildcards, so '--build="*"' will
                        build everything from source. --build=~[pattern]
                        Excluded packages, which will not be built from the
                        source, whose package reference matches the pattern.
                        The pattern uses 'fnmatch' style wildcards.
                        --build=missing:[pattern] Build from source if a
                        compatible binary does not exist, only for packages
                        matching pattern. --build=compatible:[pattern]
                        (Experimental) Build from source if a compatible
                        binary does not exist, and the requested package is
                        invalid, the closest package binary following the
                        defined compatibility policies (method and
                        compatibility.py)

remote arguments:
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -u [UPDATE], --update [UPDATE]
                        Will install newer versions and/or revisions in the
                        local cache for the given reference name, or all
                        references in the graph if no argument is supplied.
                        When using version ranges, it will install the latest
                        version that satisfies the range. It will update to
                        the latest revision for the resolved version range.

profile arguments:
  -pr PROFILE, --profile PROFILE
                        Apply the specified profile. By default, or if
                        specifying -pr:h (--profile:host), it applies to the
                        host context. Use -pr:b (--profile:build) to specify
                        the build context, or -pr:a (--profile:all) to specify
                        both contexts at once
  -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
  -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
  -pr:a PROFILE_ALL, --profile:all PROFILE_ALL
  -o OPTIONS, --options OPTIONS
                        Apply the specified options. By default, or if
                        specifying -o:h (--options:host), it applies to the
                        host context. Use -o:b (--options:build) to specify
                        the build context, or -o:a (--options:all) to specify
                        both contexts at once. Example:
                        -o="pkg/*:with_qt=True"
  -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
  -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
  -o:a OPTIONS_ALL, --options:all OPTIONS_ALL
  -s SETTINGS, --settings SETTINGS
                        Apply the specified settings. By default, or if
                        specifying -s:h (--settings:host), it applies to the
                        host context. Use -s:b (--settings:build) to specify
                        the build context, or -s:a (--settings:all) to specify
                        both contexts at once. Example: -s="compiler=gcc"
  -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
  -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
  -s:a SETTINGS_ALL, --settings:all SETTINGS_ALL
  -c CONF, --conf CONF  Apply the specified conf. By default, or if specifying
                        -c:h (--conf:host), it applies to the host context.
                        Use -c:b (--conf:build) to specify the build context,
                        or -c:a (--conf:all) to specify both contexts at once.
                        Example:
                        -c="tools.cmake.cmaketoolchain:generator=Xcode"
  -c:b CONF_BUILD, --conf:build CONF_BUILD
  -c:h CONF_HOST, --conf:host CONF_HOST
  -c:a CONF_ALL, --conf:all CONF_ALL

lockfile arguments:
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile. Use --lockfile="" to avoid
                        automatic use of existing 'conan.lock' file
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile
  --lockfile-out LOCKFILE_OUT
                        Filename of the updated lockfile
  --lockfile-clean      Remove unused entries from the lockfile
  --lockfile-overrides LOCKFILE_OVERRIDES
                        Overwrite lockfile overrides

```

The command `conan workspace super-install` is useful to install and build the current workspace
as a monolithic super-project of the editables.

By default it uses all the `editable` packages in the workspace. It is possible to select
only a subset of them with the `conan workspace super-install --pkg=pkg_name1 --pkg=pkg_name2` optional
arguments. Only the subgraph of those packages, including their dependencies and transitive
dependencies will be installed.

<a id="workspace-complete-command"></a>

## conan workspace complete

```text
$ conan workspace complete -h
usage: conan workspace complete [-h] [--out-file OUT_FILE]
                                [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                                [-cc CORE_CONF] [-b BUILD] [-r REMOTE | -nr]
                                [-u [UPDATE]] [-pr PROFILE]
                                [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST]
                                [-pr:a PROFILE_ALL] [-o OPTIONS]
                                [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                                [-o:a OPTIONS_ALL] [-s SETTINGS]
                                [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                                [-s:a SETTINGS_ALL] [-c CONF]
                                [-c:b CONF_BUILD] [-c:h CONF_HOST]
                                [-c:a CONF_ALL] [-l LOCKFILE]
                                [--lockfile-partial]

Complete the workspace, opening or adding intermediate packages to it that
have requirements to other packages in the workspace.

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
  -b BUILD, --build BUILD
                        Optional, specify which packages to build from source.
                        Combining multiple '--build' options on one command
                        line is allowed. Possible values: --build=never
                        Disallow build for all packages, use binary packages
                        or fail if a binary package is not found, it cannot be
                        combined with other '--build' options. --build=missing
                        Build packages from source whose binary package is not
                        found. --build=cascade Build packages from source that
                        have at least one dependency being built from source.
                        --build=[pattern] Build packages from source whose
                        package reference matches the pattern. The pattern
                        uses 'fnmatch' style wildcards, so '--build="*"' will
                        build everything from source. --build=~[pattern]
                        Excluded packages, which will not be built from the
                        source, whose package reference matches the pattern.
                        The pattern uses 'fnmatch' style wildcards.
                        --build=missing:[pattern] Build from source if a
                        compatible binary does not exist, only for packages
                        matching pattern. --build=compatible:[pattern]
                        (Experimental) Build from source if a compatible
                        binary does not exist, and the requested package is
                        invalid, the closest package binary following the
                        defined compatibility policies (method and
                        compatibility.py)

remote arguments:
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server
  -nr, --no-remote      Do not use remote, resolve exclusively in the cache
  -u [UPDATE], --update [UPDATE]
                        Will install newer versions and/or revisions in the
                        local cache for the given reference name, or all
                        references in the graph if no argument is supplied.
                        When using version ranges, it will install the latest
                        version that satisfies the range. It will update to
                        the latest revision for the resolved version range.

profile arguments:
  -pr PROFILE, --profile PROFILE
                        Apply the specified profile. By default, or if
                        specifying -pr:h (--profile:host), it applies to the
                        host context. Use -pr:b (--profile:build) to specify
                        the build context, or -pr:a (--profile:all) to specify
                        both contexts at once
  -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
  -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
  -pr:a PROFILE_ALL, --profile:all PROFILE_ALL
  -o OPTIONS, --options OPTIONS
                        Apply the specified options. By default, or if
                        specifying -o:h (--options:host), it applies to the
                        host context. Use -o:b (--options:build) to specify
                        the build context, or -o:a (--options:all) to specify
                        both contexts at once. Example:
                        -o="pkg/*:with_qt=True"
  -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
  -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
  -o:a OPTIONS_ALL, --options:all OPTIONS_ALL
  -s SETTINGS, --settings SETTINGS
                        Apply the specified settings. By default, or if
                        specifying -s:h (--settings:host), it applies to the
                        host context. Use -s:b (--settings:build) to specify
                        the build context, or -s:a (--settings:all) to specify
                        both contexts at once. Example: -s="compiler=gcc"
  -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
  -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
  -s:a SETTINGS_ALL, --settings:all SETTINGS_ALL
  -c CONF, --conf CONF  Apply the specified conf. By default, or if specifying
                        -c:h (--conf:host), it applies to the host context.
                        Use -c:b (--conf:build) to specify the build context,
                        or -c:a (--conf:all) to specify both contexts at once.
                        Example:
                        -c="tools.cmake.cmaketoolchain:generator=Xcode"
  -c:b CONF_BUILD, --conf:build CONF_BUILD
  -c:h CONF_HOST, --conf:host CONF_HOST
  -c:a CONF_ALL, --conf:all CONF_ALL

lockfile arguments:
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile. Use --lockfile="" to avoid
                        automatic use of existing 'conan.lock' file
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile

```

The `conan workspace complete` command is intended to complete the `conan workspace open/add` commands.
When there are packages in a workspace that have dependencies on some packages in the Conan cache, and in turn
those cache packages depend on packages that are in the workspace, this creates an undesired and risky situation.

Packages in the Conan cache must be reproducible, including their dependencies. Having binaries in the Conan cache
that build against headers and libraries in a workspace, that are not really packages yet, and might never be, is
a dangerous situation. It means that it is very easy to have Conan packages in the cache that build and link against
code and binaries that never exist in Conan, that are never uploaded as packages. When the cache packages are uploaded
and later deployed to production they will link and/or run with different packages, which can cause different issues,
from compile or link problems to very difficult to debug and understand runtime errors.

So when a Conan `workspace` command detects this situation, it will raise an error like:

```default
ERROR: Workspace definition error. Package mypkg/version in the Conan cache
has dependencies to packages in the workspace: ["dep1/1.0", "dep2/0.2"]
Try the 'conan workspace complete' to open/add intermediate packages
```

This could be solved by manually doing a `conan workspace open/add <dep>` for the missing packages, and
add them to the workspace, then repeat the previous command until the error is gone. The `conan workspace complete`
command is basically a helper to do this process automatically, detecting what are the missing packages
and adding all of them to the workspace.

#### SEE ALSO
- Read the [Workspace tutorial](https://docs.conan.io/2//tutorial/developing_packages/workspaces.html.md#tutorial-workspaces) section.
- Read the [conan new workspace](https://docs.conan.io/2//reference/commands/new.html.md#reference-commands-new) command section.
