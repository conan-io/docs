.. _incubating:


Incubating features
===================

This section is dedicated to new features that are under development, looking for user testing and feedback. They are generally behind a flag to enable them to explicitly opt-in on this testing stage. They require the very latest Conan version (sometimes recommended running from the ``develop2`` source branch), and explicitly setting those flags.


New CMakeDeps generator
-----------------------

This generator is designed as a replacement of the current ``CMakeDeps`` generator, with multiple pending fixes and improvements that couldn't easily be done in the current one without breaking:

- Creates real SHARED/STATIC/INTERFACE IMPORTED targets, no more artificial interface targets. The ``CONAN_LIB::`` and other similar targets do not exist anymore.
- Defines IMPORTED_CONFIGURATIONS for targets.
- CONFIG definition of dependencies matching the dependency ``Release/Debug/etc`` ``build_type``, no longer using the consumer one.
- Definition of IMPORTED_LOCATION and IMPORTED_IMPLIB for library targets.
- Definition of LINK_LANGUAGES based on the recipe ``languages`` and ``cpp_info/component`` ``languages`` properties.
- All these allows better propagation of linkage requirement and visibility, avoiding some linkage error of transitive shared libraries in Linux.
- Better definition of ``requires`` relationships accross components inside the same package and with respect to other packages.
- It doesn't need any ``build_context_activated`` or ``build_context_suffix`` to use ``tool_requires`` dependencies.
- Definition of ``cpp_info/component.exe`` information (should include the ``.location`` definition too), to define EXECUTABLE targets that can be run.
- Executables from ``requires`` can also be used in non cross-build scenarios. When a ``tool_requires`` to the same depependency exists, then those executables will have priority.
- Creation of a new ``conan_cmakedeps_paths.cmake`` that contains definitions of ``<pkg>_DIR`` paths for direct finding of the dependencies. This file is also planned to be used in ``cmake-conan`` to extend its usage and avoid some current limitations due to the fact that a CMake driven installation cannot inject a toolchain later.

The new fields that can be defined in the ``cpp_info`` or ``cpp_info.components``, besides the already defined in :ref:`CppInfo<conan_conanfile_model_cppinfo>` are:

.. code-block:: python

   # EXPERIMENTAL FIELDS, used exclusively by new CMakeDeps (-c tools.cmake.cmakedeps:new)
   self.cpp_info.type  # The type of this artifact "shared-library", "static-library", etc (same as package_type)
   self.cpp_info.location # full location (path and filename with extension) of the artifact
   self.cpp_info.link_location  # Location of the import library for Windows .lib associated to a dll
   self.cpp_info.languages # same as "languages" attribute, it can be "C", "C++"
   self.cpp_info.exe  # Definition of an executable artifact

These fields will be auto-deduced from the other ``cpp_info`` and ``components`` definitions, like the ``libs`` or ``libdirs`` fields, but the automatic deduction might have limitations. Defining them explicitly will inhibit the auto deduction and use the value as provided by the recipe.


This feature is enabled with the ``-c tools.cmake.cmakedeps:new=will_break_next`` configuration. The value ``will_break_next`` will change in next releases to emphasize the fact that this feature is not suitable for usage beyond testing. Just by enabling this conf and forcing the build of packages that use ``CMakeDeps`` will trigger the usage of the new generator.

Known current limitations:

- At the moment it is limited to ``xxx-config.cmake`` files. It will not generate find modules yet.
- Some paths in ``conan_cmakedeps_paths.cmake`` might be missing yet, only ``CMAKE_PROGRAM_PATH`` is defined at the moment besides the packages ``<pkg>_DIR`` locations.

For any feedback, please open new tickets in https://github.com/conan-io/conan.

Workspaces
----------

The workspaces feature can be enabled defining the environment variable ``CONAN_WORKSPACE_ENABLE=will_break_next``.
The value ``will_break_next`` is used to emphasize that it will change in next releases, and this feature is for testing only, it cannot be used in production.

Once the feature is enabled, workspaces are defined by the ``conanws.yml`` and/or ``conanws.py`` files.
By default, any Conan command will traverse up the file system from the current working directory to the filesystem root, until it finds one of those files. That will define the "root" workspace folder.

