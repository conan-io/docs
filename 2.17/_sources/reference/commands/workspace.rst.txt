.. _reference_commands_workspace:

conan workspace
===============

.. include:: ../../common/incubating_warning.inc


The ``conan workspace`` command allows to open, add, and remove packages from the current workspace. Check the
``conan workspace -h`` help and the help of the subcommands to check their usage.


.. autocommand::
    :command: conan workspace -h


conan workspace init
--------------------

.. autocommand::
    :command: conan workspace init -h


The command ``conan workspace init [path]`` creates an empty ``conanws.yml`` file and a minimal ``conanws.py`` within that path
if they don't exist yet. That path can be relative to your current working directory.

.. code-block:: bash

   $ conan workspace init myfolder
   Created empty conanws.yml in myfolder
   Created minimal conanws.py in myfolder


conan workspace [add | remove]
------------------------------

.. autocommand::
    :command: conan workspace add -h

.. autocommand::
    :command: conan workspace remove -h


Use these commands to add or remove editable packages to the current workspace. The ``conan workspace add <path>``
folder must contain a ``conanfile.py``. That path can be relative to your current workspace.

The ``conanws.py`` has a default implementation, but it is possible to override the default behavior:

.. code-block:: python
   :caption: conanws.py

   import os
   from conan import Workspace

   class MyWorkspace(Workspace):
      def name(self):
         return "myws"

      def add(self, ref, path, *args, **kwargs):
         self.output.info(f"Adding {ref} at {path}")
         super().add(ref, path, *args, **kwargs)

      def remove(self, path, *args, **kwargs):
         self.output.info(f"Removing {path}")
         return super().remove(path, *args, **kwargs)


conan workspace info
--------------------

.. autocommand::
    :command: conan workspace info -h


Use this command to show information about the current workspace

.. code-block:: bash

   $ cd myfolder
   $ conan new workspace
   $ conan workspace info
   WARN: Workspace found
   WARN: Workspace is a dev-only feature, exclusively for testing
   name: myfolder
   folder: /path/to/myfolder
   products
      app1
   packages
      liba/0.1
         path: liba
      libb/0.1
         path: libb
      app1/0.1
         path: app1


conan workspace clean
---------------------

.. autocommand::
    :command: conan workspace clean -h


The new ``conan workspace clean`` command removes by default the ``output-folder`` of every package in the workspace if it was defined.
If it is not defined, it won't remove anything by default, as removing files in user space is dangerous, and could destroy user changes or files.
It would be recommended that users manage that cleaning with ``git clean -xdf`` or similar strategies.
It is also possible to define a custom clean logic by implementing the ``clean()`` method:

.. code-block:: python

   class Ws(Workspace):
      def name(self):
         return "my_workspace"
      def clean(self):
         self.output.info("MY CLEAN!!!!")



conan workspace open
--------------------

.. autocommand::
    :command: conan workspace open -h


The new ``conan workspace open`` command implements a new concept. The packages containing an ``scm`` information in
the ``conandata.yml`` (with ``git.coordinates_to_conandata()``) can be automatically cloned and checkout inside the
current workspace from their Conan recipe reference (including recipe revision).


conan workspace build
---------------------

.. autocommand::
    :command: conan workspace build -h


The command ``conan workspace build`` does the equivalent of ``conan build <product-path> --build=editable``,
for every ``product`` defined within the workspace.

Products are the "downstream" consumers, the "root" and starting node of dependency graphs. They can be defined with the
``conan workspace add <folder> --product`` new ``--product`` argument.

The ``conan workspace build`` command just iterates all products, so it might repeat the build of editables dependencies
of the products. In most cases, it will be a no-op as the projects would be already built, but might still take some time.
This is pending for optimization, but that will be done later, the important thing now is to focus on tools, UX, flows,
and definitions (of things like the ``products``).


conan workspace install
-----------------------

.. autocommand::
    :command: conan workspace install -h


The command ``conan workspace install`` is useful to install and build the current workspace
as a monolithic super-project of the editables.

By default it uses all the ``editable`` packages in the workspace. It is possible to select
only a subset of them with the ``conan workspace install <folder1> .. <folderN>`` optional
arguments. Only the subgraph of those packages, including their dependencies and transitive
dependencies will be installed.


.. seealso::

    Read the :ref:`Workspace tutorial<tutorial_workspaces>` section.
    Read the :ref:`conan new workspace<reference_commands_new>` command section.
