.. _integrations_premake:

|premake_logo| Premake
======================

Conan provides different tools to help manage your projects using Premake. They can be
imported from ``conan.tools.premake``. The most relevant tools are:

- ``PremakeDeps``: the dependencies generator for Premake, to allow consuming dependencies from Premake projects.

- ``PremakeToolchain``: the toolchain generator for Premake. It will create a
  wrapper over premake scripts allowing premake workspace and projects
  customization.

- ``Premake``: the Premake build helper. It's simply a wrapper around the command line invocation of Premake.

.. seealso::

    - Reference for :ref:`conan_tools_premake_premakedeps`.
    - Reference for :ref:`conan_tools_premake_premaketoolchain`.
    - Reference for :ref:`conan_tools_premake_premake`.


.. |premake_logo| image:: ../images/integrations/conan-premake-logo.png
