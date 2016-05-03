.. _conanfile_txt:

Installing dependencies
-----------------------

In :ref:`Getting started<getting_started>` we used **conan install** to download the **POCO** library and build an example.
   

.. note:: When you execute the **conan install** command, the following happens:

    - It reads ``conanfile.txt`` from the current directory or the directory pointed by the command.
    - For each **[requires]** entry, conan will check locally for such conan **package recipe** , and if
      it fails, it will try to download the **package recipe** from the server. Each package recipe is
      identified by its reference, as ``Poco/1.7.2@lasote/stable``.
    - Package recipes and package binaries are installed locally in your computer, typically in a
      folder in your user home, called: ``~/.conan/data``, though you can change that configuration too.
    - The requirements will be processed transitively, retrieving package recipes if necessary, taking
      into account the current settings and options, until the full graph of dependencies is computed.
      In the previous example, recipes for **OpenSSL** and **zlib** are retrieved.
    - Once the graph is finished, and all package recipes have been retrieved, the hash (SHA1) 
      or signature of the required binaries is computed.
    - For each package, the corresponding binary, with a reference composed by the package recipe
      reference and the hash (e.g. ``Poco/1.7.2@lasote/stable:63da...3f44``), is searched locally.
    - If it is found locally, then, nothing to do. If it is not found locally, conan will look for it
      in the server, and if found, will retrieve the corresponding package binary from the server.
    - If the package binary is not found in the server, then the process will fail. The user can specify
      some variant of the ``--build`` option to tell conan to build it from sources.
    - Information is collected from the dependency graph, as **libs** to be **linked**, 
      **include directories**, **compile flags** etc. This information is propagated from the
      upstream packages to their dependents.
    - For each specified **[generator]**, conan will generate a file with relevant information
      to build the project and link with the defined dependencies.



If you execute a **conan install** command in your shell, specifying a reference like **Poco/1.7.2@lasote/stable**
instead of nothing or the path to a ``conanfile.txt`` conan will download the Poco package and 
all its dependencies (*OpenSSL/1.0.2g@lasote/stable* and *zlib/1.2.8@lasote/stable*) 
to your conan cache and print information about the folder where they are installed. 
   
You will find two **/lib** and **/include** subfolders with the libraries and headers.
You could handle them manually if you want. But we recommend the usage of a ``conanfile.txt`` instead of directly installing packages.


Requires
........

We put the required dependencies in the **[requires]** section. 
The requirements look like this:

.. code-block:: text

   [requires]
   Poco/1.7.2@lasote/stable
   

Where:

   - ``Poco`` is the name
   - ``1.7.2`` is the version
   - ``lasote`` is the owner of this package version
   - ``stable`` is the channel (there could be several channels for developing, testing, etc.)


Overriding requirements
_______________________


You can specify multiple requirements and you can **override** the "require's requirements".
In our example, conan installed the POCO requirement and all its requirements recursively:

   * **OpenSSL/1.0.2g@lasote/stable**
   * **zlib/1.2.8@lasote/stable**
   
.. tip:: 

    This is a good example to explain requirements overriding. We all know the importance of keeping the OpenSSL library updated.

Now imagine that a new release of OpenSSL library is out, and a new conan package for it is available. 
Do we need to wait until **lasote** generates a new package of POCO that includes the new OpenSSL library?

Not necessarily, just enter the new version in **[requires]**:

.. code-block:: text

   [requires]
   Poco/1.7.2@lasote/stable
   OpenSSL/1.0.2p@lasote/stable

The second line will override the OpenSSL/1.0.2g required by poco, with the (non-existent yet)  **OpenSSL/1.0.2p**

Other example could be, in order to try out some new zlib alpha features, we could replace the Zlib requirement with one from another user or channel. 

.. code-block:: text

   [requires]
   Poco/1.7.2@lasote/stable
   OpenSSL/1.0.2p@lasote/stable
   zlib/1.2.9@otheruser/alpha


.. _generators:

Generators
..........

Conan reads the **[generators]** section from ``conanfile.txt`` and creates one file for each generator with all the necessary information to link your program with the specified requirements.


*cmake*
_______

The **cmake** generator creates a file named ``conanbuildinfo.cmake`` that can be imported from your *CMakeLists.txt*.
Check the section :ref:`Integrations/CMake <cmake>` to read more about this generator.


*visual_studio*
_______________

The **visual_studio** generator creates a file named ``conanbuildinfo.props`` that can be imported to your *Visual Studio* project.
Check the section :ref:`Integrations/Visual Studio<visual_studio>` to read more about this generator.


*xcode*
_______

The **xcode** generator creates a file named ``conanbuildinfo.xcconfig`` that can be imported to your *XCode* project.
Check the section :ref:`Integrations/XCode <xcode>` to read more about this generator.

*other*
_______

There are some other generators, check them in :ref:`Integrations <integrations>`. You might
use the generic :ref:`text generator <other_generator>`, or maybe even
:ref:`create and share a new generator <dyn_generators>`
   

Options
.......

Options are intended for package specific configurations.

.. note:: 
   
   You can search and see the available options for a package with "conan search -x" command: 
      
      $ conan search Poco/1.7.2@lasote/stable -x
      

