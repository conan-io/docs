.. _conanfile_py:

Using ``conanfile.py``
----------------------

If the expresiveness of the ``conanfile.txt`` is not enough for your use case, or if you want
to further automate your project building with automatic management of settings and options,
you can use a ``conanfile.py``, which is an equivalent python version.

Migrate from ``conanfile.txt``
..............................

If you have a ``conanfile.txt`` file, the conversion to a ``conanfile.py`` is quite easy.

Let's take a look at the complete ``conanfile.txt`` from the previous *timer* example with POCO library,
in which we have added a couple of extra generators

.. code-block:: text
   
      [requires]
      Poco/1.7.3@lasote/stable
      
      [generators]
      gcc
      cmake
      txt
      
      [options]
      Poco:shared=True
      OpenSSL:shared=True
      
      [imports]
      bin, *.dll -> ./bin # Copies all dll files from the package "bin" folder to my project "bin" folder
      lib, *.dylib* -> ./bin # Copies all dylib files from the package "lib" folder to my project "bin" folder


The equivalent ``conanfile.py`` file is:

.. code-block:: python

   from conans import ConanFile, CMake
   
   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.3@lasote/stable" # comma separated list of requirements
      generators = "cmake", "gcc", "txt"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"
            
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

With this ``conanfile.py`` you can just work as usual, nothing changes from the user perspective.
You can install the requirements with (from mytimer/build folder):

.. code-block:: bash

   $ conan install ..
  

.. _conanfile_py_managed_settings:

Build automation
................

One advantage of using ``conanfile.py`` is that the project build can be further simplified,
using the conanfile.py ``build()`` method.

Building with CMake
___________________

If you are building your project with CMake, edit your ``conanfile.py`` and add the following ``build()`` method:

.. code-block:: python
   :emphasize-lines: 14, 15
   
   from conans import ConanFile, CMake
   
   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.3@lasote/stable"
      generators = "cmake", "gcc", "txt"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"

      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         cmake = CMake(self.settings)
         self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
         self.run('cmake --build . %s' % cmake.build_config)


In the code above, we are using a **CMake** helper class. This class reads the current settings and sets cmake flags to handle **arch**, **build_type**, **compiler** and **compiler.version**.  
Note that the first ``cmake`` invocation is using the ``conanfile_directory``. This is necessary if
you want to do out-of-source builds or just building in a child folder, as ``cmake`` should be
given the location of the root ``CMakeLists.txt`` (in this case located in the same folder as the
``conanfile.py``).
   
Then execute, from your project root:

.. code-block:: bash

   $ mkdir build && cd build
   $ conan install ..
   $ conan build ..
   

The **conan install** command downloads and prepares the requirements of your project
(for the specified settings) and the **conan build** command uses all that information
to invoke your ``build()`` method to build your project, which in turn calls **cmake**.

This ``conan build`` will use the same settings used in the ``conan install``, which simplifies
the process and reduces the errors of mismatches between the installed packages and the current
project configuration.


If you want to build your project for **x86_64** or another setting just change the parameters passed to ``conan install``:

.. code-block:: bash

   $ rm -rf * //to clean the current build folder
   $ conan install .. -s arch=x86_64
   $ conan build ..


From now you can just type **conan install** and conan will remember the settings.
Implementing and using the conanfile.py ``build()`` method ensures that we always use the same
settings both in the installation of requirements and the build of the project, and simplifies
calling the build system.
   

GCC
___

You could use the **gcc** helper instead of **cmake** for building your source code:


.. code-block:: python
   :emphasize-lines: 1, 14, 15, 16

   from conans import ConanFile, GCC # IMPORT GCC helper!

   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.3@lasote/stable"
      generators = "gcc"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"
     
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         gcc = GCC(self.settings)
         self.run("mkdir -p bin")
         command = 'g++ timer.cpp @conanbuildinfo.gcc -o bin/timer %s' % gcc.command_line
         self.run(command)
         

Autotools: configure / make
___________________________


If you are using **configure** and/or **make** to you can use **ConfigureEnvironment** helper.
This helper sets some common variables as environment variables with your requirements information.

