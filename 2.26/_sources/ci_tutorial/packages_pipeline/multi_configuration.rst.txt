Package pipeline: multi configuration
=====================================

In the previous section we were building just 1 configuration. This section will cover the case in which we need to build more
than 1 configuration. We will use the ``Release`` and ``Debug`` configurations here for convenience, as it is easier to 
follow, but in real case these configurations will be more like Windows, Linux, OSX, building for different architectures, 
cross building, etc.

Let's begin cleaning our cache:

.. code-block:: bash

    $ conan remove "*" -c  # Make sure no packages from last run

We will create the packages for the 2 configurations sequentially in our computer, but note these will typically run
in different computers, so it is typical for CI systems to launch the builds of different configurations in parallel.

.. code-block:: bash
    :caption: Release build

    $ cd ai  # If you were not inside "ai" folder already
    $ conan create . --build="missing:ai/*" -s build_type=Release --format=json > graph.json
    $ conan list --graph=graph.json --graph-binaries=build --format=json > built.json

    $ conan remote enable packages
    $ conan upload -l=built.json -r=packages -c --format=json > uploaded_release.json
    $ conan remote disable packages

We have done a few changes and extra steps:

- First step is similar to the one in the previous section, a ``conan create``, just making it explicit our configuration
  ``-s build_type=Release`` for clarity, and capturing the output of the ``conan create`` in a ``graph.json`` file.
- The second step is create from the ``graph.json`` a ``built.json`` **package list** file, with the packages that needs to be uploaded,
  in this case, only the packages that have been built from source (``--graph-binaries=build``) will be uploaded. This is
  done for efficiency and faster uploads.
- Third step is to enable the ``packages`` repository. It was not enabled to guarantee that all possible dependencies came from ``develop``
  repo only.
- Then, we will upload the ``built.json`` package list to the ``packages`` repository, creating the ``uploaded_release.json``
  package list with the new location of the packages (the server repository).
- Finally, we will disable again the ``packages`` repository

Likewise, the Debug build will do the same steps:


.. code-block:: bash
    :caption: Debug build

    $ conan create . --build="missing:ai/*" -s build_type=Debug --format=json > graph.json
    $ conan list --graph=graph.json --graph-binaries=build --format=json > built.json

    $ conan remote enable packages
    $ conan upload -l=built.json -r=packages -c --format=json > uploaded_debug.json
    $ conan remote disable packages


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


When all the different binaries for ``ai/1.1.0`` have been built correctly, the ``package pipeline`` can consider its job succesfull and decide
to promote those binaries. But further package builds and checks are necessary, so instead of promoting them to the ``develop`` repository,
the ``package pipeline`` can promote them to the ``products`` binary repository. As all other developers and CI use the ``develop`` repository,
no one will be broken at this stage either:

.. code-block:: bash
    :caption: Promoting from packages->product

    # aggregate the package list
    $ conan pkglist merge -l uploaded_release.json -l uploaded_debug.json --format=json > uploaded.json

    $ conan remote enable packages
    $ conan remote enable products
    # Promotion using Conan download/upload commands 
    # (slow, can be improved with art:promote custom command)
    $ conan download --list=uploaded.json -r=packages --format=json > promote.json
    $ conan upload --list=promote.json -r=products -c
    $ conan remote disable packages
    $ conan remote disable products


The first step uses the ``conan pkglist merge`` command to merge the package lists from the "Release" and "Debug" configurations and 
merge it into a single ``uploaded.json`` package list.
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


To summarize:

- We built 2 different configurations, ``Release`` and ``Debug`` (could have been Windows/Linux or others), and uploaded them
  to the ``packages`` repository.
- When all package binaries for all configurations were successfully built, we promoted them from the ``packages`` to the
  ``products`` repository, to make them available for the ``products pipeline``.
- **Package lists** were captured in the package creation process and merged into a single one to run the promotion.


There is still an aspect that we haven't considered yet, the possibility that the dependencies of ``ai/1.1.0`` change
during the build. Move to the next section to see how to use lockfiles to achieve more consistent multi-configuration builds.
