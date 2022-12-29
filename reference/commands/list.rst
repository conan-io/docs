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


The ``conan list`` command is a wide-area command, and it can list recipes and packages
from the local cache or from any specified remotes. Depending on the patterns specified as argument and taking into
account that a complete Conan reference looks like this ``name/version@use/channel#rrev:pkgid#prev``,
it is possible to list:

* Recipe references (``name/version@user/channel``).
* Recipe revisions (``#rrev``).
* Package IDs and their configurations (``:pkgids``).
* Package revisions (``#prev``).


Use cases
^^^^^^^^^

Show only recipe references (``name/version@use/channel``)
**********************************************************

All the existing recipe references (using different patterns)
-------------------------------------------------------------

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


.. code-block:: bash

    $ conan list hello/1.2.11@user/*
    Local Cache:
      hello
        hello/1.2.11@user/channel_1
        hello/1.2.11@user/channel_2


Show only recipe revisions (``name/version@use/channel#rrev``)
**************************************************************

Only the latest recipe revision
-------------------------------

.. code-block:: bash

    $ conan list zlib/1.2.11
    Local Cache:
      zlib
        zlib/1.2.11#ffa77daf83a57094149707928bdce823 (2022-11-02 13:46:53 UTC)


.. note::

    Here the ``#latest`` is implicit, i.e., that search is the same as put ``conan list zlib/1.2.11#latest``


All the recipe revisions
------------------------

.. code-block:: bash

    $ conan list zlib/1.2.11#*
    Local Cache:
      zlib
        zlib/1.2.11#ffa77daf83a57094149707928bdce823 (2022-11-02 13:46:53 UTC)
        zlib/1.2.11#8b23adc7acd6f1d6e220338a78e3a19e (2022-10-19 09:19:10 UTC)
        zlib/1.2.11#ce3665ce19f82598aa0f7ac0b71ee966 (2022-10-14 11:42:21 UTC)
        zlib/1.2.11#31ee767cb2828e539c42913a471e821a (2022-10-12 05:49:39 UTC)
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)


Show only package IDs (``name/version@use/channel#rrev:pkgid``)
***************************************************************

All the package IDs for the latest recipe revision
--------------------------------------------------

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

.. note::

    Here the ``#latest`` is implicit, i.e., that search is the same as put ``conan list zlib/1.2.11#latest:*``


All the package IDs for all recipe revisions
--------------------------------------------

.. code-block:: bash

    $ conan list zlib/1.2.11#*:*
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
        zlib/1.2.11#8b23adc7acd6f1d6e220338a78e3a19e (2022-08-05 17:17:30 UTC)
          PID: fdb823f07bc228621617c6397210a5c6c4c8807b (2022-11-18 12:33:31 UTC)
            settings:
              arch=x86_64
              build_type=Debug
              compiler=apple-clang
              compiler.version=12.0
              os=Macos
            options:
              fPIC=True
              shared=True


Show only package revisions (``name/version@use/channel#rrev:pkgid#prev``)
**************************************************************************


Only the latest package revision given a full package ID
--------------------------------------------------------

.. code-block:: bash

    $ conan list zlib/1.2.11#8b23adc7acd6f1d6e220338a78e3a19e:fdb823f07bc228621617c6397210a5c6c4c8807b
    Local Cache:
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)
          PID: d0599452a426a161e02a297c6e0c5070f99b4909
            PREV: 4834a9b0d050d7cf58c3ab391fe32e25 (2022-11-18 12:33:31 UTC)


All the package revisions for the latest recipe revision
--------------------------------------------------------

.. code-block:: bash

    $ conan list zlib/1.2.11:*#*
    Local Cache:
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)
          PID: d0599452a426a161e02a297c6e0c5070f99b4909
            PREV: 4834a9b0d050d7cf58c3ab391fe32e25 (2022-11-18 12:33:31 UTC)

.. note::

    Here the ``#latest`` is implicit, i.e., that search is the same as put ``conan list zlib/1.2.11#latest:*#*``
