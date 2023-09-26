.. _reference_commands_install:

conan install
=============

.. code-block:: text

    $ conan install -h
    usage: conan install [-h] [-v [V]] [-f FORMAT] [--name NAME]
                         [--version VERSION] [--user USER] [--channel CHANNEL]
                         [--requires REQUIRES] [--tool-requires TOOL_REQUIRES]
                         [-b BUILD] [-r REMOTE | -nr] [-u] [-o OPTIONS_HOST]
                         [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                         [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                         [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                         [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST] [-c CONF_HOST]
                         [-c:b CONF_BUILD] [-c:h CONF_HOST] [-l LOCKFILE]
                         [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]
                         [--lockfile-packages] [--lockfile-clean]
                         [--lockfile-overrides LOCKFILE_OVERRIDES] [-g GENERATOR]
                         [-of OUTPUT_FOLDER] [-d DEPLOYER]
                         [--deployer-folder DEPLOYER_FOLDER] [--build-require]
                         [path]

    Install the requirements specified in a recipe (conanfile.py or conanfile.txt).

    It can also be used to install packages without a conanfile, using the
    --requires and --tool-requires arguments.

    If any requirement is not found in the local cache, it will iterate the remotes
    looking for it. When the full dependency graph is computed, and all dependencies
    recipes have been found, it will look for binary packages matching the current settings.
    If no binary package is found for some or several dependencies, it will error,
    unless the '--build' argument is used to build it from source.

    After installation of packages, the generators and deployers will be called.

    positional arguments:
      path                  Path to a folder containing a recipe (conanfile.py or
                            conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      -f FORMAT, --format FORMAT
                            Select the output format: json
      --name NAME           Provide a package name if not specified in conanfile
      --version VERSION     Provide a package version if not specified in
                            conanfile
      --user USER           Provide a user if not specified in conanfile
      --channel CHANNEL     Provide a channel if not specified in conanfile
      --requires REQUIRES   Directly provide requires instead of a conanfile
      --tool-requires TOOL_REQUIRES
                            Directly provide tool-requires instead of a conanfile
      -b BUILD, --build BUILD
                            Optional, specify which packages to build from source.
                            Combining multiple '--build' options on one command
                            line is allowed. Possible values: --build="*" Force
                            build from source for all packages. --build=never
                            Disallow build for all packages, use binary packages
                            or fail if a binary package is not found, it cannot be
                            combined with other '--build' options. --build=missing
                            Build packages from source whose binary package is not
                            found. --build=cascade Build packages from source that
                            have at least one dependency being built from source.
                            --build=[pattern] Build packages from source whose
                            package reference matches the pattern. The pattern
                            uses 'fnmatch' style wildcards. --build=~[pattern]
                            Excluded packages, which will not be built from the
                            source, whose package reference matches the pattern.
                            The pattern uses 'fnmatch' style wildcards.
                            --build=missing:[pattern] Build from source if a
                            compatible binary does not exist, only for packages
                            matching pattern.
      -r REMOTE, --remote REMOTE
                            Look in the specified remote or remotes server
      -nr, --no-remote      Do not use remote, resolve exclusively in the cache
      -u, --update          Will check the remote and in case a newer version
                            and/or revision of the dependencies exists there, it
                            will install those in the local cache. When using
                            version ranges, it will install the latest version
                            that satisfies the range. Also, if using revisions, it
                            will update to the latest revision for the resolved
                            version range.
      -o OPTIONS_HOST, --options OPTIONS_HOST
                            Define options values (host machine), e.g.: -o
                            Pkg:with_qt=true
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                            Define options values (build machine), e.g.: -o:b
                            Pkg:with_qt=true
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                            Define options values (host machine), e.g.: -o:h
                            Pkg:with_qt=true
      -pr PROFILE_HOST, --profile PROFILE_HOST
                            Apply the specified profile to the host machine
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                            Apply the specified profile to the build machine
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                            Apply the specified profile to the host machine
      -s SETTINGS_HOST, --settings SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s compiler=gcc
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                            Settings to build the package, overwriting the
                            defaults (build machine). e.g.: -s:b compiler=gcc
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s:h compiler=gcc
      -c CONF_HOST, --conf CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:b CONF_BUILD, --conf:build CONF_BUILD
                            Configuration to build the package, overwriting the
                            defaults (build machine). e.g.: -c:b
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:h CONF_HOST, --conf:host CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c:h
                            tools.cmake.cmaketoolchain:generator=Xcode
      -l LOCKFILE, --lockfile LOCKFILE
                            Path to a lockfile. Use --lockfile="" to avoid
                            automatic use of existing 'conan.lock' file
      --lockfile-partial    Do not raise an error if some dependency is not found
                            in lockfile
      --lockfile-out LOCKFILE_OUT
                            Filename of the updated lockfile
      --lockfile-packages   Lock package-id and package-revision information
      --lockfile-clean      Remove unused entries from the lockfile
      --lockfile-overrides LOCKFILE_OVERRIDES
                            Overwrite lockfile overrides
      -g GENERATOR, --generator GENERATOR
                            Generators to use
      -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                            The root output folder for generated and build files
      -d DEPLOYER, --deployer DEPLOYER
                            Deploy using the provided deployer to the output
                            folder
      --deployer-folder DEPLOYER_FOLDER
                            Deployer output folder, base build folder by default
                            if not set
      --build-require       Whether the provided path is a build-require


The ``conan install`` command is one of the main Conan commands, and it is used to resolve and install dependencies.

This command does the following:

- Compute the whole dependency graph, for the current configuration defined by settings, options, profiles and configuration.
  It resolves version ranges, transitive dependencies, conditional requirements, etc, to build the dependency graph.
- Evaluate the existence of binaries for every package in the graph, whether or not there are precompiled binaries to download, or if
  they should be built from sources (as directed by the ``--build`` argument). If binaries are missing, it will not recompute
  the dependency graph to try to fallback to previous versions that contain binaries for that configuration. If a certain
  dependency version is desired, it should be explicitly required.
- Download precompiled binaries, or build binaries from sources in the local cache, in the right order for the dependency graph.
- Create the necessary files as requested by the "generators", so build systems and other tools can locate the locally installed dependencies
- Optionally, execute the desired ``deployers``.


.. seealso::

    - Check the :ref:`JSON format output <reference_commands_graph_info_json_format>` for this command.


Conanfile path or --requires
----------------------------

The ``conan install`` command can use 2 different origins for information. The first one is using a local ``conanfile.py`` 
or ``conanfile.txt``, containing definitions of the dependencies and generators to be used.

.. code-block:: text

    $ conan install .  # there is a conanfile.txt or a conanfile.py in the cwd
    $ conan install conanfile.py  # also works, direct reference file
    $ conan install myconan.txt  # explicit custom name
    $ conan install myfolder  # there is a conanfile in "myfolder" folder


Even if it is possible to use a custom name, in the general case, it is recommended to use the default ``conanfile.py`` 
name, located in the repository root, so users can do a straightforward ``git clone ... `` + ``conan install .``
    

The other possibility is to not have a ``conanfile`` at all, and define the requirements to be installed directly in the
command line:

.. code-block:: text

    # Install the zlib/1.2.13 library
    $ conan install --requires=zlib/1.2.13
    # Install the zlib/1.2.13 and bzip2/1.0.8 libraries
    $ conan install --requires=zlib/1.2.13 --requires=bzip2/1.0.8
    # Install the cmake/3.23.5 and ninja/1.11.0 tools
    $ conan install --tool-requires=cmake/3.23.5 --tool-requires=ninja/1.11.0
    # Install the zlib/1.2.13 library and ninja/1.11.0 tool
    $ conan install --requires=zlib/1.2.13 --tool-requires=ninja/1.11.0


In the general case, it is recommended to use a ``conanfile`` instead of defining things in the command line.


.. _reference_commands_install_composition:

Profiles, Settings, Options, Conf
---------------------------------

There are several arguments that are used to define the effective profiles that will be used, both for the "build"
and "host" contexts.

By default the arguments refer to the "host" context, so ``--settings:host, -s:h`` is totally equivalent to
``--settings, -s``. Also, by default, the ``conan install`` command will use the ``default`` profile both for the
"build" and "host" context. That means that if a profile with the "default" name has not been created, it will error.

Multiple definitions of profiles can be passed as arguments, and they will compound from left to right (right has the
highest priority)

.. code-block:: text

    # The values of myprofile3 will have higher priority
    $ conan install . -pr=myprofile1 -pr=myprofile2 -pr=myprofile3

If values for any of ``settings``, ``options`` and ``conf`` are provided in the command line, they create a profile that
is composed with the other provided ``-pr`` (or the "default" one if not specified) profiles, with higher priority,
not matter what the order of arguments is.

.. code-block:: text

    # the final "host" profile will always be build_type=Debug, even if "myprofile"
    # says "build_type=Release"
    $ conan install . -pr=myprofile -s build_type=Debug
    

Generators and deployers
------------------------

The ``-g`` argument allows to define in the command line the different built-in generators to be used:

.. code-block:: text

    $ conan install --requires=zlib/1.2.13 -g CMakeDeps -g CMakeToolchain

Note that in the general case, the recommended approach is to have the ``generators`` defined in the ``conanfile``, 
and only for the ``--requires`` use case, it would be more necessary as command line argument.

Generators are intended to create files for the build systems to locate the dependencies, while the ``deployers``
main use case is to copy files from the Conan cache to user space, and performing any other custom operations over the dependency graph,
like collecting licenses, generating reports, deploying binaries to the system, etc. The syntax for deployers is:

.. code-block:: text

    # does a full copy of the dependencies binaries to the current user folder
    $ conan install . --deployer=full_deploy


There are 2 built-in deployers:

- ``full_deploy`` does a complete copy of the dependencies binaries in the local folder, with a minimal folder
  structure to avoid conflicts between files and artifacts of different packages
- ``direct_deploy`` does a copy of only the immediate direct dependencies, but does not include the transitive
  dependencies.


Some generators might have the capability of redefining the target "package folder". That means that if some other
generator like ``CMakeDeps`` is used that is pointing to the packages, it will be pointing to the local deployed
copy, and not to the original packages in the Conan cache. See the full example in :ref:`examples_extensions_builtin_deployers_development`.

It is also possible, and it is a powerful extension point, to write custom user deployers.
Read more about custom deployers in :ref:`reference_extensions_deployers`.


Name, version, user, channel
----------------------------

The ``conan install`` command provides optional arguments for ``--name, --version, --user, --channel``. These 
arguments might not be necessary in the majority of cases. Never for ``conanfile.txt`` and for ``conanfile.py``
only in the case that they are not defined in the recipe:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.scm import Version

    class Pkg(ConanFile):
        name = "mypkg"

        def requirements(self):
            if Version(self.version) >= "3.23":
                self.requires("...")
                
    

.. code-block:: text

    # If we don't specify ``--version``, it will be None and it will fail
    $ conan install . --version=3.24


Lockfiles
---------

The ``conan install`` command has several arguments to load and produce lockfiles. 
By default, if a ``conan.lock`` file is located beside the recipe or in the current working directory
if no path is provided, will be used as an input lockfile. 

Lockfiles are strict by default, that means that
if there is some ``requires`` and it cannot find a matching locked reference in the lockfile, it will error
and stop. For cases where it is expected that the lockfile will not be complete, as there might be new
dependencies, the ``--lockfile-partial`` argument can be used.

By default, ``conan install`` will not generate an output lockfile, but if the ``--lockfile-out`` argument
is provided, pointing to a filename, like ``--lockfile-out=result.lock``, then a lockfile will be generated
from the current dependency graph. If ``--lockfile-clean`` argument is provided, all versions and revisions
not used in the current dependency graph will be dropped from the resulting lockfile.

Let's say that we already have a ``conan.lock`` input lockfile, but we just added a new ``requires = "newpkg/1.0"``
to a new dependency. We could resolve the dependencies, locking all the previously locked versions, while allowing
to resolve the new one, which was not previously present in the lockfile, and store it in a new location, or overwrite the existing lockfile:

.. code-block:: text

    # --lockfile=conan.lock is the default, not necessary
    $ conan install . --lockfile=conan.lock --lockfile-partial --lockfile-out=conan.lock 

The ``--lockfile-packages`` argument allows to create lockfiles that also lock down to the package revision, but 
it should not be necessary in the vast majority of cases, so it is discouraged in the general case.

Also, it is likely that the majority of lockfile operations are better managed by the ``conan lock`` command.


Read more about lockfiles in :ref:`tutorial_consuming_packages_versioning_lockfiles`.

.. seealso::

    - Read the tutorial about the :ref:`local package development flow <local_package_development_flow>`.
