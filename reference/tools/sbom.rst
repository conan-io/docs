.. _conan_tools_sbom:

.. include:: ../../common/experimental_warning.inc

conan.tools.sbom
=================

A Software Bill of Materials (SBOM) is a document that lists all the components, libraries,
dependencies, and other elements that make up a specific piece of software. Similar to a bill
of materials in manufacturing, which details the parts and materials used to build a product,
an SBOM provides transparency about what is contained "inside" an application or software system.

Conan allows you to generate SBOMs natively by using the resolved dependency graph.
This way, you can create the SBOM for your program at the same time you build it.

For now, this feature is in an experimental state and currently only supports the CycloneDX 1.4 standard.
If you require a different standard, another version, or if you have suggestions for improvements,
please feel free to open an issue on our `GitHub <https://github.com/conan-io/conan/issues>`_ .
We would be delighted to hear your feedback!

CycloneDX
^^^^^^^^^

CycloneDX is one of the most widely used standards for SBOMs, supported by the OWASP Foundation.

Using this feature is as simple as implementing a :ref:`hook <reference_extensions_hooks>` in your client,
which uses this tool to create the SBOM and simply stores it in the appropriate location.

Let's look at two examples:

In the first one, we have the case where we want to generate the SBOM at the moment we create our app, after the
package method. This is very useful for keeping track of the components and dependencies of our software.
In the example, we save it in the metadata folder to keep our project organized.

.. code-block:: python

    import json
    import os
    from conan.errors import ConanException
    from conan.api.output import ConanOutput
    from conan.tools.sbom.cyclonedx import cyclonedx_1_4
    def post_package(conanfile):
        sbom_cyclonedx_1_4 = cyclonedx_1_4(conanfile.subgraph)
        metadata_folder = conanfile.package_metadata_folder
        file_name = "sbom.cdx.json"
        with open(os.path.join(metadata_folder, file_name), 'w') as f:
            json.dump(sbom_cyclonedx_1_4, f, indent=4)
        ConanOutput().success(f"CYCLONEDX CREATED - {conanfile.package_metadata_folder}")


In the second example, we generate our SBOM after the generate method. This allows us to create the SBOMs when we
install the dependencies from Conan. This can be very useful for generating SBOMs for different versions of our
dependencies.

.. code-block:: python

    import json
    import os
    from conan.errors import ConanException
    from conan.api.output import ConanOutput
    from conan.tools.sbom.cyclonedx import cyclonedx_1_4
    def post_generate(conanfile):
        sbom_cyclonedx_1_4 = cyclonedx_1_4(conanfile.subgraph)
        generators_folder = conanfile.generators_folder
        file_name = "sbom.cdx.json"
        os.mkdir(os.path.join(generators_folder, "sbom"))
        with open(os.path.join(generators_folder, "sbom", file_name), 'w') as f:
            json.dump(sbom_cyclonedx_1_4, f, indent=4)
        ConanOutput().success(f"CYCLONEDX CREATED - {conanfile.generators_folder}")


Both hooks can coexist in such a way that we can generate the SBOMs for our application and our dependencies separately.
This can greatly assist us in conducting continuous analysis of our development process and ensuring software quality.