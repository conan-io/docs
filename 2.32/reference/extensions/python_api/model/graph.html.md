<a id="reference-python-api-model-graph"></a>

# Dependency graph class

A dependency graph is an opaque object, only meant to be produced and consumed by the
[`GraphAPI`](https://docs.conan.io/2//reference/extensions/python_api/GraphAPI.html.md#conan.api.subapi.graph.GraphAPI) methods. It should not be created,
inspected, or modified directly.

The only supported operation on it is calling its `serialize()` method, which returns a
`dict` representation of the graph. That representation follows the same JSON schema
documented for the [“conan graph info” JSON formatter](https://docs.conan.io/2//reference/commands/formatters/graph_info_json_formatter.html.md#reference-commands-graph-info-json-format).
