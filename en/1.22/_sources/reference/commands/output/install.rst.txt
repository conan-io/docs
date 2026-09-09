
.. _install_json:


Install and Create output
-------------------------

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
        - **id**: Reference. E.g., "openssl/1.0.2u"
        - **name**: name of the packaged library. E.g., "openssl"
        - **version**: version of the packaged library. E.g., "1.0.2u"
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

    $ conan install openssl/1.0.2u@ --json install.json

.. code-block:: json
   :caption: install.json

    {
        "error": false,
        "installed": [{
            "recipe": {
                "id": "openssl/1.0.2u",
                "downloaded": true,
                "exported": false,
                "error": null,
                "remote": "https://conan.bintray.com",
                "time": "2020-01-30T19:19:21.217923",
                "dependency": true,
                "name": "openssl",
                "version": "1.0.2u",
                "user": null,
                "channel": null
            },
            "packages": [{
                "id": "f99afdbf2a1cc98ba2029817b35103455b6a9b77",
                "downloaded": true,
                "exported": false,
                "error": null,
                "remote": "https://conan.bintray.com",
                "time": "2020-01-30T19:19:27.662199",
                "built": false,
                "cpp_info": {
                    "name": "openssl",
                    "names": {
                        "cmake_find_package": "OpenSSL",
                        "cmake_find_package_multi": "OpenSSL"
                    },
                    "includedirs": ["include"],
                    "libdirs": ["lib"],
                    "resdirs": ["res"],
                    "bindirs": ["bin"],
                    "builddirs": [""],
                    "frameworkdirs": ["Frameworks"],
                    "libs": ["ssl", "crypto", "dl", "pthread"],
                    "rootpath": "/home/user/.conan/data/openssl/1.0.2u/_/_/package/f99afdbf2a1cc98ba2029817b35103455b6a9b77",
                    "version": "1.0.2u",
                    "description": "A toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols",
                    "filter_empty": true,
                    "public_deps": ["zlib"]
                }
            }]
        }, {
            "recipe": {
                "id": "zlib/1.2.11#1cd4a227e1b846f961bf91fcb6f3980f",
                "downloaded": false,
                "exported": false,
                "error": null,
                "remote": null,
                "time": "2020-01-30T19:19:21.237131",
                "dependency": true,
                "name": "zlib",
                "version": "1.2.11",
                "user": null,
                "channel": null
            },
            "packages": [{
                "id": "6af9cc7cb931c5ad942174fd7838eb655717c709",
                "downloaded": false,
                "exported": false,
                "error": null,
                "remote": null,
                "time": "2020-01-30T19:19:22.061885",
                "built": false,
                "cpp_info": {
                    "name": "ZLIB",
                    "includedirs": ["include"],
                    "libdirs": ["lib"],
                    "resdirs": ["res"],
                    "bindirs": ["bin"],
                    "builddirs": [""],
                    "frameworkdirs": ["Frameworks"],
                    "libs": ["z"],
                    "rootpath": "/home/user/.conan/data/zlib/1.2.11/_/_/package/6af9cc7cb931c5ad942174fd7838eb655717c709",
                    "version": "1.2.11",
                    "description": "A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)",
                    "filter_empty": true
                }
            }]
        }]
    }

.. note::

    As this is a marked as *experimental*, some fields may be removed or added: fields ``version`` and ``description`` inside ``cpp_info``
    will eventually be removed and paths may be changed for absolute ones.
