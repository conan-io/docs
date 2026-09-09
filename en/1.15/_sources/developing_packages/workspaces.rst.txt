.. _workspaces:

Workspaces
==========

.. warning::

    This is an **experimental** feature. This is actually a preview of the feature, with the main goal of receiving feedbacks and improving
    it. Consider the file formats, commands and flows to be unstable and subject to changes in the next releases.

Sometimes, it is necessary to work simultaneously on more than one package. In theory, each package should be a "work unit", and developers
should be able to work on them in isolation. But sometimes, some changes require modifications in more than one package at the same time.
The local development flow can help, but it still requires using :command:`export-pkg` to put the artifacts in the local cache, where other
packages under development will consume them.

The Conan workspaces allow to have more than one package in user folders, and have them directly use other packages from user folders
without needing to put them in the local cache. Furthermore, they enable incremental builds on large projects containing multiple packages.

Lets introduce them with a practical example; the code can be found in the conan examples repository:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples.git
    $ cd features/workspace/cmake


Note that this folder contains two files *conanws_gcc.yml* and *conan_vs.yml*, for gcc (Makefiles, single-configuration build environments)
and for Visual Studio (MSBuild, multi-configuration build environment), respectively. 

Conan workspace definition
--------------------------

Workspaces are defined in a yaml file, with any user defined name. Its structure is:

.. code-block:: yaml

    editables:
        say/0.1@user/testing:
            path: say
        hello/0.1@user/testing:
            path: hello
        chat/0.1@user/testing:
            path: chat
    layout: layout_gcc
    workspace_generator: cmake
    root: chat/0.1@user/testing


The first section ``editables`` defines the mapping between package references and relative paths. Each one is equivalent to
a :ref:`conan_editable_add` command (Do NOT do this -- it is not necessary. It will be automatically done later. Just to understand
the behavior):

.. code-block:: bash

    $ conan editable add say say/0.1@user/testing --layout=layout_gcc
    $ conan editable add hello hello/0.1@user/testing --layout=layout_gcc
    $ conan editable add chat chat/0.1@user/testing --layout=layout_gcc
    

The main difference is that this *Editable* state is only temporary for this workspace. It doesn't affect other projects or
packages, which can still consume these say, hello, chat packages from the local cache.

Note that the ``layout: layout_gcc`` declaration in the workspace affects all the packages. It is also possible to define
a different layout per package, as:

.. code-block:: yaml

    editables:
        say/0.1@user/testing:
            path: say
            layout: custom_say_layout

Layout files are explained in :ref:`editable_layout` and in the :ref:`editable_packages` sections.

The ``workspace_generator`` defines the file that will be generated for the top project. The only supported value so far
is ``cmake`` and it will generate a *conanworkspace.cmake* file that looks like:

.. code-block:: cmake

    set(PACKAGE_say_SRC "<path>/examples/workspace/cmake/say/src")
    set(PACKAGE_say_BUILD "<path>/examples/workspace/cmake/say/build/Debug")
    set(PACKAGE_hello_SRC "<path>/examples/workspace/cmake/hello/src")
    set(PACKAGE_hello_BUILD "<path>/examples/workspace/cmake/hello/build/Debug")
    set(PACKAGE_chat_SRC "<path>/examples/workspace/cmake/chat/src")
    set(PACKAGE_chat_BUILD "<path>/examples/workspace/cmake/chat/build/Debug")

    macro(conan_workspace_subdirectories)
        add_subdirectory(${PACKAGE_say_SRC} ${PACKAGE_say_BUILD})
        add_subdirectory(${PACKAGE_hello_SRC} ${PACKAGE_hello_BUILD})
        add_subdirectory(${PACKAGE_chat_SRC} ${PACKAGE_chat_BUILD})
    endmacro()

This file can be included in your user-defined *CMakeLists.txt* (this file is not generated).
Here you can see the *CMakeLists.txt* used in this project:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.0)

    project(WorkspaceProject)

    include(${CMAKE_BINARY_DIR}/conanworkspace.cmake)
    conan_workspace_subdirectories()

