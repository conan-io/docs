.. _reference_commands_editable:

conan editable
==============

.. code-block:: bash

    $ conan editable --help
    usage: conan editable [-h] [-v [V]] [--logger] {add,list,remove} ...

    Allows working with a package in user folder

    positional arguments:
    {add,list,remove}  sub-command help
        add              Define the given <path> location as the package <reference>, so when this package is required, it is used from
                        this <path> location instead of from the cache
        list             List packages in editable mode
        remove           Remove the "editable" mode for this reference.

    optional arguments:
    -h, --help         show this help message and exit
    -v [V]             Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger           Show the output with log format, with time, type and message.

conan editable add
------------------

.. code-block:: bash

    $ conan editable add --help
    usage: conan editable add [-h] [-v [V]] [--logger] [--name NAME] [--version VERSION] [--user USER] [--channel CHANNEL]
                            [-of OUTPUT_FOLDER]
                            path

    Define the given <path> location as the package <reference>, so when this package is required, it is used from this <path> location
    instead of from the cache

    positional arguments:
    path                  Path to the package folder in the user workspace

    optional arguments:
    -h, --help            show this help message and exit
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.
    --name NAME           Provide a package name if not specified in conanfile
    --version VERSION     Provide a package version if not specified in conanfile
    --user USER           Provide a user if not specified in conanfile
    --channel CHANNEL     Provide a channel if not specified in conanfil
    -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                            The root output folder for generated and build files

conan editable remove
---------------------

.. code-block:: bash

    $ conan editable remove --help
    usage: conan editable remove [-h] [-v [V]] [--logger] [-r REFS] [path]

    Remove the "editable" mode for this reference.

    positional arguments:
    path                  Path to a folder containing a recipe (conanfile.py or conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt.

    optional arguments:
    -h, --help            show this help message and exit
    -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.
    -r REFS, --refs REFS  Directly provide reference patterns
