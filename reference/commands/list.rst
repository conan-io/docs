conan list
==========

.. code-block:: bash

    $ conan list -h
    usage: conan list [-h] [-f FORMAT] [-v [V]] [--logger] [-p PACKAGE_QUERY] [-r REMOTE] [-c] reference

    Lists existing recipes, revisions or packages in the cache or in remotes given a complete
    reference or a pattern.

    positional arguments:
      reference             Recipe reference or package reference. Both can contain * as wildcard at any reference field. If
                            revision is not specified, it is assumed latest one.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json, html
      -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror,
                            -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
      --logger              Show the output with log format, with time, type and message.
      -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                            Only list packages matching a specific query. e.g: os=Windows AND (arch=x86 OR compiler=gcc)
      -r REMOTE, --remote REMOTE
                            Remote names. Accepts wildcards
      -c, --cache           Search in the local cache


The ``conan list`` command is an wide-area command, and it can list recipes and packages
from the local cache or from any specified remotes. Depending on the patterns specified as argument and taking into
account that a complete Conan reference looks like this ``name/version@use/channel#rrev:pkgid#prev``,
it is possible to list:

* Recipe references (``name/version@user/channel``).
* Recipe revisions (``#rrev``).
* Package IDs and their configurations (``:pkgids``).
* Package revisions (``#prev``).


Use cases
---------

Show recipe references
**********************

.. code-block:: bash

    $ conan list *
    Local Cache:
      hello
        hello/1.0
        hello/2.0
      string-view-lite
        string-view-lite/1.6.0
      zlib
        zlib/1.2.11


.. code-block:: bash

    $ conan list zlib/*
    Local Cache:
      zlib
        zlib/1.2.11

Show recipe revisions
*********************

Show all the recipe revisions:

.. code-block:: bash

    $ conan list zlib/1.2.11#*
    Local Cache:
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)

Show all the LATEST recipe revisions given a pattern:

.. code-block:: bash

    $ conan list *#latest
    Local Cache:
      hello
        hello/1.0#fa5f6b17d0adc4de6030c9ab71cdbede (2022-12-23 14:38:31 UTC)
        hello/2.0#e1879dd51f0e775dbe816cb527d3f26d (2022-12-23 10:57:48 UTC)
      string-view-lite
        string-view-lite/1.6.0#5e4595946a0836fff9e8e376977f6715 (2022-08-25 22:38:53 UTC)
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)

Show package IDs
****************

If recipe revision is not specified, even with a pattern, it assumes the LATEST one.

.. code-block:: bash

    $ conan list zlib/1.2.11:*
    Local Cache:
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)
          PID: d0599452a426a161e02a297c6e0c5070f99b4909 (2022-11-18 12:33:31 UTC)
            settings:
              arch=x86_64
              build_type=Release
              compiler=apple-clang
              compiler.version=12.0
              os=Macos
            options:
              fPIC=True
              shared=False

Show package revisions
**********************

Show all the package revisions:

.. code-block:: bash

    $ conan list zlib/1.2.11:*#*
    Local Cache:
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)
          PID: d0599452a426a161e02a297c6e0c5070f99b4909
            PREV: 4834a9b0d050d7cf58c3ab391fe32e25 (2022-11-18 12:33:31 UTC)

Show all the LATEST package revisions given a pattern:

.. code-block:: bash

    $ conan list "*:*#latest"
    Local Cache:
      hello
        hello/1.0#fa5f6b17d0adc4de6030c9ab71cdbede (2022-12-23 14:38:31 UTC)
          PID: fdb823f07bc228621617c6397210a5c6c4c8807b
            PREV: 8267c08c7268887f4a066c87941e9d34 (2022-12-23 14:38:32 UTC)
        hello/2.0#e1879dd51f0e775dbe816cb527d3f26d (2022-12-23 10:57:48 UTC)
          There are no packages for this revision.
      string-view-lite
        string-view-lite/1.6.0#5e4595946a0836fff9e8e376977f6715 (2022-08-25 22:38:53 UTC)
          PID: da39a3ee5e6b4b0d3255bfef95601890afd80709
            PREV: f069d90b5936d963a9d06c2586e959d6 (2022-11-18 11:54:58 UTC)
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)
          PID: d0599452a426a161e02a297c6e0c5070f99b4909
            PREV: 4834a9b0d050d7cf58c3ab391fe32e25 (2022-11-18 12:33:31 UTC)
