.. _consuming_packages_intro_versioning:

Introduction to versioning
==========================

So far we have been using requires with fixed versions like ``requires = "zlib/1.2.12"``.
But sometimes dependencies evolve, new versions are released and consumers want to update to those versions as easy as possible.

It is always possible to edit the ``conanfiles`` and explicitly update the versions to the new ones, but there are mechanisms in
Conan to allow such updates without even modifying the recipes.


Version ranges
--------------

A ``requires`` can express a dependency to a certain range of versions for a given package, with the syntax ``pkgname/[version-range-expression]``.
Let's see an example, please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/consuming_packages/versioning

We can see that we have there:

.. code-block:: python
    :caption: **conanfile.py**

    from conan import ConanFile


    class CompressorRecipe(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeToolchain", "CMakeDeps"

        def requirements(self):
            self.requires("zlib/[~1.2]")

That ``requires`` contains the expression ``zlib/[~1.2]``, which means "approximately" ``1.2`` version, that means, it can resolve to
any ``zlib/1.2.8``, ``zlib/1.2.11`` or ``zlib/1.2.12``, but it will not resolve to something like ``zlib/1.3.0``. Among the available
matching versions, a version range will always pick the latest one.

If we do a :command:`conan install`, we would see something like:

.. code-block:: bash

    $ conan install .

    Graph root
        conanfile.py: .../conanfile.py
    Requirements
        zlib/1.2.12#87a7211557b6690ef5bf7fc599dd8349 - Downloaded
    Resolved version ranges
        zlib/[~1.2]: zlib/1.2.12

If we tried instead to use ``zlib/[<1.2.12]``, that means that we would like to use a version lower than ``1.2.12``, but that one is excluded,
so the latest one to satisfy the range would be ``zlib/1.2.11``:

.. code-block:: bash

    $ conan install .

    Resolved version ranges
        zlib/[<1.2.12]: zlib/1.2.11


The same applies to other type of requirements, like ``tool_requires``.
If we add now to the recipe:

.. code-block:: python
    :caption: **conanfile.py**

    from conan import ConanFile


    class CompressorRecipe(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeToolchain", "CMakeDeps"

        def requirements(self):
            self.requires("zlib/[~1.2]")
        
        def build_requirements(self):
            self.tool_requires("cmake/[>3.10]")


Then we would see it resolved to the latest available CMake package, with at least version ``3.11``:

.. code-block:: bash

    $ conan install .
    ...
    Graph root
        conanfile.py: .../conanfile.py
    Requirements
        zlib/1.2.12#87a7211557b6690ef5bf7fc599dd8349 - Cache
    Build requirements
        cmake/3.22.6#f305019023c2db74d1001c5afa5cf362 - Downloaded
    Resolved version ranges
        cmake/[>3.10]: cmake/3.22.6
        zlib/[~1.2]: zlib/1.2.12


Revisions
---------

What happens when a package creator does some change to the package recipe or to the source code, but they don't bump the ``version`` 
to reflect those changes? Conan has an internal mechanism to keep track of those modifications, and it is called the **revisions**.

The recipe revision is the hash that can be seen together with the package name and version in the form ``pkgname/version#recipe_revision``
or ``pkgname/version@user/channel#recipe_revision``.
The recipe revision is a hash of the contents of the recipe and the source code. So if something changes either in the recipe,
its associated files or in the source code that this recipe is packaging, it will create a new recipe revision.

You can list existing revisions with the :command:`conan list` command:

.. code-block:: bash

    $ conan list zlib/1.2.12#* -r=conancenter

    conancenter
      zlib
        zlib/1.2.12
          revisions
            82202701ea360c0863f1db5008067122 (2022-03-29 15:47:45 UTC)
            bd533fb124387a214816ab72c8d1df28 (2022-05-09 06:59:58 UTC)
            3b9e037ae1c615d045a06c67d88491ae (2022-05-13 13:55:39 UTC)
            ...


Revisions always resolve to the latest (chronological order of creation or upload to the server) revision.
Though it is not a common practice, it is possible to explicitly pin a given recipe revision directly in the ``conanfile``, like:

.. code-block:: python

    def requirements(self):
        self.requires("zlib/1.2.12#87a7211557b6690ef5bf7fc599dd8349")

This mechanism can however be tedious to maintain and update when new revisions are created, so probably in the general case, this
shouldn't be done.


.. _tutorial_consuming_packages_versioning_lockfiles:

Lockfiles
---------

The usage of version ranges, and the possibility of creating new revisions of a given package without bumping the version allows
to do automatic faster and more convenient updates, without need to edit recipes. 

But in some occasions, there is also a need to provide an immutable and reproducible set of dependencies. This process is known
as "locking", and the mechanism to allow it is "lockfile" files. A lockfile is a file that contains a fixed list of dependencies,
specifying the exact version and exact revision. So, for example, a lockfile will never contain a version range with an expression,
but only pinned dependencies. 

A lockfile can be seen as a snapshot of a given dependency graph at some point in time.
Such snapshot must be "realizable", that is, it needs to be a state that can be actually reproduced from the conanfile recipes.
And this lockfile can be used at a later point in time to force that same state, even if there are new created package versions.

Let's see lockfiles in action. First, let's pin the dependency to ``zlib/1.2.11`` in our example:


.. code-block:: python

    def requirements(self):
        self.requires("zlib/1.2.11")

And let's capture a lockfile:

.. code-block:: bash

    conan lock create .

    -------- Computing dependency graph ----------
    Graph root
        conanfile.py: .../conanfile.py
    Requirements
        zlib/1.2.11#4524fcdd41f33e8df88ece6e755a5dcc - Cache

    Generated lockfile: .../conan.lock

Let's see what the lockfile ``conan.lock`` contains:

.. code-block:: json

    {
        "version": "0.5",
        "requires": [
            "zlib/1.2.11#4524fcdd41f33e8df88ece6e755a5dcc%1650538915.154"
        ],
        "build_requires": [],
        "python_requires": []
    }

Now, let's restore the original ``requires`` version range:

.. code-block:: python

    def requirements(self):
        self.requires("zlib/[~1.2]")


And run :command:`conan install .`, which by default will find the ``conan.lock``, and run the equivalent :command:`conan install . --lockfile=conan.lock`

.. code-block:: bash

    conan install .

    Graph root
        conanfile.py: .../conanfile.py
    Requirements
        zlib/1.2.11#4524fcdd41f33e8df88ece6e755a5dcc - Cache


Note how the version range is no longer resolved, and it doesn't get the ``zlib/1.2.12`` dependency, even if it is the 
allowed range ``zlib/[~1.2]``, because the ``conan.lock`` lockfile is forcing it to stay in ``zlib/1.2.11`` and that exact revision too.


Read more
---------

- :ref:`Introduction to Versioning<tutorial_versioning>`

