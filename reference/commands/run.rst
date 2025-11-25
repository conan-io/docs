
conan run
=========

.. autocommand::
    :command: conan run -h


The conan run command lets you directly execute a binary from a Conan package, automatically resolving and installing
all its dependencies. There’s no need to manually activate environments: just pass the executable,
and Conan runs it.

The command can receive either a conanfile or have the requirements specified directly in the cli.

For example, if we to call an specific version of openssl we would:

.. code-block:: bash

    $ conan run "openssl --version" --tool-requires=openssl/3.5.4

    Installing and building dependencies, this might take a while...
    OpenSSL 3.5.4 30 Sep 2025 (Library: OpenSSL 3.5.4 30 Sep 2025)

This command is useful when you want to execute somme specific binary from any package.

.. note::
    This command activates both the ``host`` and ``build`` contexts, so that both contexts binaries are made available at once.
    In case that a packege exists in both contexts, the ``host`` context binaries take precedence.

.. seealso::

    See here for more advanced examples of ``conan run`` usages
