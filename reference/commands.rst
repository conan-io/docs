.. _reference_commands:

Commands
========

This section describe the Conan built-in commmands, like ``conan install`` or ``conan search``.

It is also possible to create user custom commands, visit :ref:`custom commands reference <reference_commands_custom_commands>` 
and these :ref:`custom command examples <examples_extensions_custom_commands>`



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
   commands/profile
   commands/remove
   commands/remote
   commands/search


- :doc:`conan cache <commands/cache>`: Return the path of recipes and packages in the cache
- :doc:`conan config <commands/cache>`: Manage Conan configuration (remotes, settings, plugins, etc)
- :doc:`conan graph <commands/cache>`: Obtain information about the dependency graph without fetching binaries
- :doc:`conan inspect <commands/inspect>`: Inspect a conanfile.py to return the public fields
- :doc:`conan install <commands/install>`: Install dependencies
- :doc:`conan list <commands/list>`: List recipes, revisions and packages in the local cache or in remotes
- :doc:`conan lock <commands/lock>`: Create and manage lockfiles
- :doc:`conan profile <commands/profile>`: Display and manage profile files
- :doc:`conan remove <commands/remove>`: Remove packages from the local cache or from remotes
- :doc:`conan remote <commands/remote>`: Add, remove, login/logout and manage remote server
- :doc:`conan search <commands/search>`: Search packages matching a name


.. toctree::
   :caption: Creator commands
   :maxdepth: 1
   :hidden:

   commands/upload

- :doc:`conan upload <commands/upload>`: Upload packages from the local cache to a specified remote
