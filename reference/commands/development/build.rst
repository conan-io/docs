
conan build
===========

.. code-block:: bash

    $ conan build [-h] [--file FILE] [--source-folder SOURCE_FOLDER]
                  [--build-folder BUILD_FOLDER]
                  [--package-folder PACKAGE_FOLDER]
                  [--install-folder INSTALL_FOLDER]
                  path

Calls your local conanfile.py 'build()' method. The recipe will be built in
the local directory specified by --build_folder, reading the sources from
--source_folder. If you are using a build helper, like CMake(), the
--package_folder will be configured as destination folder for the install
step.

.. code-block:: bash

    positional arguments:
      path                  path to a recipe (conanfile.py), e.g., conan build .

    optional arguments:
      -h, --help            show this help message and exit
      --file FILE, -f FILE  specify conanfile filename
      --source-folder SOURCE_FOLDER, --source_folder SOURCE_FOLDER, -sf SOURCE_FOLDER
                            local folder containing the sources. Defaulted to the
                            directory of the conanfile. A relative path can also
                            be specified (relative to the current directory)
      --build-folder BUILD_FOLDER, --build_folder BUILD_FOLDER, -bf BUILD_FOLDER
                            build folder, working directory of the build process.
                            Defaulted to the current directory. A relative path
                            can also be specified (relative to the current
                            directory)
      --package-folder PACKAGE_FOLDER, --package_folder PACKAGE_FOLDER, -pf PACKAGE_FOLDER
                            folder to install the package (when the build system
                            or build() method does it). Defaulted to the
                            '{build_folder}/package' folder. A relative path can
                            be specified, relative to the current folder. Also an
                            absolute path is allowed.
      --install-folder INSTALL_FOLDER, --install_folder INSTALL_FOLDER, -if INSTALL_FOLDER
                            Optional. Local folder containing the conaninfo.txt
                            and conanbuildinfo.txt files (from a previous conan
                            install execution). Defaulted to --build-folder

The ``build()`` method might use `settings`, `options` and `environment variables` from the specified
profile and dependencies information from the declared ``deps_XXX_info`` objects in the conanfile
requirements.
All that information is saved automatically in the ``conaninfo.txt`` and ``conanbuildinfo.txt``
files respectively, when you run the ``conan install`` command.
Those files have to be located in the specified ``--build-folder`` or in the ``--install-folder`` if
specified.

**Example**: Building a conan package (for architecture x86) in a local directory.

**conanfile.py**

.. code-block:: python

    from conans import ConanFile, CMake, tools

    class LibConan(ConanFile):
        ...

        def source(self):
            self.run("git clone https://github.com/memsharded/hello.git")

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_folder="hello")
            cmake.build()

First we will call ``conan source`` to get our source code in the ``src`` directory,
then ``conan install`` to install the requirements and generate the info files,
and finally ``conan build`` to build the package:

.. code-block:: bash
   :emphasize-lines: 3

    $ conan source . --source-folder src
    $ conan install . --install-folder build_x86 -s arch=x86
    $ conan build . --build-folder build_x86 --source-folder src

Or if we want to create the ``conaninfo.txt`` and ``conanbuildinfo.txt`` files in a different folder:

.. code-block:: bash
   :emphasize-lines: 3

    $ conan source . --source-folder src
    $ conan install --install-folder install_x86 -s arch=x86
    $ conan build . --build-folder build_x86 --install-folder install_x86 --source-folder src

However, we recommend the ``conaninfo.txt`` and ``conanbuildinfo.txt`` to be generated in the same
--build_folder, otherwise, you will need to specify a different folder in your build system to include
the files generators file. e.j ``conanbuildinfo.cmake``
