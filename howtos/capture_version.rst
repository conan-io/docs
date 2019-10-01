When is the version computed and saved
======================================

The version of a recipe is stored in the package metadata when it is exported and always taken from
the metadata later on.

On the other hand the version of a recipe is a class attribute that is evaluated everytime that the
recipe is parsed. For this reason it is important that computing it never raises an exception, even
if its value is ignored.

How to capture package version from SCM: git
============================================

The ``Git()`` helper from tools can be used to capture data from the Git repo in which
the *conanfile.py* recipe resides, and use it to define the version of the Conan package.

.. code-block:: python

    from conans import ConanFile, tools

    def get_version():
        git = tools.Git()
        try:
            return "%s_%s" % (git.get_branch(), git.get_revision())
        except:
            return None

    class HelloConan(ConanFile):
        name = "Hello"
        version = get_version()

        def build(self):
            ...

In this example, the package created with :command:`conan create` will be called 
``Hello/branch_commit@user/channel``. Note: this function should never raise, see the section about
when the version is computed and saved above.

How to capture package version from SCM: svn
============================================

The ``SVN()`` helper from tools can be used to capture data from the subversion repo in which
the *conanfile.py* recipe resides, and use it to define the version of the Conan package.

.. code-block:: python

    from conans import ConanFile, tools

    def get_svn_version(version):
        try:
            scm = tools.SVN()
            revision = scm.get_revision()
            branch = scm.get_branch() # Delivers e.g trunk, tags/v1.0.0, branches/my_branch
            branch = branch.replace("/","_")
            if scm.is_pristine():
                dirty = ""
            else:
                dirty = ".dirty"
            return "%s-%s+%s%s" % (version, revision, branch, dirty) # e.g. 1.2.0-1234+trunk.dirty
        except Exception:
            return None

    class HelloLibrary(ConanFile):
        name = "Hello"
        version = get_svn_version("1.2.0")
        
        def build(self):
            ...

In this example, the package created with :command:`conan create` will be called 
``Hello/generated_version@user/channel``. Note: this function should never raise, see the section
about when the version is computed and saved above.

How to capture package version from text or build files
=======================================================

It is common that a library version number would be already encoded in a text file, build scripts, etc.
As an example, let's assume we have the following library layout, and that we want to create a package from it:

.. code-block:: text

    conanfile.py
    CMakeLists.txt
    src
       hello.cpp
       ...


The *CMakeLists.txt* will have some variables to define the library version number. For simplicity, let's also assume
that it includes a line such as the following:

.. code-block:: cmake

    cmake_minimum_required(VERSION 2.8)
    set(MY_LIBRARY_VERSION 1.2.3) # This is the version we want
    add_library(hello src/hello.cpp)


Typically, our *conanfile.py* package recipe will include:


.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "1.2.3"


This usually requires very little maintenance, and when the CMakeLists version is bumped, so is the *conanfile.py* version.
However, if you only want to have to update the *CMakeLists.txt* version, you can extract the version dynamically, using:


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

Note: this function should never raise, see the section about when the version is computed and saved
above.
