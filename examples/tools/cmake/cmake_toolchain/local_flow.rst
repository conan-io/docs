CMakeToolchain in the developer flow
====================================


One of the advantages of using Conan toolchains is that they can help to achieve the same build
with local development flows, as if the package is created in the cache.


Let's create a basic project based on the template ``cmake_lib`` as an example of a C++ project:

.. code:: bash

    $ conan new -d name=foo -d version=1.0 cmake_lib


Generating the toolchain
------------------------

The recipe from our project declares the generator "CMakeToolchain".

We can call :command:`conan install` to install both ``Release`` and ``Debug`` configurations.
The ``conan_toolchain.cmake`` is common for both configurations and located at *build/generators* folder:

.. code:: bash

    $ conan install .
    $ conan install . -s build_type=Debug


.. note::

    The `build/generators` location is declared by the ``cmake_layout()`` in the ``layout()`` method.


Building the project
--------------------


If you are using a multi-configuration generator:

.. code:: bash

    $ cd build
    $ cmake .. -G "Visual Studio 15" -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake
    # Now you can open the IDE, select Debug or Release config and build
    # or, in the command line
    $ cmake --build . --config Release
    $ cmake --build . --config Debug


**NOTE**: The platform (Win64), is already encoded in the toolchain. The command line shouldn't pass it, so using
``-G "Visual Studio 15"`` instead of the ``-G "Visual Studio 15 Win64"``


If you are using a single-configuration generator:

.. code:: bash

    $ cd build
    $ cmake ..  -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .


Building the project using ``CMakePresets``
-------------------------------------------


A ``CMakeUserPresets.json`` file is generated in the same folder of your ``CMakeLists.txt`` file,
so you can use the ``--preset`` argument from ``cmake >= 3.23`` or use an IDE. The ``CMakeUserPresets.json`` is
including the ``CMakePresets.json`` file located at the ``build/generators`` folder.

The ``CMakePresets.json`` contain information about the ``conan_toolchain.cmake`` location and even the ``binaryDir``
set with the output directory.


If you are using a multi-configuration generator:

.. code:: bash

    $ cmake --preset default
    $ cmake --build --preset Debug
    $ cmake --build --preset Release


If you are using a single-configuration generator:

.. code:: bash

    $ cmake --preset Debug
    $ cmake --build --preset Debug
    $ cmake --preset Release
    $ cmake --build --preset Release

