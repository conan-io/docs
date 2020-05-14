
conan source
============

.. code-block:: bash

    $ conan source [-h] [-sf SOURCE_FOLDER] [-if INSTALL_FOLDER] path

Calls your local conanfile.py 'source()' method. I.e., downloads and unzip the
package source.

.. code-block:: bash

    positional arguments:
      path                  path to a folder containing a recipe (conanfile.py) or
                            to a recipe file, e.g., conan package
                            folder/conanfile.py

    optional arguments:
      -h, --help            show this help message and exit
      -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                            Destination directory. Defaulted to current directory
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Optional. Local folder containing the conaninfo.txt
                            and conanbuildinfo.txt files (from a previous conan
                            install execution). Defaulted to the current
                            directory. Optional, source method will run without
                            the information retrieved from the conaninfo.txt and
                            conanbuildinfo.txt, only required when using
                            conditional source() based on settings, options,
                            env_info and user_info

The ``source()`` method might use (optional) `settings`, `options` and `environment variables` from
the specified profile and dependencies information from the declared ``deps_XXX_info`` objects in
the conanfile requirements.

All that information is saved automatically in the *conaninfo.txt* and *conanbuildinfo.txt* files respectively, when you run the
:command:`conan install` command. Those files have to be located in the specified :command:`--install-folder`.

**Examples**:

- Call a local recipe's source method: In user space, the command will execute a local *conanfile.py* ``source()`` method, in the *src*
  folder in the current directory.

  .. code-block:: bash

      $ conan new lib/1.0@conan/stable
      $ conan source . --source-folder mysrc

- In case you need the settings/options or any info from the requirements, perform first an install:

  .. code-block:: bash

      $ conan install . --install-folder mybuild
      $ conan source . --source-folder mysrc --install-folder mybuild
