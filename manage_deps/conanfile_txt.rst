.. _conanfile_txt:

Installing dependencies
-----------------------

In :ref:`Getting started<getting_started>` we used ``$ conan install`` command to download the **POCO** library and build an example.
   
Please take a moment to inspect the generated ``conanbuildinfo.cmake`` file that was created when we did ``conan install``
You can see there that there are many CMake variables declared. For example you can see variables like ``CONAN_INCLUDE_DIRS_ZLIB``, which defines the include path to the ZLib headers, or ``CONAN_INCLUDE_DIRS`` that defines include paths for all dependencies headers.

.. image:: /images/local_cache_cmake.png
   :height: 400 px
   :width: 500 px
   :align: center

If you check the full path, you will see that they are pointing to a folder in your ``<userhome>`` folder, this is called the **conan local cache**. It is the place where package recipes and package binaries are stored and cached, so they don't have to be retrieved again. You can inspect it with ``conan search``, and you can also remove packages from it with ``conan remove`` command.

If you navigate to the paths pointed by the ``conanbuildinfo.cmake`` you will be able to see the headers and the libraries for each package.

If you execute a ``conan install Poco/1.7.3@lasote/stable`` command in your shell, conan will download the Poco package and its dependencies (*OpenSSL/1.0.2g@lasote/stable* and *zlib/1.2.8@lasote/stable*) to your conan cache and print information about the folder of the local cache where they are installed. You could handle them manually if you want. But the recommended approach is using a ``conanfile.txt``.


Requires
........

We put the required dependencies in the **[requires]** section. 
The requirements look like this:

.. code-block:: text

   [requires]
   Poco/1.7.3@lasote/stable
   

Where:

   - ``Poco`` is the name of the package, usually the same of the project/library
   - ``1.7.3`` is the version, usually matching the one of the packaged project/library. Can be any string, not necessarily a number, so it is possible to have a "develop" or "master" version. Packages can be overwritten, so it is also OK to have packages like "nightly" or "weekly", that are regenerated periodically.
   - ``lasote`` is the owner of this package version. It is basically a namespace that allows different users to have their own packages for the same library with the same name, and interchange them. So you can easily for example upload a certain libray under your own user name "lasote", and later those packages can be uploaded without modifications to another official, group or company username.
   - ``stable`` is the channel. Channels also allow to have different packages for the same library and use them interchangeably. They usually denote the maturity of the package, as an arbitrary string: "stable", "testing", but it can be used for any purpose, like package revisions (the library version has not changed, but the package recipe has evolved) 


Overriding requirements
_______________________


You can specify multiple requirements and you can **override** the transitive "require's requirements".
In our example, conan installed the POCO package and all its requirements transitively:

   * **OpenSSL/1.0.2g@lasote/stable**
   * **zlib/1.2.8@lasote/stable**
   
.. tip:: 

    This is a good example to explain requirements overriding. We all know the importance of keeping the OpenSSL library updated.

Now imagine that a new release of OpenSSL library is out, and a new conan package for it is available. 
Do we need to wait until **lasote** generates a new package of POCO that includes the new OpenSSL library?

Not necessarily, just enter the new version in **[requires]**:

.. code-block:: text

   [requires]
   Poco/1.7.3@lasote/stable
   OpenSSL/1.0.2p@lasote/stable

The second line will override the OpenSSL/1.0.2g required by poco, with the (non-existent yet)  **OpenSSL/1.0.2p**

Other example could be, in order to try out some new zlib alpha features, we could replace the Zlib requirement with one from another user or channel. 

.. code-block:: text

   [requires]
   Poco/1.7.3@lasote/stable
   OpenSSL/1.0.2p@lasote/stable
   zlib/1.2.9@otheruser/alpha


.. _generators:

Generators
..........

Conan reads the **[generators]** section from ``conanfile.txt`` and creates files for each generator with all the necessary information to link your program with the specified requirements. The generated files are usually temporary, created in build folders and not committed to version control, as they have paths to local folder that will not exist in another machin. Also, it is very important to highlight that generated files match the given configuration (Debug/Release, x86/x86_64, etc), specified at ``conan install`` time. If the configuration changes, the files will change.


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

We have already seen that there are some **settings** that can be specified at install, like ``conan install -s build_type=Debug``. The settings are typically project wide configuration that is defined by the client machine. So they cannot be defaulted. It doesn't make sense that a package defines that is using by default a "Visual Studio" compiler, because that is something defined by the end consumer, and unlikely to make sense if they are working in Linux.

On the other hand, **options** are intended for package specific configuration, that can be defaulted. For example, one package can define that its default linkage is static, and such default will be used if consumers don't specify otherwise.

.. note:: 
   
   You can search and see the available options for a package with "conan search <reference>" command: 
      
      $ conan search Poco/1.7.3@lasote/stable
      

As an example, we can modify the previous example to use dynamic linkage instead of the default one, which was static. Just edit the ``conanfile.txt``:

.. code-block:: text

    [requires]
    Poco/1.7.3@lasote/stable
    
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
You can again inspect the different installed binaries, e.g. ``conan search zlib/1.2.8@lasote/stable``.

Finally, launch the executable:

.. code-block:: bash

    $ ./bin/timer

What happened? It fails because it can't find the shared libraries in the path. Remember that shared libraries are used at runtime, and the should be locatable by the OS, which is the one running the application.

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

In Windows and OSX, the simplest approach is just to copy the shared libraries to the executable folder, so
they are found by the executable, without having to modify the path.

We can easily do that with the **[imports]** section in ``conanfile.txt``. Let's try it.

Edit the ``conanfile.txt`` file and paste the following **[imports]** section:

  
.. code-block:: text
   
    [requires]
    Poco/1.7.3@lasote/stable
    
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



Install the requirements (from the ``mytimer/build`` folder), and run the binary again:

.. code-block:: bash

   $ conan install ..
   $ ./bin/timer
   
   
Now look at the ``mytimer/build/bin`` folder and verify that the needed shared libraries are there.

As you can see, the **[imports]** section is a very generic way to import files from your requirements to your project. 

This method can be used for packaging applications and copying the result executables to your bin folder, or for copying assets, images, sounds, test static files, etc. Conan is a generic solution for package management, not only for C/C++ or libraries.



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
   
   But in **OSX** with **dylibs** it doesn't work like that. In OSX, if the linker detects that an **rpath** is invalid (the file does not exist there), it will fail. In OSX, libraries are built with the hard restriction of knowing (before installing them) where (in which folder) they will be installed.
   
   Some dependency managers try to ride out this OSX restriction by changing the rpaths or making the rpaths relative to the binary.
   
   For **conan**, these are not suitable solutions because libraries are not all together in a directory we can refer to and we don't want that, because it's not good at all for package management and reuse.
   
   So, for **OSX**, conan requires **dylibs** to be built having an rpath with only the name of the required library (just the name, without path).
   
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
  
