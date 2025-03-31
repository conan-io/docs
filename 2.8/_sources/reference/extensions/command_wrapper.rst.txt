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

    def cmd_wrapper(cmd, **kwargs):
        return 'echo "{}"'.format(cmd)

Would just intercept the commands and display them to terminal, which means that all commmands
in all recipes ``self.run()`` will not execute, but just be echoed.

The ``**kwargs`` is a mandatory generic argument to be robust against future changes and injection
by Conan of new keyword arguments. Not adding it, even if not used could make the extension fail
in future Conan versions.

A more common use case would be the injection of a parallelization tools over some commands,
which could look like:

.. code-block:: python

    def cmd_wrapper(cmd, **kwargs):
        # lets parallelize only CMake invocations
        if cmd.startswith("cmake"):
            return 'parallel-build "{}"  --parallel-argument'.format(cmd)
        # otherwise return same command, not modified
        return cmd

The ``conanfile`` object is passed as an argument, so it is possible to customize the behavior
depending on the caller:

.. code-block:: python

    def cmd_wrapper(cmd, conanfile, **kwargs):
        # Let's parallelize only CMake invocations, for a few specific heavy packages
        name = conanfile.ref.name
        heavy_pkgs = ["qt", "boost", "abseil", "opencv", "ffmpeg"]
        if cmd.startswith("cmake") and name in heavy_pkgs:
            return 'parallel-build "{}"  --parallel-argument'.format(cmd)
        # otherwise return same command, not modified
        return cmd
