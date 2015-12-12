.. _conanfile_txt:

Using ``conanfile.txt``
-----------------------

This section shows how to use the ``conanfile.txt`` to manage the required libraries in your project.

.. note::

   Remember, in :ref:`Getting started<getting_started>` we saw how to use **conan** to download the **POCO** library and compile a program.
   

But before we start with ``conanfile.txt`` details, let's review the :ref:`getting started <getting_started>` example and see what **conan** is really doing:

   
   1. We have created a ``conanfile.txt``
   
      .. code-block:: text
      
         [requires]
         Poco/1.6.1@lasote/stable
         
         [generators]
         cmake
      
   #. We execute **conan install**
   
      .. code-block:: bash
      
         $ conan install
      
   #. We include the generated file ``conanbuildinfo.cmake`` in our ``CMakeLists.txt`` file.


What is really happening?

   - When you execute **conan install**, conan reads ``conanfile.txt`` from the current directory.
   - Conan reads all the **[requires]** entries and installs them (taking care of upstream options/requires override)
       
     So conan will download the requirements (and each requirement's requirements recursively), first looking at your local store (a local cache) and, if its not found, at the remotes.
     
     In this example, conan will download *OpenSSL/1.0.2d@lasote/stable* and *zlib/1.2.8@lasote/stable*.
     
     Conan will also collect needed information from each requirement: **libs** that has to be **linked**, the **include directories**, **compile flags** etc.
     See the requires_ section for more details.
   
   
   - For each **[generator]** specified, conan will generate a file with mentioned information that will help you to build your project and link with your requirements. The generators_ section contains more details.

.. tip:: **Pro Tip**

   If you execute a **conan install** command in your shell, specifying a reference like **Poco/1.6.1@lasote/stable**, conan will download the Poco package and all its dependencies (*OpenSSL/1.0.2d@lasote/stable* and *zlib/1.2.8@lasote/stable*) to your local repository and print information about the local directory where they are installed. 
   
   You will find a **/lib** and an **/include** subfolder together with the libraries and include files. You could handle them manually if you want. But we recommend the usage of a ``conanfile.txt`` or ``conanfile.py`` instead of directly installing packages.
   

Now create your ``conanfile.txt`` in your project and start using conan.


Requires
........

We put the requirements in the **[requires]** section. 
The requirements look like this:

.. code-block:: text

   [requires]
   Poco/1.6.1@lasote/stable
   

Where:

   - ``Poco`` is the name
   - ``1.6.1`` is the version
   - ``lasote`` is the owner
   - ``stable`` is the channel (there could be several channels for developing, testing, etc.)


Overriding requirements
_______________________


You can specify multiple requirements and you can **override** the "require's requirements".
Let's see an example. 

At the beginning of this section we saw that, when we call the **conan install** command, conan installs the POCO requirement and all its requirements recursively:

   * **OpenSSL/1.0.2d@lasote/stable**
   * **zlib/1.2.8@lasote/stable**
   
.. tip:: 

    This is a good example to explain requirements overriding. We all know the importance of keeping the OpenSSL library updated.

So, What happens if a new release of OpenSSL library is out? 

Do we need to wait until **lasote** generates a new package of POCO that includes the new OpenSSL library? That is not necessary.

We just enter the new version in **[requires]**:

.. code-block:: text

   [requires]
   Poco/1.6.1@lasote/stable
   OpenSSL/1.1.0a@lasote/stable

The second line will override the OpenSSL requirement with the (non-existent yet)  **OpenSSL/1.1.0a**

And, maybe, in order to try out the new zlib alpha features, we could replace the Zlib requirement with one from another user or channel. 

.. code-block:: text

   [requires]
   Poco/1.6.1@lasote/stable
   OpenSSL/1.1.0a@lasote/stable
   zlib/1.2.9@otheruser/alpha


Handling this task without a package manager in our project could be a nightmare. Don't you think?


.. _generators:

Generators
..........

Conan reads the **[generators]** section from ``conanfile.txt`` and creates one file for each generator with all necessary information to link your program with the specified requirements.


.. _cmake_generator:

*cmake*
_______

If you are using *CMake* to build your project, you can use the *cmake* generator to manage all your requirements.


**conanfile.txt**

.. code-block:: text

   ...
   
   [generators]
   cmake


When **conan install** is executed, a file named ``conanbuildinfo.cmake`` is created. 

We can include ``conanbuildinfo.cmake`` in our project's ``CMakeLists.txt`` to manage our requirements.


This is the ``CMakeLists.txt`` file we used in the getting started example:

.. code-block:: cmake

   PROJECT(FoundationTimer)
   CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

   INCLUDE(conanbuildinfo.cmake)
   CONAN_BASIC_SETUP()
   
   ADD_EXECUTABLE(timer timer.cpp)
   TARGET_LINK_LIBRARIES(timer ${CONAN_LIBS})
   

- **include(conanbuildinfo.cmake)** will include the file generated by our **cmake** [generator]
- **CONAN_BASIC_SETUP()** call will asign to **CMake** all the needed variables for linking with our requirements. 
- **${CONAN_LIBS}** contains the libraries to link with. So TARGET_LINK_LIBRARIES, works just fine.


Let's take a look to the generated ``conanbuildinfo.cmake`` file:


.. code-block:: cmake

   SET(CONAN_INCLUDE_DIRS "/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/include"
         "/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/dd8a0e4171607d74dee9fd0c51153a922d849535/include"
         "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/include" ${CONAN_INCLUDE_DIRS})
   SET(CONAN_LIB_DIRS "/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/lib"
            "/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/dd8a0e4171607d74dee9fd0c51153a922d849535/lib"
            "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/lib" ${CONAN_LIB_DIRS})
   SET(CONAN_BIN_DIRS "/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/bin"
            "/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/dd8a0e4171607d74dee9fd0c51153a922d849535/bin"
            "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/bin" ${CONAN_BIN_DIRS})
   SET(CONAN_LIBS PocoUtil PocoXML PocoJSON PocoMongoDB PocoNet PocoCrypto PocoData PocoDataSQLite PocoZip PocoFoundation pthread dl rt ssl crypto z ${CONAN_LIBS})
   SET(CONAN_DEFINES -DPOCO_STATIC=ON
            -DPOCO_NO_AUTOMATIC_LIBS ${CONAN_DEFINES})
   SET(CONAN_CXX_FLAGS " ${CONAN_CXX_FLAGS}")
   SET(CONAN_SHARED_LINK_FLAGS " ${CONAN_SHARED_LINK_FLAGS}")
   SET(CONAN_EXE_LINKER_FLAGS " ${CONAN_EXE_LINKER_FLAGS}")
   SET(CONAN_C_FLAGS " ${CONAN_C_FLAGS}")
   
   SET(CONAN_INCLUDE_DIRS_POCO "/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/include")
   SET(CONAN_LIB_DIRS_POCO "/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/lib")
   SET(CONAN_BIN_DIRS_POCO "/home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/bin")
   SET(CONAN_LIBS_POCO PocoUtil PocoXML PocoJSON PocoMongoDB PocoNet PocoCrypto PocoData PocoDataSQLite PocoZip PocoFoundation pthread dl rt)
   SET(CONAN_DEFINES_POCO -DPOCO_STATIC=ON
            -DPOCO_NO_AUTOMATIC_LIBS)
   SET(CONAN_CXX_FLAGS_POCO "")
   SET(CONAN_SHARED_LINK_FLAGS_POCO "")
   SET(CONAN_EXE_LINKER_FLAGS_POCO "")
   SET(CONAN_C_FLAGS_POCO "")
   
   SET(CONAN_INCLUDE_DIRS_ZLIB "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/include")
   SET(CONAN_LIB_DIRS_ZLIB "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/lib")
   SET(CONAN_BIN_DIRS_ZLIB "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/bin")
   SET(CONAN_LIBS_ZLIB z)
   SET(CONAN_DEFINES_ZLIB )
   SET(CONAN_CXX_FLAGS_ZLIB "")
   SET(CONAN_SHARED_LINK_FLAGS_ZLIB "")
   SET(CONAN_EXE_LINKER_FLAGS_ZLIB "")
   SET(CONAN_C_FLAGS_ZLIB "")
   
   SET(CONAN_INCLUDE_DIRS_OPENSSL "/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/dd8a0e4171607d74dee9fd0c51153a922d849535/include")
   SET(CONAN_LIB_DIRS_OPENSSL "/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/dd8a0e4171607d74dee9fd0c51153a922d849535/lib")
   SET(CONAN_BIN_DIRS_OPENSSL "/home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/dd8a0e4171607d74dee9fd0c51153a922d849535/bin")
   SET(CONAN_LIBS_OPENSSL ssl crypto)
   SET(CONAN_DEFINES_OPENSSL )
   SET(CONAN_CXX_FLAGS_OPENSSL "")
   SET(CONAN_SHARED_LINK_FLAGS_OPENSSL "")
   SET(CONAN_EXE_LINKER_FLAGS_OPENSSL "")
   SET(CONAN_C_FLAGS_OPENSSL "")

   
   MACRO(CONAN_BASIC_SETUP)
       CONAN_CHECK_COMPILER()
       CONAN_OUTPUT_DIRS_SETUP()
       CONAN_FLAGS_SETUP()
   ENDMACRO()
   # ... macros code...


As we can see, conan is preparing some variables:

* ``CONAN_INCLUDE_DIRS``: The headers folders from the requirements.
* ``CONAN_LIB_DIRS``: The library folders from the requirements.
* ``CONAN_BIN_DIRS``: The binary folders from the requirements.
* ``CONAN_LIBS``: The name of the libs we have to link with.
* ``CONAN_DEFINES``: Defines, observe that two are defined, POCO_STATIC and POCO_NO_AUTOMATIC_LIBS, that correspond to options_.
* ``CONAN_C_FLAGS``: Flags for C. Not specified for Poco nor its requirements.
* ``CONAN_CXX_FLAGS``: Flags for CXX. Not specified for Poco nor its requirements.
* ``CONAN_SHARED_LINK_FLAGS``: Shared flags for CXX. Not specified for Poco nor its requirements.
* ``CONAN_EXE_LINKER_FLAGS``: Exe linker flags for CXX. Not specified for Poco nor its requirements.


Conan also provides the same variables isolated for each requirement, so you can handle the requirements individually:  **CONAN_INCLUDE_DIRS_POCO**, **CONAN_INCLUDE_DIRS_OPENSSL**,  etc


All these variables are 'injected' to corresponding **CMake** functions/variables *(INCLUDE_DIRECTORIES, LINK_DIRECTORIES, ADD_DEFINITIONS, CMAKE_CXX_FLAGS...etc)* when you call **CONAN_BASIC_SETUP()** in your ``CMakeLists.txt`` file.

.. _gcc_generator:

*gcc*
_____

Now we are going to compile the :ref:`getting started<getting_started>` example using **gcc** instead of the **cmake** generator.

.. note:: 
   
   We have only tested the gcc generator in linux with the gcc compiler. But maybe it works with MinGW in Windows or even clang in OSx. Try it and let us know. :D


Open ``conanfile.txt`` and change (or add) **gcc** generator:

    
.. code-block:: text

   [requires]
   Poco/1.6.1@lasote/stable
   
   [generators]
   cmake
   gcc
   
Install the requirements

.. code-block:: bash

   $ conan install


.. note::

   Remember, if you don't specify settings in **install command** with **-s**, conan will use the detected defaults. You can always change them by editing the ``~/.conan/conan.conf`` or override them with "-s" parameters.  
 
   So, now type **conan install** and you are done! 


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

   $ cd bin
   $ ./timer 
    Callback called after 249 milliseconds.
    Callback called after 749 milliseconds.
    Callback called after 1249 milliseconds.
    ...

*visual_studio*
_______________


The generator **visual_studio** creates a file named ``conanbuildinfo.props`` that can be imported to your *Visual Studio* project.
Check the section :ref:`Integrations/Visual Studio<visual_studio>` to read more about this generator.


*xcode*
_______


The generator **xcode** creates a file named ``conanbuildinfo.xcconfig`` that can be imported to your *XCode* project.
Check the section :ref:`Integrations/XCode <xcode>` to read more about this generator.

*txt*
_____


Maybe you need a more generic ``conanbuildinfo`` file to use with another build system or script.

.. note:: 
   
   Do you miss support for your build system? Tell us what you need. info@conan.io
     
Specify **txt** generator:

   .. code-block:: text
   
      [requires]
      Poco/1.6.1@lasote/stable
      
      [generators]
      txt
   
Install the requirements

.. code-block:: bash

   $ conan install

And it's the generated file, with the same information as CMake and gcc, but in a generic format:

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
   


Options
.......

Options are intended for package specific configurations.

.. note:: 
   
   You can check the available options for a package with "conan search -v" command: 
      
      $ conan search Poco/1.6.1@lasote/stable -v -r conan.io
      

We are going to adjust the option **"poco_static"** to use the shared library from POCO.

You can set the options for your requirements this way:

   .. code-block:: text
   
      [requires]
      Poco/1.6.1@lasote/stable
      
      [generators]
      gcc
      
      [options]
      Poco:poco_static=False # Just the name of the library ":" and the option name
      OpenSSL:shared=True
      

Install the requirements and compile

.. code-block:: bash

   $ conan install


.. code-block:: bash

   $ mkdir bin
   $ g++ timer.cpp @conanbuildinfo.gcc -o bin/timer
   

What happened? The **conan install** command receives the different options and resolves the right packages to link to, meaninng the ones that are the generated with **Poco:poco_static=False** and **OpenSSL:shared=True**

So if we inspect the **objdump** tool (available in linux) we can see in *Dynamic section* that the executable used the shared libraries from POCO and OpenSSL:

.. code-block:: bash

   $ cd bin
   $ objdump -p timer
    ...
    Dynamic Section:
     NEEDED               libPocoUtil.so.31
     NEEDED               libPocoXML.so.31
     NEEDED               libPocoJSON.so.31
     NEEDED               libPocoMongoDB.so.31
     NEEDED               libPocoNet.so.31
     NEEDED               libPocoCrypto.so.31
     NEEDED               libPocoData.so.31
     NEEDED               libPocoDataSQLite.so.31
     NEEDED               libPocoZip.so.31
     NEEDED               libPocoFoundation.so.31
     NEEDED               libpthread.so.0
     NEEDED               libdl.so.2
     NEEDED               librt.so.1
     NEEDED               libssl.so.1.0.0
     NEEDED               libcrypto.so.1.0.0
     NEEDED               libstdc++.so.6
     NEEDED               libm.so.6
     NEEDED               libgcc_s.so.1
     NEEDED               libc.so.6
   
     

Imports
.......

In the options_ section we got shared libraries from Poco and OpenSSL just by changing the value of the options.

This example was run in linux, where libraries can be found by the linker just by passing the library paths parameters.
But there are some differences between shared libraries on linux (\*.so), windows (\*.dll) and MacOS (\*.dylib). 

We can assume, for brevity, that **\*.dll**  and **\*.dylib** should be copied to the user's binary directory.

.. note::
   
    You can read the :ref:`Tip about rpaths<protip_shared>` to learn more about shared libraries and how conan handles them.


We can easily do that with the **[imports]** section in ``conanfile.txt``. Let's try it.

Edit the ``conanfile.txt`` file and paste the **[imports]** section

  
.. code-block:: text
   
      [requires]
      Poco/1.6.1@lasote/stable
      
      [generators]
      gcc
      
      [options]
      Poco:poco_static=False
      OpenSSL:shared=True
      
      [imports]
      bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
      lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder


.. note::
   
    You can explore the package folder in your local storage (printed after the install command) and look where the shared libraries are. It's common that **\*.dll** are copied in **/bin**
    the rest of the libraries should be found in the **/lib** folder. But it's just a convention, you can use a different one for your packages if you want.



Install the requirements

.. code-block:: bash

   $ conan install
   
   
Now look at the ``lib/`` folder of your project and verify that the needed shared libraries are there.

As you can see, the **[imports]** section is a very generic way to import files from your requirements to your project. 

Maybe conan could also be useful for packaging applications and copying the result executables to your bin folder, or for copying assets, test static files...etc. 

Conan is a pretty generic solution for package management, not just C/C++ or libraries.



.. _protip_shared:

.. tip:: **Pro Tip: Shared libraries & rpaths**

   In **UNIX** based operating systems like **Linux** and **OSx** there is something called **rpath** (run-time search path) that is used to locate the **shared libraries** that another library or executable needs for execution.
   
   The **rpath** is encoded inside dynamic libraries and executables and helps the linker to find its required shared libraries.
   
   Imagine that we have an executable **my_exe** that requires a shared library **shared_lib_1**, and **shared_lib_1**, in turn, requires another **shared_lib_2**.
   
   So the **rpaths** values could be:
   
   ============ ===================== 
   File         rpath   
   ============ =====================
   my_exe       /path/to/shared_lib_1 
   shared_lib_1 /path/to/shared_lib_2
   shared_lib_2 
   ============ =====================
   
   In **linux** **rpath** is just an option, which means the, if the linker doesn't find the library in **rpath**, it will continue the search in **system defaults paths** (LD_LIBRARY_PATH... etc)
   
   But in **OSx** with **dylibs** it doesn't work like that. In OSx, if the linker detects that an **rpath** is invalid (the file does not exist there), it will fail. In OSx, libraries are built with the hard restriction of knowing (before installing them) where (in which folder) they will be installed.
   
   Some dependency managers try to ride out this OSx restriction by changing the rpaths or making the rpaths relative to the binary.
   
   For **conan** these are not suitable solutions because libraries are not all together in a directory we can refer to and we don't want it, because it's not good at all for package management and reuse.
   
   So for **OSx** conan requires **dylibs** to be built having an rpath just with the name of the required library (just the name, without path).
   
   With conan, **rpaths** values should be:
   
   ================== ===================== 
   File               rpath   
   ================== =====================
   my_exe             shared_lib_1.dylib
   shared_lib_1.dylib shared_lib_2.dylib
   shared_lib_2.dylib 
   ================== =====================
   
   The only limitation of this convention is that **dylibs** have to be copied to the folder of our executable, just like **dll** files in windows.
   
   In **linux** you don't need to care about **rpath** but you should know that, by default, the current directory (./) is not in the **LD_LIBRARY_PATH** so it's useless if you copy ***.so** files in your executable folder, unless you modify the LD_LIBRARY_PATH.
   
   That's why we import **dll** and **dylib** files to our project with the [imports] section.
  
