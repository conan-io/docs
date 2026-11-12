.. _examples_extensions_commands_clean_revisions:

Custom command: Clean old recipe and package revisions
======================================================

.. note::

    This is mostly an example command. The built-in ``conan remove *#!latest`` syntax,
    meaning "all revisions but the latest" would probably be enough for this use case,
    without needing this custom command.

.. warning::

    Using this command requires Conan 2.21.0 or higher.


Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

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
    Found 4 pkg/version recipes matching */* in local cache
    Do you want to remove all the recipes revisions and their packages ones, except the latest package revision from the latest recipe one? (yes/no): yes
    Keeping recipe revision: other/1.0#31da245c3399e4124e39bd4f77b5261f and its latest package revisions [Local cache]
    Removed package revision: other/1.0#31da245c3399e4124e39bd4f77b5261f:da39a3ee5e6b4b0d3255bfef95601890afd80709#a16985deb2e1aa73a8480faad22b722c [Local cache]
    Removed recipe revision: other/1.0#721995a35b1a8d840ce634ea1ac71161 and all its package revisions [Local cache]
    Keeping recipe revision: hello/1.0#9a77cdcff3a539b5b077dd811b2ae3b0 and its latest package revisions [Local cache]
    Removed package revision: hello/1.0#9a77cdcff3a539b5b077dd811b2ae3b0:da39a3ee5e6b4b0d3255bfef95601890afd80709#cee90a74944125e7e9b4f74210bfec3f [Local cache]
    Removed package revision: hello/1.0#9a77cdcff3a539b5b077dd811b2ae3b0:da39a3ee5e6b4b0d3255bfef95601890afd80709#7cddd50952de9935d6c3b5b676a34c48 [Local cache]
    Keeping recipe revision: libcxx/0.1#abcdef1234567890abcdef1234567890 and its latest package revisions [Local cache]

Nothing should happen if you run it again:

.. code-block:: bash

    $ conan clean
    Do you want to remove all the recipes revisions and their packages ones, except the latest package revision from the latest recipe one? (yes/no): yes
    Keeping recipe revision: other/1.0#31da245c3399e4124e39bd4f77b5261f and its latest package revisions [Local cache]
    Keeping recipe revision: hello/1.0#9a77cdcff3a539b5b077dd811b2ae3b0 and its latest package revisions [Local cache]
    Keeping recipe revision: libcxx/0.1#abcdef1234567890abcdef1234567890 and its latest package revisions [Local cache]

Code tour
---------

The ``conan clean`` command has the following code:

.. code-block:: python
    :caption: cmd_clean.py

    from conan.api.conan_api import ConanAPI
    from conan.api.model import PackagesList, ListPattern
    from conan.api.input import UserInput
    from conan.api.output import ConanOutput, Color
    from conan.cli.command import OnceArgument, conan_command

    recipe_color = Color.BRIGHT_BLUE
    removed_color = Color.BRIGHT_YELLOW

    @conan_command(group="Custom commands")
    def clean(conan_api: ConanAPI, parser, *args):
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

        # List all recipes revisions and all their packages revisions as well
        pkg_list = conan_api.list.select(ListPattern("*/*#*:*#*", rrev=None, prev=None), remote=remote)
        if pkg_list and not confirmation("Do you want to remove all the recipes revisions and their packages ones, "
                                        "except the latest package revision from the latest recipe one?"):
            out.writeln("Aborted")
            return

        # Split the package list into based on their recipe reference
        for sub_pkg_list in pkg_list.split():
            latest = max(sub_pkg_list.items(), key=lambda item: item[0])[0]
            out.writeln(f"Keeping recipe revision: {latest.repr_notime()} "
                        f"and its latest package revisions [{output_remote}]", fg=recipe_color)
            for rref, packages in sub_pkg_list.items():
                # For the latest recipe revision, keep the latest package revision only
                if latest == rref:
                    # Get the latest package timestamp for each package_id
                    latest_pref_list = [max([p for p in packages if p.package_id == pkg_id], key=lambda p: p.timestamp)
                                        for pkg_id in {p.package_id for p in packages}]
                    for pref in packages:
                        if pref not in latest_pref_list:
                            conan_api.remove.package(pref, remote=remote)
                            out.writeln(f"Removed package revision: {pref.repr_notime()} [{output_remote}]", fg=removed_color)
                else:
                    # Otherwise, remove all outdated recipe revisions and their packages
                    conan_api.remove.recipe(rref, remote=remote)
                    out.writeln(f"Removed recipe revision: {rref.repr_notime()} "
                                f"and all its package revisions [{output_remote}]", fg=removed_color)


Let's analyze the most important parts.

parser
++++++

The ``parser`` param is an instance of the Python command-line parsing ``argparse.ArgumentParser``,
so if you want to know more about its API, visit `its official website <https://docs.python.org/3/library/argparse.html>`_.


User output
+++++++++++

``ConanOutput()``: class to manage user outputs. In this example, we're using only ``out.writeln(message, fg=None, bg=None)``
where ``fg`` is the font foreground, and ``bg`` is the font background. Apart from that, you have some predefined methods
like ``out.info()``, ``out.success()``, ``out.error()``, etc.


Conan public API
++++++++++++++++

.. include:: ../../../../common/experimental_warning.inc

The most important part of this example is the usage of the Conan API via ``conan_api`` parameter. These are some examples
which are being used in this custom command:

.. code-block:: python

    conan_api.remotes.get(args.remote)
    conan_api.list.select(ListPattern("*/*#*:*#*", rrev=None, prev=None), remote=remote)
    conan_api.remove.recipe(rrev, remote=remote)
    conan_api.remove.package(prev, remote=remote)



* ``conan_api.remotes.get(...)``: ``[RemotesAPI]`` Returns a RemoteRegistry given the remote name.
* ``conan_api.list.select(...)``: ``[ListAPI]`` Returns a list with all the recipes matching the given pattern.
* ``conan_api.remove.recipe(...)``: ``[RemoveAPI]`` Removes the given recipe revision and all its package revisions.
* ``conan_api.remove.package(...)``: ``[RemoveAPI]`` Removes the given package revision.

Besides that, it deserves especial attention these lines:

.. code-block:: python

    for sub_pkg_list in pkg_list.split():
        latest = max(sub_pkg_list.items(), key=lambda item: item[0])[0]

    ...

    latest_pref_list = [max([p for p in packages if p.package_id == pkg_id], key=lambda p: p.timestamp)
                                    for pkg_id in {p.package_id for p in packages}]

Basically, the ``pkg_list.split()`` is returning a list for the same recipe reference. Then, ``sub_pkg_list.items()`` returns
a list of tuples ``(Recipe Reference, Packages References)``, so finally, ``max(..., key=...)`` is used to get the
latest recipe reference based on its timestamp.
Later, ``latest_pref_list`` is created to keep only the latest package revision for each package ID. It iterates over the set of package IDs
to get the latest package revision based on its timestamp.


If you want to know more about the Conan API, visit the :ref:`ConanAPI section<reference_python_api_conan_api>`
