.. _reference_conanfile_methods_requirements:

requirements()
==============

The ``requirements()`` method is used to specify the dependencies of a package.

.. code-block:: python

    def requirements(self):
        self.requires("zlib/1.2.11")


For simple cases the attribute syntax can be used, like ``requires = "zlib/1.2.11"``.


Requirement traits
^^^^^^^^^^^^^^^^^^

Traits are properties of a requires clause. They determine how various parts of a
dependency are treated and propagated by Conan. Values for traits are usually computed by
Conan based on the dependency's :ref:`reference_conanfile_attributes_package_type`, but can
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

.. warning::

  Build time requirements (``tool_requires``, ``build_requires``) that define ``build=True`` are designed to
  work with their default ``visible=False``, and at the moment it is very strongly recommended to 
  keep them as ``visible=False``. If you think you might have a use case, it would be better to discuss first
  in https://github.com/conan-io/conan/issues and ask about it than trying to enable ``visible=True``.
 
  For some very exceptional cases, there is **experimental** support for build/tool requires with ``build=True``
  that also define ``visible=True``, but experimental and subject to possible breaking changes in future Conan
  versions. It is also known and designed to not propagate all traits, for example ``headers/libs`` will not be 
  propagated, because headers and libs from the "build" context cannot be linked in the host context.

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

.. _reference_conanfile_methods_requirements_package_id_mode:

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
existing conflicts. The downstream consumer's ``force`` traits always have higher priority.

override
~~~~~~~~

The same as the ``force`` trait, but not adding a ``direct`` dependency. If there is no
transitive dependency to override, this ``require`` will be discarded. This trait only
exists at the time of defining a ``requires``, but it will not exist as an actual
``requires`` once the graph is fully evaluated

.. note::

    **Best practices**

    The ``force`` and ``override`` traits to solve conflicts are not recommended as a general versioning
    solution, just as a temporary workaround to solve a version conflict. Its usage should be avoided
    whenever possible, and updating versions or version ranges in the graph to avoid the conflicts without
    overrides and forces is the recommended approach.

direct
~~~~~~

If the dependency is a direct one, that is, it has explicitly been declared by the current
recipe, or if it is a transitive one.

options
~~~~~~~

It is possible to define options values for dependencies as a trait:

.. code-block:: python

    self.requires("mydep/0.1", options={"dep_option": "value"})


.. warning::

    Defining options values in recipes does not have strong guarantees, please check 
    :ref:`this FAQ about options values for dependencies<faq_different_options_values>`. The recommended way
    to define options values is in profile files.


.. _reference_conanfile_package_type_trait_inferring:

package_type trait inferring
============================

Some traits are automatically inferred based on the value of the ``package_type`` if not explicitly set by the recipe.

 * ``application``: ``headers=False``, ``libs=False``, ``run=True``
 * ``shared-library``: ``run=True``
 * ``static-library``: ``run=False``
 * ``header-library``: ``headers=True``, ``libs=False``, ``run=False``
 * ``build-scripts``: ``headers=False``, ``libs=False``, ``run=True``, ``visible=False``

Additionally, some additional traits are inferred on top of the above mentioned based on the ``package_type`` of the dependant:

 * ``header-library``: ``transitive_headers=True``, ``transitive_libs=True``

Default traits for each kind of requires
========================================

Each kind of requires sets some additional traits by default on top of the ones stated in the last section. Those are:

 * ``requires``: ``build=False``
 * ``build_requires``:  ``headers=False``, ``libs=False``, ``build=True``, ``visible=False``
 * ``tool_requires``: ``headers=False``, ``libs=False``, ``build=True``, ``run=True``, ``visible=False``
 * ``test_requires``: ``headers=True``, ``libs=True``, ``build=False``, ``visible=False``, ``test=True``