The ``root: chat/0.1@user/testing`` defines which is the consumer node of the graph, typically some kind of executable. You
can provide a comma separated list of references. All the root nodes will be in the same dependency graph, leading to conflicts if they
depend on different versions of the same library, as in any other Conan command.


Single configuration build environments
---------------------------------------

There are some build systems, like Make, that require the developer to manage different configurations in different build folders,
and switch between folders to change configuration. The file described above is *conan_gcc.yml* file, which defines a Conan workspace that
works for a CMake based project for MinGW/Unix Makefiles gcc environments (working for apple-clang or clang would be very similar, if not identical).

Lets use it to install this workspace:

.. code-block:: bash

    $ mkdir build_release && cd build_release
    $ conan workspace install ../conanws_gcc.yml --profile=my_profile

Here we assume that you have a ``my_profile`` profile defined which would use a single-configuration build system (like Makefiles). The
example is tested with gcc in Linux, but working with apple-clang with Makefiles would be the same).
You should see something like:

.. code-block:: bash

    Configuration:
    [settings]
    ...
    build_type=Release
    compiler=gcc
    compiler.libcxx=libstdc++
    compiler.version=4.9
    ...

    Requirements
        chat/0.1@user/testing from user folder - Editable
        hello/0.1@user/testing from user folder - Editable
        say/0.1@user/testing from user folder - Editable
    Packages
        chat/0.1@user/testing:df2c4f4725219597d44b7eab2ea5c8680abd57f9 - Editable
        hello/0.1@user/testing:b0e473ad8697d6069797b921517d628bba8b5901 - Editable
        say/0.1@user/testing:80faec7955dcba29246085ff8d64a765db3b414f - Editable

    say/0.1@user/testing: Generator cmake created conanbuildinfo.cmake
    ...
    hello/0.1@user/testing: Generator cmake created conanbuildinfo.cmake
    ...
    chat/0.1@user/testing: Generator cmake created conanbuildinfo.cmake
    ...

These *conanbuildinfo.cmake* files have been created in each package *build/Release* folder, as defined by the
*layout_gcc* file:

.. code-block:: ini

    # This helps to define the location of CMakeLists.txt within package
    [source_folder]
    src

    # This defines where the conanbuildinfo.cmake will be written to
    [build_folder]
    build/{{settings.build_type}}

Now we can configure and build our project as usual:

.. code-block:: bash

    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
    $ cmake --build . # or just $ make
    $ ../chat/build/Release/app
    Release: Hello World!
    Release: Hello World!
    Release: Hello World!

Now, go do a change in some of the packages, for example the "say" one, and rebuild. See how it does an incremental build (fast).

Note that nothing will really be installed in the local cache, all the dependencies are resolved locally:

.. code-block:: bash

    $ conan search say
    There are no packages matching the 'say' pattern

.. note::

    The package *conanfile.py* recipes do not contain anything special, they are standard recipes. But the packages *CMakeLists.txt*
    have defined the following:

    .. code-block:: cmake

        conan_basic_setup(NO_OUTPUT_DIRS)

    This is because the default ``conan_basic_setup()`` does define output directories for artifacts such as *bin*, *lib*, etc, which
    is not what the local project layout expects. You need to check and make sure that your build scripts and recipe matches both
    the expected local layout (as defined in layout files), and the recipe ``package()`` method logic.


Building for debug mode is done in its own folder:

.. code-block:: bash

    $ cd .. && mkdir build_debug && cd build_debug
    $ conan workspace install ../conanws_gcc.yml --profile=my_gcc_profile -s build_type=Debug
    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug
    $ cmake --build . # or just $ make
    $ ../chat/build/Debug/app
    Debug: Bye World!
    Debug: Bye World!
    Debug: Bye World!


Multi configuration build environments
--------------------------------------

