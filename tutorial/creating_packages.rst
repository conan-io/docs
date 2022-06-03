.. _tutorial_creating_packages:

Creating packages
=================

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
   
   creating_packages/create_your_first_package
   creating_packages/handle_sources_in_packages
   creating_packages/add_dependencies_to_packages
   creating_packages/preparing_the_build
   creating_packages/validate_and_configure_packages
   creating_packages/build_packages
   creating_packages/install_packages
   creating_packages/define_package_information
   creating_packages/test_conan_packages
   creating_packages/other_types_of_packages
