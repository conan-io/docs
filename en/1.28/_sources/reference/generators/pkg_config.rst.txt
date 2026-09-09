
.. _pkg_config_generator:

pkg_config
==========

Generates pkg-config files named *<PKG-NAME>.pc* (where ``<PKG-NAME`` is the name declared by dependencies in 
``cpp_info.name`` or in ``cpp_info.names["pkg_config"]`` if specified), containing a
valid pkg-config file syntax. The ``prefix`` variable is automatically adjusted to the ``package_folder``.

Components
++++++++++

If a recipe uses :ref:`components<package_information_components>`, the files generated will be *<COMP-NAME>.pc* with their corresponding
flags and require relations.

Additionally, a *<PKG-NAME>.pc* is generated to maintain compatibility for consumers with recipes that start supporting components. This
*<PKG-NAME>.pc* file will declare the all the components of the package as requires while the rest of the fields will be empty, relying on
the propagation of flags coming from the components *<COMP-NAME>.pc* files.

Go to :ref:`Integrations/pkg-config and pc files/Use the pkg_config generator<pkg_config_generator_example>`
if you want to learn how to use this generator.
