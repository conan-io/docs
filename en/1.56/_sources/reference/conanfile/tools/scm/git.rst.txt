.. _conan_tools_scm_git:

Git
===

.. warning::

    This tool is **experimental** and subject to breaking changes. This tool is intended to replace the current ``conans.tools.Git`` and the current ``scm`` attribute, that will be removed in Conan 2.0.

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

constructor
-----------

.. code-block:: python

    def __init__(self, conanfile, folder=".")


Construct a ``Git`` object, specifying the current directory, by default ``"."``, the current working directory.


get_commit()
------------

.. code-block:: python
    
    def get_commit(self)


Returns the current commit, with ``git rev-list HEAD -n 1 -- <folder>``. The latest commit is returned, irrespective of local not committed changes.


get_remote_url()
----------------

.. code-block:: python
    
    def get_remote_url(self, remote="origin")


Obtains the URL of the ``remote`` git remote repository, with ``git remote -v``

.. warning::

    This method will get the output from ``git remote -v``. If you added tokens or credentials to the remote in the URL, they will be
    exposed. Credentials shouldn't be added to git remotes definitions, but using a credentials manager or similar mechanism.
    If you still want to use this approach, it is your responsibility to strip the credentials from the result.


commit_in_remote()
------------------

.. code-block:: python
    
    def commit_in_remote(self, commit, remote="origin")


Checks that the given commit exists in the remote, with ``branch -r --contains <commit>`` and checking an occurrence of a branch in that remote exists.


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
    
    def clone(self, url, target="", args=None)


Performs a ``git clone <url> <args> <target>`` operation,
where `target` is the target directory.

Optional arguments can be passed as a list, for example:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.scm import Git

    class App(ConanFile):
        version = "1.2.3"

        def source(self):
            git = Git(self)
            clone_args = ['--depth', '1', '--branch', self.version]
            git.clone(url="https://path/to/repo.git", args=clone_args)

    
checkout()
----------

.. code-block:: python
    
    def checkout(self, commit)


Checkouts the given commit


get_url_and_commit()
--------------------

.. code-block:: python
    
    def get_url_and_commit(self, remote="origin")
        # returns a (url, commit) tuple


.. warning::

    This method will get the output from ``git remote -v``. If you added tokens or credentials to the remote in the URL, they will be
    exposed. Credentials shouldn't be added to git remotes definitions, but using a credentials manager or similar mechanism.
    If you still want to use this approach, it is your responsibility to strip the credentials from the result.


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


included_files()
----------------

Returns the list of files not ignored by ``.gitignore``

.. code-block:: python

    def included_files(self):


This method runs ``git ls-files --full-name --others --cached --exclude-standard`` and returns the result as a list.
It can be used for implementing a controlled ``export`` of files not gitignored, something like:

.. code-block:: python

    def export_sources(self):
        git = Git(self)
        included = git.included_files()
        for i in included:
            dst =  os.path.join(self.export_sources_folder, i)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(i, dst)


run()
-----

Available since: `1.53.0 <https://github.com/conan-io/conan/releases/tag/1.53.0>`_

.. code-block:: python
    
    def run(self, cmd)


Executes `git <cmd>` and returns the console output of the command.

For example, if you want to print the git version, just pass ``cmd="--version"`` as
argument:

.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.scm import Git

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"

        def export(self):
            git = Git(self)
            self.output.info(git.run("--version"))



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
