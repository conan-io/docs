.. _search_command:

conan search
============

.. code-block:: bash

    $ conan search [-h] [--case-sensitive] [-r REMOTE] [--raw]
                   [--table TABLE] [-q QUERY] [-o]
                   [pattern]

Searches package recipes and binaries in the local cache or in a remote. If
you provide a pattern, then it will search for existing package recipes
matching that pattern. If a full and complete package reference is provided,
like Pkg/0.1@user/channel, then the existing binary packages for that
reference will be displayed. You can search in a remote or in the local cache,
if nothing is specified, the local conan cache is assumed. Search is case
sensitive, exact case has to be used. For case insensitive file systems, like
Windows, case sensitive search can be forced with the --case-sensitive
argument.

.. code-block:: bash

    positional arguments:
      pattern               Pattern name, e.g. openssl/* or package recipe
                            reference if "-q" is used. e.g.
                            MyPackage/1.2@user/channel

    optional arguments:
      -h, --help            show this help message and exit
      --case-sensitive      Make a case-sensitive search. Use it to guarantee
                            case-sensitive search in Windows or other case-
                            insensitive filesystems
      -r REMOTE, --remote REMOTE
                            Remote origin. `all` searches all remotes
      --raw                 Print just the list of recipes
     --table TABLE         Outputs html file with a table of binaries. Only valid
                            if "pattern" is a package recipe reference
      -q QUERY, --query QUERY
                            Packages query: "os=Windows AND (arch=x86 OR
                            compiler=gcc)". The "pattern" parameter has to be a
                            package recipe reference: MyPackage/1.2@user/channel
      -o, --outdated        Show only outdated from recipe packages

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

If you specify a query filter for a setting and the package recipe is not restricted by this
setting, will find all packages:

.. code-block:: python

    class MyRecipe(ConanFile):
        settings="arch"

.. code-block:: bash

    $ conan search MyRecipe/1.0@lasote/stable -q os=Windows

The query above will find all the ``MyRecipe`` binary packages, because the recipe doesn't declare
"os" as a setting.

You can generate a table for all binaries from a given recipe with the ``--table`` option:

.. code-block:: bash

    $ conan search zlib/1.2.11@conan/stable --table=file.html -r=conan-center
    $ file.html # or open the file, double-click

.. image:: /images/search_binary_table.png
    :height: 500 px
    :width: 600 px
    :align: center
