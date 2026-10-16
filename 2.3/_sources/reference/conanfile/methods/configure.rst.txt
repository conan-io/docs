.. _reference_conanfile_methods_configure:

configure()
===========

The ``configure()`` method should be used for the configuration of settings and options in the recipe
for later use in the different methods like ``generate()``, ``build()`` or ``package()``. This
method executes while building the dependency graph and expanding the packages dependencies, which means
that when this method executes the dependencies are still not there, they do not exist, and it is not
possible to access ``self.dependencies``.

For example, for a C (not C++) library, the ``compiler.libcxx`` and ``compiler.cppstd`` settings shouldn't
even exist during the ``build()``. It is not only that they are not part of the ``package_id``, but
they shouldn't be used in the build process at all. They will be defined in the profile, because
other packages in the graph can be C++ packages and need them, but it is the responsibility of this
recipe to remove them so they are not used in the recipe:

.. code-block:: python
    
    settings = "os", "compiler", "build_type", "arch"

    def configure(self):
        # Not all compilers have libcxx subsetting, so we use rm_safe
        # to avoid exceptions
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

    def package_id(self):
        # No need to delete those settings here, they were already deleted
        pass

For packages where you want to remove every subsetting of a setting, you can use the ``rm_safe`` method
with a wildcard:

.. code-block:: python

    settings = "os", "compiler", "build_type", "arch"

    def configure(self):
        self.settings.rm_safe("compiler.*")


This will remove all the subsettings of the ``compiler`` setting, like ``compiler.libcxx`` or ``compiler.cppstd``,
but keep the ``compiler`` setting itself (Which ``self.settings.rm_safe("compiler")`` would remove).

Likewise, for a package containing a library, the ``fPIC`` option really only applies when the
library is compiled as a static library, but otherwise, the ``fPIC`` option doesn't make sense,
so it should be removed:

..  code-block:: python

    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def configure(self):
        if self.options.shared:
            # fPIC might have been removed in config_options(), so we use rm_safe
            self.options.rm_safe("fPIC")

.. _reference_conanfile_methods_configure_implementations:

Available automatic implementations
+++++++++++++++++++++++++++++++++++

.. include:: ../../../common/experimental_warning.inc

When the ``configure()`` method is not defined, Conan can automatically manage some
conventional options if specified in the
:ref:`implements<conan_conanfile_attributes_implements>` ConanFile attribute:

auto_shared_fpic
----------------

Options automatically managed:

- ``fPIC`` (True, False).
- ``shared`` (True, False).
- ``header_only`` (True, False).

It can be added to the recipe like this:

.. code-block:: python
    
    from conan import ConanFile
        
    class Pkg(ConanFile):
        implements = ["auto_shared_fpic"]
        ...

Then, if no ``configure()`` method is specified in the recipe, Conan will
automatically manage the fPIC setting in the ``configure`` step like this:

.. code-block:: python

    if conanfile.options.get_safe("header_only"):
        conanfile.options.rm_safe("fPIC")
        conanfile.options.rm_safe("shared")
    elif conanfile.options.get_safe("shared"):
        conanfile.options.rm_safe("fPIC")

Be aware that adding this implementation to the recipe may also affect the
:ref:`configure<reference_conanfile_methods_config_options_implementations>` step.

If you need to implement custom behaviors in your recipes but also need this logic, it
must be explicitly declared:

.. code-block:: python


    def configure(self):
        if conanfile.options.get_safe("header_only"):
            conanfile.options.rm_safe("fPIC")
            conanfile.options.rm_safe("shared")
        elif conanfile.options.get_safe("shared"):
            conanfile.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")


Recipes can suggest values for their dependencies options as ``default_options = {"*:shared": True}``, but
it is not possible to do that conditionally. For this purpose, it is also possible to use the
``configure()`` method:

..  code-block:: python

    def configure(self):
        if something:
            self.options["*"].shared = True


.. note::

    **Best practices**

    - Recall that it is **not** possible to define ``settings`` or ``conf`` values in recipes, they are read only.
    - The definition of ``options`` values is only a "suggestion", depending on the graph computation, priorities, etc., the final value of ``options`` can be different from the one set by the recipe.


.. seealso::

    - Follow the :ref:`tutorial about recipe configuration methods<tutorial_creating_configure>`.