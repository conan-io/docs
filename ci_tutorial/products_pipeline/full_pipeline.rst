Products pipeline: distributed full pipeline with lockfiles
===========================================================

This section will present the full and complete implementation of a multi-product, multi-configuration
distributed CI pipeline. We will complete the 

Let's start as usual cleaning the local cache and defining the correct repos:

.. code-block:: bash

    # First clean the local "build" folder
    $ pwd  # should be <path>/examples2/ci/game
    $ rm -rf build  # clean the temporary build folder 
    $ mkdir build && cd build # To put temporary files

    # Now clean packages and define remotes
    $ conan remove "*" -c  # Make sure no packages from last run
    $ conan remote remove "*"  # Make sure no other remotes defined
    # Add products repo, you might need to adjust this URL
    # NOTE: The products repo is added first, it will have higher priority.
    $ conan remote add products http://localhost:8081/artifactory/api/conan/products
    # Add develop repo, you might need to adjust this URL
    $ conan remote add develop http://localhost:8081/artifactory/api/conan/develop



Now, we will start computing the build-order for ``game/1.0`` for the 2 different configurations that we are building in this tutorial, debug and release:

.. code-block:: bash

    $ conan lock create --requires=game/1.0 --lockfile-out=conan.lock
    $ conan lock create --requires=game/1.0 -s build_type=Debug 
      --lockfile=conan.lock --lockfile-out=conan.lock
    $ conan lock create --requires=mapviewer/1.0 --lockfile=conan.lock 
      --lockfile-out=conan.lock
    $ conan lock create --requires=mapviewer/1.0 -s build_type=Debug 
      --lockfile=conan.lock --lockfile-out=conan.lock


.. note::

    Recall that the ``conan.lock`` arguments are mostly optional, as that is the default lockfile name.
    The first command can be typed as ``conan lock create --requires=game/1.0``. Also, all commands, including
    ``conan install``, if they find a existing ``conan.lock`` file they will use it automatically, without an
    explicit ``--lockfile=conan.lock``. The commands in this tutorial are shown explicitly complete for
    completeness and didactical reasons.


Then, we can compute the build order for each product and configuration. These commands are identical to the ones in the
previous section, with the only difference of adding a ``--lockfile=conan.lock`` argument:


.. code-block:: bash

    $ conan graph build-order --requires=game/1.0 --lockfile=conan.lock 
      --build=missing --order-by=recipe --format=json > game_release.json
    $ conan graph build-order --requires=game/1.0 --lockfile=conan.lock 
      --build=missing -s build_type=Debug --order-by=recipe --format=json > game_debug.json
    $ conan graph build-order --requires=mapviewer/1.0 --lockfile=conan.lock 
      --build=missing --order-by=recipe --format=json > mapviewer_release.json
    $ conan graph build-order --requires=mapviewer/1.0 --lockfile=conan.lock 
      --build=missing -s build_type=Debug --order-by=recipe --format=json > mapviewer_debug.json

Likewise the ``build-order-merge`` command will be identical to the previous one.
In this case, as this command doesn't really compute a dependency graph, a ``conan.lock`` argument is not necessary,
dependencies are not being resolved:


.. code-block:: bash

    $ conan graph build-order-merge 
      --file=game_release.json --file=game_debug.json 
      --file=mapviewer_release.json --file=mapviewer_debug.json 
      --reduce --format=json > build_order.json


    






This build order summarizes the necessary builds. First it is necessary to build all different binaries for ``engine/1.0``. This recipe contains 2 different binaries, one for Release and the other for Debug. These binaries belong to the same element in the ``packages`` list, which means they do not depend on each other and can be built in parallel. Each binary tracks its own original build-order file with ``"filenames": ["game_release"],`` so it is possible to deduce the necessary profiles to apply to it.

Then, after all binaries of ``engine/1.0`` have been built, it is possible to proceed to build the different binaries for ``game/1.0``. It also contains 2 different binaries for its debug and release configurations, which can be built in parallel.

In practice, this would mean something like:

.. code-block:: bash

    # This 2 could be executed in parallel 
    # (in different machines, or different Conan caches)
    $ conan install --requires=engine/1.0 --build=engine/1.0
    $ conan install --requires=engine/1.0 --build=engine/1.0 -s build_type=Debug

    # Once engine/1.0 builds finish, it is possible
    # to build these 2 binaries in parallel (in different machines or caches)
    $ conan install --requires=game/1.0 --build=game/1.0
    $ conan install --requires=game/1.0 --build=game/1.0 -s build_type=Debug

In this section we have still omitted some important implementation details that will follow in next sections. The goal was to focus on the ``conan graph build-order-merge`` command and how different products and configurations can be merged in a single "build-order".
