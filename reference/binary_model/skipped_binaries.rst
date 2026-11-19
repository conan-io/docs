.. _reference_binary_model_skipped_binaries:

Skipped binaries
================

Conan always computes the complete dependency graph: every recipe of every dependency is resolved,
loaded and evaluated, and every node gets its ``package_id`` computed. But computing the graph doesn't
mean that all the package binaries in that graph are necessary. Very often, a large part of
the dependencies binaries are not needed at all for the current command, and Conan avoids downloading,
building or installing them. These binaries are marked as **skipped** (``Skip``).

Skipping binaries is the default behavior, it is a deliberate optimization that can save a lot of
download time, disk space and build time, and it is also one of the reasons why the graph
:ref:`package types and requirement traits<reference_conanfile_methods_requirements>` are so important.

This section explains when and why Conan skips binaries, how to recognize it and how to change
this behavior when needed.


Recognizing skipped binaries
----------------------------

Let's use the following dependency graph as an example:

- ``app/0.1`` is an ``application`` that ``requires("openssl/0.1")``
- ``openssl/0.1`` is a ``shared-library`` that ``requires("zlib/0.1")``
- ``zlib/0.1`` is a ``static-library`` that has a ``tool_requires("tool/0.1")`` (some build tool)

Installing the ``app/0.1`` application, assuming that all the binaries have already been created:

.. code-block:: text
    :emphasize-lines: 6-9

    $ conan install --requires=app/0.1
    ...
    ======== Computing necessary packages ========
    Requirements
        app/0.1#f285...:cba9...#c921... - Cache
        openssl/0.1#b66c...:43fa...#0789... - Cache
    Build requirements
    Skipped host binaries
        zlib/0.1
    Skipped build binaries
        tool/0.1

The "Computing necessary packages" step lists the binaries that are actually going to be used, and
then, in separate ``Skipped host binaries``, ``Skipped test binaries`` and ``Skipped build binaries`` sections,
the packages whose binaries are not necessary. In this case:

- The ``zlib`` static library has been linked into the ``openssl`` shared library. Using ``openssl``
  doesn't require the ``zlib`` binary at all, neither to build ``app`` nor to run it.
- The ``tool/0.1`` was only necessary to build ``zlib``. As ``zlib`` is not being built from source,
  there is no need for the ``tool/0.1`` binary at all.

Skipped binaries are also visible in other places:

- ``conan graph info`` shows ``binary: Skip`` for those nodes, and in its
  :ref:`json output<reference_commands_graph_info_json_format>` the ``"binary"`` field of the node will be
  ``"Skip"``. The requirement edges in the json output also contain a ``"skip"`` field.
- In recipes, generators and deployers, the dependencies whose binaries are skipped still
  exist in ``self.dependencies``, but their ``package_folder`` is ``None``
  (see :ref:`the dependencies reference<reference_conanfile_methods_generate>`). Their
  ``package_info()`` method is not evaluated either.
- ``conan graph build-order`` doesn't include skipped binaries.


When is a binary necessary?
---------------------------

Conan computes which binaries are necessary starting from the consumer (the ``conanfile`` being installed, or
the ``--requires`` given in the command line) and from the packages that are going to be built from source,
and following the requirement traits (``headers``, ``libs``, ``run``, ``build``) that are propagated through the
graph. The rules are:

- The **direct dependencies of the consumer** are always necessary, including its ``tool_requires`` and
  ``test_requires``.
- A **package that is going to be built from source** needs the binaries of all its direct dependencies,
  including its ``tool_requires`` and ``test_requires``.
- A **transitive dependency** binary is necessary only if some of its "files" are needed by
  a node that needs it, that is, if the requirement propagated to that node through the graph still has some of
  the ``headers``, ``libs``, ``run`` or ``build`` traits enabled. If all of them have been dropped
  along the way, the transitive dependency binary is skipped.
- Any binary that is not necessary according to the above rules is skipped.

The propagation of traits is mostly derived from the ``package_type`` of the packages. The
most common cases are, for a consumer that depends on ``pkga`` that depends on ``pkgb``:

.. list-table::
   :header-rows: 1

   * - ``pkga`` package type
     - ``pkgb`` package type
     - ``pkgb`` binary
     - Reason
   * - ``shared-library`` or ``application``
     - ``static-library`` or ``header-library``
     - Skipped
     - ``pkgb`` has been embedded (linked) inside ``pkga``, it is no longer needed.
   * - ``static-library``
     - ``header-library``
     - Skipped
     - The headers have been compiled into ``pkga`` library, and they are not propagated, unless
       ``transitive_headers=True``.
   * - ``static-library``
     - ``static-library``
     - Necessary
     - The consumer needs to link both ``pkga`` and ``pkgb`` static libraries (the ``libs`` trait is
       propagated).
   * - any
     - ``shared-library``
     - Necessary
     - The ``pkgb`` shared library is needed at runtime (the ``run`` trait is propagated), and also
       for linking if ``pkga`` is a static library.
   * - ``header-library``
     - any
     - Necessary
     - A header-only library doesn't embed anything, the consumer needs everything that ``pkgb`` provides.

Also, the ``tool_requires`` and ``test_requires`` of ``pkga`` and ``pkgb`` are only necessary if
``pkga`` or ``pkgb`` respectively are going to be built from source. Otherwise, they are skipped.

