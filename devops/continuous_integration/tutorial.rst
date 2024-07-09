Continuous Integration (CI) tutorial
====================================

Continuous Integration has different meanings for different users and organizations. In this tutorial we will cover the scenarios when users
are doing changes to the source code of their packages and want to automatically build new binaries for those packages and also compute if those new package changes integrate cleanly or break the organization main products.

We will use in this tutorial this small project that uses several packages (static libraries by default) to build a couple of applications, a video game and a map viewer utility:

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
    - However some of the principles and best practices would be general for all approaches. Things like package immutability, using promotions
      between repositories and not using the ``channel`` for that purpose are good practices that should be followed.


Packages and products pipelines
-------------------------------

When a developer is doing some changes to a package source code, we will consider 2 different parts or pipelines of the overall system CI:
the **packages pipeline** and the **products pipeline**


The **packages pipeline** will build, create and upload the package binaries for the different configurations and platforms, when some
developer is submitting some changes to one of the organization repositories source code. For example if a developer is doing some changes
to the ``ai`` package, improving some of the library functionality, and bumping the version to ``ai/1.1.0``. If the organization needs to
support both Windows and Linux platforms, then the package pipeline will build the new ``ai/1.1.0`` both for Windows and Linux, before
considering the changes are valid. If some of the configurations fail to build under a specific platform, it is common to consider the
changes invalid and stop the processing of those changes, until the code is fixed.


The **products pipeline** responds a more challenging question: does my "products" build correctly with the latest changes that have been done
to the packages? This is the real "Continuous Integration" part, in which changes in different packages are really tested against the organization
important product to check if things integrate cleanly or break. Let's continue with the example above, if we now have a new ``ai/1.1.0`` package,
is it going to break the existing ``game/1.0`` and/or ``mapviewer/1.0`` applications? Is it necessary to re-build from source some of the existing
packages that depend directly or indirectly on ``ai`` package? In this tutorial we will use ``game/1.0`` and ``mapviewer/1.0`` as our "products",
but this concept will be further explained later, and specially why it is important to think in terms of "products" instead of trying to explicitly
model the dependencies top-bottom in the CI.


Repositories and promotions
---------------------------

The concept of multiple server side repositories is very important for CI. In this tutorial we will use 3 repositories:

- ``develop``: This repository is the main one that developers have configured in their machines to be able to ``conan install`` dependencies
  and work. As such it is expected to be quite stable, similar to a shared "develop" branch in git, and the repository should contain pre-compiled
  binaries for the organization pre-defined platforms, so developers and CI don't need to do ``--build=missing`` and build again and again from
  source.
- ``packages``: This repository will be used to upload individual package binaries for different configurations. To consider a certain change
  in a package source code to be correct, it might require that such change build correctly under a variaty of platforms, lets say Windows and Linux.
  If the package builds correctly under Linux more quickly, we can upload it to the ``packages`` repository, and wait until the Windows build 
  finishes, and only when both are correct we can proceed. The ``packages`` repository serves as a temporary storage when building different
  binaries for the same package in different platforms concurrently.
- ``products``: It is possible that some changes create 


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


Let's start with the tutorial, move to the next section to do the project setup:

.. toctree::
   :maxdepth: 2

   project_setup
   packages_pipeline
   products_pipeline