We are going to adjust the option **"shared"** to use the shared library from POCO.

You can set the options for your requirements this way:

.. code-block:: text

    [requires]
    Poco/1.7.2@lasote/stable
    
    [generators]
    cmake
    
    [options]
    Poco:shared=True # Just the name of the library ":" and the option name
    OpenSSL:shared=True
      

Install the requirements and compile from the build folder (change build command if not Win):

.. code-block:: bash

    $ conan install ..
    $ cmake .. -G "Visual Studio 14 Win64"
    $ cmake --build . --config Release

Conan will install the shared library packages binaries, and the example will link with them.

Finally, launch the executable:

.. code-block:: bash

    $ ./bin/timer

What happened? It fails because it can't find the shared libraries in the path.

We could inspect the generated executable, and see that it is using the shared libraries.
For example in Linux, we could use the**objdump** tool and see in *Dynamic section*:

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

There are some differences between shared libraries on linux (\*.so), windows (\*.dll) and MacOS (\*.dylib).
The shared libraries must be located in some folder where they can be found, either by the linker,
or by the OS runtime.

It is possible to add the folders of the libraries to the system Path, or copy those shared libraries
to some system folder, so they are found by the OS. But those are typical operations of deploys or final
installation of apps, not desired while developing, and conan is intended for developers, so it
tries not to mess with the OS.

For linux, it is not necessary, as the linker is able to do the job, but in Windows and OSX, 
the simplest approach is just to copy the shared libraries to the executable folder, so
they are found by the exe, without having to modify the path.

.. note::
   
    You can read the :ref:`Tip about rpaths<protip_shared>` to learn more about shared libraries and how conan handles them.


We can easily do that with the **[imports]** section in ``conanfile.txt``. Let's try it.

Edit the ``conanfile.txt`` file and paste the **[imports]** section:

  
.. code-block:: text
   
    [requires]
    Poco/1.7.2@lasote/stable
    
    [generators]
    cmake
    
    [options]
    Poco:shared=True
    OpenSSL:shared=True
    
    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder


.. note::
   
    You can explore the package folder in your local cache (~/.conan/data) and look where the shared libraries are. It is common that **\*.dll** are copied in **/bin**
    the rest of the libraries should be found in the **/lib** folder. But it's just a convention, different layouts are possible.



Install the requirements (from the mytimer/build folder), and run the binary again:

.. code-block:: bash

   $ conan install ..
   $ ./bin/timer
   
   
Now look at the ``mytimer/build/bin`` folder and verify that the needed shared libraries are there.

As you can see, the **[imports]** section is a very generic way to import files from your requirements to your project. 

This method can be used for packaging applications and copying the result executables to your bin folder, or for copying assets, images, sounds, test static files, etc. 

Conan is a generic solution for package management, not only for C/C++ or libraries.



.. _protip_shared:

.. tip:: **Pro Tip: Shared libraries & rpaths**

   In **UNIX** based operating systems like **Linux** and **OSx**, there is something called **rpath** (run-time search path) that is used to locate the **shared libraries** that another library or executable needs for execution.
   
   The **rpath** is encoded inside dynamic libraries and executables and helps the linker to find its required shared libraries.
   
   Imagine that we have an executable, **my_exe**, that requires a shared library, **shared_lib_1**, and **shared_lib_1**, in turn, requires another **shared_lib_2**.
   
   So the **rpaths** values could be:
   
   ============ ===================== 
   File         rpath   
   ============ =====================
   my_exe       /path/to/shared_lib_1 
   shared_lib_1 /path/to/shared_lib_2
   shared_lib_2 
   ============ =====================
   
   In **linux** **rpath** is just an option, which means that, if the linker doesn't find the library in **rpath**, it will continue the search in **system defaults paths** (LD_LIBRARY_PATH... etc)
   
   But in **OSx** with **dylibs** it doesn't work like that. In OSx, if the linker detects that an **rpath** is invalid (the file does not exist there), it will fail. In OSx, libraries are built with the hard restriction of knowing (before installing them) where (in which folder) they will be installed.
   
   Some dependency managers try to ride out this OSx restriction by changing the rpaths or making the rpaths relative to the binary.
   
   For **conan**, these are not suitable solutions because libraries are not all together in a directory we can refer to and we don't want that, because it's not good at all for package management and reuse.
   
   So, for **OSx**, conan requires **dylibs** to be built having an rpath with only the name of the required library (just the name, without path).
   
   With conan, **rpaths** values should be:
   
   ================== ===================== 
   File               rpath   
   ================== =====================
   my_exe             shared_lib_1.dylib
   shared_lib_1.dylib shared_lib_2.dylib
   shared_lib_2.dylib 
   ================== =====================
   
   The only limitation of this convention is that **dylibs** have to be copied to the folder of our executable, just like **dll** files in windows.
   
   In **linux**, you don't need to care about **rpath** but you should know that, by default, the current directory (./) is not in the **LD_LIBRARY_PATH** so it's useless if you copy ***.so** files in your executable folder, unless you modify the LD_LIBRARY_PATH.
   
   That's why we import **dll** and **dylib** files to our project with the [imports] section.
  
