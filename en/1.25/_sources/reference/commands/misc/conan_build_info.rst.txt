
.. _conan_build_info:

conan_build_info v1
-------------------

.. code-block:: bash

    usage: conan_build_info [-h] [--output OUTPUT] trace_path

    Extracts build-info from a specified conan trace log and return a valid JSON

    positional arguments:
      trace_path       Path to the conan trace log file e.g.: /tmp/conan_trace.log

    optional arguments:
      -h, --help       show this help message and exit
      --output OUTPUT  Optional file to output the JSON contents, if not specified
                      the JSON will be printed to stdout


conan_build_info v2
-------------------

.. code-block:: bash

    $ conan_build_info --v2 [-h] {start,stop,create,update,publish} ...

.. code-block:: bash

    Generates build-info from lockfiles information

    positional arguments:
      {start,stop,create,update,publish}
                            sub-command help
        start               Command to incorporate to the artifacts.properties the
                            build name and number
        stop                Command to remove from the artifacts.properties the
                            build name and number
        create              Command to generate a build info json from a lockfile
        update              Command to update a build info json with another one
        publish             Command to publish the build info to Artifactory

    optional arguments:
      -h, --help            show this help message and exit

**start subcommand**:

.. code-block:: bash

    usage: conan_build_info --v2 start [-h] build_name build_number

    positional arguments:
      build_name    build name to assign
      build_number  build number to assign

    optional arguments:
      -h, --help    show this help message and exit

**stop subcommand**:

.. code-block:: bash

    usage: conan_build_info --v2 stop [-h]

    optional arguments:
      -h, --help  show this help message and exit

**create subcommand**:

.. code-block:: bash

    usage: conan_build_info --v2 create [-h] --lockfile LOCKFILE [--user [USER]]
                                        [--password [PASSWORD]] [--apikey [APIKEY]]
                                        build_info_file

    positional arguments:
      build_info_file       build info json for output

    optional arguments:
      -h, --help            show this help message and exit
      --lockfile LOCKFILE   input lockfile
      --user [USER]         user
      --password [PASSWORD]
                            password
      --apikey [APIKEY]     apikey

**publish subcommand**:

.. code-block:: bash

    usage: conan_build_info --v2 publish [-h] --url URL [--user [USER]]
                                         [--password [PASSWORD]] [--apikey [APIKEY]]
                                         buildinfo

    positional arguments:
      buildinfo             build info to upload

    optional arguments:
      -h, --help            show this help message and exit
      --url URL             url
      --user [USER]         user
      --password [PASSWORD]
                            password
      --apikey [APIKEY]     apikey


**update subcommand**:

.. code-block:: bash

    usage: conan_build_info --v2 update [-h] [--output-file OUTPUT_FILE]
                                        buildinfo [buildinfo ...]

    positional arguments:
      buildinfo             buildinfo files to merge

    optional arguments:
      -h, --help            show this help message and exit
      --output-file OUTPUT_FILE
                            path to generated build info file

