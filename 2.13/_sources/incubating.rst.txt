.. _incubating:


Incubating features
===================

This section is dedicated to new features that are under development, looking for user testing and feedback. They are generally behind a flag to enable them to explicitly opt-in on this testing stage. They require the very latest Conan version (sometimes recommended running from the ``develop2`` source branch), and explicitly setting those flags.


New CMakeConfigDeps generator
-----------------------------

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

.. note::
   
   This generator is only intended to generate ``config.cmake`` config files, it will not generate ``Find*.cmake`` find modules, and support for it is not planned.
   Use the ``CMakeDeps`` generator for that. 


The new fields that can be defined in the ``cpp_info`` or ``cpp_info.components``, besides the already defined in :ref:`CppInfo<conan_conanfile_model_cppinfo>` are:

.. code-block:: python

   # EXPERIMENTAL FIELDS, used exclusively by new CMakeConfigDeps (-c tools.cmake.cmakedeps:new)
   self.cpp_info.type  # The type of this artifact "shared-library", "static-library", etc (same as package_type)
   self.cpp_info.location # full location (path and filename with extension) of the artifact
   self.cpp_info.link_location  # Location of the import library for Windows .lib associated to a dll
   self.cpp_info.languages # same as "languages" attribute, it can be "C", "C++"
   self.cpp_info.exe  # Definition of an executable artifact

These fields will be auto-deduced from the other ``cpp_info`` and ``components`` definitions, like the ``libs`` or ``libdirs`` fields, but the automatic deduction might have limitations. Defining them explicitly will inhibit the auto deduction and use the value as provided by the recipe.


This feature is enabled with the ``-c tools.cmake.cmakedeps:new=will_break_next`` configuration. The value ``will_break_next`` will change in next releases to emphasize the fact that this feature is not suitable for usage beyond testing. Just by enabling this conf and forcing the build of packages that use ``CMakeDeps`` will trigger the usage of the new generator.

This new generator will also be usable in ``conanfile`` files with:

.. code-block::
   :caption: conanfile.txt

   [generators]
   CMakeConfigDeps

.. code-block:: python
   :caption: conanfile.py

   class Pkg(ConanFile):
      generators = "CMakeConfigDeps"

Or: 

.. code-block:: python
   :caption: conanfile.py

   from conan import ConanFile
   from conan.tools.cmake import CMakeConfigDeps

   class TestConan(ConanFile):

      def generate(self):
         deps = CMakeConfigDeps(self)
         deps.generate()


The ``-c tools.cmake.cmakedeps:new=will_break_next`` is still necessary for this recipe ``CMakeConfigDeps`` usage, if the config is not enabled, those recipes will fail.
It is also possible to define ``-c tools.cmake.cmakedeps:new=recipe_will_break`` to enable exclusively the ``CMakeConfigDeps`` generators usages, but not the automatic
replacement of existing ``CMakeDeps`` by the ``CMakeConfigDeps``.

Note that the feature is still "incubating", even for the explicit ``CMakeConfigDeps`` generator syntax, this recipe is subject to break or be removed at any time.

For any feedback, please open new tickets in https://github.com/conan-io/conan/issues.
This feedback is very important to stabilize the feature and get it out of incubating, so even if it worked fine and you found no issue, having the positive feedback
reported is very useful.




Workspaces
----------

The workspaces feature can be enabled defining the environment variable ``CONAN_WORKSPACE_ENABLE=will_break_next``.
The value ``will_break_next`` is used to emphasize that it will change in next releases, and this feature is for testing only, it cannot be used in production.

Once the feature is enabled, workspaces are defined by the ``conanws.yml`` and/or ``conanws.py`` files.
By default, any Conan command will traverse up the file system from the current working directory to the filesystem root, until it finds one of those files. That will define the "root" workspace folder.

The ``conan workspace`` command allows to open, add, remove packages from the current workspace. Check the ``conan workspace -h`` help and the help of the subcommands to check their usage.

Dependencies added to a workspace work as local ``editable`` dependencies. They are only resolved as ``editable`` under the current workspace, if the current directory is moved outside of it, those ``editable`` dependencies won't be used anymore.

The paths in the ``conanws`` files are intended to be relative to be relocatable if necessary, or could be committed to Git in monorepo-like projects.


Workspace files syntax
++++++++++++++++++++++

The most basic implementation of a workspace is a ``conanws.yml`` file with just the definition of properties.
For example, a very basic workspace file that just defines the current CONAN_HOME to be a local folder would be:

.. code-block:: yaml
   :caption: conanws.yml
   
   home_folder: myhome


But a ``conanws.yml`` can be extended with a way more powerful ``conanws.py`` that follows the same relationship as a ``ConanFile`` does with its ``conandata.yml``, for example, it can dynamically
define the workspace home with:

.. code-block:: python
   :caption: conanws.py
   
   from conan import Workspace

   class MyWs(Workspace):

      def home_folder(self):
         # This reads the "conanws.yml" file, and returns "new_myhome"
         # as the current CONAN_HOME for this workspace
         return "new_" + self.conan_data["home_folder"]


So the command ``conan config home``:

.. code-block:: bash

   $ conan config home
   /path/to/ws/new_myhome

Will display as the current CONAN_HOME the ``new_myhome`` folder (by default it is relative 
to the folder containing the ``conanws`` file)

Likewise, a workspace ``conanws.yml`` defining 2 editables could be:

.. code-block:: yaml
   :caption: conanws.yml

   editables:
      dep1/0.1:
         path: dep1
      dep2/0.1:
         path: dep2


