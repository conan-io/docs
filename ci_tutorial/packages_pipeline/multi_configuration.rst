Package pipeline: multi configuration
=====================================

In the previous section we were building just 1 configuration. This section will cover the case in which we need to build more
than 1 configuration. We will use the ``Release`` and ``Debug`` configurations here for convenience, as it is easier to 
follow, but in real case these configurations will be more like Windows, Linux, OSX, building for different architectures, 
cross building, etc.

Let's begin cleaning our cache and initializing only the ``develop`` repo:


.. code-block:: bash

    $ conan remove "*" -c  # Make sure no packages from last run
    $ conan remote remove "*"  # Make sure no other remotes defined
    $ conan remote add develop <url-develop-repo>  # Add only the develop repo


We will create the packages for the 2 configurations sequentially in our computer, but note these will typically run
in different computers, so it is typical for CI systems to launch the builds of different configurations in parallel.

.. code-block:: bash
    :caption: Release build

    $ conan create . --build="missing:ai/*" -s build_type=Release --format=json > graph.json
    $ conan list --graph=graph.json --graph-binaries=build --format=json > upload_release.json
    $ conan remote add packages "<url-packages-repo>"
    $ conan upload -l=upload_release.json -r=packages -c --format=json > upload_release.json

We have done a few changes and extra steps:

- First step is similar to the one in the previous section, a ``conan create``, just making it explicit our configuration
  ``-s build_type=Release`` for clarity, and capturing the output of the ``conan create`` in a ``graph.json`` file.
- The second step is create a ``upload_release.json`` **package list** file, with the packages that needs to be uploaded,
  in this case, only the packages that have been built from source (``--graph-binaries=build``) will be uploaded. This is
  done for efficiency and faster uploads.
- Third step is to define the ``packages`` repository
- Finally, we will upload the ``upload_release.json`` package list to the ``packages`` repository, updating the ``upload_release.json``
  package list with the new location of the packages (the server repository).

Likewise, the Debug build will do the same steps:


.. code-block:: bash
    :caption: Debug build

    $ conan create . --build="missing:ai/*" -s build_type=Debug --format=json > graph.json
    $ conan list --graph=graph.json --graph-binaries=build --format=json > upload_debug.json
    $ conan remote add packages "<url-packages-repo>" -f  # Can be ommitted, it was defined above
    $ conan upload -l=upload_debug.json -r=packages -c --format=json > upload_debug.json


When both Release and Debug configuration finish successfully, we would have these packages in the repositories:

.. graphviz::
    :align: center

    digraph repositories {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="LR"; 
        subgraph cluster_0 {
                label="Packages server";
                style=filled;
                color=lightgrey;
                subgraph cluster_1 {
                label = "packages\n repository" 
                shape = "box";
                style=filled;
                color=lightblue;
                "packages" [style=invis];
                "ai/1.1.0\n (Release)";
                "ai/1.1.0\n (Debug)";
                }
                subgraph cluster_2 {
                label = "products\n repository" 
                shape = "box";
                style=filled;
                color=lightblue;
                "products" [style=invis];
                } 
                subgraph cluster_3 {
                rankdir="BT";
                shape = "box";
                label = "develop repository";
                color=lightblue;
                rankdir="BT";
        
                node [fillcolor="lightskyblue", style=filled, shape=box]
                "game/1.0" -> "engine/1.0" -> "ai/1.0" -> "mathlib/1.0";
                "engine/1.0" -> "graphics/1.0" -> "mathlib/1.0";
                "mapviewer/1.0" -> "graphics/1.0";
                "game/1.0" [fillcolor="lightgreen"];
                "mapviewer/1.0" [fillcolor="lightgreen"];
                }
                {
                edge[style=invis];
                "packages" -> "products" -> "game/1.0" ; 
                rankdir="BT";    
                }
        }
    }


If the build of all configurations for ``ai/1.1.0`` were succesfull, then the ``packages pipeline`` can proceed and promote
them to the ``products`` repository:

.. code-block:: bash
    :caption: Promoting from packages->product

    # aggregate the package list
    $ conan pkglist merge -l upload_release.json -l upload_debug.json --format=json > promote.json

    $ conan remote add packages "<url-packages-repo>" -f  # Can be ommitted, it was defined above
    $ conan remote add products "<url-products-repo>" -f  # Can be ommitted, it was defined above

    # Promotion with Artifactory CE (slow, can be improved with art:promote)
    $ conan download --list=promote.json -r=packages --format=json > promote.json
    $ conan upload --list=promote.json -r=products -c


The first step uses the ``conan pkglist merge`` command to merge the package lists from the "Release" and "Debug" configurations and 
merge it into a single ``promote.json`` package list.
This list is the one that will be used to run the promotion.

In this example we are using a slow ``conan download`` + ``conan upload`` promotion. This can be way more efficient with 
the ``conan art:promote`` extension command.

After running the promotion we will have the following packages in the server:

.. graphviz::
    :align: center

    digraph repositories {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="LR"; 
        subgraph cluster_0 {
                label="Packages server";
                style=filled;
                color=lightgrey;
                subgraph cluster_1 {
                label = "packages\n repository" 
                shape = "box";
                style=filled;
                color=lightblue;
                "packages" [style=invis];
                "ai/1.1.0\n (Release)";
                "ai/1.1.0\n (Debug)";
                }
                subgraph cluster_2 {
                label = "products\n repository" 
                shape = "box";
                style=filled;
                color=lightblue;
                "products" [style=invis];
                "ai/promoted release" [label="ai/1.1.0\n (Release)"];
                "ai/promoted debug" [label="ai/1.1.0\n (Debug)"];
                } 
                subgraph cluster_3 {
                rankdir="BT";
                shape = "box";
                label = "develop repository";
                color=lightblue;
                rankdir="BT";
        
                node [fillcolor="lightskyblue", style=filled, shape=box]
                "game/1.0" -> "engine/1.0" -> "ai/1.0" -> "mathlib/1.0";
                "engine/1.0" -> "graphics/1.0" -> "mathlib/1.0";
                "mapviewer/1.0" -> "graphics/1.0";
                "game/1.0" [fillcolor="lightgreen"];
                "mapviewer/1.0" [fillcolor="lightgreen"];
                }
                {
                edge[style=invis];
                "packages" -> "products" -> "game/1.0" ; 
                rankdir="BT";    
                }
        }
    }
