conan lock
==========

The ``conan lock`` command contains several subcommands.
In addition to these commands, most of the Conan commands that compute a graph, like ``create``, ``install``,
``graph``, can both receive lockfiles as input and produce lockfiles as output.


.. toctree::
   :maxdepth: 1
   :hidden:
   :glob:

   lock/*


- :doc:`conan lock add <lock/add>`: Manually add items to a lockfile
- :doc:`conan lock remove <lock/remove>`: Manually remove items from a lockfile
- :doc:`conan lock create <lock/create>`: Evaluates a dependency graph and save a lockfile
- :doc:`conan lock merge <lock/merge>`: Merge several existing lockfiles into one.
- :doc:`conan lock update <lock/update>`: Manually update items from a lockfile


.. autocommand::
    :command: conan lock -h
