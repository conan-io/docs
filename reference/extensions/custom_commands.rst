.. _reference_commands_custom_commands:

Custom commands
===============

It's possible to create your own Conan commands to solve self-needs thanks to Python and Conan public API powers altogether.

Location and naming
-------------------

All the custom commands must be located in ``[YOUR_CONAN_HOME]/extensions/commands/`` folder. If you don't know where
``[YOUR_CONAN_HOME]`` is located, you can run :command:`conan config home` to check it. If _commands_ sub-directory is not created yet, you will have to create it.

Those custom commands files must be Python files and start with the prefix ``cmd_[your_command_name].py``.
The call to the custom commands is like any other existing Conan one: :command:`conan your_command_name`.


Scoping
+++++++

It's possible to have another folder layer to group some commands under the same topic.

For instance:

.. code-block:: text

    | - [YOUR_CONAN_HOME]/extensions/commands/greet/
          | - cmd_hello.py
          | - cmd_bye.py

The call to those commands change a little bit: :command:`conan [topic_name]:your_command_name`. Following the previous example:

.. code-block:: text

    $ conan greet:hello
    $ conan greet:bye

.. note::

    Only one folder layer is allowed. Something like this won't work:
    ``[YOUR_CONAN_HOME]/extensions/commands/topic1/topic2/cmd_command.py``


Decorators
----------

conan_command(group=None, formatters=None)
++++++++++++++++++++++++++++++++++++++++++

Main decorator to declare a function as a new Conan command. Where the parameters are:

* ``group`` is the name of the group of commands declared under the same name.
  This grouping will appear executing the :command:`conan -h` command.
* ``formatters`` is a dict-like Python object where the ``key`` is the formatter name and the value is the
  function instance where will be processed the information returned by the command one.


.. code-block:: python
    :caption: cmd_hello.py

    import json

    from conan.api.conan_api import ConanAPI
    from conan.api.output import cli_out_write, ConanOutput
    from conan.cli.command import conan_command


    def output_json(msg):
        cli_out_write(cli_json.dumps({"greet": msg}))

    def output_text(msg):
        ConanOutput().info(msg)


    @conan_command(group="Custom commands", formatters={"text": output_text,
                                                        "json": output_json})
    def hello(conan_api: ConanAPI, parser, *args):
        """
        Simple command to print "Hello World!" line
        """
        msg = "Hello World!"
        return msg


.. important::

    The function decorated by ``@conan_command(....)`` must have the same name as the suffix used by the Python file.
    In the previous example, the file name is ``cmd_hello.py``, and the command function decorated is ``def hello(....)``.


conan_subcommand(formatters=None)
+++++++++++++++++++++++++++++++++

Similar to ``conan_command``, but this one is declaring a sub-command of an existing custom command. For instance:

.. code-block:: python
    :caption: cmd_hello.py

    from conan.api.conan_api import ConanAPI
    from conan.api.output import ConanOutput
    from conan.cli.command import conan_command, conan_subcommand


    @conan_subcommand()
    def hello_moon(conan_api, parser, subparser, *args):
        """
        Sub-command of "hello" that prints "Hello Moon!" line
        """
        ConanOutput().info("Hello Moon!")


    @conan_command(group="Custom commands")
    def hello(conan_api: ConanAPI, parser, *args):
        """
        Simple command "hello"
        """

The command call looks like :command:`conan hello moon`.

.. note::

    Notice that to declare a sub-command is required an empty Python function acts as the main command.


Argument definition and parsing
-------------------------------

Commands can define their own arguments with the ``argparse`` Python library.


.. code-block:: python
    
    @conan_command(group='Creator')
    def build(conan_api, parser, *args):
        """
        Command help
        """
        parser.add_argument("path", nargs="?", help='help for command')
        add_reference_args(parser)
        args = parser.parse_args(*args)
        # Use args.path


When there are sub-commands, the base command cannot define arguments, only the sub-commands can do it. If you have a set of common arguments to all sub-commands, you can define a function that adds them.

