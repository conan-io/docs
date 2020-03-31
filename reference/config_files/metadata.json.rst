.. _metadata.json:

metadata.json
=============

Associated to every package in the Conan cache there is a file *metadata.json*
that stores information about it. The most important data in this file are the
revision and the name of the remote associated with the recipe and with each one
of the binary packages available.

Example of *metadata.json* file:

.. code-block:: json

    {
        "recipe":{
            "revision":"0",
            "remote":"conan-center",
            "properties":{

            },
            "checksums":{
                "conanmanifest.txt":{
                    "md5":"37ccd88d926130c4a2cb146a6ecac952",
                    "sha1":"e9ef25288a533f2315b73ac9cc4fe3fd24d83f4f"
                },
                "conanfile.py":{
                    "md5":"a67fdbd93473a0bed19434b7c50652c7",
                    "sha1":"9b9f7b89b70e5fe3a82d9bed02035db7cdad5b9b"
                },
                "conan_export.tgz":{
                    "md5":"27bc544e0e1fda673c6e2cbd3f13fbaf",
                    "sha1":"c70f8d6562ded8061a435d74856c1b01ca18f894"
                }
            }
        },
        "packages":{
            "69168f775732984eb37d785004b6ef25111fe5f9":{
                "revision":"0",
                "recipe_revision":"0",
                "remote":"conan-center",
                "properties":{

                },
                "checksums":{
                    "conanmanifest.txt":{
                    "md5":"57eb53fb37dd4c43c9dd6483d9e8fa91",
                    "sha1":"8e2ee2416364d3333c545285e5335b1118ff6c47"
                    },
                    "conaninfo.txt":{
                    "md5":"4515abe8d19cbb06f81742165ac06c33",
                    "sha1":"530faead46c1a4549a549c2e32881c5c6773173a"
                    },
                    "conan_package.tgz":{
                    "md5":"8343e258a697efa5617e134c147d9094",
                    "sha1":"436eb5ec4b440149d8fad9b1a3d0b42df2a8886e"
                    }
                }
            }
        }
    }


.. warning::

    This file and its contents are implementation details of Conan client. It can change at any time
    without further notice.


