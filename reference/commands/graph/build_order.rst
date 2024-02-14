conan graph build-order
=======================

.. autocommand::
    :command: conan graph build-order -h


The ``conan graph build-order`` command computes build order of the dependency graph for the recipe specified in ``path``.

Let's consider installing `libpng` and wanting to see the build order for this requirement:

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
recipes by default; however, we might prefer to see it sorted by configurations instead.
For that purpouse use the `--order-by` argument (that takes the value `recipe` by
default). Please, note that the `--order-by` argument will be mandatory in upcoming
releases as the absence of it will be deprecated.

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