.. code-block:: python

    @conan_command(group="MyGroup")
    def mycommand(conan_api, parser, *args):
        """
        Command help
        """
        # Do not define arguments in the base command
        pass

    @conan_subcommand()
    def mycommand_mysubcommand(conan_api: ConanAPI, parser, subparser, *args):
        """
        Subcommand help
        """
        # Arguments are added to "subparser"
        subparser.add_argument("reference", help="Recipe reference or Package reference")
        # You can add common args with your helper
        # add_my_common_args(subparser)
        # But parsing all of them happens to "parser"
        args = parser.parse_args(*args)
        # use args.reference


Formatters
----------

This allows to have different formats of output for the same command. The return of the command will be passed as argument to the formatters. If there are different formatters that 
require different arguments, the approach is to return a dictionary, and let the formatters chose the 
arguments they need.

For example, the ``graph info`` command uses several formatters like:

.. code-block:: python

    def format_graph_json(result):
        graph = result["graph"]
        conan_api = result["conan_api"]
        ...
        cli_out_write(cli_json.dumps(...))

    def format_graph_info(result):
        graph = result["graph"]
        field_filter = result["field_filter"]
        package_filter = result["package_filter"]
        ...
        cli_out_write(f"Conan info result:\n\n{graph_info_result}")
        ...

    @conan_subcommand(formatters={"text": format_graph_info,
                                  "html": format_graph_html,
                                  "json": format_graph_json,
                                  "dot": format_graph_dot})
    def graph_info(conan_api, parser, subparser, *args):
        ...
        ConanOuptup().info("Conan info command output:")
        return {"graph": deps_graph,
                "field_filter": args.filter,
                "package_filter": args.package_filter,
                "conan_api": conan_api}

So we can have different output formats:

```
$ conan graph info ...  # Will use the formatter 'text' by default
$ conan graph info ... --format json
$ conan graph info ... --format html
```

There are two standard ways of outputing information as a result of a command:
- `cli_out_write(data, fg=None, bg=None, endline="\n", indentation=0)`: This will output information
   to the `stdout`. Normally used to out put the final result of the command (like a JSON).
- `ConanOutput().info(self, msg)`: This will output information to the `stderr`. Normally used to 
   output informational messages and avoid cluttering the `stdout` but not the final result of the command.

Commands parameters
-------------------

These are the passed arguments to any custom command and its sub-commands functions:

.. code-block:: python
    :caption: cmd_command.py

    from conan.cli.command import conan_command, conan_subcommand


    @conan_subcommand()
    def command_subcommand(conan_api, parser, subparser, *args):
        """
        subcommand information. This info will appear on ``conan command subcommand -h``.

        :param conan_api: <object conan.api.conan_api.ConanAPI> instance
        :param parser: root <object argparse.ArgumentParser> instance (coming from main command)
        :param subparser: <object argparse.ArgumentParser> instance for sub-command
        :param args: ``list`` of all the arguments passed after sub-command call
        :return: (optional) whatever is returned will be passed to formatters functions (if declared)
        """
        # ...


    @conan_command(group="Custom commands")
    def command(conan_api, parser, *args):
        """
        command information. This info will appear on ``conan command -h``.

        :param conan_api: <object conan.api.conan_api.ConanAPI> instance
        :param parser: root <object argparse.ArgumentParser> instance
        :param args: ``list`` of all the arguments passed after command call
        :return: (optional) whatever is returned will be passed to formatters functions (if declared)
        """
        # ...


* ``conan_api``: instance of ``ConanAPI`` class. See more about it in :ref:`conan.api.conan_api.ConanAPI section<reference_python_api_conan_api>`
* ``parser``: root instance of Python ``argparse.ArgumentParser`` class to be used by the main command function. See more information
  in `argparse official website <https://docs.python.org/3/library/argparse.html>`_.
* ``subparser`` (only for sub-commands): child instance of Python ``argparse.ArgumentParser`` class for each sub-command function.
* ``*args``: list of all the arguments passed via command line to be parsed and used inside the command function.
  Normally, they'll be parsed as ``args = parser.parse_args(*args)``. For instance, running :command:`conan mycommand arg1 arg2 arg3`,
  the command function will receive them as a Python list-like ``["arg1", "arg2", "arg3"]``.


Read more
---------

- :ref:`Custom command to remove recipe and package revisions but the latest package one from the latest recipe one<examples_extensions_commands_clean_revisions>`.
