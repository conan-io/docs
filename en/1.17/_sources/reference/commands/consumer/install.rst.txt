
.. _conan_install:

conan install
=============

.. code-block:: bash

    $ conan install [-h] [-g GENERATOR] [-if INSTALL_FOLDER] [-m [MANIFESTS]]
                    [-mi [MANIFESTS_INTERACTIVE]] [-v [VERIFY]]
                    [--no-imports] [-j JSON] [-b [BUILD]] [-e ENV]
                    [-o OPTIONS] [-pr PROFILE] [-r REMOTE] [-s SETTINGS] [-u]
                    [-l [LOCKFILE]]
                    path_or_reference [reference]

Installs the requirements specified in a recipe (conanfile.py or conanfile.txt).

It can also be used to install a concrete package specifying a
reference. If any requirement is not found in the local cache, it will
retrieve the recipe from a remote, looking for it sequentially in the
configured remotes. When the recipes have been downloaded it will try
to download a binary package matching the specified settings, only from
the remote from which the recipe was retrieved. If no binary package is
found, it can be build from sources using the '--build' option. When
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
      -j JSON, --json JSON  Path to a json file where the install information will
                            be written
      -b [BUILD], --build [BUILD]
                            Optional, use it to choose if you want to build from
                            sources: --build Build all from sources, do not use
                            binary packages. --build=never Never build, use binary
                            packages or fail if a binary package is not found.
                            --build=missing Build from code if a binary package is
                            not found. --build=cascade Will build from code all
                            the nodes with some dependency being built (for any
                            reason). Can be used together with any other build
                            policy. Useful to make sure that any new change
                            introduced in a dependency is incorporated by building
                            again the package. --build=outdated Build from code if
                            the binary is not built with the current recipe or
                            when missing binary package. --build=[pattern] Build
                            always these packages from source, but never build the
                            others. Allows multiple --build parameters. 'pattern'
                            is a fnmatch file pattern of a package reference.
                            Default behavior: If you don't specify anything, it
                            will be similar to '--build=never', but package
                            recipes can override it with their 'build_policy'
                            attribute in the conanfile.py.
      -e ENV, --env ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      -o OPTIONS, --options OPTIONS
                            Define options values, e.g., -o Pkg:with_qt=true
      -pr PROFILE, --profile PROFILE
                            Apply the specified profile to the install command
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -s SETTINGS, --settings SETTINGS
                            Settings to build the package, overwriting the
                            defaults. e.g., -s compiler=gcc
      -u, --update          Check updates exist from upstream remotes
      -l [LOCKFILE], --lockfile [LOCKFILE]
                            Path to a lockfile or folder containing 'conan.lock'
                            file. Lockfile can be updated if packages change


:command:`conan install` executes methods of a *conanfile.py* in the following order:

1. ``config_options()``
2. ``configure()``
3. ``requirements()``
4. ``package_id()``
5. ``package_info()``
6. ``deploy()``

Note this describes the process of installing a pre-built binary package. If the package has to be built, :command:`conan install --build`
executes the following:

1. ``config_options()``
2. ``configure()``
3. ``requirements()``
4. ``package_id()``
5. ``build_requirements()``
6. ``build_id()``
7. ``system_requirements()``
8. ``source()``
9. ``imports()``
10. ``build()``
11. ``package()``
12. ``package_info()``
13. ``deploy()``

**Examples**

- Install a package requirement from a ``conanfile.txt``, saved in your current directory with one
  option and setting (other settings will be defaulted as defined in
  ``<userhome>/.conan/profiles/default``):

  .. code-block:: bash

      $ conan install . -o PkgName:use_debug_mode=on -s compiler=clang

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

- Install the **OpenCV/2.4.10@lasote/testing** reference with its default options and default
  settings from ``<userhome>/.conan/profiles/default``:

  .. code-block:: bash

      $ conan install opencv/2.4.10@lasote/testing

- Install the **OpenCV/2.4.10@lasote/testing** reference updating the recipe and the binary package
  if new upstream versions are available:

  .. code-block:: bash

      $ conan install opencv/2.4.10@lasote/testing --update

.. _buildoptions:

build options
-------------

Both the conan **install** and **create** commands have options to specify whether conan should try
to build things or not:

* :command:`--build=never`: This is the default option. It is not necessary to write it explicitly.
  Conan will not try to build packages when the requested configuration does not match, in which
  case it will throw an error.
* :command:`--build=missing`: Conan will try to build from source, all packages of which the
  requested configuration was not found on any of the active remotes.
* :command:`--build=outdated`: Conan will try to build from code if the binary is not built with the
  current recipe or when missing binary package.
* :command:`--build=[pattern]`: A fnmatch case-sensitive pattern of a package reference or only the package name.
  Conan will force the build of the packages whose reference matches the given
  **pattern**. Several patterns can be specified, chaining multiple options:

   - e.g., :command:`--build=pattern1 --build=pattern2` can be used to specify more than one pattern.
   - e.g., :command:`--build=zlib` will match any package named ``zlib`` (same as ``zlib/*``).
   - e.g., :command:`--build=z*@conan/stable` will match any package starting with ``z`` with ``conan/stable`` as user/channel.

* :command:`--build`: Always build everything from source. Produces a clean re-build of all packages
  and transitively dependent packages

env variables
-------------

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

    $ conan install . -e PYTHONPATH=[/other/path]

This way the first entry in the PYTHONPATH variable will be :command:`/other/path` but the PYTHONPATH values
declared in the requirements of the project will be appended at the end using the system path
separator.

settings
--------

With the :command:`-s` parameters you can define:

- Global settings (:command:`-s compiler="Visual Studio"`). Will apply to all the requires.
- Specific package settings (:command:`-s zlib:compiler="MinGW"`). Those settings will be applied only to
  the specified packages.

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

.. note::

    You can use :ref:`profiles <profiles>` files to create predefined sets of **settings**,
    **options** and **environment variables**.


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
