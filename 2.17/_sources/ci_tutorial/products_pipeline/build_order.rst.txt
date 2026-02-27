Products pipeline: the build-order
==================================


The previous section used ``--build=missing`` to build all the necessary packages in the same CI machine.
This is not always desired, or even possible, and in many situations it is preferable to do a distributed build, to achieve faster builds and better usage the CI resources. The most natural distribution of the build load is to build different packages in different machines. Let's see how this is possible with the ``conan graph build-order`` command.

Let's start as usual making sure we have a clean environment with the right repositories defined:

.. code-block:: bash

    # First clean the local "build" folder
    $ pwd  # should be <path>/examples2/ci/game
    $ rm -rf build  # clean the temporary build folder 
    $ mkdir build && cd build # To put temporary files

    $ conan remove "*" -c  # Make sure no packages from last run
    # NOTE: The products repo is first, it will have higher priority.
    $ conan remote enable products


We will obviate by now the ``mapviewer/1.0`` product and focus this section in the ``game/1.0`` product.
The first step is to compute the "build-order", that is, the list of packages that need to be built, and in what order.
This is done with the following ``conan graph build-order`` command:

.. code-block:: bash

    $ conan graph build-order --requires=game/1.0 --build=missing --order-by=recipe --reduce --format=json > game_build_order.json

Note a few important points:

- It is necessary to use the ``--build=missing``, in exactly the same way than in the previous section. Failing to provide the intended ``--build`` policy and argument will result in incomplete or erroneous build-orders.
- The ``--reduce`` argument eliminates all elements in the resulting order that don't have the ``binary: Build`` policy. This means that the resulting "build-order" cannot be merged with other build order files for aggregating them into a single one, which is important when there are multiple configurations and products.
- The ``--order-by`` argument allows to define different orders, by "recipe" or by "configuration". In this case, we are using ``--order-by=recipe`` which is intended to parallelize builds per recipe, that means, that all possible different binaries for a given package like ``engine/1.0`` should be built first before any consumer of ``engine/1.0`` can be built.

The resulting ``game_build_order.json`` looks like:

.. code-block:: json
  :caption: game_build_order.json

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
                                "binary": "Build",
                                "build_args": "--requires=engine/1.0 --build=engine/1.0",      
                            }
                        ]
                    ]
                }
            ],
            [
                {
                    "ref": "game/1.0#1715574045610faa2705017c71d0000e",
                    "depends": [
                        "engine/1.0#fba6659c9dd04a4bbdc7a375f22143cb"
                    ],
                    "packages": [
                        [
                            {
                                "package_id": "bac7cd2fe1592075ddc715563984bbe000059d4c",
                                "binary": "Build",
                                "build_args": "--requires=game/1.0 --build=game/1.0",
                            }
                        ]
                    ]
                }
            ]
        ]
    }


For convenience, in the same way that ``conan graph info ... --format=html > graph.html`` can generate a file with an HTML interactive dependency graph, the ``conan graph build-order ... --format=html > build_order.html`` can generate an HTML visual representation of the above json file:


.. image:: ./build_order_simple.png
   :width: 500 px
   :align: center


The resulting json contains an ``order`` element which is a list of lists. This arrangement is important, every element in the top list is a set of packages that can be built in parallel because they do not have any relationship among them. You can view this list as a list of "levels", in level 0, there are packages that have no dependencies to any other package being built, in level 1 there are packages that contain dependencies only to elements in level 0 and so on.

Then, the order of the elements in the outermost list is important and must be respected. Until the build of all the packages in one list item has finished, it is not possible to start the build of the next "level".

Using the information in the ``graph_build_order.json`` file, it is possible to execute the build of the necessary packages, in the same way that the previous section's ``--build=missing`` did, but not directly managed by us.

Taking the arguments from the json, the commands to execute would be:

.. code-block:: bash

    $ conan install --requires=engine/1.0 --build=engine/1.0
    $ conan install --requires=game/1.0 --build=game/1.0

We are executing these commands manually, but in practice, it would be a ``for`` loop in CI executing over the json output. We will see some Python code later for this. At this point we wanted to focus on the ``conan graph build-order`` command, but we haven't really explained how the build is distributed.

Also note that inside every element there is an inner list of lists, the ``"packages"`` section, for all the binaries that must be built for a specific recipe for different configurations.

Let's move now to see how a multi-product, multi-configuration build order can be computed.
