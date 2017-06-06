.. _conan_install_command:

conan install
=============


.. code-block:: bash

    $ conan install [-h] [--package PACKAGE] [--all] [--file FILE]
                    [--generator GENERATOR] [--werror]
                    [--manifests [MANIFESTS]]
                    [--manifests-interactive [MANIFESTS_INTERACTIVE]]
                    [--verify [VERIFY]] [--no-imports] [--update]
                    [--scope SCOPE] [--profile PROFILE] [-r REMOTE]
                    [--options OPTIONS] [--settings SETTINGS] [--env ENV]
                    [--build [BUILD [BUILD ...]]]
                    [reference]


Installs the requirements specified in a ``conanfile.py`` or ``conanfile.txt``.
It can also be used to install a concrete recipe/package specified by the ``reference`` parameter.
If the recipe is not found in the local cache it will retrieve the recipe from a remote, looking
for it sequentially in the available configured remotes.
When the recipe has been downloaded it will try to download a binary package matching the specified settings,
only from the remote from which the recipe was retrieved.
If no binary package is found you can build the package from sources using the ``--build`` option.


.. code-block:: bash


    positional arguments:
      reference             package recipe referencee.g.,
                            MyPackage/1.2@user/channel or ./my_project/

    optional arguments:
      -h, --help            show this help message and exit
      --package PACKAGE, -p PACKAGE
                            Force install specified package ID (ignore
                            settings/options)
      --all                 Install all packages from the specified package recipe
      --file FILE, -f FILE  specify conanfile filename
      --generator GENERATOR, -g GENERATOR
                            Generators to use
      --werror              Error instead of warnings for graph inconsistencies
      --manifests [MANIFESTS], -m [MANIFESTS]
                            Install dependencies manifests in folder for later
                            verify. Default folder is .conan_manifests, but can be
                            changed
      --manifests-interactive [MANIFESTS_INTERACTIVE], -mi [MANIFESTS_INTERACTIVE]
                            Install dependencies manifests in folder for later
                            verify, asking user for confirmation. Default folder
                            is .conan_manifests, but can be changed
      --verify [VERIFY], -v [VERIFY]
                            Verify dependencies manifests against stored ones
      --no-imports          Install specified packages but avoid running imports
      --update, -u          check updates exist from upstream remotes
      --scope SCOPE, -sc SCOPE
                            Use the specified scope in the install command
      --profile PROFILE, -pr PROFILE
                            Apply the specified profile to the install command
      -r REMOTE, --remote REMOTE
                            look in the specified remote server
      --options OPTIONS, -o OPTIONS
                            Options to build the package, overwriting the
                            defaults. e.g., -o with_qt=true
      --settings SETTINGS, -s SETTINGS
                            Settings to build the package, overwriting the
                            defaults. e.g., -s compiler=gcc
      --env ENV, -e ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]
                            Optional, use it to choose if you want to build from
                            sources: --build Build all from sources, do not use
                            binary packages. --build=never Default option. Never
                            build, use binary packages or fail if a binary package
                            is not found. --build=missing Build from code if a
                            binary package is not found. --build=outdated Build
                            from code if the binary is not built with the current
                            recipe or when missing binary package.
                            --build=[pattern] Build always these packages from
                            source, but never build the others. Allows multiple
                            --build parameters.


**Examples**

- Install a package requirement from a ``conanfile.txt``, saved in your current directory with one option and setting (other settings will be defaulted as defined in ``<userhome>/.conan/conan.conf``):

.. code-block:: bash

    $ conan install . -o use_debug_mode=on -s compiler=clang


.. note::

   You have to take into account that **settings** are cached as defaults in the **conaninfo.txt** file,
   so you don't have to type them again and again in the **conan install** or **conan test**
   commands.

   However, the default **options** are defined in your **conanfile**.
   If you want to change the default options across all your **conan install** commands, change
   them in the **conanfile**. When you change the **options** on the command line, they are only changed
   for one shot. Next time, **conan install** will take the **conanfile** options as default values, if you
   don't specify them again in the command line.


- Install the **OpenCV/2.4.10@lasote/testing** reference with its default options and default settings from ``<userhome>/.conan/conan.conf``:

.. code-block:: bash

    $ conan install opencv/2.4.10@lasote/testing


- Install the **OpenCV/2.4.10@lasote/testing** reference updating the recipe and the binary package if new upstream versions are available:

.. code-block:: bash

   $ conan install opencv/2.4.10@lasote/testing --update


.. _buildoptions:


build options
-------------

Both the conan **install** and **test** commands have options to specify whether conan should
try to build things or not:

* :command:`--build=never`  This is the default option. It is not necessary to write it explicitly. Conan will
  not try to build packages when the requested configuration does not match, in which case it will
  throw an error.
* :command:`--build=missing` Conan will try to build from source, all packages of which the requested configuration
  was not found on any of the active remotes.
* :command:`--build=outdated` Conan will try to build from code if the binary is not built with the current recipe or when missing binary package
* :command:`--build=[pattern]` Conan will force the build of the packages, the name of which matches the given **pattern**.
  Several patterns can be specified, chaining multiple options, e.g. :command:`--build=pattern1 --build=pattern2`
* :command:`--build` Always build everything from source. Produces a clean re-build of all packages
  and transitively dependent packages


env variables
-------------

With the **-e** parameters you can define:

   - Global environment variables (``-e SOME_VAR="SOME_VALUE"``). These variables will be defined before the `build` step in all the packages and will be cleaned after the `build` execution.
   - Specific package environment variables (``-e zlib:SOME_VAR="SOME_VALUE"``). These variables will be defined only in the specified packages (e.g. zlib).

You can specify this variables not only for your direct ``requires`` but for any package in the dependency graph.

If you want to define an environment variable but you want to append the variables declared in your
requirements you can use the [] syntax:

.. code-block:: bash

    conan install -e PYTHONPATH=[/other/path]

This way the first entry in the PYTHONPATH variable will be `/other/path` but the PYTHONPATH values declared in the requirements
of the project will be appended at the end using the system path separator.


settings
--------

With the **-s** parameters you can define:

   - Global settings (-s compiler="Visual Studio"). Will apply to all the requires.
   - Specific package settings (-s zlib:compiler="MinGW"). Those settings will be applied only to the specified packages.

You can specify custom settings not only for your direct ``requires`` but for any package in the dependency graph.


options
-------

With the **-o** parameters you can only define specific package options (-o zlib:shared=True).


.. note::

   You can use :ref:`profiles <profiles>` files to create predefined sets of **settings**, **options**, **environment variables** and **scopes**
