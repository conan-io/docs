.. _ci_tutorial:

Continuous Integration (CI) tutorial
====================================

.. note::

  - This is an advanced topic, previous knowledge of Conan is necessary. Please :ref:`read and practice the user tutorial<tutorial>` first.
  - This section is intended for devops and build engineers designing and implementing a CI pipeline involving Conan packages, if it is not the
    case, you can skip this section.


Continuous Integration has different meanings for different users and organizations. In this tutorial we will cover the scenarios when users
are doing changes to the source code of their packages and want to automatically build new binaries for those packages and also compute if those new package changes integrate cleanly or break the organization main products.

In this tutorial we will use this small project that uses several packages (static libraries by default) to build a couple of applications, a video game and a map viewer utility. The ``game`` and ``mapviewer`` are our final "**products**", what we distribute to our users:

.. graphviz::
    :align: center

    digraph game {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="BT"
        "game/1.0" -> "engine/1.0" -> "ai/1.0" -> "mathlib/1.0";
        "engine/1.0" -> "graphics/1.0" -> "mathlib/1.0";
        "mapviewer/1.0" -> "graphics/1.0";
        "game/1.0" [fillcolor="lightgreen"];
        "mapviewer/1.0" [fillcolor="lightgreen"];
        {
            rank = same;
            edge[ style=invis];
            "game/1.0" -> "mapviewer/1.0" ;
            rankdir = LR;
        }
    }


All of the packages in the dependency graph have a ``requires`` to its direct dependencies using version ranges, for example, ``game`` contains a ``requires("engine/[>=1.0 <2]")`` so new patch and minor versions of the dependencies will automatically be used without needing to modify the recipes.

.. note::

    **Important notes**

    - This section is written as a hands-on tutorial. It is intended to be reproduced by copying the commands in your machine.
    - The tutorial presents some of the tools, good practices and common approaches to the CI problem. But there are no silver bullets.
      This tutorial is not the unique way that things should be done.
      Different organizations might have different needs and priorities, different build services power and budget, different sizes, etc.
      The principles and practices presented in the tutorial might need to be adapted.
    - If you have any questions or feedback, please submit a new issue in https://github.com/conan-io/conan/issues
    - However some of the principles and best practices would be general for all approaches. Things like package immutability, using promotions
      between repositories and not using the ``channel`` for that purpose are good practices that should be followed.


Packages and products pipelines
-------------------------------

When a developer is doing some changes to a package source code, we will consider 2 different parts or pipelines of the overall system CI:
the **packages pipeline** and the **products pipeline**

- The **packages pipeline** takes care of building one single package when its code is changed. If necessary it will build it for different configurations.
- The **products pipeline** takes care of building the main organization "products" (the packages that implement the final applications or deliverables),
  and making sure that changes and new versions in dependencies integrate correctly, rebuilding any intermediate packages in the graph if necessary.

The idea is that if some developer does changes to the ``ai`` package, producing a new ``ai/1.1.0`` version, the packages pipeline will first build this
new version. But this new version might accidentally break or require rebuilding some consumer packages. If our organization main **products** are
``game/1.0`` and ``mapviewer/1.0``, then the products pipeline can be triggered, in this case it would rebuild ``engine/1.0`` and ``game/1.0`` as
they are affected by the change.


Repositories and promotions
---------------------------

The concept of multiple server side repositories is very important for CI. In this tutorial we will use 3 repositories:

- ``develop``: This repository is the main one that developers have configured in their machines to be able to ``conan install`` dependencies
  and work. As such it is expected to be quite stable, similar to a shared "develop" branch in git, and the repository should contain pre-compiled
  binaries for the organization's pre-defined platforms, so developers and CI don't need to do ``--build=missing`` and build again and again from
  source.
- ``packages``: This repository will be used to temporarily upload the packages built by the "packages pipeline", to not upload them directly to
  the ``develop`` repo and avoid disruption until these packages are fully validated.
- ``products``: This repository will be used to temporarily upload the packages built by the "products pipeline", while building and testing that
  new dependencies changes do not break the main "products".

.. graphviz::
    :align: center

    digraph repositories {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="LR";
        subgraph cluster_0 {
            style=filled;
		    color=lightgrey;
            rankdir="LR";
            label = "Packages server";
            "packages\n repository" -> "products\n repository" -> "develop\n repository" [ label="promotion" ];
        }
       
    }

Promotions are the mechanism used to make packages available from one pipeline to the other. Connecting the above packages and product pipelines
with the repositories, there will be 2 promotions:

- When all the different binaries for the different configurations have been built for a single package with the ``packages pipeline``, and uploaded
  to the ``packages`` repository, the new version and changes to the package can be considered "correct" and promoted (copied) to the ``products``
  repository.
- When the ``products pipeline`` has built from source all the necessary packages that need a re-build because of the new package versions in
  the ``products`` repository and has checked that the organization "products" (such ``game/1.0`` and ``mapviewer/1.0``) are not broken, then
  the packages can be promoted (copied) from the ``products`` repo to the ``develop`` repo, to make them available for all other developers and CI.


.. note::

  - The concept of **immutability** is important in package management and devops. Modifying ``channel`` is strongly discouraged, see :ref:`Package promotions<devops_package_promotions>`.
  - The versioning approach is important. This tutorial will be following :ref:`the default Conan versioning approach, see details here<devops_versioning_default>`

This tutorial is just modeling the **development** flow. In production systems, there will be other repositories
and promotions, like a ``testing`` repository for the QA team, and a final ``release`` repository for final users, such that packages can
be promoted from ``develop`` to ``testing`` to ``release`` as they pass validation. Read more about promotions in :ref:`Package promotions<devops_package_promotions>`.


Let's start with the tutorial, move to the next section to do the project setup:

.. toctree::
   :maxdepth: 2

   project_setup
   packages_pipeline
   products_pipeline
