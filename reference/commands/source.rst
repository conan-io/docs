.. _reference_commands_source:

conan source
============

.. code-block:: text

    $ conan source -h
    usage: conan source [-h] [-v [V]] [--name NAME] [--version VERSION]
                        [--user USER] [--channel CHANNEL]
                        [path]

    Call the source() method.

    positional arguments:
      path               Path to a folder containing a recipe (conanfile.py or
                         conanfile.txt) or to a recipe file. e.g.,
                         ./my_project/conanfile.txt.

    optional arguments:
      -h, --help         show this help message and exit
      -v [V]             Level of detail of the output. Valid options from less
                         verbose to more verbose: -vquiet, -verror, -vwarning,
                         -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv
                         or -vtrace
      --name NAME        Provide a package name if not specified in conanfile
      --version VERSION  Provide a package version if not specified in conanfile
      --user USER        Provide a user if not specified in conanfile
      --channel CHANNEL  Provide a channel if not specified in conanfile

.. seealso::

    - Read the tutorial about the :ref:`local package development flow <local_package_development_flow>`.
