.. _reference_conanfile_methods_package_id:

package_id()
============

Conan computes a unique ``package_id`` reference for each configuration, including ``settings``, ``options`` and ``dependencies`` versions.
This ``package_id()`` method allows some customizations and changes over the computed ``package_id``, in general with the goal to relax some of the global binary compatibility assumptions.

The general rule is that every different value of ``settings`` and ``options`` creates a different ``package_id``. This rule can be relaxed or expanded following different approaches:

- A given package recipe can decide in its ``package_id()`` that the final binary is independent of some settings, for example if it is a header-only library, that uses input settings to build some tests, it might completely clear all configuration, so the resulting ``package_id`` is always the same irrespective of the inputs. Likewise a C library might want to remove the effect of ``compiler.cppstd`` and/or ``compiler.libcxx`` from its binary ``package_id``, because as a C library, its binary will be independent.
- A given package recipe can implement some partial erasure of information, for example to obtain the same ``package_id`` for a range of compiler versions. This type of binary compatibility is in general better addressed with the global ``compatibility`` plugin, or with the ``compatibility()`` method if the global plugin is not enough.
- A package recipe can decide to inject extra variability in its computed ``package_id``, adding ``conf`` items or "target" settings.

.. _reference_conanfile_methods_package_id_implementations:

Available automatic implementations
+++++++++++++++++++++++++++++++++++

.. include:: ../../../common/experimental_warning.inc

When the ``package_id()`` method is not defined, the following automatic implementation
can be specified in the :ref:`implements<conan_conanfile_attributes_implements>` ConanFile
attribute:

auto_header_only
----------------

Conan will automatically manage the package ID clearing settings and options when the
recipe declares an option ``header_only=True`` or when ``package_type`` is
``"header-library"``. It can be added to the recipe like this:

.. code-block:: python
    
    from conan import ConanFile
        
    class Pkg(ConanFile):
        implements = ["auto_header_only"]
        ...

Then, if no ``package_id()`` method is specified in the recipe, Conan will
automatically manage it and call ``self.info.clear()`` in the ``package_id()`` automatically,
to make the ``package_id`` independent of settings, options, configuration and requirements.


If you need to implement custom behaviors in your recipes but also need this logic, it
must be explicitly declared, for example, something like this:

.. code-block:: python

    def package_id(self):
        def package_id(self):
            if self.package_type == "header-library":
                self.info.clear()
            else:
                self.info.settings.rm_safe("compiler.libcxx")
                self.info.settings.rm_safe("compiler.cppstd")


.. _reference_conanfile_methods_package_id_clear:

Information erasure
-------------------

This is a ``package_id`` relaxing strategy. Let's check the first case: a header-only library, that has input ``settings``, because it still wants to use them for some unit-tests in its ``build()`` method. In order to have exactly one final binary for all configurations, because the final artifact should be identical in all cases (just the header files), it would be necessary to do:

.. code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build(self):
        cmake = CMake(self) # need specific settings to build
        ...
        cmake.test()  # running unit tests for the current configuration

    def package_id(self):
        # Completely clear all the settings from the ``package_id`` information ("info" object)
        # All resulting ``package_id`` will be the same, irrespective of configuration 
        self.info.settings.clear()


.. warning::

    The modifications of the information always happen over the ``self.info`` object, not on ``self.settings`` or ``self.options``


If a package is just a C library, but it couldn't remove the ``compiler.cppstd`` and ``compiler.libcxx`` in the ``configure()`` method (the recommended approach for most cases, to guarantee those flags are not used in the build), because there are C++ unit tests to the C library, then as the tests are not packaged and the final binary will be independent of C++, those could be removed with:

.. code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build(self):
        # building C++ tests for a C library

    def package_id(self):
        del self.info.settings.compiler.cppstd
        # Some compilers might not declare libcxx subsetting
        self.info.settings.rm_safe("compiler.libcxx")


If a package is building an executable to be used as a tool, and only 1 executable for each OS and architecture is desired to be more efficient, the ``package_id()`` could remove the other settings and options if existing:

.. code-block:: python

    # this will be a "tool_require"
    package_type = "application"
    settings = "os", "compiler", "arch", "build_type"

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

Note that this doesn't mean that the ``compiler`` and ``build_type`` should be removed for every application executable. For other things that are not tools, but final products to release, the most common situation is that maintaining the different builds for the different compilers, compiler versions, build types, etc. is the best approach.
It also means that we are erasing some information. We will not have the information of the compiler and build type that was used for the binary that we are using (it will not be in the ``conan list`` output, and it will not be in the server metadata either). If we compile a new binary with a different compiler or build type, it will create a new package revision under the same ``package_id``.


Partial information erasure
---------------------------

It is also possible to partially erase information for given subsets of values. For example, if we want to have the same ``package_id`` for all the binaries compiled with ``gcc`` between versions 4.5 and 5.0, we can do:

.. code-block:: python

    def package_id(self):
        v = Version(str(self.info.settings.compiler.version))
        if self.info.settings.compiler == "gcc" and (v >= "4.5" and v < "5.0"):
            # The assigned string can be arbitrary
            self.info.settings.compiler.version = "GCC 4 between 4.5 and 5.0"

This will result in all other compilers rather than ``gcc`` and other versions outside of that range to have a different ``package_id``, but there will be only 1 ``package_id`` binary for all ``gcc`` ``4.5-5.0`` versions. This also has the disadvantage mentioned above about losing the information that created this binary.

This approach is not recommended in the general case, and it would be better approached with the global ``compatibility`` plugin or the recipe ``compatibility()`` method.



Adding information
------------------

There is some information not added by default to the ``package_id``. 
If we are creating a package for a tool, to be used as a ``tool_require``, and it happens that such package binary will be different for each "target" configuration, like it is the case for some cross-compilers, if the compiler itself might be different for the different architectures that it is targeting, it will be necessary to add the ``settings_target`` to the ``package_id`` with:

.. code-block:: python

    def package_id(self):
        self.info.settings_target = self.settings_target

The ``conf`` items do not affect the ``package_id`` by default. It is possible to explicitly make them part of it at the recipe level with:

.. code-block:: python

    def package_id(self):
        self.info.conf.define("user.myconf:myitem", self.conf.get("user.myconf:myitem"))

Although this can be achieved for all recipes without the ``package_id()`` method, using the ``tools.info.package_id:confs = ["user.myconf:myitem"]`` configuration.

**Using regex patterns:** 
You can use regex patterns in the `tools.info.package_id:confs`. This means that instead
of specifying each individual configuration item, you can use a regex pattern to match
multiple configurations. This is particularly useful when dealing with a large number of
configurations or when configurations follow a predictable naming pattern. For instance:

- ``tools.info.package_id:confs=[".*"]`` matches all configurations.
- ``tools.info.package_id:confs=["tools\..*"]`` matches configurations starting with "tools.".
- ``tools.info.package_id:confs=["(tools\.deploy|core)"]`` matches configurations starting with "tools.deploy" or "core".

.. seealso::
    
    - See :ref:`the tutorial about header-only packages<creating_packages_other_header_only>` for explanations about the ``package_id()`` method.
    - Read the :ref:`binary model reference<reference_binary_model>` for a full view of the Conan binary model.
