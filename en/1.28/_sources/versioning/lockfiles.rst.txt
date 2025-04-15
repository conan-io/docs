.. _versioning_lockfiles:

Lockfiles
-------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


Lockfiles are files that store the information of a dependency graph, including the
exact versions, revisions, options, and configuration of that dependency graph. These
files allow for later achieving reproducible results, and installing or using the exact
same dependencies even when the requirements are not fully reproducible, for example when using
version ranges or using package revisions.


.. toctree::
   :maxdepth: 2

   lockfiles/introduction
   lockfiles/configurations
   lockfiles/build_order
   lockfiles/ci