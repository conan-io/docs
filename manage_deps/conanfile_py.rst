.. _conanfile_py:

Using ``conanfile.py``
----------------------

If you know a little bit about python you can use ``conanfile.py`` to invoke your build system and take advantage of, among many other things, managing all settings and options of your requirements.

Migrate from ``conanfile.txt``
..............................

If you have a ``conanfile.txt`` file, the conversion to ``conanfile.py`` is quite easy.

Let's take a look at the complete ``conanfile.txt`` from our :ref:`conanfile.txt section<conanfile_txt>` with POCO:

.. code-block:: text
   
      [requires]
      Poco/1.6.1@lasote/stable
      OpenSSL/1.0.2d@lasote/stable # just an example of how to migrate multiple requirements, it shouldn't exist in your file
      
      [generators]
      gcc
      cmake
      txt
      
      [options]
      Poco:poco_static=False
      OpenSSL:shared=True
      
      [imports]
      bin, *.dll -> ./bin # Copies all dll files from the package "bin" folder to my project "bin" folder
      lib, *.dylib* -> ./bin # Copies all dylib files from the package "lib" folder to my project "bin" folder


And the equivalent ``conanfile.py`` file:

.. code-block:: python

   from conans import ConanFile, CMake
   
   class MyProjectWithConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.6.1@lasote/stable", "OpenSSL/1.0.2d@lasote/stable"
      generators = "cmake", "gcc", "txt"
      default_options = "Poco:poco_static=False", "OpenSSL:shared=False"
            
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

Install the requirements as usual

.. code-block:: bash

   $ conan install
  

Well, now we have our ``conanfile.py`` created. But where is the improvement?
In the previous ``conanfile.py`` we omitted the **build** method.

The full ``conanfile.py`` will allow you to:

1. Have **full managed settings** for both your project and its requirements.
2. Have **full managed options** for both your project and its requirements.
3. Get ready if you want to natively **build your own conan package**.

.. _conanfile_py_managed_settings:

Managed settings
................


Example with CMake
__________________


If you are building your project with CMake, go through this example to manage your settings.

Edit your ``conanfile.py`` and add the ``build()`` method:

.. code-block:: python

   from conans import ConanFile, CMake
   
   class MyProjectWithConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.6.1@lasote/stable", "OpenSSL/1.0.2d@lasote/stable"
      generators = "cmake", "gcc", "txt"
      default_options = "Poco:poco_static=False", "OpenSSL:shared=False"

      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         cmake = CMake(self.settings)
         self.run('cmake . %s' % cmake.command_line)
         self.run("cmake --build . %s" % cmake.build_config)


In the code above, we are using a **CMake** helper class. This class reads the current settings and sets cmake flags to handle **arch**, **build_type**, **compiler** and **compiler.version**.  

You only need to include the following lines in your ``CMakeLists.txt``:


.. code-block:: cmake

   # ... 
   
   include(conanbuildinfo.cmake)
   conan_basic_setup()
   
   # ... Your original cmakelists.txt contents ...
   
   target_link_libraries(YOUR_TARGET ${CONAN_LIBS})
   

Then execute:

.. code-block:: bash

   $ conan install # conan remembers: build_type=Release -s arch=x86s settings: -s build_type=Release -s arch=x86
   $ conan build
   

The **conan install** command downloads and prepares the requirements of your project
(for the specified settings) and the **conan build** command uses all that information
to invoke your ``build()`` method, which in turn calls **cmake**.

The big benefit is that **cmake** will compile your code for the specified settings too.

If you want to compile your project for **x86_64** and **Debug** or another setting just change the parameters passed to install:

.. code-block:: bash

   $ conan install -s build_type=Debug -s arch=x86_64
   $ conan build


From now you can just type **conan install** and conan will remember the settings.

As you can see, if you integrate your build system with conan, the settings become standard and well organized.
   

