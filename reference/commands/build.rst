
conan build
===========


.. code-block:: bash

	$ conan build [-h] [--file FILE] [--source_folder SOURCE_FOLDER]
                   [--build_folder BUILD_FOLDER]
                   [--package_folder PACKAGE_FOLDER]
                   path

Utility command to call the build() method of a local 'conanfile.py'. The
recipe will be built in the local directory specified by --build_folder,
reading the sources from --source_folder. If you are using a build helper,
like CMake(), the --package_folder will be configured as destination folder
for the install step.



.. code-block:: bash

    positional arguments:
      path                  path to a conanfile.py, e.g., conan build .

    optional arguments:
      -h, --help            show this help message and exit
      --file FILE, -f FILE  specify conanfile filename
      --source_folder SOURCE_FOLDER, -sf SOURCE_FOLDER
                            local folder containing the sources. Defaulted to the
                            directory ofthe conanfile. A relative path can also be
                            specified (relative to the current directory)
      --build_folder BUILD_FOLDER, -bf BUILD_FOLDER
                            build folder, working directory of the build process.
                            Defaulted to the current directory. A relative path
                            can also be specified (relative to the current
                            directory)
      --package_folder PACKAGE_FOLDER, -pf PACKAGE_FOLDER
                            folder to install the package (when the build system
                            or build() method does it). Defaulted to the
                            '{build_folder}/package' folder. A relative path can
                            be specified (relative to the build_folder directory)



The ``conan build .`` and the ``build()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step in the ``conanbuildinfo.txt``.


**Examples**:


1. Build your project locally in a "build" subfolder.


.. code-block:: bash

    $ mkdir build && cd build
    $ conan install .. -p MyProfile
    $ conan build ..

Or use the ``--build_folder`` parameter:


.. code-block:: bash

    $ conan install .. -p MyProfile -cwd build
    $ conan build . --build_folder=build


2. Build your project using different folders for ``src`` and ``build``:

::

   conanfile.py
   src/
      CMakeLists.txt
      example.cpp
   build/

.. code-block:: bash

    $ conan install .. -p MyProfile -cwd build
    $ conan build . --build_folder=build --source_folder=src


3. Use an installation ``package_folder``, specially useful if you are using the ``CMake(self).install()``
build helper. It will be accesible using ``self.package_folder`` in the build() method.

.. code-block:: bash

    $ conan install .. -p MyProfile -cwd build
    $ conan build . --build_folder=build --source_folder=src --package_folder=mypackage

If ``package_folder`` parameter is not specified, but it's used in the ``build()`` method, a folder
``{build_folder}/package`` will be used automatically.



