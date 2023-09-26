.. _reference_graph_info:

conan graph info
================

.. code-block:: text
        
        $ conan graph info -h
        usage: conan graph info [-h] [-f FORMAT] [-v [V]] [--name NAME]
                                [--version VERSION] [--user USER] [--channel CHANNEL]
                                [--requires REQUIRES] [--tool-requires TOOL_REQUIRES]
                                [-b BUILD] [-r REMOTE | -nr] [-u] [-o OPTIONS_HOST]
                                [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                                [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                                [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                                [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                                [-c CONF_HOST] [-c:b CONF_BUILD] [-c:h CONF_HOST]
                                [-l LOCKFILE] [--lockfile-partial]
                                [--lockfile-out LOCKFILE_OUT] [--lockfile-packages]
                                [--lockfile-clean]
                                [--lockfile-overrides LOCKFILE_OVERRIDES]
                                [--check-updates] [--filter FILTER]
                                [--package-filter PACKAGE_FILTER] [-d DEPLOYER]
                                [-df DEPLOYER_FOLDER] [--build-require]
                                [path]

        Compute the dependency graph and show information about it.

        positional arguments:
          path                  Path to a folder containing a recipe (conanfile.py or
                                conanfile.txt) or to a recipe file. e.g.,
                                ./my_project/conanfile.txt.

        optional arguments:
          -h, --help            show this help message and exit
          -f FORMAT, --format FORMAT
                                Select the output format: html, json, dot
          -v [V]                Level of detail of the output. Valid options from less
                                verbose to more verbose: -vquiet, -verror, -vwarning,
                                -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                                -vvv or -vtrace
          --name NAME           Provide a package name if not specified in conanfile
          --version VERSION     Provide a package version if not specified in
                                conanfile
          --user USER           Provide a user if not specified in conanfile
          --channel CHANNEL     Provide a channel if not specified in conanfile
          --requires REQUIRES   Directly provide requires instead of a conanfile
          --tool-requires TOOL_REQUIRES
                                Directly provide tool-requires instead of a conanfile
          -b BUILD, --build BUILD
                                Optional, specify which packages to build from source.
                                Combining multiple '--build' options on one command
                                line is allowed. Possible values: --build="*" Force
                                build from source for all packages. --build=never
                                Disallow build for all packages, use binary packages
                                or fail if a binary package is not found, it cannot be
                                combined with other '--build' options. --build=missing
                                Build packages from source whose binary package is not
                                found. --build=cascade Build packages from source that
                                have at least one dependency being built from source.
                                --build=[pattern] Build packages from source whose
                                package reference matches the pattern. The pattern
                                uses 'fnmatch' style wildcards. --build=~[pattern]
                                Excluded packages, which will not be built from the
                                source, whose package reference matches the pattern.
                                The pattern uses 'fnmatch' style wildcards.
                                --build=missing:[pattern] Build from source if a
                                compatible binary does not exist, only for packages
                                matching pattern.
          -r REMOTE, --remote REMOTE
                                Look in the specified remote or remotes server
          -nr, --no-remote      Do not use remote, resolve exclusively in the cache
          -u, --update          Will check the remote and in case a newer version
                                and/or revision of the dependencies exists there, it
                                will install those in the local cache. When using
                                version ranges, it will install the latest version
                                that satisfies the range. Also, if using revisions, it
                                will update to the latest revision for the resolved
                                version range.
          -o OPTIONS_HOST, --options OPTIONS_HOST
                                Define options values (host machine), e.g.: -o
                                Pkg:with_qt=true
          -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                                Define options values (build machine), e.g.: -o:b
                                Pkg:with_qt=true
          -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                                Define options values (host machine), e.g.: -o:h
                                Pkg:with_qt=true
          -pr PROFILE_HOST, --profile PROFILE_HOST
                                Apply the specified profile to the host machine
          -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                                Apply the specified profile to the build machine
          -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                                Apply the specified profile to the host machine
          -s SETTINGS_HOST, --settings SETTINGS_HOST
                                Settings to build the package, overwriting the
                                defaults (host machine). e.g.: -s compiler=gcc
          -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                                Settings to build the package, overwriting the
                                defaults (build machine). e.g.: -s:b compiler=gcc
          -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                                Settings to build the package, overwriting the
                                defaults (host machine). e.g.: -s:h compiler=gcc
          -c CONF_HOST, --conf CONF_HOST
                                Configuration to build the package, overwriting the
                                defaults (host machine). e.g.: -c
                                tools.cmake.cmaketoolchain:generator=Xcode
          -c:b CONF_BUILD, --conf:build CONF_BUILD
                                Configuration to build the package, overwriting the
                                defaults (build machine). e.g.: -c:b
                                tools.cmake.cmaketoolchain:generator=Xcode
          -c:h CONF_HOST, --conf:host CONF_HOST
                                Configuration to build the package, overwriting the
                                defaults (host machine). e.g.: -c:h
                                tools.cmake.cmaketoolchain:generator=Xcode
          -l LOCKFILE, --lockfile LOCKFILE
                                Path to a lockfile. Use --lockfile="" to avoid
                                automatic use of existing 'conan.lock' file
          --lockfile-partial    Do not raise an error if some dependency is not found
                                in lockfile
          --lockfile-out LOCKFILE_OUT
                                Filename of the updated lockfile
          --lockfile-packages   Lock package-id and package-revision information
          --lockfile-clean      Remove unused entries from the lockfile
          --lockfile-overrides LOCKFILE_OVERRIDES
                                Overwrite lockfile overrides
          --check-updates       Check if there are recipe updates
          --filter FILTER       Show only the specified fields
          --package-filter PACKAGE_FILTER
                                Print information only for packages that match the
                                patterns
          -d DEPLOYER, --deployer DEPLOYER
                                Deploy using the provided deployer to the output
                                folder
          -df DEPLOYER_FOLDER, --deployer-folder DEPLOYER_FOLDER
                                Deployer output folder, base build folder by default
                                if not set
          --build-require       Whether the provided reference is a build-require

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
