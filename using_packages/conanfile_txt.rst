.. _conanfile_txt:

Installing dependencies
-----------------------

In :ref:`Getting started<getting_started>` we used :command:`conan install` command to download the
**Poco** library and build an example.

Please take a moment to inspect the generated ``conanbuildinfo.cmake`` file that was created when we
did :command:`conan install`. You can see there that there are many CMake variables declared. For example
``CONAN_INCLUDE_DIRS_ZLIB``, which defines the include path to the ZLib headers, or
``CONAN_INCLUDE_DIRS`` that defines include paths for all dependencies headers.

.. image:: /images/local_cache_cmake.png
   :height: 400 px
   :width: 500 px
   :align: center

If you check the full path, you will see that they are pointing to a folder in your ``<userhome>``
folder, this is called the **local cache**. It is the place where package recipes and binary
packages are stored and cached, so they don't have to be retrieved again. You can inspect the
**local cache** with :command:`conan search`, and you can also remove packages from it with
:command:`conan remove` command.

If you navigate to the paths pointed by the ``conanbuildinfo.cmake`` you will be able to see the
headers and the libraries for each package.

If you execute a :command:`conan install Poco/1.7.8p3@pocoproject/stable` command in your shell, conan will
download the Poco package and its dependencies (*OpenSSL/1.0.2l@conan/stable* and
*zlib/1.2.11@conan/stable*) to your local cache and print information about the folder of the where
they are installed. You could handle them manually if you want. But the recommended approach is
using a ``conanfile.txt``.

Requires
........

We put the required dependencies in the **[requires]** section. 
The requirements look like this:

.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable

Where:

  - ``Poco`` is the name of the package, usually the same of the project/library.
  - ``1.7.3`` is the version, usually matching the one of the packaged project/library. Can be any
    string, not necessarily a number, so it is possible to have a "develop" or "master" version.
    Packages can be overwritten, so it is also OK to have packages like "nightly" or "weekly", that
    are regenerated periodically.
  - ``pocoproject`` is the owner of this package version. It is basically a namespace that allows
    different users to have their own packages for the same library with the same name, and
    interchange them. So, for example, you can easily upload a certain library under your own user
    name "lasote", and later those packages can be uploaded without modifications to another
    official group or company username.
  - ``stable`` is the channel. Channels also allow to have different packages for the same library
    and use them interchangeably. They usually denote the maturity of the package, as an arbitrary
    string: "stable", "testing", but it can be used for any purpose, like package revisions (the
    library version has not changed, but the package recipe has evolved).

Overriding requirements
_______________________

You can specify multiple requirements and you can **override** the transitive "require's
requirements". In our example, conan installed the Poco package and all its requirements
transitively:

  * **OpenSSL/1.0.2l@conan/stable**
  * **zlib/1.2.11@conan/stable**

.. tip::

    This is a good example to explain requirements overriding. We all know the importance of keeping
    the OpenSSL library updated.

Now imagine that a new release of OpenSSL library is out, and a new conan package for it is
available. Do we need to wait until the author `pocoproject`_ generates a new package of POCO that
includes the new OpenSSL library?

Not necessarily, just enter the new version in **[requires]**:

.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable
    OpenSSL/1.0.2p@conan/stable

The second line will override the OpenSSL/1.0.2l required by POCO, with the (non-existent yet)
**OpenSSL/1.0.2p**.

Other example could be, in order to try out some new zlib alpha features, we could replace the zlib
requirement with one from another user or channel.

.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable
    OpenSSL/1.0.2p@conan/stable
    zlib/1.2.11@otheruser/alpha

.. _generators:

Generators
..........

Conan reads the **[generators]** section from ``conanfile.txt`` and creates files for each generator
with all the necessary information to link your program with the specified requirements. The
generated files are usually temporary, created in build folders and not committed to version
control, as they have paths to local folder that will not exist in another machine. Also, it is very
important to highlight that generated files match the given configuration (Debug/Release,
x86/x86_64, etc), specified at :command:`conan install` time. If the configuration changes, the files will
change.

Check the complete :ref:`generators<generators_reference>` reference.

.. _options_txt:

Options
.......