Some build systems, like Visual Studio (MSBuild), use "multi-configuration" environments. That is, even if the project is configured just once
you can switch between different configurations (like Debug/Release) directly in the IDE and build there.

The above example uses the Conan ``cmake`` generator, that creates a single *conanbuildinfo.cmake* file. This is not a problem if we have our
configurations built in different folders. Each one will contain its own *conanbuildinfo.cmake*. For Visual Studio that means that if
we wanted to switch from Debug<->Release, we should issue a new ``conan workspace install`` command with the right ``-s build_type`` and
do a clean build, in order to get the right dependencies.

Conan has the :ref:`cmake_multi` generator, that allows this direct switch of Debug/Release configuration in the IDE. The *conanfile.py*
recipes they have defined the ``cmake`` generator, so the first step is to override that in our *conanws_vs.yml* file:

.. code-block:: yaml

    editables:
    say/0.1@user/testing:
        path: say
    hello/0.1@user/testing:
        path: hello
    chat/0.1@user/testing:
        path: chat
    layout: layout_vs
    generators: cmake_multi
    workspace_generator: cmake
    root: chat/0.1@user/testing

Note the ``generators: cmake_multi`` line, that will define the generators to be used by our workspace packages. Also, our *CMakeLists.txt*
should take into account that now we won't have a *conanbuildinfo.cmake* file, but a *conanbuildinfo_multi.cmake* file. See for example
the *hello/src/CMakeLists.txt* file:

.. code-block:: cmake

    project(Hello)

    if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
        include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
    else()
        include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
    endif()

    conan_basic_setup(NO_OUTPUT_DIRS)

    add_library(hello hello.cpp)
    conan_target_link_libraries(hello)


The last ``conan_target_link_libraries(hello)`` is a helper that does the right linking with Debug/Release libraries (also works when using cmake
targets).

Make sure to install both Debug and Release configurations straight ahead, if we want to later switch between them in the IDE:

.. code-block:: bash

    $ mkdir build && cd build
    $ conan workspace install ../conanws_vs.yml
    $ conan workspace install ../conanws_vs.yml -s build_type=Debug
    $ cmake .. -G "Visual Studio 15 Win64"

With those commands you will get a Visual Studio solution, that you can open, select the *app* executable as StartUp project, and start building,
executing, debugging, switching from Debug and Release configurations freely from the IDE, without needing to issue further Conan commands.

You can check in the project folders, how the following files have been generated:

.. code-block:: text

    hello
      |- build
            | - conanbuildinfo_multi.cmake
            | - conanbuildinfo_release.cmake
            | - conanbuildinfo_debug.cmake


Note that they are not located in *build/Release* and *build/Debug* subfolders; that is because of the multi-config environment. To account for that
the *layout_vs* define the ``[build_folder]`` not as ``build/{settings.build_type}`` but just as:

.. code-block:: ini

    [build_folder]
    build

Out of source builds
--------------------

The above examples are using a build folder in-source of the packages in editable mode. It is possible to define out-of-source builds layouts, 
using relative paths and the ``reference`` argument. The following layout definition could be used to locate the build artifacts of an 
editable package in a sibling ``build/<package-name>`` folder:

.. code-block:: ini

    [build_folder]
    ../build/{{reference.name}}/{{settings.build_type}}

    [includedirs]
    src

    [libdirs]
    ../build/{{reference.name}}/{{settings.build_type}}/lib


Notes
-----

Note that this way of developing packages shouldn't be used to create the final packages (you could try to use :command:`conan export-pkg`), but instead,
a full package creation with :command:`conan create` (best in CI) is recommended. 

So far, only the CMake super-project generator is implemented. A Visual Studio one is being considered, and seems feasible, but not yet available.

.. important::

    We really want your feedback. Please submit any issues to https://github.com/conan-io/conan/issues with any suggestion, problem, idea,
    and using [workspaces] prefix in the issue title.
