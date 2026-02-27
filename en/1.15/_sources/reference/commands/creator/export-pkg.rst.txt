
.. _conan_export-pkg:

conan export-pkg
================

.. code-block:: bash

    $ conan export-pkg [-h] [-bf BUILD_FOLDER] [-e ENV] [-f]
                       [-if INSTALL_FOLDER] [-o OPTIONS] [-pr PROFILE]
                       [-pf PACKAGE_FOLDER] [-s SETTINGS] [-sf SOURCE_FOLDER]
                       [-j JSON]
                       path reference

Exports a recipe, then creates a package from local source and build folders.
The package is created by calling the package() method applied to the local
folders '--source-folder' and '--build-folder' It's created in the local cache
for the specified 'reference' and for the specified '--settings', '--options'
and or '--profile'.

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
                            Define options values, e.g., -o pkg:with_qt=true
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


:command:`conan export-pkg` executes the following methods of a *conanfile.py* whenever ``--package-folder`` is used:

1. ``config_options()``
2. ``configure()``
3. ``requirements()``
4. ``package_id()``

In case a package folder is not specified, this command will also execute:

5. ``package()``

Note that this is **not** the normal or recommended flow for creating Conan packages,
as packages created this way will not have a reproducible build from sources.
This command should be used when:

 - It is not possible to build the packages from sources (only pre-built binaries available).
 - You are developing your package locally and want to export the built artifacts to the local
   cache.

The command :command:`conan new <ref> --bare` will create a simple recipe that could be used in combination
with the ``export-pkg`` command. Check this :ref:`How to package existing binaries
<existing_binaries>`.

:command:`export-pkg` has two different modes of operation:

- Specifying :command:`--package-folder` will perform a copy of the given folder, without executing the ``package()`` method.
  Use it if you have already created the package, for example with :command:`conan package` or
  with ``cmake.install()`` from the ``build()`` step.
- Specifying :command:`--build-folder` and/or :command:`--source-folder` will execute the ``package()`` method,
  to filter, select and arrange the layout of the artifacts.

**Examples**:

- Create a package from a directory containing the binaries for Windows/x86/Release:

  Having these files:

  .. code-block:: text

      Release_x86/lib/libmycoollib.a
      Release_x86/lib/other.a
      Release_x86/include/mylib.h
      Release_x86/include/other.h

  Run:

  .. code-block:: bash

      $ conan new Hello/0.1 --bare  # In case you still don't have a recipe for the binaries
      $ conan export-pkg . Hello/0.1@user/stable -s os=Windows -s arch=x86 -s build_type=Release --build-folder=Release_x86

- Create a package from a user folder build and sources folders:

  Given these files in the current folder

  .. code-block:: text

      sources/include/mylib.h
      sources/src/file.cpp
      build/lib/mylib.lib
      build/lib/mylib.tmp
      build/file.obj

  And assuming the ``Hello/0.1@user/stable`` recipe has a ``package()`` method like this:

  .. code-block:: python

      def package(self):
          self.copy("*.h", dst="include", src="include")
          self.copy("*.lib", dst="lib", keep_path=False)

  Then, the following code will create a package in the conan local cache:

  .. code-block:: bash

      $ conan export-pkg . Hello/0.1@user/stable -pr=myprofile --source-folder=sources --build-folder=build

  And such package will contain just the files:

  .. code-block:: text

      include/mylib.h
      lib/mylib.lib

- Building a conan package (for architecture x86) in a local directory and then send it to the local cache:

  **conanfile.py**

  .. code-block:: python

      from conans import ConanFile, CMake, tools

      class LibConan(ConanFile):
          name = "Hello"
          version = "0.1"
          ...

          def source(self):
              self.run("git clone https://github.com/conan-io/hello.git")

          def build(self):
              cmake = CMake(self)
              cmake.configure(source_folder="hello")
              cmake.build()

          def package(self):
              self.copy("*.h", dst="include", src="include")
              self.copy("*.lib", dst="lib", keep_path=False)

  First we will call :command:`conan source` to get our source code in the *src* directory, then
  :command:`conan install` to install the requirements and generate the info files, :command:`conan build` to
  build the package, and finally :command:`conan export-pkg` to send the binary files to a package in the
  local cache:

  .. code-block:: bash
      :emphasize-lines: 4

      $ conan source . --source-folder src
      $ conan install . --install-folder build_x86 -s arch=x86
      $ conan build . --build-folder build_x86 --source-folder src
      $ conan export-pkg . Hello/0.1@user/stable --build-folder build_x86 -s arch=x86


.. note::

    Note that if :command:`--profile` or settings, options, are not provided to :command:`export-pkg`,
    the configuration will be extracted from the information from a previous :command:`conan install`.
    That information might be incomplete in some edge cases, so we strongly recommend the usage of
    :command:`--profile` or :command:`--settings, --options`, etc.
