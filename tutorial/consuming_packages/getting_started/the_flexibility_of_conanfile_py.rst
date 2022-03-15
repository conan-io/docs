.. _consuming_packages_getting_started_flexibility_of_conanfile_py:

Understanding the flexibility of using conanfile.py vs conanfile.txt
====================================================================

.. important::

    In this example, we will retrieve Conan packages from a Conan repository with
    packages compatible for Conan 2.0. To run this example succesfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


In the previous examples, we declared our dependencies (*Zlib* and *CMake*) in a
*conanfile.txt* file. Let's have a look at that file:

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    zlib/1.2.11

    [tool_requires]
    cmake/3.19.8

    [generators]
    CMakeDeps
    CMakeToolchain

Using a *conanfile.txt* to build your projects using Conan it's enough for simple cases,
but if you need more flexibility you should use a *conanfile.py* file where you can use
Python code to make things such as adding requirements dinamically, changing options
depending on other options or setting options for your requirements. Let's see an example
on how to migrate to a *conanfile.py* and use some of those features.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd tutorial/consuming_packages/getting_started/conanfile_py



Read more
=========

- Importing resource files in the generate() method
- Layouts advanced use
