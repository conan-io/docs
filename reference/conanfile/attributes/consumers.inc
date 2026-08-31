
Package information for consumers
+++++++++++++++++++++++++++++++++


cpp_info
--------

Same as using ``self.cpp.package`` in the ``layout()`` method. Use it if you need to read
the ``package_folder`` to locate the already located artifacts.

.. seealso::

    - :ref:`CppInfo<conan_conanfile_model_cppinfo>` model.


.. important::

    This attribute is only defined inside ``package_info()`` method being `None` elsewhere.


.. _conan_conanfile_attributes_buildenv_info:

buildenv_info
-------------

For the dependant recipes, the declared environment variables will be present during the
build process. Should be only filled in the ``package_info()`` method.


.. important::

    This attribute is only defined inside ``package_info()`` method being `None` elsewhere.

.. code-block:: python

    def package_info(self):
        self.buildenv_info.append_path("PATH", self.package_folder)


.. seealso::

    Check the reference of the :ref:`Environment<conan_tools_env_environment_model>` object to know how to fill
    the ``self.buildenv_info``.


.. _conan_conanfile_attributes_runenv_info:

runenv_info
-----------

For the dependant recipes, the declared environment variables will be present at runtime.
Should be only filled in the ``package_info()`` method.


.. important::

   This attribute is only defined inside ``package_info()`` method being `None` elsewhere.

.. code-block:: python

    def package_info(self):
        self.runenv_info.define_path("RUNTIME_VAR", "c:/path/to/exe")


.. seealso::

    Check the reference of the :ref:`Environment<conan_tools_env_environment_model>` object to know how to fill
    the ``self.runenv_info``.


.. _conan_conanfile_attributes_conf_info:

conf_info
---------

Configuration variables to be passed to the dependant recipes.
Should be only filled in the ``package_info()`` method.

.. code-block:: python

    class Pkg(ConanFile):
        name = "pkg"

        def package_info(self):
            self.conf_info.define("tools.build:verbosity", "debug")
            self.conf_info.get("tools.build:verbosity")  # == "debug"
            self.conf_info.append("user.myconf.build:ldflags", "--flag3")  # == ["--flag1", "--flag2", "--flag3"]
            self.conf_info.update("tools.microsoft.msbuildtoolchain:compile_options", {"ExpandAttributedSource": "false"})
            self.conf_info.unset("tools.microsoft.msbuildtoolchain:compile_options")
            self.conf_info.remove("user.myconf.build:ldflags", "--flag1")  # == ["--flag0", "--flag2", "--flag3"]
            self.conf_info.pop("tools.system.package_manager:sudo")

.. seealso::

      Read here :ref:`the complete reference of self.conf_info <conan_conanfile_model_conf_info>`.


generator_info
--------------

.. include:: ../../common/experimental_warning.inc

Generators to be passed to the dependant recipes.
Should be only filled in the ``package_info()`` method, ``None`` by default.

.. seealso::

      See :ref:`an example usage here <reference_commands_custom_generators_tool_requires>`
      and :ref:`the complete reference of self.generator_info <conan_conanfile_model_generator_info>`.

deprecated
----------

This attribute declares that the recipe is deprecated, causing a user-friendly warning
message to be emitted whenever it is used

For example, the following code:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "cpp-taskflow"
        version = "1.0"
        deprecated = True

may emit a ``risk`` warning like:

.. code-block:: bash

    Deprecated
        cpp-taskflow/1.0

    WARN: risk: There are deprecated packages in the graph


Optionally, the attribute may specify the name of the suggested replacement:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "cpp-taskflow"
        version = "1.0"
        deprecated = "Not secure, use better taskflow>1.2.3"

This will emit a ``risk`` warning like:

.. code-block:: bash

    Deprecated
        cpp-taskflow/1.0: Not secure, use better taskflow>1.2.3

    WARN: risk: There are deprecated packages in the graph

If the value of the attribute evaluates to ``False``, no warning is printed.


provides
--------

This attribute declares that the recipe provides the same functionality as other recipe(s).
The attribute is usually needed if two or more libraries implement the same API to prevent
link-time and run-time conflicts (ODR violations). One typical situation is forked libraries.
Some examples are:
    
