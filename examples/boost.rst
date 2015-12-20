.. _boost_example:

Boost
=====

Boost doesn't need any intro. Let's go straight to build the typical regex example against Boost 1.60.
There are more than 60 pre-built binary packages in conan.io, check them at https://www.conan.io/source/Boost/1.60.0/lasote/stable


It is very easy to setup your own project, but here is a repository for convenience:


.. code-block:: bash

   $ git clone https://github.com/memsharded/example-boost.git


It contains a very simple ``CMakeLists.txt``, the ``main.cpp`` source file of the regex example
and a ``conanfile.txt`` with the following contents:

.. code-block:: text

   [requires]
   Boost/1.60.0@lasote/stable
   
   [generators]
   cmake
   
   [imports]
   bin, *.dll -> ./bin
   lib, *.dylib* -> ./bin


Install the requirements, configure the project with CMake, and build it:

.. code-block:: bash

   $ cd example-boost
   $ mkdir build && cd build
   $ conan install ..
   $ cmake .. -G "Visual Studio 14 Win64"
   $ cmake --build . --config Release
   $ cd bin
   $ regex

The above configuration assumes that your predefined settings are VS14, 64 bits, Release, MD runtime.
If your settings are different, just specify them at the conan install, e.g.:

.. code-block:: bash

   $ conan install .. -s compiler="Visual Studio" -s compiler.version=12 -s arch=x86 -s build_type=Debug -s compiler.runtime=MDd
   $ cmake .. -G "Visual Studio 12"
   $ cmake --build . --config Debug

In the above case it is important to specify the runtime ``MDd`` to be compatible with the ``Debug`` 
version we are requesting.


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
   
