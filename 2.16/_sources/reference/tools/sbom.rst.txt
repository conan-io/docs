.. _conan_tools_sbom:

.. include:: ../../common/experimental_warning.inc

conan.tools.sbom
=================

A Software Bill of Materials (SBOM) is a document that lists all the components, libraries,
dependencies, and other elements that make up a specific piece of software. Similar to a bill
of materials in manufacturing, which details the parts and materials used to build a product,
an SBOM provides transparency about what is contained "inside" an application or software system.

Conan allows you to generate SBOMs natively by using a resolved dependency graph.
This way, you can create the SBOM for your program at the same time you build it.

For now, **this feature is in an experimental state, which means that the interface, functionality or generated
files may change in the future**. Additionally, it currently supports CycloneDX versions 1.4 and 1.6.
If you need a different standard, another version, or if you encounter any potential improvements,
please feel free to open an issue on our `GitHub <https://github.com/conan-io/conan/issues>`_ .
We would be delighted to hear your feedback!

CycloneDX
^^^^^^^^^

Conan supports `CycloneDX <https://cyclonedx.org/>`_ out-of-the-box, which is one of the most widely used standards for SBOMs.

The CycloneDX tool is available in the ``conan.tools.sbom.cyclonedx`` module.
It provides the ``cyclonedx_1_4`` and ``cyclonedx_1_6`` functions which receive a ``conanfile``
and return a dictionary with the SBOM data in the CycloneDX 1.4/1.6 JSON format.

.. currentmodule:: conan.tools.sbom.cyclonedx
.. autofunction:: cyclonedx_1_4
.. autofunction:: cyclonedx_1_6

Using this feature is as simple as implementing a :ref:`hook <reference_extensions_hooks>` in your client
which uses this tool to create the SBOM and stores it in the appropriate location.

Usage examples
~~~~~~~~~~~~~~

Let's look at two examples:

In the first one, we want to generate the SBOM at the moment we create our app, after the
package method. This is very useful for keeping track of the components and dependencies of that went into building our software.
In the example, we save the generated sbom in the package metadata folder to keep our project organized


.. code-block:: python

    import json
    import os
    from conan.api.output import ConanOutput
    from conan.tools.sbom.cyclonedx import cyclonedx_1_6

    def post_package(conanfile, **kwargs):
        sbom_cyclonedx_1_6 = cyclonedx_1_6(conanfile)
        metadata_folder = conanfile.package_metadata_folder
        file_name = "sbom.cdx.json"
        with open(os.path.join(metadata_folder, file_name), 'w') as f:
            json.dump(sbom_cyclonedx_1_6, f, indent=4)
        ConanOutput().success(f"CYCLONEDX CREATED - {conanfile.package_metadata_folder}")

.. seealso::

    - :ref:`See here for more information on the metadata feature <devops_metadata>`.


In the second example, we generate our SBOM after the generate method. This allows us to create the SBOMs when we
install the dependencies from Conan. This can be very useful for generating SBOMs for different versions of our
dependencies. Note that this time we're saving the SBOM in the generators folder, so that the user installing the dependencies
has easy access to the SBOM.

.. code-block:: python

    import json
    import os
    from conan.api.output import ConanOutput
    from conan.tools.sbom.cyclonedx import cyclonedx_1_6

    def post_generate(conanfile, **kwargs):
        sbom_cyclonedx_1_6 = cyclonedx_1_6(conanfile)
        generators_folder = conanfile.generators_folder
        file_name = "sbom.cdx.json"
        os.mkdir(os.path.join(generators_folder, "sbom"))
        with open(os.path.join(generators_folder, "sbom", file_name), 'w') as f:
            json.dump(sbom_cyclonedx_1_6, f, indent=4)
        ConanOutput().success(f"CYCLONEDX CREATED - {conanfile.generators_folder}")


Both hooks can coexist in such a way that we can generate the SBOMs for our application and our dependencies separately.
This can greatly assist us in conducting continuous analysis of our development process and ensuring software quality.

Generating a Conan-based SBOM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Instead of using a standard, we can take a "Conan-based approach". Thanks to the ``conanfile.subgraph.serialize()``
function, we can directly obtain information about the dependencies of our package.
In the following example, we can see a hook that generates a simplified SBOM
consisting of the serialization of the subgraph, which includes all data Conan has
about the specific dependencies. Note that this serialization is not a standard SBOM format,
and is not standardized in any way. The information is similar to the one provided by the
:command:`conan graph info ... --format=json` command.

.. code-block:: python

    import json
    import os
    from conan.api.output import ConanOutput

    def post_package(conanfile, **kwargs):
        metadata_folder = conanfile.package_metadata_folder
        file_name = "sbom.conan.json"
        with open(os.path.join(metadata_folder, file_name), 'w') as f:
            json.dump(conanfile.subgraph.serialize(), f, indent=2)
        ConanOutput().success(f"CONAN SBOM CREATED - {conanfile.package_metadata_folder}")

