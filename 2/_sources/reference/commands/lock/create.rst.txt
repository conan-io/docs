conan lock create
=================

.. autocommand::
    :command: conan lock create -h


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
