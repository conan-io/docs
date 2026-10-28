.. _conan_tools_microsoft_msbuilddeps:


MSBuildDeps
============

The ``MSBuildDeps`` is the dependency information generator for Microsoft MSBuild build system.
It will generate multiple *xxxx.props* properties files, one per dependency of a package,
to be used by consumers using MSBuild or Visual Studio, just adding the generated properties files
to the solution and projects.


The ``MSBuildDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "MSBuildDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    MSBuildDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.microsoft import MSBuildDeps

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = MSBuildDeps(self)
            ms.generate()


Generated files
---------------

The ``MSBuildDeps`` generator is a multi-configuration generator, and generates different files for any different
Debug/Release configuration. For instance, running these commands:

.. code-block:: bash

    $ conan install .  # default is Release
    $ conan install . -s build_type=Debug

It generates the next files:

- *conan_zlib_vars_release_x64.props*: ``Conanzlibxxxx`` variables definitions for the ``zlib`` dependency,
  Release config, like ``ConanzlibIncludeDirs``, ``ConanzlibLibs``, etc.
- *conan_zlib_vars_debug_x64.props*: Same ``Conanzlib``variables for ``zlib`` dependency, Debug config
- *conan_zlib_release_x64.props*: Activation of ``Conanzlibxxxx`` variables in the current build as standard C/C++
  build configuration, Release config. This file contains also the transitive dependencies definitions.
- *conan_zlib_debug_x64.props*: Same activation of ``Conanzlibxxxx`` variables, Debug config, also inclusion
  of transitive dependencies.
- *conan_zlib.props*: Properties file for ``zlib``. It conditionally includes, depending on the configuration,
  one of the two immediately above Release/Debug properties files.
- Same 5 files are generated for every dependency in the graph, in this case ``conan_bzip.props`` too, which
  conditionally includes the Release/Debug bzip properties files.
- *conandeps.props*: Properties files that includes all direct dependencies, for this case ``conan_zlib.props``
  and ``conan_bzip2.props``

Add the *conandeps.props* to your solution project files if you want to depend on all the declared
dependencies. For single project solutions, this is probably the way to go. For multi-project solutions, you might
be more efficient and add properties files per project. You could add *conan_zlib.props* properties to "project1"
in the solution and *conan_bzip2.props* to "project2" in the solution for example.

The above files are generated when the package doesn't have components. If the package has defined components, the following files
will be generated:

- *conan_pkgname_compname_vars_release_x64.props*: Definition of variables for the component ``compname`` of the package ``pkgname``
- *conan_pkgname_compname_release_x64.props*: Activation of the above variables into VS effective variables to be used in the build
- *conan_pkgname_compname.props*: Properties file for component ``compname`` of package ``pkgname``. It conditionally includes, depending on the configuration,
  the specific activation property files.
- *conan_pkgname.props*: Properties file for package ``pkgname``. It includes and aggregates all the components of the package.
- *conandeps.props*: Same as above, aggregates all the direct dependencies property files for the packages (like ``conan_pkgname.props``)

If your project depends only on certain components, the specific ``conan_pkgname_compname.props`` files can be added to the project instead of the global or
the package ones.

Requirement traits support
++++++++++++++++++++++++++

The above generated files, more specifically the files containing the variables (``conan_pkgname_vars_release_x64.props/conan_pkgname_compname_vars_release_x64.props``),
will not contain all the information if the requirement traits have excluded them. For example, by default, the ``includedirs`` of transitive dependencies
will be empty, as those headers shouldn't be included by the user unless a specific ``requires`` to that package is defined.


Configurations
---------------

If your Visual Studio project defines custom configurations, like ``ReleaseShared``, or ``MyCustomConfig``,
it is possible to define it into the ``MSBuildDeps`` generator, so different project configurations can
use different set of dependencies. Let's say that our current project can be built as a shared library,
with the custom configuration ``ReleaseShared``, and the package also controls this with the ``shared``
option:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.microsoft import MSBuildDeps

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        options = {"shared": [True, False]}
        default_options = {"shared": False}
        requires = "zlib/1.2.11"

        def generate(self):
            ms = MSBuildDeps(self)
            # We assume that -o *:shared=True is used to install all shared deps too
            if self.options.shared:
                ms.configuration = str(self.settings.build_type) + "Shared"
            ms.generate()

This generates new properties files for this custom configuration, and switching it
in the IDE allows to gather dependencies configuration like Debug/Release, and
even static and/or shared libraries.

Dependencies
--------------

``MSBuildDeps`` uses the ``self.dependencies`` to access to the dependencies information. The following
dependencies are translated to properties files:

- All the direct dependencies, which are the ones declared by the current ``conanfile``, live in the
  ``host`` context: all regular ``requires``, plus the ``tool_requires``, that are in the host context, e.g.
  test frameworks like ``gtest`` or ``catch``.
- All transitive ``requires`` of those direct dependencies (all in the host context)
- Tool requires, in the build context, that is, application and executables that run in the build
  machine irrespective of the destination platform, are added exclusively to the ``<ExecutablePath>``
  property, taking the value from ``$(Conan{{name}}BinaryDirectories)`` defined properties. This
  allows to define custom build commands, invoke code generation tools, with the ``<CustomBuild>`` and
  ``<Command>`` elements.


Customization
---------------

conf
++++

``MSBuildDeps`` is affected by these ``[conf]`` variables:

- ``tools.microsoft.msbuilddeps:exclude_code_analysis`` list of packages names patterns to be added to the
  Visual Studio ``CAExcludePath`` property.


Reference
---------

.. currentmodule:: conan.tools.microsoft

.. autoclass:: MSBuildDeps
    :members: generate
