

How to capture package version from text or build files
=======================================================

It is common that a library version number would be already encoded in a text file, in some build scripts, etc.
Lets take as an example that we have the following library layout, that we want to create a package from it:

.. code-block:: text

    conanfile.py
    CMakeLists.txt
    src
       hello.cpp
       ...


The *CMakeLists.txt* will have some variables to define the library version number. Lets assume for simplicity
that it has some line like:

.. code-block:: cmake

    cmake_minimum_required(VERSION 2.8)
    set(MY_LIBRARY_VERSION 1.2.3) # This is the version we want
    add_library(hello src/hello.cpp)


We will typically have in our *conanfile.py* package recipe:


.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "1.2.3"


Usually this takes very little maintenance, and when the CMakeLists version is bumped, the *conanfile.py* version is bumped too.
But if you want to only have to update the *CMakeLists.txt* version, you can extract the version dynamically, with:


.. code-block:: python

    from conans import ConanFile
    from conans.tools import load
    import re

    def get_version():
        try:
            content = load("CMakeLists.txt")
            version = re.search(b"set\(MY_LIBRARY_VERSION (.*)\)", content).group(1)
            return version.strip()
        except Exception as e:
            return None

    class HelloConan(ConanFile):
        name = "Hello"
        version = get_version()


Even if the *CMakeLists.txt* file is not exported to the local cache, it will still work, as the ``get_version()`` function returns None
when it is not found, then taking the version number from the package metadata (layout).
