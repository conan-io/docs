.. _consuming_packages_getting_started_tool_requires:

Using build tools as Conan packages
===================================

.. important::

    In this example, we will retrieve the CMake Conan package from a Conan repository with
    packages compatible for Conan 2.0. To run this example succesfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


In the previous example, we built our CMake project and used Conan to install and
locate the *Zlib* library. To build this example we needed to have a CMake version
installed and set in the path. But, what happens if you  don't have CMake installed in
your build environment or want to build your project with a specific CMake version
different from the one you have already installed system-wide? In this case you can
declare this dependency in Conan using a special type of requirement named
``tool_requires``. Let's see an example on how to add this kind of requirement to the
previous example and use a different CMake version to build the example. 


1. Please, first clone the sources to recreate this project, you can find them in the
   `examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

    .. code-block:: bash

        $ git clone https://github.com/conan-io/examples2.git
        $ cd tutorial/consuming_packages/getting_started/tool_requires

2. The structure of the project is the same as the one of the previous example:

.. code-block:: text

    .
    ├── conanfile.txt
    ├── CMakeLists.txt
    └── src
        └── main.c


The main difference is the addition of the **[tool_requires]** section in the
**conanfile.txt** file. In this section we are going to declare that we want to build our
application using CMake v3.16.9.

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    zlib/1.2.11

    [tool_requires]
    cmake/3.16.9

    [generators]
    CMakeDeps
    CMakeToolchain


3. Now, as in the previous example, we will use Conan to install **Zlib** and **CMake
   3.16.9** and generate the files to find the both CMake and Zlib. We will
   generate those files in the folder *cmake-build-release*. To do that, just run:

.. code-block:: bash

    $ conan install . --output-folder cmake-build-release

You can check the output:

.. code-block:: bash

    -------- Computing dependency graph ----------
    cmake/3.16.9: Not found in local cache, looking in remotes...
    cmake/3.16.9: Checking remote: conanv2
    cmake/3.16.9: Trying with 'conanv2'...
    Downloading conanmanifest.txt
    Downloading conanfile.py
    cmake/3.16.9: Downloaded recipe revision 3e3d8f3a848b2a60afafbe7a0955085a
    Graph root
        conanfile.txt: /Users/carlosz/Documents/developer/conan/examples2/tutorial/consuming_packages/getting_started/tool_requires/conanfile.txt
    Requirements
        zlib/1.2.11#f1fadf0d3b196dc0332750354ad8ab7b - Cache
    Build requirements
        cmake/3.16.9#3e3d8f3a848b2a60afafbe7a0955085a - Downloaded (conanv2)

    -------- Computing necessary packages ----------
    Requirements
        zlib/1.2.11#f1fadf0d3b196dc0332750354ad8ab7b:2a823fda5c9d8b4f682cb27c30caf4124c5726c8#48bc7191ec1ee467f1e951033d7d41b2 - Cache
    Build requirements
        cmake/3.16.9#3e3d8f3a848b2a60afafbe7a0955085a:f2f48d9745706caf77ea883a5855538256e7f2d4#6c519070f013da19afd56b52c465b596 - Download (conanv2)

    -------- Installing packages ----------

    Installing (downloading, building) binaries...
    cmake/3.16.9: Retrieving package f2f48d9745706caf77ea883a5855538256e7f2d4 from remote 'conanv2' 
    Downloading conanmanifest.txt
    Downloading conaninfo.txt
    Downloading conan_package.tgz
    Decompressing conan_package.tgz
    cmake/3.16.9: Package installed f2f48d9745706caf77ea883a5855538256e7f2d4
    cmake/3.16.9: Downloaded package revision 6c519070f013da19afd56b52c465b596
    zlib/1.2.11: Already installed!

    -------- Finalizing install (deploy, generators) ----------
    conanfile.txt: Generator 'CMakeToolchain' calling 'generate()'
    conanfile.txt: Generator 'CMakeDeps' calling 'generate()'
    conanfile.txt: Aggregating env generators

Now, if you check the *cmake-build-release* folder you will see that Conan generated a new
file called ``conanbuild.sh``. This is the result of automatically invoking a
``VirtualBuildEnv`` generator when we declared the ``tool_requires`` in the
**conanfile.txt**. This file, declares some environment variables like a new ``PATH`` that
we can use to inject to our environment the location of CMake v3.16.9.

4. Activate the virtual environment, and now you can run ``cmake --version`` to check that you
   have the installed CMake in path.

.. code-block:: bash

    $ source ./cmake-build-release/conanbuild.sh
    Capturing current environment in deactivate_conanbuildenv-release-x86_64.sh
    Configuring environment variables
    
    $ cmake --version
    cmake version 3.16.9
    ...


As you can see, after activating the environment, the CMake v3.16.9 binary folder was
added to the path and is the current active version now. Also note that when we activated
the environment another file named ``deactivate_conanbuild.sh`` was created in the same
folder. If you source this file you can restore the environment as it was before.

.. code-block:: bash

    $ source ./cmake-build-release/deactivate_conanbuild.sh
    Restoring environment
    
    $ cmake --version
    cmake version 3.22.0
    ...


Read more
---------

- Using MinGW as tool_requires...
- Using tool_requires in profiles?
