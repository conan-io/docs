.. _reference_conanfile_methods_requirements:

requirements()
==============

The ``requirements()`` method is used to specify the dependencies of a package.

.. code-block:: python

    def requirements(self):
        self.requires("zlib/1.3.1")


For simple cases the attribute syntax can be used, like ``requires = "zlib/1.3.1"``.


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

.. warning::

    The ``visible`` trait can create conflicts if a transitive dependency has a ``visible=True``
    requirement to the same package that the current recipe is declaring as ``visible=False``.
    In these cases where different visibility rules reach the same package, the visible transitive
    dependency will be used and propagated downstream.


transitive_headers
~~~~~~~~~~~~~~~~~~

If ``True`` the headers of the dependency will be visible downstream. 
Read more about this trait in the :ref:`tutorial for headers transitivity<tutorial_create_packages_headers_transitivity>`.

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

The same as the ``force`` trait, but not adding a ``direct`` dependency. **If there is no
transitive dependency to override, this ``require`` will be discarded**. This trait only
exists at the time of defining a ``requires``, but it will not exist as an actual
``requires`` once the graph is fully evaluated

.. note::

    **Best practices**

    - The ``force`` and ``override`` traits to solve conflicts are not recommended as a general versioning
      solution, just as a temporary workaround to solve a version conflict. Its usage should be avoided
      whenever possible, and updating versions or version ranges in the graph to avoid the conflicts without
      overrides and forces is the recommended approach.
    - A key takeaway is that the ``override`` trait does not create a direct dependency from your package, while
      the ``force`` trait does. This means that the ``override`` trait is only useful when you want to override
      the version of one of your transitive dependencies, while not adding a direct dependency to it.

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


no_skip
~~~~~~~

This trait is an **experimental** feature introduced in Conan 2.16, and subject to breaking changes.
See :ref:`the Conan stability<stability>` section for more information.

Conan is able to avoid the download of the package binaries of the transitive dependencies when they are not needed.
For example if a ``package_type = "application"`` package that contains an executable depends (``requires``) another package
that is a ``package_type = "static-library"`` (or a regular library, but with option ``shared=False``), then, installing the
application package binary doesn't require the binaries of the static libraries dependencies to work. Conan will then "skip"
the download of those binaries, saving the time and transfer cost of such download and installation. These binaries are 
marked as "Skipped binaries" in the Conan commands output.

The ``tools.graph:skip_binaries`` conf can change the default behavior and if ``False`` it will avoid skipping binaries, which 
can be useful in some scenarios. 

The ``no_skip=True`` trait can be defined in a dependency like:

.. code-block:: python

  name = "mypkg"

  def requirements(self):
    self.requires("mydep/0.1", no_skip=True)

And that will force the download of the binary for ``mydep/0.1`` when the binary for ``mypkg`` is necessary.

.. note::

  **Best practices**

  The usage of ``no_skip=True`` should be exceptional, for very limited and extraordinary use cases, the default Conan 
  "skipping binaries" behavior should be good for the vast majority of cases. Typically, it wouldn't make sense in isolation,
  but if used jointly with other traits such as ``visible=False``. Avoid using it except when absolutely
  necessary, and it should only be used in very particular recipes. If used in many recipes, it is most likely an abuse.



.. _reference_conanfile_package_type_trait_inferring:

package_type trait inferring
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some traits are automatically inferred based on the value of the ``package_type`` of the dependency
if not explicitly set by the recipe.

.. note::

    The ``libs``, ``headers`` and ``visible`` traits are set to ``True`` by default
    unless otherwise stated in the lists shown below, or if they are manually set by the user to ``False``.

The inferring rules are:

 * ``application``: ``headers=False``, ``libs=False``, ``run=True``
 * ``shared-library``: ``run=True``
 * ``static-library``: ``run=False``
 * ``header-library``: ``headers=True``, ``libs=False``, ``run=False``
 * ``build-scripts``: ``headers=False``, ``libs=False``, ``run=True``, ``visible=False``

This means that if in your recipe you have ``self.requires("mypkg/1.0")``, and ``mypkg/1.0`` has
``package_type="application"``, then the effective traits for that ``requires`` will be
``headers=False``, ``libs=False``, ``run=True``. These can then be overridden by explicitly
setting them in the ``requires``.

Additionally, some additional traits are inferred on top of the above mentioned choices,
based on the ``package_type`` of your recipe:

 * ``header-library``: ``transitive_headers=True``, ``transitive_libs=True``

This means that if your package is a ``header-library``, then all its requirements
will have ``transitive_headers=True`` and ``transitive_libs=True`` by default.

Default traits for each kind of requires
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each kind of requires sets some additional traits by default on top of the ones stated in the last section. Those are:

 * ``requires``: ``build=False``
 * ``build_requires``:  ``headers=False``, ``libs=False``, ``build=True``, ``visible=False``
 * ``tool_requires``: ``headers=False``, ``libs=False``, ``build=True``, ``run=True``, ``visible=False``
 * ``test_requires``: ``headers=True``, ``libs=True``, ``build=False``, ``visible=False``, ``test=True``

For example, taking all the logic shown into account, this means that if in your library
that has ``package_type="header-library"`` you have a requirement of the form
``self.requires("mypkg/1.0")`` and ``mypkg/1.0`` has ``package_type="shared-library"``,
the effective traits for that ``requires`` will be:

 * Inferred from ``mypkg``'s ``package_type``: ``run=True``
 * Inferred from your package's ``package_type``: ``transitive_headers=True``, ``transitive_libs=True``
 * By the ``requires`` kind: ``build=False``
 * By default: ``headers=True``, ``libs=True``
