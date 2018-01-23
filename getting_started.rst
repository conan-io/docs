.. _getting_started:


Getting started
===============

Let's start with an example using one of the most popular C++ libraries: POCO_. For convenience purposes we'll use CMake.
Keep in mind that Conan **works with any build system** and does not depend on CMake.

.. _POCO: https://pocoproject.org/


A Timer using POCO libraries
----------------------------

First, let's create a folder for our project:

.. code-block:: bash

   $ mkdir mytimer
   $ cd mytimer
   
.. note::

    If your code is in a GitHub repository you can simply clone the project, instead of creating this folder, using the following command:
    
    .. code-block:: bash
    
       $ git clone https://github.com/memsharded/example-poco-timer.git mytimer
       
       
Next, create the following source files inside this folder:


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


Now, create a ``conanfile.txt`` inside this folder with the following content:

**conanfile.txt**

.. code-block:: text

   [requires]
   Poco/1.8.0.1@pocoproject/stable
   
   [generators]
   cmake


In this example we will use **cmake** to build the project, which is why the **cmake** generator is specified. This generator will create a ``conanbuildinfo.cmake`` file that defines cmake variables as include paths and library names, that can be used in our build.

.. note::
 
     If you are not a **cmake** user, change the [generators] section of your **conanfile.txt** to **gcc** or a more generic **txt** to handle requirements with any build system.
     Learn more on :ref:`Using packages<manage_deps>`.


Just include the generated file and use these variables inside our ``CMakeLists.txt``:

**CMakeLists.txt**

.. code-block:: cmake

   project(FoundationTimer)
   cmake_minimum_required(VERSION 2.8.12)
   add_definitions("-std=c++11")

   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup()
   
   add_executable(timer timer.cpp)
   target_link_libraries(timer ${CONAN_LIBS})
   
Installing dependencies
--------------------------
If you have a terminal with light colors, like the default gnome terminal in Ubuntu, set ``CONAN_COLOR_DARK=1`` for better contrast.
Then create a build folder, for temporary build files, and install the requirements (pointing to the parent directory, where the conanfile.txt is located):


.. code-block:: bash

   $ mkdir build && cd build
   $ conan install ..

The ``install`` command will download the binary package required for your configuration (which is detected the first time you run the conan command), **together
with other (transitively required by Poco) libraries, like OpenSSL and Zlib**. 
It will also create the ``conanbuildinfo.cmake`` file in the current directory, in which you can see the cmake defined variables, and a ``conaninfo.txt`` where information about settings, requirements and options is saved.


It is very important to understand the installation process. When a ``conan install`` command is issued, it will use the settings specified in the command line or taken from the defaults in ``<userhome>/.conan/profiles/default`` file.

.. image:: images/install_flow.png
   :height: 400 px
   :width: 500 px
   :align: center

For a ``$ conan install -s os="Linux" -s compiler="gcc"`` command, the steps are:

- Check if the package recipe (for the Poco/1.8.0.1@pocoproject/stable package) exists in the conan local cache. If we are just starting, the cache will be empty.
- Search for the package recipe in the defined remotes. By default, Conan comes with the Bintray remotes defined (this can be changed), and the conan client will search in `conan-center` and `conan-transit` for the recipe.
- If the recipe exists, the conan client will fetch and store it in your local cache.
- With the package recipe and the input settings (Linux, gcc), the conan client will check in the local cache if the corresponding binary exists. This does not apply for the initial installation.
- The Conan client will search for the corresponding binary package in the remote, if it exists, it will be fetched.
- The Conan client will then complete generating the requested files specified in ``generators``.

If the binary package necessary for some given settings doesn't exist, the conan client will throw an error. It is possible to try to build the binary package from sources with the ``--build missing`` command line argument to install. A detailed description of how a binary package is built from sources is provided in a later section.

.. warning::

   In the Bintray repositories there are binaries for several mainstream compilers and versions, such as Visual Studio 12, 14, linux-gcc 4.9 and apple-clang 3.5.
   If you are using another setup, the command might fail because of the missing package. You can try to change your settings or build the package from source, using the ``--build missing`` option, instead of retrieving the binaries. Such a build might not have been tested and eventually fail.


Building the timer example
--------------------------

Now you are ready to build and run your project:

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

The retrieved packages are installed on your local user cache (typically ``.conan/data``), and can be reused in other projects. This allows to keep you current project clean and to continue working even without network connection. Search packages in the local cache using:

.. code-block:: bash

    $ conan search 

Inspect binary package detais (for different installed binaries for a given package recipe) using:

.. code-block:: bash

    $ conan search Poco/1.8.0.1@pocoproject/stable

Generate a table for all binaries from a given recipe using the ``--table`` option, even in remotes:

.. code-block:: bash

    $ conan search zlib/1.2.11@conan/stable --table=file.html -r=conan-center
    $ file.html # or open the file, double-click

.. image:: /images/search_binary_table.png
    :height: 250 px
    :width: 300 px
    :align: center


Check the reference for more information on how to search in remotes, how to remove or clean packages from the local cache, and how to define a custom cache directory per user or per project.

Inspect your current project dependencies with the ``info`` command, pointing it to the folder where the ``conanfile.txt`` is:

.. code-block:: bash

    $ conan info ..

Generate a graph of your dependencies, in dot or html formats:

.. code-block:: bash

    $ conan info .. --graph=file.html
    $ file.html # or open the file, double-click

.. image:: /images/info_deps_html_graph.png
    :height: 150 px
    :width: 200 px
    :align: center


Building with other configurations
----------------------------------
As an exercise, try building your timer project with a different configuration.
For example, you could try building the 32 bits version.

- The first time you run the **conan** command, your settings will be detected (compiler, architecture...) automatically.
- You can change your default settings by editing the ``~/.conan/profiles/default`` file
- You can always override the default settings in **install** command with the **-s** parameter. Example:

.. code-block:: bash

    $ conan install -s arch=x86 -s compiler=gcc -s compiler.version=4.9

- Install a different package, using the ``-s arch=x86`` setting, instead of the default used previously, that in most cases will be ``x86_64``
- Change your project build:
   * In Windows, change the cmake invocation accordingly to ``Visual Studio 14``
   * In Linux, add the ``-m32`` flag to your CMakeLists.txt:
     ``SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m32")``, and the same to
     ``CMAKE_C_FLAGS, CMAKE_SHARED_LINK_FLAGS and CMAKE_EXE_LINKER_FLAGS``.
     This can also be done more easily, automatically with conan, as we'll see later.
   * In Mac, add the definition ``-DCMAKE_OSX_ARCHITECTURES=i386``

Have a question? Check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write to us</a>
