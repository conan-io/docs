.. _tutorial_workspaces:

Workspaces
==========

.. include:: ../../common/incubating_warning.inc


In the previous section, we worked with *editable packages* and how to define a custom layout. Let's introduce the concept
of *workspace* and how to use it.

Introduction
------------

.. important::

   The workspace feature can be enabled defining the environment variable ``CONAN_WORKSPACE_ENABLE=will_break_next``.
   The value ``will_break_next`` is used to emphasize that it will change in next releases, and this feature is for testing only,
   it cannot be used in production.


A Conan *workspace* gives you the chance to manage several packages as ``editable`` mode in an
*orchestrated* or *monolithic* (also called *super-project*) way:

* *orchestrated*, we denote Conan building the editable packages one by one starting on the applications/consumers if exist.
* *monolithic*, we denote the editable packages built as a monolith, generating a single result (generators, etc) for the whole workspace.

Notice that the packages added to the workspace are automatically resolved as ``editable`` ones. Those editable packages
are named as workspace's ``packages``. Also, the root consumers of those ``packages`` are named as ``products``.


How to define a workspace
-------------------------

Workspaces are defined by the files ``conanws.yml`` and/or ``conanws.py`` files. Any Conan workspace command will traverse
up the file system from the current working directory to the filesystem root, until it finds one of those files. That will
define the "root" workspace folder. The paths in the ``conanws`` file are intended to be relative to be relocatable if
necessary, or could be committed to Git in monorepo-like projects.

Through the ``conan workspace`` command, we can open, add, and/or remove ``packages`` and ``products`` from the current workspace.

.. seealso::

    Read the :ref:`workspace files<reference_workspace_files>` section.
    Read the :ref:`conan workspace command<reference_commands_workspace>` section.

.. _tutorial_workspaces_monolithic:

Monolithic build
----------------

Conan workspaces can be built as a single monolithic project (super-project), which can be very convenient.
Let's see it with an example:

.. code-block:: bash

   $ conan new workspace
   $ conan workspace install
   $ cmake --preset conan-release # use conan-default in Win
   $ cmake --build --preset conan-release


Let's explain a bit what happened.
At first, the ``conan new workspace`` created a template project with some relevant files and the following structure:

..  code-block:: text

   .
   ├── CMakeLists.txt
   ├── app1
   │    ├── CMakeLists.txt
   │    ├── conanfile.py
   │    ├── src
   │    │    ├── app1.cpp
   │    │    ├── app1.h
   │    │    └── main.cpp
   │    └── test_package
   │        └── conanfile.py
   ├── conanws.py
   ├── conanws.yml
   ├── liba
   │    ├── CMakeLists.txt
   │    ├── conanfile.py
   │    ├── include
   │    │    └── liba.h
   │    ├── src
   │    │    └── liba.cpp
   │    └── test_package
   │        ├── CMakeLists.txt
   │        ├── conanfile.py
   │        └── src
   │            └── example.cpp
   └── libb
       ├── CMakeLists.txt
       ├── conanfile.py
       ├── include
       │    └── libb.h
       ├── src
       │    └── libb.cpp
       └── test_package
           ├── CMakeLists.txt
           ├── conanfile.py
           └── src
               └── example.cpp


The root ``CMakeLists.txt`` defines the super-project with:

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
For this to work correctly, the subprojects must be CMake based subprojects with
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


.. _tutorial_workspaces_orchestrated:

Orchestrated build
------------------

Conan workspaces can also build the different ``packages`` separately, and taking into account if there are ``products``
consuming them.

Let's use another structure to understand better how it works. Now, let's create it from scratch with the ``conan workspace init .`` that creates an almost empty conanws.py/conanws.yml, and using the ``conan new cmake_lib/cmake_exe`` basic templates, that create regular CMake-based conan packages:

.. code-block:: bash

   $ mkdir myproject && cd myproject
   $ conan workspace init .
   $ conan new cmake_lib -d name=hello -d version=1.0 -o hello
   $ conan new cmake_exe -d name=app -d version=1.0 -d requires=hello/1.0 -o app

Those commands created a file structure like this:

.. code-block:: text

   .
   ├── conanws.py
   ├── conanws.yml
   ├── app
   │    ├── CMakeLists.txt
   │    ├── conanfile.py
   │    ├── src
   │    │    ├── app.cpp
   │    │    ├── app.h
   │    │    └── main.cpp
   │    └── test_package
   │        └── conanfile.py
   └── hello
        ├── CMakeLists.txt
        ├── conanfile.py
        ├── include
        │    └── hello.h
        ├── src
        │    └── hello.cpp
        └── test_package
            ├── CMakeLists.txt
            ├── conanfile.py
            └── src
                └── example.cpp


Now, the ``conanws.yml`` is empty and the ``conanws.py`` has a quite minimal definition. Let's add the ``app`` application
(consumes ``hello``) and the ``hello`` lib as a new ``products`` and ``packages`` respectively to the workspace:

.. code-block:: bash

   $ conan workspace add hello
   Reference 'hello/1.0' added to workspace
   $ conan workspace add app --product
   Reference 'app/1.0' added to workspace

Defined the workspace's ``packages`` and ``products``, we can build them and execute the application:

.. code-block:: bash

   $ conan workspace build
   $ app/build/Release/app
   hello/1.0: Hello World Release!
   ...
   app/1.0: Hello World Release!
   ...


For any feedback, please open new tickets in https://github.com/conan-io/conan/issues.
