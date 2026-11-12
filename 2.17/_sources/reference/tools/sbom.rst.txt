.. _conan_tools_sbom:

.. include:: ../../common/experimental_warning.inc

conan.tools.sbom
=================

CycloneDX
^^^^^^^^^
The CycloneDX tool is available in the ``conan.tools.sbom.cyclonedx`` module.

It provides the ``cyclonedx_1_4`` and ``cyclonedx_1_6`` functions which receive a ``conanfile``
and return a dictionary with the SBOM data in the CycloneDX 1.4/1.6 JSON format.

.. currentmodule:: conan.tools.sbom.cyclonedx
.. autofunction:: cyclonedx_1_4
.. autofunction:: cyclonedx_1_6


Both functions share an interface and are very similar; the main difference is the version of CycloneDX that each of
them supports. The options ``add_build`` and ``add_test`` allow you to include the build and test packages,
respectively, resolved by the graph.

Remember to enable the option if you wish to add any of them to your SBOM!

.. seealso::

    - :ref:`Software Bills of Materials (SBOM) <security_sboms>`.
