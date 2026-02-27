
.. _conan_imports:

conan imports
=============

.. code-block:: bash

    $ conan imports [-h] [-if INSTALL_FOLDER] [-imf IMPORT_FOLDER] [-u] path

Calls your local conanfile.py or conanfile.txt 'imports' method.

It requires to have been previously installed and have a
conanbuildinfo.txt generated file in the --install-folder (defaulted to
the current directory).

.. code-block:: text

    positional arguments:
      path                  Path to a folder containing a conanfile.py or to a
                            recipe file e.g., my_folder/conanfile.py With --undo
                            option, this parameter is the folder containing the
                            conan_imports_manifest.txt file generated in a
                            previous execution. e.g.: conan imports
                            ./imported_files --undo

    optional arguments:
      -h, --help            show this help message and exit
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Directory containing the conaninfo.txt and
                            conanbuildinfo.txt files (from previous 'conan
                            install'). Defaulted to --build-folder
      -imf IMPORT_FOLDER, --import-folder IMPORT_FOLDER
                            Directory to copy the artifacts to. By default it will
                            be the current directory
      -u, --undo            Undo imports. Remove imported files


The ``imports()`` method might use `settings`, `options` and `environment variables` from the
specified profile and dependencies information from the declared ``deps_XXX_info`` objects in the
conanfile requirements.

All that information is saved automatically in the *conaninfo.txt* and *conanbuildinfo.txt* files respectively, when you run
:command:`conan install`. Those files have to be located in the specified :command:`--install-folder`.

**Examples**

- Import files from a current conanfile in current directory:

  .. code-block:: bash

      $ conan install . --no-imports # Creates the conanbuildinfo.txt
      $ conan imports .

- Remove the copied files (undo the import):

  .. code-block:: bash

      $ conan imports . --undo
