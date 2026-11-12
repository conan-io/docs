
.. _run_environment_reference:

RunEnvironment
==============

The ``RunEnvironment`` helper prepare ``PATH``, ``LD_LIBRARY_PATH`` and ``DYLD_LIBRARY_PATH`` environment variables to locate shared libraries and executables of your requirements at runtime.

This helper is specially useful:

- If you are requiring packages with shared libraries and you are running some executable that needs those libraries.
- If you have a requirement with some tool (executable) and you need it in the path.

.. code-block:: python
   :emphasize-lines: 7, 8, 9

   from conans import ConanFile, RunEnvironment

   class ExampleConan(ConanFile):
      ...

      def build(self):
         env_build = RunEnvironment(self)
         with tools.environment_append(env_build.vars):
            self.run("....")
            # All the requirements bin folder will be available at PATH
            # All the lib folders will be available in LD_LIBRARY_PATH and DYLD_LIBRARY_PATH


Set environment variables:

+--------------------+---------------------------------------------------------------------+
| NAME               | DESCRIPTION                                                         |
+====================+=====================================================================+
| PATH               | Containing all the requirements ``bin`` folders.                    |
+--------------------+---------------------------------------------------------------------+
| LD_LIBRARY_PATH    | Containing all the requirements ``lib`` folders. (Linux)            |
+--------------------+---------------------------------------------------------------------+
| DYLD_LIBRARY_PATH  | Containing all the requirements ``lib`` folders. (OSX)              |
+--------------------+---------------------------------------------------------------------+


.. seealso:: - :ref:`Reference/Tools/environment_append <environment_append_tool>`