.. _reference_commands_download:

conan download
==============

.. code-block:: text

    $ conan download -h
    usage: conan download [-h] [-v [V]] [--logger] [--only-recipe]
                          [-p PACKAGE_QUERY] -r REMOTE
                          reference

    Download (without installing) a single conan package from a remote server.

    It downloads just the package, but not its transitive dependencies, and it will not call
    any generate, generators or deployers.
    It can download multiple packages if patterns are used, and also works with queries over
    the package binaries.

    positional arguments:
      reference             Recipe reference or package reference, can contain *
                            as wildcard at any reference field. If revision is not
                            specified, it is assumed latest one.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.
      --only-recipe         Download only the recipe/s, not the binary packages.
      -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                            Only upload packages matching a specific query. e.g:
                            os=Windows AND (arch=x86 OR compiler=gcc)
      -r REMOTE, --remote REMOTE
                            Download from this specific remote
