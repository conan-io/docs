.. _other_generator:


Other generators (create your own)
=====================================

Maybe you need a more generic ``conanbuildinfo`` file to use with another build system or script.

.. note:: 
   
   Do you miss support for your build system? Tell us what you need. info@conan.io
     
Specify **txt** generator:

   .. code-block:: text
   
      [requires]
      Poco/1.7.2@lasote/stable
      
      [generators]
      txt
   
Install the requirements:

.. code-block:: bash

   $ conan install

And a file is generated, with the same information as in the case of CMake and gcc, only in a generic format:

.. code-block:: text

   [includedirs]
   /home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/include
   /home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/include
   /home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/include
   
   [libs]
   PocoUtil
   PocoXML
   PocoJSON
   PocoMongoDB
   PocoNet
   PocoCrypto
   PocoData
   PocoDataSQLite
   PocoZip
   PocoFoundation
   pthread
   dl
   rt
   ssl
   crypto
   z
   
   [libdirs]
   /home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/lib
   /home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/lib
   /home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/lib
   
   [bindirs]
   /home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/bin
   /home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/bin
   /home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/bin
   
   [defines]
   POCO_STATIC=ON
   POCO_NO_AUTOMATIC_LIBS