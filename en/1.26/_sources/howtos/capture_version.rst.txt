.. _capture_version:

How to dynamically define the name and version of a package
===========================================================

The ``name`` and ``version`` fields are used to define constant values. The ``set_name()`` and ``set_version()``
methods can be used to dynamically define those values, for example if we want to extract the version from a text
file or from the git repository.

The version of a recipe is stored in the package metadata when it is exported (or created) and always taken from
the metadata later on. This means that the ``set_name()`` and ``set_version()`` methods will not be executed once
the recipe is in the cache, or when it is installed from a server. Both methods will use the current folder as
the current working directory to resolve relative paths. To define paths relative to the location of the *conanfile.py*
use the ``self.recipe_folder`` attribute.


How to capture package version from SCM: git
============================================

The ``Git()`` helper from tools can be used to capture data from the Git repo in which
the *conanfile.py* recipe resides, and use it to define the version of the Conan package.

.. code-block:: python

    from conans import ConanFile, tools

    class HelloConan(ConanFile):
        name = "hello"

        def set_version(self):
            git = tools.Git(folder=self.recipe_folder)
            self.version = "%s_%s" % (git.get_branch(), git.get_revision())

        def build(self):
            ...

In this example, the package created with :command:`conan create` will be called 
``hello/branch_commit@user/channel``.

How to capture package version from SCM: svn
============================================

The ``SVN()`` helper from tools can be used to capture data from the subversion repo in which
the *conanfile.py* recipe resides, and use it to define the version of the Conan package.

.. code-block:: python

    from conans import ConanFile, tools

    class HelloLibrary(ConanFile):
        name = "hello"
        def set_version(self):
            scm = tools.SVN(folder=self.recipe_folder)
            revision = scm.get_revision()
            branch = scm.get_branch() # Delivers e.g trunk, tags/v1.0.0, branches/my_branch
            branch = branch.replace("/","_")
            if scm.is_pristine():
                dirty = ""
            else:
                dirty = ".dirty"
            self.version = "%s-%s+%s%s" % (version, revision, branch, dirty) # e.g. 1.2.0-1234+trunk.dirty
        
        def build(self):
            ...

In this example, the package created with :command:`conan create` will be called 
``hello/generated_version@user/channel``. Note: this function should never raise, see the section
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

You can extract the version dynamically using:

.. code-block:: python

    from conans import ConanFile
    from conans.tools import load
    import re, os

    class HelloConan(ConanFile):
        name = "hello"
        def set_version(self):
            content = load(os.path.join(self.recipe_folder, "CMakeLists.txt"))
            version = re.search(b"set\(MY_LIBRARY_VERSION (.*)\)", content).group(1)
            self.version = version.strip()
