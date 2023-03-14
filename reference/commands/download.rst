.. _reference_commands_download:

conan download
==============

.. code-block:: text

    $ conan download -h
    usage: conan download [-h] [-v [V]] [--only-recipe]
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
      --only-recipe         Download only the recipe/s, not the binary packages.
      -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                            Only download packages matching a specific query. e.g:
                            os=Windows AND (arch=x86 OR compiler=gcc)
      -r REMOTE, --remote REMOTE
                            Download from this specific remote


Downloads recipe and binaries to the local cache from the specified remote.

..  note::

    Please, be aware that :command:`conan download` unlike :command:`conan install`, will not
    download any of the transitive dependencies of the downloaded package.


You can use patterns to download specific references just like in other commands like
:command:`conan list` or :command:`conan upload`:

..  code-block:: bash
    
    # download latest revision and packages for all openssl versions in foo remote
    $ conan download "openssl/*" -r foo

.. note::

  :command:`conan download` will download only the latest revision by default. If you want
  to download more revisions other than the latest one you can use wildcards in the
  revisions part of the reference pattern argument

You may also just download recipes (in this case selecting all the revisions in the
pattern, not just the latest one):

..  code-block:: bash
    
    # download all recipe revisions for zlib/1.2.13
    $ conan download "zlib/1.2.13#*" -r foo --only-recipe


If you just want to download the packages belonging to a specific setting, use the ``--package-query`` argument:

.. code-block:: bash

    $ conan download "zlib/1.2.13#*" -r foo --package-query="os=Linux and arch=x86" 
