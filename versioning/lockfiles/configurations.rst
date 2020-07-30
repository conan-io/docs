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

    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_release.lock
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_debug.lock -s build_type=Debug
        

.. important::

    The dependency graph is different for each different configuration/profile. Not only the package-ids, but also because of
    conditional requirements, the dependencies can be different. Then, it is necessary to create a lockfile for every different 
    configuration/profile. 


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
