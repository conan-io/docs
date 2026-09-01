# Audit API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* AuditAPI(conan_api)

This class provides the functionality to scan references for vulnerabilities.

#### *static* scan(deps_graph, provider, context=None)

Scan a given recipe for vulnerabilities in its dependencies.

#### *static* list(references, provider)

List the vulnerabilities of the given reference.

#### get_provider(provider_name)

Get the provider by name.

#### list_providers()

Get all available providers.

#### add_provider(name, url, provider_type)

Add a provider.

#### remove_provider(provider_name)

Remove a provider.

#### auth_provider(provider, token)

Authenticate a provider.
