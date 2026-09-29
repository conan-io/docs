.. _versioning_lockfiles_configurations:

Multiple configurations
=======================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

In the previous section we managed just 1 configuration, for the default profile. In many applications,
packages needs to be built with several different configurations, typically managed by different profile
files.

.. note::

    This section continues with the previous example with the :ref:`versioning_lockfiles_introduction`.
    The code used in this section, including a *build.py* script to reproduce it, is in the
    examples repository: https://github.com/conan-io/examples. You can go step by step
    reproducing this example while reading the below documentation.

    .. code:: bash

        $ git clone https://github.com/conan-io/examples.git
        $ cd features/lockfiles/intro
        # $ python build.py only to run the full example, but better go step by step


Lets start in the *features/lockfiles/intro* of the examples repository, remove the previous packages,
and create both release and debug ``pkga`` packages:

.. code-block:: bash

    $ conan remove "pkg*" -f
    $ conan create pkga pkga/0.1@user/testing
    $ conan create pkga pkga/0.1@user/testing -s build_type=Debug


Now, we could (don't do it) create 2 different lockfiles, one for each configuration:


.. code-block:: bash

    # DO NOT type these commands, we'll do it better below
    $ cd pkgb
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_release.lock
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_debug.lock -s build_type=Debug
        

.. important::

    The dependency graph is different for each different configuration/profile. Not only the package-ids, but also because of
    conditional requirements, the dependencies can be different. Then, it is necessary to create a lockfile for every different 
    configuration/profile. 


But, what if a new ``pkga/0.2@user/testing`` version was created in the time between both commands,? Although this is unlikely to happen in this
example, because everything is local. However, it could happen that ``pkga`` was in a server and the CI, uploads the new
version while we are running the above commands.


Base lockfiles
--------------

Conan proposes a "base" lockfile, with the :command:`--base` argument, that will capture only the versions and topology of the
graph, but not the package-ids:

.. code-block:: bash

    $ cd pkgb
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_base.lock --base

Let's inspect the *locks/pkgb_base.lock* lockfile:

.. code-block:: json

    {                                  
        "graph_lock": {                   
            "nodes": {                       
                "0": {                          
                    "ref": "pkgb/0.1@user/testing",
                    "requires": ["1"],                             
                    "path": "..\\conanfile.py",    
                    "context": "host"              
                },                              
                "1": {                          
                    "ref": "pkga/0.1@user/testing",
                    "context": "host"              
                }                               
            },                               
            "revisions_enabled": false       
        },                                
        "version": "0.4"                  
    } 

This lockfile is different to the ones in the previous section. It does not store the ``profile``, and it does not capture
the package-ids or the options of the nodes. It captures the topology of the graph, and the package references and versions.

At this point, the new ``pkga/0.2@user/testing`` version packages could be created:

.. code-block:: bash

    $ cd ..
    # The recipe generates different package code depending on the version, automatically
    $ conan create pkga pkga/0.2@user/testing
    $ conan create pkga pkga/0.2@user/testing -s build_type=Debug


Using the "base" *locks/pkgb_base.lock* lockfile, now we can obtain a new lockfile for both debug and release configurations, and
it is guaranteed that both will use the ``pkga/0.1@user/testing`` dependency, and not the new one:

.. code-block:: bash

    $ cd pkgb
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile=locks/pkgb_base.lock --lockfile-out=locks/pkgb_deps_debug.lock -s build_type=Debug
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile=locks/pkgb_base.lock --lockfile-out=locks/pkgb_deps_release.lock

Now, we will have 2 lockfiles, *locks/pkgb_deps_debug.lock* and *locks/pkgb_deps_release.lock*. Each one will lock different profiles and different package-id
of ``pkga/0.1@user/testing``.


Locked configuration
--------------------

The lockfiles store the effective configuration, settings, options, resulting from the used profiles and command line arguments.
That configuration arguments can be passed to the ``conan lock create`` command, but not when using lockfiles. For example:

.. code-block:: bash

    $ mkdir build && cd build
    $ conan install .. --lockfile=../locks/pkgb_deps_debug.lock -s build_type=Debug
    ERROR: Cannot use profile, settings, options or env 'host' when using lockfile

results in an error, because the *locks/pkgb_deps_debug.lock* already stores the ``settings.build_type`` and passing it in the command line
could only result in inconsistencies and errors.

.. important::

    Lockfiles store the full effective profile configuration. It is not possible to pass configuration, settings, options or 
    profile arguments when using lockfiles (only when creating the lockfiles)

With the two captured lockfiles, now we can locally build and run our ``pkgb`` application for both configurations, guaranteeing
the dependency to ``pkga/0.1@user/testing``:

.. code-block:: bash

    $ conan install .. --lockfile=../locks/pkgb_deps_release.lock
    $ cmake ../src -G "Visual Studio 15 Win64"
    $ cmake --build . --config Release
    $ ./bin/greet
    HelloA 0.1 Release
    HelloB Release!
    Greetings Release!
    $ conan install .. --lockfile=../locks/pkgb_deps_debug.lock
    $ cmake --build . --config Debug
    $ ./bin/greet
    HelloA 0.1 Debug
    HelloB Debug!
    Greetings Debug!

We can create ``pkgb`` package again for both configurations:

.. code-block:: bash

    $ cd ..
    $ conan create . user/testing --lockfile=locks/pkgb_deps_release.lock --lockfile-out=locks/pkgb_release.lock
    $ conan create . user/testing --lockfile=locks/pkgb_deps_debug.lock --lockfile-out=locks/pkgb_debug.lock


And we could still use the lockfiles later in time to install the ``pkgb`` package with the same dependencies
and configuration that were used to create that package:


.. code-block:: bash

    $ cd ..
    $ mkdir consume
    $ cd consume
    $ conan install pkgb/0.1@user/testing --lockfile=../pkgb/locks/pkgb_release.lock
    $ ./bin/greet
    HelloA 0.1 Release
    HelloB Release!
    Greetings Release!
    $ conan install pkgb/0.1@user/testing --lockfile=../pkgb/locks/pkgb_debug.lock
    $ ./bin/greet
    HelloA 0.1 Debug
    HelloB Debug!
    Greetings Debug!

As you can see, the immutability principle remains. If we try to use *pkgb_release.lock* to create the ``pkgb`` package
again instead of the *pkgb_deps_release.lock* lockfile, it will error, as ``pkgb`` would be already fully
locked in the former.
