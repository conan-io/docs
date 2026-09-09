conan graph build-order
=======================

.. autocommand::
    :command: conan graph build-order -h


The ``conan graph build-order`` command computes the build order of the dependency graph for the recipe specified in ``path`` or in ``--requires/--tool-requires``.

There are 2 important arguments that affect how this build order is computed:

- The ``--order-by`` argument can take 2 values ``recipe`` and ``configuration``, depending how we want to
  structure and parallelize our CI.
- The ``--reduce`` argument will strip all packages in the order that doesn't need to be built from source.

By default, the ``conan graph build-order`` will return the order for the full dependency graph, and it will annotate
in each element what needs to be done, for example ``"binary": "Cache"`` if the binary is already in the Conan Cache
and doesnt need to be built from source, and ``"binary": "Build"``, if it needs to be built from source.
Having the full order is necessary if we want to ``conan graph build-order-merge`` several build-orders into a single
one later, because having the full information allows to preserve the relative order that would otherwise be lost and
broken.
Consequently, the ``--reduce`` argument should only be used when we are directly going to use the result to do the
build, but not if we plan to later do a merge of the resulting build-order with other ones.


Let's consider installing `libpng` and wanting to see the build order for this requirement ordered by recipe:

.. warning::

    Please be aware that starting with Conan 2.1.0, using the `--order-by` argument is
    recommended, and its absence is deprecated. This argument will be removed in the near
    future. It is maintained for backward compatibility. Note that the JSON output will
    differ if you use the `--order-by` argument, changing from a simple list to a
    dictionary with extended information.


.. code-block:: text

    $ conan graph build-order --requires=libpng/1.5.30 --format=json --order-by=recipe
    ...
    ======== Computing the build order ========
    {
        "order_by": "recipe",
        "reduced": false,
        "order": [
            [
                {
                    "ref": "zlib/1.3#06023034579559bb64357db3a53f88a4",
                    "depends": [],
                    "packages": [
                        [
                            {
                                "package_id": "d62dff20d86436b9c58ddc0162499d197be9de1e",
                                "prev": "54b9c3efd9ddd25eb6a8cbf01860b499",
                                "context": "host",
                                "binary": "Cache",
                                "options": [],
                                "filenames": [],
                                "depends": [],
                                "overrides": {},
                                "build_args": null
                            }
                        ]
                    ]
                }
            ],
            [
                {
                    "ref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b",
                    "depends": [
                        "zlib/1.3#06023034579559bb64357db3a53f88a4"
                    ],
                    "packages": [
                        [
                            {
                                "package_id": "60778dfa43503cdcda3636d15124c19bf6546ae3",
                                "prev": "ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                                "context": "host",
                                "binary": "Download",
                                "options": [],
                                "filenames": [],
                                "depends": [],
                                "overrides": {},
                                "build_args": null
                            }
                        ]
                    ]
                }
            ]
        ]
    }


Firstly, we can see the `zlib` package, as `libpng` depends on it. The output is sorted by
recipes as we passed with the `--order-by` argument; however, we might prefer to see it
sorted by configurations instead. For that purpouse use the `--order-by` argument with
value `configuration`.

.. code-block:: text

    $ conan graph build-order --requires=libpng/1.5.30 --format=json --order-by=configuration
    ...
    ======== Computing the build order ========
    {
        "order_by": "configuration",
        "reduced": false,
        "order": [
            [
                {
                    "ref": "zlib/1.3#06023034579559bb64357db3a53f88a4",
                    "pref": "zlib/1.3#06023034579559bb64357db3a53f88a4:d62dff20d86436b9c58ddc0162499d197be9de1e#54b9c3efd9ddd25eb6a8cbf01860b499",
                    "package_id": "d62dff20d86436b9c58ddc0162499d197be9de1e",
                    "prev": "54b9c3efd9ddd25eb6a8cbf01860b499",
                    "context": "host",
                    "binary": "Cache",
                    "options": [],
                    "filenames": [],
                    "depends": [],
                    "overrides": {},
                    "build_args": null
                }
            ],
            [
                {
                    "ref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b",
                    "pref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b:60778dfa43503cdcda3636d15124c19bf6546ae3#ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                    "package_id": "60778dfa43503cdcda3636d15124c19bf6546ae3",
                    "prev": "ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                    "context": "host",
                    "binary": "Download",
                    "options": [],
                    "filenames": [],
                    "depends": [
                        "zlib/1.3#06023034579559bb64357db3a53f88a4:d62dff20d86436b9c58ddc0162499d197be9de1e#54b9c3efd9ddd25eb6a8cbf01860b499"
                    ],
                    "overrides": {},
                    "build_args": null
                }
            ]
        ]
    }

If we now apply the ``--reduce``:

.. code-block:: text

    $ conan graph build-order --requires=libpng/1.5.30 --reduce --format=json --order-by=configuration
    ...
    ======== Computing the build order ========
    {
        "order_by": "configuration",
        "reduced": false,
        "order": []
    }

As there are no binaries to build here, all binaries already exist. If we explicitly force to build some,
the result would be only those that are going to be built:


.. code-block:: text

    $ conan graph build-order --requires=libpng/1.5.30 --build="libpng/*" --reduce --format=json --order-by=configuration
    ...
    ======== Computing the build order ========
    {
        "order_by": "configuration",
        "reduced": false,
        "order": [
            [
                {
                    "ref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b",
                    "pref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b:60778dfa43503cdcda3636d15124c19bf6546ae3#ad092d2e4aebcd9d48a5b1f3fd51ba9a",
                    "package_id": "60778dfa43503cdcda3636d15124c19bf6546ae3",
                    "prev": null,
                    "context": "host",
                    "binary": "Build",
                    "options": [],
                    "filenames": [],
                    "depends": [],
                    "overrides": {},
                    "build_args": "--require=libpng/1.5.30 --build=libpng/1.5.30"
                }
            ]
        ]
    }

Then it will contain exclusively the ``binary=Build`` nodes, but not the rest.
Note that it will also provide a ``build_args`` field with the arguments needed for a ``conan install <args>`` to fire the build of this package
in the CI agent.


**Getting a visual representation of the Build Order**

You can obtain a visual representation of the build order by using the HTML formatter. For example:

.. code-block:: text

    $ conan graph build-order --requires=opencv/4.9.0 --order-by=recipe --build=missing --format=html > build-order.html


.. image:: /images/conan-build-order-html.png
   :width: 100%
   :align: center
