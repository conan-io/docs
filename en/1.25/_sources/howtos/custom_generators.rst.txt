.. _dyn_generators:

How to create and share a custom generator with generator packages
==================================================================

There are several built-in generators, like ``cmake``, ``visual_studio``, ``xcode``... But what if your build system is not included or the
existing built-in ones doesn't satisfy your needs? This **how to** will show you how to create a generator for
Premake_ build system.

.. important::

    Check the reference of the :ref:`custom_generator` section to know the syntax and attributes available.

Creating a Premake generator
----------------------------

Create a folder with a new *conanfile.py* with the following contents:

.. code-block:: bash

   $ mkdir conan-premake && cd conan-premake

.. code-block:: python
   :caption: *conanfile.py*

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

This is a full working example. Note the ``PremakeDeps`` class as a helper. The generator is creating Premake information for each
individual library separately, then also an aggregated information for all dependencies. This ``PremakeDeps`` wraps a single item of such
information.

Note the **name of the package** will be **premakegen/0.1@<user>/<channel>** as that is the name given to it, while the generator name is
**Premake** (the name of the class that inherits from ``Generator``). You can give the package any name you want, even the same as the
generator's name if desired.

You ``export`` the package recipe to the local cache, so it can be used by other projects as usual:

.. code-block:: bash

   $ conan export . myuser/testing

Using the generator
-------------------

Let's create a test project that uses this generator. We will use a simple application that will use a "Hello World" library package as a
requirement.

First, let's create the "Hello World" library package:

.. code-block:: bash

    $ mkdir conan-hello && cd conan-hello
    $ conan new hello/0.1
    $ conan create . myuser/testing

Now, let's create a folder for the application that will use Premake as build system:

.. code-block:: bash

    $ cd ..
    $ mkdir premake-project && cd premake-project

Put the following files inside. Note the ``premakegen@0.1@myuser/testing`` package reference in your *conanfile.txt*.

.. code-block:: text
   :caption: *conanfile.txt*

    [requires]
    hello/0.1@myuser/testing
    premakegen@0.1@myuser/testing

    [generators]
    Premake

.. code-block:: cpp
   :caption: *main.cpp*

    #include "hello.h"

    int main (void) {
        hello();
    }

.. code-block:: lua
   :caption: *premake4.lua*

    -- premake4.lua

    require 'conanpremake'

    -- A solution contains projects, and defines the available configurations solution "MyApplication"

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

Let's install the requirements:

.. code-block:: bash

    $ conan install . -s compiler=gcc -s compiler.version=4.9 -s compiler.libcxx=libstdc++ --build

This generates the *premake4.lua* file with the requirements information for building.

Now we are ready to build the project:

.. code-block:: bash

    $ premake4 gmake
    $ make (or mingw32-make if in windows-mingw)
    $ ./MyApplication
    Hello World Release!

Now everything works, so you might want to share your generator:

.. code-block:: bash

    $ conan upload PremakeGen/0.1@myuser/testing

.. tip::

    This is a regular Conan package, so you could create a *test_package* folder with a *conanfile.py* to test the generator as done in
    the example above (invoke the Premake build in the ``build()`` method).

Using template files for custom generators
------------------------------------------

If your generator has a lot of common, non-parameterized text, you might want to use files that contain the template. It is possible to do
this as long as the template file is exported in the recipe. The following example uses a simple text file, but you could use other
templating formats:

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


.. _`Premake`: https://premake.github.io/