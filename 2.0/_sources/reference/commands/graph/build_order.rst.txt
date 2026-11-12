conan graph build-order
=======================

.. autocommand::
    :command: conan graph build-order -h


The ``conan graph build-order`` command computes build order of the dependency graph for the recipe specified in ``path``.


**Example**:

Let's think of installing `libpng`, and we want to see the build order for this requirement:

.. code-block:: text

    $ conan graph build-order --requires libpng/1.5.30 --format json
    ...
    ======== Computing the build order ========
    [
        [
            {
                "ref": "zlib/1.3#5c0f3a1a222eebb6bff34980bcd3e024",
                "depends": [],
                "packages": [
                    [
                        {
                            "package_id": "be7ccd6109b8a8f9da81fd00ee143a1f5bbd5bbf",
                            "prev": null,
                            "context": "host",
                            "binary": "Missing",
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
                    "zlib/1.3#5c0f3a1a222eebb6bff34980bcd3e024"
                ],
                "packages": [
                    [
                        {
                            "package_id": "235f6d8c648e7c618d86155a8c3c6efb96d61fa1",
                            "prev": null,
                            "context": "host",
                            "binary": "Missing",
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

At first place, we can see the ``zlib`` package as ``libpng`` depends on it. That output is ordered by recipes by default, but
we could want to see it ordered by configurations instead:

.. code-block:: text

    $ conan graph build-order --requires libpng/1.5.30 --format json --order configuration
    ...
    ======== Computing the build order ========
    [
        [
            {
                "ref": "zlib/1.3#5c0f3a1a222eebb6bff34980bcd3e024",
                "pref": "zlib/1.3#5c0f3a1a222eebb6bff34980bcd3e024:be7ccd6109b8a8f9da81fd00ee143a1f5bbd5bbf",
                "package_id": "be7ccd6109b8a8f9da81fd00ee143a1f5bbd5bbf",
                "prev": null,
                "context": "host",
                "binary": "Missing",
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
                "pref": "libpng/1.5.30#ed8593b3f837c6c9aa766f231c917a5b:235f6d8c648e7c618d86155a8c3c6efb96d61fa1",
                "package_id": "235f6d8c648e7c618d86155a8c3c6efb96d61fa1",
                "prev": null,
                "context": "host",
                "binary": "Missing",
                "options": [],
                "filenames": [],
                "depends": [
                    "zlib/1.3#5c0f3a1a222eebb6bff34980bcd3e024:be7ccd6109b8a8f9da81fd00ee143a1f5bbd5bbf"
                ],
                "overrides": {},
                "build_args": null
            }
        ]
    ]
