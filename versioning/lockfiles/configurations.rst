.. _versioning_lockfiles_configurations:

Multiple configurations
=======================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


This section continues with the previous example with the :ref:`versioning_lockfiles_introduction`.
In that example we have managed just 1 configuration, for the default profile. In many applications,
packages needs to be built with several different configurations, typically managed by different profile
files.

Lets start in the *features/lockfiles/intro* of the examples repository, remove the previous packages,
and create both release and debug ``pkga`` packages:

.. code-block:: bash

    $ conan remove "*" -f
    $ conan create pkga pkga/0.1@user/testing
    $ conan create pkga pkga/0.1@user/testing -s build_type=Debug


Now, we could create 2 different lockfiles, one for each configuration:


.. code-block:: bash

    $ cd pkgb
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_release.lock
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_debug.lock -s build_type=Debug
        

.. important::

    The dependency graph is different for each different configuration/profile. Not only the package-ids, but also because of
    conditional requirements, the dependencies can be different. Then, it is necessary to create a lockfile for every different 
    configuration/profile. 

Base lockfiles
--------------

But what if between both commands, the new ``pkga/0.2@user/testing`` version was created? Although this is unlikely in this
example, because everything is local, it is a possibility if ``pkga`` was in a server, and someone (or CI), upload the new
version while we are running the above commands.

Conan proposes a "base" lockfile, defined by the ``--base`` argument, that will capture only the versions and topology of the
graph, but not the package-ids:

.. code-block:: bash

    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb.lock --base

Lets inspect the *locks/pkgb.lock* lockfile:

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


Using the "base" *locks/pkgb.lock* lockfile, now we can obtain a new lockfile for both debug and release configurations, and
it is guaranteed that both will use the ``pkga/0.1@user/testing`` dependency, and not the new one:

.. code-block:: bash

    $ cd pkgb
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile=locks/pkgb.lock --lockfile-out=locks/pkgb_debug.lock -s build_type=Debug
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile=locks/pkgb.lock --lockfile-out=locks/pkgb_release.lock

Now, we will have 2 lockfiles, *locks/pkgb_debug.lock* and *locks/pkgb_release.lock*. Each one will lock different profiles and different package-id
of ``pkga/0.1@user/testing``.


Locked configuration
--------------------

The lockfiles store the effective configuration, settings, options, resulting from the used profiles and command line arguments.
That configuration arguments can be passed to the ``conan lock create`` command, but not when using lockfiles. For example:

.. code-block:: bash

    $ mkdir build && cd build
    $ conan install .. --lockfile=../locks/pkgb_debug.lock -s build_type=Debug
    ERROR: Cannot use profile, settings, options or env 'host' when using lockfile

results in an error, because the *locks/pkgb_debug.lock* already stores the ``settings.build_type`` and passing it in the command line
could only result in inconsistencies and errors.

.. important::

    Lockfiles store the full effective profile configuration. It is not possible to pass configuration, settings, options or 
    profile arguments when using lockfiles (only when creating the lockfiles)

With the two captured lockfiles, now we can locally build and run our ``pkgb`` application for both configurations, guaranteeing
the dependency to ``pkga/0.1@user/testing``:

.. code-block:: bash

    $ conan install .. --lockfile=../locks/pkgb_release.lock" 
    $ cmake ../src -G "Visual Studio 15 Win64"
    $ cmake --build . --config Release
    $ ./bin/greet
    HelloA 0.1 Release
    HelloB Release!
    Greetings Release!
    $ conan install .. --lockfile=../locks/pkgb_debug.lock" 
    $ cmake --build . --config Debug
    $ ./bin/greet
    HelloA 0.1 Debug
    HelloB Debug!
    Greetings Debug!

We can again create the ``pkgb`` package for both configurations:

.. code-block:: bash

    $ conan create . user/testing --lockfile=locks/pkgb_release.lock --lockfile-out=locks/pkgb_release.lock
    $ conan create . user/testing --lockfile=locks/pkgb_debug.lock --lockfile-out=locks/pkgb_debug.lock