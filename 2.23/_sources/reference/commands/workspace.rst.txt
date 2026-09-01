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
   packages
     - path: liba
       ref: liba/0.1
     - path: libb
       ref: libb/0.1
     - path: app1
       ref: app1/0.1


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


conan workspace root
--------------------

.. autocommand::
    :command: conan workspace root -h


Return the folder containing the conanws.py/conanws.yml workspace file.


conan workspace source
----------------------

.. autocommand::
    :command: conan workspace source -h

The command ``conan workspace source`` performs the equivalent of ``conan source <package-path>`` for every ``package``
defined within the workspace.


conan workspace install
-----------------------

.. autocommand::
    :command: conan workspace install -h


The command ``conan workspace install`` performs the equivalent of ``conan install <package-path>`` for every ``package``
defined within the workspace in the correct order.


conan workspace build
---------------------

.. autocommand::
    :command: conan workspace build -h


The command ``conan workspace build`` performs the equivalent of ``conan build <package-path>`` for every ``package``
defined within the workspace in the correct order.


conan workspace create
----------------------

.. autocommand::
    :command: conan workspace create -h

The command ``conan workspace create`` performs the equivalent of ``conan create <package-path>`` for every ``package``
defined within the workspace in the correct order. They will be created in the Conan cache, not locally.


conan workspace super-install
-----------------------------

.. autocommand::
    :command: conan workspace super-install -h


The command ``conan workspace super-install`` is useful to install and build the current workspace
as a monolithic super-project of the editables.

By default it uses all the ``editable`` packages in the workspace. It is possible to select
only a subset of them with the ``conan workspace super-install --pkg=pkg_name1 --pkg=pkg_name2`` optional
arguments. Only the subgraph of those packages, including their dependencies and transitive
dependencies will be installed.


.. seealso::

    Read the :ref:`Workspace tutorial<tutorial_workspaces>` section.
    Read the :ref:`conan new workspace<reference_commands_new>` command section.
