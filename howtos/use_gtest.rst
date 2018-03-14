.. _google_test_example:

How to test test your project with Google Test
==============================================

Google Test is a framework for writing C++ tests on a variety of platforms.
We are going to see an example of how to use GTest with conan.


The source code
---------------

Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


This is our project layout:

.. code-block:: text

    conan-gtest-example/
          ├── .travis.yml
          ├── .gitlab-ci.yml
          ├── appveyor.yml
          ├── CMakeLists.txt
          ├── conanfile.py
          ├── encrypter.cpp
          ├── encrypter.h
          ├── LICENSE
          ├── README.md
          └── test_package
              ├── CMakeLists.txt
              ├── conanfile.py
              └── encryption_test.cpp


We will compile our project with CMake and Conan, so we use the **cmake** generator in ``conanfile.py``


Installing requirements, compiling and running our tests
--------------------------------------------------------

Conan will install all dependencies, build your project, create a package and run all tests

.. code-block:: bash

    $ conan create . demo/testing

The :command:`conan create` automates all steps for you. However, you need to create the test directory and *conanfile.py* to make sure that
your package is correct.

CMake
-----

Optionally, you could use CMake to build your project:

Install requirements

.. code-block:: bash

   $ conan install .

Build your project normally with CMake:

.. code-block:: bash

   $ mkdir build && cd build
   $ cmake .. && cmake --build .

If you just want to build the project, all steps can be executed directly
by CMake, or just invoking :command:`conan build`.


Step by step
------------

You could execute all Conan steps individually,

Install dependencies

.. code-block:: bash

   $ conan install .

Export and build the project

.. code-block:: bash

   $ conan export . lasote/testing
   $ conan install conan-gtest-example/0.1.0@lasote/testing --build conan-gtest-example

So far, the package was exported and created, without testing.

Build test project

.. code-block:: bash

   $ cd test_package
   $ mkdir build && cd build
   $ conan install ..
   $ conan build ..


And run!

.. code-block:: bash

    $ bin/encryption_test

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
