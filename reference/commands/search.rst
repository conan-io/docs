conan search
============

Search existing recipes in remotes.
This command is equivalent to ``conan list recipes <query> -r=*``, and is provided for simpler UX.

.. code-block:: bash

    conan search -h
    usage: conan search [-h] [-f {cli,json}] [-r REMOTE] query

    Searches for package recipes in a remote or remotes

    positional arguments:
    query                 Search query to find package recipe reference, e.g., 'boost', 'lib*'

    optional arguments:
    -h, --help            show this help message and exit
    -f {cli,json}, --format {cli,json}
                            Select the output format: cli, json. 'cli' is the default output.
    -r REMOTE, --remote REMOTE
                            Remote names. Accepts wildcards. If not specified it searches in all remotes



.. code-block:: bash

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
