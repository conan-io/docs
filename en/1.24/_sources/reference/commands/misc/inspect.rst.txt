
.. _conan_inspect:

conan inspect
=============

.. warning::

      This is an **experimental** feature subject to breaking changes in future releases.

.. code-block:: bash

    $ conan inspect [-h] [-a [ATTRIBUTE]] [-r REMOTE] [-j JSON] [--raw RAW]
                    path_or_reference

Displays conanfile attributes, like name, version and options. Works locally,
in local cache and remote.

.. code-block:: text

    positional arguments:
      path_or_reference     Path to a folder containing a recipe (conanfile.py) or
                            to a recipe file. e.g., ./my_project/conanfile.py. It
                            could also be a reference

    optional arguments:
      -h, --help            show this help message and exit
      -a [ATTRIBUTE], --attribute [ATTRIBUTE]
                            The attribute to be displayed, e.g "name"
      -r REMOTE, --remote REMOTE
                            look in the specified remote server
      -j JSON, --json JSON  json output file
      --raw RAW             Print just the value of the requested attribute


Examples:

.. code-block:: bash

    $ conan inspect zlib/1.2.11@ -a=name -a=version -a=options -a default_options -r=conan-center
    name: zlib
    version: 1.2.11
    options
        shared: [True, False]
    default_options: shared=False

.. code-block:: bash

    $ conan inspect zlib/1.2.11@ -a=license -a=url
    license: Zlib
    url: https://github.com/conan-io/conan-center-index

.. code-block:: bash

    $ conan inspect zlib/1.2.11@ --raw=settings
    ('os', 'arch', 'compiler', 'build_type')


If no specific attributes are defined via ``-a``, then, some default attributes will be displayed:

.. code-block:: bash

    $ conan inspect zlib/1.2.11@
    name: zlib
    version: 1.2.11
    url: https://github.com/conan-io/conan-center-index
    homepage: https://zlib.net
    license: Zlib
    author: None
    description: A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)
    topics: None
    generators: cmake
    exports: None
    exports_sources: ['CMakeLists.txt', 'CMakeLists_minizip.txt', 'minizip.patch']
    short_paths: False
    apply_env: True
    build_policy: None
    revision_mode: hash
    settings: ('os', 'arch', 'compiler', 'build_type')
    options:
        fPIC: [True, False]
        minizip: [True, False]
        shared: [True, False]
    default_options:
        fPIC: True
        minizip: False
        shared: False
