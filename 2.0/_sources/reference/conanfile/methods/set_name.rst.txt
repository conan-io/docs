.. _reference_conanfile_methods_set_name:


set_name()
==========

Dynamically define ``name`` attribute. This method would be rarely needed, as the only use case that makes sense is when a recipe
is shared and used to create different packages with the same recipe. In most cases the recommended approach is to define the
``name = "mypkg"`` attribute in the recipe.

This method is executed only when the recipe is exported to the cache ``conan create`` and ``conan export``, and when the recipe
is being locally used, like with ``conan install .``. In all other cases, the name of the package is fully defined, and ``set_name()``
will not be called, so do not rely on it for any other functionality different than defining the ``self.name`` value.

If the current package name was defined in a *name.txt* file, it would be possible to do:

..  code-block:: python

    from conan import ConanFile
    from conan.tools.files import load

    class Pkg(ConanFile):
        def set_name(self):
            # This will execute relatively to the current user directory (name.txt in cwd)
            self.name = load(self, "name.txt")
            # if "name.txt" is located relative to the conanfile.py better do:
            self.name = load(self, os.path.join(self.recipe_folder, "name.txt"))

The package name can also be defined in command line for some commands with ``--name=xxxx`` argument. If we want to prioritize the
command line argument we should do:

..  code-block:: python

    from conan import ConanFile
    from conan.tools.files import load

    class Pkg(ConanFile):
        def set_name(self):
            # Command line ``--name=xxxx`` will be assigned first to self.name and have priority
            self.name = self.name or load(self, "name.txt")


The ``set_name()`` method can decide to define the ``name`` value, irrespective of the potential
``--name=xxx`` command line argument, that can be even completely ignored by ``set_name()``. It 
is the responsibility of the developer to provide a correct ``set_name()``:

.. code-block:: python

    def set_name(self):
        # This will always assign "pkg" as name, ignoring ``--name`` command line argument
        # and without erroring or warning
        self.name = "pkg"


If a command line argument ``--name=xxx`` is provided, it will be initialized in the ``self.name``
attribute, so ``set_name()`` method can read and use it:

.. code-block:: python

    def set_name(self):
        # Takes the provided command line ``--name`` argument and creates a name appending to
        # it the ".extra" string
        self.name = self.name + ".extra"


.. warning::

    The ``set_name()`` method is an alternative to the ``name`` attribute. It is
    not advised or supported to define both a ``name`` attribute and a ``set_name()`` method. 
