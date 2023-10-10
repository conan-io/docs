Customizing the binary compatibility
====================================

The default binary compatibility requires an almost exact match of settings and options, and a versioned match
of dependencies versions, as explained in the :ref:`previous section about dependencies<reference_binary_model_dependencies>`.

In summary, the required binaries ``package_id`` when installing dependencies should match by default:

- All the settings in the ``package_id`` except ``compiler.cppstd`` should match exactly the ones provided in the input profiles, including the compiler version. So ``compiler.version=9`` is different than ``compiler.version=9.1``.
- The default behavior will assume binary compatibility among different ``compiler.cppstd`` values for C++ packages, being able to fall back to other values rather than the one specified in the input profiles, if the ``cppstd`` required by the input profile does not exist. This is controlled by the ``compatibility.py`` plugin, that can be customized by users.
- All the options in the ``package_id`` should match exactly the ones provided in the input profiles.
- The versions of the dependencies should match:

  - In case of "embedding dependencies", should match the exact version, including the recipe-revision and the dependency ``package_id``. The ``package_revision`` is never included as it is assumed to be ill-formed to have more than one ``package_revision`` for the same ``package_id``.
  - In case of "non-embedding dependencies", the versions of the dependencies should match down to the ``minor`` version, being the ``patch``, ``recipe_revision`` and further information not taken into account.
  - In case of "tool dependencies", the versions of the dependencies do not affect at all by default to the consumer ``package_id``.


These rules can be customized and changed using different approaches, depending on the needs, as explained in following sections

Customizing binary compatibility of settings and options
--------------------------------------------------------

Information erasure in package_id() method
++++++++++++++++++++++++++++++++++++++++++

Recipes can **erase** information from their ``package_id`` using their ``package_id()`` method. For example, a package containing only an executable can decide to remove the information from ``settings.compiler`` and ``settings.build_type`` from their ``package_id``, assuming that an executable built with any compiler will be valid, and that it is not necessary to store different binaries built with different compilers:

.. code-block:: python

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

It is also possible to assign a value for a given setting, for example if we want to have one single binary for all gcc versions included in the [>=5 <7>] range, we could do:

.. code-block:: python

    def package_id(self):
        if self.info.settings.compiler == "gcc":
            version = Version(self.info.settings.compiler.version)
            if version >= "5.0" and version < "7.0":
                self.info.settings.compiler.version = "gcc5-6"


.. note::

    **Best practice**

    Note that information erasure in ``package_id()`` means that 1 single ``package_id`` will represent a whole range of different settings, but the information of what exact setting was used to create the binary will be lost, and only 1 binary can be created for that range. Re-creating the package with different settings in the range, will create a new binary that overwrites the previous one (with a new package-revision).

    If we want to be able to create, store and manage different binaries for different input settings, information erasure can't be used, and using the below ``compatibility`` approaches is recommended.

Read more about ``package_id()`` in:

- :ref:`creating_packages_configure_options_settings`
- :ref:`package_id() method reference<reference_conanfile_methods_package_id>`


The compatibility() method
++++++++++++++++++++++++++

Recipes can define their binary compatibility rules, using their ``compatibility()`` method.
For example, if we want that binaries
built with gcc versions 4.8, 4.7 and 4.6 to be considered compatible with the ones compiled
with 4.9 we could declare a ``compatibility()`` method like this:

..  code-block:: python

    def compatibility(self):
        if self.settings.compiler == "gcc" and self.settings.compiler.version == "4.9":
            return [{"settings": [("compiler.version", v)]}
                    for v in ("4.8", "4.7", "4.6")]
                

Read more about the ``compatibility()`` method in :ref:`the compatibility() method reference<reference_conanfile_methods_compatibility>`


The ``compatibility.py`` plugin
+++++++++++++++++++++++++++++++

Compatibility can be defined globally via the ``compatibility.py`` plugin, in the same way that the ``compatibility()`` method does for one recipe, but for all packages globally.

Check the binary compatibility :ref:`compatibility.py extension <reference_extensions_binary_compatibility>`.



Customizing binary compatibility of dependencies versions
---------------------------------------------------------

Global default package_id modes
+++++++++++++++++++++++++++++++

The ``core.package_id:default_xxx`` configurations defined in ``global.conf`` can be used to globally change the defaults of how dependencies affect their consumers

.. code-block:: ini

    core.package_id:default_build_mode: By default, 'None'
    core.package_id:default_embed_mode: By default, 'full_mode'
    core.package_id:default_non_embed_mode: By default, 'minor_mode'
    core.package_id:default_python_mode: By default, 'minor_mode'
    core.package_id:default_unknown_mode: By default, 'semver_mode'

.. note::

    **Best practices**

    It is strongly recommended that the ``core.package_id:default_xxx`` should be global, consistent and immutable accross organizations. It can be confusing to change these defaults for different projects or teams, because it will result in missing binaries.

    It should also be consistent and shared with the consumers of generated packages if those packages are
    shared outside the organization, in that case sharing the ``global.conf`` file via ``conan config install``
    could be recommended.

    Consider using the Conan defaults, they should be a good balance between efficiency and safety, ensuring exact re-building for embed cases, and good control via versions for non-embed cases.


Custom package_id modes for recipe consumers
++++++++++++++++++++++++++++++++++++++++++++

Recipes can define their default effect to their consumers, via some ``package_id_xxxx_mode`` attributes.

The ``package_id_embed_mode, package_id_non_embed_mode, package_id_unknown_mode`` are class attributes that can be defined in recipes to define the effect they have on their consumers ``package_id``. Can be declared as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        ...
        package_id_embed_mode = "full_mode"
        package_id_non_embed_mode = "patch_mode"
        package_id_unknown_mode = "minor_mode"


Read more in :ref:`reference_conanfile_attributes_package_id_modes`

Custom package_id from recipe dependencies
++++++++++++++++++++++++++++++++++++++++++

Recipes can define how their dependencies affect their ``package_id``, using the ``package_id_mode`` trait:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        def requirements(self):
            self.requires("mydep/1.0", package_id_mode="patch_mode")


Using ``package_id_mode`` trait does not differentiate between the "embed" and "non-embed" cases, it is up to the user to define the correct value. It is likely that this approach should only be used for very special cases that do not have variability of shared/static libraries controlled via ``options``.

Note that the ``requirements()`` method is evaluated while the graph is being expanded, the dependencies do not exist yet (haven't been computed), so it is not possible to know the dependencies options.
In this case it might be preferred to use the ``package_id()`` method.

The ``package_id()`` method can define how the dependencies affect the current package with:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        def package_id(self):
            self.info.requires["mydep"].major_mode()

The different modes that can be used are defined in :ref:`reference_conanfile_attributes_package_id_modes`