We have already seen that there are some **settings** that can be specified at install time, for
example :command:`conan install . -s build_type=Debug`. The settings are typically a project-wide
configuration, defined by the client machine. So they cannot have a default value in the recipe. For
example, it doesn't make sense for a package recipe to declare as default compiler "Visual Studio",
because that is something defined by the end consumer, and unlikely to make sense if they are
working in Linux.

On the other hand, **options** are intended for package specific configuration, that can be set to a
default value in the recipe. For example, one package can define that its default linkage is static,
and such default will be used if consumers don't specify otherwise.

.. note:: 

    You can see the available options for a package inspecting the recipe with :command:`conan get <reference>` command:

    .. code-block:: text

        $ conan get Poco/1.7.8p3@pocoproject/stable

As an example, we can modify the previous example to use dynamic linkage instead of the default one, which was static. Just edit the
*conanfile.txt*:

.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable

    [generators]
    cmake

    [options]
    Poco:shared=True # PACKAGE:OPTION=VALUE
    OpenSSL:shared=True

Install the requirements and compile from the build folder (change the CMake generator if not in Windows):

.. code-block:: bash

    $ conan install ..
    $ cmake .. -G "Visual Studio 14 Win64"
    $ cmake --build . --config Release

You can also avoid defining the options in the ``conanfile.txt`` and directly define them in the
command line:

.. code-block:: bash

    $ conan install .. -o Poco:shared=True -o OpenSSL:shared=True
    # or even with wildcards, to apply to many packages
    $ conan install .. -o *:shared=True

Conan will install the shared library packages binaries, and the example will link with them. You can again inspect the different installed
binaries, e.g. :command:`conan search zlib/1.2.8@lasote/stable`.

Finally, launch the executable:

.. code-block:: bash

    $ ./bin/timer

What happened? It fails because it can't find the shared libraries in the path. Remember that shared
libraries are used at runtime, and should be locatable by the OS, which is the one running the
application.

We could inspect the generated executable, and see that it is using the shared libraries. For
example in Linux, we could use the `objdump` tool and see in *Dynamic section*:

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

.. _imports_txt:

Imports
.......

There are some differences between shared libraries on linux (\*.so), windows (\*.dll) and MacOS
(\*.dylib). The shared libraries must be located in some folder where they can be found, either by
the linker, or by the OS runtime.

It is possible to add the folders of the libraries to the path (dynamic linker LD_LIBRARY_PATH path
in Linux, DYLD_LIBRARY_PATH in OSX, or system PATH in Windows), or copy those shared libraries to
some system folder, so they are found by the OS. But those are typical operations of deploys or
final installation of apps, not desired while developing, and conan is intended for developers, so
it tries not to mess with the OS.

In Windows and OSX, the simplest approach is just to copy the shared libraries to the executable
folder, so they are found by the executable, without having to modify the path.

We can easily do that with the **[imports]** section in ``conanfile.txt``. Let's try it.

Edit the ``conanfile.txt`` file and paste the following **[imports]** section:

.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable
    
    [generators]
    cmake
    
    [options]
    Poco:shared=True
    OpenSSL:shared=True
    
    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder

.. note::

    You can explore the package folder in your local cache (~/.conan/data) and look where the shared
    libraries are. It is common that **\*.dll** are copied in **/bin** the rest of the libraries
    should be found in the **/lib** folder. But it's just a convention, different layouts are
    possible.

Install the requirements (from the ``mytimer/build`` folder), and run the binary again:

.. code-block:: bash

    $ conan install ..
    $ ./bin/timer

Now look at the ``mytimer/build/bin`` folder and verify that the needed shared libraries are there.

As you can see, the **[imports]** section is a very generic way to import files from your
requirements to your project. 

This method can be used for packaging applications and copying the result executables to your bin
folder, or for copying assets, images, sounds, test static files, etc. Conan is a generic solution
for package management, not only (but focused in) for C/C++ or libraries.

.. seealso::

    Check the section :ref:`Howtos/Manage shared libraries<manage_shared>` to know more about
    working with shared libraries.


.. _`pocoproject`: https://bintray.com/pocoproject/conan/Poco%3Apocoproject
