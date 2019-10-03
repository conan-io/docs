
.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   conanfile
      Can refer to either `conanfile.txt` or `conanfile.py` depending on what's the context it is
      used in.

   conanfile.py
      The file that defines a conan recipe that can be used to create or consume packages. Inside of this
      recipe is defined between other things how to download the package's source code, how to build
      the binaries from those sources, how to package the binaries and information for futures
      consumers on how to consume the package.

   conanfile.txt
      The file used to define a package or list of packages to be consumed by a project. Can define some
      more auxiliary files to build or run the project such as generators for different build systems
      or files to be imported fro the package to the local folder.

   recipe
      Python script defined in a `conanfile.py` that specifies how the package is built from sources, what
      the final binary artifacts are, the package dependencies, etc.

   package
      wip

   lockfile
      Files that store the information with the exact versions, revisions, options, and configuration
      of a dependency graph. They are intended to make the building process reproducible even if the
      dependency definitions in conanfile recipes are not fully deterministic

   revision
      wip

   recipe revision
      wip

   package revision
      wip

   dependency graph
      wip

   build system
      wip

   compiler
      wip

   cross compile
      wip

   client
      wip

   server
      wip

   recipe
      wip

   reference
      wip

   generator
      wip

   build helper
      wip

   metadata
      wip

   system package
      wip

   semantic versioning
      wip

   local cache
      wip

   toolchain
      wip

   hook
      wip

   workspace
      wip

   build info
      wip

   dependency
      wip

   transitive dependency
      wip

   profile
      wip

   library
      wip

   shared library
      wip

   static library
      wip

   fPIC
      wip

   soname
      wip

   rpath
      wip
