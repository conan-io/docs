Toolchains
==========

.. warning: 

    This is a very **EXPERIMENTAL** feature, introduced in Conan 1.26, only supporting CMake
    and with limited functionality, and subject to breaking changes in the future.
    The current goal is to gather experience and feedback
    to evolve it, while adding more build systems.

    Please try it and provide feedback at: https://github.com/conan-io/conan/issues


Toolchains are the new, experimental way to integrate with build systems in Conan.
Recipes can define a ``toolchain()`` method that will return an object which
can generate files from the current configuration that can be used by the build systems.
Conan *generators* provide information about dependencies, while toolchains provide a
"translation" from the Conan settings and options, and the recipe defined configuration
to something that the build system can understand. A recipe that does not have dependencies
does not need a generator, but can still use a toolchain.

A toolchain can be defined, among the built-ins toolchains, with an attribute:

.. code:: python

    toolchain = "cmake"

.. note::

    At the moment (Conan 1.26), the only available toolchain is the CMake one.

But in the more general case, and if it needs any specific configuration beyond the default
one:


.. code:: python

    from conans import CMakeToolchain

    def toolchain(self):
        tc = CMakeToolchain(self)
        # customize toolchain "tc"
        return tc


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

    from conans import CMakeToolchain, CMake

    def toolchain(self):
        tc = CMakeToolchain(self)
        # customize toolchain "tc"
        return tc

    def build(self):
        # NOTE: This is a simplified helper
        # Not all arguments attributes and methods might be available
        cmake = CMake(self)


Built-in toolchains
-------------------

.. toctree::
   :maxdepth: 2

   toolchains/cmake
