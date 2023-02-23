.. _reference_commands_inspect:

conan inspect
=============

.. include:: ../../common/experimental_warning.inc

.. code-block:: text

    $ conan inspect -h
    usage: conan inspect [-h] [-f FORMAT] [-v [V]] [--logger] path

    Inspect a conanfile.py to return its public fields.

    positional arguments:
      path                  Path to a folder containing a recipe (conanfile.py)

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.

.. note::

    ``conan inspect`` doesn't really evaluate any methods or apply any conditional logic. It lists class attributes only.

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
    license: libpng-2.0
    name: libpng
    no_copy_source: False
    options:
        shared: [True, False]
        fPIC: [True, False]
        neon: [True, 'check', False]
        msa: [True, False]
        sse: [True, False]
        vsx: [True, False]
        api_prefix: ['ANY']
    revision_mode: hash
    settings: ('os', 'arch', 'compiler', 'build_type')
    topics: ('png', 'graphics', 'image')
    url: https://github.com/conan-io/conan-center-index

The :command:`conan inspect ... --format=json` returns a JSON output format in ``stdout`` (which can be redirected to a file) with the following structure:

.. code-block:: text

    $ conan inspect -f json .
    {
        "author": null,
        "build_policy": null,
        "build_requires": null,
        "buildenv_info": null,
        "channel": null,
        "conf_info": null,
        "cpp": null,
        "default_options": {
            "shared": false,
            "fPIC": true,
            "neon": true,
            "msa": true,
            "sse": true,
            "vsx": true,
            "api_prefix": ""
        },
        "deprecated": null,
        "description": "libpng is the official PNG file format reference library.",
        "exports": null,
        "exports_sources": null,
        "generators": [],
        "homepage": "http://www.libpng.org",
        "license": "libpng-2.0",
        "name": "libpng",
        "no_copy_source": false,
        "options": {
            "shared": [
                true,
                false
            ],
            "fPIC": [
                true,
                false
            ],
            "neon": [
                true,
                "check",
                false
            ],
            "msa": [
                true,
                false
            ],
            "sse": [
                true,
                false
            ],
            "vsx": [
                true,
                false
            ],
            "api_prefix": [
                "ANY"
            ]
        },
        "package_type": null,
        "provides": null,
        "recipe_folder": null,
        "requires": null,
        "revision_mode": "hash",
        "runenv_info": null,
        "settings": [
            "os",
            "arch",
            "compiler",
            "build_type"
        ],
        "test_requires": null,
        "tested_reference_str": null,
        "tool_requires": null,
        "topics": [
            "png",
            "graphics",
            "image"
        ],
        "upload_policy": null,
        "url": "https://github.com/conan-io/conan-center-index",
        "user": null,
        "version": null,
        "win_bash": null,
        "win_bash_run": null
    }
