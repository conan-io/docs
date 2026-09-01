.. _reference_commands:

Commands
========

This section describes the Conan built-in commands, like ``conan install`` or ``conan search``.

It is also possible to create user custom commands, visit :ref:`custom commands reference <reference_commands_custom_commands>`
and these :ref:`custom command examples <examples_extensions_custom_commands>`


**Consumer commands:**

.. toctree::
   :caption: Consumer commands
   :maxdepth: 1
   :hidden:

   commands/cache
   commands/config
   commands/graph
   commands/inspect
   commands/install
   commands/list
   commands/lock
   commands/pkglist
   commands/profile
   commands/remove
   commands/remote
   commands/search
   commands/version
   commands/workspace

- :doc:`conan cache <commands/cache>`: Return the path of recipes and packages in the cache
- :doc:`conan config <commands/config>`: Manage Conan configuration (remotes, settings, plugins, etc)
- :doc:`conan graph <commands/graph>`: Obtain information about the dependency graph without fetching binaries
- :doc:`conan inspect <commands/inspect>`: Inspect a conanfile.py to return the public fields
- :doc:`conan install <commands/install>`: Install dependencies
- :doc:`conan list <commands/list>`: List recipes, revisions and packages in the local cache or in remotes
- :doc:`conan lock <commands/lock>`: Create and manage lockfiles
- :doc:`conan pkglist <commands/pkglist>`: Manipulate package lists, merge them or find packages in remotes.
- :doc:`conan profile <commands/profile>`: Display and manage profile files
- :doc:`conan remove <commands/remove>`: Remove packages from the local cache or from remotes
- :doc:`conan remote <commands/remote>`: Add, remove, login/logout and manage remote server
- :doc:`conan search <commands/search>`: Search packages matching a name
- :doc:`conan version <commands/version>`: Give information about the Conan client version
- :doc:`conan workspace (incubating) <commands/workspace>`: Manage Conan workspaces


**Creator commands:**

..  toctree::
    :caption: Creator commands
    :maxdepth: 1
    :hidden:

    commands/build
    commands/create
    commands/download
    commands/editable
    commands/export
    commands/export-pkg
    commands/new
    commands/source
    commands/test
    commands/upload

- :doc:`conan build <commands/build>`: Install package and call its build method
- :doc:`conan create <commands/create>`: Create a package from a recipe
- :doc:`conan download <commands/download>`: Download (without install) a single conan package from a remote server.
- :doc:`conan editable <commands/editable>`: Allows working with a package in user folder
- :doc:`conan export <commands/export>`: Export a recipe to the Conan package cache
- :doc:`conan export-pkg <commands/export-pkg>`: Create a package directly from pre-compiled binaries
- :doc:`conan new <commands/new>`: Create a new recipe from a predefined template
- :doc:`conan source <commands/source>`: Calls the source() method
- :doc:`conan test <commands/test>`: Test a package
- :doc:`conan upload <commands/upload>`: Upload packages from the local cache to a specified remote

**Security Commands**

.. toctree::
   :caption: Security Commands
   :maxdepth: 1
   :hidden:

   commands/audit
   commands/report

- :doc:`conan audit <commands/audit>`: Checks for vulnerabilities in your Conan packages.
- :doc:`conan report <commands/report>`: Get information about the packages

.. _commands_output:

**Commands Output to stdout and stderr**

Conan commands output information following a deliberate design choice that aligns with
common practices in many CLI tools and the `POSIX standard
<https://pubs.opengroup.org/onlinepubs/9699919799/functions/stderr.html>`_:

- ``stdout``: For final command results (e.g., JSON, HTML).
- ``stderr``: For diagnostic output, including logs, warnings, errors, and progress
  messages.

More info can be found more in the :ref:`FAQ section<faq_stdout_stderr_redirects>`.

**Redirecting Output to Files**

You can redirect Conan output to files using shell redirection:

.. code-block:: bash

    $ conan install . --format=json > output.json

Alternatively, use the ``--out-file`` argument (available since Conan 2.12.0) to specify an
output file directly:

.. code-block:: bash

    $ conan install . --format=json --out-file=output.json


Command formatters
------------------

Almost all the commands have the parameter ``--format xxxx`` which is used to apply an output conversion.
The command formatters help users see the command output in a different way that could fit better with their needs.
Here, there are only some of the most important ones whose details are worthy of having a separate section.


.. toctree::
   :caption: Command formatters
   :maxdepth: 1
   :hidden:

   commands/formatters/graph_info_json_formatter


- :doc:`graph-info formatter <commands/formatters/graph_info_json_formatter>`: Show the graph information in JSON
  format. It's used by several commands.
