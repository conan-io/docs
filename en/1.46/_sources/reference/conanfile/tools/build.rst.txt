.. _conan_tools_build:

conan.tools.build
=================

conan.tools.build.cross_building()
----------------------------------

.. code-block:: python

    def cross_building(conanfile=None, skip_x64_x86=False):


Check it we are cross building comparing the *build* and *host* settings. Returns ``True``
in the case that we are cross-building.

Parameters:

- **conanfile**: Conanfile object, use always ``self``.
- **skip_x64_x86**: Will not consider the as cross-building the case of building in 64 bit
  architecture for 32 bit architecture, like ``build_arch=x86_64`` and ``host_arch=x86``
  for example.
