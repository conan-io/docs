conan lock create
=================

.. code-block:: text

    $ conan lock create -h
    usage: conan lock create [-h] [-v [V]] [--name NAME]
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
                             [path]

    Create a lockfile from a conanfile or a reference.

    positional arguments:
      path                  Path to a folder containing a recipe (conanfile.py or
                            conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt.

    optional arguments:
      -h, --help            show this help message and exit
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
                            or fail if a binary package is not found. Cannot be
                            combined with other '--build' options. --build=missing
                            Build packages from source whose binary package is not
                            found. --build=cascade Build packages from source that
                            have at least one dependency being built from source.
                            --build=[pattern] Build packages from source whose
                            package reference matches the pattern. The pattern
                            uses 'fnmatch' style wildcards. --build=![pattern]
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

The ``conan lock create`` command creates a lockfile for the recipe or reference specified in ``path`` or ``--requires``.
This command will compute the dependency graph, evaluate which binaries do exist or need to be built, but it will
not try to install or build from source those binaries. In that regard, it is equivalent to the ``conan graph info`` command.
Most of the arguments accepted by this command are the same as ``conan graph info`` (and ``conan install``, ``conan create``), 
because the ``conan lock create`` creates or update a lockfile for a given configuration.

A lockfile can be created from scratch, computing a new dependency graph from a local conanfile, or from
requires, for example for this ``conanfile.txt``:

.. code-block:: text
  :caption: conanfile.txt

  [requires]
  fmt/9.0.0

  [tool_requires]
  cmake/3.23.5

We can run:

.. code-block:: bash

  $ conan lock create .
  
  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "fmt/9.0.0#ca4ae2047ef0ccd7d2210d8d91bd0e02%1675126491.773"
      ],
      "build_requires": [
          "cmake/3.23.5#5f184bc602682bcea668356d75e7563b%1676913225.027"
      ],
      "python_requires": []
  }

``conan lock create`` accepts a ``--lockfile`` input lockfile (if a ``conan.lock`` default one is found, it will
be automatically used), and then it will add new information in the ``--lockfile-out`` (by default, also ``conan.lock``).
For example if we change the above ``conanfile.txt``, removing the ``tool_requires``, updating ``fmt`` to ``9.1.0``
and adding a new dependency to ``zlib/1.2.13``:

.. code-block:: text
  :caption: conanfile.txt

  [requires]
  fmt/9.1.0
  zlib/1.2.13

  [tool_requires]

We will see how ``conan lock create`` **extends** the existing lockfile with the new configuration, but it doesn't 
remove unused versions or packages from it:

.. code-block:: bash

  $ conan lock create .  # will use the existing conan.lock as base, and rewrite it
  # use --lockfile and --lockfile-out to change that behavior
  
  $ cat conan.lock
  {                                                                          
    "version": "0.5",                                                      
    "requires": [                                                          
        "zlib/1.2.13#13c96f538b52e1600c40b88994de240f%1667396813.733",     
        "fmt/9.1.0#e747928f85b03f48aaf227ff897d9634%1675126490.952",       
        "fmt/9.0.0#ca4ae2047ef0ccd7d2210d8d91bd0e02%1675126491.773"        
    ],                                                                     
    "build_requires": [                                                    
        "cmake/3.23.5#5f184bc602682bcea668356d75e7563b%1676913225.027"     
    ],                                                                     
    "python_requires": []                                                  
  }

This behavior is very important to be able to capture multiple different configurations (Linux/Windows, shared/static,
Debug/Release, etc) that might have different dependency graphs. See the :ref:`lockfiles tutorial<tutorial_versioning_lockfiles>`,
to read more about lockfiles for multiple configurations.

If we want to trim unused versions and packages we can force it with the ``--lockfile-clean`` argument:

.. code-block:: bash

  $ conan lock create . --lockfile-clean
  # will use the existing conan.lock as base, and rewrite it, cleaning unused versions
  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "zlib/1.2.13#13c96f538b52e1600c40b88994de240f%1667396813.733",
          "fmt/9.1.0#e747928f85b03f48aaf227ff897d9634%1675126490.952"
      ],
      "build_requires": [],
      "python_requires": []
  }

.. seealso::

  The :ref:`lockfiles tutorial section<tutorial_versioning_lockfiles>` has more examples and hands on
  explanations of lockfiles.
