.. _integrations_autotools:

|autotools_logo| Autotools
==========================

Conan provides different tools to help manage your projects using Autotools. They can be
imported from ``conan.tools.gnu``. The most relevant are:

- `AutotoolsDeps` is the dependencies generator for Autotools. It will generate shell
  scripts containing environment variable definitions that the autotools build system can
  understand.

- `AutotoolsToolchain` is the toolchain generator for Autotools. It will generate shell
  scripts containing environment variable definitions that the autotools build system can
  understand.

- `Autotools` build helper is a wrapper around the command line invocation of autotools.
  It abstracts calls like `./configure` or `make` into Python method calls.

- `PkgConfigDeps` is the dependencies generator for `pkg-config`. Generates `pkg-config`
  files for all the required dependencies of a package.

For the full list of tools under ``conan.tools.gnu`` please check the :ref:`reference
<conan_tools_gnu>`. 

.. seealso::

    - Reference for :ref:`AutotoolsDeps<conan_tools_gnu_autotoolsdeps>`,
      :ref:`AutotoolsToolchain<conan_tools_gnu_autotoolstoolchain>`, :ref:`Autotools<conan_tools_gnu_build_helper>` and
      :ref:`PkgConfigDeps<conan_tools_gnu_pkgconfigdeps>`.

.. |autotools_logo| image:: ../images/integrations/conan-autotools-logo.png
