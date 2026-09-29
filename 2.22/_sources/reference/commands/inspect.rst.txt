.. _reference_commands_inspect:

conan inspect
=============

.. include:: ../../common/experimental_warning.inc

.. autocommand::
    :command: conan inspect -h


The :command:`conan inspect` command shows the public attributes of any recipe (`conanfile.py`) as follows:

.. code-block:: text

    $ conan inspect .
    default_options:
        shared: False
        fPIC: True
        neon: True
        msa: True
        sse: True
        vsx: True
        api_prefix:
    description: libpng is the official PNG file format reference library.
    generators: []
    homepage: http://www.libpng.org
    label:
    license: libpng-2.0
    name: libpng
    options:
        api_prefix:
        fPIC: True
        msa: True
        neon: True
        shared: False
        sse: True
        vsx: True
    options_definitions:
        shared: ['True', 'False']
        fPIC: ['True', 'False']
        neon: ['True', 'check', 'False']
        msa: ['True', 'False']
        sse: ['True', 'False']
        vsx: ['True', 'False']
        api_prefix: ['ANY']
    package_type: None
    requires: []
    revision_mode: hash
    settings: ['os', 'arch', 'compiler', 'build_type']
    topics: ['png', 'graphics', 'image']
    url: https://github.com/conan-io/conan-center-index


``conan inspect`` evaluates recipe methods such as ``set_name()`` and ``set_version()``,
and is capable of resolving ``python_requires`` dependencies (which can be locked with the ``--lockfile`` argument),
so its base methods will also be properly executed.

.. note::
    The ``--remote`` argument is used *only* for fetching remote ``python_requires`` in cases where they are needed,
    **not** to inspect recipes from a remote. Use :ref:`conan graph info<reference_graph_info>` for such cases.


The :command:`conan inspect ... --format=json` returns a JSON output format in ``stdout`` (which can be redirected to a file) with the following structure:

.. code-block:: text

    $ conan inspect . --format=json
    {
        "name": "libpng",
        "url": "https://github.com/conan-io/conan-center-index",
        "license": "libpng-2.0",
        "description": "libpng is the official PNG file format reference library.",
        "homepage": "http://www.libpng.org",
        "revision_mode": "hash",
        "default_options": {
            "shared": false,
            "fPIC": true,
            "neon": true,
            "msa": true,
            "sse": true,
            "vsx": true,
            "api_prefix": ""
        },
        "topics": [
            "png",
            "graphics",
            "image"
        ],
        "package_type": "None",
        "settings": [
            "os",
            "arch",
            "compiler",
            "build_type"
        ],
        "options": {
            "api_prefix": "",
            "fPIC": "True",
            "msa": "True",
            "neon": "True",
            "shared": "False",
            "sse": "True",
            "vsx": "True"
        },
        "options_definitions": {
            "shared": [
                "True",
                "False"
            ],
            "fPIC": [
                "True",
                "False"
            ],
            "neon": [
                "True",
                "check",
                "False"
            ],
            "msa": [
                "True",
                "False"
            ],
            "sse": [
                "True",
                "False"
            ],
            "vsx": [
                "True",
                "False"
            ],
            "api_prefix": [
                "ANY"
            ]
        },
        "generators": [],
        "requires": [],
        "source_folder": null,
        "build_folder": null,
        "generators_folder": null,
        "package_folder": null,
        "label": ""
    }

.. note::
    ``conan inspect`` does not list any requirements listed in the ``requirements()`` method,
    only those present in the ``requires`` attribute will be shown.
