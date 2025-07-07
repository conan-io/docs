.. _reference_commands_remove:

conan remove
============

.. autocommand::
    :command: conan remove -h


The ``conan remove`` command removes recipes and packages from the local cache or from a
specified remote. Depending on the patterns specified as argument, it is possible to
remove a complete package, or just remove the binaries, leaving still the recipe
available. You can also use the keyword ``!latest`` in the revision part of the pattern to
avoid removing the latest recipe or package revision of a certain Conan package.

Use ``--dry-run`` to avoid performing actual deletions, and instead get a list of the elements that would have been removed.

It has 2 possible and mutually exclusive inputs:

- The ``conan remove <pattern>`` pattern-based matching of recipes.
- The ``conan remove --list=<pkglist>`` that will remove the artifacts specified in the ``pkglist`` json file


There are other commands like :command:`conan list` (see the patterns documentation there :ref:`reference_commands_list`), :command:`conan upload` and :command:`conan download`, that take the same patterns. 

To remove recipes and their associated package binaries from the local cache:


.. code-block:: text

    $ conan remove "*"
    # Removes everything from the cache

    $ conan remove "zlib/*""
    # Remove all possible versions of zlib, including all recipes, revisions and packages

    $ conan remove zlib/1.3.1
    # Remove zlib/1.3.1, all its revisions and package binaries. Leave other zlib versions

    $ conan remove "zlib/[<1.2.13]"
    # Remove zlib/1.3.1 and zlib/1.2.12, all its revisions and package binaries.

    $ conan remove zlib/1.3.1#latest
    # Remove zlib/1.3.1, only its latest recipe revision and binaries of that revision
    # Leave the other zlib/1.3.1 revisions intact

    $ conan remove zlib/1.3.1#!latest
    # Remove all the recipe revisions from zlib/1.3.1 but the latest one
    # Leave the latest zlib/1.3.1 revision intact

    $ conan remove zlib/1.3.1#<revision>
    # Remove zlib/1.3.1, only its exact <revision> and binaries of that revision
    # Leave the other zlib/1.3.1 revisions intact


To remove only package binaries, but leaving the recipes, it is necessary to specify the
pattern including the ``:`` separator of the ``package_id``:

.. code-block:: text

    $ conan remove "zlib/1.3.1:*"
    # Removes all the zlib/1.3.1 package binaries from all the recipe revisions

    $ conan remove "zlib/*:*"
    # Removes all the binaries from all the recipe revisions from all zlib versions

    $ conan remove "zlib/1.3.1#latest:*"
    # Removes all the zlib/1.3.1 package binaries only from the latest zlib/1.3.1 recipe revision

    $ conan remove "zlib/1.3.1#!latest:*"
    # Removes all the zlib/1.3.1 package binaries from all the recipe revisions but the latest one

    $ conan remove zlib/1.3.1:<package_id>
    # Removes the package binary <package_id> from all the zlib/1.3.1 recipe revisions

    $ conan remove zlib/1.3.1:#latest<package_id>#latest
    # Removes only the latest package revision of the binary identified with <package_id>
    # from the latest recipe revision of zlib/1.3.1
    # WARNING: Recall that having more than 1 package revision is a smell and shouldn't happen
    # in normal situations


Note that you can filter which packages will be removed using the ``--package-query`` argument:

.. code-block:: text

    $ conan remove zlib/1.3.1:* -p compiler=clang
    # Removes all the zlib/1.3.1 packages built with Clang compiler


You can query packages by both their settings and options, including custom ones.
To query for options you need to explicitly add the `options.` prefix, so that
`-p options.shared=False` will work but `-p shared=False` won't.



All the above commands, by default, operate in the Conan cache.
To remove artifacts from a server, use the ``-r=myremote`` argument:

.. code-block:: text

    $ conan remove zlib/1.3.1:* -r=myremote
    # Removes all the zlib/1.3.1 package binaries from all the recipe revisions in 
    # the remote <myremote>
