<a id="reference-commands-remote"></a>

# conan remote

Use this command to add, edit and remove Conan repositories from the Conan remote
registry and also manage authentication to those remotes. For more information on how to
work with Conan repositories, please check the [dedicated section](https://docs.conan.io/2//tutorial/conan_repositories.html.md#conan-repositories).

```text
$ conan remote -h
usage: conan remote [-h] [--out-file OUT_FILE]
                    [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                    [-cc CORE_CONF]
                    {add,auth,disable,enable,list,list-users,login,logout,remove,rename,set-user,update}
                    ...

Manage the remote list and the users authenticated on them.

positional arguments:
  {add,auth,disable,enable,list,list-users,login,logout,remove,rename,set-user,update}
                        sub-command help
    add                 Add a remote.
    auth                Authenticate in the defined remotes. Use
                        CONAN_LOGIN_USERNAME* and CONAN_PASSWORD* variables if
                        available. Ask for username and password interactively
                        in case (re-)authentication is required and there are
                        no CONAN_LOGIN* and CONAN_PASSWORD* variables
                        available which could be used. Usually you'd use this
                        method over conan remote login for scripting which
                        needs to run in CI and locally.
    disable             Disable all the remotes matching a pattern.
    enable              Enable all the remotes matching a pattern.
    list                List current remotes.
    list-users          List the users logged into all the remotes.
    login               Login into the specified remotes matching a pattern.
    logout              Clear the existing credentials for the specified
                        remotes matching a pattern.
    remove              Remove remotes.
    rename              Rename a remote.
    set-user            Associate a username with a remote matching a pattern
                        without performing the authentication.
    update              Update a remote.

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

## conan remote add

```text
$ conan remote add -h
usage: conan remote add [-h] [--out-file OUT_FILE]
                        [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                        [-cc CORE_CONF] [--insecure] [--index INDEX] [-f]
                        [-ap ALLOWED_PACKAGES] [-t {local-recipes-index}]
                        [--recipes-only]
                        name url

Add a remote.

positional arguments:
  name                  Name of the remote to add
  url                   Url of the remote

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
  --insecure            Allow insecure server connections when using SSL
  --index INDEX         Insert the remote at a specific position in the remote
                        list
  -f, --force           Force the definition of the remote even if duplicated
  -ap ALLOWED_PACKAGES, --allowed-packages ALLOWED_PACKAGES
                        Add recipe reference pattern to list of allowed
                        packages for this remote
  -t {local-recipes-index}, --type {local-recipes-index}
                        Define the remote type
  --recipes-only        Disallow binary downloads from this remote, only
                        recipes will be downloaded

```

## conan remote auth

```text
$ conan remote auth -h
usage: conan remote auth [-h] [-f FORMAT] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF] [--with-user] [--force]
                         remote

Authenticate in the defined remotes. Use CONAN_LOGIN_USERNAME* and
CONAN_PASSWORD* variables if available. Ask for username and password
interactively in case (re-)authentication is required and there are no
CONAN_LOGIN* and CONAN_PASSWORD* variables available which could be used.
Usually you'd use this method over conan remote login for scripting which
needs to run in CI and locally.

positional arguments:
  remote                Pattern or name of the remote/s to authenticate
                        against. The pattern uses 'fnmatch' style wildcards.

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
  --with-user           Only try to auth in those remotes that already have a
                        username or a CONAN_LOGIN_USERNAME* env-var defined
  --force               Force authentication for anonymous-enabled
                        repositories. Can be used for force authentication in
                        case your Artifactory instance has anonymous access
                        enabled and Conan would not ask for username and
                        password even for non-anonymous repositories if not
                        yet authenticated.

```

#### NOTE
If a remote which allows anonymous access matches the pattern given to the command, Conan won’t try to authenticate with it by default.
If you want to authenticate with a remote that allows anonymous access, you can use the `--force` option.

## conan remote disable

```text
$ conan remote disable -h
usage: conan remote disable [-h] [-f FORMAT] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF]
                            remote

