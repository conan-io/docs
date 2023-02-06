.. _reference_conanfile_methods_configure:

configure()
===========

The ``configure()`` method should be used for configuration of settings and options in the recipe
for later use in the different methods like ``generate()``, ``build()`` or ``package()``. This
method executes while building the dependency graph and expanding the packages dependencies, that means
that when this method executes the dependencies are still not there, they do not exist, and it is not
possible to access ``self.dependencies``.

For example, for a C (not C++) library, the ``compiler.libcxx`` and ``compiler.cppstd`` shouldn't
even exist during the ``build()``. It is not only that they are not part of the ``package_id``, but
they shouldn't be used in the build process at all. They will be defined in the profile, because
other packages in the graph can be C++ packages and need them, but it is the responsibility of this
recipe to remove them so they are not used in the recipe:

.. code-block:: python
    
    settings = "os", "compiler", "build_type", "arch"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def package_id(self):
        # No need to delete those settings here, they were already deleted
        pass

Likewise, for a package containing a library, the ``fPIC`` option really only applies when the
library is compiled as a static library, but otherwise, the ``fPIC`` option doesn't make sense,
so it should be removed:

..  code-block:: python

    options = {"shared": [True, False]
    default_options = {"shared": False}

    def configure(self):
        if self.options.shared:
            del self.options.fPIC


Recipes can suggest dependencies option values as ``default_options = {"*:shared": True}``, but 
it is not possible to do that conditionally. For this purpose, it is also possible to use the
``configure()`` method:

..  code-block:: python

    def configure(self):
        if something:
            self.options["*"].shared = True


.. note::

    **Best practices**

    - Recall it is **not** possible to define ``settings`` or ``conf`` values in recipes, they are read only. 
    - The definition of ``options`` values is only a "suggestion", but not always defining the value, depending on the graph computation, priorities, etc., the final value of ``options`` can be different.
