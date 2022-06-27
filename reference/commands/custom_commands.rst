.. _examples_extensions_custom_commands:

Custom commands
=================

Since Conan 2.0, it's so easy to create your own Conan commands.

Location and naming
--------------------

All the custom commands must be located in ``[YOUR_CONAN_HOME]/extensions/commands/`` folder. If _commands_ one is not created yet,
you will have to do it. Those custom commands files must be Python files and start with the prefix ``cmd_[your_command_name].py``.
The call to the custom commands is like any other existing Conan one: :command:`conan your_command_name`.


Scoping
++++++++++

It's possible to have another folder layer to group some commands under the same topic.

For instance:

.. code-block:: text

    [YOUR_CONAN_HOME]/extensions/commands/greet/
        | - cmd_hello.py
        | - cmd_bye.py

The call to those commands change a little bit: :command:`conan [topic_name]:your_command_name`. Following the previous example:

.. code-block:: text

    $ conan greet:hello
    $ conan greet:bye


Decorators
-----------

conan_command(group=None, formatters=None)
+++++++++++++++++++++++++++++++++++++++++++

Main decorator to declare a function as a new Conan command. Where the parameters are:

* ``group`` is the name of the group of commands declared under the same name.
  This grouping will appear executing the :command:`conan -h` command.
* ``formatters`` is a dict-like Python object where the ``key`` is the formatter name and the value is the
  function instance where will be processed the information returned by the command one.


.. code-block:: python
    :caption: cmd_hello.py

    import json

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command
    from conans.cli.output import ConanOutput


    def output_json(msg):
        return json.dumps({"greet": msg})


    @conan_command(group="custom commands", formatters={"json": output_json})
    def hello(conan_api: ConanAPIV2, parser, *args):
        """
        Simple command to print "Hello World!" line
        """
        msg = "Hello World!"
        ConanOutput().info(msg)
        return msg


.. important::

    The function decorated by ``@conan_command(....)`` must have the same name as the suffix used by the Python file.
    For instance, the previous example, the file name is ``cmd_hello.py``, and the command function decorated is ``def hello(....)``.


conan_subcommand(formatters=None)
++++++++++++++++++++++++++++++++++++

Similar to ``conan_command``, but this one is declaring a sub-command of an existing custom command. For instance:

.. code-block:: python
    :caption: cmd_hello.py

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command, conan_subcommand
    from conans.cli.output import ConanOutput


    @conan_subcommand()
    def hello_moon(conan_api, parser, subparser, *args):
        """
        Sub-command of "hello" that prints "Hello Moon!" line
        """
        ConanOutput().info("Hello Moon!")


    @conan_command(group="Custom commands")
    def hello(conan_api: ConanAPIV2, parser, *args):
        """
        Simple command "hello"
        """

The command call looks like :command:`conan hello moon`.


Command function arguments
----------------------------

These are the passed arguments to any custom command and its sub-commands functions:

.. code-block:: python
    :caption: cmd_command.py

    from conans.cli.command import conan_command, conan_subcommand

    @conan_subcommand()
    def command_subcommand(conan_api, parser, subparser, *args):
        pass

    @conan_command(group="Custom commands")
    def command(conan_api, parser, *args):
        pass


* ``conan_api``: instance of ``ConanAPIV2`` class. See more about it in :ref:`ConanAPIV2 section<reference_python_api_conan_api_v2>`
* ``parser``: root instance of Python ``argparse.ArgumentParser`` class to be used by the root command. See more information in `argparse official website<https://docs.python.org/3/library/argparse.html>`_.
* ``subparser`` (only for sub-commands): child instance of Python ``argparse.ArgumentParser`` class for each sub-command.
* ``*args``: all the arguments passed via command line. Normally, they'll be parsed as ``args = parser.parse_args(*args)``.


Read more
---------

- :ref:`Custom command to remove recipe and package revisions but the latest package revision from the latest recipe revision<examples_extensions_commands_clean_revisions>`.
