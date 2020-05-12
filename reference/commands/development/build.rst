
.. _conan_build:

conan build
===========

.. code-block:: bash

    $ conan build [-h] [-b] [-bf BUILD_FOLDER] [-c] [-i] [-t]
                  [-if INSTALL_FOLDER] [-pf PACKAGE_FOLDER]
                  [-sf SOURCE_FOLDER]
                  path

Calls your local conanfile.py 'build()' method.

The recipe will be built in the local directory specified by
--build-folder, reading the sources from --source-folder. If you are
using a build helper, like CMake(), the --package-folder will be
configured as the destination folder for the install step.

.. code-block:: text

    positional arguments:
      path                  Path to a folder containing a conanfile.py or to a
                            recipe file e.g., my_folder/conanfile.py

    optional arguments:
      -h, --help            show this help message and exit
      -b, --build           Execute the build step (variable should_build=True).
                            When specified, configure/install/test won't run
                            unless --configure/--install/--test specified
      -bf BUILD_FOLDER, --build-folder BUILD_FOLDER
                            Directory for the build process. Defaulted to the
                            current directory. A relative path to the current
                            directory can also be specified
      -c, --configure       Execute the configuration step (variable
                            should_configure=True). When specified,
                            build/install/test won't run unless
                            --build/--install/--test specified
      -i, --install         Execute the install step (variable
                            should_install=True). When specified,
                            configure/build/test won't run unless
                            --configure/--build/--test specified
      -t, --test            Execute the test step (variable should_test=True).
                            When specified, configure/build/install won't run
                            unless --configure/--build/--install specified
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Directory containing the conaninfo.txt and
                            conanbuildinfo.txt files (from previous 'conan
                            install'). Defaulted to --build-folder
      -pf PACKAGE_FOLDER, --package-folder PACKAGE_FOLDER
                            Directory to install the package (when the build
                            system or build() method does it). Defaulted to the
                            '{build_folder}/package' folder. A relative path can
                            be specified, relative to the current folder. Also an
                            absolute path is allowed.
      -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                            Directory containing the sources. Defaulted to the
                            conanfile's directory. A relative path to the current
                            directory can also be specified


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
            self.run("git clone https://github.com/conan-io/hello.git")

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
    $ conan install . --install-folder install_x86 -s arch=x86
    $ conan build . --build-folder build_x86 --install-folder install_x86 --source-folder src

However, we recommend the ``conaninfo.txt`` and ``conanbuildinfo.txt`` to be generated in the same
--build-folder, otherwise, you will need to specify a different folder in your build system to include
the files generators file. E.g., ``conanbuildinfo.cmake``


**Example**: Control the build stages

You can control the build stages using :command:`--configure`/:command:`--build`/:command:`--install`/:command:`--test` arguments. Here is
an example using the CMake build helper:

.. code-block:: bash

    $ conan build . --configure # only run cmake.configure(). Other methods will do nothing
    $ conan build . --build     # only run cmake.build(). Other methods will do nothing
    $ conan build . --install   # only run cmake.install(). Other methods will do nothing
    $ conan build . --test      # only run cmake.test(). Other methods will do nothing
    # They can be combined
    $ conan build . -c -b # run cmake.configure() + cmake.build(), but not cmake.install() nor cmake.test

If nothing is specified, all the methods will be called.

.. seealso::

    Read more about :ref:`attribute_build_stages`.
