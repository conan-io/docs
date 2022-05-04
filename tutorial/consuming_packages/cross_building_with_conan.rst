.. _consuming_packages_cross_building_with_conan:

How to cross-compile your applications using Conan: host and build contexts
===========================================================================

.. important::

    In this example, we will retrieve Conan packages from a Conan repository with
    packages compatible with Conan 2.0. To run this example successfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


In the previous examples, we learned how to use a *conanfile.py* or *conanfile.txt* to
build an application that compresses strings using the *Zlib* and *CMake* Conan
packages. Also, we explained that you can set information like the operating system,
compiler or build configuration in a file called the Conan profile.

For all these examples we used the same platform for building and running the application.
But, what if you want to build the application in your machine running Macos but you would
like that application to run it other platform like, for example, a Raspberry Pi? Conan
can model that case by using two different profiles, one for the machine that **builds**
the application (Macos) and another one for the machine that **runs** the application
(Raspberry Pi). We will explain this "two profiles" approach in the section that follows.

Conan two profiles: build and host profiles
-------------------------------------------

...

Read more
---------

- Using Conan with Android Studio

