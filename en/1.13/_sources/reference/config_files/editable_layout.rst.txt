.. _editable_layout:

Editable layout files
=====================

This file contain information consumed by :ref:`editable packages <editable_packages>`. It is
an *.ini* file listing the directories that Conan should use for the packages that are opened
in editable mode. Before parsing this file Conan runs Jinja2 template engine with the
``settings``, ``options`` and ``reference`` objects, so you can add *any* logic to this files:

.. code-block:: ini

    # Affects to all packages but cool/version@user/dev
    [includedirs]
    src/include

    # using placeholders from conan settings and options
    [libdirs]
    build/{{settings.build_type}}/{{settings.arch}}

    [bindirs]
    {% if options.shared %}
    build/{{settings.build_type}}/shared
    {% else %}
    build/{{settings.build_type}}/static
    {% endif %}

    # Affects only to cool/version@user/dev
    [cool/version@user/dev:includedirs]
    src/core/include
    src/cmp_a/include

    # The source_folder, build_folder are useful for workspaces
    [source_folder]
    src

    [build_folder]
    build/{{settings.build_type}}/{{settings.arch}}


The specific sections using a package reference will have higher priority than the general ones.


This file can live in the conan cache, in the ``.conan/layouts`` folder, or in a user folder, like
inside the source repo.

If there exists a ``.conan/layouts/default`` layout file in the cache and no layout file is specified
in the :command:`conan editable add <path> <reference>` command, that file will be used.

The ``[source_folder]`` and ``[build_folder]`` are useful for workspaces. For example, when using ``cmake``
workspace-generator, it will locate the ``CMakeLists.txt`` of each package in editable mode in the
``[source_folder]`` and it will use the ``[build_folder]`` as the base folder for the build temporary files.


.. seealso::

    Check the section :ref:`editable_packages` and :ref:`workspaces` to learn more about this file.
