.. _tutorial_consuming_packages:

Consuming packages
==================

This section shows how to build your projects using Conan to manage your dependencies. We
will begin with a basic example of a C project that uses CMake and depends on the **zlib**
library. This project will use a *conanfile.txt* file to declare its dependencies.

We will also cover how you can not only use 'regular' libraries with Conan but also manage
tools you may need to use while building: like CMake, msys2, MinGW, etc. 

Then, we will explain different Conan concepts like settings and options and how you can
use them to build your projects for different configurations like Debug, Release, with
static or shared libraries, etc. 

Also, we will explain how to transition from the *conanfile.txt* file we used in the first
example to a more powerful *conanfile.py*.

.. toctree::
   :maxdepth: 2
   :caption: Table of contents
   
   consuming_packages/build_simple_cmake_project
   consuming_packages/use_tools_as_conan_packages
   consuming_packages/different_configurations
   consuming_packages/the_flexibility_of_conanfile_py
