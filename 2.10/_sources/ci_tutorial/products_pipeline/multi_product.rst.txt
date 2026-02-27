Products pipeline: multi-product multi-configuration builds
===========================================================

In the previous section we computed a ``conan graph build-order`` with several simplifications, we didn't take the ``mapviewer`` product into account, and we processed only 1 configuration.

In real scenarios, it will be necessary to manage more than one product and the most common case is that there is more than one configuration for every product. If we build these different cases sequentially it will be much slower and inefficient, and if we try to build them in parallel there will easily be many duplicated and unnecessary builds of the same packages, wasting resources and even producing issues as race conditions or traceability problems.

To avoid this issue, it is possible to compute a single unified "build-order" that aggregates all the different build-orders that are computed for the different products and configurations.

Let's start as usual cleaning the local cache and defining the correct repos:

.. code-block:: bash

    # First clean the local "build" folder
    $ pwd  # should be <path>/examples2/ci/game
    $ rm -rf build  # clean the temporary build folder 
    $ mkdir build && cd build # To put temporary files

    $ conan remove "*" -c  # Make sure no packages from last run
    # NOTE: The products repo is first, it will have higher priority.
    $ conan remote enable products

Now, we will start computing the build-order for ``game/1.0`` for the 2 different configurations that we are building in this tutorial, debug and release:

.. code-block:: bash

    $ conan graph build-order --requires=game/1.0 --build=missing --order-by=recipe --format=json > game_release.json
    $ conan graph build-order --requires=game/1.0 --build=missing --order-by=recipe -s build_type=Debug --format=json > game_debug.json

These commands are basically the same as in the previous section, each one with a different configuration and creating a different output file ``game_release.json`` and ``game_debug.json``. These files will be similar to the previous ones, but as we haven't used the ``--reduce`` argument (this is important!) they will actually contain a "build-order" of all elements in the graph, even if only some contain the ``binary: Build`` definition, and others will contain other ``binary: Download|Cache|etc``.

Now, let's compute the build-order for ``mapviewer/1.0``:

.. code-block:: bash

    $ conan graph build-order --requires=mapviewer/1.0 --build=missing --order-by=recipe --format=json > mapviewer_release.json
    $ conan graph build-order --requires=mapviewer/1.0 --build=missing --order-by=recipe -s build_type=Debug --format=json > mapviewer_debug.json


Note that in the generated ``mapviewer_xxx.json`` build-order files, there will be only 1 element for ``mapviewer/1.0`` that contains a ``binary: Download``, because there is really no other package to be built, and as ``mapviewer`` is an application linked statically, Conan knows that it can "skip" its dependencies binaries. If we had used the ``--reduce`` argument we would have obtained an empty ``order``. But this is not an issue, as the next final step will really compute what needs to be built.

Let's take all the 4 different "build-order" files (2 products x 2 configurations each), and merge them together:

.. code-block:: bash

    $ conan graph build-order-merge --file=game_release.json --file=game_debug.json --file=mapviewer_release.json --file=mapviewer_debug.json --reduce --format=json > build_order.json


Now we have applied the ``--reduce`` argument to produce a final ``build_order.json`` that is ready for distribution to the build agents and it only contains those specific packages that need to be built:

.. code-block:: json

    {
        "order_by": "recipe",
        "reduced": true,
        "order": [
            [
                {
                    "ref": "engine/1.0#fba6659c9dd04a4bbdc7a375f22143cb",
                    "packages": [
                        [
                            {
                                "package_id": "de738ff5d09f0359b81da17c58256c619814a765",
                                "filenames": ["game_release"],
                                "build_args": "--requires=engine/1.0 --build=engine/1.0",     
                            },
                            {
                                "package_id": "cbeb3ac76e3d890c630dae5c068bc178e538b090",
                                "filenames": ["game_debug"],
                                "build_args": "--requires=engine/1.0 --build=engine/1.0",
                                
                            }
                        ]
                    ]
                }
            ],
            [
                {
                    "ref": "game/1.0#1715574045610faa2705017c71d0000e",
                    "packages": [
                        [
                            {
                                "package_id": "bac7cd2fe1592075ddc715563984bbe000059d4c",
                                "filenames": ["game_release"],
                                "build_args": "--requires=game/1.0 --build=game/1.0",
                            },
                            {
                                "package_id": "01fbc27d2c156886244dafd0804eef1fff13440b",
                                "filenames": ["game_debug"],
                                "build_args": "--requires=game/1.0 --build=game/1.0",
                            }
                        ]
                    ]
                }
            ]
        ],
        "profiles": {
            "game_release": {"args": ""},
            "game_debug": {"args": "-s:h=\"build_type=Debug\""},
            "mapviewer_release": {"args": ""},
            "mapviewer_debug": {"args": "-s:h=\"build_type=Debug\""}
        }
    }


This build order summarizes the necessary builds. First it is necessary to build all different binaries for ``engine/1.0``. This recipe contains 2 different binaries, one for Release and the other for Debug. These binaries belong to the same element in the ``packages`` list, which means they do not depend on each other and can be built in parallel. Each binary tracks its own original build-order file with ``"filenames": ["game_release"],`` so it is possible to deduce the necessary profiles to apply to it. The ``build_order.json`` file contains a ``profiles`` section that helps recovering the profile and settings command line arguments that were used to create the respective original build-order files.

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

In this section we have still omitted some important implementation details that will follow in next sections. The goal was to focus on the ``conan graph build-order-merge`` command and how different products and configurations can be merged in a single "build-order". The next section will show with more details how this build-order can be really distributed in CI, using lockfiles to guarantee constant dependencies.
