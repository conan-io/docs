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
   warning(msg)
   error(msg)



These output functions will only output if the verbosity level with which Conan was launched is the same or higher than the message,
so running with ``-vwarning` will output calls to ``warning()`` and ``error()``, but not ``info()``
(Additionally, the ``highlight()`` and ``success()`` methods have a ``-vnotice`` verbosity level)

Note that these methods return the output object again, so that you can chain output calls if needed.


.. _reference_conanfile_run:


Running commands
----------------

.. code-block:: python

    run(self, command, stdout=None, cwd=None, ignore_errors=False, env="", quiet=False, shell=True, scope="build")


``self.run()`` is a helper to run system commands while injecting the calls to activate the appropriate environment,
and throw exceptions when errors occur so that command errors do not pass unnoticed.
It also wraps the commands with the results of the :ref:`command wrapper plugin<reference_extensions_command_wrapper>`.


* ``command`` should be specified as a string which is passed to the system shell.
* When the argument ``quiet`` is set to true, the invocation of ``self.run()`` will not print the command to be executed.
