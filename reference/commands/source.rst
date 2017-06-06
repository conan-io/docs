
conan source
============

.. code-block:: bash

   $ conan source [-h] [-f] [reference]


The ``source`` command executes a conanfile.py ``source()`` method, retrieving source code as
defined in the method, both locally, in user space or for a package in the local cache.


.. code-block:: bash

	positional arguments:
	  reference    package recipe reference. e.g., MyPackage/1.2@user/channel or
	               ./my_project/

	optional arguments:
	  -h, --help   show this help message and exit
	  -f, --force  In the case of local cache, force the removal of the source
	               folder, then the execution and retrieval of the source code.
	               Otherwise, if the code has already been retrieved, it will do
	               nothing.


The ``conan source`` and the ``source()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan source`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt

or adding ``txt`` generator to the consuming conanfile ``generators`` section


**Examples**:

- Call a local recipe's source method: In user space, the command will execute a local conanfile.py
  ``source()`` method, in the current directory.

.. code-block:: bash

   $ conan source ../mysource_folder


- Call a cached recipe's source method: In the conan local cache, it will execute the recipe ``source()`` ,
  in the corresponding ``source`` folder, as defined by the local cache layout.
  This command is useful for retrieving such source code before launching multiple concurrent package builds,
  that could otherwise collide in the source code retrieval process.

.. code-block:: bash

   $ conan source Pkg/0.2@user/channel


