.. _reference_conanfile_output:


Running and output
==================

Output text from recipes
------------------------

Use the ``self.output`` attribute to output text from the recipes. Do **not** use Python's ``print()`` function.
The ``self.output`` attribute has the following methods to express the level of the printed message:

..  code-block:: python

   trace(msg)
   debug(msg)
   verbose(msg)
   status(msg)
   info(msg)
   highlight(msg)
   success(msg)
   warning(msg, warn_tag=None)
   error(msg)



These output functions will only output if the verbosity level with which Conan was launched is the same or higher than the message,
so running with ``-vwarning`` will output calls to ``warning()`` and ``error()``, but not ``info()``
(Additionally, the ``highlight()`` and ``success()`` methods have a ``-vnotice`` verbosity level)

Note that these methods return the output object again, so that you can chain output calls if needed.

Using the ``core:warnings_as_errors`` conf, you can make Conan raise an exception when either errors or a tagged warning matching any of the given patterns is printed.
This is useful to make sure that recipes are not printing unexpected warnings or errors.
Additionally, you can skip which warnings trigger an exception :ref:`with the *core:skip_warnings* conf<reference_config_files_global_conf_skip_warnings>`.

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


.. _reference_conanfile_run:


Running commands
----------------

.. code-block:: python

    run(self, command, stdout=None, cwd=None, ignore_errors=False, env="", quiet=False, shell=True, scope="build", stderr=None)


``self.run()`` is a helper to run system commands while injecting the calls to activate the appropriate environment,
and throw exceptions when errors occur so that command errors do not pass unnoticed.
It also wraps the commands with the results of the :ref:`command wrapper plugin<reference_extensions_command_wrapper>`.


* ``command`` should be specified as a string which is passed to the system shell.
* When the argument ``quiet`` is set to true, the invocation of ``self.run()`` will not print the command to be executed.

Use the ``stdout`` and ``stderr`` arguments to redirect the output of the command to a file-like object instead of the console.

.. code-block:: python

    # Redirect stdout to a file
    with open("ninja_stdout.log", "w") as stdout:
        # Redirect stderr to a StringIO object to be able to read it later
        stderr = StringIO()
        self.run("ninja ...", stdout=stdout, stderr=stderr)
