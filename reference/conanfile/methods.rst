.. spelling::

  ing
  ver

.. _conan_conanfile_methods:

Methods
=======


requirements()
--------------

Requirement traits
^^^^^^^^^^^^^^^^^^

Traits are properties of a requires clause. They determine how various parts of a
dependency are treated and propagated by Conan. Values for traits are usually computed by
Conan based on dependency's :ref:`reference_conanfile_attributes_package_type`, but can
also be specified manually.

A good introduction to traits is provided in the `Advanced Dependencies Model in Conan 2.0
<https://youtu.be/kKGglzm5ous>`_ presentation.

In the example below ``headers`` and ``libs`` are traits.

.. code-block:: python

       self.requires("math/1.0", headers=True, libs=True)


headers
~~~~~~~

Indicates that there are headers that are going to be ``#included`` from this package at
compile time. The dependency will be in the host context.

libs
~~~~

The dependency contains some library or artifact that will be used at link time of the
consumer. This trait will typically be ``True`` for direct shared and static libraries,
but could be false for indirect static libraries that are consumed via a shared library.
The dependency will be in the host context.

build
~~~~~

This dependency is a build tool, an application or executable, like cmake, that is used
exclusively at build time. It is not linked/embedded into binaries, and will be in the
build context.

run
~~~

This dependency contains some executables, either apps or shared libraries that need to be
available to execute (typically in the path, or other system env-vars). This trait can be
``True`` for ``build=False``, in that case, the package will contain some executables that
can run in the host system when installing it, typically like an end-user application.
This trait can be ``True`` for ``build=True``, the package will contain executables that
will run in the build context, typically while being used to build other packages.

visible
~~~~~~~

This ``require`` will be propagated downstream, even if it doesn't propagate ``headers``,
``libs`` or ``run`` traits. Requirements that propagate downstream can cause version
conflicts. This is typically ``True``, because in most cases, having 2 different versions of
the same library in the same dependency graph is at least complicated, if not directly
violating ODR or causing linking errors. It can be set to ``False`` in advanced scenarios,
when we want to use different versions of the same package during the build.

transitive_headers
~~~~~~~~~~~~~~~~~~

If ``True`` the headers of the dependency will be visible downstream.

transitive_libs
~~~~~~~~~~~~~~~

If ``True`` the libraries to link with of the dependency will be visible downstream.

test
~~~~

This requirement is a test library or framework, like Catch2 or gtest. It is mostly a
library that needs to be included and linked, but that will not be propagated downstream.

package_id_mode
~~~~~~~~~~~~~~~

If the recipe wants to specify how the dependency version affects the current package
``package_id``, can be directly specified here.

While it could be also done in the ``package_id()`` method, it seems simpler to be able to
specify it in the ``requires`` while avoiding some ambiguities.

.. code-block:: python

    # We set the package_id_mode so it is part of the package_id
    self.tool_requires("tool/1.1.1", package_id_mode="minor_mode")

Which would be equivalent to:

.. code-block:: python

    def package_id(self):
      self.info.requires["tool"].minor_mode()

force
~~~~~

This ``requires`` will force its version in the dependency graph upstream, overriding
other existing versions even of transitive dependencies, and also solving potential
existing conflicts.

override
~~~~~~~~

The same as the ``force`` trait, but not adding a ``direct`` dependency. If there is no
transitive dependency to override, this ``require`` will be discarded. This trait only
exists at the time of defining a ``requires``, but it will not exist as an actual
``requires`` once the graph is fully evaluated

direct
~~~~~~

If the dependency is a direct one, that is, it has explicitly been declared by the current
recipe, or if it is a transitive one.


validate_build()
----------------

The ``validate_build()`` method is used to verify if a configuration is valid for building a package. It is different
from the ``validate()`` method that checks if the binary package is "impossible" or invalid for a given configuration.

The ``validate()`` method should do the checks of the settings and options using the ``self.info.settings``
and ``self.info.options``.

The ``validate_build()`` method has to use always the ``self.settings`` and ``self.options``:

.. code-block:: python

    from conan import ConanFile
    from conan.errors import ConanInvalidConfiguration
    class myConan(ConanFile):
        name = "foo"
        version = "1.0"
        settings = "os", "arch", "compiler"
        def package_id(self):
            # For this package, it doesn't matter the compiler used for the binary package
            del self.info.settings.compiler
        def validate_build(self):
            # But we know this cannot be build with "gcc"
            if self.settings.compiler == "gcc":
                raise ConanInvalidConfiguration("This doesn't build in GCC")
        def validate(self):
            # We shouldn't check here the self.info.settings.compiler because it has been removed in the package_id()
            # so it doesn't make sense to check if the binary is compatible with gcc because the compiler doesn't matter
            pass

.. _conanfile_methods_layout:

layout()
--------

Read about the Conan package layout :ref:`here<conanfile_conan_package_layout>`.

In the layout() method you can adjust ``self.folders`` and ``self.cpp``.


.. _layout_folders_reference:


self.folders
^^^^^^^^^^^^

- **self.folders.source** (Defaulted to ""): Specifies a subfolder where the sources are.
  The ``self.source_folder`` attribute inside the ``source(self)`` and ``build(self)``
  methods will be set with this subfolder. The *current working directory* in the
  ``source(self)`` method will include this subfolder. The `export_sources`, `exports` and
  `scm` sources will also be copied to the root source directory. It is used in the cache
  when running :command:`conan create` (relative to the cache source folder) as well as in
  a local folder when running :command:`conan build` (relative to the local current
  folder).

- **self.folders.build** (Defaulted to ""): Specifies a subfolder where the files from the
  build are. The ``self.build_folder`` attribute and the *current working directory*
  inside the ``build(self)`` method will be set with this subfolder. It is used in the
  cache when running :command:`conan create` (relative to the cache source folder) as well
  as in a local folder when running :command:`conan build` (relative to the local current
  folder).

- **self.folders.generators** (Defaulted to ""): Specifies a subfolder where to write the
  files from the generators and the toolchains. In the cache, when running the
  :command:`conan create`, this subfolder will be relative to the root build folder and
  when running the :command:`conan install` command it will be relative to the current
  working directory.

- **self.folders.imports** (Defaulted to ""): Specifies a subfolder where to write the
  files copied when using the ``imports(self)`` method in a ``conanfile.py``. In the
  cache, when running the :command:`conan create`, this subfolder will be relative to the
  root build folder and when running the :command:`conan imports` command it will be
  relative to the current working directory.

- **self.folders.root** (Defaulted to None): Specifies a parent directory where the
  sources, generators, etc., are located specifically when the ``conanfile.py`` is located
  in a separated subdirectory.

- **self.folders.subproject** (Defaulted to None): Specifies a subfolder where the
  ``conanfile.py`` is relative to the project root. This is particularly useful for
  :ref:`layouts with multiple subprojects<package_layout_example_multiple_subprojects>`


self.cpp
^^^^^^^^

The ``layout()`` method allows to declare ``cpp_info`` objects not only for the final
package (like the classic approach with the ``self.cpp_info`` in the
``package_info(self)`` method) but for the ``self.source_folder`` and
``self.build_folder``.

The fields of the cpp_info objects at ``self.cpp.build`` and ``self.cpp.source`` are the
same described :ref:`here<conan_conanfile_model_cppinfo>`. Components are also supported.
