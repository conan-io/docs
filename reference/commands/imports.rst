

conan imports
=============

.. code-block:: bash

   $ conan imports [-h] [--file FILE] [-d DEST] [-u] [reference]



Execute the ``imports`` stage of a conanfile.txt or a conanfile.py. It requires
to have been previously installed it and have a ``conanbuildinfo.txt`` generated file.

The ``imports`` functionality needs a ``conanbuildinfo.txt`` file, so it has
to be generated with a previous ``conan install`` either specifying it in the conanfile, or as
a command line parameter. It will generate a manifest file called ``conan_imports_manifests.txt``
with the files that have been copied from conan local cache to user space.


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

The ``conan imports`` and the ``imports()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan imports`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt

or adding ``txt`` generator to the consuming conanfile ``generators`` section



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
