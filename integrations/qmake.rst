.. _qmake:

QMake
======

The ``qmake`` generator will generate a *conanbuildinfo.pri* file that can be used for your qmake builds.

.. code-block:: bash

    $ conan install . -g qmake

Add ``conan_basic_setup`` to ``CONFIG`` and include the file in your existing project *.pro* file:

.. code-block:: text
   :caption: *yourproject.pro*

    ...

    CONFIG += conan_basic_setup
    include(conanbuildinfo.pri)

This will include all the statements in *conanbuildinfo.pri* in your project. Include paths, libraries, defines, etc. will be set up
for all requirements you have defined as dependencies in a *conanfile.txt*.

If you'd prefer to manually add the variables for each dependency, you can do so by skipping the ``CONFIG`` statement and
only including *conanbuildinfo.pri*:

.. code-block:: text
   :caption: *yourproject.pro*

    # ...

    include(conanbuildinfo.pri)

    # you may now modify your variables manually for each library, such as
    # INCLUDEPATH += CONAN_INCLUDEPATH_POCO

The ``qmake`` generator allows multi-configuration packages, i.e. packages that contains both Debug and Release artifacts.

Example
-------

.. tip::

    This complete example is stored in https://github.com/memsharded/qmake_example

This example project will depend on a multi-configuration (Debug/Release) "Hello World" package. It should be installed first:

.. code-block:: bash

    $ git clone https://github.com/memsharded/hello_multi_config
    $ cd hello_multi_config
    $ conan create . memsharded/testing
    Hello/0.1@memsharded/testing export: Copied 1 '.txt' file: CMakeLists.txt
    Hello/0.1@memsharded/testing export: Copied 1 '.cpp' file: hello.cpp
    Hello/0.1@memsharded/testing export: Copied 1 '.h' file: hello.h
    Hello/0.1@memsharded/testing: A new conanfile.py version was exported

This hello package is created with CMake, but that doesn't matter for this example, as it can be consumed from a qmake project with the
configuration showed before.

Now let's get the qmake project and install its `Hello/0.1@memsharded/testing` dependency:

.. code-block:: bash

    $ git clone https://github.com/memsharded/qmake_example
    $ cd qmake_example
    $ conan install .
    PROJECT: Installing C:\Users\memsharded\qmake_example\conanfile.txt
    Requirements
        Hello/0.1@memsharded/testing from local cache - Cache
    Packages
        Hello/0.1@memsharded/testing:15af85373a5688417675aa1e5065700263bf257e - Cache

    Hello/0.1@memsharded/testing: Already installed!
    PROJECT: Generator qmake created conanbuildinfo.pri
    PROJECT: Generator txt created conanbuildinfo.txt
    PROJECT: Generated conaninfo.txt

As you can see, we got the dependency information in the *conanbuildinfo.pri* file. You can inspect the file to see the variables generated.
Now let's build the project for Release and then for Debug:

.. code-block:: bash

    $ qmake
    $ make
    $ ./helloworld
    > Hello World Release!

    # now let's build the Debug one
    $ make clean
    $ qmake CONFIG+=debug
    $ make
    $ ./helloworld
    > Hello World Debug!

.. seealso::

    Check the complete reference of the :ref:`qmake generator<qmake_generator>`.
