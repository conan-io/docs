
conan package
=============

.. code-block:: bash

    $ conan package [-h] [-sf SOURCE_FOLDER] [-bf BUILD_FOLDER]
                    [-pf PACKAGE_FOLDER] [-if INSTALL_FOLDER]
                    path

Calls your local conanfile.py 'package()' method. This command works locally,
in the user space, and it will copy artifacts from the --build-folder and
--source-folder folder to the --package-folder one. It won't create a new
package in the local cache, if you want to do it, use 'create' or use 'export-
pkg' after a 'build' command.

.. code-block:: bash

    positional arguments:
      path                  path to a folder containing a recipe (conanfile.py) or
                            to a recipe file, e.g., conan package
                            folder/conanfile.py

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
                            folder to install the package. Defaulted to the
                            '{build_folder}/package' folder. A relative path can
                            be specified (relative to the current directory). Also
                            an absolute path is allowed.
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Optional. Local folder containing the conaninfo.txt
                            and conanbuildinfo.txt files (from a previous conan
                            install execution). Defaulted to --build-folder

The ``package()`` method might use `settings`, `options` and `environment variables` from the specified
profile and dependencies information from the declared ``deps_XXX_info`` objects in the conanfile
requirements.

All that information is saved automatically in the *conaninfo.txt* and *conanbuildinfo.txt* files respectively, when you run
:command:`conan install`. Those files have to be located in the specified :command:`--build-folder`.

.. code-block:: bash

    $ conan install . --build-folder=build

**Examples**

This example shows how ``package()`` works in a package which can be edited and built in user folders instead of the local cache.

.. code-block:: bash

    $ conan new Hello/0.1 -s
    $ conan install . --install-folder=build_x86 -s arch=x86
    $ conan build . --build-folder=build_x86
    $ conan package . --build-folder=build_x86 --package-folder=package_x86
    $ ls package/x86
    > conaninfo.txt  conanmanifest.txt  include/  lib/

.. note::

    The packages created locally are just for the user, but cannot be directly consumed by other
    packages, nor they can be uploaded to a remote repository. In order to make these packages
    available to the system, they have to be put in the conan local cache, which can be done with
    the :command:`conan export-pkg` command instead of using :command:`conan package` command:

    .. code-block:: bash

        $ conan new Hello/0.1 -s
        $ conan install . --install-folder=build_x86 -s arch=x86
        $ conan build . --build-folder=build_x86
        $ conan export-pkg . Hello/0.1@user/stable --build-folder=build_x86 -s arch=x86
