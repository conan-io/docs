
.. _conan_search:

conan search
============

.. code-block:: bash

    $ conan search [-h] [-o] [-q QUERY] [-r REMOTE] [--case-sensitive]
                   [--raw] [--table TABLE] [-j JSON] [-rev]
                   [pattern_or_reference]

Searches package recipes and binaries in the local cache or in a remote.

If you provide a pattern, then it will search for existing package
recipes matching it.  If a full reference is provided
(pkg/0.1@user/channel) then the existing binary packages for that
reference will be displayed. The default remote is ignored, if no
remote is specified, the search will be done in the local cache.
Search is case sensitive, exact case has to be used. For case
insensitive file systems, like Windows, case sensitive search
can be forced with '--case-sensitive'.

.. code-block:: text

    positional arguments:
      pattern_or_reference  Pattern or package recipe reference, e.g., 'boost/*',
                            'MyPackage/1.2@user/channel'

    optional arguments:
      -h, --help            show this help message and exit
      -o, --outdated        Show only outdated from recipe packages. This flag can
                            only be used with a reference
      -q QUERY, --query QUERY
                            Packages query: 'os=Windows AND (arch=x86 OR
                            compiler=gcc)'. The 'pattern_or_reference' parameter
                            has to be a reference: MyPackage/1.2@user/channel
      -r REMOTE, --remote REMOTE
                            Remote to search in. '-r all' searches all remotes
      --case-sensitive      Make a case-sensitive search. Use it to guarantee
                            case-sensitive search in Windows or other case-
                            insensitive file systems
      --raw                 Print just the list of recipes
      --table TABLE         Outputs html file with a table of binaries. Only valid
                            for a reference search
      -j JSON, --json JSON  json file path where the search information will be
                            written to
      -rev, --revisions     Get a list of revisions for a reference or a package
                            reference.


**Examples**

.. code-block:: bash

    $ conan search zlib/*
    $ conan search zlib/* -r=conan-center

To search for recipes in all defined remotes use ``--all`` (this is only valid for searching recipes, not binaries):

.. code-block:: bash

    $ conan search zlib/* -r=all


If you use instead the full package recipe reference, you can explore the binaries existing for
that recipe, also in a remote or in the local conan cache:

.. code-block:: bash

    $ conan search Boost/1.60.0@lasote/stable

A query syntax is allowed to look for specific binaries, you can use ``AND`` and ``OR`` operators
and parenthesis, with settings and also options.

.. code-block:: bash

    $ conan search Boost/1.60.0@lasote/stable -q arch=x86_64
    $ conan search Boost/1.60.0@lasote/stable -q "(arch=x86_64 OR arch=ARM) AND (build_type=Release OR os=Windows)"

Also, query syntax allows sub-settings, even for custom properties. e.g:

.. code-block:: bash

    $ conan search Boost/1.60.0@lasote/stable -q "compiler=gcc AND compiler.version=9"
    $ conan search Boost/1.60.0@lasote/stable -q "os=Linux AND os.distro=Ubuntu AND os.distro.version=19.04"

If you specify a query filter for a setting and the package recipe is not restricted by this
setting, Conan won't find the packages. e.g:

.. code-block:: python

    class MyRecipe(ConanFile):
        settings="arch"

.. code-block:: bash

    $ conan search MyRecipe/1.0@lasote/stable -q os=Windows

The query above won't find the ``MyRecipe`` binary packages (because the recipe doesn't declare
"os" as a setting) unless you specify the ``None`` value:

.. code-block:: bash

    $ conan search MyRecipe/1.0@lasote/stable -q os=None

You can generate a table for all binaries from a given recipe with the ``--table`` option:

.. code-block:: bash

    $ conan search zlib/1.2.11@conan/stable --table=file.html -r=conan-center
    $ file.html # or open the file, double-click

.. image:: /images/conan-search_binary_table.png
    :height: 500 px
    :width: 600 px
    :align: center


Search all the local Conan packages matching a pattern and showing the revision:

.. code-block:: bash

    $ conan search lib* --revisions
    $ Existing package recipes:

      lib/1.0@user/channel#404e86c18e4a47a166fabe70b3b15e33


Search the local revision for a local cache recipe:

.. code-block:: bash

    $ conan search lib/1.0@conan/testing --revisions
    $ Revisions for 'lib/1.0@conan/testing':
        a55e3b054fdbf4e2c6f10e955da69502 (2019-03-05 16:37:27 UTC)

Search the remote revisions in a server:

.. code-block:: bash

    $ conan search lib/1.0@conan/testing --revisions -r=myremote
      Revisions for 'lib/1.0@conan/testing' at remote 'myremote':
        78fcef25a1eaeecd5facbbf08624c561 (2019-03-05 16:37:27 UTC)
        f3367e0e7d170aa12abccb175fee5f97 (2019-03-05 16:37:27 UTC)
