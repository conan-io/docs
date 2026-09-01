.. spelling::

  mytimer


.. _gcc_integration:


Compilers on command line
=========================

The **compiler_args** generator creates a file named ``conanbuildinfo.args`` containing command
line arguments to invoke ``gcc``, ``clang`` or ``cl`` (Visual Studio) compiler.

Now we are going to compile the :ref:`getting started<getting_started>` example using **compiler_args** instead of the **cmake** generator.

Open ``conanfile.txt`` and change (or add) **compiler_args** generator:


.. code-block:: text

   [requires]
   poco/1.9.4

   [generators]
   compiler_args

Install the requirements (from the mytimer/build folder):

.. code-block:: bash

   $ conan install ..


.. note::

   Remember, if you don't specify settings in the **install command** with **-s**, Conan will use the detected defaults.
   You can always change them by editing the ``~/.conan/profiles/default`` or override them with "-s" parameters.


The generated ``conanbuildinfo.args`` show:

.. code-block:: text

   -DPOCO_STATIC=ON -DPOCO_NO_AUTOMATIC_LIBS
   -I/home/user/.conan/data/poco/1.9.4/_/_/package/58080bce1cc38259eb7c282aa95c25aecde8efe4/include
   -I/home/user/.conan/data/openssl/1.0.2t/_/_/package/f99afdbf2a1cc98ba2029817b35103455b6a9b77/include
   -I/home/user/.conan/data/zlib/1.2.11/_/_/package/6af9cc7cb931c5ad942174fd7838eb655717c709/include
   -m64 -O3 -s -DNDEBUG
   -Wl,-rpath="/home/user/.conan/data/poco/1.9.4/_/_/package/58080bce1cc38259eb7c282aa95c25aecde8efe4/lib"
   -Wl,-rpath="/home/user/.conan/data/openssl/1.0.2t/_/_/package/f99afdbf2a1cc98ba2029817b35103455b6a9b77/lib"
   -Wl,-rpath="/home/user/.conan/data/zlib/1.2.11/_/_/package/6af9cc7cb931c5ad942174fd7838eb655717c709/lib"
   -L/home/user/.conan/data/poco/1.9.4/_/_/package/58080bce1cc38259eb7c282aa95c25aecde8efe4/lib
   -L/home/user/.conan/data/openssl/1.0.2t/_/_/package/f99afdbf2a1cc98ba2029817b35103455b6a9b77/lib
   -L/home/user/.conan/data/zlib/1.2.11/_/_/package/6af9cc7cb931c5ad942174fd7838eb655717c709/lib
   -lPocoMongoDB -lPocoNetSSL -lPocoNet -lPocoCrypto -lPocoDataSQLite -lPocoData -lPocoZip -lPocoUtil
   -lPocoXML -lPocoJSON -lPocoRedis -lPocoFoundation
   -lrt -lssl -lcrypto -ldl -lpthread -lz
   -D_GLIBCXX_USE_CXX11_ABI=1

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
