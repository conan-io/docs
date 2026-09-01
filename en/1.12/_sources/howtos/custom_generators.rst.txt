.. _dyn_generators:

How to create and share a custom generator with generator packages
==================================================================

There are several built-in generators, like ``cmake``, ``visual_studio``, ``xcode``...
But what if your build system is not included? Or maybe the existing built-in generators
doesn't satisfy your needs. There are several options:

- Use the ``txt`` generator, that generates a plain text file easy to parse, which you might
  be able to use.
- Use ``conanfile.py`` data, and for example in the ``build()`` method, access that information
  directly and generate a file or call directly your system
- Fork the conan codebase and write a built-in generator. Please make a pull request if possible to
  contribute it to the community.
- Write a custom generator in a ``conanfile.py`` and manage it as a package. You can upload it
  to your own server and share with your team, or share with the world uploading it to bintray.
  You can manage it as a package, you can version it, overwrite it, delete it, create channels (testing/stable...),
  and the most important: bring it to your projects as a regular dependency.

This **how to** will show you how to do the latest one. We will build a generator for **premake** (https://premake.github.io/)
build system:

Creating a custom generator
---------------------------

Basically a generator is a class that extends ``Generator`` and implements two properties: ``filename``,
which will be the name of the file that will be generated, and ``content`` with the contents of
that file. The **name of the generator** itself will be taken from the class name:

.. code-block:: python

    class MyGeneratorName(Generator):
        @property
        def filename(self):
            return "mygenerator.file"
    
        @property
        def content(self):     
            return "whatever contents the generator produces"
            
This class is just included in a ``conanfile.py`` that must contain also a ``ConanFile`` class
that implements the package itself, with the name of the package, the version, etc. This
class typically has no ``source()``, ``build()``, ``package()``, and even the ``package_info()`` method is
overridden as it doesn't have to define any include paths or library paths.

If you want to create a generator that creates more than one file, you can leave the ``filename()`` empty, and return a dictionary of
filenames->contents in the ``content()`` method:

.. code-block:: python

    class MultiGenerator(Generator):

        @property
        def content(self):
            return {"filename1.txt": "contents of file1",
                    "filename2.txt": "contents of file2"}  # any number of files

        @property
        def filename(self):
            pass

Once, it is defined in the ``conanfile.py`` you can treat is as a regular package, typically you
will ``export`` it first to your local cache, test it, and once it is working fine, you would
``upload`` it to a server.


You have access to the ``conanfile`` instance at ``self.conanfile`` and get information from the requirements:

+-----------------------------------------+------------------------------------------------------------------------------------------------+
| Variable                                | Description                                                                                    |
+=========================================+================================================================================================+
| self.conanfile.deps_cpp_info            | :ref:`deps_cpp_info<deps_cpp_info_attributes_reference>`                                       |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| self.conanfile.deps_env_info            | :ref:`deps_env_info<deps_env_info_attributes_reference>`                                       |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| self.conanfile.deps_user_info           | :ref:`deps_user_info<deps_user_info_attributes_reference>`                                     |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| self.conanfile.env                      | dict with the applied env vars declared in the requirements                                    |
+-----------------------------------------+------------------------------------------------------------------------------------------------+

Premake generator example
-------------------------

Create a project (the best is a git repository):

.. code-block:: bash

   $ mkdir conan-premake && cd conan-premake
   
Then, write in it the following **conanfile.py**:

.. code-block:: python

    from conans.model import Generator
    from conans import ConanFile

    class PremakeDeps(object):
        def __init__(self, deps_cpp_info):
            self.include_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                            for p in deps_cpp_info.include_paths)
            self.lib_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                        for p in deps_cpp_info.lib_paths)
            self.bin_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                        for p in deps_cpp_info.bin_paths)
            self.libs = ", ".join('"%s"' % p for p in deps_cpp_info.libs)
            self.defines = ", ".join('"%s"' % p for p in deps_cpp_info.defines)
            self.cppflags = ", ".join('"%s"' % p for p in deps_cpp_info.cppflags)
            self.cflags = ", ".join('"%s"' % p for p in deps_cpp_info.cflags)
            self.sharedlinkflags = ", ".join('"%s"' % p for p in deps_cpp_info.sharedlinkflags)
            self.exelinkflags = ", ".join('"%s"' % p for p in deps_cpp_info.exelinkflags)

            self.rootpath = "%s" % deps_cpp_info.rootpath.replace("\\", "/")

    class Premake(Generator):
        @property
        def filename(self):
            return "conanpremake.lua"

        @property
        def content(self):
            deps = PremakeDeps(self.deps_build_info)

            template = ('conan_includedirs{dep} = {{{deps.include_paths}}}\n'
                        'conan_libdirs{dep} = {{{deps.lib_paths}}}\n'
                        'conan_bindirs{dep} = {{{deps.bin_paths}}}\n'
                        'conan_libs{dep} = {{{deps.libs}}}\n'
                        'conan_cppdefines{dep} = {{{deps.defines}}}\n'
                        'conan_cppflags{dep} = {{{deps.cppflags}}}\n'
                        'conan_cflags{dep} = {{{deps.cflags}}}\n'
                        'conan_sharedlinkflags{dep} = {{{deps.sharedlinkflags}}}\n'
                        'conan_exelinkflags{dep} = {{{deps.exelinkflags}}}\n')

            sections = ["#!lua"]
            all_flags = template.format(dep="", deps=deps)
            sections.append(all_flags)
            template_deps = template + 'conan_rootpath{dep} = "{deps.rootpath}"\n'

            for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
                deps = PremakeDeps(dep_cpp_info)
                dep_name = dep_name.replace("-", "_")
                dep_flags = template_deps.format(dep="_" + dep_name, deps=deps)
                sections.append(dep_flags)

            return "\n".join(sections)


    class MyCustomGeneratorPackage(ConanFile):
        name = "PremakeGen"
        version = "0.1"
        url = "https://github.com/memsharded/conan-premake"
        license = "MIT"

        def build(self):
            pass

        def package_info(self):
            self.cpp_info.includedirs = []
            self.cpp_info.libdirs = []
            self.cpp_info.bindirs = []

