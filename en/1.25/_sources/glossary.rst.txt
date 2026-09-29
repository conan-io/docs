
.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   conanfile
      Can refer to either `conanfile.txt` or `conanfile.py` depending on what's the context it is
      used in.

   conanfile.py
      The file that defines a Conan recipe that is typically used to create packages, but can be used
      also to consume packages only (see conanfile.txt). Inside of this recipe, it is defined (among
      other things) how to download the package's source code, how to build the binaries from those
      sources, how to package the binaries and information for future consumers on how to consume
      the package.

   conanfile.txt
      It is a simplified version of the `conanfile.py` used only for consuming packages. It defines a
      list of packages to be consumed by a project and can also define the
      :ref:`generators<generators>` for the build system we are using, and if we want to
      :ref:`import<imports_txt>` files from the dependencies, as shared libraries, executables or
      assets.

   recipe
      Python script defined in a `conanfile.py` that specifies how the package is built from sources,
      what the final binary artifacts are, the package dependencies, etc.

   recipe reference
      A recipe reference is the combination of the package name, version, and two optional fields
      named user and channel that could be useful to identify a forked recipe from the community with
      changes specific to your company. It adopts the form of ``name/version@user/channel``.

   package reference
      A package reference is the combination of the recipe reference and the package ID. It adopts
      the form of ``name/version@user/channel:package_id_hash``.

   package
      A Conan package is a collection of files that include the recipe and the N binary packages
      generated for different configurations and settings. It can contain binary files such as
      libraries, headers or tools to be reused by the consumer of the package.

   lockfile
      Files that store the information with the exact versions, revisions, options, and configuration
      of a dependency graph. They are intended to make the building process reproducible even if the
      dependency definitions in conanfile recipes are not fully deterministic.

   revision
      It is the :ref:`mechanism<package_revisions>` to implicitly version the changes done in a recipe or
      package without bumping the actual reference or package version.

   recipe revision
      A unique ID using the latest VCS hash or a checksum of the `conanfile.py` with
      the exported files if any. See the :ref:`revisions mechanism<package_revisions>` page.

   package revision
      A unique ID using the checksum of the package (all files stored in a binary package). See the :ref:`revisions mechanism<package_revisions>` page.

   package ID
      The package id is a hash of the settings options and requirements used to identify the binary
      packages.  Applying different profiles to the `conan create` command, it will generate
      different package IDs. e.g: Windows, x86, shared...

   binary package
      Output binary usually obtained with a `conan create` command applying settings and options as input. Usually, there are N
      binary packages inside one Conan package, one for each set of settings and options. Every
      binary package is identified by a package_id.

   settings
      A set of keys and values, like  `os`, `compiler` and `build_type` that are declared at the
      `~/.conan/settings.yml` file.

   options
      :ref:`Options<conanfile_options>` are declared in the recipes, it is similar to
      the `setting` concept but it is something that can be defaulted by the recipe creator, like if
      a library is static or shared. Options are specific to each package (there is not a yml file
      like the `settings.yml` file), and each package creator can define their options "header_only"
      for example. The most common example is the "shared" option, with possibles values `True/False`
      and typically defaulted to `False`.

   requirement
      Packages on which another package depends on. They are represented by a conan reference:
      `lib/1.0@`

   build requirement
      Requirements that are only needed when you need to build a package (that declares the `build requirement`)
      from sources, but if the binary package already exists, the build-require is not retrieved.

   dependency graph
      A directed graph representing dependencies of several Conan packages towards each other. The
      relations between the packages are declared with the `requirements` in the recipes. A
      dependency graph in Conan depends on the input profile applied because the requirements can be
      :ref:`conditioned<conditional_settings_options_requirements>` to a specific configuration.

   build system
      Tools used to automate the process of building binaries from sources. Some examples are Make,
      Autotools, SCons, CMake, Premake, Ninja or Meson. Conan has integrations with some of these
      build systems using :ref:`generators<generators>` and :ref:`build helpers<build_helpers>`.

   toolchain
      A toolchain is the set of tools usually intended for compiling, debugging and profiling
      applications.

   cross compiler
      A cross compiler is a compiler capable of creating an executable intended to run in a platform
      different from the one in which the compiler is running.

   generator
      A generator provides the information of dependencies calculated by Conan in a suitable format
      that is usually injected in a build system. They normally provide a file that can be included
      or passed as input to the specific build system to help it to find the packages declared in the
      recipe. There are other generators that are not intended to be used with the build system. e.g.
      :ref:`"deploy"<deploy_generator>`, :ref:`"YouCompleteMe"<youcompleteme_integration>`.

   build helper
      A build helper is a Python script that translates Conan settings to the specific settings of a
      build tool. For example, in the case of CMake, the build helper sets the CMake flag for
      the generator from Conan settings like the compiler, operating system, and architecture. Conan
      provides integration for several build tools such as :ref:`CMake<cmake_reference>`,
      :ref:`Autotools<autotools_reference>`, :ref:`MSBuild<msbuild>` or
      :ref:`Meson<meson_build_reference>`. You can also `integrate your preferred build system
      <https://blog.conan.io/2019/07/24/C++-build-systems-new-integrations-in-Conan-package-manager.html>`_
      in Conan if it is not available by default.

   system packages
      System packages are packages that are typically installed system-wide via system package
      management tools such as apt, yum, pkg, pkgutil, brew or pacman. It is possible to install
      :ref:`system-wide packages methods<method_system_requirements>` from Conan adding a
      ``system_requirements()`` method to the conanfile.

   hook
      :ref:`Conan Hooks <hooks>` are Python scripts containing functions that will be executed before
      and after a particular task performed by the Conan client. Those tasks could be Conan commands,
      recipe interactions such as exporting or packaging, or interactions with the remotes. For
      example, you could have a hook that checks that the recipe includes attributes like license,
      url and description.

   semantic versioning
      Versioning system with versions in the form of ``MAJOR.MINOR.PATCH`` where ``PATCH`` version
      changes when you make backward-compatible bug fixes, ``MINOR`` version changes when you add
      functionality in a backward-compatible manner, and ``MAJOR`` version changes when you make
      incompatible API changes. Conan uses semantic versioning by default but this behavior can be
      :ref:`easily configured and changed<define_abi_compatibility>` in the ``package_id()`` method
      of your conanfile, and any versioning scheme you desire is supported.

   local cache
      A folder in which Conan stores the package cache and some configuration files such as the
      `conan.conf` or `settings.yml`. By default, this file will be located in the user home folder
      **~/.conan/** but it's configurable with the environment variable ``CONAN_USER_HOME``. In some
      scenarios like CI environments or when using per-project management and storage changing the
      default conan cache location :ref:`could be useful<custom_cache>`.

   editable package
      A :ref:`package<editable_packages>` that resides in the user workspace, but is consumed as if
      it was in the cache. This mode is useful when you are developing the packages, and the projects
      that consume them at the same time.

   workspace
      :ref:`Conan workspaces<workspaces>` allow us to have more than one package in user folders and
      have them directly use other packages from user folders without needing to put them in the
      local cache. Furthermore, they enable incremental builds on large projects containing multiple
      packages.

   transitive dependency
      A dependency that is induced by the dependency that the program references directly. Imagine
      that your project uses the **Poco** library that needs the **OpenSSL** library, and **OpenSSL**
      is calling to the zlib library. In this case, **OpenSSL** and **zlib** would be transitive
      dependencies.

   profile
      :ref:`A profile<conan_profile>` is the set of different settings, options, environment
      variables and build requirements used when working with packages. The settings define the
      operating system, architecture, compiler, build type, and C++ standard. Options define, among
      other things, if dependencies are linked in shared or static mode or other compile options.

   library
      A library is a collection of code and resources to be reused by other programs.

   shared library
      A library that is loaded at runtime into the target application.

   static library
      A library that is copied at compile time to the target application.

   remote
      The binary repository that hosts Conan packages inside a server.

