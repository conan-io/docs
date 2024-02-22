.. _tutorial_versioning_lockfiles:

Lockfiles
=========

Lockfiles are a mechanism to achieve reproducible dependencies, even when new versions or revisions
of those dependencies are created.
Let's see it with a practical example, start cloning  the `examples2 repository <https://github.com/conan-io/examples2>`_:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/versioning/lockfiles/intro

In this folder we have a small project, consisting in 3 packages: a ``matrix`` package, emulating some mathematical
library, an ``engine`` package emulating some game engine, and a ``sound32`` package, emulating a sound library for 
some 32bits systems. These packages are actually most empty, they do not build any code, but they are good to learn
the concepts of lockfiles.

.. graphviz::
    :align: center

    digraph lockfiles {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="BT"
        "engine/1.0" -> "matrix/1.0";
        "engine/1.0" -> "sound32/1.0" [label="if arch==x86"];
    }

|

We will start by creating the first ``matrix/1.0`` version:

.. code-block:: bash

    $ conan create matrix --version=1.0

Now we can check in the ``engine`` folder its recipe:

.. code-block:: python

    class Engine(ConanFile):
        name = "engine"
        settings = "arch"

        def requirements(self):
            self.requires("matrix/[>=1.0 <2.0]")
            if self.settings.arch == "x86":
                self.requires("sound32/[>=1.0 <2.0]")

Lets move to the ``engine`` folder and install its dependencies:

.. code-block:: bash

    $ cd engine
    $ conan install .
    ... 
    Requirements
        matrix/1.0#905c3f0babc520684c84127378fefdd0 - Cache
    Resolved version ranges
        matrix/[>=1.0 <2.0]: matrix/1.0

As the ``matrix/1.0`` version is in the valid range, it is resolved and used.
But if someone creates a new ``matrix/1.1`` or ``1.X`` version, it would also be automatically used, because
it is also in the valid range. To avoid this, we will capture a "snapshot" of the current dependencies
creating a ``conan.lock`` lockfile:

.. code-block:: bash

    $ conan lock create .
    $ cat conan.lock
    {
        "version": "0.5",
        "requires": [
            "matrix/1.0#905c3f0babc520684c84127378fefdd0%1675278126.0552447"
        ],
        "build_requires": [],
        "python_requires": []
    }

We can see how the created ``conan.lock`` lockfile contains the ``matrix/1.0`` version
and its revision. But ``sound32/1.0`` is not in the lockfile, because for the default
configuration profile (not ``x86``), this ``sound32`` is not a dependency.

Now, a new ``matrix/1.1`` version is created:

.. code-block:: bash

    $ cd ..
    $ conan create matrix --version=1.1
    $ cd engine

And see what happens when we issue a new ``conan install`` command for the engine:

.. code-block:: bash

    $ conan install .
    # equivalent to conan install . --lockfile=conan.lock 
    ...
    Requirements
       matrix/1.0#905c3f0babc520684c84127378fefdd0 - Cache

As we can see, the new ``matrix/1.1`` was not used, even if it is in the valid range!
This happens because by default the ``--lockfile=conan.lock`` will be used if the
``conan.lock`` file is found. The locked ``matrix/1.0`` version and revision will be
used to resolve the range, and the ``matrix/1.1`` will be ignored.

Likewise, it is possible to issue other Conan commands, and if the ``conan.lock`` is there,
it will be used:

.. code-block:: bash

    $ conan graph info . --filter=requires # --lockfile=conan.lock is implicit
    # display info for matrix/1.0
    $ conan create . --version=1.0 # --lockfile=conan.lock is implicit
    # creates the engine/1.0 package, using matrix/1.0 as dependency
    
If using a lockfile is intended, like in CI, it is better that the argument ``--lockfile=conan.lock`` explicit.


Multi-configuration lockfiles
-----------------------------

We saw above that the ``engine`` has a conditional dependency to the ``sound32`` package, in case the architecture
is ``x86``. That also means that such ``sound32`` package version was not captured in the above lockfile.

