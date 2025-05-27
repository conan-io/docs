.. _reference_plugins:

Plugins
==========

Conan plugins are a powerful mechanism to customize and extend Conan's built-in
behavior. They are Python scripts loaded dynamically from the user's local
Conan cache, allowing users to intercept and augment specific parts of the
Conan workflow without modifying the Conan source code.

Plugins are ideal for advanced scenarios where teams or organizations need to:

- Enforce custom authorization or access control rules.
- Dynamically modify profiles or settings based on complex logic.
- Customize compression or packaging formats to optimize bandwidth or storage.
- Inject organization-specific policies into the package creation or usage flow.

Plugins offer a clean, maintainable, and shareable way to implement advanced
behavior, particularly in CI/CD pipelines or large-scale deployments.

They can be distributed and shared using ``conan config install``, making it easy to apply
consistent behavior across all users in a team.

The following types of plugins are currently supported:

.. toctree::
   :maxdepth: 2

   plugins/authorization_plugins
   plugins/profile_plugin
   plugins/compression_plugin

Each plugin type has a specific purpose and interface, which is documented in its corresponding section.
