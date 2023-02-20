.. _reference_commands_inspect:

conan inspect
=============

.. code-block:: bash

    $ conan inspect -h
    usage: conan inspect [-h] [-f FORMAT] [-v [V]] [--logger] path

    Inspect a conanfile.py to return its public fields.

    positional arguments:
      path                  Path to a folder containing a recipe (conanfile.py)

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