Note that this is very much aligned with the "embed" and "non-embed" modes explained in
:ref:`the effect of dependencies on package_id<reference_binary_model_dependencies>`. When a package binary
**embeds** a dependency (for example a shared library linking a static library), the dependency
artifacts are already contained inside the consumer binary. That is the reason why the consumer
needs a new ``package_id`` for every change of the dependency (``full_mode`` by default), and it is also
the reason why the dependency binary can be skipped when using the consumer binary.

The traits can be modified explicitly in the ``requires()`` calls, like ``transitive_headers=True`` or
``transitive_libs=True``, and that will also change which binaries are necessary. See the
:ref:`requirement traits reference<reference_conanfile_methods_requirements>`.

.. important::

    The correct definition of ``package_type`` (explicitly, or implicitly via the ``shared`` option)
    is critical for this behavior. If the package types are unknown, Conan cannot know if a dependency
    has been embedded or not, and will be conservative, propagating the traits and requiring
    more binaries than necessary.


Skipped binaries and build modes
--------------------------------

The skipping of binaries happens after Conan has decided which binaries exist and which need to be built,
and it has some implications that are worth knowing:

- **A missing binary that is skipped is not an error**. In the example above, if the ``zlib/0.1`` binary
  doesn't exist in the cache or in any remote, ``conan install --requires=app/0.1`` will still succeed, because
  that binary is not needed. Only the binaries that are necessary will raise a "missing binary" error.
- **Build missing only builds necessary binaries**. If the ``zlib/0.1`` binary is missing, but
  ``app`` and ``openssl`` binaries exist, ``conan install --requires=app/0.1 --build=missing`` will not build
  ``zlib`` from source, it will be skipped. The same applies to ``--build=missing:[pattern]``.
- **Forced builds always build**. Packages explicitly forced to be built with ``--build="pkg/*"`` (or
  ``--build="*"``) are always built, even if their binaries wouldn't be necessary otherwise. As they are
  built, their dependencies binaries become necessary too. In the example above,
  ``conan install --requires=app/0.1 --build="openssl/*" --build=missing`` will build ``openssl``, and as it needs
  ``zlib`` to link, ``zlib`` will also be built if its binary is missing, and ``tool/0.1`` will no longer be skipped,
  as it is needed to build ``zlib``.

.. code-block:: text

    $ conan install --requires=app/0.1 --build="openssl/*" --build=missing
    ...
    Requirements
        app/0.1#f285...:cba9...#c921... - Cache
        openssl/0.1#b66c...:43fa... - Build
        zlib/0.1#f6a2...:dcf6... - Build
    Build requirements
        tool/0.1#6cb7...:dcf6...#e018... - Cache


Note that the recipes of skipped packages are still necessary: they are downloaded (if not in the cache) and
evaluated to compute the dependency graph and the ``package_id`` of their consumers. Skipping is
only about the package binaries. Skipped packages are still part of the dependency graph, so they will also be
captured in lockfiles, and listed by ``conan graph info``.

The ``tools.graph:skip_build`` and ``tools.graph:skip_test`` confs are a different thing: they make Conan not
expand ``tool_requires`` and ``test_requires`` at all, so not even their recipes are part of the graph.
In most cases they are not necessary, as Conan will already skip those binaries when they are not needed.
See :ref:`the build_requirements() reference<reference_conanfile_methods_build_requirements>`.


Disabling the skipping of binaries
----------------------------------

The default behavior should be good for the vast majority of cases, but there are some situations in which
all the binaries of the graph are needed, for example:

- Deploying all the dependencies binaries with a :ref:`deployer<reference_extensions_deployers>`, including
  the ones that have been embedded in other binaries.
- Collecting information that is only available in the package binaries of the whole graph, like licenses files.
- Populating a cache or a server with all the binaries of a dependency graph, or building all of them.

There are a few mechanisms to modify the default behavior:

- The ``tools.graph:skip_binaries`` conf, ``True`` by default. Defining it as ``False`` will make all
  binaries necessary:

  .. code-block:: bash

      $ conan install --requires=app/0.1 -c tools.graph:skip_binaries=False

  It can also be defined per-package using :ref:`conf patterns<reference_config_files_global_conf_patterns>`,
  to avoid skipping only some specific packages binaries, like ``-c "zlib/*:tools.graph:skip_binaries=False"``.

  Note that ``-c`` only applies to the "host" context. To also avoid skipping the binaries of the
  "build" context, like the ``tool_requires``, it is necessary to define it for the build context too,
  with ``-c:b`` or ``-c:a`` (for all contexts), or in the ``[conf]`` section of the build profile.

  If a package that would have been built only because of ``--build=missing`` defines
  ``tools.graph:skip_binaries=False``, it will be built (and its dependencies binaries will be necessary),
  even if its binary would have been skipped otherwise.

- The :ref:`no_skip=True requirement trait<reference_conanfile_methods_requirements_no_skip>`, defined in
  a recipe ``requires()``, forces the dependency binary to be necessary whenever the consumer binary is necessary.
  This should only be used in exceptional cases.

- If a dependency always needs to be available at runtime for all of its consumers, for example a
  ``static-library`` package that also contains some shared libraries, the
  :ref:`package_type_traits<conan_conanfile_attributes_package_type_traits>` attribute can be used in that
  dependency recipe to define ``"run": True``, so the ``run`` trait is propagated downstream and its binary will not
  be skipped.
