.. _reference_extensions_command_wrapper:

Command wrapper
---------------

The ``cmd_wrapper.py`` extension plugin is a Python script that receives the command line
argument provided by ``self.run()`` recipe calls, and allows intercepting them and returning
a new one. 

This plugin must be located in the ``extensions/plugins`` cache folder, and can be installed
with the ``conan config install`` command.

For example:

.. code-block:: python

    def cmd_wrapper(cmd):
        return 'echo "{}"'.format(cmd)

Would just intercept the commands and display them to terminal, which means that all commmands
in all recipes ``self.run()`` will not execute, but just be echoed.

A more common use case would be the injection of a parallelization tools over some commands,
which could look like:

.. code-block:: python

    def cmd_wrapper(cmd):
        # lets paralellize only CMake invocations
        if cmd.startswith("cmake"):
            return 'parallel-build "{}"  --parallel-argument'.format(cmd)
        # otherwise return same command, not modified
        return cmd
