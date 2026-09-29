.. _workspaces:

Workspaces [experimental]
=========================

.. warning::

    This is an experimental feature. It is actually a preview of the feature, with the main goal of receiving feedback and improving it.
    Consider the file formats, commands and flows to be unstable and subject to changes in the next releases.

Sometimes, it is necessary to work on more than one package simultaneously. In theory, each package should be a distinct "work unit", and developers
should be able to work on them in isolation. However, some changes require modifications in more than one package at the same time.
The local development flow can help, but it still requires using ``export-pkg`` to put the artifacts in the local cache, where other packages
under development can consume them.

Conan Workspaces allow having more than one package in user folders, and have them directly use other packages from user folders
without having to put them in the local cache.

Let's introduce Workspaces with a practical example:

.. code-block:: bash

    $ git clone https://github.com/memsharded/conan-workspace-example.git
    $ cd conan-workspace-example

Note that this folder contains a *conanws.yml* file in the root, with the following contents:

.. code-block:: text

    HelloB:
        folder: B
        includedirs: src
        cmakedir: src
    HelloC:
        folder: C
        includedirs: src
        cmakedir: src
    HelloA:
        folder: A
        cmakedir: src

    root: HelloA
    generator: cmake
    name: MyProject


Next, run a :command:`conan install` as usual, using a *build* folder to output the dependencies information:

.. code-block:: bash

    $ conan install . -if=build
    Using conanws.yml file from C:\Users\<youruser>\conan-workspace-example
    Workspace: Installing...
    Requirements
        HelloA/root@project/develop from 'conanws.yml'
        HelloB/0.1@user/testing from 'conanws.yml'
        HelloC/0.1@user/testing from 'conanws.yml'
    Packages
        HelloA/root@project/develop:8a1ff0ad9a2a372996a26ff4136faa83268b5442
        HelloB/0.1@user/testing:e5affb0ca4e5d6998c29f435daf78ab20ef50be5
        HelloC/0.1@user/testing:63da998e3642b50bee33f4449826b2d623661505

    Workspace HelloC: Generator cmake created conanbuildinfo.cmake
    Workspace HelloC: Generated conaninfo.txt
    Workspace HelloC: Generated conanbuildinfo.txt
    Workspace HelloB: Generator cmake created conanbuildinfo.cmake
    Workspace HelloB: Generated conaninfo.txt
    Workspace HelloB: Generated conanbuildinfo.txt
    Workspace HelloA: Generator cmake created conanbuildinfo.cmake
    Workspace HelloA: Generated conaninfo.txt
    Workspace HelloA: Generated conanbuildinfo.txt


Note that nothing will really be installed in the local cache. All the dependencies are resolved locally:

.. code-block:: bash

    $ conan search
    There are no packages

Also, all the generated *conanbuildinfo.cmake* files for the dependencies are installed in the *build* folder. You can inspect them to check
that the paths they define for their dependencies are user folders. They don't point to the local cache.

As defined in the *conanws.yml*, a root *CMakeLists.txt* is generated for us. We can use it to generate the super-project and build it:

.. code-block:: bash

    $ cd build
    $ cmake .. -G "Visual Studio 14 Win64" # Adapt accordingly to your conan profile
    # Now build it. You can also open your IDE and build
    $ cmake --build . --config Release
    $ ./A/Release/app.exe
    Hello World C Release!
    Hello World B Release!
    Hello World A Release!

Now the project is editable. You can change the code of folder C *hello.cpp* to say "Bye World" and:

.. code-block:: bash

    # Edit your C/src/hello.cpp file to say "Bye"
    # Or press the build button of your IDE
    $ cmake --build . --config Release
    $ ./A/Release/app.exe
    Bye World C Release!
    Hello World B Release!
    Hello World A Release!

In-source builds
----------------
The current approach with automatic generation of the super-project is only valid if all the opened packages are using the
same build system, CMake. However, without using a super-project, you can still use Workspaces to simultaneously
work on different packages with different build systems. 

For this case, the *conanws.yml* won't have the ``generator`` or ``name`` fields.
The installation will be done without specifying an install folder:

.. code-block:: bash

    $ conan install .

Each local package will have its own build folder, which will contain the generated *conanbuildinfo.cmake* file.
You can do local builds in each of the packages, and they will be referring and linking the other opened packages in
user folders.


conanws.yml syntax
------------------
The *conanws.yml* file can be located in any parent folder of the location pointed to by the :command:`conan install` command.
Conan will search up through the folder hierarchy looking for a *conanws.yml* file. If the file is not found, the normal :command:`conan install`
command for a single package will be executed.


Any "opened" package will have an entry in the *conanws.yml* file. This entry will define the relative location of different
folders:

.. code-block:: text

    HelloB:
        folder: B
        includedirs: src  # relative to B, i.e. B/src
        cmakedir: src # Where the CMakeLists.txt is, necessary for the super-project
        build: "'build' if '{os}'=='Windows' else 'build_{build_type}'.lower()"
        libdirs: "'build/{build_type}' if '{os}'=='Windows' else 'build_{build_type}'.lower()"

If necessary, the local ``build`` and ``libdirs`` folders can be parameterized with the build type and the architecture (``arch``) to account for
different layouts and configurations.


The ``root`` field of *conanws.yml* defines the end consumers. They are needed as an input to define the dependency graph.
There can be more than one ``root`` in a comma separated list, but all of them will share the same dependency graph, so if they
require different versions of the same dependencies, they will conflict.

.. code-block:: text

    root: HelloA, Other
    generator: cmake # The super-project build system
    name: MyProject # Name for the super-project


Known limitations
-----------------

So far, only the CMake super-project generator is implemented. A Visual Studio version seems feasible, but is currently still under development and not yet available.


.. important:: 

    We really want your feedback. Please submit any suggestions, problems or ideas as issues to https://github.com/conan-io/conan/issues
    making sure to use the [workspaces] prefix in the issue title.
