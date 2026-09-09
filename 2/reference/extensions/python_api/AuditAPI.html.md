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

* **Parameters:**
  * **deps_graph** – Dependency graph as returned by the [`Graph API`](https://docs.conan.io/2//reference/extensions/python_api/GraphAPI.html.md#conan.api.subapi.graph.GraphAPI)
  * **provider** – Provider object as returned by [`get_provider()`](#conan.api.subapi.audit.AuditAPI.get_provider)
  * **context** – Context to filter the dependencies (e.g., `"host"` or `"build"`). If `None`, all contexts are considered.
* **Returns:**
  A `dict` mapping each scanned reference to its vulnerability information,
  together with some metadata about the request, with the following shape:
  ```python
  {
      "data": {
          # One entry per scanned reference
          "openssl/3.2.0": {
              "vulnerabilities": {
                  "totalCount": 2,
                  # One "node" per vulnerability, holding its name,
                  # description, severity, cvss, references,
                  # advisories, fixed versions, etc.
                  "edges": [{"node": {...}}, ...]
              }
          },
          # References that could not be scanned carry an error instead
          "unknown/1.0": {"error": {"details": "Package 'unknown/1.0' not scanned: Not found."}},
      },
      # URL of the provider that produced the data, or None
      "provider_url": "https://...",
      # Only present if the whole request failed (authentication,
      # rate limit, server error...). When set, the scan is aborted.
      "conan_error": "...",
  }
  ```

#### *static* list(references: List[str], provider)

List the vulnerabilities of the given reference.

* **Parameters:**
  * **references** – List of reference strings
  * **provider** – Provider object as returned by [`get_provider()`](#conan.api.subapi.audit.AuditAPI.get_provider)
* **Returns:**
  A `dict` with the vulnerability information for each reference, with the same
  structure as the one returned by [`scan()`](#conan.api.subapi.audit.AuditAPI.scan).

#### get_provider(provider_name: str)

Get the provider opaque object by name.
This object is only meant to be used as arguments for other methods in this class,
and should not be used/modified directly.

* **Parameters:**
  **provider_name** – Provider name
* **Returns:**
  Provider opaque object

#### list_providers()

Get all available providers.

* **Returns:**
  The list of available providers

#### add_provider(name: str, url: str, provider_type: str)

Add a provider.

* **Parameters:**
  * **name** – Provider name
  * **url** – Provider url
  * **provider_type** – Provider type, either `conan-center-proxy` or `private`

#### remove_provider(provider_name: str)

Remove a provider.

* **Parameters:**
  **provider_name** – Provider name

#### auth_provider(provider, token: str)

Set authentication token for the provider.
Note that this does not perform an authentication attempt, it just stores the token for future use.

* **Parameters:**
  * **provider** – Provider name
  * **token** – Provider token
