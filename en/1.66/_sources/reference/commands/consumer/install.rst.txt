
.. _conan_install:

conan install
=============

.. code-block:: bash

     $ conan install [-h] [-g GENERATOR] [-if INSTALL_FOLDER] [-of OUTPUT_FOLDER] [-m [MANIFESTS]] [-mi [MANIFESTS_INTERACTIVE]]
                     [-v [VERIFY]] [--no-imports] [--build-require] [-j JSON] [-b [BUILD]] [-r REMOTE] [-u] [-l LOCKFILE] [--lockfile-out LOCKFILE_OUT]
                     [-e ENV_HOST] [-e:b ENV_BUILD] [-e:h ENV_HOST] [-o OPTIONS_HOST] [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST] [-pr PROFILE_HOST]
                     [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST] [-s SETTINGS_HOST] [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST] [-c CONF_HOST]
                     [-c:b CONF_BUILD] [-c:h CONF_HOST] [--lockfile-node-id LOCKFILE_NODE_ID] [--require-override REQUIRE_OVERRIDE]
                     path_or_reference [reference]


Installs the requirements specified in a recipe (conanfile.py or conanfile.txt).

It can also be used to install a concrete package specifying a
reference. If any requirement is not found in the local cache, it will
retrieve the recipe from a remote, looking for it sequentially in the
configured remotes. When the recipes have been downloaded it will try
to download a binary package matching the specified settings, only from
the remote from which the recipe was retrieved. If no binary package is
found, it can be built from sources using the '--build' option. When
the package is installed, Conan will write the files for the specified
generators.

