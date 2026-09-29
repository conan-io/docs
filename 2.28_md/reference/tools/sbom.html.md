<a id="conan-tools-sbom"></a>

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

# conan.tools.sbom

## CycloneDX

The CycloneDX tool is available in the `conan.tools.sbom` module.

It provides the `cyclonedx_1_4` and `cyclonedx_1_6` functions which receive a `conanfile`
and return a dictionary with the SBOM data in the CycloneDX 1.4/1.6 JSON format.

### cyclonedx_1_4(conanfile, name=None, add_build=False, add_tests=False, \*\*kwargs)

(Experimental) Generate cyclone 1.4 SBOM with JSON format

Creates a CycloneDX 1.4 Software Bill of Materials (SBOM) from a given dependency graph.

Parameters:
: conanfile: The conanfile instance.
  name (str, optional): Custom name for the metadata field.
  add_build (bool, optional, default=False): Include build dependencies.
  add_tests (bool, optional, default=False): Include test dependencies.

Returns:
: The generated CycloneDX 1.4 document as a string.

Example usage:
``
cyclonedx_1_4(conanfile, name="custom_name", add_build=True, add_test=True, **kwargs)
``

### cyclonedx_1_6(conanfile, name=None, add_build=False, add_tests=False, \*\*kwargs)

(Experimental) Generate cyclone 1.6 SBOM with JSON format

Creates a CycloneDX 1.6 Software Bill of Materials (SBOM) from a given dependency graph.

Parameters:
: conanfile: The conanfile instance.
  name (str, optional): Custom name for the metadata field.
  add_build (bool, optional, default=False): Include build dependencies.
  add_tests (bool, optional, default=False): Include test dependencies.

Returns:
: The generated CycloneDX 1.6 document as a string.

Example usage:
``
cyclonedx_1_6(conanfile, name="custom_name", add_build=True, add_test=True, **kwargs)
``

Both functions share an interface and are very similar; the main difference is the version of CycloneDX that each of
them supports. The options `add_build` and `add_test` allow you to include the build and test packages,
respectively, resolved by the graph.

Remember to enable the option if you wish to add any of them to your SBOM!

#### SEE ALSO
- [Software Bills of Materials (SBOM)](https://docs.conan.io/2//security/sboms.html.md#security-sboms).
- [Generate SBOMs with the built-in deployers](https://docs.conan.io/2//reference/extensions/deployers.html.md#reference-extensions-deployer-cyclone).
