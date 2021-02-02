.. _debugging_packages:

Debugging packages
------------------

In order to run a debug session and step into the source code, the debugger needs to find
the source files (or `pdb files`_ ones for Visual Studio), for Mac and Unix system the location
of these files is stored inside the library itself.

Usually Conan packages don't include these files and if they do, the path to the local cache
might be different: in a typical scenario the packages are generated in a CI machine and the
debug session will take place in the developers one, so the path to the sources won't be
the same.

The only **rule of thumb is to compile the library we want to debug in the developer machine**, and
thanks to Conan this is straightforward:

.. code-block:: bash

   conan install <reference> --build <name> --profile <debug_profile>

This command will trigger the build of the library locally in the developer's machine, so the binaries will
point to the sources where they are actually located and the debugger will find them.


.. note::

    Keep updated as we are investigating more `integrated solutions`_ using :ref:`hooks <hooks>`
    and for the major IDEs, :ref:`Visual Studio <visual_studio>` and :ref:`CLion <clion>`.


.. _`pdb files`: https://en.wikipedia.org/wiki/Program_database
.. _`integrated solutions`: https://github.com/conan-io/conan/issues/4736