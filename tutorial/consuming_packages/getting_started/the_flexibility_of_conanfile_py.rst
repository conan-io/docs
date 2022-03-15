.. _consuming_packages_getting_started_flexibility_of_conanfile_py:

Understanding the flexibility of using conanfile.py vs conanfile.txt
====================================================================

.. important::

    In this example, we will retrieve Conan packages from a Conan repository with
    packages compatible for Conan 2.0. To run this example succesfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


In the previous examples, we declared our dependencies (*Zlib* and *CMake*) in a
*conanfile.txt* file. Let's have a look at that file:

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    zlib/1.2.11

    [tool_requires]
    cmake/3.19.8

    [generators]
    CMakeDeps
    CMakeToolchain

Using a *conanfile.txt* to build your projects using Conan it's enough for simple cases,
but if you need more flexibility you should use a *conanfile.py* file where you can use
Python code to make things such as adding requirements dinamically, changing options
depending on other options or setting options for your requirements. Let's see an example
on how to migrate to a *conanfile.py* and use some of those features.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd tutorial/consuming_packages/getting_started/conanfile_py

Check the contents of the folder and note that the contents are the same that in the
previous examples but with a *conanfile.py* instead of a *conanfile.txt*.

.. code-block:: bash

    .
    ├── CMakeLists.txt
    ├── conanfile.py
    └── src
        └── main.c

Remember that in the previous examples the *conanfile.txt* had this information:

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    zlib/1.2.11

    [tool_requires]
    cmake/3.19.8

    [generators]
    CMakeDeps
    CMakeToolchain

We will translate that same information to a *conanfile.py*. This file is what is
typically called a "Conan recipe". It can be used for consuming packages, like in this
case, and also to create packages. For our current case it will define our requirements
(both libraries and build tools) and logic to modify options and set how we want to
consume those packages. In the case of using this file to create packages it can define
(among other things) how to download the package’s source code, how to build the binaries
from those sources, how to package the binaries and information for future consumers on
how to consume the package. We will later explain how to use Conan recipes to create
packages in the "Creating Packages" section.

The equivalent of the *conanfile.txt* in form of Conan recipe could look like this:

.. code-block:: python
    :caption: **conanfile.py**

    from conan import ConanFile


    class CompressorRecipe(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeToolchain", "CMakeDeps"

        def requirements(self):
            self.requires("zlib/1.2.11")
            self.tool_requires("cmake/3.19.8")


To create the Conan recipe we declared a new class that inherits from the ``ConanFile``
class and set the information defining different class attributes and methods:

* **settings** this class attribute defines the project-wide variables, like the compiler,
  its version, or the OS itself that may change when we build our project. This is related
  to how Conan manages binary compatibility as these values will affect the value of the
  package ID. We will explain how Conan uses this value to manage binary compatibility
  later.
* **generators** this class attribute specifies which Conan generators will be run when we
  call to the ``conan install`` command. In this case, as we are using CMake for building
  our project we added **CMakeToolchain** and **CMakeDeps**.
* **requirements()** in this method we can use the ``self.requires()`` and
  ``self.tool_requires()`` methods to declare all our dependencies.

You can check that running the same commands as in the previous examples will lead to the
same results as before.

.. code-block:: bash
    :caption: Windows

    $ conan install . --output-folder=build --build=missing
    $ cd build
    $ conanbuild.bat
    # assuming Visual Studio 15 2017 is your VS version and that it matches your default profile
    $ cmake .. -G "Visual Studio 15 2017" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build . --config Release
    ...
    Building with CMake version: 3.19.8
    ...
    [100%] Built target compressor
    $ Release\compressor.exe
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11
    $ deactivate_conanbuild.bat

.. code-block:: bash
    :caption: Linux, macOS
    
    $ conan install . --output-folder cmake-build-release --build=missing
    $ cd cmake-build-release
    $ source conanbuild.sh
    Capturing current environment in deactivate_conanbuildenv-release-x86_64.sh
    Configuring environment variables    
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build .
    ...
    Building with CMake version: 3.19.8
    ...
    [100%] Built target compressor
    $ ./compressor
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11
    $ source deactivate_conanbuild.sh




Read more
=========

- Importing resource files in the generate() method
- Layouts advanced use
- Conditional generators in configure()
