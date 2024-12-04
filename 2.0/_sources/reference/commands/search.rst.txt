.. _reference_commands_search:

conan search
============

Search existing recipes in remotes.
This command is equivalent to ``conan list <query> -r=*``, and is provided for simpler UX.

.. autocommand::
    :command: conan search -h


.. code-block:: text

    $ conan search zlib
    conancenter
      zlib
        zlib/1.2.8
        zlib/1.2.11
        zlib/1.2.12
        zlib/1.2.13

    $ conan search zlib -r=conancenter
    conancenter
      zlib
        zlib/1.2.8
        zlib/1.2.11
        zlib/1.2.12
        zlib/1.2.13

    $ conan search zlib/1.2.1* -r=conancenter
    conancenter
      zlib
        zlib/1.2.11
        zlib/1.2.12
        zlib/1.2.13

    $ conan search zlib/1.2.1* -r=conancenter --format=json
    {
        "conancenter": {
            "zlib/1.2.11": {},
            "zlib/1.2.12": {},
            "zlib/1.2.13": {}
        }
    }
