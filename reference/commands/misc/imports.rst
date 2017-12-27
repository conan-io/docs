
conan imports
=============

.. code-block:: bash

    $ conan imports [-h] [--import-folder IMPORT_FOLDER]
                    [--install-folder INSTALL_FOLDER] [-u]
                    path

Calls your local conanfile.py or conanfile.txt 'imports' method. It requires
to have been previously installed and have a conanbuildinfo.txt generated file
in the --install-folder (defaulted to current directory).

.. code-block:: bash

    positional arguments:
      path                  path to a recipe (conanfile.py). e.g.,
                            ./my_project/With --undo option, this parameter is the
                            folder containing the conan_imports_manifest.txt file
                            generated in a previousexecution. e.j: conan imports
                            ./imported_files --undo

    optional arguments:
      -h, --help            show this help message and exit
      --import-folder IMPORT_FOLDER, --import_folder IMPORT_FOLDER, -imf IMPORT_FOLDER
                            Directory to copy the artifacts to. By default it will
                            be the current directory
      --install-folder INSTALL_FOLDER, --install_folder INSTALL_FOLDER, -if INSTALL_FOLDER
                           local folder containing the conaninfo.txt and
                            conanbuildinfo.txt files (from a previous conan
                            install execution)
      -u, --undo            Undo imports. Remove imported files

The ``imports()`` method might use `settings`, `options` and `environment variables` from the
specified profile and dependencies information from the declared ``deps_XXX_info`` objects in the
conanfile requirements.

All that information is saved automatically in the ``conaninfo.txt`` and ``conanbuildinfo.txt``
files respectively, when you run the ``conan install`` command. Those files have to be located in
the specified ``--install-folder``.

**Examples**

- Import files from a current conanfile in current directory:

  .. code-block:: bash

      $ conan install . --no-imports # Creates the conanbuildinfo.txt
      $ conan imports .

- Remove the copied files (undo the import):

  .. code-block:: bash

      $ conan imports . --undo
