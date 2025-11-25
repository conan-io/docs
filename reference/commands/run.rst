
conan run
=========

.. autocommand::
    :command: conan run -h


The conan run command lets you directly execute a binary from a Conan package, automatically resolving and installing
all its dependencies. There’s no need to search for paths or manually activate environments: just pass the executable,
and Conan runs it.

For example, if we have a package called mypackage with dependencies on zlib and cmake, we can run it like this:

.. code-block:: bash

    $ conan run mypackage --requires=zlib/1.3 --tool-requires=cmake/3.31.6

This will automatically install zlib and cmake if needed, set up the proper environment, and execute the mypackage
binary in a single step.