It works prepending the *command_line* to your **configure and make** commands:

    
.. code-block:: python
   :emphasize-lines: 13, 14
   
   from conans import ConanFile, ConfigureEnvironment

   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.3@lasote/stable"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"
     
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
   
      def build(self):
         env = ConfigureEnvironment(self)
         self.run("%s ./configure" % env.command_line_env)
         self.run("%s make" % env.command_line_env)
         
         # nmake also works for Windows:
         # command = '%s && nmake /f Makefile.msvc"' % env.command_line_env
         # self.run(command)

This helper is specially useful when **configure** script hasn't enough parameters to define where the requirements are located.
It also works with **nmake** in Windows.

Used environment variables:

+-------------+--------------------+------------------------------------------------------+
| OS          | NAME               | DESCRIPTION                                          |
+=============+====================+======================================================+
| **LINUX**   | LIBS               | Library names to link                                |
+-------------+--------------------+------------------------------------------------------+
| **LINUX**   | LDFLAGS            | Link flags, (filled with -L lib paths)               |
+-------------+--------------------+------------------------------------------------------+
| **LINUX**   | CFLAGS             | Options for the C compiler                           |
+-------------+--------------------+------------------------------------------------------+
| **LINUX**   | CPPFLAGS           | Options for the C++ compiler                         |
+-------------+--------------------+------------------------------------------------------+
| **LINUX**   | C_INCLUDE_PATH     | Include paths for C compiler                         |
+-------------+--------------------+------------------------------------------------------+
| **LINUX**   | CPLUS_INCLUDE_PATH | Include paths for C++ compiler                       |
+-------------+--------------------+------------------------------------------------------+
| **WINDOWS** | LIB                | Libraries with full path (appended with semicolon)   |
+-------------+--------------------+------------------------------------------------------+
| **WINDOWS** | CL                 | Compiler flags, (filled with include directories /I) |
+-------------+--------------------+------------------------------------------------------+


.. _usingoptions:


Using options
.............

We are going to use the **Poco** timer example, but instead of building just an executable, we 
are building also a library with the ``ExampleTimer`` class, that is used by the executable.

.. note::

    If you are using the repository in https://github.com/memsharded/example-poco-timer.git, 
    the code is already available in a branch:
    
    $ git checkout conanfile_py
    

The code will be split in 3 files: **timer.cpp** and **timer.h** containing the class, and an
**main.cpp** containing the example app executable:

**timer.h** (note the required dllexport if we want to build a shared lib)

.. code-block:: cpp

    #pragma once
    #include "Poco/Timer.h"
    #include "Poco/Stopwatch.h"
    
    #ifdef WIN32
        #define POCO_TIMER_EXPORT __declspec(dllexport)
    #else
        #define POCO_TIMER_EXPORT
    #endif
    
    using Poco::Timer;
    using Poco::Stopwatch;
    
    class POCO_TIMER_EXPORT TimerExample{
    public:
        TimerExample(){ _sw.start();}
        void onTimer(Timer& timer);
    private:
        Stopwatch _sw;
    };
    
**timer.cpp**

.. code-block:: cpp

    #include "timer.h"
    #include <iostream>
    
    void TimerExample::onTimer(Timer& timer){
        std::cout << "Callback called after " << _sw.elapsed()/1000 << " milliseconds." << std::endl;
    }


**main.cpp**

.. code-block:: cpp

    #include "timer.h"

    using Poco::TimerCallback;
    using Poco::Thread;
    
    int main(int argc, char** argv){
        TimerExample example;
        Timer timer(250, 500);
        timer.start(TimerCallback<TimerExample>(example, &TimerExample::onTimer));
    
        Thread::sleep(5000);
        timer.stop();
        return 0;
    }
    


This library will depend in turn on POCO library too, so we could write a ``conanfile.py`` for our
package and define **options** and **default_options** this way:
   
   
.. code-block:: python
   :emphasize-lines: 7, 8, 16, 17
   
    from conans import ConanFile, CMake
    
    class PocoTimerConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        requires = "Poco/1.7.3@lasote/stable"
        generators = "cmake", "gcc", "txt"
        options = {"shared": [True, False]} # Values can be True or False (number or string value is also possible)
        default_options = "shared=False", "Poco:shared=True", "OpenSSL:shared=True"
    
        def imports(self):
            self.copy("*.dll", dst="bin", src="bin") # From bin to bin
            self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
    
        def build(self):
            cmake = CMake(self.settings)
            shared_definition = "-DSHARED=1" if self.options.shared else ""
            self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, shared_definition))
            self.run('cmake --build . %s' % cmake.build_config)
   
   
