
.. _run_environment_reference:

RunEnvironment
==============

Prepares the needed environment variables to locate shared libraries and executables of your requirements at runtime.

.. code-block:: python
   :emphasize-lines: 7, 8, 9

    def build(self):
         env_build = RunEnvironment(self)
         with tools.environment_append(env_build.vars):
             self.run("....")


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