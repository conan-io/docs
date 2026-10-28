Products pipeline: distributed full pipeline with lockfiles
===========================================================

This section will present the full and complete implementation of a multi-product, multi-configuration
distributed CI pipeline. It will cover important implementation details:

- Using lockfiles to guarantee a consistent and fixed set of dependencies for all configurations.
- Uploading built packages to the ``products`` repository.
- Capturing "package lists" and using them to run the final promotion.
- How to iterate the "build-order" programmatically


Let's start as usual cleaning the local cache and defining the correct repos:

.. code-block:: bash

    # First clean the local "build" folder
    $ pwd  # should be <path>/examples2/ci/game
    $ rm -rf build  # clean the temporary build folder 
    $ mkdir build && cd build # To put temporary files

    $ conan remove "*" -c  # Make sure no packages from last run
    # NOTE: The products repo is first, it will have higher priority.
    $ conan remote enable products


Similarly to what we did in the ``packages pipeline`` when we wanted to ensure that the dependencies are exactly the same when building the different configurations and products, the first necessary step is to compute a ``conan.lock`` lockfile that we can pass to the different CI build agents to enforce the same set of dependencies everywhere. This can be done incrementally for the different ``products`` and configurations, aggregating it in the final single ``conan.lock`` lockfile. This approach assumes that both ``game/1.0`` and ``mapviewer/1.0`` will be using the same versions and revisions of the common dependencies. 

.. code-block:: bash

    $ conan lock create --requires=game/1.0 --lockfile-out=conan.lock
    $ conan lock create --requires=game/1.0 -s build_type=Debug --lockfile=conan.lock --lockfile-out=conan.lock
    $ conan lock create --requires=mapviewer/1.0 --lockfile=conan.lock --lockfile-out=conan.lock
    $ conan lock create --requires=mapviewer/1.0 -s build_type=Debug --lockfile=conan.lock --lockfile-out=conan.lock


.. note::

    Recall that the ``conan.lock`` arguments are mostly optional, as that is the default lockfile name.
    The first command can be typed as ``conan lock create --requires=game/1.0``. Also, all commands, including
    ``conan install``, if they find a existing ``conan.lock`` file they will use it automatically, without an
    explicit ``--lockfile=conan.lock``. The commands in this tutorial are shown explicitly complete for
    completeness and didactical reasons.


Then, we can compute the build order for each product and configuration. These commands are identical to the ones in the
previous section, with the only difference of adding a ``--lockfile=conan.lock`` argument:


.. code-block:: bash

    $ conan graph build-order --requires=game/1.0 --lockfile=conan.lock --build=missing --order-by=recipe --format=json > game_release.json
    $ conan graph build-order --requires=game/1.0 --lockfile=conan.lock --build=missing -s build_type=Debug --order-by=recipe --format=json > game_debug.json
    $ conan graph build-order --requires=mapviewer/1.0 --lockfile=conan.lock --build=missing --order-by=recipe --format=json > mapviewer_release.json
    $ conan graph build-order --requires=mapviewer/1.0 --lockfile=conan.lock --build=missing -s build_type=Debug --order-by=recipe --format=json > mapviewer_debug.json

Likewise the ``build-order-merge`` command will be identical to the previous one.
In this case, as this command doesn't really compute a dependency graph, a ``conan.lock`` argument is not necessary,
dependencies are not being resolved:


.. code-block:: bash

    $ conan graph build-order-merge --file=game_release.json --file=game_debug.json --file=mapviewer_release.json --file=mapviewer_debug.json --reduce --format=json > build_order.json


    
So far, this process has been almost identical to the previous section one, just with the difference of capturing and using a lockfile.
Now, we will explain the "core" of the ``products`` pipeline: iterating the build-order and distributing the build, and gathering the 
resulting built packages.

This would be an example of some Python code that performs the iteration sequentially (a real CI system would distribute the builds to different agents in parallel):


