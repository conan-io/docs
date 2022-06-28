.. _examples_extensions_commands_clean_revisions:

Custom command: Clean old recipe and package revisions
========================================================

Please, first of all, clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/extensions/commands/clean


In this example we are going to see how to create/use a custom command: :command:`conan clean`. It removes
every recipe and its package revisions from the local cache or the remotes, except the latest package revision from
the latest recipe one.

.. note::

    To understand better this example, it is highly recommended to read previously the :ref:`Custom commands reference<reference_commands_custom_commands>`.


Locate the command
-------------------

Copy the command file ``cmd_clean.py`` into your ``[YOUR_CONAN_HOME]/extensions/commands/`` folder (create it if it's not there).
If you don't know where ``[YOUR_CONAN_HOME]`` is located, you can run :command:`conan config home` to check it.


Run it
--------

Now, you should be able to see the new command in your command prompt:

.. code-block:: bash

    $ conan -h
    ...
    Custom commands
    clean        Deletes (from local cache or remotes) all recipe and package revisions but the
                   latest package revision from the latest recipe revision.

    $ conan clean -h
    usage: conan clean [-h] [-r REMOTE] [--force]

    Deletes (from local cache or remotes) all recipe and package revisions but
    the latest package revision from the latest recipe revision.

    optional arguments:
      -h, --help            show this help message and exit
      -r REMOTE, --remote REMOTE
                            Will remove from the specified remote
      --force               Remove without requesting a confirmation


Finally, if you execute :command:`conan clean`:

.. code-block:: bash

    $ conan clean
    Do you want to remove all the recipes revisions and their packages ones, except the latest package revision from the latest recipe one? (yes/no): yes
    other/1.0
    Removed package revision: other/1.0#31da245c3399e4124e39bd4f77b5261f:da39a3ee5e6b4b0d3255bfef95601890afd80709#a16985deb2e1aa73a8480faad22b722c [Local cache]
    Removed recipe revision: other/1.0#721995a35b1a8d840ce634ea1ac71161 and all its package revisions [Local cache]
    hello/1.0
    Removed package revision: hello/1.0#9a77cdcff3a539b5b077dd811b2ae3b0:da39a3ee5e6b4b0d3255bfef95601890afd80709#cee90a74944125e7e9b4f74210bfec3f [Local cache]
    Removed package revision: hello/1.0#9a77cdcff3a539b5b077dd811b2ae3b0:da39a3ee5e6b4b0d3255bfef95601890afd80709#7cddd50952de9935d6c3b5b676a34c48 [Local cache]
    libcxx/0.1

Nothing should happen if you run it again:

.. code-block:: bash

    $ conan clean
    Do you want to remove all the recipes revisions and their packages ones, except the latest package revision from the latest recipe one? (yes/no): yes
    other/1.0
    hello/1.0
    libcxx/0.1


Conan public API
-----------------

The most important part of this example is the usage of the Conan API. These are some examples which are being used in
this custom command:

.. code-block:: python

    # [RemotesAPI] Returns a RemoteRegistry given the remote name
    conan_api.remotes.get(args.remote)
    # [SearchAPI] Returns a list with all the recipes matching the given pattern
    conan_api.search.recipes("*/*", remote=remote)
    # [ListAPI] Returns a list with all the recipe revisions given a recipe reference
    conan_api.list.recipe_revisions(recipe, remote=remote)
    # [RemoveAPI] Remove the given recipe revision
    conan_api.remove.recipe(rrev, remote=remote)
    # [SearchAPI] Returns the list of package revisions for a given recipe revision
    conan_api.search.package_revisions(f"{rrev.repr_notime()}:*#*", remote=remote)
    # [RemoveAPI] Remove the given package revision
    conan_api.remove.package(prev, remote=remote)


If you want to know more about it, visit the :ref:`ConanAPIV2 section<reference_python_api_conan_api_v2>`
