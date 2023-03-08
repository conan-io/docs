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
- :doc:`conan lock create <lock/create>`: Evaluates a dependency graph and save a lockfile
- :doc:`conan lock merge <lock/merge>`: Merge several existing lockfiles into one.


.. code-block:: bash

   $ conan lock -h
   usage: conan lock [-h] [-v [V]] {add,create,merge} ...

   Create or manage lockfiles.

   positional arguments:
   {add,create,merge}  sub-command help
      add               Add requires, build-requires or python-requires to an existing or new lockfile. The resulting lockfile will be ordered, newer
                        versions/revisions first. References can be supplied with and without revisions like "--requires=pkg/version", but they must be
                        package references, including at least the version, and they cannot contain a version range.
      create            Create a lockfile from a conanfile or a reference.
      merge             Merge 2 or more lockfiles.

   optional arguments:
   -h, --help          show this help message and exit
   -v [V]              Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or
                        -vverbose, -vv or -vdebug, -vvv or -vtrace