Observe the **build** method. We are reading **self.options.shared** and appending a definition to our **cmake** command.

So let's use this option in our **CMakeLists.txt**:

.. code-block:: cmake
   :emphasize-lines: 7

    project(FoundationTimer)
    cmake_minimum_required(VERSION 2.8.12)
    
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
    
    if(SHARED)
      add_library(timer SHARED timer.cpp)
    else()
      add_library(timer STATIC timer.cpp)
    endif()
       
    target_link_libraries(timer PUBLIC ${CONAN_LIBS}) 
       
    add_executable(example main.cpp)
    target_link_libraries(example timer)
   

Now, we can pass the option ``shared`` to the install command. It will be stored in the ``conaninfo.txt``
file for later calls. So you can execute:

.. code-block:: bash
   :emphasize-lines: 2, 6
   
   $ mkdir build && cd build
   $ conan install .. -o shared=True
   $ conan build ..  
   ...
   $ rm -rf * (in the build folder, better to remove cmake temporaries)
   $ conan install .. -o shared=False
   $ conan build ..  
  
This feature is very convenient for example if you want to keep several different builds in parallel,
without having to delete and re-create build projects. As explained in :ref:`common workflows<workflows>`,
you could maintain **both shared and static builds** very easily:

.. code-block:: bash
   
   $ mkdir build_shared && cd build_shared
   $ conan install .. -o shared=True
   $ conan build ..  
   $ cd ..
   $ mkdir build_static && cd build_static
   $ conan install .. -o shared=False
   $ conan build .. 
   // now, move from build_static <-> build_shared as you want and
   $ conan build .. 



``conanfile.py`` becomes a self documented file for checking what options we can adjust to compile a library.


.. note::

   You can use **-DBUILD_SHARED_LIBS=ON** instead of **-DSHARED=1** and CMake will automatically build SHARED libraries,
   without the need of modifying your CMakeLists.
   We used a custom definition as an example to show you how to control your build through **conan options** and **cmake definitions**.

   

-------------------------------------------------------------------------------------------------------




Conditional settings, options and requirements
..............................................

Remember, in your ``conanfile.py`` you have also access to the options of your dependencies,
and you can use them to:

* Add requirements dynamically
* Change options values

The **config** method is the right place to change values of options and settings.

Here is an example of what we could do in our **config method**:

.. code-block:: python

      ...
      requires = "Poco/1.7.3@lasote/stable" # We will add OpenSSL dynamically "OpenSSL/1.0.2d@lasote/stable"
      ...

      def config(self):
          # We can control the options of our dependencies based on current options
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



There is another advantage of using ``conanfile.py`` instead of ``conanfile.txt``.

Scopes
......


Scopes vs options
_________________

In the previous example we added an option ``shared`` to our conanfile.py to control if the library has to be static or shared.

For the Poco package, if we specify ``shared=True`` or ``shared=False`` in the ``conan install`` command we get different binary packages.
When we declare new options we open the possibility of having multiple packages for the same recipe, as it happens with the settings.


First, we are going to see how to control the tests build with an **option** (generally not a good idea). Adding a new option ``build_tests`` we can control when to run the tests:

**conanfile.py**

.. code-block:: python
   :emphasize-lines: 3

     class PocoTimerConan(ConanFile):
        ...
        options = {"build_tests": [True, False]}  # NOT A GOOD APROACH
        default_options = "build_tests=False"
        ...

        def build(self):
            cmake = CMake(self.settings)
            flag_build_tests = "-DBUILD_TEST=1" if self.options.build_tests else ""
            self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, flag_build_tests))
            self.run('cmake --build . %s' % cmake.build_config)



**CMakeLists.txt**

.. code-block:: cmake

   option(BUILD_TEST OFF)
   if(BUILD_TEST)
       include(CTest)
       enable_testing()
       ...
   endif()


Then we could use ``conan install -o build_test=False/True`` to activate or deactivate the tests launch.


But, what happens if we are creating a conan package?

If we install our package specifying different values for the option "build_test", we will generate/require different conan packages,
but the library (binary artifact) will be the same, so, why different conan packages?

