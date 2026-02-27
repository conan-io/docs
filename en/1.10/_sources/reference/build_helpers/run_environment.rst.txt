.. _run_environment_reference:

RunEnvironment
==============

The ``RunEnvironment`` helper prepares ``PATH``, ``LD_LIBRARY_PATH`` and ``DYLD_LIBRARY_PATH`` environment variables to locate shared libraries and executables of your requirements at runtime.

.. warning::

    The ``RunEnvironment`` is no longer needed, at least explicitly in *conanfile.py*. It has been integrated
    into the ``self.run(..., run_environment=True)`` argument. Check :ref:`self.run()<running_commands>`.

This helper is specially useful if:

- You are requiring packages with shared libraries and you are running some executable that needs those libraries.
- You have a requirement with some tool (executable) and you need it to be in the path.

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


It sets the following environment variables:

+--------------------+---------------------------------------------------------------------+
| NAME               | DESCRIPTION                                                         |
+====================+=====================================================================+
| PATH               | Containing all the requirements ``bin`` folders.                    |
+--------------------+---------------------------------------------------------------------+
| LD_LIBRARY_PATH    | Containing all the requirements ``lib`` folders. (Linux)            |
+--------------------+---------------------------------------------------------------------+
| DYLD_LIBRARY_PATH  | Containing all the requirements ``lib`` folders. (OSX)              |
+--------------------+---------------------------------------------------------------------+

.. important::

    Security restrictions might apply in OSX
    (`read this thread <https://stackoverflow.com/questions/35568122/why-isnt-dyld-library-path-being-propagated-here>`_), so the
    ``DYLD_LIBRARY_PATH`` environment variable is not directly transferred to the child process. In that case, you have to use it explicitly in
    your *conanfile.py*:

    .. code-block:: python

        def build(self):
            env_build = RunEnvironment(self)
            with tools.environment_append(env_build.vars):
                # self.run('./myexetool") # won't work, even if 'DYLD_LIBRARY_PATH' is in the env
                self.run('DYLD_LIBRARY_PATH=%s ./myexetool" % os.environ['DYLD_LIBRARY_PATH'])

    This is already handled automatically by the ``self.run(..., run_environment=True)`` argument.

.. seealso::

    - :ref:`manage_shared_libraries_env_vars`
    - :ref:`environment_append_tool`
