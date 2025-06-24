.. _reference_workspace_files:

Workspace files
===============

.. include:: ../common/incubating_warning.inc

Workspaces are defined by the ``conanws.yml`` and/or ``conanws.py`` files that will define the "root" workspace folder.

conanws.yml
-----------

The most basic implementation of a workspace is a ``conanws.yml`` file. It defines the workspace's ``packages`` (editable packages).
For instance, a workspace ``conanws.yml`` defining 2 ``packages`` could be:

.. code-block:: yaml
   :caption: conanws.yml

   packages:
      - path: dep1
        ref: dep1/0.1
      - path: dep2
        ref: dep2/0.1


Moreover, it could not have the ``ref`` field, and let Conan read the *name/version* from the respective *path/conanfile.py*:

.. code-block:: yaml
   :caption: conanws.yml

   packages:
      - path: dep1
      - path: dep2


conanws.py
----------

A ``conanws.yml`` can be extended with a way more powerful ``conanws.py`` that follows the same relationship as
a ``ConanFile`` does with its ``conandata.yml``. If we want to dynamically define the ``packages``, for example based
on the existence of some ``name.txt`` and ``version.txt`` files in folders, the packages could be defined in ``conanws.py`` as:

.. code-block:: python
   :caption: conanws.py

   import os
   from conan import Workspace

   class MyWorkspace(Workspace):

      def packages(self):
         result = []
         for f in os.listdir(self.folder):
            if os.path.isdir(os.path.join(self.folder, f)):
               with open(os.path.join(self.folder, f, "name.txt")) as fname:
                  name = fname.read().strip()
               with open(os.path.join(self.folder, f, "version.txt")) as fversion:
                  version = fversion.read().strip()
               result.append({"path": f, "ref": f"{name}/{version}"})
         return result


It is also possible to re-use the ``conanfile.py`` logic in ``set_name()`` and ``set_version()``
methods, using the ``Workspace.load_conanfile()`` helper:

.. code-block:: python
   :caption: conanws.py

   import os
   from conan import Workspace

   class MyWorkspace(Workspace):
      def packages(self):
         result = []
         for f in os.listdir(self.folder):
            if os.path.isdir(os.path.join(self.folder, f)):
               conanfile = self.load_conanfile(f)
               result.append({"path": f, "ref": f"{conanfile.name}/{conanfile.version}"})
         return result


.. seealso::

    Read :ref:`the Workspace tutorial<tutorial_workspaces>` section.
