
conan package
=============


.. code-block:: bash

   $ conan package [-h] [--build_folder BUILD_FOLDER]
                     [--source_folder SOURCE_FOLDER]
                     reference [package_id]


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
			reference             package recipe reference e.g. MyPkg/0.1@user/channel,
                            or local path to the build folder (relative or
                            absolute)
			package_id            Package ID to regenerate. e.g.,
                            9cf83afd07b678d38a9c1645f605875400847ff3 This optional
                            parameter is only used for the local conan cache. If
                            not specified, ALL binaries for this recipe are re-
                            packaged

		optional arguments:
			-h, --help            show this help message and exit
			--build_folder BUILD_FOLDER, -bf BUILD_FOLDER
                            local folder containing the build
			--source_folder SOURCE_FOLDER, -sf SOURCE_FOLDER
                            local folder containing the sources


This command has 2 different modes:

- Cache mode: When used providing a full package reference, like ``conan package Pkg/0.1@user/channel``, it will work in the local conan cache, re-packaging from the cache "build" folder to the cache "package" folder. The ``package_id`` argument only makes sense in this mode, while the other arguments are not used. This mode is used mainly by package creators to debug a package recipe that might not be packaging as expected, and a re-build of the binaries is not wanted, because they are debugging the ``package()`` recipe method.

- Local mode: When a full package reference is not provided, the ``package`` command works in user space, and the ``reference`` argument refers to a local path, can be relative to the current directory, or absolute. In this mode, the ouput package is created in the current directory, i.e. a user folder. This directory cannot be the same as the directory. This mode requires a ``conanfile.py`` file that has been previously "installed" with ``conan install``. Such command will generate a ``conaninfo.txt`` file with all the configuration, settings/options, which is assumed to be the configuration of the binary being packaged.


The ``conan package`` and the ``package()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan package`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt

or adding  ``txt`` generator to the consuming conanfile ``generators`` section.


**Examples cache mode**

- Copy the artifacts from the build directory to package directory in the local cache, for that specific package 9cf8...7ff3:

.. code-block:: bash

	$ conan package MyPackage/1.2@user/channel 9cf83afd07b678da9c1645f605875400847ff3

- Copy the artifacts from the build directory to package directory in the local cache, for all variants of the package that have been built in the local cache:

.. code-block:: bash

	$ conan package MyPackage/1.2@user/channel


**Examples local mode**

This example shows how ``package`` works in a package which can be edited and built in user folders instead of the local cache.

.. code-block:: bash

	$ conan new Hello/0.1 -s
	$ conan install
	$ conan build . # You can also use your build system to build your code
	$ mkdir mypkg && cd mypkg # assume we are in the conanfile.py folder
	$ conan package .. # Will package from the conanfile.py folder
	# Now in the current dif "mypkg" we have the final package
	$ ls
	> conaninfo.txt  conanmanifest.txt  include/  lib/

The above is not really recommended, because it will clutter the recipe folder with all temporary build files. It is better to create a "build" folder where to put them:

.. code-block:: bash

	$ conan new Hello/0.1 -s
	$ mkdir build && cd build
	$ conan install ..
	$ conan build ..
	$ cd ..
	$ mkdir mypkg && cd mypkg
	$ conan package .. --build_folder=../build
	# Same result as above

This process can be repated cleanly for many different configurations (release/debug, 32/64), just by creating different folders like "build_release_32" and "pkg_release_32" both for the build and the final package.

If you have the source code in a different folder than the recipe (as when you have the recipe in a separate repository, and it uses the ``source()`` method to retrieve the source code), you can also specify it:

.. code-block:: bash

	$ conan new Hello/0.1 -s
	# simulate the different source folder, moving the src folder
	$ mkdir sources && mv src sources
	$ mkdir build && cd build
	$ conan install ..
	$ conan build .. --source_folder=../sources
	$ cd ..
	$ mkdir mypkg && cd mypkg
	$ conan package .. --build_folder=../build --source_folder=../sources
	# Same result as above

.. note::

	The packages created locally are just for the user, but cannot be directly consumed by other packages, nor they can be uploaded to a remote repository. In order to make these packages available to the system, they have to be put in the conan local cache, which can be done with the ``conan package_files`` command.
