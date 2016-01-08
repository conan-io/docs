.. _building_hello_world:

Building a Hello World package
==============================

We will build a package out of a "hello world" library available on github.
It is a very simple project, consisting of some source code files and a CMakeLists.txt
that builds a library and an executable. It can be built and run without conan.

First, let's create a folder for our project and get the source code:

.. code-block:: bash

   $ mkdir hellopack
   $ cd hellopack
   $ git clone https://github.com/memsharded/hello.git

(you can also just download and copy the source code to a "hello" subfolder)
   

Now we will write our **conanfile.py** in the **root "hellopack"** folder.
It is the script that defines how this package is built and used:

.. code-block:: python
   
   from conans import ConanFile, CMake
   
   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       settings = "os", "compiler", "build_type", "arch"
       exports = "hello/*"
   
       def build(self):
           cmake = CMake(self.settings)
           self.run('cd hello && cmake . %s' % cmake.command_line)
           self.run("cd hello && cmake --build . %s" % cmake.build_config)
   
       def package(self):
           self.copy("*.h", dst="include", src="hello")
           self.copy("*.lib", dst="lib", src="hello/lib")
           self.copy("*.a", dst="lib", src="hello/lib")
   
       def package_info(self):
           self.cpp_info.libs = ["hello"]
           
 
This ``conanfile.py`` uses this specific layout and in-source build as an example. If you want to
support more generic layouts, you can use ``conanfile_directory`` property that points to the
directory in which the ``conanfile.py`` is located, and which could be used for this case as:

.. code-block:: python

   def build(self):
      cmake = CMake(self.settings)
      self.run('cmake "%s/hello" %s' % (self.conanfile_directory, cmake.command_line))
      self.run('cmake --build . %s' % cmake.build_config)
      

A package ``name`` and ``version`` are always required to create packages. 

The ``settings`` field defines a set of predefined variables that affect the binary package.
The binary package is actually different for different OSs and compilers, also depending on
whether the ``build_type`` is Debug or Release, or the architecture is 32 or
64 bits. The possible values of those settings are also pre-defined.

The ``exports`` field is optional. It defines which auxiliary files will be exported together with
this **conanfile.py** file. In this particular case, we state that all the files inside the hello subfolder
will be stored together with the **conanfile.py**. This is not required, since the retrieval of
source code can be easily defined in an optional ``source()`` method, which can make git clone,
download & unzip, etc. We use the ``exports`` field here for brevity.

The ``build()`` method just builds the package, invoking CMake. The first line is the project creation
and configuration, and the second one is the actual build. They are just plain CMake commands, the
only additional feature being the translation of the ``settings`` field to CMake syntax inside the
cmake_command_line and cmake_build_config helpers, which just automatically define things like
the CMake generator or build flags. You can configure your actual build with regular python syntax,
using the settings, options, requirements, etc of the package as input.
Also note that **CMake is not strictly required**. You can build packages directly invoking **make**,
**MSBuild**, **SCons** or any other build system.

Then, the ``package()`` method takes charge of extracting the results of the build from the
build folder and putting them in another package folder. The ``copy()`` helper allows files
matching certain patterns to be copied to a package destination (typically folders like
include, lib, bin) from a source origin within the build folder.

Finally, the ``package_info`` method defines which configuration is needed, in order to 
actually consume this package. By default the package ``include``, ``lib`` and ``bin`` folders
are automatically added to their respective ``cpp_info`` paths. One of the most common usages
of ``cpp_info`` is to define the library names that package consumers should link with. This
method can also be configured with python scripting, defining for example different names if your
building process actually outputs different library names (e.g. debug, mt, 32 suffixes).


Once we have our **conanfile.py** all we have to do to start using this package in our machine
is to ``export`` it to the conan local store:


.. code-block:: bash

   $ conan export demo/testing
   

The export takes the name and the version from the conanfile, but it can be exported and 
afterwards reused under different user names and channels. In this case, the user is *demo* and
the channel is *testing*. 

.. code-block:: bash

   $ conan search


How can we know if the package builds properly? We can invoke the install command, passing
the full name of the package (we will use the default settings from conan.conf, but you can change
them if you want):

.. code-block:: bash

   $ conan install Hello/0.1@demo/testing
   ...
   ERROR: Can't find a 'Hello/0.1@demo/testing' package for the specified options and settings.
   ...


It failed, because there is no binary package that matches our settings. In fact, there aren't
any binary packages, we have just written and exported the conanfile.py which can create them. Now we will
try again, instructing conan to build the package from sources:

.. code-block:: bash

   $ conan install Hello/0.1@demo/testing --build Hello
   
   
Check :ref:`commands` for full details about the **install --build** options.

Now, try a ``conan search`` again in order to ensure that the package has just been created:

.. code-block:: bash

   $ conan search
   
So the package is there, but we still need to check if the package is actually properly created and
that there are no missing headers, libs or flags.

The best way to do that is to require this package from another test project that actually consumes it.
You could depend on this package explicitely from another project with a **conanfile.txt** file,
just as shown in :ref:`Getting started<getting_started>`. The ``Hello/0.1@demo/testing`` packages
will be built on demand, when the consumer project requires a specific package configuration.

In the next section we will see how it is possible to further automate the creation and testing of
multiple packages.
   



Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
