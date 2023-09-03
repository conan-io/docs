.. _reference_extensions:

Extensions
----------

Conan can be extended in a few ways, with custom user code:

- ``python_requires`` allow to put common recipe code in a recipe package that can be
  reused by other recipes by declaring a ``python_requires = "mypythoncode/version"``
- You can create your own custom Conan commands to solve self-needs thanks to Python and
  Conan public API powers altogether.
- It's also possible to make your own custom Conan generators in case you are using build
  systems that are not supported by the built-in Conan tools. Those can be used from
  ``python_requires`` or installed globally.
- ``hooks`` are "pre" and "post" recipe methods (like ``pre_build()`` and ``post_build()``) 
  extensions that can be used to complement recipes
  with orthogonal functionality, like quality checks, binary analyzing, logging, etc.
- Binary compatibility ``compatibility.py`` extension allows to write custom rules for
  defining custom binary compatibility across different settings and options
- The ``cmd_wrapper.py`` extension allows to inject arbitrary command wrappers to any
  ``self.run()`` recipe command invocation, which can be useful to inject wrappers as
  parallelization tools
- The package signing extension allows to sign and verify packages at upload and install time
  respectively
- Deployers, a mechanism to facilitate copying files from one folder, usually the Conan cache, to user folders


..  note::

    Besides the built-in Conan extensions listed in this document, there is a repository
    that contains extensions for Conan, such as custom commands and deployers, useful for
    different purposes like artifactory tasks, Conan Center Index, etc.

    You can find more information on how to use those extensions in `the GitHub repository
    <https://github.com/conan-io/conan-extensions>`_.


Contents:

.. toctree::
   :maxdepth: 2

   extensions/python_requires
   extensions/custom_commands
   extensions/custom_generators
   extensions/python_api
   extensions/deployers
   extensions/hooks
   extensions/binary_compatibility
   extensions/profile_plugin
   extensions/command_wrapper
   extensions/package_signing
   
