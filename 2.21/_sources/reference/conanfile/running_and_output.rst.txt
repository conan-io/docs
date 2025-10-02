.. _reference_conanfile_output:


Running and output
==================

Output text from recipes
------------------------

Use the ``self.output`` attribute to output text from the recipes. Do **not** use Python's ``print()`` function.

.. autofunction:: conan.api.output.ConanOutput.error
.. autofunction:: conan.api.output.ConanOutput.warning
.. autofunction:: conan.api.output.ConanOutput.success
.. autofunction:: conan.api.output.ConanOutput.highlight
.. autofunction:: conan.api.output.ConanOutput.info
.. autofunction:: conan.api.output.ConanOutput.status

The following three methods are not shown by default and are usually reserved for scenarios that require a higher level
of verbosity. You can display them using the arguments ``-v``, ``-vv``, and ``-vvv`` respectively.

.. autofunction:: conan.api.output.ConanOutput.verbose
.. autofunction:: conan.api.output.ConanOutput.debug
.. autofunction:: conan.api.output.ConanOutput.trace

These output functions will only output if the verbosity level with which Conan was launched is the same or higher than the message,
so running with ``-vwarning`` will output calls to ``warning()`` and ``error()``, but not ``info()``
(Additionally, the ``highlight()`` and ``success()`` methods have a ``-vnotice`` verbosity level)

Note that these methods return the output object again, so that you can chain output calls if needed.

Using the ``core:warnings_as_errors`` conf, you can make Conan raise an exception when either errors or a tagged warning matching any of the given patterns is printed.
This is useful to make sure that recipes are not printing unexpected warnings or errors.
Additionally, you can skip which warnings trigger an exception :ref:`with the core:skip_warnings conf<reference_config_files_global_conf_skip_warnings>`.

.. code-block:: text

    # Raise an exception if any warning or error is printed
    core:warnings_as_errors=['*']
    # But skip the deprecation warnings
    core:skip_warnings=['deprecated']

Both confs accept a list of patterns to match against the warning tags.
A special ``unknown`` value can be used to match any warning without a tag.

To tag a warning, use the ``warn_tag`` argument of the ``warning()`` method in your recipes:

.. code-block:: python

    self.output.warning("Extra warning", warn_tag="custom_tag")


.. note::

   Custom commands and tools are free to instantiate their own ``ConanOutput`` object.


Some methods have optional ``fg`` and ``bg`` arguments, these are colour codes for the foreground and background of the text,
available in the ``conan.api.output.Color`` class.

.. code-block:: python

    self.output.info("This is a message", fg=Color.BLUE, bg=Color.YELLOW)


.. _reference_conanfile_run:

Running commands
----------------

Recipes and helpers can use the ``self.run()`` method to run system commands while injecting the calls to activate the appropriate environment,
and throw exceptions when errors occur so that command errors do not pass unnoticed.
It also wraps the commands with the results of the :ref:`command wrapper plugin<reference_extensions_command_wrapper>`.

.. autofunction:: conan.internal.model.conan_file.ConanFile.run

Use the ``stdout`` and ``stderr`` arguments to redirect the output of the command to a file-like object instead of the console.

.. code-block:: python

    # Redirect stdout to a file
    with open("ninja_stdout.log", "w") as stdout:
        # Redirect stderr to a StringIO object to be able to read it later
        stderr = StringIO()
        self.run("ninja ...", stdout=stdout, stderr=stderr)
