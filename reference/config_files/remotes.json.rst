.. _remotes.json:

remotes.json
============

.. note::

    *remotes.json* was introduced in Conan 1.15 and it substitutes, together with the *metadata.json* file in
    each package folder, the *registry.json* and *registry.txt* files.


This file is managed automatically by Conan and the :command:`conan remote` commands. It stores information about
the remotes: name, URL and different configuration arguments.


Example of *registry.json* file:

.. code-block:: json

    {
        "remotes": [
        {
        "name": "conan-center",
        "url": "https://conan.bintray.com",
        "verify_ssl": true
        },
        {
        "name": "artifactory-local",
        "url": "http://localhost:8081/artifactory/api/conan/conan-local",
        "verify_ssl": true,
        "disabled": true
        }
        ]
    }

.. warning::

    This file and its contents are implementation details of Conan client. It can change at any time
    without further notice, use the :ref:`conan_remote` command to access and modify its contents.
