Automatically creating and testing packages
===========================================

In the previous two sections we created two package recipes, exported them to our local cache, 
and used those packages in another project. 

This is a very common task for package creators, so conan allows to embed such "consuming" project
in the package recipe and use it to automatically create and test packages.

Let's create a ``test_package`` subfolder inside our package recipe (any of the two should work),
and add the following files in it, which are in essence the same as the consuming project we
did before:
         
**main.cpp**, which is consuming and using the package

.. code-block:: cpp

   #include "hello.h"

   int main (void){
       hello();
   }
   
**conanfile.py** to build the consuming application:

.. code-block:: python

    from conans import ConanFile, CMake
    import os
    
    # This easily allows to copy the package in other user or channel
    channel = os.getenv("CONAN_CHANNEL", "testing")
    username = os.getenv("CONAN_USERNAME", "demo")
    
    class HelloReuseConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        requires = "Hello/0.1@%s/%s" % (username, channel)
        generators = "cmake"
    
        def build(self):
            cmake = CMake(self.settings)
            self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
            self.run("cmake --build . %s" % cmake.build_config)
    
        def test(self):
            # equal to ./bin/greet, but portable win: .\bin\greet
            self.run(os.sep.join([".","bin", "greet"]))
               

This file is very similar to our previous package recipes (the one that generated the package) but with a few
differences:

- It doesn't have a name and version, because we are not creating a package, so it's not necessary.
- It defines a ``requires`` field, that points to our package recipe.
- It uses the ``cmake`` generator, we are consuming a package, so it is convenient.
- The ``package()`` and ``package_info()`` methods are not required, since we are not creating a package.
- The ``test()`` method specifies which binaries have to be run.

.. note::

   These tests are very different from the library unit or integration tests, which should be more
   comprehensive. These tests are "package" tests, and validate that the package is properly
   created, and that package consumers will be able to link against it and reuse it.
   

Finally, the **CMakeLists.txt** is totally equivalent to what we have seen before:

.. code-block:: cmake

   project(MyHello)
   cmake_minimum_required(VERSION 2.8.12)
   
   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup()
   
   add_executable(greet main.cpp)
   target_link_libraries(greet ${CONAN_LIBS})


The current folder layout could be:

::

   project
      conanfile.py  //the original, to create the package
      //possible other sources, depending if this recipe is internal or external
      test_package
         conanfile.py //the one to build the test, consuming the package
         main.cpp
         CMakeLists.txt
         

Now, we can take advantage of the ``test_package`` command that will install the requirements,
building the "Hello" package, and 
building the consumer test project inside ``test_package`` folder with its ``build()`` method.
Finally, it will run the ``test()`` method of the consumer project, to check that everything works:

.. code-block:: bash

   $ conan test_package
   ...
   Hello world!

This command uses the **--build=Hello** option by default, i.e. it always re-builds the package.
If you just want to check if the package is properly created, but don't want to re-build it,
use the **--build=never** option:

.. code-block:: bash

   $ conan test_package --build=never
   ...
   Hello world!
   
The ``conan test_package`` command receives the same command line parameters as ``conan install`` so you
can pass to it the same settings, options, and command line switches.

With some python (or just pure shell or bash) scripting, we could easily automate the whole
package creation and testing process, for many different configurations.
For example you could put the following script in the package root folder. Name it ``build.py``:


.. code-block:: python

   import os, sys
   import platform
   
   def system(command):
      retcode = os.system(command)
      if retcode != 0:
          raise Exception("Error while executing:\n\t %s" % command)
   
   if __name__ == "__main__":
      system('conan export demo/testing')
      params = " ".join(sys.argv[1:])
   
      if platform.system() == "Windows":
          system('conan test_package -s compiler="Visual Studio" -s compiler.version=14 %s' % params)
          system('conan test_package -s compiler="Visual Studio" -s compiler.version=12 %s' % params)
          system('conan test_package -s compiler="gcc" -s compiler.version=4.8 %s' % params)
      else:
          pass

This is a pure python script, not related to conan, and should be run as such:

.. code:: bash

   $ python build.py

You can check all your created packages with:

.. code-block:: bash

   $ conan search -v
 


Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
