.. _reference_extensions:

Extensions
----------

Conan can be extended in a few ways, with custom user code:

- ``python_requires`` allow to put common recipe code in a recipe package that can be reused
  by other recipes by declaring a ``python_requires = "mypythoncode/version"``
- ``hooks`` are "pre" and "post" recipe methods (like ``pre_build()`` and ``post_build()``) 
  extensions that can be used to complement recipes
  with orthogonal functionality, like quality checks, binary analyzing, logging, etc.
- Binary compatibility ``compatibility.py`` extension allows to write custom rules for
  defining custom binary compatibility accross different settings and options
- The ``cmd_wrapper.py`` extension allows to inject arbitrary command wrappers to any
  ``self.run()`` recipe command invocation, which can be useful to inject wrappers as
  parallelization tools
- The package signing extension allows to sign and verify packages at upload and install time
  respectively


TODO: Put commands here?


Contents:

.. toctree::
   :maxdepth: 2

   extensions/python_requires
   extensions/custom_commands
   extensions/python_api
   extensions/hooks
   extensions/binary_compatibility
   extensions/profile_plugin
   extensions/command_wrapper
   extensions/package_signing
   
