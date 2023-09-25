.. _reference_binary_model_dependencies:

The effect of dependencies on ``package_id``
============================================

The effect of dependencies:

- embed vs non-embed mode


Default package_id modes
------------------------
core.package_id:default_build_mode: By default, 'None'
core.package_id:default_embed_mode: By default, 'full_mode'
core.package_id:default_non_embed_mode: By default, 'minor_mode'
core.package_id:default_python_mode: By default, 'minor_mode'
core.package_id:default_unknown_mode: By default, 'semver_mode'



<reference_conanfile_attributes_package_id_modes>

Default package recipe modes
----------------------------

package_id_{embed,non_embed,unknown}_mode

The ``package_id_embed_mode, package_id_non_embed_mode, package_id_unknown_mode`` are class attributes that can be defined in recipes to define the effect they have on their consumers ``package_id``. Can be declared as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0.0"
        package_id_embed_mode = "full_mode"
        package_id_non_embed_mode = "patch_mode"
        package_id_unknown_mode = "minor_mode"