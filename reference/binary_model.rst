.. _reference_binary_model:

The binary model
================

This section introduces first how the ``package_id``, the package binaries identifier is computed, hashing the configuration (settings + options + dependencies versions). While the effect of ``settings`` and ``options`` is more straightforward, understanding the effects of the dependencies requires more explanations, so that will be done in its own section.

Conan binary model is extensible, and users can define their custom settings, options and configuration to model their own binaries characteristics.

Finally, the default binary compatibility model will be described, and how it can be customized to adapt to different needs.


.. toctree::
    :maxdepth: 1

    binary_model/package_id
    binary_model/dependencies
    binary_model/extending
    binary_model/custom_compatibility
