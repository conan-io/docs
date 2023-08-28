.. _reference_commands_editable:

conan editable
==============

Allow working with a package that resides in user folder.

conan editable add
------------------

..  code-block:: text

    $ conan editable add -h
    usage: conan editable add [-h] [-v [V]] [--name NAME] [--version VERSION]
                              [--user USER] [--channel CHANNEL]
                              [-of OUTPUT_FOLDER] [-r REMOTE | -nr]
                              path

    Define the given <path> location as the package <reference>, so when this
    package is required, it is used from this <path> location instead of the
    cache.

    positional arguments:
      path                  Path to the package folder in the user workspace

    options:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --name NAME           Provide a package name if not specified in conanfile
      --version VERSION     Provide a package version if not specified in
                            conanfile
      --user USER           Provide a user if not specified in conanfile
      --channel CHANNEL     Provide a channel if not specified in conanfile
      -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                            The root output folder for generated and build files
      -r REMOTE, --remote REMOTE
                            Look in the specified remote or remotes server
      -nr, --no-remote      Do not use remote, resolve exclusively in the cache

conan editable remove
---------------------

..  code-block:: text

    $ conan editable remove -h
    usage: conan editable remove [-h] [-v [V]] [-r REFS] [path]

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
      -r REFS, --refs REFS  Directly provide reference patterns


conan editable list
-------------------

..  code-block:: text

    $ conan editable list -h
    usage: conan editable list [-h] [-f FORMAT] [-v [V]]

    List all the packages in editable mode.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace


.. seealso::

    - Read the tutorial about editable packages :ref:`editable package<editable_packages>`.
