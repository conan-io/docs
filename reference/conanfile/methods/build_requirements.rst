.. _reference_conanfile_methods_build_requirements:

build_requirements()
====================

The ``build_requirements()`` method is functionally equivalent to the ``requirements()`` one, it is executed just after it. It is not strictly necessary, in theory everything that is inside this method, could be done in the end of the ``requirements()`` one. Still, ``build_requirements()`` is good for having a dedicated place to define ``tool_requires`` and ``test_requires``:

.. code-block:: python

    def build_requirements(self):
       self.tool_requires("cmake/3.23.5")
       self.test_requires("gtest/1.13.0")


For simple cases the attribute syntax can be enough, like ``tool_requires = "cmake/3.23.5"`` and ``test_requires = "gtest/1.13.0"``. The method form can be necessary for conditional or parameterized requirements.

The ``tool_requires`` and ``test_requires`` methods are just a specialized instance of ``requires`` with some predefined trait values. See the :ref:`requires() reference<reference_conanfile_methods_requirements>` for more information about traits.

.. _reference_conanfile_methods_build_requirements_tool_requires:

tool_requires()
---------------

The ``tool_requires`` is equivalent to ``requires()`` with the following traits:

- ``build=True``. This dependency is in the "build" context, being necessary at build time, but not at application runtime, and will receive the "build" profile and configuration.
- ``visible=False``. The dependency to a tool requirement is not propagated downstream. For example, one package can call ``tool_requires("cmake/3.23.5")``, but that doesn't mean that the consumer packages also use ``cmake``, they could even use a different build system, or a different version, without causing conflicts.
- ``run=True``. This dependency has some executables or runtime that needs to be ran at build time.
- ``headers=False`` A tool requirement does not have headers.
- ``libs=False``: A tool requirement does not have libraries to be linked by the consumer (if it had libraries they would be in the "build" context and could be incompatible with the "host" context of the consumer package). 


Recall that ``tool_requires`` are intended exclusively for depending on tools like ``cmake`` or ``ninja``, which run in the "build" context, but not for library-like dependencies that would be linked into binaries. For libraries or library-like dependencies, use ``requires`` or ``test_requires``.


.. _reference_conanfile_build_requirements_host_version:

<host_version>
**************

.. include:: ../../../common/experimental_warning.inc

This syntax is useful when you're using the same package recipe as a *requires* and as a *tool_requires* and you want to avoid
conflicting downstream if any user decides to override the original *requires* version in the *host* context, i.e., the user could end up with
two different versions in the host and build contexts of the same dependency.

In a nutshell, the ``<host_version>`` specifier allows us to ensure that the version resolved for the *tool_requires*
always matches the one for the host requirement.

For instance, let's show a simple recipe using *protobuf*:

.. code-block:: python

    from conan import ConanFile

    class mylibRecipe(ConanFile):
        name = "mylib"
        version = "0.1"
        def requirements(self):
            self.requires("protobuf/3.18.1")
        def build_requirements(self):
            self.tool_requires("protobuf/<host_version>")

Then, if any user wants to use *mylib/0.1*, but another version of *protobuf*, there shouldn't be any problems overriding it:

.. code-block:: python

    from conan import ConanFile

    class myappRecipe(ConanFile):
        name = "myapp"
        version = "0.1"
        def requirements(self):
            self.requires("mylib/0.1")
            self.requires("protobuf/3.21.9", override=True)

The ``<host_version>`` defined upstream is ensuring that the host and build contexts are using the same version of that requirement.

Additionally, the syntax ``<host_version:mylib>`` can be used to specify the name of the package to be tracked,
should the *requires* and *tool_requires* have different names. For instance:

.. code-block:: python

    from conan import ConanFile

    class mylibRecipe(ConanFile):
        name = "mylib"
        version = "0.1"
        def requirements(self):
            self.requires("gettext/2.31")
        def build_requirements(self):
            self.tool_requires("libgettext/<host_version:gettext>")


.. seealso::

    - :ref:`examples_graph_tool_requires_protobuf`

.. _reference_conanfile_methods_build_requirements_test_requires:

test_requires
-------------

The ``test_requires`` is equivalent to ``requires()`` with the following traits:

- ``test=True``. This dependency is a "test" dependency, existing in the "host" context, but not aiming to be part of the final product.
- ``visible=False``. The dependency to a test requirement is not propagated downstream. For example, one package can call ``self.test_requires("gtest/1.13.0")``, but that doesn't mean that the consumer packages also use ``gtest``, they could even use a different test framework, or the same ``gtest`` with a different version, without causing conflicts.


It is possible to further modify individual traits of ``tool_requires()`` and ``test_requires()`` if necessary, for example:

.. code-block:: python

    def build_requirements(self):
       self.tool_requires("cmake/3.23.5", options={"shared": False})


The ``test_requires()`` allows the ``force=True`` trait in case there are transitive test requirements with conflicting versions, and likewise ``tool_requires()`` support the ``override=True`` trait, for overriding possible transitive dependencies of the direct tool requirements.

.. note::

    **Best practices**

    - ``tool_requires`` are exclusively for build time **tools**, not for libraries that would be included and linked into the consumer package. For libraries with some special characteristics, use a ``requires()`` with custom trait values.
    - The ``self.test_requires()`` and ``self.tool_requires()`` methods should exclusively be used in the ``build_requirements()`` method, with the only possible exception being the ``requirements()`` method. Using them in any other method is forbidden. To access information about dependencies when necessary in some methods, the :ref:`self.dependencies<conan_conanfile_model_dependencies>` attribute should be used.


.. seealso::

    - Follow the :ref:`tutorial about consuming Conan packages as tools<consuming_packages_tool_requires>`.
    - Read the :ref:`tutorial about creating tool_requires packages<tutorial_other_tool_requires_packages>`.
    - :ref:`examples_graph_tool_requires_protobuf`
