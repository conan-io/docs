Changelog
=========

2.0.0-beta1 (20-June-2022)
--------------------------

For a more detailed description of the major changes that Conan 2.0 brings, compared with Conan 1.X, please read :ref:`whatsnew`


- Feature: New graph model to better support C and C++ binaries relationships, compilation, and linkage.
- Feature: New documented public Python API, for user automation
- Feature: New build system integrations, more flexible and powerful, and providing transparent integration when possible, like ``CMakeDeps`` and ``CMakeToolchain``
- Feature: New custom user commands, that can be built using the public PythonAPI and can be shared and installed with ``conan config install``
- Feature: New CLI interface, with cleaner commands and more structured output
- Feature: New deployers mechanism to copy artifacts from the cache to user folders, and consume those copies while building.
- Feature: Improved ``package_id`` computation, taking into account the new more detailed graph model.
- Feature: Added ``compatibility.py`` extension mechanism to allow users to define binary compatibility globally.
- Feature: Simpler and more powerful ``lockfiles`` to provide reproducibility over time.
- Feature: Better configuration with ``[conf]`` and better environment management with the new ``conan.tools.env`` tools.
- Feature: Conan cache now can store multiple revisions simultaneously.
- Feature: New extensions plugins to implement profile checking, package signing, and build commands wrapping.
- Feature: Used the package immutability for an improved update, install and upload flows.