- `LibreSSL <https://www.libressl.org/>`__, `BoringSSL <https://boringssl.googlesource.com/boringssl/>`__ and `OpenSSL <https://www.openssl.org/>`__
- `libav <https://en.wikipedia.org/wiki/Libav>`__ and `ffmpeg <https://ffmpeg.org/>`__
- `MariaDB client <https://downloads.mariadb.org/client-native>`__ and `MySQL client <https://dev.mysql.com/downloads/c-api/>`__
 


If Conan encounters two or more libraries providing the same functionality within a single graph, it raises an error:

.. code-block:: bash

    At least two recipes provides the same functionality:
    - 'libjpeg' provided by 'libjpeg/9d', 'libjpeg-turbo/2.0.5'

The attribute value should be a string with a recipe name or a tuple of such recipe names.

For example, to declare that ``libjpeg-turbo`` recipe offers the same functionality as ``libjpeg`` recipe, the following code could be used:

.. code-block:: python

    from conan import ConanFile

    class LibJpegTurbo(ConanFile):
        name = "libjpeg-turbo"
        version = "1.0"
        provides = "libjpeg"


To declare that a recipe provides the functionality of several different recipes at the same time, the following code could be used:

.. code-block:: python

    from conan import ConanFile

    class OpenBLAS(ConanFile):
        name = "openblas"
        version = "1.0"
        provides = "cblas", "lapack"

If the attribute is omitted, the value of the attribute is assumed to be equal to the current package name. Thus, it's redundant for
``libjpeg`` recipe to declare that it provides ``libjpeg``, it's already implicitly assumed by Conan.

.. _conan_conanfile_attributes_package_type_traits:

package_type_traits
-------------------

This attribute declares that the package has runtime artifacts that consumers should be aware of.
This is useful for ``package_type="static-library"`` recipes that nevertheless also contain shared libraries, or by  ``package_type="header-library"`` that have some kind of resource that library needs at runtime,
so that at runtime their folders are exposed to the consumers.

It is important to still declare the ``package_type`` that best describes the package for linkage and
``package_id`` purposes (see :ref:`the effect of dependencies on package_id<reference_binary_model_dependencies>`
and :ref:`package_type trait inferring<reference_conanfile_package_type_trait_inferring>`), and use
``package_type_traits`` only to fix the specific trait that ``package_type`` got wrong, instead of changing
the ``package_type`` itself. For example, a package that is fundamentally a static library, meant to be
embedded and to force a rebuild of its direct consumers like any other static library, should keep
``package_type = "static-library"``, even if it also happens to ship a shared library or some other resource
needed at runtime. Declaring it instead as ``package_type = "shared-library"`` would also change the
``package_id`` computation mode and the linkage information propagated to consumers, when the only thing
that actually needs fixing is the ``run`` trait.

By default, a ``static-library`` dependency gets the ``run`` requirement trait set to ``False`` (see
:ref:`package_type trait inferring<reference_conanfile_package_type_trait_inferring>`), so its binary can be
skipped when only linked transitively, and its folders are not added to the runtime environment by
generators like :ref:`VirtualRunEnv<conan_tools_env_virtualrunenv>`, nor collected by deployers like
:ref:`runtime_deploy<reference_extensions_deployer_runtime_deploy>`. Declaring ``package_type_traits = {"run": True}``
forces ``run=True`` for every consumer of the package, regardless of its ``package_type``:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "mypkg"
        version = "1.0"
        # This is a static library, but it also ships a shared library (e.g. a plugin) that
        # consumers need available at runtime
        package_type = "static-library"
        package_type_traits = {"run": True}

.. note::

    At the moment, ``run`` is the only key read from ``package_type_traits``, and ``True`` is the only
    value that has an effect. Setting any other trait or value currently does nothing, so it shouldn't be
    relied upon: unsupported keys are silently ignored today, but might be validated, or start having an
    effect, in future Conan versions.

.. seealso::

    - :ref:`The run requirement trait<reference_conanfile_methods_requirements>`.
    - :ref:`How package_type infers the run trait<reference_conanfile_package_type_trait_inferring>`.
