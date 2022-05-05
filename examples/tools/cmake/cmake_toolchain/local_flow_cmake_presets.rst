CMakeToolchain using CMakePresets
=================================

.. note::

    You can find the following example in this repository

    .. code-block:: bash

        $ git clone https://github.com/conan-io/examples2.git
        $ cd examples2/examples/tools/cmake/cmake_toolchain/local_flow_cmake_presets


One of the advantages of using Conan toolchains is that they can help to achieve the same build
with local development flows, as if the package is created in the cache.


Let's create a basic project based on the template ``cmake_exe`` as an example of a C++ project:

.. code:: bash

    $ conan new -d name=foo -d version=1.0 cmake_exe


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
    $ build\Debug\foo.exe
    foo/1.0: Hello World Release!

    $ cmake --build --preset Release
    $ build\Release\foo.exe
    foo/1.0: Hello World Release!


If you are using a single-configuration generator:

.. code:: bash

    $ cmake --preset Debug
    $ cmake --build --preset Debug
    $ ./cmake-build-debug/foo
    foo/1.0: Hello World Debug!


    $ cmake --preset Release
    $ cmake --build --preset Release
    $ ./cmake-build-release/foo
    foo/1.0: Hello World Release!

