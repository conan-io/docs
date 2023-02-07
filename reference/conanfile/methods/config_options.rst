.. _reference_conanfile_methods_config_options:

config_options()
================

The ``config_options()`` method
is used to configure or constraint the available options in a package, **before** they are given a value. A typical use case is to remove an option in a given platform. For example,
the ``fPIC`` flag doesn't exist in Windows, so it should be removed in this method like so:

.. code-block:: python

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

The ``config_options()`` method executes before the ``configure()`` method, and before the actual assignment of the ``options`` values, but after settings are already defined.

.. seealso::

    - Follow the :ref:`tutorial about recipe configuration methods<tutorial_creating_configure>`.
