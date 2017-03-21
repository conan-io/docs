
conan package
=============


.. code-block:: bash

   $ conan package [-h] reference [package]


Calls your conanfile.py ``package()`` method for a specific package recipe.
Intended for package creators, for regenerating a package without recompiling
the source, i.e. for troubleshooting, and fixing the ``package()`` method, not
normal operation.

It requires that the package has been built locally, it won't
re-package otherwise. When used in a user space project, it
will execute from the build folder specified as parameter, and the current
directory. This is useful while creating package recipes or just for
extracting artifacts from the current project, without even being a package

This command also works locally, in the user space, and it will copy artifacts from the provided
folder to the current one.

.. code-block:: bash

    positional arguments:
	  reference   package recipe reference e.g. MyPkg/0.1@user/channel, or local
	              path to the build folder (relative or absolute)
	  package     Package ID to regenerate. e.g.,
	              9cf83afd07b678d38a9c1645f605875400847ff3 This optional parameter
	              is only used for the local conan cache. If not specified, ALL binaries
	              for this recipe are re-packaged

The ``conan package`` and the ``package()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan package`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt

or adding  ``txt`` generator to the consuming conanfile ``generators`` section


**Examples**


- Copy artifacts from the provided ``build`` folder to the current one:

.. code-block:: bash

   $ conan package ../build


- Copy the artifacts from the build directory to package directory in the local cache:


.. code-block:: bash

	$ conan package MyPackage/1.2@user/channel 9cf83afd07b678da9c1645f605875400847ff3


.. note::

    Conan package command won't create a new package, use ``install`` or ``test_package`` instead for
    creating packages in the conan local cache, or ``build`` for conanfile.py in user space.

