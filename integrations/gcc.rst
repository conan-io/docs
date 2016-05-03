.. _gcc_generator:


gcc
=====

Conan provides a **gcc** generator, able to generate files to be directly used in the command line
by the gcc compiler.

Now we are going to compile the :ref:`getting started<getting_started>` example using **gcc** instead of the **cmake** generator.

.. note:: 
   
   We have only tested the gcc generator in linux with the gcc compiler. But maybe it works with MinGW in Windows or even clang in OSx. Try it and let us know. :D


Open ``conanfile.txt`` and change (or add) **gcc** generator:

    
.. code-block:: text

   [requires]
   Poco/1.7.2@lasote/stable
   
   [generators]
   gcc
   
Install the requirements (from the mytimer/build folder):

.. code-block:: bash

   $ conan install ..


.. note::

   Remember, if you don't specify settings in **install command** with **-s**, conan will use the detected defaults. You can always change them by editing the ``~/.conan/conan.conf`` or override them with "-s" parameters.  
 

Let's take a look to the generated ``conanbuildinfo.gcc``:

.. code-block:: text
   
   -DPOCO_STATIC=ON -DPOCO_NO_AUTOMATIC_LIBS -I/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/include -I/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/include -I/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/include -L/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/lib -L/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/lib -L/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/lib -Wl,-rpath=/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/lib -Wl,-rpath=/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/lib -Wl,-rpath=/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/lib -lPocoUtil -lPocoXML -lPocoJSON -lPocoMongoDB -lPocoNet -lPocoCrypto -lPocoData -lPocoDataSQLite -lPocoZip -lPocoFoundation -lpthread -ldl -lrt -lssl -lcrypto -lz    

Wow, it's a little hard to read, but those are just the **gcc** parameters needed to compile our program. But you could recognize **-I** options with headers directories, **-L** for libraries directories... 

It's the same information we saw in ``conanbuildinfo.cmake``.

So just execute:

.. code-block:: bash

   $ mkdir bin
   $ g++ timer.cpp @conanbuildinfo.gcc -o bin/timer


.. note:: 
   
   "@conanbuildinfo.gcc" appends all the file contents to g++ command parameters
   

.. code-block:: bash

   $ ./bin/timer
    Callback called after 250 milliseconds.
    ...