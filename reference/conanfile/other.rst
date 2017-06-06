Output and Running
==================

Output contents
---------------

Use the `self.output` to print contents to the output.

..  code-block:: python

   self.output.success("This is a good, should be green")
   self.output.info("This is a neutral, should be white")
   self.output.warn("This is a warning, should be yellow")
   self.output.error("Error, should be red")
   self.output.rewrite_line("for progress bars, issues a cr")

Check the source code. You might be able to produce different outputs with different colors.


Running commands
----------------

``self.run()`` is a helper to run system commands and throw exceptions when errors occur,
so that command errors are do not pass unnoticed. It is just a wrapper for ``os.system()``

Optional parameters:

- ``output``: Defaulted to True, will write in stdout. You can pass any stream that accepts a ``write`` method like a ``StringIO.StringIO()``
  Note: Be careful with the Python2 and Python3 compatibility, StringIO has been realocated between them.

- ``cwd``: Current directory to run the command. Default "."

