.. _reference_commands_remote:

conan remote
============

Use this command to add, edit and remove remote repositories from the Conan remote
registry and also manage authentication to those remotes. For more information on how to
work with remote repositories, please check the :ref:`dedicated section
<remote_repositories>`.

.. code-block:: bash

    $ conan remote --help
    usage: conan remote [-h] [-v [V]] [--logger] {add,disable,enable,list,list-users,login,logout,remove,rename,set-user,update} ...

    Manages the remote list and the users authenticated on them.

    positional arguments:
    {add,disable,enable,list,list-users,login,logout,remove,rename,set-user,update}
                            sub-command help
        add                 Add a remote
        disable             Disable all the remotes matching a pattern
        enable              Enable all the remotes matching a pattern
        list                List current remotes
        list-users          List the users logged into the remotes
        login               Login into the specified remotes
        logout              Clear the existing credentials for the specified remotes
        remove              Remove a remote
        rename              Rename a remote
        set-user            Associates a username with a remote without performing the authentication
        update              Update the remote

    optional arguments:
    -h, --help            show this help message and exit
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.


conan remote add
----------------

.. code-block:: bash

    $ conan remote add --help
    usage: conan remote add [-h] [-v [V]] [--logger] [--insecure] [--index INDEX] name url

    Add a remote

    positional arguments:
    name           Name of the remote to add
    url            Url of the remote

    optional arguments:
    -h, --help     show this help message and exit
    -v [V]         Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger       Show the output with log format, with time, type and message.
    --insecure     Allow insecure server connections when using SSL
    --index INDEX  Insert the remote at a specific position in the remote list 


conan remote disable
--------------------

.. code-block:: bash

    $ conan remote disable --help
    usage: conan remote disable [-h] [-v [V]] [--logger] remote

    Disable all the remotes matching a pattern

    positional arguments:
    remote      Pattern of the remote/s to disable. The pattern uses 'fnmatch' style wildcards.

    optional arguments:
    -h, --help  show this help message and exit
    -v [V]      Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger    Show the output with log format, with time, type and message.


conan remote enable
-------------------

.. code-block:: bash

    $ conan remote enable --help 
    usage: conan remote enable [-h] [-v [V]] [--logger] remote

    Enable all the remotes matching a pattern

    positional arguments:
    remote      Pattern of the remote/s to enable. The pattern uses 'fnmatch' style wildcards.

    optional arguments:
    -h, --help  show this help message and exit
    -v [V]      Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger    Show the output with log format, with time, type and message.


conan remote list
-----------------

.. code-block:: bash

    $ conan remote list --help  
    usage: conan remote list [-h] [-f FORMAT] [-v [V]] [--logger]

    List current remotes

    optional arguments:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Select the output format: json
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.


conan remote list-users
-----------------------

.. code-block:: bash

    $ conan remote list-users --help
    usage: conan remote list-users [-h] [-f FORMAT] [-v [V]] [--logger]

    List the users logged into the remotes

    optional arguments:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Select the output format: json
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.


conan remote login
------------------

.. code-block:: bash

    $ conan remote login --help     
    usage: conan remote login [-h] [-f FORMAT] [-v [V]] [--logger] [-p [PASSWORD]] remote username

    Login into the specified remotes

    positional arguments:
    remote                Pattern or name of the remote to login into. The pattern uses 'fnmatch' style wildcards.
    username              Username

    optional arguments:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Select the output format: json
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.
    -p [PASSWORD], --password [PASSWORD]
                            User password. Use double quotes if password with spacing, and escape quotes if existing. If empty, the password is requested interactively (not exposed)


conan remote logout
-------------------

.. code-block:: bash

    $ conan remote logout --help
    usage: conan remote logout [-h] [-f FORMAT] [-v [V]] [--logger] remote

    Clear the existing credentials for the specified remotes

    positional arguments:
    remote                Pattern or name of the remote to logout. The pattern uses 'fnmatch' style wildcards.

    optional arguments:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Select the output format: json
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.


conan remote remove
-------------------

.. code-block:: bash

    $ conan remote remove --help
    usage: conan remote remove [-h] [-v [V]] [--logger] remote

    Remove a remote

    positional arguments:
    remote      Name of the remote to remove. Accepts 'fnmatch' style wildcards.

    optional arguments:
    -h, --help  show this help message and exit
    -v [V]      Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger    Show the output with log format, with time, type and message.


conan remote rename
-------------------

.. code-block:: bash

    $ conan remote rename --help
    usage: conan remote rename [-h] [-v [V]] [--logger] remote new_name

    Rename a remote

    positional arguments:
    remote      Current name of the remote
    new_name    New name for the remote

    optional arguments:
    -h, --help  show this help message and exit
    -v [V]      Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger    Show the output with log format, with time, type and message.


conan remote set-user
---------------------

.. code-block:: bash

    $ conan remote set-user --help
    usage: conan remote set-user [-h] [-f FORMAT] [-v [V]] [--logger] remote username

    Associates a username with a remote without performing the authentication

    positional arguments:
    remote                Pattern or name of the remote. The pattern uses 'fnmatch' style wildcards.
    username              Username

    optional arguments:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Select the output format: json
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.


conan remote update
-------------------

.. code-block:: bash

    $ conan remote update --help  
    usage: conan remote update [-h] [-v [V]] [--logger] [--url URL] [--secure] [--insecure] [--index INDEX] remote

    Update the remote

    positional arguments:
    remote         Name of the remote to update

    optional arguments:
    -h, --help     show this help message and exit
    -v [V]         Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger       Show the output with log format, with time, type and message.
    --url URL      New url for the remote
    --secure       Don\'t allow insecure server connections when using SSL
    --insecure     Allow insecure server connections when using SSL
    --index INDEX  Insert the remote at a specific position in the remote list
