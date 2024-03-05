.. _reference_commands_install:

conan install
=============

.. autocommand::
    :command: conan install -h


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
    

.. _reference_commands_install_generators_deployers:

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

It is possible to also invoke the package recipes ``deploy()`` method with the ``--deployer-package``:

.. code-block:: bash

    # Execute deploy() method of every recipe that defines it
    $ conan install --requires=pkg/0.1 --deployer-package=*
    # Execute deploy() method only for "pkg" (any version) recipes
    $ conan install --requires=pkg/0.1 --deployer-package=pkg/*

The ``--deployer-package`` argument is a pattern and accept multiple values, all package references matching any of the defined patterns will execute its ``deploy()`` method. The ``--deployer-folder`` argument will also affect the output location of this deployment. See the :ref:`deploy() method<reference_conanfile_methods_deploy>`.

If multiple deployed packages deploy to the same location, it is their responsibility to not mutually overwrite their binaries if they have the same filenames. For example if multiple packages ``deploy()`` a file called "License.txt", each recipe is responsible for creating an intermediate folder with the package name and/or version that makes it unique, so other recipes ``deploy()`` method do not overwrite previously deployed "License.txt" files.


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


Also, it is likely that the majority of lockfile operations are better managed by the ``conan lock`` command.

.. seealso::

    - :ref:`tutorial_consuming_packages_versioning_lockfiles`.
    - Read the tutorial about the :ref:`local package development flow <local_package_development_flow>`.


Update
------

The ``conan install`` command has an ``--update`` argument that will force the re-evaluation of the selected items of the dependency graph,
allowing for the update of the dependencies to the latest version if using version ranges, or to the latest revision of the same version,
when those versions are not locked in the given lockfile. Passing ``--update`` will check every package in the dependency graph,
but it is also possible to pass a package name to the ``--update`` argument (it can be added to the command more than once with different names),
to only update those packages, which avoids the re-evaluation of the whole graph.

.. code-block:: bash

   $ conan install . --update  # Update all packages in the graph
   $ conan install . --update=openssl  # Update only the openssl package
   $ conan install . --update=openssl --update=boost  # Update both openssl and boost packages
