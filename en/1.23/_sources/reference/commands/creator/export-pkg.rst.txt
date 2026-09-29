
.. _conan_export-pkg:

conan export-pkg
================

.. code-block:: bash

    $ conan export-pkg [-h] [-bf BUILD_FOLDER] [-e ENV] [-f]
                       [-if INSTALL_FOLDER] [-o OPTIONS] [-pr PROFILE]
                       [-pf PACKAGE_FOLDER] [-s SETTINGS] [-sf SOURCE_FOLDER]
                       [-j JSON] [-l [LOCKFILE]] [--ignore-dirty]
                       path [reference]

Exports a recipe, then creates a package from local source and build folders.

If '--package-folder' is provided it will copy the files from there, otherwise it
will execute package() method over '--source-folder' and '--build-folder' to create
the binary package.

.. code-block:: text

    positional arguments:
      path                  Path to a folder containing a conanfile.py or to a
                            recipe file e.g., my_folder/conanfile.py
      reference             user/channel or pkg/version@user/channel (if name and
                            version are not declared in the conanfile.py)

    optional arguments:
      -h, --help            show this help message and exit
      -bf BUILD_FOLDER, --build-folder BUILD_FOLDER
                            Directory for the build process. Defaulted to the
                            current directory. A relative path to current
                            directory can also be specified
      -e ENV, --env ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      -f, --force           Overwrite existing package if existing
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Directory containing the conaninfo.txt and
                            conanbuildinfo.txt files (from previous 'conan
                            install'). Defaulted to --build-folder If these files
                            are found in the specified folder and any of '-e',
                            '-o', '-pr' or '-s' arguments are used, it will raise
                            an error.
      -o OPTIONS, --options OPTIONS
                            Define options values, e.g., -o pkg:with_qt=True
      -pr PROFILE, --profile PROFILE
                            Profile for this package
      -pf PACKAGE_FOLDER, --package-folder PACKAGE_FOLDER
                            folder containing a locally created package. If a
                            value is given, it won't call the recipe 'package()'
                            method, and will run a copy of the provided folder.
      -s SETTINGS, --settings SETTINGS
                            Define settings values, e.g., -s compiler=gcc
      -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                            Directory containing the sources. Defaulted to the
                            conanfile's directory. A relative path to current
                            directory can also be specified
      -j JSON, --json JSON  Path to a json file where the install information will
                            be written
      -l [LOCKFILE], --lockfile [LOCKFILE]
                            Path to a lockfile or folder containing 'conan.lock'
                            file. Lockfile will be updated with the exported
                            package
      --ignore-dirty        When using the "scm" feature with "auto" values,
                            capture the revision and url even if there are
                            uncommitted changes


The :command:`export-pkg` command let you create a package from already existing files
in your working folder, it can be useful if you are using a build process external to Conan
and do not want to provide it with the recipe. Nevertheless, you should take into
account that it will generate a package and Conan won't be able to guarantee its
reproducibility or regenerate it again. This is **not** the normal or recommended flow
for creating Conan packages.

Execution of this command will result in several files copied to the package
folder in the cache identified by its ``package_id`` (Conan will perform all the
required actions to compute this _id_: build the graph, evaluate the requirements and
options, and call any required method), but there could be two
different sources for the files:

 * If the argument ``--package-folder`` is provided, Conan will just copy all the
   contents of that folder to the package one in the cache.
 * If no ``--package-folder`` is given, Conan will execute the method ``package()`` once
   and the ``self.copy(...)`` functions will copy matching files from the ``source_folder``
   **and** ``build_folder`` to the corresponding path in the Conan cache (working directory
   corresponds to the ``build_folder``).


There are different scenarios where this command could look like useful:

 - You are :ref:`working locally on a package<package_dev_flow>` and you want to
   upload it to the cache to be able to consume it from other recipes. In this situation
   you can use the :command:`export-pkg` command to copy the package to the cache,
   but you could also put the :ref:`package in editable mode<editable_packages>` and
   avoid this extra step.

 - You only have precompiled binaries available, then you can use the :command:`export-pkg`
   to create the Conan package, or you can build a working recipe to download and
   package them. These scenarios are described in the documentation section
   :ref:`How to package existing binaries <existing_binaries>`.


.. note::

    Note that if :command:`--profile`, settings or options are not provided to :command:`export-pkg`,
    the configuration will be extracted from the information stored after a previous :command:`conan install`.
    That information might be incomplete in some edge cases, so we strongly recommend the usage of
    :command:`--profile` or :command:`--settings, --options`, etc.


**Examples**

- Create a package from a directory containing the binaries for Windows/x86/Release:

  We need to collect all the files from the local filesystem and tell Conan to
  compute the proper ``package_id`` so its get associated with the correct
  settings and it works when consuming it.

  If the files in the working folder are:

  .. code-block:: text

      Release_x86/lib/libmycoollib.a
      Release_x86/lib/other.a
      Release_x86/include/mylib.h
      Release_x86/include/other.h

  then, just run:

  .. code-block:: bash

      $ conan new Hello/0.1 --bare  # It creates a minimum recipe example
      $ conan export-pkg . Hello/0.1@user/stable -s os=Windows -s arch=x86 -s build_type=Release --package-folder=Release_x86

  This last command will copy all the contents from the ``package-folder`` and
  create the package associated with the settings provided through the command
  line.

- Create a package from a source and build folder:

  The objective is to collect the files that will be part of the package from
  the source folder (*include files*) and from the build folder (libraries), so,
  if these are the files in the working folder:

  .. code-block:: text

      sources/include/mylib.h
      sources/src/file.cpp
      build/lib/mylib.lib
      build/lib/mylib.tmp
      build/file.obj

  we would need a slightly more complicated *conanfile.py* than in the previous
  example to select which files to copy, we need to change the patterns in the
  ``package()`` method:

  .. code-block:: python

      def package(self):
         self.copy("*.h", dst="include", src="include")
         self.copy("*.lib", dst="lib", keep_path=False)

  Now, we can run Conan to create the package:

  .. code-block:: bash

      $ conan export-pkg . Hello/0.1@user/stable -pr=myprofile --source-folder=sources --build-folder=build
