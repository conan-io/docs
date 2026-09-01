Command API
===========

.. include:: ../../../common/experimental_warning.inc

.. include:: ../../../common/subapi_instantiation_warning.inc

.. currentmodule:: conan.api.subapi.command

.. autoclass:: CommandAPI
    :members:


.. note::

   When consuming this sub-API from a standalone script where the ``ConanAPI`` class is instantiated manually
   (which is not the recommended way to use the Python API, and :ref:`custom commands<reference_commands_custom_commands>` should be preferred),
   an extra step is required, because the ``ConanAPI`` class does not automatically set the CLI interface needed for this sub-API to work properly.
   In that case, the following code snippet should be used:

   .. code-block:: python
      :emphasize-lines: 2, 5, 6

      from conan.api.conan_api import ConanAPI
      from conan.cli.cli import Cli

      api = ConanAPI()
      cli = Cli(api)
      cli.add_commands()
      result = api.command.run(["remote", "list"])


   The ``Cli`` class should be treated as a private opaque object, and its usage limited to the above snippet.
