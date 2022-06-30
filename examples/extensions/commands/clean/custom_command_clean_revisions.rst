.. _examples_extensions_commands_clean_revisions:

Custom command: Clean old recipe and package revisions
======================================================

Please, first of all, clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/extensions/commands/clean


In this example we are going to see how to create/use a custom command: :command:`conan clean`. It removes
every recipe and its package revisions from the local cache or the remotes, except the latest package revision from
the latest recipe one.

.. note::

    To understand better this example, it is highly recommended to read previously the :ref:`Custom commands reference<reference_commands_custom_commands>`.


Locate the command
------------------

Copy the command file ``cmd_clean.py`` into your ``[YOUR_CONAN_HOME]/extensions/commands/`` folder (create it if it's not there).
If you don't know where ``[YOUR_CONAN_HOME]`` is located, you can run :command:`conan config home` to check it.


Run it
------

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

Code tour
---------

The ``conan clean`` command has the following code:

.. code-block:: python
    :caption: cmd_clean.py

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command, OnceArgument
    from conans.cli.output import Color, ConanOutput
    from conans.client.userio import UserInput

    recipe_color = Color.BRIGHT_BLUE
    removed_color = Color.BRIGHT_YELLOW


    @conan_command(group="Custom commands")
    def clean(conan_api: ConanAPIV2, parser, *args):
        """
        Deletes (from local cache or remotes) all recipe and package revisions but
        the latest package revision from the latest recipe revision.
        """
        parser.add_argument('-r', '--remote', action=OnceArgument,
                            help='Will remove from the specified remote')
        parser.add_argument('--force', default=False, action='store_true',
                            help='Remove without requesting a confirmation')
        args = parser.parse_args(*args)

        def confirmation(message):
            return args.force or ui.request_boolean(message)

        ui = UserInput(non_interactive=False)
        out = ConanOutput()
        remote = conan_api.remotes.get(args.remote) if args.remote else None
        output_remote = remote or "Local cache"

        # Getting all the recipes
        recipes = conan_api.search.recipes("*/*", remote=remote)
        if recipes and not confirmation("Do you want to remove all the recipes revisions and their packages ones, "
                                        "except the latest package revision from the latest recipe one?"):
            return
        for recipe in recipes:
            out.writeln(f"{str(recipe)}", fg=recipe_color)
            all_rrevs = conan_api.list.recipe_revisions(recipe, remote=remote)
            latest_rrev = all_rrevs[0] if all_rrevs else None
            for rrev in all_rrevs:
                if rrev != latest_rrev:
                    conan_api.remove.recipe(rrev, remote=remote)
                    out.writeln(f"Removed recipe revision: {rrev.repr_notime()} "
                                f"and all its package revisions [{output_remote}]", fg=removed_color)
                else:
                    all_prevs = conan_api.search.package_revisions(f"{rrev.repr_notime()}:*#*", remote=remote)
                    latest_prev = all_prevs[0] if all_prevs else None
                    for prev in all_prevs:
                        if prev != latest_prev:
                            conan_api.remove.package(prev, remote=remote)
                            out.writeln(f"Removed package revision: {prev.repr_notime()} [{output_remote}]", fg=removed_color)


Let's analize the most important parts.

parser
++++++

The ``parser`` param is an instance of the Python command-line parsing ``argparse.ArgumentParser``,
so if you want to know more about its API, visit `its official website <https://docs.python.org/3/library/argparse.html>`_.


User input and user output
++++++++++++++++++++++++++

Important classes to manage user input and user output:

.. code-block:: python

    ui = UserInput(non_interactive=False)
    out = ConanOutput()


* ``UserInput(non_interactive)``: class to manage user inputs. In this example we're using ``ui.request_boolean("Do you want to proceed?")``,
  so it'll be automatically translated to ``Do you want to proceed? (yes/no):`` in the command prompt.
  **Note**: you can use ``UserInput(non_interactive=conan_api.config.get("core:non_interactive"))`` too.
* ``ConanOutput()``: class to manage user outputs. In this example, we're using only ``out.writeln(message, fg=None, bg=None)``
  where ``fg`` is the font foreground, and ``bg`` is the font background. Apart from that, you have some predefined methods
  like ``out.info()``, ``out.success()``, ``out.error()``, etc.


Conan public API
++++++++++++++++

The most important part of this example is the usage of the Conan API via ``conan_api`` parameter. These are some examples
which are being used in this custom command:

.. code-block:: python

    conan_api.remotes.get(args.remote)
    conan_api.search.recipes("*/*", remote=remote)
    conan_api.list.recipe_revisions(recipe, remote=remote)
    conan_api.remove.recipe(rrev, remote=remote)
    conan_api.search.package_revisions(f"{rrev.repr_notime()}:*#*", remote=remote)
    conan_api.remove.package(prev, remote=remote)



* ``conan_api.remotes.get(...)``: ``[RemotesAPI]`` Returns a RemoteRegistry given the remote name.
* ``conan_api.search.recipes(...)``: ``[SearchAPI]`` Returns a list with all the recipes matching the given pattern.
* ``conan_api.list.recipe_revisions(...)``: ``[ListAPI]`` Returns a list with all the recipe revisions given a recipe reference.
* ``conan_api.remove.recipe(...)``: ``[RemoveAPI]`` Removes the given recipe revision.
* ``conan_api.search.package_revisions(...)``: ``[SearchAPI]`` Returns the list of package revisions for a given recipe revision.
* ``conan_api.remove.package(...)``: ``[RemoveAPI]`` Removes the given package revision.

Besides that, it deserves especial attention these lines:

.. code-block:: python

    all_rrevs = conan_api.list.recipe_revisions(recipe, remote=remote)
    latest_rrev = all_rrevs[0] if all_rrevs else None
    # .......
    all_prevs = conan_api.search.package_revisions(f"{rrev.repr_notime()}:*#*", remote=remote)
    latest_prev = all_prevs[0] if all_prevs else None

Basically, these API calls are returning a list of recipe revisions and package ones respectively, but we're saving the
first element as the latest one because these calls are getting an ordered list always. Take into account that it's using
``rrev.repr_notime()`` because it represents the recipe revision as a string and pruning the timestamps.


If you want to know more about the Conan API, visit the :ref:`ConanAPIV2 section<reference_python_api_conan_api_v2>`
