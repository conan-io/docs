Automatically creating and testing packages
===========================================

So in the previous section we created a package that we could consume in new projects just by
adding a **conanfile.txt** to them and running ``conan install``.

But it is typical that for a given project we want to create different packages, for different
OSs, or for different settings in general. It turns out that using the same **conanfile.py**
files, this task is much simpler to automate than if using a plain text **conanfile.txt**.

Let's create inside our ``hellopack`` folder a ``test`` subfolder with the following files:
         

**main.cpp** is exactly equal to the original one

.. code-block:: cpp

   #include "hello.h"

   int main (void){
       hello();
   }
   
**conanfile.py** would be:

.. code-block:: python

   from conans import ConanFile, CMake
   import os
   
   class HelloReuseConan(ConanFile):
       settings = "os", "compiler", "build_type", "arch"
       requires = "Hello/0.1@demo/testing"
       generators = "cmake"
   
       def build(self):
           cmake = CMake(self.settings)
           self.run('cmake . %s' % cmake.command_line)
           self.run("cmake --build . %s" % cmake.build_config)
   
       def test(self):
           # equal to ./bin/greet, but portable win: .\bin\greet
           self.run(os.sep.join([".","bin", "greet"]))
           

This file is very similar to the previous one, the one that generated the packages, but with a few
differences:

- It doesn't have a name and version, cause we are not creating a package yet, not needed
- It defines a ``requires`` field, that points to our package
- It creates a ``cmake`` information file about the requirements (include directories, etc)
- The ``package()`` and ``package_info()`` methods are not required, as we are not creating a package.
- The ``test()`` method specifies which binaries have to be run

.. note::

   These tests are very different from the library unit or integration tests, which should be more
   comprenhensive. These tests are "package" tests, and validate that the package is properly
   created, and package consumers will be able to link against it and reuse it.
   

Finally, the **CMakeLists.txt** is totally equivalent to what we have seen before:

.. code-block:: cmake

   PROJECT(MyHello)
   cmake_minimum_required(VERSION 2.8)
   
   include(conanbuildinfo.cmake)
   CONAN_BASIC_SETUP()
   
   ADD_EXECUTABLE(greet main.cpp)
   TARGET_LINK_LIBRARIES(greet ${CONAN_LIBS})


The current folders layout should be:

::

   hellopack
      conanfile.py  //the original, to create the package
      hello
         CMakeLists.txt
         main.cpp
         hello.cpp
         hello.h
      test
         conanfile.py //the one to build the test, consuming the package
         main.cpp
         CMakeLists.txt
         

Now, we can take advantage of the ``test`` command that will build the consumer project with
its ``build()`` method and run the ``test()`` method:

.. code-block:: bash

   $ conan test
   ...
   Hello world!

This command uses by default the **--build=Hello** option, i.e. it always re-build the package.
If you just want to check that the package is properly created, but don't want to re-build it,
use the **--build=never** option:

.. code-block:: bash

   $ conan test --build=never
   ...
   Hello world!

With some python (or just pure shell or bash) scripting, we could easily automate the whole package creation and testing process,
for many different configurations.
For example you could put the following script in the ``hellopack`` folder,  name it ``build.py``:


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
          system('conan test -s compiler="Visual Studio" -s compiler.version=14 %s' % params)
          system('conan test -s compiler="Visual Studio" -s compiler.version=12 %s' % params)
          system('conan test -s compiler="gcc" -s compiler.version=4.8 %s' % params)
      else:
          pass

This is a pure python script, not related to conan, and should be run as such:

.. code:: bash

   $ python build.py

You can check all your created packages with:

.. code-block:: bash

   $ conan search


Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
