.. _reference_commands_editable:

conan editable
==============

.. code-block:: bash

    $ conan editable --help
    usage: conan editable [-h] [-v [V]] [--logger] {add,list,remove} ...

    Allows working with a package in user folder

    positional arguments:
    {add,list,remove}  sub-command help
        add              Define the given <path> location as the package <reference>, so when this package is required, it is
                        used from this <path> location instead of from the cache
        list             List packages in editable mode
        remove           Remove the "editable" mode for this reference.

    optional arguments:
    -h, --help         show this help message and exit
    -v [V]             Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror,
                        -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger           Show the output with log format, with time, type and message.
