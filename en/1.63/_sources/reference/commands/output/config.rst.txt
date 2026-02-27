
.. _config_json:


Config output
-------------

.. caution::

    We are actively working to finalize the *Conan 2.0 Release*. Some of the information on this page references
    **deprecated** features which will not be carried forward with the new release. It's important to check the 
    :ref:`Migration Guidelines<conan2_migration_guide>` to ensure you are using the most up to date features.

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
