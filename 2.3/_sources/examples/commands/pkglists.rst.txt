.. _examples_commands_pkglists:

Using packages-lists
====================

.. include:: ../../common/experimental_warning.inc


Packages lists are a powerful and convenient Conan feature that allows to automate and concatenate different Conan commands.
Let's see some common use cases:


Listing packages and downloading them
-------------------------------------

A first simple use case could be listing some recipes and/or binaries in a server, and then downloading them.

We can do any ``conan list``, for example, to list all ``zlib`` versions above ``1.2.11``, the latest recipe revision,
all Windows binaries for that latest recipe revision, and finally the latest package revision for every binary.
Note that if we want to actually download something later, it is necessary to specify the ``latest`` package revision,
otherwise only the recipes will be downloaded.

.. code-block:: bash

    $ conan list "zlib/[>1.2.11]#latest:*#latest" -p os=Windows --format=json -r=conancenter > pkglist.json


The output of the command is sent in ``json`` format to the file ``pkglist.json`` that looks like:


.. code-block:: json
    :caption: pkglist.json (simplified)

    "conancenter": {
        "zlib/1.2.12": {
            "revisions": {
                "b1fd071d8a2234a488b3ff74a3526f81": {
                    "timestamp": 1667396813.987,
                    "packages": {
                        "ae9eaf478e918e6470fe64a4d8d4d9552b0b3606": {
                            "revisions": {
                                "19808a47de859c2408ffcf8e5df1fdaf": {
                                }
                            },
                            "info": {
                                "settings": {
                                    "arch": "x86_64",
                                    "os": "Windows"
                                }
                            }
                        }
                    }
                }
            },
        "zlib/1.2.13": {
        }
    }


The first level in the ``pkglist.json`` is the "origin" remote or "Local Cache" if the list happens in the cache. 
In this case, as we listed the packages in ``conancenter`` remote, that will be the origin.


We can now do a download of these recipes and binaries with a single ``conan download`` invocation:

.. code-block:: bash

    $ conan download --list=pkglist.json -r=conancenter
    # Download the recipes and binaries in pkglist.json
    # And displays a report of the downloaded things


Downloading from one remote and uploading to a different remote
---------------------------------------------------------------

Let's say that we create a new package list from the packages downloaded in the previous step:

.. code-block:: bash

    $ conan download --list=pkglist.json -r=conancenter --format=json > downloaded.json
    # Download the recipes and binaries in pkglist.json
    # And stores the result in "downloaded.json"


The resulting ``downloaded.json`` will be almost the same as the ``pkglist.json`` file, but in this case, the "origin" of
those packages is the ``"Local Cache"`` (as the downloaded packages will be in the cache):


.. code-block:: json
    :caption: downloaded.json (simplified)

    "Local Cache": {
            "zlib/1.2.12": {
                "revisions": {
                }
            }
        }

That means that we can now upload this same set of recipes and binaries to a different remote:

.. code-block:: bash

    $ conan upload --list=downloaded.json -r=myremote -c
    # Upload those artifacts to the same remote


.. note::

    **Best practices**

    This would be a **slow** mechanism to run promotions between different server repositories. Servers like
    Artifactory provide ways to directly copy packages from one repository to another without using a client, 
    that are orders of magnitude faster because of file deduplication, so that would be the recommended approach.
    The presented approach in this section might be used for air-gapped environments and other situations in which
    it is not possible to do a server-to-server copy.



Building and uploading packages
-------------------------------

One of the most interesting flows is the one when some packages are being built in the local cache, with a 
``conan create`` or ``conan install --build=xxx`` command. Typically, we would like to upload the locally built
packages to the server, so they don't have to be re-built again by others. But we might want to upload only
the built binaries, but not all others transitive dependencies, or other packages that we had previously in
our local cache.

It is possible to compute a package list from the output of a ``conan install``, ``conan create`` and ``conan graph info``
commands. Then, that package list can be used for the upload. Step by step:

First let's say that we have our own package ``mypkg/0.1`` and we create it:

.. code-block:: bash

    $ conan new cmake_lib -d name=mypkg -d version=0.1
    $ conan create . --format=json > create.json


This will create a json representation of the graph, with information of what packages have been built ``"binary": "Build"``:

.. code-block:: json
    :caption: create.json (simplified)

    {
    "graph": {
        "nodes": {
            "0": {
                "ref": "conanfile",
                "id": "0",
                "recipe": "Cli",
                "context": "host",
                "test": false
            },
            "1": {
                "ref": "mypkg/0.1#f57cc9a1824f47af2f52df0dbdd440f6",
                "id": "1",
                "recipe": "Cache",
                "package_id": "2401fa1d188d289bb25c37cfa3317e13e377a351",
                "prev": "75f44d989175c05bc4be2399edc63091",
                "build_id": null,
                "binary": "Build"
            }
        }
    }


We can compute a package list from this file, and then upload those artifacts to the server with:

.. code-block:: bash

    $ conan list --graph=create.json --graph-binaries=build --format=json > pkglist.json
    # Create a pkglist.json with the known list of recipes and binaries built from sources
    $ conan upload --list=pkglist.json -r=myremote -c


Removing packages lists
-----------------------

It is also possible to first ``conan list`` and create a list of things to remove, and then remove them:

.. code-block:: bash

    # Removes everything from the cache
    $ conan list *#* --format=json > pkglist.json
    $ conan remove --list=pkglist.json  -c

Note that in this case, the default patterns are different in ``list`` and ``remove``, because of the destructive nature of ``conan remove``:

- When a recipe is passed to ``remove`` like ``conan remove zlib/1.2.13``, it will remove the recipe of ``zlib/1.2.13`` and all of its binaries, because the binaries cannot live without the recipe.
- When a ``package_id`` is passed, like ``conan remove zlib/1.2.13:package_id``, then that specific ``package_id`` will be removed, but the recipe will not

Then the pattern to remove everything will be different if we call directly ``conan remove`` or if we call first ``conan list``, for example:

.. code-block:: bash

    # Removes everything from the cache
    $ conan remove *
    # OR via list, we need to explicitly include all revisions
    $ conan list *#* --format=json > pkglist.json
    $ conan remove --list=pkglist.json  -c

    # Removes only the binaries from the cache (leave recipes)
    $ conan remove *:*
    # OR via list, we need to explicitly include all revisions
    $ conan list *#*:* --format=json > pkglist.json
    $ conan remove --list=pkglist.json  -c


For more information see the :ref:`Reference commands section<reference_commands>`