.. code-block:: python

  build_order = open("build_order.json", "r").read()
  build_order = json.loads(build_order)
  to_build = build_order["order"]

  pkg_lists = []  # to aggregate the uploaded package-lists
  for level in to_build:
      for recipe in level:  # This could be executed in parallel
          ref = recipe["ref"]
          # For every ref, multiple binary packages are being built. 
          # This can be done in parallel too. Often it is for different platforms
          # they will need to be distributed to different build agents
          for packages_level in recipe["packages"]:
              # This could be executed in parallel too
              for package in packages_level:
                  build_args = package["build_args"]
                  filenames = package["filenames"]
                  build_type = "-s build_type=Debug" if any("debug" in f for f in filenames) else ""
                  run(f"conan install {build_args} {build_type} --lockfile=conan.lock --format=json", file_stdout="graph.json")
                  run("conan list --graph=graph.json --format=json", file_stdout="built.json")
                  filename = f"uploaded{len(pkg_lists)}.json"
                  run(f"conan upload -l=built.json -r=products -c --format=json", file_stdout=filename)
                  pkg_lists.append(filename)


.. note::

  - This code is specific for the ``--order-by=recipe`` build-order, if chosing the ``--order-by=configuration``, the json
    is different and it would require a different iteration.


These are the tasks that the above Python code is doing:

- For every ``package`` in the build-order, a ``conan install --require=<pkg> --build=<pkg>`` is issued, and the result of this command is stored in a ``graph.json`` file
- The ``conan list`` command transform this ``graph.json`` into a package list called ``built.json``. Note that this package list actually stores both the built packages and the necessary transitive dependencies. This is done for simplicity, as later these package lists will be used for running a promotion, and we also want to promote the dependencies such as ``ai/1.1.0`` that were built in the ``packages pipeline`` and not by this job.
- The ``conan upload`` command uploads the package list to the ``products`` repo. Note that the ``upload`` first checks what packages already exist in the repo, avoiding costly transfers if they already exist.
- The result of the ``conan upload`` command is captured in a new package list called ``uploaded<index>.json``, that we will accumulate later, that will serve for the final promotion.


In practice this translates to the following commands (that you can execute to continue the tutorial):

.. code-block:: bash

  # engine/1.0 release
  $ conan install --requires=engine/1.0 --build=engine/1.0 --lockfile=conan.lock --format=json > graph.json
  $ conan list --graph=graph.json --format=json > built.json
  $ conan upload -l=built.json -r=products -c --format=json > uploaded1.json

  # engine/1.0 debug
  $ conan install --requires=engine/1.0 --build=engine/1.0 --lockfile=conan.lock -s build_type=Debug --format=json > graph.json
  $ conan list --graph=graph.json --format=json > built.json
  $ conan upload -l=built.json -r=products -c --format=json > uploaded2.json

  # game/1.0 release
  $ conan install --requires=game/1.0 --build=game/1.0 --lockfile=conan.lock --format=json > graph.json
  $ conan list --graph=graph.json --format=json > built.json
  $ conan upload -l=built.json -r=products -c --format=json > uploaded3.json

  # game/1.0 debug
  $ conan install --requires=game/1.0 --build=game/1.0 --lockfile=conan.lock -s build_type=Debug --format=json > graph.json
  $ conan list --graph=graph.json --format=json > built.json
  $ conan upload -l=built.json -r=products -c --format=json > uploaded4.json


After this step the newly built packages will be in the ``products`` repo and we will have 4 ``uploaded1.json`` - ``uploaded4.json`` files.

Simplifying the different release and debug configurations, the state of our repositories would be something like:


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
            "ai/promoted" [label="ai/1.1.0\n(new version)"];
            "engine/promoted" [label="engine/1.0\n(new binary)"];
            "game/promoted" [label="game/1.0\n(new binary)", fillcolor="lightgreen"];


            node [fillcolor="lightskyblue", style=filled, shape=box]
            "game/promoted" -> "engine/promoted" -> "ai/promoted";
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


We can now accumulate the different ``uploadedX.json`` files into a single package list ``uploaded.json`` that contains everything:

.. code-block:: bash

    $ conan pkglist merge -l uploaded0.json -l uploaded1.json -l uploaded2.json -l uploaded3.json --format=json > uploaded.json


