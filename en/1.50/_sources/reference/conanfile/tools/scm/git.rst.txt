.. _conan_tools_scm_git:

Git
===

.. warning::

    This tool is **experimental** and subject to breaking changes. This tool is intended to replace the current ``conans.tools.Git`` and the current ``scm`` attribute, that will be removed in Conan 2.0.


constructor
-----------

.. code-block:: python

    def __init__(self, conanfile, folder=".")


Construct a ``Git`` object, specifying the current directory, by default ``"."``, the current working directory.


get_commit()
------------

.. code-block:: python
    
    def get_commit(self)


Returns the current commit, with ``git rev-list HEAD -n 1 -- <folder>``. The latest commit is returned, irrespective of local not commmited changes.


get_remote_url()
----------------

.. code-block:: python
    
    def get_remote_url(self, remote="origin")


Obtains the URL of the ``remote`` git remote repository, with ``git remote -v``


commit_in_remote()
------------------

.. code-block:: python
    
    def commit_in_remote(self, commit, remote="origin")


Checks that the given commit exists in the remote, with ``branch -r --contains <commit>`` and checking an occurence of a branch in that remote exists.


is_dirty()
----------

.. code-block:: python
    
    def is_dirty(self)


Returns if the current folder is dirty, running ``git status -s``



get_repo_root()
---------------

.. code-block:: python
    
    def get_repo_root(self)


Returns the current repository top folder with ``git rev-parse --show-toplevel``



clone()
-------

.. code-block:: python
    
    def clone(self, url, target="")


Does a ``git clone <url> <target>`` 


checkout()
----------

.. code-block:: python
    
    def checkout(self, commit)


Checkouts the given commit


get_url_and_commit()
--------------------

.. code-block:: python
    
    def get_url_and_commit(self, remote="origin")


This is an advanced method, that returns both the current commit, and the remote repository url.
This method is intended to capture the current remote coordinates for a package creation, so that can be used later to build
again from sources from the same commit. This is the behavior:

- If the repository is dirty, it will raise an exception. Doesn't make sense to capture coordinates of something dirty, as
  it will not be reproducible. If there are local changes, and the user wants to test a local ``conan create``, should commit
  the changes first (locally, not push the changes).
- If the repository is not dirty, but the commit doesn't exist in the given remote, the method will return that commit and the
  URL of the local user checkout. This way, a package can be ``conan create`` created locally, testing everything works, before
  pushing some changes to the remote.
- If the repository is not dirty, and the commit exists in the specified remote, it will return that commit and the url of the
  remote. 


Example: Implementing the ``scm`` feature 
-----------------------------------------

This example is the new way to implement the ``scm`` feature (the ``scm`` attribute will be removed in Conan 2.0, and the way it will survive is the one described in this section), using this new ``Git`` capabilities.

Assume we have this project with this layout, in a git repository:

.. code-block:: text

        ├── conanfile.py
        ├── CMakeLists.txt
        ├── src
        │   └── hello.cpp


And the conanfile.py is:


.. code-block:: python

        import os
        from conan import ConanFile
        from conan.tools.scm import Git
        from conan.tools.files import load, update_conandata


        class Pkg(ConanFile):
            name = "pkg"
            version = "0.1"

            def export(self):
                git = Git(self, self.recipe_folder)
                scm_url, scm_commit = git.get_url_and_commit()
                # we store the current url and commit in conandata.yml
                update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

            def layout(self):
                self.folders.source = "."

            def source(self):
                # we recover the saved url and commit from conandata.yml and use them to get sources
                git = Git(self)
                sources = self.conan_data["sources"]
                git.clone(url=sources["url"], target=".")
                git.checkout(commit=sources["commit"])

            def build(self):
                # build() will have access to the sources, obtained with the clone in source()
                cmake = os.path.join(self.source_folder, "CMakeLists.txt")
                hello = os.path.join(self.source_folder, "src/hello.cpp")
                self.output.info("MYCMAKE-BUILD: {}".format(load(self, cmake)))
                self.output.info("MYFILE-BUILD: {}".format(load(self, hello)))


This conanfile does:

- In the ``export()`` method, it captures the url and commit, according to the rules of ``get_url_and_commit()`` above
- The url and commit are saved in the ``conandata.yml``
- These two first steps happen in the ``conan export`` or first part of ``conan create`` when the recipe is exported to the cache.
- When the recipe is building from sources in the cache, it will call the ``source()`` method which will clone and checkout from 
  the user folder if the commit is only local or from the git remote if the commit is remote too.

This ``conan create`` flow is not recommended for continuous usage. To develop and test, users should use the local flow (``conan install`` + build system).
Only in the last stage, to check that things are looking good to push, the user can do a local commit, and before pushing, do a ``conan create`` to check
locally.