.. note::

   If you don't want to alter your CMakefile.txt file, you can have a subfolder with your proyect.
   Then, in conan's CMakelists.txt, wrap your CMakefile with **add_subdirectory**.


Example with GCC
________________

You can use the **gcc** helper instead of **cmake** for building your source code:


.. code-block:: python

   ############ IMPORT GCC helper! ###########
   from conans import ConanFile, GCC

   class MyProjectWithConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.6.1@lasote/stable", "OpenSSL/1.0.2d@lasote/stable"
      generators = "gcc"
      default_options = "Poco:poco_static=False", "OpenSSL:shared=False"
     
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         ############ GCC helper ###########
         gcc = GCC(self.settings)
         self.run("mkdir -p bin")
         command = 'g++ timer.cpp @conanbuildinfo.gcc -o bin/timer %s' % gcc.command_line
         self.run(command)
         

Example with Autotools: configure / make
________________________________________


If you are using **configure** and/or **make** to you can use **ConfigureEnvironment** helper.
This helper sets some common variables as environment variables with your requirements information.

It works prepending the *command_line* to your **configure and make** commands:

    
.. code-block:: python

   from conans import ConanFile, ConfigureEnvironment

   class MyProjectWithConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.6.1@lasote/stable", "OpenSSL/1.0.2d@lasote/stable"
      default_options = "Poco:poco_static=False", "OpenSSL:shared=False"
     
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         ############ ConfigureEnvironment helper ###########
         env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
         self.run("%s && ./configure" % env.command_line)
         self.run("%s && make" % env.command_line)
         
         # nmake also works for Windows:
         # command = '%s && nmake /f Makefile.msvc"' % env.command_line
         # self.run(command)

This helper is specially useful when **configure** script hasn't enough parameters to define where the requirements are located.
It also works with **nmake** in Windows.

Setted environment variables:

+-------------+------------------+--------------------------------------------------------+
| OS          | NAME             | DESCRIPTION                                            |
+=============+==================+========================================================+
| **LINUX**   | LIBS             |  Library names to link                                 |
+-------------+------------------+--------------------------------------------------------+
| **LINUX**   | LDFLAGS          |  Link flags, (filled with -L lib paths)                |
+-------------+------------------+--------------------------------------------------------+
| **LINUX**   | CFLAGS           |  Options for the C compiler                            |
+-------------+------------------+--------------------------------------------------------+
| **LINUX**   | CPPFLAGS         |  Options for the C++ compiler                          |
+-------------+------------------+--------------------------------------------------------+
| **LINUX**   | C_INCLUDE_PATH   |  Include paths for C compiler                          |
+-------------+------------------+--------------------------------------------------------+
| **LINUX**   | CPP_INCLUDE_PATH |  Include paths for C++ compiler                        |
+-------------+------------------+--------------------------------------------------------+
| **WINDOWS** | LIB              |  Libraries with full path (appended with semicolon)    |
+-------------+------------------+--------------------------------------------------------+
| **WINDOWS** | CL               |  Compiler flags, (filled with include directories /I)  |
+-------------+------------------+--------------------------------------------------------+


Example with other build systems
________________________________

If you are using **scons** or any other build system you can use conan too.
In the ``build()`` method you can access your settings and build information from your requirements and pass it to your build system.


