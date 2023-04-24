
.. _pkg_config_generator:

pkg_config
==========

.. warning::

    This is a **deprecated** feature. Please refer to the :ref:`Migration Guidelines<conan2_migration_guide>`
    to find the feature that replaced this one.

Generates pkg-config files named *<PKG-NAME>.pc* (where ``<PKG-NAME`` is the name declared by dependencies in
``cpp_info.names["pkg_config"]`` if specified), containing a
valid pkg-config file syntax. The ``prefix`` variable is automatically adjusted to the ``package_folder``.

Components
++++++++++

Available since: `1.28.0 <https://github.com/conan-io/conan/releases/tag/1.28.0>`_

If a recipe uses :ref:`components<package_information_components>`, the files generated will be *<COMP-NAME>.pc* with their corresponding
flags and require relations.

Additionally, a *<PKG-NAME>.pc* is generated to maintain compatibility for consumers with recipes that start supporting components. This
*<PKG-NAME>.pc* file will declare all the components of the package as requires while the rest of the fields will be empty, relying on
the propagation of flags coming from the components *<COMP-NAME>.pc* files.

Go to :ref:`Integrations/pkg-config and pc files/Use the pkg_config generator<pkg_config_generator_example>`
if you want to learn how to use this generator.


Properties
++++++++++

The following properties affect the ``pkg_config`` generator:

- **pkg_config_name** property equivalent to the ``names`` attribute.
- **pkg_config_custom_content** property will add user defined content to the *.pc* files created by this generator.
- **component_version** property sets a custom version to be used in the ``Version`` field belonging to the created ``*.pc`` file for that component.
