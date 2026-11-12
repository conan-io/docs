.. _conanfile_txt:

Installing dependencies
-----------------------

In :ref:`Getting started<getting_started>` we used the :command:`conan install` command to download the
**Poco** library and build an example.

If you inspect the ``conanbuildinfo.cmake`` file that was created when running :command:`conan install`,
you can see there that there are many CMake variables declared. For example
``CONAN_INCLUDE_DIRS_ZLIB``, that defines the include path to the zlib headers, and
``CONAN_INCLUDE_DIRS`` that defines include paths for all dependencies headers.

.. image:: /images/local_cache_cmake.png
   :height: 400 px
   :width: 500 px
   :align: center

If you check the full path that each of these variables defines, you will see that it points to a folder under your ``<userhome>``
folder. Together, these folders are the **local cache**. This is where package recipes and binary
packages are stored and cached, so they don't have to be retrieved again. You can inspect the
**local cache** with :command:`conan search`, and remove packages from it with
:command:`conan remove` command.

If you navigate to the folders referenced in ``conanbuildinfo.cmake`` you will find the
headers and libraries for each package.

If you execute a :command:`conan install Poco/1.9.0@pocoproject/stable` command in your shell, Conan will
download the Poco package and its dependencies (*OpenSSL/1.0.2l@conan/stable* and
*zlib/1.2.11@conan/stable*) to your local cache and print information about the folder where
they are installed. While you can install each of your dependencies individually like that,
the recommended approach for handling dependencies is to use a ``conanfile.txt`` file.
The structure of ``conanfile.txt`` is described below.

Requires
........

The required dependencies should be specified in the **[requires]** section.
Here is an example:

.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable

Where:

  - ``Poco`` is the name of the package which is usually the same as the project/library.
  - ``1.9.0`` is the version which usually matches that of the packaged project/library. This can be any
    string; it does not have to be a number, so, for example, it could indicate if this is a "develop" or "master" version.
    Packages can be overwritten, so it is also OK to have packages like "nightly" or "weekly", that
    are regenerated periodically.
  - ``pocoproject`` is the owner of this package. It is basically a namespace that allows different users to have their own packages for
    the same library with the same name.
  - ``stable`` is the channel. Channels provide another way to have different variants of packages for the same library
    and use them interchangeably. They usually denote the maturity of the package as an arbitrary
    string such as "stable" or "testing", but they can be used for any purpose such as package revisions (e.g., the
    library version has not changed, but the package recipe has evolved).

Overriding requirements
_______________________

You can specify multiple requirements and **override** transitive "require's
requirements". In our example, Conan installed the Poco package and all its requirements
transitively:

  * **OpenSSL/1.0.2l@conan/stable**
  * **zlib/1.2.11@conan/stable**

.. tip::

    This is a good example of overriding requirements given the importance of keeping
    the OpenSSL library updated.

Consider that a new release of the OpenSSL library has been released, and a new corresponding Conan package is
available. In our example, we do not need to wait until `pocoproject`_ (the author) generates a new package of POCO that
includes the new OpenSSL library.

We can simply enter the new version in the **[requires]** section:

.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable
    OpenSSL/1.0.2p@conan/stable

The second line will override the OpenSSL/1.0.2l required by POCO with the currently non-existent **OpenSSL/1.0.2p**.

Another example in which we may want to try some new zlib alpha features: we could replace the zlib
requirement with one from another user or channel.

.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable
    OpenSSL/1.0.2p@conan/stable
    zlib/1.2.11@otheruser/alpha

.. note::

    You can use environment variable :ref:`CONAN_ERROR_ON_OVERRIDE<env_vars_conan_error_on_override>`
    to raise an error for every overriden requirement not marked explicitly with the ``override`` keyword.


.. _generators:

Generators
..........

Conan reads the **[generators]** section from ``conanfile.txt`` and creates files for each generator
with all the information needed to link your program with the specified requirements. The
generated files are usually temporary, created in build folders and not committed to version
control, as they have paths to local folders that will not exist in another machine. Moreover, it is very
important to highlight that generated files match the given configuration (Debug/Release,
x86/x86_64, etc) specified when running :command:`conan install`. If the configuration changes, the files will
change accordingly.

