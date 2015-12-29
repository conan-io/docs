.. _openssl_example:

OpenSSL
=======

The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.

It is very easy to set up your own project with conan, but here is a repository for convenience:


.. code-block:: bash

   $ git clone https://github.com/lasote/example-openssl.git


It contains a very simple ``CMakeLists.txt``, the ``main.cpp`` source file of the md5 example
and a ``conanfile.txt`` with the following contents:

.. code-block:: text

    [requires]
    OpenSSL/1.0.2e@lasote/stable
    
    [generators]
    cmake
    
    [imports]
    bin, *.dll -> ./bin
    lib, *.dylib* -> ./bin


Install the requirements, configure the project with CMake, and build it:

.. code-block:: bash

   $ cd example-openssl
   $ mkdir build && cd build
   $ conan install ..
   $ cmake .. -G "Visual Studio 14 Win64"
   $ cmake --build . --config Release
   $ cd bin
   $ regex

.. note::

    If you don't want OpenSSL binary packages you can always build OpenSSL from source using **"conan install --build OpenSSL"**.

The above configuration assumes that your predefined settings are VS14, 64 bits, Release, MD runtime.
If your settings are different, just specify them while executing conan install, e.g.:

.. code-block:: bash

   $ conan install .. -s compiler="Visual Studio" -s compiler.version=12 -s arch=x86 -s build_type=Debug -s compiler.runtime=MDd
   $ cmake .. -G "Visual Studio 12"
   $ cmake --build . --config Debug

In the case above, it is important to specify the runtime ``MDd`` to be compatible with the ``Debug`` 
version we are requesting.

This is the project's ``CMakeLists.txt``:

.. code-block:: cmake

    PROJECT(ExampleOpenSSL)
    CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
    
    INCLUDE(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    CONAN_BASIC_SETUP()
    
    ADD_EXECUTABLE(md5 main.cpp)
    TARGET_LINK_LIBRARIES(md5 ${CONAN_LIBS})


Non CMake projects
------------------
Even if you are not using ``cmake`` in your project, it is possible to use conan. Put the
following ``conanfile.txt`` in your project root:

.. code-block:: text

   [requires]
   OpenSSL/1.0.2e@lasote/stable

   [generators]
   visual_studio

   [imports]
   bin, *.dll -> ./bin
   lib, *.dylib* -> ./bin


Install your requirements as above:

.. code-block:: bash

   $ conan install -s compiler="Visual Studio" -s compiler.version=14 -s arch=x86 -s build_type=Release

Then follow the instructions in :ref:`Visual Studio generator <visual_studio>` to load the generated
``conanbuildinfo.props`` into your project. Ensure that your project configuration matches the
installed requirements and build as usual. The above ``conanfile.txt`` assumes that the output
directory will be the ``bin`` one, and will put the OpenSSL dynamic libraries there, if needed. You
can either configure your Visual Studio project or your ``conanfile.txt`` to use the same output
directory for convenience when launching or debugging your application.

There are :ref:`other generators <generators>` available. Check the docs!


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
   
