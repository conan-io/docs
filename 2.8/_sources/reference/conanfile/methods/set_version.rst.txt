.. _reference_conanfile_methods_set_version:


set_version()
=============

Dynamically define ``version`` attribute. This method might be needed when the same recipe is being used to create different versions
of the same package, and such version is defined elsewhere, like in the git branch or in a text or build script file. This would be a common situation.

This method is executed only when the recipe is exported to the cache ``conan create`` and ``conan export``, and when the recipe
is being locally used, like with ``conan install .``. In all other cases, the version of the package is fully defined, and ``set_version()``
will not be called, so do not rely on it for any other functionality different than defining the ``self.version`` value.

If the current package version was defined in a *version.txt* file, it would be possible to do:

..  code-block:: python

    from conan import ConanFile
    from conan.tools.files import load

    class Pkg(ConanFile):
        def set_version(self):
            # This will execute relatively to the current user directory (version.txt in cwd)
            self.version = load(self, "version.txt")
            # if "version.txt" is located relative to the conanfile.py better do:
            self.version = load(self, os.path.join(self.recipe_folder, "version.txt"))

The package version can also be defined in command line for some commands with ``--version=xxxx`` argument. If we want to prioritize the
command line argument we should do:

..  code-block:: python

    from conan import ConanFile
    from conan.tools.files import load

    class Pkg(ConanFile):
        def set_version(self):
            # Command line ``--version=xxxx`` will be assigned first to self.version and have priority
            self.version = self.version or load(self, "version.txt")

A common use case could be to define the ``version`` dynamically from some version control mechanism, like the current git tag. This
could be done with:

..  code-block:: python

    from conan import ConanFile
    from conan.tools.scm import Git

    class Pkg(ConanFile):
        name = "pkg"
        
        def set_version(self):
            git = Git(self, self.recipe_folder)
            self.version = git.run("describe --tags")


The ``set_version()`` method can decide to define the ``version`` value, irrespective of the potential
``--version=xxx`` command line argument, that can be even completely ignored by ``set_version()``. It 
is the responsibility of the developer to provide a correct ``set_version()``:

.. code-block:: python

    def set_version(self):
        # This will always assign "2.1" as version, ignoring ``--version`` command line argument
        # and without erroring or warning
        self.version = "2.1"


If a command line argument ``--version=xxx`` is provided, it will be initialized in the ``self.version``
attribute, so ``set_version()`` method can read and use it:

.. code-block:: python

    def set_version(self):
        # Takes the provided command line ``--version`` argument and creates a version appending to
        # it the ".extra" string
        self.version = self.version + ".extra"


.. warning::

    The ``set_version()`` method is an alternative to the ``version`` attribute. It is
    not advised or supported to define both a ``version`` class attribute and a ``set_version()`` method. 
