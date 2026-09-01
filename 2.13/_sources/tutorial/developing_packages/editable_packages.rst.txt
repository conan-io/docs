.. _editable_packages:

Packages in editable mode
=========================

The normal way of working with Conan packages is to run a ``conan create`` or ``conan
export-pkg`` to store them in the local cache, so that consumers use the packages stored
in the cache. In some cases, when you want to consume these packages while developing
them, it can be tedious to run ``conan create`` each time you make changes to the package.
For those cases, you can put your package in editable mode, and consumers will be able to
find the headers and artifacts in your local working directory, eliminating the need for
packaging.

Let's see how we can put a package in editable mode and consume it from the local working
directory.

Please, first of all, clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/developing_packages/editable_packages

There are 2 folders inside this project:

..  code-block:: text

    .
    ├── hello
    │   ├── CMakeLists.txt
    │   ├── conanfile.py
    │   └── src
    │       └── hello.cpp
    └── say
        ├── CMakeLists.txt
        ├── conanfile.py
        ├── include
        │   └── say.h
        └── src
            └── say.cpp


- A "say" folder containing a fully fledged package, with its ``conanfile.py`` and its source
  code.
- A "hello" folder containing a simple consumer project with a ``conanfile.py`` and its
  source code, which depends on the ``say/1.0`` requirement.

We will put ``say/1.0`` in editable mode and show how the ``hello`` consumer can find ``say/1.0``
headers and binaries in its local working directory.

Put say/1.0 package in editable mode
------------------------------------

To avoid creating the package ``say/1.0`` in the cache for every change, we are going to
put that package in editable mode, creating **a link from the reference in the cache to
the local working directory**:

.. code-block:: bash

    $ conan editable add say
    $ conan editable list
    say/1.0
        Path: /Users/.../examples2/tutorial/developing_packages/editable_packages/say/conanfile.py


From now on, every usage of ``say/1.0`` by any other Conan package or project will be
redirected to the
``/Users/.../examples2/tutorial/developing_packages/editable_packages/say/conanfile.py``
user folder instead of using the package from the Conan cache.

Note that the key of editable packages is a correct definition of the ``layout()`` of the
package. Read the :ref:`package layout() section <reference_conanfile_methods_layout>` to learn more
about this method. 

In this example, the ``say`` ``conanfile.py`` recipe is using the predefined
``cmake_layout()`` which defines the typical CMake project layout that can be different
depending on the platform and generator used.

Now that the ``say/1.0`` package is in editable mode, let's build it locally:

.. include:: ../cmake_presets_note.inc

.. code-block:: bash

    $ cd say

    # Windows: we will build 2 configurations to show multi-config
    $ conan install . -s build_type=Release
    $ conan install . -s build_type=Debug
    $ cmake --preset conan-default
    $ cmake --build --preset conan-release
    $ cmake --build --preset conan-debug

    # Linux, MacOS: we will only build 1 configuration
    $ conan install .
    $ cmake --preset conan-release
    $ cmake --build --preset conan-release


Using say/1.0 package in editable mode
--------------------------------------

Consuming a package in editable mode is transparent from the consumer perspective.
In this case we can build the ``hello`` application as usual:

.. code-block:: bash

    $ cd ../hello

    # Windows: we will build 2 configurations to show multi-config
    $ conan install . -s build_type=Release
    $ conan install . -s build_type=Debug
    $ cmake --preset conan-default
    $ cmake --build --preset conan-release
    $ cmake --build --preset conan-debug
    $ build\Release\hello.exe
    say/1.0: Hello World Release!
    ...
    $ build\Debug\hello.exe
    say/1.0: Hello World Debug!
    ...

    # Linux, MacOS: we will only build 1 configuration
    $ conan install .
    $ cmake --preset conan-release
    $ cmake --build --preset conan-release
    $ ./build/Release/hello
    say/1.0: Hello World Release!

As you can see, ``hello`` can successfully find ``say/1.0`` header and library files.


Working with editable packages
------------------------------

Once the above steps have been completed, you can work with your build system or IDE
without involving Conan and make changes to the editable packages. The consumers will use
those changes directly. Let's see how this works by making a change in the ``say`` source
code:

.. code-block:: bash

    $ cd ../say
    # Edit src/say.cpp and change the error message from "Hello" to "Bye"

    # Windows: we will build 2 configurations to show multi-config
    $ cmake --build --preset conan-release
    $ cmake --build --preset conan-debug

    # Linux, MacOS: we will only build 1 configuration
    $ cmake --build --preset conan-release


And build and run the "hello" project:

.. code-block:: bash

    $ cd ../hello

    # Windows
    $ cd build
    $ cmake --build --preset conan-release
    $ cmake --build --preset conan-debug
    $ Release\hello.exe
    say/1.0: Bye World Release!
    $ Debug\hello.exe
    say/1.0: Bye World Debug!

    # Linux, MacOS
    $ cmake --build --preset conan-release
    $ ./hello
    say/1.0: Bye World Release!


In this manner, you can develop both the ``say`` library and the ``hello`` application
simultaneously without executing any Conan command in between. If you have both open in
your IDE, you can simply build one after the other.

Building editable dependencies
------------------------------

If there are many editable dependencies, it might be inconvenient to go one by one, building them in the right order.
It is possible to do an ordered build of the editable dependencies with the ``--build`` argument.

Let's clean the previous local executables:

.. code-block:: bash

    $ git clean -xdf

And using the ``build()`` method in the ``hello/conanfile.py`` recipe that we haven't really used so far (because
we have been building directly calling ``cmake``, not by calling ``conan build`` command), we can do such build with
just:

.. code-block:: bash

    $ conan build hello


Note that all we had to do to do a full build of this project is these two commands. Starting from scratch in a different folder:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/developing_packages/editable_packages
    $ conan editable add say
    $ conan build hello --build=editable


Note that if we don't pass the ``--build=editable`` to ``conan build hello``, the binaries for ``say/0.1`` that is in editable mode
won't be available and it will fail. With the ``--build=editable``, first a build of the ``say`` binaries is done locally and 
incrementally, and then another incremental build of ``hello`` will be done. Everything will still happen locally, with no packages
built in the cache. If there are multiple ``editable`` dependencies, with nested transitive dependencies, Conan will build them
in the right order. 

If editable packages have dependants in the Conan cache, it is possible to force the rebuild from source of the
cache dependants by using ``--build=editable --build=cascade``. In general this should be avoided, and the recommendation if it
is needed to rebuild those dependencies is to put them in editable mode too.

Note that it is possible to build and test a package in editable with with its own ``test_package`` folder.
If a package is put in ``editable`` mode, and if it contains a ``test_package`` folder, the ``conan create`` command
will still do a local build of the current package. 


Revert the editable mode
------------------------

In order to revert the editable mode just remove the link using:

.. code-block:: bash

    $ conan editable remove --refs=say/1.0

It will remove the link (the local directory won't be affected) and all the packages consuming this
requirement will get it from the cache again.

.. warning::

    Packages that are built while consuming an editable package in their upstreams can
    generate binaries and packages that are incompatible with the released version of the
    editable package. Avoid uploading these packages without re-creating them with the
    in-cache version of all the libraries.
