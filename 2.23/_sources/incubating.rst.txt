.. _incubating:

Incubating features
===================

This section is dedicated to new features that are under development, looking for user testing and feedback.
They are generally behind a flag to enable them to be explicitly opted-in at this testing stage. They require the very latest
Conan version (sometimes recommended running from the ``develop2`` source branch), and explicitly setting those flags.


New CMakeConfigDeps generator
-----------------------------

This generator is designed as a replacement of the current ``CMakeDeps`` generator, with multiple pending fixes and improvements that couldn't easily be done in the current one without breaking:

- Creates real SHARED/STATIC/INTERFACE IMPORTED targets, no more artificial interface targets. The ``CONAN_LIB::`` and other similar targets do not exist anymore.
- Defines IMPORTED_CONFIGURATIONS for targets.
- CONFIG definition of dependencies matching the dependency ``Release/Debug/etc`` ``build_type``, no longer using the consumer one.
- Definition of IMPORTED_LOCATION and IMPORTED_IMPLIB for library targets.
- Definition of LINK_LANGUAGES based on the recipe ``languages`` and ``cpp_info/component`` ``languages`` properties.
- All these allows better propagation of linkage requirement and visibility, avoiding some linkage error of transitive shared libraries in Linux.
- Better definition of ``requires`` relationships across components inside the same package and with respect to other packages.
- It doesn't need any ``build_context_activated`` or ``build_context_suffix`` to use ``tool_requires`` dependencies.
- Definition of ``cpp_info/component.exe`` information (should include the ``.location`` definition too), to define EXECUTABLE targets that can be run.
- Executables from ``requires`` can also be used in non cross-build scenarios. When a ``tool_requires`` to the same depependency exists, then those executables will have priority.
- Creation of a new ``conan_cmakedeps_paths.cmake`` that contains definitions of ``<pkg>_DIR`` paths for direct finding of the dependencies. This file is also planned to be used in ``cmake-conan`` to extend its usage and avoid some current limitations due to the fact that a CMake driven installation cannot inject a toolchain later.
- (new since Conan 2.14) Better management of the system OSX Frameworks through ``cpp_info.frameworks``.
- (new since Conan 2.14) Definition of ``cpp_info/component.package_framework`` information (should include the ``.location`` definition too,
  e.g., ``os.path.join(self.package_folder, "MyFramework.framework", "MyFramework")``) to define the custom OSX Framework library to be linked against.

.. note::

   This generator is only intended to generate ``config.cmake`` config files, it will not generate ``Find*.cmake`` find modules, and support for it is not planned.
   Use the ``CMakeDeps`` generator for that.


The new fields that can be defined in the ``cpp_info`` or ``cpp_info.components``, besides the already defined in :ref:`CppInfo<conan_conanfile_model_cppinfo>` are:

.. code-block:: python

   # EXPERIMENTAL FIELDS, used exclusively by new CMakeConfigDeps (-c tools.cmake.cmakedeps:new)
   self.cpp_info.type  # The type of this artifact "shared-library", "static-library", etc (same as package_type)
   self.cpp_info.location # full location (path and filename with extension) of the artifact or the Apple Framework library one
   self.cpp_info.link_location  # Location of the import library for Windows .lib associated to a dll
   self.cpp_info.languages # same as "languages" attribute, it can be "C", "C++"
   self.cpp_info.exe  # Definition of an executable artifact
   self.cpp_info.package_framework  # Definition of an Apple Framework (new since Conan 2.14)
   self.cpp_info.sources  # List of paths to source files in the package (for packages that provide source code to consumers)


These fields will be auto-deduced from the other ``cpp_info`` and ``components`` definitions, like the ``libs`` or ``libdirs`` fields, but the automatic deduction might have limitations. Defining them explicitly will inhibit the auto deduction and use the value as provided by the recipe.

Declare sources for targets with:

.. code-block:: python

   self.cpp_info.sources = ["src/mylib.cpp", "src/other.cpp"]

This allows packages to provide source code as a dependency to consumers. The paths should be relative to the package folder.
The source files will be added as `INTERFACE_SOURCES` property to the CMake library (or component) target and consumers that
link with this target will compile the sources when building their own targets.

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

Moved to :ref:`tutorial_workspaces`

Workspace files syntax
++++++++++++++++++++++

Moved to :ref:`reference_workspace_files`


Workspace commands
++++++++++++++++++
Moved to :ref:`reference_commands_workspace`


Workspace monolithic builds
+++++++++++++++++++++++++++

Moved to :ref:`tutorial_workspaces_monolithic`


For any feedback, please open new tickets in https://github.com/conan-io/conan/issues.