For a full list of generators, please refer to the complete :ref:`generators<generators_reference>` reference.

.. _options_txt:

Options
.......

We have already seen that there are some **settings** that can be specified during installation. For
example, :command:`conan install .. -s build_type=Debug`. These settings are typically a project-wide
configuration defined by the client machine, so they cannot have a default value in the recipe. For
example, it doesn't make sense for a package recipe to declare "Visual Studio" as a default compiler
because that is something defined by the end consumer, and unlikely to make sense if they are
working in Linux.

On the other hand, **options** are intended for package specific configuration that can be set to a
default value in the recipe. For example, one package can define that its default linkage is static,
and this is the linkage that should be used if consumers don't specify otherwise.

.. note:: 

    You can see the available options for a package by inspecting the recipe with :command:`conan get <reference>` command:

    .. code-block:: text

        $ conan get Poco/1.9.0@pocoproject/stable

    To see only specific fields of the recipe you can use the :command:`conan inspect` command instead:

    .. code-block:: text

        $ conan inspect Poco/1.9.0@pocoproject/stable -a=options
        $ conan inspect Poco/1.9.0@pocoproject/stable -a=default_options

For example, we can modify the previous example to use dynamic linkage instead of the default one, which was static, by editing the
**[options]** section in ``conanfile.txt``:

.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable

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

As an alternative to defining options in the ``conanfile.txt`` file, you can specify them directly in the
command line:

.. code-block:: bash

    $ conan install .. -o Poco:shared=True -o OpenSSL:shared=True
    # or even with wildcards, to apply to many packages
    $ conan install .. -o *:shared=True

Conan will install the binaries of the shared library packages, and the example will link with them. You can again inspect the different binaries installed.
For example, :command:`conan search zlib/1.2.8@conan/stable`.

Finally, launch the executable:

.. code-block:: bash

    $ ./bin/md5

What happened? It fails because it can't find the shared libraries in the path. Remember that shared
libraries are used at runtime, so the operating system, which is running the application, must be able to locate them.

We could inspect the generated executable, and see that it is using the shared libraries. For
example, in Linux, we could use the `objdump` tool and see the *Dynamic section*:

.. code-block:: bash

    $ cd bin
    $ objdump -p md5
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

There are some differences between shared libraries on Linux (\*.so), Windows (\*.dll) and MacOS
(\*.dylib). The shared libraries must be located in a folder where they can be found, either by
the linker, or by the OS runtime.

You can add the libraries' folders to the path (LD_LIBRARY_PATH environment variable
in Linux, DYLD_LIBRARY_PATH in OSX, or system PATH in Windows), or copy those shared libraries to
some system folder where they can be found by the OS. But these operations are only related to the deployment or
installation of apps; they are not relevant during development. Conan is intended for developers, so
it avoids such manipulation of the OS environment.

In Windows and OSX, the simplest approach is to copy the shared libraries to the executable
folder, so they are found by the executable, without having to modify the path.

This is done using the **[imports]** section in ``conanfile.txt``.

To demonstrate this, edit the ``conanfile.txt`` file and paste the following **[imports]** section:

.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable
    
    [generators]
    cmake
    
    [options]
    Poco:shared=True
    OpenSSL:shared=True
    
    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder

.. note::

    You can explore the package folder in your local cache (~/.conan/data) and see where the shared
    libraries are. It is common that **\*.dll** are copied to **/bin**. The rest of the libraries
    should be found in the **/lib** folder, however, this is just a convention, and different layouts are
    possible.

Install the requirements (from the ``build`` folder), and run the binary again:

.. code-block:: bash

    $ conan install ..
    $ ./bin/md5

Now look at the ``build/bin`` folder and verify that the required shared libraries are there.

As you can see, the **[imports]** section is a very generic way to import files from your
requirements to your project. 

This method can be used for packaging applications and copying the resulting executables to your bin
folder, or for copying assets, images, sounds, test static files, etc. Conan is a generic solution
for package management, not only for (but focused on) C/C++ libraries.

.. seealso::

    To learn more about working with shared libraries, please refer to :ref:`Howtos/Manage shared libraries<manage_shared>`.


.. _`pocoproject`: https://bintray.com/pocoproject/conan/Poco%3Apocoproject
