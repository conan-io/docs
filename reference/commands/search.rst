.. _reference_commands_search:

conan search
============

Search existing recipes in remotes.
This command is equivalent to ``conan list recipes <query> -r=*``, and is provided for simpler UX.

.. code-block:: text

    $ conan search -h
    usage: conan search [-h] [-f FORMAT] [-v [V]] [-r REMOTE] reference

    Search for package recipes in all the remotes (by default), or a remote.

    positional arguments:
      reference             Recipe reference to search for.It can contain * as
                            wildcard at any reference field.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      -r REMOTE, --remote REMOTE
                            Remote names. Accepts wildcards. If not specified it
                            searches in all the remotes



.. code-block:: text

    $ conan search zlib
    conancenter:
    zlib
        zlib/1.2.11
        zlib/1.2.8

    $ conan search zlib -r=conancenter
    conancenter:
    zlib
        zlib/1.2.11
        zlib/1.2.8

    $ conan search zlib/1.2.1* -r=conancenter
    conancenter:
    zlib
        zlib/1.2.11

    $ conan search zlib/1.2.1* -r=conancenter --format=json
    [
        {
            "remote": "conancenter",
            "error": null,
            "results": [
                {
                    "name": "zlib",
                    "id": "zlib/1.2.11"
                }
            ]
        }
    ]
