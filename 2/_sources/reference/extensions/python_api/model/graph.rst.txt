.. _reference_python_api_model_graph:

Dependency graph class
~~~~~~~~~~~~~~~~~~~~~~

A dependency graph is an opaque object, only meant to be produced and consumed by the
:class:`GraphAPI <conan.api.subapi.graph.GraphAPI>` methods. It should not be created,
inspected, or modified directly.

The only supported operation on it is calling its ``serialize()`` method, which returns a
``dict`` representation of the graph. That representation follows the same JSON schema
documented for the :ref:`"conan graph info" JSON formatter <reference_commands_graph_info_json_format>`.
