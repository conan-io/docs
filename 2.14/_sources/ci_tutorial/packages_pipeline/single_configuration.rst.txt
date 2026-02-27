Package pipeline: single configuration
======================================

We will start with the most simple case, in which we only had to build 1 configuration, and that configuration 
can be built in the current CI machine.

As we described before while presenting the different server binary repositories, the idea is that package builds
will use by default the ``develop`` repo only, which is considered the stable one for developer and CI jobs.

This pipeline starts from a clean state, with no packages in the cache, and only the ``develop`` repository enabled.

With this configuration the CI job could just do:

.. code-block:: bash

    $ cd ai
    $ conan create . --build="missing:ai/*"
    ...
    ai/1.1.0: SUPER BETTER Artificial Intelligence for aliens (Release)!
    ai/1.1.0: Intelligence level=50


Note the ``--build="missing:ai/*"`` might not be fully necessary in some cases, but it can save time in other situations.
For example, if the developer did some changes just to the repo README, and didn't bump the version at all, Conan will not 
generate a new ``recipe revision``, and detect this as a no-op, avoiding having to unnecessarily rebuild binaries from source.

If we are in a single-configuration scenario and it built correctly, for this simple case we don't need a promotion,
and just uploading directly the built packages to the ``products`` repository will be enough, where the ``products pipeline``
will pick it later.


.. code-block:: bash

    # We don't want to disrupt developers or CI, upload to products 
    $ conan remote enable products
    $ conan upload "ai*" -r=products -c
    $ conan remote disable products

As the cache was initially clean, all ``ai`` packages would be the ones that were built in this pipeline.


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
                }
                subgraph cluster_2 {
                label = "products\n repository" 
                shape = "box";
                style=filled;
                color=lightblue;
                "products" [style=invis];
                "ai/1.1.0\n (single config)";
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


This was a very simple scenario, let's move to a more realistic one: having to build more than one configuration.
