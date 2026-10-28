Toolchains
==========

.. warning:

    This is a very **EXPERIMENTAL** feature, introduced in Conan 1.26, with limited functionality,
    and subject to breaking changes in the future.
    The current goal is to gather experience and feedback
    to evolve it, while adding more build systems.

    Please try it and provide feedback at: https://github.com/conan-io/conan/issues

.. warning:

    Starting in Conan 1.32 ``toolchain()`` method and ``toolchain`` attribute have been
    deprecated. They will be removed in Conan 1.33, please use ``generate()`` instead of
    ``toolchain()`` and ``generators = "ToolChainClassName"`` instead of
    ``toolchain`` attribute.

Toolchains are the new, experimental way to integrate with build systems in Conan.
Recipes can define a ``generate()`` method that will return an object which
can generate files from the current configuration that can be used by the build systems.
Conan *generators* provide information about dependencies, while toolchains provide a
"translation" from the Conan settings and options, and the recipe defined configuration
to something that the build system can understand. A recipe that does not have dependencies
does not need a generator, but can still use a toolchain.

A toolchain can be defined, among the built-ins toolchains, with an attribute with the name of the
toolchain class to use.

.. code:: python

    generators = "<ToolChainClassName>"

For example, for using the CMake toolchain this should be declared in the recipe:

.. code:: python

    generators = "CMakeToolchain"

.. note::

    At the moment (Conan 1.32), the available built-in toolchains are ``CMakeToolchain``,
    ``MSBuildToolchain`` and ``MesonToolchain``.

But in the more general case, and if it needs any specific configuration beyond the default
one:


.. code:: python

    from conan.tools.cmake import CMakeToolchain

    def generate(self):
        tc = CMakeToolchain(self)
        # customize toolchain "tc"
        tc.generate()


It is possible to use the ``generate()`` method to create your own files, which will typically be
deduced from the current configuration of ``self.settings`` and ``self.options``.

.. code:: python

    from conans.tools import save

    def generate(self):
        # Based on the self.settings, self.options, the user
        # can generate their own files:
        save("mytoolchain.tool", "my own toolchain contents, deduced from the settings and options")
        # The "mytoolchain.tool" file can be used by the build system to
        # define the build


And as usual, you can create your own toolchain helpers, put them in a ``python_requires`` package and reuse them in all
your recipes.


Toolchains have some important advantages:

- They execute at :command:`conan install` time. They generate files, not command line
  arguments, providing better reproducibility and debugging of builds.
- They provide a better developer experience. The command line used by developers locally, like
  ``cmake ...`` will achieve the same build, with the same flags, as the :command:`conan build` or
  the build that is done in the cache with a :command:`conan create`.
- They are more extensible and configurable.

The toolchains implement most of the build system logic, leaving the build helpers, like ``CMake()``,
doing less work, and acting basically as a high level wrapper of the build system. Many of the
existing arguments, attributes or methds of those build helpers will not be available. Check
the documentation of each toolchain to check the associated build helper available functionality.


.. code:: python

    from conan.tools.cmake import CMakeToolchain, CMake

    def generate(self):
        tc = CMakeToolchain(self)
        # customize toolchain "tc"
        tc.generate()

    def build(self):
        # NOTE: This is a simplified helper
        # Not all arguments attributes and methods might be available
        cmake = CMake(self)


To learn more about existing built-in toolchains, read the reference in :ref:`conan_tools`.
