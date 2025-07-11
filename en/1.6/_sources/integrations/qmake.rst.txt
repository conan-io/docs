.. _qmake:


QMake
======

A qmake generator will generate a ``conanbuildinfo.pri`` file that can be used for your qmake builds.

.. code-block:: bash

    $ conan install . -g qmake

Add ``conan_basic_setup`` to ``CONFIG`` and include the file in your existing project ``.pro`` file:

**yourproject.pro**

.. code-block:: text

   # ...
   
   CONFIG += conan_basic_setup
   include(conanbuildinfo.pri)

This will include all the statements in ``conanbuildinfo.pri`` in your project.
Include paths, libraries, defines, etc. will be set up for all requirements you have defined in ``conanfile.txt``.

If you'd rather like to manually add the variables for each dependency, you can do so by skipping the CONFIG statement and only include ``conanbuildinfo.pri``:

**yourproject.pro**

.. code-block:: text

   # ...
   
   include(conanbuildinfo.pri)
   
   # you may now modify your variables manually for each library, such as
   # INCLUDEPATH += CONAN_INCLUDEPATH_POCO

The ``qmake`` generator allows multi-configuration packages, i.e. packages that contains both debug and release artifacts. Lets see an example:

Example
----------

There is a complete example in https://github.com/memsharded/qmake_example
This project will depend on a multi-configuration (debug/release) "Hello World" package, that should be installed first:

.. code-block:: bash

    $ git clone https://github.com/memsharded/hello_multi_config
    $ cd hello_multi_config
    $ conan create . user/channel

This hello package is created with cmake, but that doesn't matter, it can be consumed from a qmake project:

Then, you can get the qmake project and build it, both for debug and release (this example has been tested on linux):

.. code-block:: bash

    $ git clone https://github.com/memsharded/qmake_example
    $ cd qmake_example
    $ conan install .
    $ qmake
    $ make
    $ ./helloworld
    > Hello World Release!
    # now lets build the debug one
    $ make clean
    $ qmake CONFIG+=debug
    $ make
    $ ./helloworld
    > Hello World Debug!




.. seealso:: Check the :ref:`Reference/Generators/qmake <qmake_generator>` for the complete reference.

