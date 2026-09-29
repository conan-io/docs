.. _reference_conanfile_methods_build_id:

build_id()
==========

The ``build_id()`` method allows to re-use the same build to create different binary packages in the cache,
potentially saving build time as it can avoid some unnecessary re-builds. It is therefore an optimization method.

In the general case, there is one build folder for each binary package, with the exact same ``package_id`` of the package. However this behavior
can be changed, there are a couple of scenarios that this might be useful:

- The package build scripts generate several different configurations at once (like both debug and release artifacts) in the same run, without the possibility of building each configuration separately.
- The package build scripts generate one binary configuration, but different artifacts that can be packaged separately. For example if there are some test executables, you might want to create two packages: one just containing the library for general usage, and another one also containing the tests (for compliance, later reproducibility, debugging, etc).

In the first case, we could for example write:

..  code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build_id(self):
        self.info_build.settings.build_type = "Any"

This recipe will generate a final different package with a different ``package_id`` for debug and release configurations. But as the ``build_id()`` will generate the
same ``build_id`` for any ``build_type``, then just one folder and one ``build()`` will be done, building both debug and release artifacts,
and then the ``package()`` method will be called for each configuration, and it should package the artifacts conditionally to the ``self.settings.build_type`` value. Different builds will still be
executed if using different compilers or architectures.

Other information like custom package options can also be changed:

..  code-block:: python

    def build_id(self):
        self.info_build.options.myoption = 'MyValue' # any value possible
        self.info_build.options.fullsource = 'Always'

If the ``build_id()`` method does not modify the ``info_build`` data, and it still produces a different id than
the ``package_id``, then the standard behavior will be applied. Consider the following:

..  code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build_id(self):
        if self.settings.os == "Windows":
            self.info_build.settings.build_type = "Any"

This will only produce a different ``build_id`` if the package is for Windows, thus running ``build()`` just
once for all ``build_type`` values. The behavior
in any other OS will be the standard one, as if the ``build_id()`` method was not defined, running
one different ``build()`` for each ``build_type``.


.. note::

    **Best practices**

    Conan strongly recommends to use one package binary with its own ``package_id`` for each different configuration. The goal of the ``build_id()`` method is to deal with legacy build scripts that cannot easily be changed to do the build of one configuration each time.
