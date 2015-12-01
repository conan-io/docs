.. _google_test_example:

Google Test
===========

Google Test is a  framework for writing C++ tests on a variety of platforms.
We are going to see an example of how to use GTest with conan.


The source code
---------------

Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


This is our project layout:

.. code-block:: text

    my_project/
          ├── test/
          │   ├── encryption.cpp
          │
          ├── my_library.cpp
          ├── my_library.h
          ├── conanfile.txt
          ├── CMakeLists.txt
  
We will compile our project with CMake, so we use the **cmake** generator in ``conanfile.txt``

         
Installing requirements
-----------------------


.. code-block:: bash

   $ conan install



Compiling and running our tests
-------------------------------

Build your project normally with cmake:

.. code-block:: bash

   $ mkdir build && cd build 
   $ cmake ../ -DBUILD_TEST=TRUE && cmake --build .


And execute the test!

.. code-block:: bash

   $ cd bin
   $ ./encryption_test
   
   [100%] Built target mytest
	Running main() from gtest_main.cc
	[==========] Running 1 test from 1 test case.
	[----------] Global test environment set-up.
	[----------] 1 test from TestingEncryption
	[ RUN      ] TestingEncryption.cipher
	
	
	Decrypted text is:
	The quick brown fox jumps over the lazy dog
	[       OK ] TestingEncryption.cipher (2 ms)
	[----------] 1 test from TestingEncryption (2 ms total)
	
	[----------] Global test environment tear-down
	[==========] 1 test from 1 test case ran. (2 ms total)
	[  PASSED  ] 1 test.



Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
   
