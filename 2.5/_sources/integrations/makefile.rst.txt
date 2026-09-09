.. _integrations_makefile:

|gnu_make_logo| Makefile
========================

Conan provides different tools to help manage your projects using Make. They can be
imported from ``conan.tools.gnu``. Besides the most popular variant, GNU Make, Conan also
supports other variants like BSD Make. The most relevant tools are:

- `MakeDeps`: the dependencies generator for Make, which generates a Makefile containing
  definitions that the Make build tool can understand.

Currently, there is no ``MakeToolchain`` generator, it should be added in the future.

For the full list of tools under ``conan.tools.gnu`` please check the :ref:`reference
<conan_tools_gnu>` section.

.. seealso::

    - Reference for :ref:`MakeDeps<conan_tools_gnu_makedeps>`.

.. |gnu_make_logo| image:: ../images/integrations/conan-autotools-logo.png
