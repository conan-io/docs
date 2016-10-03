.. _building_hello_world:

Packaging from the source project
=====================================

We will write a package recipe inside a "hello world" library. The package recipe (a 
``conanfile.py`` file), will be stored inside the library, in the
same repository.
The initial source code is a very simple "Hello world" project,
that builds a library and an executable. It can be built and run without conan.

First, let's get the initial source code (you can also just download and copy the source code to a "hello" folder):

.. code-block:: bash

   $ git clone https://github.com/memsharded/hello.git
   $ cd hello

Creating the package recipe
---------------------------------------

Now we will write our package recipe: a **conanfile.py** file in the root folder.
It is the script that defines how the packages are built and used:

.. code-block:: python
   
    from conans import ConanFile, CMake
   
    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        exports = "*"
    
        def build(self):
            cmake = CMake(self.settings)
            self.run('cmake %s %s' % (self.conanfile_directory, cmake.command_line))
            self.run("cmake --build . %s" % cmake.build_config)
    
        def package(self):
            self.copy("*.h", dst="include")
            self.copy("*.lib", dst="lib", src="lib")
            self.copy("*.a", dst="lib", src="lib")
    
        def package_info(self):
            self.cpp_info.libs = ["hello"]
           
 
This ``conanfile.py`` uses the ``conanfile_directory`` property to point to the project, so it
can be built from elsewhere, out-of-source builds, etc.
      
This are the basics of this file:

* A package ``name`` and ``version`` are always required in ``conanfile.py``. 

* The ``settings`` field defines a set of predefined variables that affect the binary packages.
  The package recipe will generate different packages for different OSs and compilers, also depending on
  whether the ``build_type`` is Debug or Release, or the architecture is 32 or
  64 bits. The possible values of those settings are also pre-defined.

* The ``exports`` field is optional. It defines which auxiliary files will be exported together with
  this **conanfile.py** file. All those 'export' files with the **conanfile.py** compose the **package recipe**.

* The ``build()`` method just builds the package, invoking CMake. The first line is the project creation
  and configuration, and the second one is the actual build. They are just plain CMake commands, the
  only additional feature being the translation of the ``settings`` field to CMake syntax inside the
  cmake_command_line and cmake_build_config helpers, which just automatically define things like
  the CMake generator or build flags. You can configure your actual build with regular python syntax,
  using the settings, options, requirements, etc of the package as input.
  Also note that **CMake is not strictly required**. You can build packages directly invoking **make**,
  **MSBuild**, **SCons** or any other build system.

* Then, the ``package()`` method takes charge of extracting the results of the build from the
  build folder and putting them in another package folder. The ``copy()`` helper allows files
  matching certain patterns to be copied to a package destination (typically folders like
  include, lib, bin) from a source origin within the build folder.

* Finally, the ``package_info()`` method defines which configuration is needed, in order to 
  actually consume this package. By default the package ``include``, ``lib`` and ``bin`` folders
  are automatically added to their respective ``cpp_info`` paths. One of the most common usages
  of ``cpp_info`` is to define the library names that package consumers should link with. This
  method can also be configured with python scripting, defining for example different names if your
  building process actually outputs different library names (e.g. debug, mt, 32 suffixes).


Once we have our **conanfile.py** all we have to do to start using this package recipe in our machine
is to ``export`` it to the conan local store:


.. code-block:: bash

   $ conan export demo/testing
   
.. note::

    Note that **demo** is a username. You don't need to register in conan.io to use conan, so any
    other name can be used too. If you intend to upload later this package to the conan.io
    server, maybe it is a good idea to register now, and use now your real username instead of "demo".
    
.. note::

    The ``export="*"`` has matched all the files inside our repository and added them to the package
    recipe. This is the recommended method for package recipes contained in the project folder. Basically,
    it makes a snapshot of the code and stores it in the package recipe, so it doesn't need other
    external sources. If your repository contains temporary or not necessary files, it is a good
    idea to clean them before ``conan export``. Also, a list of comma separated patterns is possible
    in ``exports``, so you can also do the any selection of files you want.
    
The export takes the name and the version from the conanfile, but it can be exported and 
afterwards reused under different user names and channels. In this case, the user is *demo* and
the channel is *testing*. 

Let's check that our package recipe is already in our local cache. You can see also, that it has
no binaries yet. At this stage, we haven't created binaries yet for this package. Binaries will be created
on demand, when another project is using this package, with the settings that such project uses.
It is possible to create binaries and upload them too, so they are ready to be used. Conan
has tools to automate this process too, but lets keep it this way by now:

.. code-block:: bash

   $ conan search
   

.. note::

    That's all. Now our package is defined and installed locally, ready to be used by other projects.
   
    Note that we haven't had to upload it anywhere, it can be fully developed, tested and consumed
    locally. We'll see how to upload it later.


.. _using_package:

Using the package in another project
---------------------------------------

Let's use the package recipe from another project, so we can test that the package we have just
defined is working fine. Create a new project (outside of the previous one). Some sample code
is provided in a repository for convenience, but its contents are very simple: 

.. code-block:: bash

   $ cd ..
   $ git clone https://github.com/memsharded/hello-use.git
   $ cd hello-use
   
This project is just like the first project we did in the :ref:`getting started<getting_started>`,
it just contain a requirement to the package we have just created:

.. code-block:: text

    [requires]
    Hello/0.1@demo/testing
    
    [generators]
    cmake


Lets try to build this project:

.. code-block:: bash

   $ mkdir build && cd build
   $ conan install ..
   
**It will fail**, complaining that a binary does not exist for your current settings. It will
give some hints about what can be done. Basically, if a binary package is not existing, you
have to use the option to build from sources. Lets try again:

.. code-block:: bash

   $ conan install .. --build
   
   
Check :ref:`commands` for full details about the **install --build** options.

Now, try a ``conan search <reference>`` again in order to ensure that a package binary has just been created:

.. code-block:: bash

   $ conan search Hello/0.1@demo/testing
   
So a new package has been built. Lets build and run our project, to check that it is successfully
using and linking to our ``hello`` package


.. code-block:: bash

   $ cmake .. -G "Visual Studio 14 Win64"
   $ cmake --build . --config Release
   $ bin/greet
   Hello World!
   

Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
