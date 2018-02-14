conan help
==========

.. code-block:: bash

    $ usage: conan help [-h] [command]

Show help of a specific commmand.

.. code-block:: bash

    positional arguments:
    command     command

    optional arguments:
    -h, --help  show this help message and exit


This command is equivalent to the ``--help`` and ``-h`` arguments

**Example**:

.. code-block:: bash

    $ conan help get
    > usage: conan get [-h] [-p PACKAGE] [-r REMOTE] [-raw] reference [path]
    > Gets a file or list a directory of a given reference or package.

    # same as
    $ conan get -h
