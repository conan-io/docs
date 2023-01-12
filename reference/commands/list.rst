conan list
==========

.. code-block:: bash

    $ conan list -h
    usage: conan list [-h] [-f FORMAT] [-v [V]] [--logger] [-p PACKAGE_QUERY] [-r REMOTE] [-c] reference

    Lists existing recipes, revisions or packages in the cache or in remotes given a complete
    reference or a pattern.

    positional arguments:
      reference             Recipe reference or package reference. Both can contain * as wildcard at any reference field. If revision is not specified, it is assumed latest
                            one.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json, html
      -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose,
                            -vv or -vdebug, -vvv or -vtrace
      --logger              Show the output with log format, with time, type and message.
      -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                            Only list packages matching a specific query. e.g: os=Windows AND (arch=x86 OR compiler=gcc)
      -r REMOTE, --remote REMOTE
                            Remote names. Accepts wildcards
      -c, --cache           Search in the local cache


The ``conan list`` command can list recipes and packages from the local cache, from the
specified remotes or from both. This command uses a *reference pattern* as input. The
structure of this pattern is based on a complete Conan reference that looks like: 

``name/version@user/channel#rrev:pkgid#prev``

This pattern supports using ``*`` as wildcard. Using it you can list:

* Recipe references (``name/version@userr/channel``).
* Recipe revisions (``name/version@userr/channel#rrev``).
* Package IDs and their configurations (``name/version@userr/channel#rrev:pkgids``).
* Package revisions (``name/version@userr/channel#rrev:pkgids#prev``).

Let's see some examples on how to use this pattern:

Listing recipe references
-------------------------

.. code-block:: bash
  :caption: *list all references on local cache*

    $ conan list *
    Local Cache:
      hello
        hello/2.26.1@mycompany/testing
        hello/2.20.2@mycompany/testing
        hello/1.0.4@mycompany/testing
        hello/2.3.2@mycompany/stable
        hello/1.0.4@mycompany/stable
      string-view-lite
        string-view-lite/1.6.0
      zlib
        zlib/1.2.11


.. code-block:: bash
  :caption: *list all versions of a reference*

    $ conan list zlib
    Local Cache:
      zlib
        zlib/1.2.11


As we commented, you can also use the ``*`` wildcard inside the reference you want to
search.

.. code-block:: bash
    :caption: *list all versions of a reference, equivalent to the previous one*

    $ conan list zlib/*
    Local Cache:
      zlib
        zlib/1.2.11

Use the pattern for searching only references matching a specific channel:

.. code-block:: bash
    :caption: *list references with 'stable' channel*

    $ conan list */*@*/stable
    Local Cache:
      hello
        hello/2.3.2@mycompany/stable
        hello/1.0.4@mycompany/stable


Listing recipe revisions
------------------------

The shortest way of listing the latest recipe revision for a recipe is using the
``name/version@user/channel`` as the pattern:

.. code-block:: bash
    :caption: *list latest recipe revision*

    $ conan list zlib/1.2.11
    Local Cache:
      zlib
        zlib/1.2.11#ffa77daf83a57094149707928bdce823 (2022-11-02 13:46:53 UTC)

This is equivalent to specify explicitly that you want to list the latest recipe revision
using the ``#latest`` placeholder:

.. code-block:: bash
    :caption: *list latest recipe revision*

    $ conan list zlib/1.2.11#latest
    Local Cache:
      zlib
        zlib/1.2.11#ffa77daf83a57094149707928bdce823 (2022-11-02 13:46:53 UTC)

To list all recipe revisions use the ``*`` wildcard:

.. code-block:: bash
  :caption: *list all recipe revisions*

    $ conan list zlib/1.2.11#*
    Local Cache:
      zlib
        zlib/1.2.11#ffa77daf83a57094149707928bdce823 (2022-11-02 13:46:53 UTC)
        zlib/1.2.11#8b23adc7acd6f1d6e220338a78e3a19e (2022-10-19 09:19:10 UTC)
        zlib/1.2.11#ce3665ce19f82598aa0f7ac0b71ee966 (2022-10-14 11:42:21 UTC)
        zlib/1.2.11#31ee767cb2828e539c42913a471e821a (2022-10-12 05:49:39 UTC)
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)

Listing package IDs
-------------------

The shortest way of listing all the package IDs belonging to the latest recipe revision is
using ``name/version@user/channel:*`` as the pattern:

.. code-block:: bash
  :caption: *list all package IDs for latest recipe revision*

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

    Here the ``#latest`` for the recipe revision is implicit, i.e., that pattern is
    equivalent to ``zlib/1.2.11#latest:*``


To list all the package IDs for all the recipe revisions use the ``*`` wildcard in the
revision ``#`` part:

.. code-block:: bash
  :caption: *list all the package IDs for all the recipe revisions*

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


Listing package revisions
-------------------------

The shortest way of listing the latest package revision for a specific recipe revision and
package ID is using the pattern ``name/version@user/channel#rrev:pkgid``

.. code-block:: bash
  :caption: *list latest package revision for a specific recipe revision and package ID*

    $ conan list zlib/1.2.11#8b23adc7acd6f1d6e220338a78e3a19e:fdb823f07bc228621617c6397210a5c6c4c8807b
    Local Cache:
      zlib
        zlib/1.2.11#d77ee68739fcbe5bf37b8a4690eea6ea (2022-08-05 17:17:30 UTC)
          PID: d0599452a426a161e02a297c6e0c5070f99b4909
            PREV: 4834a9b0d050d7cf58c3ab391fe32e25 (2022-11-18 12:33:31 UTC)


To list all the package revisions for for the latest recipe revision:

.. code-block:: bash
  :caption: *list all the package revisions for for the latest recipe revision*

    $ conan list zlib/1.2.11:*#*
    Local Cache:
      zlib
        zlib/1.2.11#6a6451bbfcb0e591333827e9784d7dfa (2022-12-29 11:51:39 UTC)
          PID: b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed
            PREV: 67bb089d9d968cbc4ef69e657a03de84 (2022-12-29 11:47:36 UTC)
          PID: b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed
            PREV: 5e196dbea832f1efee1e70e058a7eead (2022-12-29 11:47:26 UTC)
          PID: b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed
            PREV: 26475a416fa5b61cb962041623748d73 (2022-12-29 11:02:14 UTC)
          PID: d15c4f81b5de757b13ca26b636246edff7bdbf24
            PREV: a2eb7f4c8f2243b6e80ec9e7ee0e1b25 (2022-12-29 11:51:40 UTC)

.. note::

    Here the ``#latest`` for the recipe revision is implicit, i.e., that pattern is
    equivalent to ``zlib/1.2.11#latest:*#*``