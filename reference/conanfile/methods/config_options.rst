.. _reference_conanfile_methods_config_options:

config_options()
================

The ``config_options()`` method is used to configure or constrain the available options in a package **before** assigning them a value.
A typical use case is to remove an option in a given platform.
For example, the ``SSE2`` flag doesn't exist in architectures different than 32 bits, so it should be removed in this method like so:

.. code-block:: python

    def config_options(self):
        if self.settings.arch != "x86_64":
            del self.options.with_sse2

The ``config_options()`` method executes:
* Before calling the ``configure()`` method.
* Before assigning the ``options`` values.
* After ``settings`` are already defined.

Default behavior
++++++++++++++++

.. include:: ../../../common/experimental_warning.inc

When the ``config_options()`` method is not defined, Conan automatically manages some conventional options using
the :ref:`conan.tools.default_config_options()<conan_tools_default_config_options>` tool.

Options automatically managed:

- ``fPIC`` (True, False).

To opt-out from this behavior, the method can be empty-defined:

.. code-block:: python

    def config_options(self):
        pass

To manage extra options apart from the ones automatically handled, the tool has to be explicitly called:

.. code-block:: python

    from conan.tools import default_config_options

    def config_options(self):
        default_config_options(self)
        if self.settings.arch != "x86_64":
            del self.options.with_sse2

.. seealso::

    - Follow the :ref:`tutorial about recipe configuration methods<tutorial_creating_configure>`.
