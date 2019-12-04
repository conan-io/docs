.. _debugging_packages:

Debugging packages
------------------

One of the core features of Conan is to distribute existing binaries that matches the configuration
requested instead of building from sources. In C++, even if those binaries correspond to a
*Debug* build, that's not enough to run a debug session and step into the library sources,
the debugger will need the actual sources or the `pdb files`_ (if using Visual Studio).

.. _`pdb files`: https://en.wikipedia.org/wiki/Program_database

That shouldn't be a big issue if the debug packages include the sources or the `pdb` files
together with the actual binaries; nevertheless, there is one more thing needed: the debugger
has to find those files in order to use them and here it is another problem: Conan packages
are usually generated in a different machine to the one they are being consumed (it can be
generated once in a CI server and consumed by dozens of developers) and paths in different
machines might we different. Binaries, depending on the system, include a path to the sources in
order to find the debug symbols, but that path would be the one in the machine where the binaries
are generated and not the path in the developers machine.

The only **rule of thumb is to compile the library we want to debug in the developer machine**, and
thanks to Conan this is straightforward:

.. code-block:: bash

   conan install <reference> --build <name> --profile <debug_profile>

This command will trigger the build of the library locally in our cache, so the binaries will
point to the sources where they are located and the debugger will find them.


.. note::

    Keep updated as we are investigating more integrated solutions using :ref:`hooks <hooks>`
    and for the major IDEs, :ref:`Visual Studio <visual_studio>` and :ref:`CLion <clion>`.
