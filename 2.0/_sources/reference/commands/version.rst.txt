.. _reference_commands_version:

conan version
=============

.. include:: ../../common/experimental_warning.inc

.. autocommand::
    :command: conan version -h


The :command:`conan version` command shows the conan version as well the python version from the system:

.. code-block:: text

    $ conan version
    version: 2.0.6
    python
      version: 3.10.4
      sys_version: 3.10.4 (main, May 17 2022, 10:53:07) [Clang 13.1.6 (clang-1316.0.21.2.3)]


The :command:`conan version --format=json` returns a JSON output format in ``stdout`` (which can be redirected to a file) with the following structure:

.. code-block:: text

    $ conan version --format=json
    {
        "version": "2.0.6",
        "python": {
            "version": "3.10.4",
            "sys_version": "3.10.4 (main, May 17 2022, 10:53:07) [Clang 13.1.6 (clang-1316.0.21.2.3)]"
        }
    }