But if we wanted to dynamically define the ``editables``, for example based on the
existence of some ``name.txt`` and ``version.txt`` files in folders, the editables
could be defined in ``conanws.py`` as:

.. code-block:: python
   :caption: conanws.py

   import os
   from conan import Workspace

   class MyWorkspace(Workspace):

      def editables(self):
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
      def editables(self):
         result = {}
         for f in os.listdir(self.folder):
            if os.path.isdir(os.path.join(self.folder, f)):
               conanfile = self.load_conanfile(f)
               result[f"{conanfile.name}/{conanfile.version}"] = {"path": f}
         return result


Workspace commands
++++++++++++++++++

conan workspace add/remove
**************************

Use these commands to add or remove editable packages to the current workspace. The ``conan workspace add <path>`` folder must contain a ``conanfile.py``.

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
********************

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
********************

The new ``conan workspace open`` command implements a new concept. Those packages containing an ``scm`` information in the ``conandata.yml`` (with ``git.coordinates_to_conandata()``) can be automatically cloned and checkout inside the current workspace from their Conan recipe reference (including recipe revision).


conan new workspace
*******************

The command ``conan new`` has learned a new built-in (experimental) template ``workspace`` that creates a local project with some editable packages
and a ``conanws.yml`` that represents it. It is useful for quick demos, proofs of concepts and experimentation.


conan workspace build
*********************

The command ``conan workspace build`` does the equivalent of ``conan build <product-path> --build=editable``, for every ``product`` defined
in the workspace.

Products are the "downstream" consumers, the "root" and starting node of dependency graphs. They can be defined with the ``conan workspace add <folder> --product``
new ``--product`` argument.

The ``conan workspace build`` command just iterates all products, so it might repeat the build of editables dependencies of the products. In most cases, it will be a no-op as the projects would be already built, but might still take some time. This is pending for optimization, but that will be done later, the important thing now is to focus on tools, UX, flows, and definitions (of things like the ``products``).


conan workspace install
***********************

The command ``conan workspace install`` is useful to install and build the current workspace
as a monolithic super-project of the editables. See next section.


Workspace monolithic builds
+++++++++++++++++++++++++++

Conan workspaces can be built as a single monolithic project (sometimes called super-project),
which can be very convenient. Let's see it with an example:

.. code-block:: bash

   $ conan new workspace
   $ conan workspace install
   $ cmake --preset conan-release # use conan-default in Win
   $ cmake --build --preset conan-release

Let's explain a bit what happened.
First the ``conan new workspace`` created a template project with some relevant files:

The ``CMakeLists.txt`` defines the super-project with:

.. code-block:: cmake
   :caption: CMakeLists.txt

   cmake_minimum_required(VERSION 3.25)
   project(monorepo CXX)

   include(FetchContent)

   function(add_project SUBFOLDER)
      FetchContent_Declare(
         ${SUBFOLDER}
         SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/${SUBFOLDER}
         SYSTEM
         OVERRIDE_FIND_PACKAGE
      )
      FetchContent_MakeAvailable(${SUBFOLDER})
   endfunction()

   add_project(liba)
   # They should be defined in the liba/CMakeLists.txt, but we can fix it here
   add_library(liba::liba ALIAS liba)
   add_project(libb)
   add_library(libb::libb ALIAS libb)
   add_project(app1)

So basically, the super-project uses ``FetchContent`` to add the subfolders sub-projects.
For this to work correctly, the subprojects must be CMake based sub projects with
``CMakeLists.txt``. Also, the subprojects must define the correct targets as would be
defined by the ``find_package()`` scripts, like ``liba::liba``. If this is not the case,
it is always possible to define some local ``ALIAS`` targets.

The other important part is the ``conanws.py`` file:


.. code-block:: python
   :caption: conanws.py

   from conan import Workspace
   from conan import ConanFile
   from conan.tools.cmake import CMakeDeps, CMakeToolchain, cmake_layout

   class MyWs(ConanFile):
      """ This is a special conanfile, used only for workspace definition of layout
      and generators. It shouldn't have requirements, tool_requirements. It shouldn't have
      build() or package() methods
      """
      settings = "os", "compiler", "build_type", "arch"

      def generate(self):
         deps = CMakeDeps(self)
         deps.generate()
         tc = CMakeToolchain(self)
         tc.generate()

      def layout(self):
         cmake_layout(self)

   class Ws(Workspace):
      def root_conanfile(self):
         return MyWs  # Note this is the class name


The role of the ``class MyWs(ConanFile)`` embedded conanfile is important, it defines
the super-project necessary generators and layout.

The ``conan workspace install`` does not install the different editables separately, for
this command, the editables do not exist, they are just treated as a single "node" in
the dependency graph, as they will be part of the super-project build. So there is only
a single generated ``conan_toolchain.cmake`` and a single common set of dependencies
``xxx-config.cmake`` files for all super-project external dependencies.


The template above worked without external dependencies, but everything would work
the same when there are external dependencies. This can be tested with:

.. code-block:: bash

   $ conan new cmake_lib -d name=mymath
   $ conan create . 
   $ conan new workspace -d requires=mymath/0.1
   $ conan workspace install
   $ cmake ...


.. note::

   The current ``conan new workspace`` generates a CMake based super project.
   But it is possible to define a super-project using other build systems, like a
   MSBuild solution file that adds the different ``.vcxproj`` subprojects. As long as
   the super-project knows how to aggregate and manage the sub-projects, this is possible.

   It might also be possible for the ``add()`` method in the ``conanws.py`` to manage the 
   addition of the subprojects to the super-project, if there is some structure.


For any feedback, please open new tickets in https://github.com/conan-io/conan/issues.
