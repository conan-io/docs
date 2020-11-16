.. _versioning_lockfiles:

Lockfiles
-------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


Lockfiles are files that store the information of a dependency graph, including the
exact versions, revisions, options, and configuration of that dependency graph. These
files allow for achieving reproducible results later, and installing or using the exact
same dependencies even when the requirements are not fully reproducible, for example when using
version ranges or using package revisions.

Overview
+++++++++++++

There are two principale type of Lockfiles, configuration specific and base, which enable 
various workflows. The mechanism behind configuration specific Lockfiles is outline in the 
:ref:`Introduction<versioning_lockfiles_introduction>` along with how they garantee 
reproducible builds and prevent mutations. Base lockfiles are ideal when the dependency graph, 
limited to version and revision, must be replicated through :ref:`multiple configurations<versioning_lockfiles_configurations>`.


.. toctree::
   :maxdepth: 2

   lockfiles/introduction
   lockfiles/configurations
   lockfiles/evolving
   lockfiles/build_order
   lockfiles/ci

Minimal example
+++++++++++++++++++

Given a generic ``pkg`` with several transitive dependencies that may be changed upstream, it may 
be desireable to lock the dependency graph for reproduciblity.

.. code-block:: bash

    $ cd pkg
    $ conan lock create conanfile.py --lockfile-out=locks/base.lock --base

Now before running the ``conan install`` or ``conan create`` processes, a configuration specific lock 
can be generated for that set of options, settings, and/or host.

.. code-block:: bash

    $ cd pkg
    $ conan lock create conanfile.py --lockfile=locks/base.lock --lockfile-out=locks/debug.lock -s build_type=Debug
    $ conan lock create conanfile.py --lockfile=locks/base.lock --lockfile-out=locks/release.lock
    $ conan create . --lockfile=locks/debug.lock # no need to repeate settings
    ...
