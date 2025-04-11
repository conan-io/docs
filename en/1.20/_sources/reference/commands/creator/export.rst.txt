
.. _conan_export:

conan export
============

.. code-block:: bash

    $ conan export [-h] [-k] [-l [LOCKFILE]] [--ignore-dirty]
                   path [reference]

Copies the recipe (conanfile.py & associated files) to your local cache.

Use the 'reference' param to specify a user and channel where to export
it. Once the recipe is in the local cache it can be shared, reused and
to any remote with the 'conan upload' command.

.. code-block:: text

    positional arguments:
      path                  Path to a folder containing a conanfile.py or to a
                            recipe file e.g., my_folder/conanfile.py
      reference             user/channel, or Pkg/version@user/channel (if name and
                            version are not declared in the conanfile.py

    optional arguments:
      -h, --help            show this help message and exit
      -k, -ks, --keep-source
                            Do not remove the source folder in local cache, even
                            if the recipe changed. Use this for testing purposes
                            only
      -l [LOCKFILE], --lockfile [LOCKFILE]
                            Path to a lockfile or folder containing 'conan.lock'
                            file. Lockfile will be updated with the exported
                            package
      --ignore-dirty        When using the "scm" feature with "auto" values,
                            capture the revision and url even if there are
                            uncommitted changes


The ``reference`` field can be:

- A complete package reference: ``pkg/version@user/channel``. In this case, the recipe doesn't need
  to declare the name or the version. If the recipe declares them, they should match the provided values
  in the command line.
- The user and channel: ``user/channel``. The command will assume that the name and version are provided
  by the recipe.
- The version, user and channel: ``version@user/channel``. The recipe must provide the name, and if it
  does provide the version, it should match the command line one.

The ``export`` command will run a linting of the package recipe, looking for possible
inconsistencies, bugs and py2-3 incompatibilities. It is possible to customize the rules for this
linting, as well as totally disabling it. Look at the ``recipe_linter`` and ``pylintrc`` variables
in :ref:`conan.conf<conan_conf>` and the ``PYLINTRC`` environment variable.

**Examples**

- Export a recipe using a full reference. Only valid if ``name`` and ``version`` are not declared in
  the recipe:

  .. code-block:: bash

      $ conan export . mylib/1.0@myuser/channel

- Export a recipe from any folder directory, under the ``myuser/stable`` user and channel:

  .. code-block:: bash

      $ conan export ./folder_name myuser/stable

- Export a recipe without removing the source folder in the local cache:

  .. code-block:: bash

      $ conan export . fenix/stable -k
