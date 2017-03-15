Runtime dependencies and execution
====================================

The ``RunEnvironment`` helper prepare some environment variables to locate shared libraries and executables of your requirements at runtime:


+--------------------+---------------------------------------------------------------------+
| NAME               | DESCRIPTION                                                         |
+====================+=====================================================================+
| PATH               | Containing all the requirements ``bin`` folders.                    |
+--------------------+---------------------------------------------------------------------+
| LD_LIBRARY_PATH    | Containing all the requirements ``lib`` folders. (Linux)            |
+--------------------+---------------------------------------------------------------------+
| DYLIB_LIBRARY_PATH | Containing all the requirements ``lib`` folders. (OSX)              |
+--------------------+---------------------------------------------------------------------+


This helper is specially useful:

- If you are requiring packages with shared libraries and you are running some executable that needs those libraries.
- If you have a requirement with some tool (executable) and you need it in the path.


Example:


.. code-block:: python
   :emphasize-lines: 7, 8, 9

   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):
      ...

      def build(self):
         env_build = RunEnvironment(self)
         with tools.environment_append(env_build.vars):
            self.run("....")
            # All the requirements bin folder will be available at PATH
            # All the lib folders will be available in LD_LIBRARY_PATH and DYLIB_LIBRARY_PATH


Runtime generators
--------------------

- virtualenv
- virtualrunenv