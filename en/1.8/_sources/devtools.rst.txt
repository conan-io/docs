.. _package_tools_apps:

Package apps and devtools
--------------------------

With conan it is possible to package and deploy applications.
It is also possible that these applications are also dev-tools, like compilers (e.g. MinGW), or build systems (e.g. CMake).

This section describes how to package and run executables, and also how to package dev-tools. 
Also, how to apply applications like dev-tools or even libraries (like testing frameworks) to other packages to build them from sources:``build_requires``

.. toctree::
   :maxdepth: 2

   devtools/running_packages
   devtools/create_installer_packages
   devtools/build_requires
