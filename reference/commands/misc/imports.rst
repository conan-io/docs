

conan imports
=============

.. code-block:: bash

   $ conan imports [-h] [--file FILE] [-d DEST]
                   [--install-folder INSTALL_FOLDER] [-u]
                   path



Calls your local conanfile.py or conanfile.txt 'imports' method. It requires
to have been previously installed and have a conanbuildinfo.txt generated file
in the --install-folder (defaulted to current directory).


.. code-block:: bash

	positional arguments:
	  reference             Specify the location of the folder containing the
	                        conanfile. By default it will be the current directory.
	                        It can also use a full reference e.g.
	                        MyPackage/1.2@user/channel and the recipe
	                        'imports()' for that package in the local conan cache
	                        will be used

	optional arguments:
	  -h, --help            show this help message and exit
	  --file FILE, -f FILE  Use another filename, e.g.: conan imports
	                        -f=conanfile2.py
	  -d DEST, --dest DEST  Directory to copy the artifacts to. By default it will
	                        be the current directory
	  -u, --undo            Undo imports. Remove imported files


The ``imports()`` method might use `settings`, `options` and `environment variables` from the specified
profile and dependencies information from the declared ``deps_XXX_info`` objects in the conanfile
requirements.
All that information is saved automatically in the ``conaninfo.txt`` and ``conanbuildinfo.txt``
files respectively, when you run the ``conan install`` command.
Those files have to be located in the specified ``--install-folder``.



**Examples**

- Execute the ``imports()`` method for a package in the local cache:


.. code-block:: bash

   $ conan imports MyPackage/1.2@user/channel


- Import files from a current conanfile in current directory:

.. code-block:: bash

   $ conan install --no-imports -g txt # Creates the conanbuildinfo.txt
   $ conan imports


- Remove the copied files (undo the import):


.. code-block:: bash

   $ conan imports --undo