.. code-block:: text

    positional arguments:
      path_or_reference     Path to a folder containing a recipe (conanfile.py or
                            conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt. It could also be a
                            reference
      reference             Reference for the conanfile path of the first
                            argument: user/channel, version@user/channel or
                            pkg/version@user/channel(if name or version declared
                            in conanfile.py, they should match)

    optional arguments:
      -h, --help            show this help message and exit
      -g GENERATOR, --generator GENERATOR
                            Generators to use
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Use this directory as the directory where to put the
                            generatorfiles. e.g., conaninfo/conanbuildinfo.txt
      -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                            The root output folder for generated and build files
      -m [MANIFESTS], --manifests [MANIFESTS]
                            Install dependencies manifests in folder for later
                            verify. Default folder is .conan_manifests, but can be
                            changed
      -mi [MANIFESTS_INTERACTIVE], --manifests-interactive [MANIFESTS_INTERACTIVE]
                            Install dependencies manifests in folder for later
                            verify, asking user for confirmation. Default folder
                            is .conan_manifests, but can be changed
      -v [VERIFY], --verify [VERIFY]
                            Verify dependencies manifests against stored ones
      --no-imports          Install specified packages but avoid running imports
      --build-require       The provided reference is a build-require
      -j JSON, --json JSON  Path to a json file where the install information will
                            be written
      -b [BUILD], --build [BUILD]
                            Optional, specify which packages to build from source.
                            Combining multiple '--build' options on one command
                            line is allowed. For dependencies, the optional
                            'build_policy' attribute in their conanfile.py takes
                            precedence over the command line parameter. Possible
                            parameters: --build Force build for all packages, do
                            not use binary packages. --build=never Disallow build
                            for all packages, use binary packages or fail if a
                            binary package is not found. Cannot be combined with
                            other '--build' options. --build=missing Build
                            packages from source whose binary package is not
                            found. --build=outdated Build packages from source
                            whose binary package was not generated from the latest
                            recipe or is not found. --build=cascade Build packages
                            from source that have at least one dependency being
                            built from source. --build=[pattern] Build packages
                            from source whose package reference matches the
                            pattern. The pattern uses 'fnmatch' style wildcards.
                            --build=![pattern] Excluded packages, which will not
                            be built from the source, whose package reference
                            matches the pattern. The pattern uses 'fnmatch' style
                            wildcards. Default behavior: If you omit the '--build'
                            option, the 'build_policy' attribute in conanfile.py
                            will be used if it exists, otherwise the behavior is
                            like '--build=never'.
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -u, --update          Will check the remote and in case a newer version
                            and/or revision of the dependencies exists there, it
                            will install those in the local cache. When using
                            version ranges, it will install the latest version
                            that satisfies the range. Also, if using revisions, it
                            will update to the latest revision for the resolved
                            version range.
      -l LOCKFILE, --lockfile LOCKFILE
                            Path to a lockfile
      --lockfile-out LOCKFILE_OUT
                            Filename of the updated lockfile
      -e ENV_HOST, --env ENV_HOST
                            (Deprecated) Environment variables that will be set
                            during the package build (host machine). e.g.: -e
                            CXX=/usr/bin/clang++
      -e:b ENV_BUILD, --env:build ENV_BUILD
                            (Deprecated) Environment variables that will be set
                            during the package build (build machine). e.g.: -e:b
                            CXX=/usr/bin/clang++
      -e:h ENV_HOST, --env:host ENV_HOST
                            (Deprecated) Environment variables that will be set
                            during the package build (host machine). e.g.: -e:h
                            CXX=/usr/bin/clang++
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
                            Configuration to build the package, overwriting the defaults (host machine). e.g.: -c
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:b CONF_BUILD, --conf:build CONF_BUILD
                            Configuration to build the package, overwriting the defaults (build machine). e.g.: -c:b
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:h CONF_HOST, --conf:host CONF_HOST
                            Configuration to build the package, overwriting the defaults (host machine). e.g.: -c:h
                            tools.cmake.cmaketoolchain:generator=Xcode
      --lockfile-node-id LOCKFILE_NODE_ID
                            NodeID of the referenced package in the lockfile
      --require-override REQUIRE_OVERRIDE
                            Define a requirement override


:command:`conan install` executes methods of a *conanfile.py* in the following order:

1. ``config_options()``
2. ``configure()``
3. ``layout()``
4. ``requirements()``
5. ``package_id()``
6. ``validate()``
7. ``validate_build()``
8. ``package_info()``
9. ``deploy()``

Note this describes the process of installing a pre-built binary package. If the package has to be built, :command:`conan install --build`
executes the following:

1. ``config_options()``
2. ``configure()``
3. ``layout()``
4. ``requirements()``
5. ``package_id()``
6. ``validate()``
7. ``validate_build()``
8. ``build_requirements()``
9. ``build_id()``
10. ``system_requirements()``
11. ``source()``
12. ``generate()``
13. ``imports()``
14. ``build()``
15. ``package()``
16. ``package_info()``
17. ``deploy()``

**Examples**

- Install a package requirement from a ``conanfile.txt``, saved in your current directory with one
  option and setting (other settings will be defaulted as defined in
  ``<userhome>/.conan/profiles/default``):

  .. code-block:: bash

      $ conan install . -o pkg_name:use_debug_mode=on -s compiler=clang

- Install the requirements defined in a ``conanfile.py`` file in your current directory, with the
  default settings in default profile ``<userhome>/.conan/profiles/default``, and specifying the
  version, user and channel (as they might be used in the recipe):

  .. code-block:: python

      class Pkg(ConanFile):
         name = "mypkg"
         # see, no version defined!
         def requirements(self):
             # this trick allow to depend on packages on your same user/channel
             self.requires("dep/0.3@%s/%s" % (self.user, self.channel))

         def build(self):
             if self.version == "myversion":
                 # something specific for this version of the package.

  .. code-block:: bash

      $ conan install . myversion@someuser/somechannel

  Those values are cached in a file, so later calls to local commands like ``conan build`` can find
  and use this version, user and channel data.

- Install the **opencv/4.1.1@conan/stable** reference with its default options and default
  settings from ``<userhome>/.conan/profiles/default``:

  .. code-block:: bash

      $ conan install opencv/4.1.1@conan/stable

- Install the **opencv/4.1.1@conan/stable** reference updating the recipe and the binary package
  if new upstream versions are available:

  .. code-block:: bash

      $ conan install opencv/4.1.1@conan/stable --update

.. _buildoptions:

build options
-------------

Both the conan **install** and **create** commands accept :command:`--build` options to specify
which packages to build from source. Combining multiple :command:`--build` options on one command
line is allowed, where a package is built from source if at least one of the given build options
selects it for the build. For dependencies, the optional ``build_policy`` attribute in their
`conanfile.py` can override the behavior of the given command line parameters.
Possible values are:

* :command:`--build`: Always build everything from source. Produces a clean re-build of all packages.
  and transitively dependent packages
* :command:`--build=never`: Conan will not try to build packages when the requested configuration
  does not match, in which case it will throw an error. This option can not be combined with other
  :command:`--build` options.
* :command:`--build=missing`: Conan will try to build packages from source whose binary package was
  not found in the requested configuration on any of the active remotes or the cache.
* :command:`--build=outdated`: Conan will try to build packages from source whose binary package was
  not built with the current recipe or when missing the binary package.
* :command:`--build=cascade`: Conan selects packages for the build where at least one of its
  dependencies is selected for the build. This is useful to rebuild packages that, directly or
  indirectly, depend on changed packages.
* :command:`--build=[pattern]`: A fnmatch case-sensitive pattern of a package reference or only the package name.
  Conan will force the build of the packages whose reference matches the given
  **pattern**. Several patterns can be specified, chaining multiple options:

   - e.g., :command:`--build=pattern1 --build=pattern2` can be used to specify more than one pattern.
   - e.g., :command:`--build=zlib` will match any package named ``zlib`` (same as ``zlib/*``).
   - e.g., :command:`--build=z*@conan/stable` will match any package starting with ``z`` with ``conan/stable`` as user/channel.

* :command:`--build=![pattern]`: A fnmatch case-sensitive pattern of a package reference or only the package name.
  Conan will exclude the build of the packages whose reference matches the given
  **pattern**. Several patterns can be specified, chaining multiple options:

   - e.g., :command:`--build=!zlib --build` Build all packages from source, except for zlib.
   - e.g., :command:`--build=!z* --build` Build all packages from source, except for those starting with ``z``

If you omit the :command:`--build` option, the ``build_policy`` attribute in `conanfile.py` will be
looked up. If it is set to ``missing`` or ``always``, this build option will be used, otherwise the
command will behave like :command:`--build=never` was set.

env variables [DEPRECATED]
--------------------------

.. warning::

    :command:`-e` parameters are deprecated and was removed in Conan 2.0. Use :command:`-c`, profile `[conf]` or
    :ref:`global.conf <global_conf>` instead.

With the :command:`-e` parameters you can define:

- Global environment variables (:command:`-e SOME_VAR="SOME_VALUE"`). These variables will be defined
  before the `build` step in all the packages and will be cleaned after the `build` execution.
- Specific package environment variables (:command:`-e zlib:SOME_VAR="SOME_VALUE"`). These variables will
  be defined only in the specified packages (e.g., zlib).

You can specify this variables not only for your direct ``requires`` but for any package in the
dependency graph.

If you want to define an environment variable but you want to append the variables declared in your
requirements you can use the [] syntax:

.. code-block:: bash

    $ conan install . -e PATH=[/other/path]

This way the first entry in the ``PATH`` variable will be */other/path* but the ``PATH`` values
declared in the requirements of the project will be appended at the end using the system path
separator.

settings
--------

With the :command:`-s` parameters you can define:

- Global settings (:command:`-s compiler="Visual Studio"`). Will apply to all the requires.
- Specific package settings (:command:`-s zlib:compiler="MinGW"`). Those settings will be applied only to
  the specified packages. They accept patterns too, like ``-s *@myuser/*:compiler=MinGW``, which means that packages that have the username "myuser" will use MinGW as compiler.
- **Experimental:** Settings only for the consumer package. (:command:`-s &:compiler="MinGW"`). If `&` is specified as the package name it will apply
  only to the consumer conanfile (.py or .txt). This is a special case because the consumer conanfile might not declare a `name` so
  it would be impossible to reference it.

You can specify custom settings not only for your direct ``requires`` but for any package in the
dependency graph.

options
-------

With the :command:`-o` parameters you can only define specific package options.

.. code-block:: bash

    $ conan install . -o zlib:shared=True
    $ conan install . -o zlib:shared=True -o bzip2:option=132
    # you can also apply the same options to many packages with wildcards:
    $ conan install . -o *:shared=True

**Experimental:** To define an option just for the consumer conanfile.py use :command:`-o &:shared=True` syntax.
If `&` is specified as the package name it will apply only to the consumer conanfile.py. This is a special case
because the consumer conanfile might not declare a `name` so it would be impossible to reference it.

.. note::

    You can use :ref:`profiles <profiles>` files to create predefined sets of **settings**,
    **options** and **environment variables**.

folders
-------

The ``--output-folder`` define together with the ``layout()`` recipe
method the location of the output files. For example, the files created by build system integrations
such as ``CMakeToolchain`` or ``PkgConfigDeps`` will be created in the folder defined by the
``layout()`` ``generators`` folder, inside the defined ``--output-folder``. By default, the
``--output-folder`` is the folder containing the ``conanfile.py``.


conf
----

With the :command:`-c` parameters you can define specific tool configurations.

.. code-block:: bash

    $ conan install . -c tools.microsoft.msbuild:verbosity=Diagnostic
    $ conan install . -c mypkg/*:tools.microsoft.msbuild:verbosity=Diagnostic
    $ conan install . -c tools.microsoft.msbuild:verbosity=Detailed -c tools.build:processes=10


.. note::
    To list all possible configurations available, run :command:`conan config list`.

.. seealso::

    You can see more information about configurations in :ref:`global.conf section <global_conf>`.


reference
---------

An optional positional argument, if used the first argument should be a path.
If the reference specifies name and/or version, and they are also declared in the ``conanfile.py``,
they should match, otherwise, an error will be raised.

.. code-block:: bash

    $ conan install . # OK, user and channel will be None
    $ conan install . user/testing # OK
    $ conan install . version@user/testing # OK
    $ conan install . pkg/version@user/testing # OK
    $ conan install pkg/version@user/testing user/channel # Error, first arg is not a path


lockfiles
---------

The ``install`` command accepts several arguments related to :ref:`lockfiles<versioning_lockfiles>`:

- ``--lockfile=<path-to-lockfile>``: The ``conan install ... --lockfile=path/to/file.lock`` command will provide an input
  lockfile to the command. Versions, revisions, and other data contained in that lockfile will be respected. If something has
  changed locally that diverges with respect the locked information in the lockfile, the command will fail.
- ``--lockfile-out=<path-to-lockfile>``: This argument will define the filename of the resulting ``install`` operation. If the
  input lockfile has not completely locked something, and the install command can, for example, build some dependency from source
  with the ``--build=<dep-name>`` argument, this will provide new data, like a new package revision. This new data can be captured
  and locked in the output lockfile.
- ``--lockfile-node-id=<node-id>``: **Experimental, subject to breaking changes**. In some cases, it is impossible to reference a package
  in the dependency graph by name or reference, because there might be several instances of it with the same one. This could happen with
  some special type of requirements, like build-requires or private requires. Providing the ``node-id``, as defined in the lockfile file,
  can define without any ambiguity the package in the graph that the command is referencing.


.. note::

  Installation of binaries can be accelerated setting up parallel downloads with the ``general.parallel_download``
  **under development** configuration in :ref:`conan_conf`.

--build-require
---------------

Available since: `1.37.0 <https://github.com/conan-io/conan/releases/tag/1.37.0>`_

The ``--build-require`` allows to install the package using the
configuration and settings of the "build" context, as it was a ``build_require``. Lets see it with an example:

We have a ``mycmake/1.0`` package, which bundles cmake executable, and we are cross-compiling from Windows
to Linux, so all the usual install commands will use something like ``-pr:b=Windows -pr:h=Linux``.
At some point we might want to install the ``build-require`` to test it, executing it directly in the
terminal, with ``-build-require`` it is possible:

.. code-block:: bash

    $ conan install mycmake/1.0@ --build-require -g virtualenv -pr:b=Windows -pr:h=Linux
    # Installs Windows package binary, not the Linux one.
    $ source ./activate.sh && mycmake
    # This will execute the "mycmake" from the Windows package.

This also works when building a dependency graph, including build-requires, in CI. As the
``conan lock build-order`` command will return a list including the build/host context, it is
possible to use that to add the ``--build-require`` to the command, and build ``build-requires``
as necessary without needing to change the profiles at all.


.. _cli_arg_require_override:

--require-override
------------------


Available since: `1.39.0 <https://github.com/conan-io/conan/releases/tag/1.39.0>`_

The ``--require-override`` argument allows to inject an override requirement to the consumer conanfile being called
by this command, that would be equivalent to:

.. code-block:: python

    class Pkg(ConanFile):

        def requirements(self):
            self.requires("zlib/1.3", override=True)

This allows to dynamically test specific versions upstream without requiring editions to conanfiles. Note however this
would not be a generally recommended practice for production, it would be better to actually update the conanfiles to
explicitly reflect in code which specific versions upstream are being used.

If the consumer conanfile already contains a direct requirement to that dependency, then such version will be directly overwritten,
but no ``override=True`` will be added (note that ``override=True`` means that the current package does not depend on that
other package).

This feature affects only to regular ``requires``, not to ``tool_requires`` or ``python_requires``, as those don't have such
an overriding mechanism, and they are private to their consumer, not propagating downstream nor upstream.
