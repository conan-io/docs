
.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   conanfile
      Can refer to either `conanfile.txt` or `conanfile.py` depending on what's the context it is
      used in.

   conanfile.py
      The file that defines a Conan recipe that can be used to create or consume packages. Inside of
      this recipe, it is defined (among other things) how to download the package's source code, how to
      build the binaries from those sources, how to package the binaries and information for futures
      consumers on how to consume the package.

   conanfile.txt
      The file used to define a package or list of packages to be consumed by a project. It can define
      some more auxiliary files to build or run the project such as generators for different build
      systems or files to be imported from the package to the local folder.

   recipe
      Python script defined in a `conanfile.py` that specifies how the package is built from sources,
      what the final binary artifacts are, the package dependencies, etc.

   reference
      A package reference is the combination of the package name, version, and two optional fields
      named user and channel that could be useful to identify a forked recipe from the community with
      changes specific to your company.

   package
      A Conan package is a collection of files meant to be consumed for a certain configuration and
      settings. It can contain binary files such as libraries, headers or tools to be reused by the
      consumer of the package.

   lockfile
      Files that store the information with the exact versions, revisions, options, and configuration
      of a dependency graph. They are intended to make the building process reproducible even if the
      dependency definitions in conanfile recipes are not fully deterministic.

   revision
      Is the way to implicitly version the changes done in a recipe or package without bumping the
      actual reference or package version.

   recipe revision
      A unique ID using the latest VCS hash or a checksum of the recipe manifest (`conanfile.py` with
      files exported if any).

   package revision
      A unique ID using the checksum of the package manifest (all files stored in a binary package).

   package ID
      The package id is a hash of the settings options and requirements used to identify the binary
      packages

   binary package
      Output binary for the recipe compatible for certain settings and options.

   settings
      Settings are a set of different configurations that define the ABI of your package and that a 
      consumer can indicate as input to retrieve the correct packages for his configuration.

   options
      An option is something that can be defaulted by the package creator, like if a library is
      static or shared. Options are specific to each package, and each package creator can define
      their options "header_only" for example. There is an option that is the most usual, and
      recommended name shared = True/False

   requirement
      Packages on which another package depends on.

   build requirement
      Requirements that are only needed when you need to build a package from sources, but if the
      binary package already exists, you don’t want to install or retrieve them.

   dependency
      A component that is directly referenced by a program.

   dependency graph
      A directed graph representing dependencies of several Conan packages towards each other.

   build system
      Tools used to automate the process of building binaries from sources. Some examples are Make,
      Autotools, SCons, CMake, Premake, Ninja or Meson.

   toolchain
      A toolchain is the set of tools usually intended for compiling, debugging and profiling
      applications.

   cross compiler
      A cross compiler is a compiler capable of creating an executable intended to run in a platform
      different from the one in which the compiler is running.

   generator
      A generator provides the information of dependencies calculated by Conan in a suitable format
      for a build system. They normally provide a file that can be included or injected to the
      specific build system to help it to find the packages declared in the recipe.

   build helper
      A build helper is a Python script to translate Conan settings to the specific settings of a
      build tool.

   system packages
      System packages are packages that are typically installed system-wide via system package
      management tools such as apt, yum, pkg, pkgutil, brew or pacman.

   hook
      Hooks are Python scripts containing functions that will be executed before and after a
      particular task performed by the Conan client. Those tasks could be Conan commands, recipe
      interactions such as exporting or packaging, or interactions with the remotes.

   semantic versioning
      Versioning system with versions in the form of MAJOR.MINOR.PATCH where PATCH version changes
      when you make backward-compatible bug fixes, MINOR version changes when you add functionality
      in a backward-compatible manner, and MAJOR version changes when you make incompatible API
      changes.

   local cache
      A folder in which Conan stores the package cache and some configuration files such as the
      `conan.conf` or `settings.yml`. It's configurable with the environment variable ``CONAN_USER_HOME``.

   editable package
      A package that resides in the user workspace, but is consumed as if It was in the cache.

   workspace
      Conan workspaces allow us to have more than one package in user folders and have them directly
      use other packages from user folders without needing to put them in the local cache.
      Furthermore, they enable incremental builds on large projects containing multiple packages.

   transitive dependency
      A dependency that is induced by the dependency that the program references directly.

   profile
      A profile is the set of different settings, options, environment variables and build
      requirements that are used when working with packages.

   library
      A library is a collection of code and resources to be reused by other programs.

   shared library
      A library that is loaded at runtime into the target application.

   static library
      A library that is copied at compile time to the target application.

   remote
      The server that hosts Conan packages.

