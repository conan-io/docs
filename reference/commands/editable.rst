.. _reference_commands_editable:

conan editable
==============

Allow working with a package that resides in user folder.


conan editable add
------------------

.. code-block:: bash

    $ conan editable add -h
    usage: conan editable add [-h] [-v [V]] [--logger] [--name NAME]
                              [--version VERSION] [--user USER]
                              [--channel CHANNEL] [-of OUTPUT_FOLDER]
                              path

    Define the given <path> location as the package <reference>, so when this
    package is required, it is used from this <path> location instead of the
    cache.

    positional arguments:
      path                  Path to the package folder in the user workspace

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.
      --name NAME           Provide a package name if not specified in conanfile
      --version VERSION     Provide a package version if not specified in
                            conanfile
      --user USER           Provide a user if not specified in conanfile
      --channel CHANNEL     Provide a channel if not specified in conanfile
      -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                            The root output folder for generated and build files

conan editable remove
---------------------

.. code-block:: bash

    $ conan editable remove -h
    usage: conan editable remove [-h] [-v [V]] [--logger] [-r REFS] [path]

    Remove the "editable" mode for this reference.

    positional arguments:
      path                  Path to a folder containing a recipe (conanfile.py or
                            conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.
      -r REFS, --refs REFS  Directly provide reference patterns
