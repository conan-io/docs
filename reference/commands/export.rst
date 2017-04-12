
conan export
============


.. code-block:: bash

	$ conan export [-h] [--path PATH] [--keep-source] [--file FILE] user

Copies the package recipe (conanfile.py and associated files) to your local cache.
From the local cache it can be shared and reused in other projects.
Also, from the local cache, it can be uploaded to any remote with the "upload" command.


.. code-block:: bash


    positional arguments:
      user                  user_name[/channel]. By default, channel is "testing",
                            e.g., phil or phil/stable

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Optional. Folder with a conanfile.py. Default current
                            directory.
      --keep-source, -k     Optional. Do not remove the source folder in the local
                            cache. Use for testing purposes only
      --file FILE, -f FILE  specify conanfile filename




**Examples**


- Export a recipe from the current directory, under the ``myuser/testing`` user and channel:

.. code-block:: bash

	$ conan export myuser


- Export a recipe from any folder directory, under the ``myuser/stable`` user and channel:

.. code-block:: bash

	$ conan export ./folder_name myuser/stable


- Export a recipe without removing the source folder in the local cache:

.. code-block:: bash

	$ conan export fenix/stable -k

