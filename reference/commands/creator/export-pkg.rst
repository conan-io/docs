.. _conan_export_pkg_command:

conan export-pkg
================

.. code-block:: bash

	$  conan export-pkg . [-h] [--source-folder SOURCE_FOLDER]
                          [--build-folder BUILD_FOLDER] [--profile PROFILE]
                          [--options OPTIONS] [--settings SETTINGS]
                          [--env ENV] [-f] [--no-export]
                          path reference


Exports a recipe & creates a package with given files calling 'package'. It
executes the package() method applied to the local folders '--source_folder'
and '--build_folder' and creates a new package in the local cache for the
specified 'reference' and for the specified '--settings', '--options' and or '
--profile'.


.. code-block:: bash

    positional arguments:
      path                  path to a recipe (conanfile.py). e.j: "."
      reference             user/channel, or a full package reference
                            (Pkg/version@user/channel), if name and version are
                            not declared in the recipe (conanfile.py)

    optional arguments:
      -h, --help            show this help message and exit
      --source-folder SOURCE_FOLDER, --source_folder SOURCE_FOLDER, -sf SOURCE_FOLDER
                            local folder containing the sources. Defaulted to
                            --build-folder. A relative path to the current dir can
                            also be specified
      --build-folder BUILD_FOLDER, --build_folder BUILD_FOLDER, -bf BUILD_FOLDER
                            build folder, working directory of the build process.
                            Defaulted to the current directory. A relative path
                            can also be specified (relative to the current
                            directory)
      --profile PROFILE, -pr PROFILE
                            Profile for this package
      --options OPTIONS, -o OPTIONS
                            Options for this package. e.g., -o with_qt=true
      --settings SETTINGS, -s SETTINGS
                            Settings for this package e.g., -s compiler=gcc
      --env ENV, -e ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      -f, --force           Overwrite existing package if existing
      --no-export, -ne      Do not export the recipe



Note that this is **not** the normal or recommended flow for creating conan packages,
as packages created this way will not have a reproducible build from sources.
This command should be used when:

 - It is not possible to build the packages from sources (only pre-built binaries available).
 - You are developing your package locally and want to export the built artifacts to the local cache.

The command ``conan new <ref> --bare`` will create a simple recipe that could be used in combination
with the ``export-pkg`` command. Check this :ref:`How to package existing binaries <existing_binaries>`.

This command will use the ``package()`` method.


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
    $ conan export-pkg . Hello/0.1@user/stable -s os=Windows -s arch=x86 -s build_type=Release --build_folder=Release_x86


- Create a package from a user folder build and sources folders:

Given this files in the current folder

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

    $ conan export-pkg . Hello/0.1@user/stable -pr=myprofile --source_folder=sources --build_folder=build

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
            self.run("git clone https://github.com/memsharded/hello.git")

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_dir="%s/hello" % self.source_folder)
            cmake.build()

        def package(self):
            self.copy("*.h", dst="include", src="include")
            self.copy("*.lib", dst="lib", keep_path=False)


First we will call ``conan source`` to get our source code in the ``src`` directory,
then ``conan install`` to install the requirements and generate the info files,
``conan build`` to build the package, and finally ``conan export-pkg`` to send the binary
files to a package in the local cache:


.. code-block:: bash
   :emphasize-lines: 3


    $ conan source . --source-folder src
    $ conan install --build-folder build_x86 -s arch=x86
    $ conan build . --build-folder build_x86 --source-folder src
    $ conan export-pkg . Hello/0.1@user/stable --build-folder build_x86 -s arch=x86