Lets create the ``sound32/1.0`` package first, then try to install ``engine``:

.. code-block:: bash

    $ cd ..
    $ conan create sound32 --version=1.0
    $ cd engine
    $ conan install . -s arch=x86 # FAILS!
    ERROR: Requirement 'sound32/[>=1.0 <2.0]' not in lockfile

This happens because the ``conan.lock`` lockfile doesn't contain a locked version for ``sound32``. By default
lockfiles are strict, if we are locking dependencies, a matching version inside the lockfile must be found.
We can relax this assumption with the ``--lockfile-partial`` argument:


.. code-block:: bash

    $ conan install . -s arch=x86 --lockfile-partial
    ...
    Requirements
        matrix/1.0#905c3f0babc520684c84127378fefdd0 - Cache
        sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7 - Cache
    Resolved version ranges
        sound32/[>=1.0 <2.0]: sound32/1.0

This will manage to partially lock to ``matrix/1.0``, and resolve ``sound32`` version range as usual.
But we can do better, we can extend our lockfile to also lock ``sound32/1.0`` version, to avoid
possible disruptions caused by new ``sound32`` unexpected versions:


.. code-block:: bash

    $ conan lock create . -s arch=x86
    $ cat conan.lock
    {                                                                         
        "version": "0.5",                                                     
        "requires": [                                                         
            "sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7%1675278904.0791488",
            "matrix/1.0#905c3f0babc520684c84127378fefdd0%1675278900.0103245"  
        ],                                                                    
        "build_requires": [],                                                 
        "python_requires": []                                                 
    }

Now, both ``matrix/1.0`` and ``sound32/1.0`` are locked inside our ``conan.lock`` lockfile.
It is possible to use this lockfile for both configurations (64bits, and x86 architectures),
having versions in a lockfile that are not used for a given configuration is not an issue,
as long as the necessary dependencies for that configuration find a matching version in it.

.. important::

    Lockfiles contains sorted lists of requirements, ordered by versions and revisions, so
    latest versions and revisions are the ones that are prioritized when resolving against a lockfile.
    A lockfile can contain two or more different versions of the same package, just because different
    version ranges require them. The sorting will provide the right logic so each range resolves to
    each valid versions.
    
    If a version in the lockfile doesn't fit in a valid range, it will not be used. It is not possible
    for lockfiles to force a dependency that goes against what ``conanfile`` requires define, as they 
    are "snapshots" of an existing/realizable dependency graph, but cannot define an "impossible" 
    dependency graph.


Evolving lockfiles
------------------

Even if lockfiles enforce and constraint the versions that can be resolved for a graph, it doesn't
mean that lockfiles cannot evolve. Actually, controlled evolution of lockfiles is paramount to
important processes like Continuous Integration, when the effect of one change in the graph wants
to be tested in isolation of other possible concurrent changes.

In this section we will introduce some of the basic functionality of lockfiles that allows such
evolution.

First, if we would like now to introduce and test the new ``matrix/1.1`` version in our ``engine``, 
without necessarily pulling many other dependencies that could have got new versions too, we could
manually add ``matrix/1.1`` to the lockfile:

.. code-block:: bash

    $ Running: conan lock add --requires=matrix/1.1                              
    $ cat conan.lock  
    {                                                                   
        "version": "0.5",                                                      
        "requires": [                                                          
            "sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7%1675278904.0791488", 
            "matrix/1.1",                                                      
            "matrix/1.0#905c3f0babc520684c84127378fefdd0%1675278900.0103245"   
        ],                                                                     
        "build_requires": [],                                                  
        "python_requires": []                                                  
    }

To be clear: manually adding with ``conan lock add`` is not necessarily a recommended flow, it is
possible to automate the task with other approaches, that will be explained later. This is just
an introduction to the principles and concepts.

