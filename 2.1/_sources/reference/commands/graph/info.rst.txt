.. _reference_graph_info:

conan graph info
================

.. autocommand::
    :command: conan graph info -h


The ``conan graph info`` command shows information about the dependency graph for the recipe specified in ``path``.


**Examples**:

.. code-block:: bash

    $ conan graph info .
    $ conan graph info myproject_folder
    $ conan graph info myproject_folder/conanfile.py
    $ conan graph info --requires=hello/1.0@user/channel

The output will look like:

.. code-block:: text

    $ conan graph info --require=binutils/2.38 -r=conancenter

    ...

    ======== Basic graph information ========
    conanfile:
      ref: conanfile
      id: 0
      recipe: Cli
      package_id: None
      prev: None
      build_id: None
      binary: None
      invalid_build: False
      info_invalid: None
      revision_mode: hash
      package_type: unknown
      settings:
        os: Macos
        arch: armv8
        compiler: apple-clang
        compiler.cppstd: gnu17
        compiler.libcxx: libc++
        compiler.version: 14
        build_type: Release
      options:
      system_requires:
      recipe_folder: None
      source_folder: None
      build_folder: None
      generators_folder: None
      package_folder: None
      cpp_info:
        root:
          includedirs: ['include']
          srcdirs: None
          libdirs: ['lib']
          resdirs: None
          bindirs: ['bin']
          builddirs: None
          frameworkdirs: None
          system_libs: None
          frameworks: None
          libs: None
          defines: None
          cflags: None
          cxxflags: None
          sharedlinkflags: None
          exelinkflags: None
          objects: None
          sysroot: None
          requires: None
          properties: None
      label: cli
      context: host
      test: False
      requires:
        1: binutils/2.38#0dc90586530d3e194d01d17cb70d9461
    binutils/2.38#0dc90586530d3e194d01d17cb70d9461:
      ref: binutils/2.38#0dc90586530d3e194d01d17cb70d9461
      id: 1
      recipe: Downloaded
      package_id: 5350e016ee8d04f418b50b7be75f5d8be9d79547
      prev: None
      build_id: None
      binary: Invalid
      invalid_build: False
      info_invalid: cci does not support building binutils for Macos since binutils is degraded there (no as/ld + armv8 does not build)
      url: https://github.com/conan-io/conan-center-index/
      license: GPL-2.0-or-later
      description: The GNU Binutils are a collection of binary tools.
      topics: ('gnu', 'ld', 'linker', 'as', 'assembler', 'objcopy', 'objdump')
      homepage: https://www.gnu.org/software/binutils
      revision_mode: hash
      package_type: application
      settings:
        os: Macos
        arch: armv8
        compiler: apple-clang
        compiler.version: 14
        build_type: Release
      options:
        multilib: True
        prefix: aarch64-apple-darwin-
        target_arch: armv8
        target_os: Macos
        target_triplet: aarch64-apple-darwin
        with_libquadmath: True
      system_requires:
      recipe_folder: /Users/barbarian/.conan2/p/binut53bd9b3ee9490/e
      source_folder: None
      build_folder: None
      generators_folder: None
      package_folder: None
      cpp_info:
        root:
          includedirs: ['include']
          srcdirs: None
          libdirs: ['lib']
          resdirs: None
          bindirs: ['bin']
          builddirs: None
          frameworkdirs: None
          system_libs: None
          frameworks: None
          libs: None
          defines: None
          cflags: None
          cxxflags: None
          sharedlinkflags: None
          exelinkflags: None
          objects: None
          sysroot: None
          requires: None
          properties: None
      label: binutils/2.38
      context: host
      test: False
      requires:
        2: zlib/1.2.13#416618fa04d433c6bd94279ed2e93638
    zlib/1.2.13#416618fa04d433c6bd94279ed2e93638:
      ref: zlib/1.2.13#416618fa04d433c6bd94279ed2e93638
      id: 2
      recipe: Cache
      package_id: 76f7d863f21b130b4e6527af3b1d430f7f8edbea
      prev: 866f53e31e2d9b04d49d0bb18606e88e
      build_id: None
      binary: Skip
      invalid_build: False
      info_invalid: None
      url: https://github.com/conan-io/conan-center-index
      license: Zlib
      description: A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)
      topics: ('zlib', 'compression')
      homepage: https://zlib.net
      revision_mode: hash
      package_type: static-library
      settings:
        os: Macos
        arch: armv8
        compiler: apple-clang
        compiler.version: 14
        build_type: Release
      options:
        fPIC: True
        shared: False
      system_requires:
      recipe_folder: /Users/barbarian/.conan2/p/zlibbcf9063fcc882/e
      source_folder: None
      build_folder: None
      generators_folder: None
      package_folder: None
      cpp_info:
        root:
          includedirs: ['include']
          srcdirs: None
          libdirs: ['lib']
          resdirs: None
          bindirs: ['bin']
          builddirs: None
          frameworkdirs: None
          system_libs: None
          frameworks: None
          libs: None
          defines: None
          cflags: None
          cxxflags: None
          sharedlinkflags: None
          exelinkflags: None
          objects: None
          sysroot: None
          requires: None
          properties: None
      label: zlib/1.2.13
      context: host
      test: False
      requires:


