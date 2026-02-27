
.. _install_json:


Install and Create output [EXPERIMENTAL]
----------------------------------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The :command:`conan install` and :command:`conan create` provide a ``--json`` parameter to generate
a file containing the information of the installation process.

The output JSON contains a two first level keys:

  - **error**: ``True`` if the install completed without error, ``False`` otherwise.
  - **installed**: A list of installed packages. Each element contains:

     - **recipe**: Document representing the downloaded recipe.

        - **remote**: remote URL if the recipe has been downloaded. ``null`` otherwise.
        - **cache**: ``true``/``false``. Retrieved from cache (not downloaded).
        - **downloaded**: ``true``/``false``. Downloaded from a remote (not in cache).
        - **time**: ``ISO 8601`` string with the time the recipe was downloaded/retrieved.
        - **error**: ``true``/``false``.
        - **id**: Reference. E.g., "OpenSSL/1.0.2n@conan/stable"
        - **name**: name of the packaged library. E.g., "OpenSSL"
        - **version**: version of the packaged library. E.g., "1.0.2n"
        - **user**: user of the packaged library. E.g., "conan"
        - **channel**: channel of the packaged library. E.g., "stable"
        - **dependency**: ``true``/``false``. Is the package being installed/created or a
          dependency. Same as :ref:`develop conanfile attribute<develop_attribute>`.

     - **packages**: List of elements, representing the binary packages downloaded for the recipe.
       Normally there will be only 1 element in this list, only in special cases with build
       requires, private dependencies and settings overridden this list could have more than one
       element.

        - **remote**: remote URL if the recipe has been downloaded. ``null`` otherwise.
        - **cache**: ``true``/``false``. Retrieved from cache (not downloaded).
        - **downloaded**: ``true``/``false``. Downloaded from a remote (not in cache).
        - **time**: ISO 8601 string with the time the recipe was downloaded/retrieved.
        - **error**: ``true``/``false``.
        - **id**: Package ID. E.g., "8018a4df6e7d2b4630a814fa40c81b85b9182d2b"
        - **cpp_info**: dictionary containing the build information defined in the ``package_info``
          method on the recipe.

**Example:**

.. code-block:: bash

    $ conan install OpenSSL/1.0.2l@conan/stable --json install.json

.. code-block:: json
   :caption: install.json

    {
        "error":false,
        "installed":[
            {
                "recipe":{
                    "id":"OpenSSL/1.0.2l@conan/stable",
                    "downloaded":true,
                    "exported":false,
                    "error":null,
                    "remote":"https://api.bintray.com/conan/conan/conan-center",
                    "time":"2018-11-29T11:59:53.601813",
                    "dependency":true,
                    "name":"OpenSSL",
                    "version":"1.0.2l",
                    "user":"conan",
                    "channel":"stable"
                },
                "packages":[
                    {
                        "id":"606fdb601e335c2001bdf31d478826b644747077",
                        "downloaded":true,
                        "exported":false,
                        "error":null,
                        "remote":"https://api.bintray.com/conan/conan/conan-center",
                        "time":"2018-11-29T12:00:03.874284",
                        "built":false,
                        "cpp_info":{
                            "includedirs":[
                                "include"
                            ],
                            "libdirs":[
                                "lib"
                            ],
                            "resdirs":[
                                "res"
                            ],
                            "bindirs":[
                                "bin"
                            ],
                            "builddirs":[
                                ""
                            ],
                            "libs":[
                                "ssleay32",
                                "libeay32",
                                "crypt32",
                                "msi",
                                "ws2_32"
                            ],
                            "rootpath":"C:/Users/user/.conan/data/OpenSSL/1.0.2l/conan/stable/package/606fdb601e335c2001bdf31d478826b644747077",
                            "version":"1.0.2l",
                            "description":"OpenSSL is an open source project that provides a robust, commercial-grade, and full-featured toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols",
                            "public_deps":[
                                "zlib"
                            ]
                        }
                    }
                ]
            },
            {"...":"..."
            }
        ]
    }

.. note::

    As this is a marked as *experimental*, some fields may be removed or added: fields ``version`` and ``description`` inside ``cpp_info``
    will eventually be removed and paths may be changed for absolute ones.
