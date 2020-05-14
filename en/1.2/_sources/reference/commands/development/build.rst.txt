
conan build
===========

.. code-block:: bash

    $ conan build [-h] [-sf SOURCE_FOLDER] [-bf BUILD_FOLDER]
                  [-pf PACKAGE_FOLDER] [-if INSTALL_FOLDER] [-c] [-b] [-i]
                  path

Calls your local conanfile.py 'build()' method. The recipe will be built in
the local directory specified by --build-folder, reading the sources from
--source-folder. If you are using a build helper, like CMake(), the
--package-folder will be configured as destination folder for the install
step.

.. code-block:: text

    positional arguments:
      path                  path to a recipe (conanfile.py), e.g., conan build .

    optional arguments:
      -h, --help            show this help message and exit
      -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                            local folder containing the sources. Defaulted to the
                            directory of the conanfile. A relative path can also
                            be specified (relative to the current directory)
      -bf BUILD_FOLDER, --build-folder BUILD_FOLDER
                            build folder, working directory of the build process.
                            Defaulted to the current directory. A relative path
                            can also be specified (relative to the current
                            directory)
      -pf PACKAGE_FOLDER, --package-folder PACKAGE_FOLDER
                            folder to install the package (when the build system
                            or build() method does it). Defaulted to the
                            '{build_folder}/package' folder. A relative path can
                            be specified, relative to the current folder. Also an
                            absolute path is allowed.
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Optional. Local folder containing the conaninfo.txt
                            and conanbuildinfo.txt files (from a previous conan
                            install execution). Defaulted to --build-folder
      -c, --configure       Execute the configuration step (variable
                            should_configure=True). When specified, build/install
                            won't run unless --build/--install specified
      -b, --build           Execute the build step (variable should_build=True).
                            When specified, configure/install won't run unless
                            --configure/--install specified
      -i, --install         Execute the install step (variable
                            should_install=True). When specified, configure/build
                            won't run unless --configure/--build specified

The ``build()`` method might use `settings`, `options` and `environment variables` from the specified profile and dependencies information
from the declared ``deps_XXX_info`` objects in the conanfile requirements. All that information is saved automatically in the
*conaninfo.txt* and *conanbuildinfo.txt* files respectively, when you run the :command:`conan install` command. Those files have to be located
in the specified :command:`--build-folder` or in the :command:`--install-folder` if specified.


The :command:`--configure, --build, --install` arguments control which parts of the ``build()`` are actually executed.
They have related conanfile boolean variables ``should_configure, should_build, should_install``, which are ``True``
by default, but that will change if some of these arguments are used in the command line. The ``CMake`` and
``Meson`` and ``AutotoolsBuildEnvironment`` helpers already use these variables.



**Example**: Building a conan package (for architecture x86) in a local directory.

.. code-block:: python
   :caption: conanfile.py

    from conans import ConanFile, CMake, tools

    class LibConan(ConanFile):
        ...

        def source(self):
            self.run("git clone https://github.com/memsharded/hello.git")

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_folder="hello")
            cmake.build()

First we will call :command:`conan source` to get our source code in the *src* directory, then :command:`conan install` to install the requirements
and generate the info files, and finally :command:`conan build` to build the package:

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
--build-folder, otherwise, you will need to specify a different folder in your build system to include
the files generators file. e.j ``conanbuildinfo.cmake``


**Example**: Control the build stages

Given a conanfile with this ``build()`` method:

.. code-block:: python

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

If nothing is specified, all three methods will be called. But using command line arguments, this can be changed:


.. code-block:: bash

    $ conan build . -c # only run cmake.configure(). Other methods will do nothing
    $ conan build . -b # only run cmake.build(). Other methods will do nothing
    $ conan build . -i # only run cmake.install(). Other methods will do nothing
    # They can be combined
    $ conan build . -c -b # run cmake.configure() + cmake.build(), but not cmake.install()


Autotools and Meson helpers already implement the same functionality. For other build systems, you can use
the following variables in the ``build()`` method:

.. code-block:: python

    def build(self):
        if self.should_configure:
            # Run my configure stage
        if self.should_build:
            # Run my build stage
        if self.should_install: # If my build has install, otherwise use package()
            # Run my install stage


Note these ``should_configure, should_build, should_install`` variables will always be ``True`` while
building in the local cache. They can only be modified for the local flow with :command:`conan build`.
