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

After that, we will introduce the concept of Conan build and host profiles and explain how
you can use them to cross-compile your application to different platforms.

Then, in the "Introduction to versioning" we will learn about using different versions, 
defining requirements with version ranges, the concept of revisions and a brief introduction 
to lockfiles to achieve reproducibility of the dependency graph.


.. toctree::
   :maxdepth: 2
   :caption: Table of contents
   
   consuming_packages/build_simple_cmake_project
   consuming_packages/use_tools_as_conan_packages
   consuming_packages/different_configurations
   consuming_packages/the_flexibility_of_conanfile_py
   consuming_packages/cross_building_with_conan.rst
   consuming_packages/intro_to_versioning
