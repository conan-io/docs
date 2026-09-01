.. _reference_commands_audit:

conan audit
===========

The ``conan audit`` command is used to check for known vulnerabilities in your Conan packages.

See :ref:`the audit devops page<devops_audit>` to see examples on how to use the ``conan audit`` command.


conan audit scan
================

.. autocommand::
    :command: conan audit scan -h

The ``conan audit scan`` checks for vulnerabilities in the given references and their transitive dependencies.
This command receives configuration arguments such as profiles and settings, to control the expansion of the graph.

conan audit list
================

.. autocommand::
    :command: conan audit list -h

The ``conan audit list`` command lists vulnerabilities for the given references, without checking their transitive dependencies.
You can pass a single reference, or a pkglist file with multiple references.

conan audit provider
====================

.. autocommand::
    :command: conan audit provider -h

The ``conan audit provider`` command manages the list of providers used to check for vulnerabilities.

By default the ``conan audit`` subcommands use the ConanCenter provider, but you can add your own providers to the list.
For now, besides the default ConanCenter provider, only private JFrog Security providers are supported, see :ref:`the audit devops page<devops_audit_private_providers>` for more information.

There are 3 subcommands:
- ``conan audit provider auth``: Authenticates a provider with a token.
- ``conan audit provider add``: Adds a provider to the list.
- ``conan audit provider remove``: Removes a provider from the list.
