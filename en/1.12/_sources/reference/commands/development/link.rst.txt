
.. _conan_link:

conan link
==========

.. code-block:: bash

    $ usage: conan link [-h] [--remove] [-l LAYOUT] [target] reference


Links a conan reference (e.g ``lib/1.0@conan/stable``) with a local folder path.

.. code-block:: text

    positional arguments:
    target                Path to the package folder in the user workspace
    reference             Reference to link. e.g.: mylib/1.X@user/channel

    optional arguments:
    -h, --help            show this help message and exit
    --remove              Remove linked reference (target not required)
    -l LAYOUT, --layout LAYOUT
                            Relative or absolute path to a file containing the
                            layout. Relative paths will be resolved first relative
                            to current dir, then to local cache "layouts" folder

This command puts a package in :ref:`"Editable mode" <editable_packages>`, and consumers of this package will use
it from the given user folder instead of using it from the cache.
The path pointed by ``target`` should exist and contain a ``conanfile.py``.


**Examples**:

- Put the package ``cool/version@user/dev`` in editable mode, using the layout specified by
  the file ``win_layout``.

.. code-block:: bash

    $ conan link . cool/version@user/dev --layout=win_layout


- Remove the "Editable mode", use again package from the cache:

.. code-block:: bash

    $ conan link --remove cool/version@user/dev
