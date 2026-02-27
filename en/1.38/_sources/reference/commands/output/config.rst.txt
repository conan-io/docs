
.. _config_json:


Config output
-------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The :command:`conan config home` provides a ``--json`` parameter to generate
a file containing the information of the conan home directory.

..  code-block:: bash

    $ conan config home --json home.json

It will create a JSON file like:

..  code-block:: json
    :caption: home.json

    {
        "home": "/path/to/conan/home"
    }
