.. _versioning_lockfiles:

Lockfiles
=========

Lockfiles are files that store the information of a dependency graph, including the
exact versions, revisions, options, and configuration of that dependency graph. As 
they depend on the configuration, and the dependency graph can change with every 
different configuration, there will be one lockfile for every configuration.

Lockfiles are useful for achieving deterministic builds, even if the dependency 
definitions in conanfile rcipes are not fully deterministic, for example when using
version ranges or using package revisions.

Commands
--------

conan graph lock
++++++++++++++++

This command will generate a *conan.lock* file. It behaves like :command:`conan install` command,
(this will also generate a lockfile by default), but without needing to actually install the
binaries, so it will be faster. In that regard it is equal to :command:`conan info` that can also
generate a lockfile, but the problem with :command:`conan info -if=.` is that it does not allow to 
specify a profile or settings.

conan install/create/export/info --lockfile
+++++++++++++++++++++++++++++++++++++++++++

If the command builds a package, it can modify its reference. Even if teh version is not changed,
if something in the recipe changes, it will get a new recipe revision RREV and if the package is
built from sources again, it might end with a new, different package revision PREV. Those changes
will be updated in the *conan.lock* lockfile, and the package will be marked as "modified".

conan graph update-lock
+++++++++++++++++++++++

Update the current lockfile with the information of the second lockfile. Only the nodes marked
as "modified" will be updated. Trying to update to the current lockfile one node that has already
been "modified" will result in an error.

conan graph build-order
+++++++++++++++++++++++


How to use lockfiles in CI
--------------------------

