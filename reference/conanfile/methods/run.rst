.. _reference_conanfile_methods_run:

run()
=====

Running commands
----------------

.. code-block:: python

    run(self, command, stdout=None, cwd=None, ignore_errors=False, env="", quiet=False, shell=True, scope="build")


``self.run()`` is a helper to run system commands while injecting the calls to activate the appropriate environment,
and throw exceptions when errors occur so that command errors do not pass unnoticed.
It also wraps the commands with the results of the :ref:`command wrapper plugin<reference_extensions_command_wrapper>`.


* ``command`` should be specified as a string which is passed to the system shell.
* When the argument ``quiet`` is set to true, the invocation of ``self.run()`` will not print the command to be executed.
