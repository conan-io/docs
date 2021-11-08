conan list
==========

conan list recipes
------------------

.. code-block:: bash

    $ conan list recipes zlib -r=conancenter
    conancenter:
    zlib
        zlib/1.2.11
        zlib/1.2.8

    $ conan list recipes zlib/1.2.1* -r=conancenter
    conancenter:
    zlib
        zlib/1.2.11

    $ conan list recipes zlib/1.2.1* -r=conancenter --format=json
    [
        {
            "remote": "conancenter",
            "error": null,
            "results": [
                {
                    "name": "zlib",
                    "id": "zlib/1.2.11"
                }
            ]
        }
    ]

conan list package-ids
----------------------

.. code-block:: bash

    $ conan list package-ids zlib/1.2.11 -r=conancenter
    ...
    zlib/1.2.11:1513b3452ef7e2a2dd5f931247c5e02edeb98cc9
        settings:
        os=Macos
        arch=x86_64
        compiler=apple-clang
        build_type=Debug
        compiler.version=10.0
        options:
        shared=False
        fPIC=True
    zlib/1.2.11:963bb116781855de98dbb23aaac41621e5d312d8
        settings:
        os=Windows
        compiler.runtime=MTd
        arch=x86_64
        compiler=Visual Studio
        build_type=Debug
        compiler.version=15
        options:
        shared=False
    zlib/1.2.11:bf6871a88a66b609883bce5de4dd61adb1e033a7
        settings:
        os=Linux
        arch=x86_64
        compiler=gcc
        build_type=Debug
        compiler.version=5
        options:
        shared=True
    ...



conan list recipe-revisions
---------------------------

.. code-block:: bash

    $ conan list recipe-revisions zlib/1.2.11 -r=conancenter
    conancenter:
    ...
      zlib/1.2.11#b3eaf63da20a8606f3d84602c2cfa854 (2021-08-27T20:02:46Z)
      zlib/1.2.11#08c5163c8e302d1482d8fa2be93736af (2021-05-05T16:17:39Z)
      zlib/1.2.11#b291478a29f383b998e1633bee1c0536 (2021-03-25T10:03:21Z)
      zlib/1.2.11#514b772abf9c36ad9be48b84cfc6fdc2 (2021-02-19T14:33:26Z)


conan list package-revisions
----------------------------

.. code-block:: bash

    $conan list package-revisions zlib/1.2.11#b3eaf63da20a8606f3d84602c2cfa854:963bb116781855de98dbb23aaac41621e5d312d8 -r=conancenter
    conancenter:
      zlib/1.2.11#b3eaf63da20a8606f3d84602c2cfa854:963bb116781855de98dbb23aaac41621e5d312d8#dd44f4a86108e836f0c2d35af89cd8cd (2021-08-27T20:12:00Z)
