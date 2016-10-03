.. _creating_out:

Packaging from external sources
=====================================

In this case, we will create a package from the sources available from any other origin,
could be another external repository, or just downloading it from some site.


So we will create another package, from the same "hello" repository, but this time, we will not
embed the package recipe ``conanfile.py`` inside that repository. We will maintain it in a separate
one. This method is perfect for packaging third party projects.

We will write a package recipe for the "hello world" library available on github.
It is a very simple project, consisting of some source code files and a CMakeLists.txt
that builds a library and an executable. It can be built and run without conan.

Creating the package recipe
---------------------------------------

First, let's create a folder for our package recipe:

.. code-block:: bash

   $ mkdir greet && cd greet


Now we will write our package recipe, add a ``conanfile.py`` in the "greet" folder. Note that
we are calling this package **Greet**. The final package will be indeed basically the same as 
the "Hello" package we developed in the previous section:

.. code-block:: python
   
    from conans import ConanFile, CMake
    
    class GreetConan(ConanFile):
        name = "Greet"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        # No exports necessary
    
        def source(self):
            # this will create a hello subfolder, take it into account
            self.run("git clone https://github.com/memsharded/hello.git")
    
        def build(self):
            cmake = CMake(self.settings)
            self.run('cmake %s/hello %s' % (self.conanfile_directory, cmake.command_line))
            self.run("cmake --build . %s" % cmake.build_config)
    
        def package(self):
            self.copy("*.h", dst="include", src="hello")
            self.copy("*.lib", dst="lib", src="lib")
            self.copy("*.a", dst="lib", src="lib")
    
        def package_info(self):
            self.cpp_info.libs = ["hello"]

 
This ``conanfile.py`` is pretty much the same as in the previous section, just with a couple of changes:

* The ``exports`` field is not necessary in this case, as it doesn't have sources within the 
  package recipe to be bundled with the recipe
* The ``source()`` method is added, and a ``git clone`` is done to retrieve the sources. This will
  be done only at package build time, but it is not necessary if package binaries already exist.
  Any other way to retrieve sources is allowed, tools are provided to make easier to download and
  unzip files too.


Once we have our **conanfile.py** all we have to do to start using this package recipe in our machine
is to ``export`` it to our conan local package cache:


.. code-block:: bash

   $ conan export demo/testing
   $ conan search
   $ conan search Greet/0.1@demo/testing
   
It will show no binaries, as we have just exported the recipe, but not binaries have been created yet.


Using the package in another project
---------------------------------------

Using this new package is identical as in the :ref:`previous section <using_package>`.
The consuming project does not have to change at all. Just use the previous **hello-use** project and change
the **conanfile.txt** to use the new **Greet** package: 

.. code-block:: text

    [requires]
    Greet/0.1@demo/testing
    
    [generators]
    cmake

Search again for binaries:

.. code-block:: bash

   $ conan search Greet/0.1@demo/testing
   

Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
