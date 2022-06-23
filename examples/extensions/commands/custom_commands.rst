.. _examples_extensions_custom_commands:


Custom commands
=================

Since Conan 2.0, it's so easy to create your own Conan commands. These are some of the rules/tips to create custom commands:

* All the custom commands must be located under the ``[YOUR_CONAN_HOME]/extensions/commands/`` folder.
    * It can be created another folders layer to act like ``scope`` for the commands under it, e.g., ``[YOUR_CONAN_HOME]/extensions/commands/myscope/``.
* Every custom command file must be named like ``cmd_[YOUR_CUSTOM_COMMAND_NAME].py``.
* Any command can have sub-commands.
* It can be performed different formatters to output any command result.
* It is automatically injected one object instance of :ref:`ConanAPIV2 class<reference_python_api_conan_api_v2>` as first paremeter in the command function.

Let's see some basic examples of custom commands:

Simple "hello" command
--------------------------

This is the simplest command that runs a ``conan hello`` command and outputs ``Hello World!`` in your console.

First of all, ensure that your ``[YOUR_CONAN_HOME]/extensions/commands/`` folder is already there, otherwise, create it.

Save the ``cmd_hello.py`` file in the mentioned folder. Its content looks like this:

.. code-block:: python
    :caption: cmd_hello.py

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command
    from conans.cli.output import ConanOutput


    @conan_command(group="Custom commands")
    def hello(conan_api: ConanAPIV2, parser, *args, **kwargs):
        """
        Simple command to print "Hello World!" line
        """
        ConanOutput().info("Hello World!")


Run :command:`conan -h` to see the new ``hello`` command there:

.. code-block:: text

    ....
    Custom commands
    hello      Simple command to print "Hello World!" line

Running this one:

.. code-block:: bash

    $ conan hello
    Hello World!


.. _conan_custom_commands_scoping:

Scoping commands
-------------------

Sometimes you need to create some commands that could be related to the same topic, so it's possible thanks to the
scoping mechanism.

Create a folder named ``greet`` under ``[YOUR_CONAN_HOME]/extensions/commands/`` folder. Now, add this new command
file there:

.. code-block:: python
    :caption: cmd_bye.py

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.output import ConanOutput
    from conans.cli.command import conan_command, conan_subcommand

    @conan_subcommand()
    def bye_say(conan_api, parser, *args, **kwargs):
        """
        Sub-command of bye that prints "Bye!" line
        """
        ConanOutput().info("Bye!")

    @conan_command(group="Custom commands")
    def bye(conan_api: ConanAPIV2, parser, *args, **kwargs):
        """
        Simple command to print "Bye!" line
        """

Notice that it's been added a sub-command named ``say`` as well.

Run :command:`conan -h` to see the new ``greet:bye`` command there:

.. code-block:: text

    ....
    Custom commands
    hello      Simple command to print "Hello World!" line
    greet:bye  Simple command to print "Bye!" line

Run it:

.. code-block:: bash

    $ conan greet:bye say
    Bye!


Output formats
---------------

Finally, it's possible to define several formats for your command output.

Let's create another command file in ``[YOUR_CONAN_HOME]/extensions/commands/``:

.. code-block:: python
    :caption: cmd_cache_folder.py

    import json
    import os

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command


    def output_mycommand_cli(info):
        return f"Conan cache folder is: {info.get('cache_folder')}"


    def output_mycommand_json(info):
        return json.dumps(info)


    @conan_command(group="custom commands",
                   formatters={"cli": output_mycommand_cli,
                               "json": output_mycommand_json})
    def cache_folder(conan_api: ConanAPIV2, parser, *args, **kwargs):
        """
        Prints the location of the cache folder
        """
        return {"cache_folder": os.path.basename(conan_api.cache_folder)}


Run again :command:`conan -h`:

.. code-block:: text

    ....
    Custom commands
    cache-folder Prints the location of the cache folder
    hello        Simple command to print "Hello World!" line
    greet:bye    Simple command to print "Bye!" line

Try it out:

.. code-block:: bash

    $ conan cache-folder -f cli
    Conan cache folder is: .conan2
    $ conan cache-folder -f json
    {"cache_folder": ".conan2"}

These formats are useful to pipe this information to a file:

.. code-block:: bash

    $ conan cache-folder -f cli > out.txt
    $ conan cache-folder -f json > out.json


Read more
---------

- :ref:`Custom command to remove recipe and package revisions but the latest package revision from the latest recipe revision<examples_extensions_commands_clean_revisions>`.
