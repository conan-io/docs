
conan build
===========


.. code-block:: bash

	$ conan build [-h] [--file FILE] [--source-folder SOURCE_FOLDER]
                  [--build-folder BUILD_FOLDER]
                  [--package-folder PACKAGE_FOLDER]
                  path


Calls your local conanfile.py 'build()' method. The recipe will be built in
the local directory specified by ``--build_folder``, reading the sources from
``--source_folder``. If you are using a build helper, like CMake(), the
``--package_folder`` will be configured as destination folder for the install
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
                            be specified (relative to the build_folder directory).
                            Also an absolute path is allowed.



The ``build()`` method might use `settings`, `options` and `environment variables` from the specified
profile, and dependencies information from the declared ``deps_XXX_info`` objects in the dependencies.
All that information is saved in the automatically in the ``conaninfo.txt`` and
``conanbuildinfo.txt`` files respectively, when you run the ``conan install`` command.
Those files have to be located in the specified ``--build_folder``.


**Example**:

.. code-block:: python

    from conans import ConanFile, CMake, tools


    class LibConan(ConanFile):
        ...

        def source(self):
            self.run("git clone https://github.com/memsharded/hello.git")

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_dir="%s/hello" % self.source_folder)
            cmake.build()



.. code-block:: bash
   :emphasize-lines: 4

    $ mkdir build_x86
    $ conan source . --source-folder src
    $ conan install --build-folder build_x86 -s arch=x86
    $ conan build . --build-folder build_x86 --source-folder src