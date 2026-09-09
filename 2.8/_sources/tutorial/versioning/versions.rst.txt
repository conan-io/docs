.. _tutorial_versioning_versions:

Versions
========

This section explains how different versions of a given package can be created, first starting with
manually changing the version attribute in the ``conanfile.py`` recipe, and then introducing the
``set_version()`` method as a mechanism to automate the definition of the package version.

.. note::

    This section uses very simple, empty recipes without building any code, so without ``build()``,
    ``package()``, etc., to illustrate the versioning with the simplest possible recipes, and allowing
    the examples to run easily and to be very fast and simple. In real life, the recipes would be 
    full-blown recipes as seen in previous sections of the tutorial, building actual libraries and packages.


Let's start with a very simple recipe:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile

    class pkgRecipe(ConanFile):
        name = "pkg"
        version = "1.0"

        # The recipe would export files and package them, but not really
        # necessary for the purpose of this part of the tutorial
        # exports_sources = "include/*"
        # def package(self):
        #    ...


That we can create ``pkg/1.0`` package with:

.. code-block:: bash

    $ conan create .
    ...
    pkg/1.0 .
    ...

    $ conan list "*"
    Local Cache
      pkg
        pkg/1.0

If we now did some changes to the source files of this library,
this would be a new version, and we could change the ``conanfile.py`` version to ``version = "1.1"`` and
create the new ``pkg/1.1`` version:

.. code-block:: bash

    # Make sure you modified conanfile.py to version=1.1
    $ conan create .
    ...
    pkg/1.1 .
    ...

    $ conan list "*"
    Local Cache
      pkg
        pkg/1.0
        pkg/1.1

As we can see, now we see in our cache both ``pkg/1.0`` and ``pkg/1.1``. The Conan cache can store
any number of different versions and configurations for the same ``pkg`` package.


Automating versions
-------------------

Instead of manually changing the version in ``conanfile.py``, it is possible to automate it with 2 different approaches.

First it is possible to provide the ``version`` directly in the command line. In the example above, we could
remove the ``version`` attribute from the recipe and do:

.. code-block:: bash

    # Make sure you removed the version attribute in conanfile.py
    $ conan create . --version=1.2
    ...
    pkg/1.2 .
    ...

    $ conan list "*"
    Local Cache
      pkg
        pkg/1.0
        pkg/1.1
        pkg/1.2


The other possibility is to use the ``set_version()`` method to define the version dynamically, for example, if
the version already exists in the source code or in a text file, or it should be deduced from the git version.

Let's assume that we have a ``version.txt`` file in the repo, that contains just the version string ``1.3``. 
Then, this can be done:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.files import  load


    class pkgRecipe(ConanFile):
        name = "pkg"

        def set_version(self):
            self.version = load(self, "version.txt")


.. code-block:: bash

    # No need to specify the version in CLI arg or in recipe attribute
    $ conan create .
    ...
    pkg/1.3 .
    ...

    $ conan list "*"
    Local Cache
      pkg
        pkg/1.0
        pkg/1.1
        pkg/1.2
        pkg/1.3

It is also possible to combine the command line version definition, falling back to reading from file if the
command line argument is not provided with the following syntax:

.. code-block:: python
    :caption: conanfile.py

    def set_version(self):
        # if self.version is already defined from CLI --version arg, it will
        # not load version.txt
        self.version = self.version or load(self, "version.txt")

.. code-block:: bash

    # This will create the "1.4" version even if the version.txt file contains "1.3"
    $ conan create . --version=1.4
    ...
    pkg/1.4 .
    ...

    $ conan list "*"
    Local Cache
      pkg
        pkg/1.0
        pkg/1.1
        pkg/1.2
        pkg/1.3
        pkg/1.4

Likewise, it is possible to obtain the version from a Git tag:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.scm import Git

    class pkgRecipe(ConanFile):
        name = "pkg"

        def set_version(self):
            git = Git(self)
            tag = git.run("describe --tags")
            self.version = tag


.. code-block:: bash

    # assuming this is a git repo, and it was tagged to 1.5
    $ git init .
    $ git add .
    $ git commit -m "initial commit"
    $ git tag 1.5
    $ conan create .
        ...
        pkg/1.5 .
        ...

        $ conan list "*"
        Local Cache
          pkg
            pkg/1.0
            pkg/1.1
            pkg/1.2
            pkg/1.3
            pkg/1.4
            pkg/1.5

.. note::

    **Best practices**

    - We could try to use something like the branch name or the commit as the version number. However this might
      have some disadvantages, for example, when this package is being required, it will need a explicit
      ``requires = "pkg/commit"`` in every other package recipe requiring this one, and it might be difficult to
      update consumers consistently, and to know if a newer or older dependency is being used.


Requiring the new versions
--------------------------

When a new package version is created, if other package recipes requiring this one contain a explicit ``requires``,
pinning the exact version like:

.. code-block:: python
    :caption: app/conanfile.py

    from conan import ConanFile

    class AppRecipe(ConanFile):
        name = "app"
        version = "1.0"
        requires = "pkg/1.0"

Then, installing or creating the ``app`` recipe will keep requiring and using the ``pkg/1.0`` version and not 
the newer ones. To start using the new ``pkg`` versions, it is necessary to explicitly update the ``requires`` like:

.. code-block:: python
    :caption: app/conanfile.py

    from conan import ConanFile

    class AppRecipe(ConanFile):
        name = "app"
        version = "1.0"
        requires = "pkg/1.5"


This process, while it achieves very good reproducibility and traceability, can be a bit tedious if we are
managing a large dependency graph and we want to move forward to use the latest dependencies versions faster 
and with less manual intervention. To automate this, the *version-ranges* explained in the next section can be used.
