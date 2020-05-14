.. spelling::

  mytimer


.. _gcc_integration:


Compilers on command line
=========================

The **compiler_args** generator creates a file named ``conanbuildinfo.args`` containing a command
line arguments to invoke ``gcc``, ``clang`` or ``cl`` (Visual Studio) compiler.

Now we are going to compile the :ref:`getting started<getting_started>` example using **compiler_args** instead of the **cmake** generator.

Open ``conanfile.txt`` and change (or add) **compiler_args** generator:


.. code-block:: text

   [requires]
   Poco/1.9.0@pocoproject/stable

   [generators]
   compiler_args

Install the requirements (from the mytimer/build folder):

.. code-block:: bash

   $ conan install ..


.. note::

   Remember, if you don't specify settings in **install command** with **-s**, conan will use the detected defaults.
   You can always change them by editing the ``~/.conan/profiles/default`` or override them with "-s" parameters.


The generated ``conanbuildinfo.args``:

.. code-block:: text

   -DPOCO_STATIC=ON -DPOCO_NO_AUTOMATIC_LIBS
   -Ipath/to/Poco/1.7.9/pocoproject/stable/package/dd758cf2da203f96c86eb99047ac152bcd0c0fa9/include
   -Ipath/to/OpenSSL/1.0.2l/conan/stable/package/227fb0ea22f4797212e72ba94ea89c7b3fbc2a0c/include
   -Ipath/to/zlib/1.2.11/conan/stable/package/8018a4df6e7d2b4630a814fa40c81b85b9182d2b/include
   -m64 -DNDEBUG -Wl,-rpath,"path/to/Poco/1.7.9/pocoproject/stable/package/dd758cf2da203f96c86eb99047ac152bcd0c0fa9/lib"
   -Wl,-rpath,"path/to/OpenSSL/1.0.2l/conan/stable/package/227fb0ea22f4797212e72ba94ea89c7b3fbc2a0c/lib"
   -Wl,-rpath,"path/to/zlib/1.2.11/conan/stable/package/8018a4df6e7d2b4630a814fa40c81b85b9182d2b/lib"
   -Lpath/to/Poco/1.7.9/pocoproject/stable/package/dd758cf2da203f96c86eb99047ac152bcd0c0fa9/lib
   -Lpath/to/OpenSSL/1.0.2l/conan/stable/package/227fb0ea22f4797212e72ba94ea89c7b3fbc2a0c/lib
   -Lpath/to/zlib/1.2.11/conan/stable/package/8018a4df6e7d2b4630a814fa40c81b85b9182d2b/lib
   -lPocoUtil -lPocoMongoDB -lPocoNet -lPocoNetSSL -lPocoCrypto -lPocoData -lPocoDataSQLite -lPocoZip
   -lPocoXML -lPocoJSON -lPocoFoundation -lssl -lcrypto -lz -stdlib=libc++

This is hard to read, but those are just the **compiler_args** parameters needed to compile our program:

  - **-I** options with headers directories
  - **-L** for libraries directories
  - **-l** for library names
  - and so on... see the :ref:`complete reference here<compiler_args_generator>`

It's almost the same information we can see in ``conanbuildinfo.cmake`` and many other generators' files.

Run:

.. code-block:: bash

   $ mkdir bin
   $ g++ ../timer.cpp @conanbuildinfo.args -std=c++14 -o bin/timer


.. note:: 
   
   "@conanbuildinfo.args" appends all the file contents to g++ command parameters
   

.. code-block:: bash

   $ ./bin/timer
    Callback called after 250 milliseconds.
    ...


To invoke ``cl`` (Visual Studio compiler):


.. code-block:: bash

    $ cl /EHsc timer.cpp @conanbuildinfo.args

You can also use the generator within your ``build()`` method of your conanfile.py.

Check the :ref:`Reference, generators, compiler_args <compiler_args_generator>` section for more info.