This is a full working example. Note the ``PremakeDeps`` class as a helper. The generator is
creating premake information for each individual library separately, then also an aggregated
information for all dependencies. This ``PremakeDeps`` wraps a single item of such information.

Note the **name of the package** will be **PremakeGen/0.1@user/channel** as that is the name given
to it, while the generator name is **Premake**. You can give the package any name you want, even
matching the generator name if desired.

You ``export`` the package recipe to the local cache, so it can be used by other projects as usual:

.. code-block:: bash

   $ conan export memsharded/testing

Using the generator
-------------------

Let's create a test project that uses this generator, and also an existing library conan package,
we will use the simple "Hello World" package we already created before:

.. code-block:: bash

   $ cd ..
   $ mkdir premake-project && cd premake-project
   

Now put the following files inside. Note the ``PremakeGen@0.1@memsharded/testing`` package
reference in conanfile.txt.

**conanfile.txt**

.. code-block:: text

    [requires]
    Hello/0.1@memsharded/testing
    PremakeGen@0.1@memsharded/testing
    
    [generators]
    Premake

**main.cpp**

.. code-block:: cpp

    #include "hello.h"
    
    int main (void){
        hello();
    }
    
**premake4.lua**

.. code-block:: lua

    #!lua
    
    require 'conanpremake'
    
    -- A solution contains projects, and defines the available configurations
    solution "MyApplication"
       configurations { "Debug", "Release" }
       includedirs { conan_includedirs }
       libdirs { conan_libdirs }
       links { conan_libs }
       -- A project defines one build target
       project "MyApplication"
          kind "ConsoleApp"
          language "C++"
          files { "**.h", "**.cpp" }
     
          configuration "Debug"
             defines { "DEBUG" }
             flags { "Symbols" }
    
          configuration "Release"
             defines { "NDEBUG" }
             flags { "Optimize" }


Let's install the requirements and build the project:

.. code-block:: bash

   $ conan install . -s compiler=gcc -s compiler.version=4.9 -s compiler.libcxx=libstdc++ --build
   $ premake4 gmake
   $ make (or mingw32-make if in windows-mingw)
   $ ./MyApplication
   Hello World!
   
Now, everything works, so you might want to share your generator:

.. code-block:: bash

    $ conan upload PremakeGen/0.1@memsharded/testing

.. note::

    This is a regular conan package. You could for example embed this example in a *test_package* folder, create a *conanfile.py* that
    invokes premake4 in the build() method, and use :command:`conan test` to automatically test your custom generator with a real project.

Using template files for custom generators
------------------------------------------

If your generator has a lot of common, non-parameterized text, you might want to use files that contain the template.
It is possible to do this as long as the template file is exported in the recipe. The following example uses a simple text file,
but you could use other templating formats:

.. code-block:: python

    import os
    from conans import ConanFile, load
    from conans.model import Generator

    class MyCustomGenerator(Generator):
        @property
        def filename(self):
            return "customfile.gen"
        @property
        def content(self):
            template = load(os.path.join(os.path.dirname(__file__), "mytemplate.txt"))
            return template % "Hello"

    class MyCustomGeneratorPackage(ConanFile):
        name = "custom"
        version = "0.1"
        exports = "mytemplate.txt"
