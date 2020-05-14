
.. _pkg_config_generator:

pkg_config
==========

Generates N files named ``<PKG-NAME>.pc`` (where ``<PKG-NAME`` is the name declared by dependencies in 
``cpp_info.name`` or in ``cpp_info.names["pkg_config"]`` if specified), containing a
valid pkg-config file syntax. The ``prefix`` variable is automatically adjusted to the ``package_folder``.

Go to :ref:`Integrations/pkg-config and pc files/Use the pkg_config generator<pkg_config_generator_example>`
if you want to learn how to use this generator.


