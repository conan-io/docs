How the ``package_id`` is computed
==================================

Let's take some package and list its binaries, for example:

.. code-block:: bash
    :emphasize-lines: 8,19

    $ conan list zlib/1.2.13:* -r=conancenter

    zlib
      zlib/1.2.13
        revisions
          97d5730b529b4224045fe7090592d4c1 (2023-08-22 02:51:57 UTC)
            packages
              d62dff20d86436b9c58ddc0162499d197be9de1e  # package_id
                info
                  settings
                    arch: x86_64
                    build_type: Release
                    compiler: apple-clang
                    compiler.version: 13
                    os: Macos
                  options
                    fPIC: True
                    shared: False
              abe5e2b04ea92ce2ee91bc9834317dbe66628206  # package_id
                info
                  settings
                    arch: x86_64
                    build_type: Release
                    compiler: gcc
                    compiler.version: 11
                    os: Linux
                  options
                    shared: True


We can see, for the latest recipe revision of ``zlib/1.2.13`` several binaries. Every binary is identified by its own ``package_id``, and below it we can see some information for that binary under ``info``. This information is the one used to compute the ``package_id``. Every time something change in this information, like the architecture, or being a static or a shared library, a new ``package_id`` is computed because it represents a different binary.

.. image:: /images/conan_package_id.png
   :width: 680 px
   :align: center

The ``packge_id`` is computed as the sha1 hash of the ``conaninfo.txt`` file, containing the ``info`` displayed above. It is relatively easy to display such file:

.. code-block:: bash

    $ conan install --requires=zlib/1.2.13 --build=missing
    # Use the <package-id> listed in the install
    $ conan cache path zlib/1.2.13:<package-id>
    # cat the conaninfo.txt in the returned path
    $ cat <path>/conaninfo.txt
    [settings]
    arch=x86_64
    build_type=Release
    compiler=msvc
    compilerruntime=dynamic
    compilerruntime_type=Release
    compiler.version=193
    os=Windows
    [options]
    shared=False
    $ sha1sum <path>/conaninfo.txt
    # Should be the "package_id"!

The ``package_id`` is the sha1 checksum of the ``conaninfo.txt`` file inside the package. You can validate it with the ``sha1sum`` utility.





- Graphic2