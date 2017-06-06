.. _getting_started:


Getting started
===============

As an example, let's start with one of the most popular C++ libraries: [POCO](https://pocoproject.org/).
Conan **works with any build system** and it does not depend on CMake, though we will use CMake for this example for convenience.

A Timer using POCO libraries
----------------------------

First, let's create a folder for our project:

.. code-block:: bash

   $ mkdir mytimer
   $ cd mytimer
   
.. note::

    if you have the code in a github repository, instead of creating the folder, you can
    just clone the project
    
    .. code-block:: bash
    
       $ git clone https://github.com/memsharded/example-poco-timer.git mytimer
       
       
Create the following source files inside that folder :


**timer.cpp**

.. code-block:: cpp

	// $Id: //poco/1.4/Foundation/samples/Timer/src/Timer.cpp#1 $
	// This sample demonstrates the Timer and Stopwatch classes.
	// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
	// and Contributors.
	// SPDX-License-Identifier:	BSL-1.0

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


Now, also create a ``conanfile.txt`` inside the same folder with the following content:

**conanfile.txt**

.. code-block:: text

   [requires]
   Poco/1.7.3@lasote/stable
   
   [generators]
   cmake


In this example we will use **cmake** to build the project, which is why the **cmake** generator 
is specified. This generator will create
a ``conanbuildinfo.cmake`` file that defines cmake variables as include paths and library names,
that can be used in our build.

.. note::
 
     If you are not a **cmake** user, change the [generators] section of your **conanfile.txt** to **gcc** or a more generic one **txt** to handle requirements with any build system.
     Learn more in :ref:`Using packages<manage_deps>`


Just include the generated file and use those variables inside our own ``CMakeLists.txt``: 

**CMakeLists.txt**

.. code-block:: cmake

   project(FoundationTimer)
   cmake_minimum_required(VERSION 2.8.12)

   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup()
   
   add_executable(timer timer.cpp)
   target_link_libraries(timer ${CONAN_LIBS})
   
Installing dependencies
--------------------------
Lets create a build folder, so temporary build files are put there, and install the requirements
(pointing to the parent directory, as it is where the conanfile.txt is):


.. code-block:: bash

   $ mkdir build && cd build
   $ conan install ..

This ``install`` command will download the binary package required for your configuration
(detected the first time that you ran the conan command), **together
with other (transitively required by Poco) libraries, like OpenSSL and Zlib**. 
It will also create the ``conanbuildinfo.cmake`` file in the current directory, in which you
can see the cmake defined variables, and a ``conaninfo.txt`` where information about settings,
requirements and options is saved.


It is very important to understand the installation process. When a ``conan install`` command is issued, it will use some settings, specified in the command line or taken from the defaults in ``<userhome>/.conan/conan.conf`` file.

.. image:: images/install_flow.png
   :height: 400 px
   :width: 500 px
   :align: center

So for a command like ``$ conan install -s os="Linux" -s compiler="gcc"``, the steps are:

- First check if the package recipe (for Poco/1.7.3@lasote/stable package) exist in the conan local cache. If we are just starting, our cache will be empty.
- Look for the package recipe in the defined remotes. By default, conan comes with the conan.io remote defined (you can change that), so the conan client will look in conan.io if such package recipe exists.
- If exists, it will fetch the package recipe and store it in your local cache.
- With the package recipe and the input settings (Linux, gcc), it will check in the local cache if the corresponding binary is there, if we are installing for the first time, it won't.
- Conan will try to look for the corresponding package binary in the remote, if such package binary exists, it will be fetched.
- It will finish generating the requested files specified in ``generators``.

If the package binary necessary for some given settings doesn't exist, it will throw an error. It is possible to try to build the package binary from sources with the ``--build missing`` command line argument to install. Detailed explanations about how a package binary is built from sources will be done in a later section.

.. warning::

   In conan.io there are binaries for several mainstream compilers and versions, like Visual Studio 12, 14, linux-gcc 4.9 and apple-clang 3.5.
   If you are using another setup, the command might fail because of the missing package. You could try to change your settings or build it 
   from source, using the **--build missing** option, instead of retrieving the binaries. Such a build might not have
   been tested and eventually fail. OpenSSL requires perl and some specific tools to build from source.


Building the timer example
--------------------------

Now, you are ready to build and run your project:

.. code-block:: bash

    (win)
    $ cmake .. -G "Visual Studio 14 Win64"
    $ cmake --build . --config Release

    (linux, mac)
    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .
    ...
    [100%] Built target timer
    $ ./bin/timer
    Callback called after 250 milliseconds.
    ...


Inspecting dependencies
-----------------------

The retrieved packages have been installed to your local user cache (typically ``.conan/data``), 
so they can be reused from there in other projects, and allow to clean your current project and 
keep working even without network connection. To search packages in the local cache you can do:

.. code-block:: bash

    $ conan search 

You can also inspect the package binaries (for different installed binaries for a given package recipe) details with:

.. code-block:: bash

    $ conan search Poco/1.7.3@lasote/stable

Please check the reference for more information on how to search in remotes, or how to remove
or clean packages from the local cache, or how to define custom cache directory per user or per project.

You can also inspect your current projects dependencies with the ``info`` command, pointing it to
the folder where the ``conanfile.txt`` is:

.. code-block:: bash

    $ conan info ..


Building with other configurations
----------------------------------
As an exercise to the reader, try building your timer project with a different configuration.
For example, you could try building the 32 bits version.

- The first time you run the **conan** command, your settings will be detected (compiler, architecture...) automatically.
- You can change your default settings by editing the ``~/.conan/conan.conf`` file
- You can always override the default settings in **install** command with the **-s** parameter. Example:

.. code-block:: bash

    $ conan install -s arch=x86 -s compiler=gcc -s compiler.version=4.9

- You should install a different package, using the ``-s arch=x86`` setting, instead of the default used previously, that in most cases will be ``x86_64``
- You will also have to change your project build:
   * In Windows, change the cmake invocation accordingly to ``Visual Studio 14``
   * In Linux, you have to add the ``-m32`` flag to your CMakeLists.txt:
     ``SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m32")``, and the same to
     ``CMAKE_C_FLAGS, CMAKE_SHARED_LINK_FLAGS and CMAKE_EXE_LINKER_FLAGS``.
     This can also be done more easily, automatically with conan, as we'll see later.
   * In Mac, you need to add the definition ``-DCMAKE_OSX_ARCHITECTURES=i386``

Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write to us</a>
