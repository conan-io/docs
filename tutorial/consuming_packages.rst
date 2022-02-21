.. _tutorial_consuming_packages:

Consuming Packages
==================

This section shows how to build your projects using Conan to manage your dependencies. We
will begin with a :ref:`basic example <consuming_packages_getting_started>` of a C project
that uses CMake and depends on the **zlib** library. This project will use a
*conanfile.txt* file to declare it's dependencies.

We will also cover how you can not only use 'regular' libraries with Conan but also
:ref:`manage tools you may need to use while building <consuming_packages_tool_requires>`:
like CMake, msys2, MinGW, etc. 

Then, we will explain different Conan concepts like settings and options and how you can
use them to :ref:`build your projects for different
<consuming_packages_different_configurations>` configurations like Debug, Release, with
static or shared libraries, etc. 

Also, we will explain how to transition from the *conanfile.txt* file we used in the first
example to a :ref:`a more powerful conanfile.py
<consuming_packages_the_power_of_conanfile_py>`.

.. toctree::
   :maxdepth: 2
   :caption: Table of contents
   
   consuming_packages/getting_started
   consuming_packages/build_tools_as_conan_packages
   consuming_packages/different_configurations
   consuming_packages/the_power_of_conanfile_py
