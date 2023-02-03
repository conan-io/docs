.. _editable_packages:

Packages in editable mode
=========================

When working in big projects with several functionalities interconnected it is recommended to avoid
the one-and-only huge project approach in favor of several libraries, each one specialized
in a set of common tasks, even maintained by dedicated teams. This approach helps to isolate
and reusing code helps with compiling times and reduces the likelihood of including files that
not correspond to the API of the required library.

Nevertheless, in some case, it is useful to work in several libraries at the same time and see how
the changes in one of them are propagated to the others. With the normal flow, for every source change,
it is necessary to do ``conan create`` or ``conan export-pkg`` to put the package in the cache and
make it available to consumers.

With the editable packages, you can tell Conan where to find the headers and the artifacts ready for
consumption in your local working directory. There is no need to package.

Please, first of all, clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/developing_packages/editable_packages

There are 2 folders inside this project:

- A "say" folder containing a fully fledge package, with its ``conanfile.py``, its source code.
- A "hello" folder containing a simple consumer project with a ``conanfile.txt`` and its source code,
  which depends on the ``say/1.0@user/testing`` requirement.

The goal is to be able to build the "hello" project, without actually having the ``say/1.0@user/testing``
package in the cache, but directly in this project folder.

Put a package in editable mode
------------------------------

To avoid creating the package ``say/1.0`` in the cache for every change, we are going
to put that package in editable mode, creating **a link from the reference in the cache to the local
working directory**:

.. code-block:: bash

    $ conan editable add say say/1.0
    $ conan editable list
    say/1.0
        Path: /Users/.../examples2/tutorial/developing_packages/editable_packages/say/conanfile.py


That is it. Now, every usage of ``say/1.0``, by any other Conan package or
project, will be redirected to the
``/examples2/tutorial/developing_packages/editable_packages/say`` user folder instead of
using the package from the Conan cache.

Note that the key of editable packages is a correct definition of the ``layout()`` of the
package. Read the :ref:`package layout() section <conanfile_methods_layout>` to learn more
about this method. 

In this example, the ``say`` ``conanfile.py`` recipe is using the predefined
``cmake_layout()`` which defines the typical CMake project layout, which can be different
in the different platforms.

Now the ``say/1.0`` package is in editable mode, lets build it locally:

.. code-block:: bash

    $ cd say

    # Windows: we will build 2 configurations to show multi-config
    $ conan install . -s build_type=Release
    $ conan install . -s build_type=Debug
    $ cmake --preset default
    $ cmake --build --preset release
    $ cmake --build --preset debug

    # Linux, MacOS: we will only build 1 configuration
    $ conan install .
    $ cmake --preset release
    $ cmake --build --preset release


Using a package in editable mode
--------------------------------

Consuming a package in editable mode is transparent from the consumer perspective.
In this case we can build the ``hello`` application as usual:

.. code-block:: bash

    $ cd ../hello

    # Windows: we will build 2 configurations to show multi-config
    $ conan install . -s build_type=Release
    $ conan install . -s build_type=Debug
    $ cmake --preset default
    $ cmake --build --preset release
    $ cmake --build --preset debug
    $ build\Release\hello.exe
    say/1.0: Hello World Release!
    ...
    $ build\Debug\hello.exe
    say/1.0: Hello World Debug!
    ...

    # Linux, MacOS: we will only build 1 configuration
    $ conan install .
    $ cmake --preset release
    $ cmake --build --preset release
    $ ./build/Release/hello
    say/1.0: Hello World Release!


Working with editable packages
------------------------------

Once the above steps have been done, we can basically work with our build system or IDE,
no Conan involved, and do changes in the editable packages and have those changes used by
the consumers directly. Lets see it, lets start by doing a change in the ``say`` source
code:

.. code-block:: bash

    $ cd ../say
    # Edit src/say.cpp and change the error message from "Hello" to "Bye"

    # Windows: we will build 2 configurations to show multi-config
    $ cmake --build --preset release
    $ cmake --build --preset debug

    # Linux, MacOS: we will only build 1 configuration
    $ cmake --build --preset release


And build and run the "hello" project:

.. code-block:: bash

    $ cd ../hello

    # Windows
    $ cd build
    $ cmake --build --preset release
    $ cmake --build --preset debug
    $ Release\hello.exe
    say/1.0: Bye World Release!
    $ Debug\hello.exe
    say/1.0: Bye World Debug!

    # Linux, MacOS
    $ cmake --build --preset release
    $ ./hello
    say/1.0: Bye World Release!


In that way, it is possible to be developing both the ``say`` library and the ``hello``
application, at the same time, without any Conan command. If you had both open in the IDE,
it would be just building one after the other.

.. note::

    When a package is in editable mode, some commands will not work. It is not
    possible to :command:`conan upload`, :command:`conan export` or :command:`conan
    create` when a package is in editable mode.


Revert the editable mode
------------------------

In order to revert the editable mode just remove the link using:

.. code-block:: bash

    $ conan editable remove say/1.0

It will remove the link (the local directory won't be affected) and all the packages consuming this
requirement will get it from the cache again.

.. warning::

   Packages that are built consuming an editable package in its graph upstreams can
   generate binaries and packages incompatible with the released version of the editable
   package. Avoid uploading these packages without re-creating them with the in-cache
   version of all the libraries.