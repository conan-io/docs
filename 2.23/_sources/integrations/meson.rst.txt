.. _integrations_meson:

|meson_logo| Meson
==================

Conan provides different tools to help manage your projects using Meson. They can be
imported from ``conan.tools.meson``. The most relevant tools are:

- `MesonToolchain`: generates the .ini files for Meson with the definitions of all the
  Meson properties related to the Conan options and settings for the current package,
  platform, etc. MesonToolchain normally works together with
  :ref:`PkgConfigDeps<conan_tools_gnu_pkgconfigdeps>` to manage all the dependencies.

- `Meson` build helper, a wrapper around the command line invocation of Meson.

.. seealso::

    - Reference for :ref:`MesonToolchain<conan_tools_meson_mesontoolchain>` and
      :ref:`Meson<conan_tools_meson_meson>`.
    - Build a simple Meson project using Conan
      :ref:`example<examples_tools_meson_toolchain_build_simple_meson_project>`

Build a simple Meson project using Conan

.. |meson_logo| image:: ../images/integrations/conan-meson-logo.png