And finally, if everything worked well, and we consider this new set of versions and new package binaries is ready to be used by developers and other CI jobs, then we can run the final promotion from the ``products`` to the ``develop`` repository:

.. code-block:: bash
    :caption: Promoting from products->develop

    # Promotion using Conan download/upload commands 
    # (slow, can be improved with art:promote custom command)
    $ conan download --list=uploaded.json -r=products --format=json > promote.json
    $ conan upload --list=promote.json -r=develop -c


And our final ``develop`` repository state will be:


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
            "ai/promoted" [label="ai/1.1.0\n(new version)"];
            "engine/promoted" [label="engine/1.0\n(new binary)"];
            "game/promoted" [label="game/1.0\n(new binary)", fillcolor="lightgreen"];
            "game/promoted" -> "engine/promoted" -> "ai/promoted" -> "mathlib/1.0";
             "engine/promoted" -> "graphics/1.0";
          }
          {
            edge[style=invis];
            "packages" -> "products" -> "game/1.0" ; 
            rankdir="BT";    
          }
        }
    }


This state of the ``develop`` repository will have the following behavior:

- Developers installing ``game/1.0`` or ``engine/1.0`` will by default resolve to latest ``ai/1.1.0`` and use it. They will find pre-compiled binaries for the dependencies too, and they can continue developing using the latest set of dependencies.
- Developers and CI that were using a lockfile that was locking ``ai/1.0`` version, will still be able to keep working with that dependency without anything breaking, as the new versions and package binaries do not break or invalidate the previous existing binaries.


At this point, the question of what to do with the lockfile used in the Ci could arise. Note that the ``conan.lock`` now contains the ``ai/1.1.0`` version locked. There could be different strategies, like storing this lockfile in the "products" git repositories, making it easily available when developers checkout those repos. Note, however, that this lockfile matches the latest state of the ``develop`` repo, so developers checking out one of the "products" git repositories and doing a ``conan install`` against the ``develop`` server repository will naturally resolve to the same dependencies stored in the lockfile.

It is a good idea to at least store this lockfile in any release bundle, if the "products" are bundled somehow (a installer, a debian/rpm/choco/etc package), to include or attach to this bundled release for the final users of the software, the lockfile used to produce it, so no matter what changes in development repositories, those lockfiles can be recovered from the release information later in time.


Final remarks
-------------

As commented in this CI tutorial introduction, this doesn't pretend to be a silver bullet, a CI system that you can deploy as-is in your organization.
This tutorial so far presents a "happy path" of a Continuous Integration process for developers, and how their changes in packages that are part of larger products can be tested and validated as part of those products.

The focus of this CI tutorial is to introduce some important concepts, good practices and tools such as:

- The importance of defining the organization "products", the main deliverables that need to be checked and built against new dependencies versions created by developers.
- How new dependencies versions of developers shouldn't be uploaded to the main development repositories until validated, to not break other developers and CI jobs.
- How multiple repositories can be used to build a CI pipeline that isolate non validated changes and new versions.
- How large dependency graphs can be built efficiently in CI with the ``conan graph build-order``, and how build-orders for different configurations and products can be merged together.
- Why ``lockfiles`` are necessary in CI when there are concurrent CI builds.
- The importance of versioning, and the role of ``package_id`` to re-build only what is necessary in large dependency graphs.
- Not using ``user/channel`` as variable and dynamic qualifiers of packages that change accross the CI pipeline, but using instead different server repositories.
- Running package promotions (copies) accross server repositories when new package versions are validated.


There are still many implementation details, strategies, use cases, and error scenarios that are not covered in this tutorial yet:

- How to integrate breaking changes of a package that requires a new breaking major version.
- Different versioning strategies, using pre-releases, using versions or relying on recipe revisions in certain cases.
- How lockfiles can be stored and used accross different builds, if it is good to persist them and where.
- Different branching and merging strategies, nightly builds, releases flows.

We plan to extend this CI tutorial, including more examples and use cases. If you have any question or feedback, please create a ticket in https://github.com/conan-io/conan/issues.