:command:`conan graph info` builds the complete dependency graph, like :command:`conan install` does.
The main difference is that it doesn't try to install or build the binaries, but the package recipes
will be retrieved from remotes if necessary.

It is very important to note that the :command:`conan graph info` command outputs the dependency graph for a
given configuration (settings, options), as the dependency graph can be different for different
configurations. This means that the input to the :command:`conan graph info` command
is the same as :command:`conan install`, the configuration can be specified directly with settings and options,
or using profiles,and querying the graph of a specific recipe is possible by using the ``--requires`` flag as shown above.


You can additionally filter the output, both by filtering by fields (``--filter``) and by package (``--filter-package``).
For example, to get the options of zlib, the following command could be run:

.. code-block:: text

    $ conan graph info --require=binutils/2.38 -r=conancenter --filter=options --package-filter="zlib*"

    ...

    ======== Basic graph information ========
    zlib/1.2.13#13c96f538b52e1600c40b88994de240f:
      ref: zlib/1.2.13#13c96f538b52e1600c40b88994de240f
      options:
        fPIC: True
        shared: False


You can generate a graph of your dependencies in ``json``, ``dot`` or ``html`` formats:

Now, let's try the ``dot`` format for instance:

.. code-block:: bash
    :caption: **binutils/2.38 graph info to DOT**

    $ conan graph info --require=binutils/2.38 -r=conancenter --format=dot > graph.dot

Which generates the following file:

.. code-block:: dot
    :caption: **graph.dot**

    digraph {
            "cli" -> "binutils/2.38"
            "binutils/2.38" -> "zlib/1.2.13"
    }

.. graphviz::

    digraph {
            "cli" -> "binutils/2.38"
            "binutils/2.38" -> "zlib/1.2.13"
    }


.. note::
    If using ``format=html``, the generated html contains links to a third-party resource,
    the *vis.js* library with 2 files: *vis.min.js*, *vis.min.css*.
    By default they are retrieved from Cloudfare. However, for environments without internet connection,
    you'll need to create a template for the file and place it in ``CONAN_HOME/templates/graph.html``.
    to point to a local version of these files:

    - *vis.min.js*: "https://cdnjs.cloudflare.com/ajax/libs/vis/4.18.1/vis.min.js"
    - *vis.min.css*: "https://cdnjs.cloudflare.com/ajax/libs/vis/4.18.1/vis.min.css"

    You can use the template found in ``cli/formatters/graph/info_graph.html`` as a basis for your own.


.. seealso::

    - Check the :ref:`JSON format output <reference_commands_graph_info_json_format>` for this command.
