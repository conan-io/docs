.. _default_layout:

layouts/default
===============

This file contain information consumed by :ref:`editable packages <editable_packages>`. It is
an *.ini* file listing the directories that Conan should use for the references that are
linked to a local folder:

.. code-block:: ini

    [cool:includedirs]
    src/core/include
    src/cmp_a/include

    [*:libdirs]
    build/{settings.build_type}/{options.shared}

    [*:bindirs]
    build/{settings.build_type}/{options.shared}

Each editable package will use sections with *namespace* if any is found, otherwise it will use the
directories from the wildcarded sections. Here any reference matching ``cool/*@*/*`` will only use
the paths under the section ``[cool:includedirs]``.


.. note::

    This file has lower precedence than the one defined inside the working directory if it exists.

.. seealso::

    Check the section :ref:`editable_packages` to read more about this file.