Conan has **scope variables** to control the conanfile.py without generating different packages no matter what is the value of the scope variable.


Now using scope variables:


**conanfile.py**

.. code-block:: python
   :emphasize-lines: 3

     class PocoTimerConan(ConanFile):
        ...

        def build(self):
            cmake = CMake(self.settings)
            flag_build_tests = "-DBUILD_TEST=1" if self.scope.build_tests else ""
            self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, flag_build_tests))
            self.run('cmake --build . %s' % cmake.build_config)


Then we could use ``conan install --scope build_test=False/True`` to activate or deactivate the tests launch.


``dev`` scope
_____________


There is a special scope variable called ``dev`` that is automatically set to True if you are using **conanfile.py** in your project.

If we export the recipe and install it from a local or remote repository, the variable ``dev`` will be False.

It's specially useful to require some testing packages (just for run the tests) or anything that not affect to the built artifact.

In the following example we will require the ``catch`` package for unit test our project:

.. code-block:: python
   :emphasize-lines: 6,10

     class PocoTimerConan(ConanFile):
        ...

        def config(self):
           if self.scope.dev:
              self.requires("catch/1.3.0@TyRoXx/stable")

        def build(self):
            cmake = CMake(self.settings)
            flag_build_tests = "-DBUILD_TEST=1" if self.scope.dev and self.scope.build_tests else ""
            self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, flag_build_tests))
            self.run('cmake --build . %s' % cmake.build_config)


It guarantees that when you build a conan package with your project, no one that requires it (from its conanfile.txt or its conanfile.py) will require the ``catch`` library, because it's not needed.


There is also a simplified way to require development packages:


.. code-block:: python
   :emphasize-lines: 5

     class PocoTimerConan(ConanFile):
        ...

        def config(self):
            self.requires("catch/1.3.0@TyRoXx/stable", dev=True)


An extra shortcut for this syntax would be to use the new ``dev_requires`` attribute:

.. code-block:: python
   :emphasize-lines: 2

     class PocoTimerConan(ConanFile):
        dev_requires = "catch/1.3.0@TyRoXx/stable"




Defining scopes
_______________

Setting a scope variable in a requirement is very similar to options:


.. code-block:: bash

   $ conan install --scope Poco:somescope=somevalue


If we want to set it in our project conanfile we don't specify the package namespace:

.. code-block:: bash

   $ conan install --scope somescope=somevalue


There is an special namespace called ``ALL`` that will apply to all our requirements and our conanfile:


.. code-block:: bash

   $ conan install --scope ALL:somescope=somevalue

Note that if defining specific values for a certain package, the specific value will have
precedence:

.. code-block:: bash

   $ conan install --scope ALL:somescope=somevalue Poco:somescope=othervalue

In this case, the scope ``somescope`` of Poco will have the value ``othervalue``


At this point you almost have your library prepared for being a conan package. In next section
we will create our own packages using ``conanfile.py``.


Build policies
..............

By default, ``conan install`` command will search for a binary package (corresponding to our settings and defined options) in a remote, if it's not present the install command will fail.

As we previously see, we can use the **--build** option to change the default ``conan install`` behaviour:

- **- -build some_package** will build only "some_package"
- **- -build missing** will build only the missing requires.
- **- -build** will build all requires from sources.
* **- -build outdated** will try to build from code if the binary is not built with the current recipe or when missing binary package 


With the ``build_policy`` attribute the package creator can change the default conan's build behavior.
The allowed build_policy values are:

- ``missing``: If no binary package is found, conan will build it without the need of invoke conan install with **--build missing** option.
- ``always``: The package will be built always, **retrieving each time the source code** executing the "source" method.


.. code-block:: python
   :emphasize-lines: 6

     class PocoTimerConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        requires = "Poco/1.7.3@lasote/stable" # comma separated list of requirements
        generators = "cmake", "gcc", "txt"
        default_options = "Poco:shared=True", "OpenSSL:shared=True"
        build_policy = "always" # "missing"

       
These build policies are specially useful if the package creator don't want to provide binary packages, for example with header only libraries.

The "always" policy, will retrieve the sources each time the package is installed so it can be useful for provide a "latest" mechanism or ignore the uploaded binary packages.
