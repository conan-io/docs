
.. _info_json:


Info output
-----------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The :command:`conan info` provides a :command:`--json` parameter to generate
a file containing the output of the command.

There are several possible outputs depending on other arguments:


Build order
===========


.. warning::

    The command ``conan info --build-order`` is deprecated in favor of :ref:`conan graph build-order<conan_graph_build_order>`.


The build order printed with the argument :command:`--build-order` can be
formatted as JSON. It will show a list of lists where the references inside
each nested one can be built in parallel.

.. code-block:: json
   :caption: build_order.json

    {  
        "groups":[  
            [  
                "LibA/0.1@lasote/stable",
                "LibE/0.1@lasote/stable",
                "LibF/0.1@lasote/stable"
            ],
            [  
                "LibB/0.1@lasote/stable",
                "LibC/0.1@lasote/stable"
            ]
        ]
    }


Nodes to build
==============

When called with the argument :command:`--build` it will retrieve the list of
nodes to be built according to the build policy. Output will be just a list of
references.

.. code-block:: json
   :caption: nodes_to_build.json

    [  
        "H0/0.1@lu/st",
        "H1a/0.1@lu/st",
        "H1c/0.1@lu/st",
        "H2a/0.1@lu/st",
        "H2c/0.1@lu/st"
    ]


Info output
===========

The output of a :command:`conan info` call over a reference or a path gives information
about all the nodes involved in its build graph; the generated JSON file will
contain a list with the information for each of the nodes.

.. code-block:: json
   :caption: info.json

    [  
        {  
            "reference":"LibA/0.1@lasote/stable",
            "is_ref":true,
            "display_name":"LibA/0.1@lasote/stable",
            "id":"8da7d879f40d12efabc9a1f26ab12f1b6cafb6ad",
            "build_id":null,
            "url":"myurl",
            "license":[  
                "MIT"
            ],
            "recipe":"No remote",
            "binary":"Missing",
            "creation_date":"2019-01-29 17:22:41",
            "required_by":[  
                "LibC/0.1@lasote/stable",
                "LibB/0.1@lasote/stable"
            ]
        },
        {  
            "reference":"LibB/0.1@lasote/stable",
            "is_ref":true,
            "display_name":"LibB/0.1@lasote/stable",
            "id":"c4ec2bf350e2a02405029ab366535e26372a4f63",
            "build_id":null,
            "url":"myurl",
            "license":[  
                "MIT"
            ],
            "recipe":"No remote",
            "binary":"Missing",
            "creation_date":"2019-01-29 17:22:41",
            "required_by":[  
                "conanfile.py (LibD/0.1@None/None)"
            ],
            "requires":[  
                "LibA/0.1@lasote/stable",
                "LibE/0.1@lasote/stable"
            ]
        },
        { "...": "..."}
    ]


.. note::

    As this is a marked as *experimental*, some fields may be removed or added.
