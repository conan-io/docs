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



conanws.py super-build options
++++++++++++++++++++++++++++++

A ``conanws.py`` used for a super-build workspaces file can manage options in two different ways:

- It can define its own ``options`` with the normal ``conanfile.py`` syntax, so the generated ``conan_toolchain.cmake`` for the super-project uses those inputs.
- It can collect the options of the workspace's packages with the ``workspace_packages_options`` and process them in any user-custom way.


**super-project options**

A ``conanws.py`` must define the options for the super-build in the ``ConanFile`` class, and use those options in the ``generate()`` method, as it usually happens with ``conanfile.py`` files, something like:

.. code-block:: python

   from conan import ConanFile, Workspace

   class MyWs(ConanFile):
      settings = "arch", "build_type"
      options = {"myoption": [1, 2, 3]}

      def generate(self):
         self.output.info(f"Generating with my option {self.options.myoption}!!!!")

   class Ws(Workspace):
      def root_conanfile(self):
         return MyWs

Then, options can be provided with the usual syntax, via profiles or command line:

.. code-block:: bash

   $ conan workspace super-install -of=build -o "*:myoption=1"
   > conanws.py base project Conanfile: Generating with my option 1!!!!

Note there can be overlap with the ``options`` defined in the workspace packages, as for super-projects those options are simply ignored, and only the options of the super-project are taken into account to generate the ``conan_toolchain.cmake``. For example, the ``conanws.py`` can define a ``shared`` option if it is desired that the ``conan_toolchain.cmake`` will correctly define ``BUILD_SHARED_LIBS`` or not when defining something like ``-o "*:shared=True"``, as the workspace packages having the ``shared`` option information is discarded when the workspace packages are collapsed in the dependency graph to model the super-project.

**packages options**

The second alternative is to collect the ``options`` of the workspace packages that have been collapsed. Recall that in the final dependency graph, the workspace packages are no longer represented, as they are no longer individual packages but part as the current super-build. The way to access their options information is via the ``workspace_packages_options``, and that information can be used in the ``generate()`` method to do any desired action at the super-build project level.


So let's say that a workspace containing a ``dep/0.1`` package that contains the standard ``shared`` options defines the following super-build ``ConanFile``:

.. code-block:: python

   from conan import ConanFile, Workspace

   class MyWs(ConanFile):
      def generate(self):
         for pkg, options in self.workspace_packages_options.items():
            for k, v in options.items():
                  self.output.info(f"Generating with opt {pkg}:{k}={v}!!!!")

   class Ws(Workspace):
      def root_conanfile(self):
         return MyWs


Then, when the workspace package options are defined, the workspace ``ConanFile`` can collect them.

.. code-block:: bash

   $ conan workspace super-install -of=build -o "*:shared=True"
   > conanws.py base project Conanfile: Generating with opt dep/0.1:shared=True!!!!!!!!


.. note::

   In practice it is the responsibility of the workspace creator to define what to do with the options, either by defining its own options or collecting the workspace packages ones. Note it is not possible to automatically map workspace packages options to the super-project, as options are defined per-package. Two different packages could have different ``shared=True`` and ``shared=False`` values. Also, very often, the effect on the generated toolchain files is custom and implemented in each package ``generate()`` method. This effect is programmatic (not declarative), it would be extremely challenging to aggregate all these effects in a single toolchain.


.. seealso::

    Read :ref:`the Workspace tutorial<tutorial_workspaces>` section.
