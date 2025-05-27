.. _tutorial_workspace:

Workspace (incubating)
======================

.. include:: ../../common/incubating_warning.inc


The workspaces feature can be enabled defining the environment variable ``CONAN_WORKSPACE_ENABLE=will_break_next``.
The value ``will_break_next`` is used to emphasize that it will change in next releases, and this feature is for testing only,
it cannot be used in production.

Once the feature is enabled, workspaces are defined by the ``conanws.yml`` and/or ``conanws.py`` files
It's recommended to learn more about :ref:`the conanws.[yml|py] files section<reference_conanws>` before moving forward).
By default, any Conan workspace command will traverse up the file system from the current working directory to the filesystem root,
until it finds one of those files. That will define the "root" workspace folder.

The ``conan workspace`` command allows to open, add, remove packages from the current workspace.
Check the :ref:`conan workspace command<reference_commands_workspace>` to know more about its usage.

Dependencies added to a workspace work as local ``editable`` dependencies. They are only resolved as ``editable`` under
the current workspace, if the current directory is moved outside of it, those ``editable`` dependencies won't be used anymore.
Those editable dependencies are named as workspace's ``packages``. There is another concept named as ``products``
that refers to root consumers of those packages.

The paths in the ``conanws`` files are intended to be relative to be relocatable if necessary, or could be committed to
Git in monorepo-like projects.


.. _tutorial_workspace_monolithic:

Workspace monolithic builds
---------------------------


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

So basically, the super-project uses ``FetchContent`` to add the subfolders' sub-projects.
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
