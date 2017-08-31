
conan export
============


.. code-block:: bash

	$ conan export [-h] [--path PATH] [--keep-source] [--file FILE] reference

Copies the package recipe (conanfile.py and associated files) to your local
cache. From the local cache it can be shared and reused in other projects.
Also, from the local cache, it can be uploaded to any remote with the "upload"
command.


.. code-block:: bash


    positional arguments:
    reference             a full package reference Pkg/version@user/channel, or
                          just the user/channel if package and version are
                          defined in recipe

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Optional. Folder with a conanfile.py. Default current
                            directory.
      --keep-source, -k     Optional. Do not remove the source folder in the local
                            cache. Use for testing purposes only
      --file FILE, -f FILE  specify conanfile filename


The ``export`` command will run a linting of the package recipe, looking for possible inconsistencies, bugs and py2-3 incompatibilities. It is possible to customize the rules for this linting, as well as totally disabling it. Look at the ``recipe_linter`` and ``pylintrc`` variables in :ref:`conan.conf<conan_conf>` and the ``PYLINTRC`` environment variable.


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