The important idea is that now we got 2 versions of ``matrix`` in the lockfile, and ``matrix/1.1``
is before ``matrix/1.0``, so for the range ``matrix/[>=1.0 <2.0]``, the first one (``matrix/1.1``)
would be prioritized. That means that when now the new lockfile is used, it will resolve to
``matrix/1.1`` version (even if a ``matrix/1.2`` or higher version existed in the system):

.. code-block:: bash

    $ conan install . -s arch=x86 --lockfile-out=conan.lock
    Requirements
        matrix/1.1#905c3f0babc520684c84127378fefdd0 - Cache
        sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7 - Cache
    $ cat conan.lock
    {                                                                   
        "version": "0.5",                                                       
        "requires": [                                                           
            "sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7%1675278904.0791488",  
            "matrix/1.1#905c3f0babc520684c84127378fefdd0%1675278901.7527816",   
            "matrix/1.0#905c3f0babc520684c84127378fefdd0%1675278900.0103245"    
        ],                                                                      
        "build_requires": [],                                                   
        "python_requires": []                                                   
    }

Note that now ``matrix/1.1`` was resolved, and it also got its ``revision`` stored in
the lockfile (because ``--lockfile-out=conan.lock`` was passed as argument).

It is true that the former ``matrix/1.0`` version was not used. As said above, having
old versions in the lockfile that are not used is not harmful. However, if we want to 
prune the unused versions and revisions, we could use the ``--lockfile-clean`` for that
purpose:

.. code-block:: bash

    $ conan install . -s arch=x86 --lockfile-out=conan.lock --lockfile-clean
    ...
    Requirements
        matrix/1.1#905c3f0babc520684c84127378fefdd0 - Cache
        sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7 - Cache
    ...
    $ cat conan.lock
    {
        "version": "0.5",
        "requires": [
            "sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7%1675278904.0791488",
            "matrix/1.1#905c3f0babc520684c84127378fefdd0%1675278901.7527816"
        ],
        "build_requires": [],
        "python_requires": []
    }

It is relevant to note that the ``-lockfile-clean`` could remove locked versions in
given configurations. For example, if instead of the above, the ``x86_64`` architecture
is used, the ``--lockfile-clean`` will prune the "unused" ``sound32``, because in that 
configuration is not used. It is possible to evaluate new lockfiles for every different
configuration, and then merge them:

.. code-block:: bash

    $ conan lock create . --lockfile-out=64.lock --lockfile-clean
    $ conan lock create . -s arch=x86 --lockfile-out=32.lock --lockfile-clean
    $ cat 64.lock
    {                                                                                                   
        "version": "0.5",                                                                               
        "requires": [                                                                                   
            "matrix/1.1#905c3f0babc520684c84127378fefdd0%1675294635.6049662"                            
        ],                                                                                              
        "build_requires": [],                                                                           
        "python_requires": []                                                                           
    }             
    $ cat 32.lock                                                                                      
    {                                                                                                   
        "version": "0.5",                                                                               
        "requires": [                                                                                   
            "sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7%1675294637.9775107",                          
            "matrix/1.1#905c3f0babc520684c84127378fefdd0%1675294635.6049662"                            
        ],                                                                                              
        "build_requires": [],                                                                           
        "python_requires": []                                                                           
    }               
    $ conan lock merge --lockfile=32.lock --lockfile=64.lock --lockfile-out=conan.lock         
    $ cat conan.lock                                                                               
    {                                                                                                   
        "version": "0.5",                                                                               
        "requires": [                                                                                   
            "sound32/1.0#83d4b7bf607b3b60a6546f8b58b5cdd7%1675294637.9775107",                          
            "matrix/1.1#905c3f0babc520684c84127378fefdd0%1675294635.6049662"                            
        ],                                                                                              
        "build_requires": [],                                                                           
        "python_requires": []                                                                           
    }                                                                                                   

This multiple-clean + merge operation is not something that developers should do, only CI
scripts, and for some advanced CI flows that will be explained later.


Read more
---------
- It is possible to lock down to package revisions, but this would be not recommended for
  most use cases, and should only be used in extreme and problematic cases.
- Continuous Integrations links.
