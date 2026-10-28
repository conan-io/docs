.. _tutorial_versioning:


Versioning
==========

This section of the tutorial introduces several concepts about versioning of packages.

First, explicit version updates and how to define versions of packages is explained.

Then, it will be introduced how ``requires`` with version ranges can 
help to automate updating to the latest versions.

There are some situations when recipes or source code are changed, but the version of the
package is not increased. For those situations, Conan uses automatic ``revisions`` to 
be able to provide traceability and reproducibility of those changes.

Lockfiles are a common mechanism in package managers to be able to reproduce the same
dependency graph later in time, even when new versions or revisions of dependencies are uploaded.
Conan also provides lockfiles to be able to guarantee this reproducibility.

Finally, when different branches of a dependency graph ``requires`` different versions of the
same package, that is called a "version conflict". The tutorial will also introduce these
errors and how to address them.


.. toctree::
   :maxdepth: 2
   :caption: Table of contents

   versioning/versions
   versioning/version_ranges
   versioning/revisions
   versioning/lockfiles
   versioning/conflicts
