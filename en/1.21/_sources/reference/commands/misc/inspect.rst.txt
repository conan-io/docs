
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

    $ conan inspect zlib/1.2.11@conan/stable -a=name -a=version -a=options -a default_options -r=conan-center
    name: zlib
    version: 1.2.11
    options
        shared: [True, False]
    default_options: shared=False

.. code-block:: bash

    $ conan inspect zlib/1.2.11@conan/stable -a=license -a=url
    license: http://www.zlib.net/zlib_license.html
    url: http://github.com/conan-community/conan-zlib

.. code-block:: bash

    $ conan inspect zlib/1.2.11@conan/stable --raw=settings
    ('os', 'arch', 'compiler', 'build_type')


If no specific attributes are defined via ``-a``, then, some default attributes will be displayed:

.. code-block:: bash

    $ conan inspect zlib/1.2.11@conan/stable
    name: zlib
    version: 1.2.11
    url: http://github.com/conan-community/conan-zlib
    license: http://www.zlib.net/zlib_license.html
    author: None
    description: A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)
    generators: cmake
    exports: None
    exports_sources: ['CMakeLists.txt']
    short_paths: False
    apply_env: True
    build_policy: None
    topics: None
    settings: ('os', 'arch', 'compiler', 'build_type')
    options:
        shared: [True, False]
    default_options:
        shared: False