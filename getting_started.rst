.. _getting_started:


Getting started
===============

As an example, let's start with one of the most popular C++ libraries: POCO.

We will use CMake. Even though it is not a **conan** requirement, it is very convenient.

A Timer using POCO libraries
----------------------------

First, let's create a folder for our project:

.. code-block:: bash

   $ mkdir mytimer
   $ cd mytimer
   

Create the following source file inside that folder:

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
   Poco/1.6.1@lasote/stable
   
   [generators]
   cmake


In this example we will use **cmake** to build the project, which is why the **cmake** generator is specified, but please feel free to use any other build system.   

.. note::
 
     If you are not a **cmake** user, change the [generators] section of your **conanfile.txt** to **gcc** or a more generic one **txt** to handle requirements with any build system.
     Learn more in :ref:`Manage your dependencies<manage_deps>`


Install the requirements:


.. code-block:: bash

   $ conan install


This command will download the binary package required for your configuration (detected the first time that you ran the conan command), **together
with other required libraries, like OpenSSL and Zlib**.

.. warning::

   There are binaries for Visual Studio 12, linux-gcc 4.9 and apple-clang 3.5. If you are using another setup,
   the command will fail because of the missing package. You could try to change your settings or build it 
   from source, using the **--build missing** option, instead of retrieving the binaries. Such a build might not have
   been tested and eventually fail. OpenSSL requires perl and some specific tools to build from source.


This command will also create a ``conanbuildinfo.cmake`` with useful variables (like
``CONAN_INCLUDE_DIRS`` and ``CONAN_LIBS``) for building your example.


Building the timer example
--------------------------

We can just include the generated file and use those variables inside our own ``CMakeLists.txt``,
that we should create inside our example folder: 

**CMakeLists.txt**

.. code-block:: cmake

   PROJECT(FoundationTimer)
   CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

   INCLUDE(conanbuildinfo.cmake)
   CONAN_BASIC_SETUP()
   
   ADD_EXECUTABLE(timer timer.cpp)
   TARGET_LINK_LIBRARIES(timer ${CONAN_LIBS})


Now, you are ready to build and run your project:

.. code-block:: bash

    $ mkdir build && cd build

    (win)
    $ cmake .. -G "Visual Studio 12 Win64"
    $ cmake --build . --config Release

    (linux, mac)
    $ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .
    ...
    [100%] Built target timer
    $> ./bin/timer


Building with other configurations
----------------------------------
Let's try building your timer project with a different configuration.
For example, you could try building the 32 bits version.

- The first time you run the **conan** command, your settings will be detected (compiler, architecture...) automatically.
- You can change your default settings by editing the ``~/.conan/conan.conf`` file-
- You can always override the default settings in **install** command with the **-s** parameter. Example:

.. code-block:: bash

    $ conan install -s arch=x86 -s compiler=gcc -s compiler.version=4.9

- You should install a different package, using the ``-s arch=x86`` setting
  , instead of the default used previously, that in most cases will be ``x86_64``
- You will also have to change your project build:
   * In Windows, change the cmake invocation accordingly to ``Visual Studio 12``
   * In Linux, you have to add the ``-m32`` flag to your CMakeLists.txt:
     ``SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m32")``, and the same to
     ``CMAKE_C_FLAGS, CMAKE_SHARED_LINK_FLAGS and CMAKE_EXE_LINKER_FLAGS``.
     This can also be done more easily, automatically with conan, as we'll see later.
   * In Mac, you need to add the definition ``-DCMAKE_OSX_ARCHITECTURES=i386``

Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:support@conan.io" target="_blank">write to us</a>
