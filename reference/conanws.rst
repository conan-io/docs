.. _reference_conanws:

conanws.yml | conanws.py (incubating)
=====================================

.. include:: ../common/incubating_warning.inc


The most basic implementation of a workspace is a ``conanws.yml`` file. It defines the workspace's ``packages`` (editable dependencies)
and ``products`` (root consumers). For instance, a workspace ``conanws.yml`` defining 2 ``packages`` could be:

.. code-block:: yaml
   :caption: conanws.yml

   packages:
      dep1/0.1:
         path: dep1
      dep2/0.1:
         path: dep2


But a ``conanws.yml`` can be extended with a way more powerful ``conanws.py`` that follows the same relationship as
a ``ConanFile`` does with its ``conandata.yml``. If we want to dynamically define the ``packages``, for example based
on the existence of some ``name.txt`` and ``version.txt`` files in folders, the packages could be defined in ``conanws.py`` as:

.. code-block:: python
   :caption: conanws.py

   import os
   from conan import Workspace

   class MyWorkspace(Workspace):

      def packages(self):
         result = {}
         for f in os.listdir(self.folder):
            if os.path.isdir(os.path.join(self.folder, f)):
               with open(os.path.join(self.folder, f, "name.txt")) as fname:
                  name = fname.read().strip()
               with open(os.path.join(self.folder, f, "version.txt")) as fversion:
                  version = fversion.read().strip()
               result[f"{name}/{version}"] = {"path": f}
         return result


It is also possible to re-use the ``conanfile.py`` logic in ``set_name()`` and ``set_version()``
methods, using the ``Workspace.load_conanfile()`` helper:

.. code-block:: python
   :caption: conanws.py

   import os
   from conan import Workspace

   class MyWorkspace(Workspace):
      def packages(self):
         result = {}
         for f in os.listdir(self.folder):
            if os.path.isdir(os.path.join(self.folder, f)):
               conanfile = self.load_conanfile(f)
               result[f"{conanfile.name}/{conanfile.version}"] = {"path": f}
         return result


.. seealso::

    Read :ref:`the Workspace tutorial<tutorial_workspace>` section.
