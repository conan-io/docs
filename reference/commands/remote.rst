.. _reference_commands_remote:

conan remote
============

Use this command to add, edit and remove Conan repositories from the Conan remote
registry and also manage authentication to those remotes. For more information on how to
work with Conan repositories, please check the :ref:`dedicated section <conan_repositories>`.

..  code-block:: text

    $ conan remote -h
    usage: conan remote [-h] [-v [V]] [--logger] {add,auth,disable,enable,list,list-users,login,logout,remove,rename,set-user,update} ...

    Manage the remote list and the users authenticated on them.

    positional arguments:
    {add,auth,disable,enable,list,list-users,login,logout,remove,rename,set-user,update}
                            sub-command help
        add                 Add a remote.
        auth                Authenticate in the defined remotes
        disable             Disable all the remotes matching a pattern.
        enable              Enable all the remotes matching a pattern.
        list                List current remotes.
        list-users          List the users logged into all the remotes.
        login               Login into the specified remotes matching a pattern.
        logout              Clear the existing credentials for the specified remotes matching a pattern.
        remove              Remove a remote.
        rename              Rename a remote.
        set-user            Associate a username with a remote matching a pattern without performing the authentication.
        update              Update a remote.

    optional arguments:
    -h, --help            show this help message and exit
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.



conan remote add
----------------

..  code-block:: text

    $ conan remote add -h
    usage: conan remote add [-h] [-i [INSERT]] [-f] remote url [verify_ssl]

    positional arguments:
      remote                Name of the remote
      url                   URL of the remote
      verify_ssl            Verify SSL certificate. Defaulted to True

    optional arguments:
      -h, --help            show this help message and exit
      -i [INSERT], --insert [INSERT]
                            insert remote at specific index
      -f, --force           Force addition, will update if existing


conan remote auth
-----------------

..  code-block:: text

    $ conan remote auth -h
    usage: conan remote auth [-h] [-v [V]] [--logger] [--with-user] remote

    Authenticate in the defined remotes

    positional arguments:
    remote       Pattern of the remote/s to disable. The pattern uses 'fnmatch' style wildcards.

    optional arguments:
    -h, --help   show this help message and exit
    -v [V]       Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice,
                -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger     Show the output with log format, with time, type and message.
    --with-user  Only try to auth in those remotes that already have a username or a CONAN_LOGIN_ env-var defined


conan remote disable
--------------------

..  code-block:: text

    $ conan remote disable -h
    usage: conan remote disable [-h] [-v [V]] [--logger] remote

    Disable all the remotes matching a pattern.

    positional arguments:
      remote      Pattern of the remote/s to disable. The pattern uses 'fnmatch'
                  style wildcards.

    optional arguments:
      -h, --help  show this help message and exit
      -v [V]      Level of detail of the output. Valid options from less verbose
                  to more verbose: -vquiet, -verror, -vwarning, -vnotice,
                  -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
      --logger    Show the output with log format, with time, type and message.


conan remote enable
-------------------

.. code-block:: text

    $ conan remote enable -h
    usage: conan remote enable [-h] [-v [V]] [--logger] remote

    Enable all the remotes matching a pattern.

    positional arguments:
      remote      Pattern of the remote/s to enable. The pattern uses 'fnmatch'
                  style wildcards.

    optional arguments:
      -h, --help  show this help message and exit
      -v [V]      Level of detail of the output. Valid options from less verbose
                  to more verbose: -vquiet, -verror, -vwarning, -vnotice,
                  -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
      --logger    Show the output with log format, with time, type and message.


conan remote list
-----------------

..  code-block:: text

    $ conan remote list -h
    usage: conan remote list [-h] [-f FORMAT] [-v [V]] [--logger]

    List current remotes.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.


conan remote list-users
-----------------------

.. code-block:: text

    $ conan remote list-users -h
    usage: conan remote list-users [-h] [-f FORMAT] [-v [V]] [--logger]

    List the users logged into all the remotes.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.


conan remote login
------------------

.. code-block:: text

    $ conan remote login -h
    usage: conan remote login [-h] [-f FORMAT] [-v [V]] [--logger] [-p [PASSWORD]]
                              remote username

    Login into the specified remotes matching a pattern.

    positional arguments:
      remote                Pattern or name of the remote to login into. The
                            pattern uses 'fnmatch' style wildcards.
      username              Username

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.
      -p [PASSWORD], --password [PASSWORD]
                            User password. Use double quotes if password with
                            spacing, and escape quotes if existing. If empty, the
                            password is requested interactively (not exposed)


conan remote logout
-------------------

.. code-block:: text

    $ conan remote logout -h
    usage: conan remote logout [-h] [-f FORMAT] [-v [V]] [--logger] remote

    Clear the existing credentials for the specified remotes matching a pattern.

    positional arguments:
      remote                Pattern or name of the remote to logout. The pattern
                            uses 'fnmatch' style wildcards.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.


conan remote remove
-------------------

.. code-block:: text

    $ conan remote remove -h
    usage: conan remote remove [-h] [-v [V]] [--logger] remote

    Remove a remote.

    positional arguments:
      remote      Name of the remote to remove. Accepts 'fnmatch' style wildcards.

    optional arguments:
      -h, --help  show this help message and exit
      -v [V]      Level of detail of the output. Valid options from less verbose
                  to more verbose: -vquiet, -verror, -vwarning, -vnotice,
                  -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
      --logger    Show the output with log format, with time, type and message.


conan remote rename
-------------------

.. code-block:: text

    $ conan remote rename -h
    usage: conan remote rename [-h] [-v [V]] [--logger] remote new_name

    Rename a remote.

    positional arguments:
      remote      Current name of the remote
      new_name    New name for the remote

    optional arguments:
      -h, --help  show this help message and exit
      -v [V]      Level of detail of the output. Valid options from less verbose
                  to more verbose: -vquiet, -verror, -vwarning, -vnotice,
                  -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
      --logger    Show the output with log format, with time, type and message.


conan remote set-user
---------------------

.. code-block:: text

    $ conan remote set-user -h
    usage: conan remote set-user [-h] [-f FORMAT] [-v [V]] [--logger]
                                 remote username

    Associate a username with a remote matching a pattern without performing the
    authentication.

    positional arguments:
      remote                Pattern or name of the remote. The pattern uses
                            'fnmatch' style wildcards.
      username              Username

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.


conan remote update
-------------------

.. code-block:: text

    $ conan remote update -h
    usage: conan remote update [-h] [-v [V]] [--logger] [--url URL] [--secure]
                               [--insecure] [--index INDEX]
                               remote

    Update a remote.

    positional arguments:
      remote         Name of the remote to update

    optional arguments:
      -h, --help     show this help message and exit
      -v [V]         Level of detail of the output. Valid options from less
                     verbose to more verbose: -vquiet, -verror, -vwarning,
                     -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or
                     -vtrace
      --logger       Show the output with log format, with time, type and message.
      --url URL      New url for the remote
      --secure       Don't allow insecure server connections when using SSL
      --insecure     Allow insecure server connections when using SSL
      --index INDEX  Insert the remote at a specific position in the remote list


Read more
---------

- :ref:`Uploading packages tutorial <uploading_packages>`
- :ref:`Working with Conan repositories <conan_repositories>`
- :ref:`Upload Conan packages to remotes using conan upload command <reference_commands_upload>`
