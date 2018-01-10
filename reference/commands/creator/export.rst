
conan export
============


.. code-block:: bash

	$ conan export [-h] [--path PATH] [--file FILE] [--keep-source] reference

Copies the recipe (conanfile.py & associated files) to your local cache. Use
the 'reference' param to specify a user and channel where to export. Once the
recipe is in the local cache it can be shared and reused. It can be uploaded
to any remote with the "conan upload" command.


.. code-block:: bash


    positional arguments:
      reference             user/channel, or a full package reference
                            (Pkg/version@user/channel), if name and version are
                            not declared in the recipe

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Optional. Folder with a conanfile.py. Default current
                            directory.
      --file FILE, -f FILE  specify conanfile filename
      --keep-source, -k     Optional. Do not remove the source folder in the local
                            cache. Use for testing purposes only


The ``export`` command will run a linting of the package recipe, looking for possible inconsistencies, bugs and py2-3 incompatibilities.
It is possible to customize the rules for this linting, as well as totally disabling it.
Look at the ``recipe_linter`` and ``pylintrc`` variables in :ref:`conan.conf<conan_conf>` and the ``PYLINTRC`` environment variable.


**Examples**


- Export a recipe using a full reference. Only valid if ``name`` and ``version`` are not declared in the recipe:

.. code-block:: bash

	$ conan export mylib/1.0@myuser/channel


- Export a recipe from any folder directory, under the ``myuser/stable`` user and channel:

.. code-block:: bash

	$ conan export ./folder_name myuser/stable


- Export a recipe without removing the source folder in the local cache:

.. code-block:: bash

	$ conan export fenix/stable -k

