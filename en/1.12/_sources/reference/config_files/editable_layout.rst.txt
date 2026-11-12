.. _editable_layout:

Editable layout files
=====================

This file contain information consumed by :ref:`editable packages <editable_packages>`. It is
an *.ini* file listing the directories that Conan should use for the packages that are opened
in editable mode:

.. code-block:: ini

    # Affects to all packages but cool/version@user/dev
    [includedirs]
    src/include

    # using placeholders from conan settings and options
    [libdirs]
    build/{settings.build_type}/{settings.arch}

    [bindirs]
    build/{settings.build_type}/{settings.arch}

    # Affects only to cool/version@user/dev
    [cool/version@user/dev:includedirs]
    src/core/include
    src/cmp_a/include


The specific sections using a package reference will have higher priority than the general ones.


This file can live in the conan cache, in the ``.conan/layouts`` folder, or in a user folder, like
inside the source repo.

If there exists a ``.conan/layouts/default`` layout file in the cache and no layout file is specified
in the ``conan link <path> <reference>`` command, that file will be used.


.. seealso::

    Check the section :ref:`editable_packages` to read more about this file.