Disable all the remotes matching a pattern.

positional arguments:
  remote                Pattern of the remote/s to disable. The pattern uses
                        'fnmatch' style wildcards.

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

## conan remote enable

```text
$ conan remote enable -h
usage: conan remote enable [-h] [-f FORMAT] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF]
                           remote

Enable all the remotes matching a pattern.

positional arguments:
  remote                Pattern of the remote/s to enable. The pattern uses
                        'fnmatch' style wildcards.

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

## conan remote list

```text
$ conan remote list -h
usage: conan remote list [-h] [-f FORMAT] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF]

List current remotes.

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

## conan remote list-users

```text
$ conan remote list-users -h
usage: conan remote list-users [-h] [-f FORMAT] [--out-file OUT_FILE]
                               [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                               [-cc CORE_CONF]

List the users logged into all the remotes.

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

## conan remote login

```text
$ conan remote login -h
usage: conan remote login [-h] [-f FORMAT] [--out-file OUT_FILE]
                          [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                          [-cc CORE_CONF] [-p [PASSWORD]]
                          remote [username]

Login into the specified remotes matching a pattern.

positional arguments:
  remote                Pattern or name of the remote to login into. The
                        pattern uses 'fnmatch' style wildcards.
  username              Username

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
  -p [PASSWORD], --password [PASSWORD]
                        User password. Use double quotes if password with
                        spacing, and escape quotes if existing. If empty, the
                        password is requested interactively (not exposed)

```

## conan remote logout

```text
$ conan remote logout -h
usage: conan remote logout [-h] [-f FORMAT] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF]
                           remote

Clear the existing credentials for the specified remotes matching a pattern.

positional arguments:
  remote                Pattern or name of the remote to logout. The pattern
                        uses 'fnmatch' style wildcards.

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

## conan remote remove

```text
$ conan remote remove -h
usage: conan remote remove [-h] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF]
                           remote

Remove remotes.

positional arguments:
  remote                Name of the remote to remove. Accepts 'fnmatch' style
                        wildcards.

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

## conan remote rename

```text
$ conan remote rename -h
usage: conan remote rename [-h] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF]
                           remote new_name

Rename a remote.

positional arguments:
  remote                Current name of the remote
  new_name              New name for the remote

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

## conan remote set-user

```text
$ conan remote set-user -h
usage: conan remote set-user [-h] [-f FORMAT] [--out-file OUT_FILE]
                             [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                             [-cc CORE_CONF]
                             remote username

Associate a username with a remote matching a pattern without performing the
authentication.

positional arguments:
  remote                Pattern or name of the remote. The pattern uses
                        'fnmatch' style wildcards.
  username              Username

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

## conan remote update

```text
$ conan remote update -h
usage: conan remote update [-h] [--out-file OUT_FILE]
                           [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                           [-cc CORE_CONF] [--url URL] [--secure] [--insecure]
                           [--index INDEX] [-ap ALLOWED_PACKAGES]
                           [--recipes-only [{True,False}]]
                           remote

Update a remote.

positional arguments:
  remote                Name of the remote to update

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
  --url URL             New url for the remote
  --secure              Don't allow insecure server connections when using SSL
  --insecure            Allow insecure server connections when using SSL
  --index INDEX         Insert the remote at a specific position in the remote
                        list
  -ap ALLOWED_PACKAGES, --allowed-packages ALLOWED_PACKAGES
                        Add recipe reference pattern to the list of allowed
                        packages for this remote
  --recipes-only [{True,False}]
                        Disallow binary downloads from this remote, only
                        recipes will be downloaded

```

#### SEE ALSO
- [Uploading packages tutorial](https://docs.conan.io/2//tutorial/conan_repositories/uploading_packages.html.md#uploading-packages)
- [Working with Conan repositories](https://docs.conan.io/2//tutorial/conan_repositories.html.md#conan-repositories)
- [Upload Conan packages to remotes using conan upload command](https://docs.conan.io/2//reference/commands/upload.html.md#reference-commands-upload)