.. code-block:: python

   from conans import ConanFile

   class MyProjectWithConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.6.1@lasote/stable", "OpenSSL/1.0.2d@lasote/stable"
      ########### IT'S IMPORTANT TO DECLARE THE TXT GENERATOR TO DEAL WITH A GENERIC BUILD SYSTEM
      generators = "txt"
      default_options = "Poco:poco_static=True", "OpenSSL:shared=False"
   
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         ############ Without any helper ###########
         # Settings
         print(self.settings.os)
         print(self.settings.arch)
         print(self.settings.compiler)
   
         # Options
         #print(self.options.my_option)
         print(self.options["OpenSSL"].shared)
         print(self.options["Poco"].poco_static)
   
         # Paths and libraries, all
         print("-------- ALL --------------")
         print(self.deps_cpp_info.include_paths)
         print(self.deps_cpp_info.lib_paths)
         print(self.deps_cpp_info.bin_paths)
         print(self.deps_cpp_info.libs)
         print(self.deps_cpp_info.defines)
         print(self.deps_cpp_info.cflags)
         print(self.deps_cpp_info.cppflags)
         print(self.deps_cpp_info.sharedlinkflags)
         print(self.deps_cpp_info.exelinkflags)
   
         # Just from OpenSSL
         print("--------- FROM OPENSSL -------------")
         print(self.deps_cpp_info["OpenSSL"].include_paths)
         print(self.deps_cpp_info["OpenSSL"].lib_paths)
         print(self.deps_cpp_info["OpenSSL"].bin_paths)
         print(self.deps_cpp_info["OpenSSL"].libs)
         print(self.deps_cpp_info["OpenSSL"].defines)
         print(self.deps_cpp_info["OpenSSL"].cflags)
         print(self.deps_cpp_info["OpenSSL"].cppflags)
         print(self.deps_cpp_info["OpenSSL"].sharedlinkflags)
         print(self.deps_cpp_info["OpenSSL"].exelinkflags)
   
         # Just from POCO
         print("--------- FROM POCO -------------")
         print(self.deps_cpp_info["Poco"].include_paths)
         print(self.deps_cpp_info["Poco"].lib_paths)
         print(self.deps_cpp_info["Poco"].bin_paths)
         print(self.deps_cpp_info["Poco"].libs)
         print(self.deps_cpp_info["Poco"].defines)
         print(self.deps_cpp_info["Poco"].cflags)
         print(self.deps_cpp_info["Poco"].cppflags)
         print(self.deps_cpp_info["Poco"].sharedlinkflags)
         print(self.deps_cpp_info["Poco"].exelinkflags)
   
   
         # self.run("invoke here your configure, make, or others")
         # self.run("basically you can do what you want with your requirements build info)


Managed options
...............

We can have our **options** managed too. 

In this section we will only use CMake. We will build a library in our project, for which GCC becomes a little messy.
In the real world it's not very common to use GCC for complex projects. Frequently, **make** is used.


Suppose we are developing a library, and we want to add an option to control if our library is shared or static.
Let's create a new **cpp** file that will simulate our library: 

**mylib.cpp**

.. code-block:: cpp
   
   int a=2; // We don't care about the code, it's just an example.
     
And out **timer.cpp** (the same from previous examples):


.. code-block:: cpp

   #include "Poco/Timer.h"
   #include "Poco/Thread.h"
   #include "Poco/Stopwatch.h"
   #include <iostream>

   using Poco::Timer;
   using Poco::TimerCallback;
   using Poco::Thread;
   using Poco::Stopwatch;

   class TimerExample{
   public:
      TimerExample(){ _sw.start();}
      
      void onTimer(Timer& timer){
         std::cout << "Callback called after " << _sw.elapsed()/1000 << " milliseconds." << std::endl;
      }     
   private:
      Stopwatch _sw;
   };

   int main(int argc, char** argv){ 
      TimerExample example;
      Timer timer(250, 500);
      timer.start(TimerCallback<TimerExample>(example, &TimerExample::onTimer));
      
      Thread::sleep(5000);
      timer.stop();
      return 0;
   }
   
   
Define **options** and **default_options** this way:
   
   
   
.. code-block:: python

   from conans import ConanFile, CMake

   class MyProjectWithConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.6.1@lasote/stable", "OpenSSL/1.0.2d@lasote/stable"
      generators = "cmake", "gcc", "txt"    
      ################### NEW ###########################
      options = {"shared": [True, False]} # Values can be True or False (number or string value is also possible)
      default_options = "shared=False", "Poco:poco_static=False", "OpenSSL:shared=False" # Default value for shared is False (static)
      ###################################################

      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         cmake = CMake(self.settings)
         ################### NEW ##########################
         shared_definition = "-DSHARED=1" if self.options.shared else ""
         self.run('cmake . %s %s' % (cmake.command_line, shared_definition))
         ##################################################
         self.run("cmake --build . %s" % cmake.build_config)
   
   
