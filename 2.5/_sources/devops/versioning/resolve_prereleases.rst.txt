.. _resolve_prereleases_summary:

Handling version ranges and pre-releases
========================================

When developing a package and using version ranges for defining our dependencies,
there might come a time when a new version of a dependency gets a new pre-release version that we would like to test
before it's released to have a change to validate the new version ahead of time.

At first glance, it could be expected that the new version matches our range if it intersect it,
but :ref:`as described in the version ranges tutorial<tutorial_version_ranges_expressions>`,
by default Conan does not match pre-release versions to ranges that don't specify it.
Conan provides the :ref:`global.conf<reference_config_files_global_conf>` ``core.version_ranges:resolve_prereleases``,
which when set to ``True``, enables pre-release matching in version ranges.
This avoids having to modify and export the recipes of your dependency graph, which would become unfeasible for large ones.

This conf has the added benefit of affecting the whole dependency graph, so that if any of our dependencies also define
a requirement to our library of interest, the new version will also be picked up by it.

Let's see this in action. Imagine we have the following (summarized) dependency graph,
in which we depend on ``libpng`` and ``libmysqlclient``, both of which depend on ``zlib`` via the ``[>1.2 <2]`` version range:

.. graphviz::

   digraph G {
      node [fillcolor="lightskyblue", style=filled, shape=box]
      "app" -> "libpng/1.6.40"
      "app" -> "libmysqlclient/8.1.0"

      "libpng/1.6.40" -> "zlib/1.2.13" [label="[>1.2 <2]"]
      "libmysqlclient/8.1.0" -> "zlib/1.2.13" [label="[>1.2 <2]"]
   }

If ``zlib/1.3-pre`` is now published, using it is as easy as modifying your :ref:`global.conf<reference_config_files_global_conf>`
file and adding the line ``core.version_ranges:resolve_prereleases=True``
(or adding the ``--core-conf core.version_ranges:resolve_prereleases=True`` CLI argument to your command invocations),
after which, running ``conan create`` will now output the expected prerelease version of ``zlib`` being used:

.. code-block:: text

   ...

   ======== Computing dependency graph ========
   Graph root
      cli
   Requirements
      libmysqlclient/8.1.0#493d36bd9641e15993479706dea3c341 - Cache
      libpng/1.6.40#2ba025f1324ff820cf68c9e9c94b7772 - Cache
      lz4/1.9.4#b572cad582ca4d39c0fccb5185fbb691 - Cache
      openssl/3.1.2#f2eb8e67d3f5513e8a9b5e3b62d87ea1 - Cache
      zlib/1.3-pre#f2eb8e6ve24ff825bca32bea494b77dd - Cache
      zstd/1.5.5#54d99a44717a7ff82e9d37f9b6ff415c - Cache
   Build requirements
      cmake/3.27.1#de7930d308bf5edde100f2b1624841d9 - Cache
   Resolved version ranges
      cmake/[>=3.18 <4]: cmake/3.27.1
      openssl/[>=1.1 <4]: openssl/3.1.2
      zlib/[>1.2 <2]: zlib/1.3-pre
   ...


Now our package can be tested and validated against this new version,
and the conf be afterwards removed once the testing is over to go back to the usual Conan behaviour.
