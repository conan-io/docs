
.. _upload_json:


Upload output [EXPERIMENTAL]
----------------------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The :command:`conan upload` provides a ``--json`` parameter to generate a file containing the
information of the upload process.

The output JSON contains a two first level keys:

  - **error**: ``True`` if the upload completed without error, ``False`` otherwise.
  - **uploaded**: A list of uploaded packages. Each element contains:

     - **recipe**: Document representing the uploaded recipe.

        - **id**: Reference, e.g., "OpenSSL/1.0.2n@conan/stable"
        - **remote_name**: Remote name where the recipe was uploaded.
        - **remote_url**: Remote URL where the recipe was uploaded.
        - **time**: ``ISO 8601`` string with the time the recipe was uploaded.

     - **packages**: List of elements, representing the binary packages uploaded for the recipe.
        - **id**: Package ID, e.g., "8018a4df6e7d2b4630a814fa40c81b85b9182d2b"
        - **time**: ISO 8601 string with the time the recipe was uploaded.

**Example:**

.. code-block:: bash

    $ conan upload h* -all -r conan-center --json upload.json

.. code-block:: json
   :caption: upload.json

    {
        "error":false,
        "uploaded":[
            {
                "recipe":{
                    "id":"Hello/0.1@conan/testing",
                    "remote_name":"conan-center",
                    "remote_url":"https://conan.bintray.com",
                    "time":"2018-04-30T11:18:19.204728"
                },
                "packages":[
                    {
                        "id":"3f3387d49612e03a5306289405a2101383b861f0",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:21.534877"
                    },
                    {
                        "id":"6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:23.934152"
                    },
                    {
                        "id":"889d5d7812b4723bd3ef05693ffd190b1106ea43",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:28.195266"
                    },
                    {
                        "id":"e98aac15065fc710dffd1b4fbee382b087c3ad1d",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:30.495989"
                    }
                ]
            },
            {
                "recipe":{
                    "id":"Hello0/1.2.1@conan/testing",
                    "remote_name":"conan-center",
                    "remote_url":"https://conan.bintray.com",
                    "time":"2018-04-30T11:18:32.688651"
                },
                "packages":[
                    {
                        "id":"5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:34.991721"
                    }
                ]
            },
            {
                "recipe":{
                    "id":"HelloApp/0.1@conan/testing",
                    "remote_name":"conan-center",
                    "remote_url":"https://conan.bintray.com",
                    "time":"2018-04-30T11:18:36.901333"
                },
                "packages":[
                    {
                        "id":"6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:39.243895"
                    }
                ]
            },
            {
                "recipe":{
                    "id":"HelloPythonConan/0.1@conan/testing",
                    "remote_name":"conan-center",
                    "remote_url":"https://conan.bintray.com",
                    "time":"2018-04-30T11:18:41.181543"
                },
                "packages":[
                    {
                        "id":"5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:43.749422"
                    }
                ]
            },
            {
                "recipe":{
                    "id":"HelloPythonReuseConan/0.1@conan/testing",
                    "remote_name":"conan-center",
                    "remote_url":"https://conan.bintray.com",
                    "time":"2018-04-30T11:18:45.614096"
                },
                "packages":[
                    {
                        "id":"6a051b2648c89dbd1f8ada0031105b287deea9d2",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:47.942491"
                    }
                ]
            },
            {
                "recipe":{
                    "id":"hdf5/1.8.20@acri/testing",
                    "remote_name":"conan-center",
                    "remote_url":"https://conan.bintray.com",
                    "time":"2018-04-30T11:18:48.291756"
                },
                "packages":[

                ]
            },
            {
                "recipe":{
                    "id":"http_parser/2.8.0@conan/testing",
                    "remote_name":"conan-center",
                    "remote_url":"https://conan.bintray.com",
                    "time":"2018-04-30T11:18:48.637576"
                },
                "packages":[
                    {
                        "id":"6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7",
                        "remote_name":"conan-center",
                        "remote_url":"https://conan.bintray.com",
                        "time":"2018-04-30T11:18:51.125189"
                    }
                ]
            }
        ]
    }