The ``conan workspace`` command allows to open, add, remove packages from the current workspace. Check the ``conan workspace -h`` help and the help of the subcommands to check their usage.

Dependencies added to a workspace work as local ``editable`` dependencies. They are only resolved as ``editable`` under the current workspace, if the current directory is moved outside of it, those ``editable`` dependencies won't be used anymore.

The paths in the ``conanws`` files are intended to be relative to be relocatable if necessary, or could be committed to Git in monorepo-like projects.

The ``conanws.yml`` and ``conanws.py`` files act as a fallback, that is, by default a workspace will look for an ``editables()`` function inside the ``conanws.py`` and use it if exists. Otherwise, it will fallback to the ``editables`` definition in the ``yml`` file.

A workspace could define editables dynamically for example:

.. code-block:: python
   :caption: conanws.py

   import os
   name = "myws"

   workspace_folder = os.path.dirname(os.path.abspath(__file__))

   def editables():
      result = {}
      for f in os.listdir(workspace_folder):
         if os.path.isdir(os.path.join(workspace_folder, f)):
               name = open(os.path.join(workspace_folder, f, "name.txt")).read().strip()
               version = open(os.path.join(workspace_folder, f,
                                          "version.txt")).read().strip()
               p = os.path.join(f, "conanfile.py").replace("\\\\", "/")
               result[f"{name}/{version}"] = {"path": p}
      return result


There is also a very preliminary api that could be used to load conanfiles to reuse their ``set_version()`` methods, something like:

.. code-block:: python

   import os
   name = "myws"

   def editables(*args, **kwargs):
         result = {}
         for f in os.listdir(workspace_api.folder):
            if os.path.isdir(os.path.join(workspace_api.folder, f)):
               f = os.path.join(f, "conanfile.py").replace("\\\\", "/")
               conanfile = workspace_api.load(f)
               result[f"{conanfile.name}/{conanfile.version}"] = {"path": f}
         return result


Likewise, the ``home_folder``, to define an optional Conan cache location for this workspace, will be a fallback. A variable in ``conanws.py`` can be defined, and if it doesn't exist, it will fallback to the ``conanws.yml`` one. The ``home_folder()`` can be a function too, that uses data from the ``conanws.yml`` and extends it dynamically, like:

.. code-block:: python

   def home_folder():
      # if the conanws.yml contains "myfolder", the Conan
      # cache will be in "newmyfolder" subfolder (relative
      # to the workspace root folder)
      return "new" + conanws_data["home_folder"]

conan workspace add/remove
++++++++++++++++++++++++++

Use these commands to add or remove editable packages to the current workspace. The ``conan workspace add <path>`` folder must contain a ``conanfile.py``.

conan workspace info
++++++++++++++++++++

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
   editables
      liba/0.1
         path: liba
      libb/0.1
         path: libb
      app1/0.1
         path: app1


conan workspace open
++++++++++++++++++++

The new ``conan workspace open`` command implements a new concept. Those packages containing an ``scm`` information in the ``conandata.yml`` (with ``git.coordinates_to_conandata()``) can be automatically cloned and checkout inside the current workspace from their Conan recipe reference (including recipe revision).


conan new workspace
+++++++++++++++++++

The command ``conan new`` has learned a new built-in (experimental) template ``workspace`` that creates a local project with some editable packages
and a ``conanws.yml`` that represents it. It is useful for quick demos, proofs of concepts and experimentation.


conan workspace build
+++++++++++++++++++++

The command ``conan workspace build`` does the equivalent of ``conan build <product-path> --build=editable``, for every ``product`` defined
in the workspace.

Products are the "downstream" consumers, the "root" and starting node of dependency graphs. They can be defined with the ``conan workspace add <folder> --product``
new ``--product`` argument.



Limitations:

- At the moment, the ``workspace`` feature only manages local editables packages. It doesn't create any specific meta-project, or does any orchestrated build.
- The ``conan workspace build`` command just iterates all products, so it might repeat the build of editables dependencies of the products. In most cases, it
  will be a no-op as the projects would be already built, but might still take some time. This is pending for optimization, but that will be done later, the
  important thing now is to focus on tools, UX, flows, and definitions (of things like the ``products``).

For any feedback, please open new tickets in https://github.com/conan-io/conan.