Observe the **build** method. We are reading **self.options.shared** and appending a definition to our **cmake** command.

So let's use this option in our CMakeLists.txt

.. code-block:: cmake

   project(FoundationTimer)
   cmake_minimum_required(VERSION 2.8)
   
   include(conanbuildinfo.cmake)
   conan_basic_setup()
   
   # Create a library, shared or static
   if(SHARED)
      message("BUILDING SHARED LIBRARY")
      add_library(mylibrary SHARED lib.cpp)
   else()
      add_library(mylibrary STATIC lib.cpp)
   endif()
   
   # Link library dependencies
   target_link_libraries(mylibrary ${CONAN_LIBS})
   
   add_executable(timer timer.cpp)
   
   # Link our lib to our executable
   target_link_libraries(timer mylibrary)
                 
                         
.. code-block:: bash

   $ conan install -o shared=True
   $ conan build   
  
   BUILDING SHARED LIBRARY
   -- Configuring done
   -- Generating done
   -- Build files have been written
   [ 50%] Building CXX object CMakeFiles/mylibrary.dir/lib.cpp.o
   Linking CXX shared library libmylibrary.so
   [ 50%] Built target mylibrary
   Linking CXX executable bin/timer
   [100%] Built target timer

Observe the **"-o shared=True"** in the install command and **cmake ouput**. ``libmylibrary.so`` has been generated just by changing that option.
You can add as many options as you need to your library. 

``conanfile.py`` becomes a self documented file for checking what options we can adjust to compile a library.


.. note::

   You can use **-DBUILD_SHARED_LIBS=ON** instead of **-DSHARED=1** and CMake will automatically build SHARED libraries,
   without the need of modifying your CMakeLists.
   We used a custom definition to show you how to control your build through **conan options** and **cmake definitions**.

   

-------------------------------------------------------------------------------------------------------


Conditional settings, options and requirements
..............................................

Remember, in your ``conanfile.py`` you have also access to the options of your dependencies, and you can play with them to:

* Add requirements dynamically
* Change options values

The **config** method is the right place to change values of options and settings, but you can read them from build and imports methods (and all others, as we will see).

Here is an example of what we could do in our **config method**:

.. code-block:: python

      ...
      requires = "Poco/1.6.1@lasote/stable" # We will add OpenSSL dynamically "OpenSSL/1.0.2d@lasote/stable"
      ...
       
      def config(self):
          # We can control the options of our dependencies based on current options
          self.options["Poco"].poco_static = not self.options.shared
          self.options["OpenSSL"].shared = self.options.shared
          
          # Maybe in windows we know that OpenSSL works better as shared (false)
          if self.settings.os == "Windows":
             self.options["OpenSSL"].shared = True
             
             # Or adjust any other available option 
             self.options["Poco"].other_option = "foo"
             
          # Or add a new requirement!
          if self.options.testing:
             self.requires("OpenSSL/2.1@memsharded/testing")
          else:
             self.requires("OpenSSL/1.0.2d@lasote/stable")
                 


Get ready to make your conan package
....................................

Well, at this point you almost have your library prepared for being a conan package.

You just have these tasks pending:


1. Separate source code from ``conanfile.py``: We recommend to have your source code in a repository and use the **method 'source'** to get it.
2. Copy the compiled libraries/headers/binaries to a well known directory in the package, with **method 'package'**
3. Declare library names, compilation flags and definitions needed to reuse your library, with **method 'package_info'**
4. Test and upload your package to your own in-house server or to **conan.io**


In :ref:`building getting started section<building_hello_world>` you will review the entire ``conanfile.py`` structure and the process to build a package from the beginning.
