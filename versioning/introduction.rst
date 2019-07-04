.. _versioning_introduction:

Introduction to versioning
==========================

Versioning approaches
---------------------

Fixed versions
++++++++++++++

This is the standard, direct way to specify dependencies versions, with their exact
version, for example in a *conanfile.py* recipe:

.. code-block:: python

    requires = "zlib/1.2.11@conan/stable"

When doing a :command:`conan install`, it will try to fetch from the remotes exactly
that *1.2.11* version.

This method is nicely explicit and deterministic, and is probably the most used one.
As a possible disadvantage, it requires the consumers to explicitly modify the recipes
to use updated versions, which could be tedious or difficult to scale for large projects
with many dependencies, in which those dependencies are frequently modified, and
it is desired to move the whole project forward to those updated dependencies.

Version ranges
++++++++++++++

A *conanfile* can specify a range of valid versions that could be consumed, using brackets:

..  code-block:: python

      requires = "pkg/[>1.0 <1.8]@user/stable"

When a :command:`conan install` is executed, it will check in the local cache first and if
not in the remotes what ``pkg`` versions are available and will select the latest one
that satisfies the defined range.

By default, it is less deterministic, one ``conan install`` can resolve to ``pkg/1.1`` and
then ``pkg/1.2`` is published, and a new ``conan install`` (by users, or CI), will automatically
pick the newer 1.2 version, with different results. On the other hand it doesn't require
changes to consumer recipes to upgrade to use new versions of dependencies.

It is also true that the *semver* definition that comes from other programming languages
doesn't fit that well to C and C++ packages, because of different reasons, because of 
open source libraries that don't closely follow the semver specification, but also because
of the ABI compatibility issues and compilation model that is so characteristic of C and C++ binaries.

Read more about it in :ref:`version_ranges` section.

Package alias
+++++++++++++

It is possible to define a "proxy" package that references another one, using the syntax:

.. code-block:: python

    from conans import ConanFile

    class AliasConanfile(ConanFile):
        alias = "pkg/0.1@user/testing"

This package creation can be automatically created with the :ref:`conan_alias` command, that
can for example create a ``pkg/latest@user/testing`` alias that will be pointing to that
``pkg/0.1@user/testing``. Consumers can define ``requires = "pkg/latest@user/testing"`` and
when the graph is evaluated, it will be directly replaced by the ``pkg/0.1`` one. That is,
the ``pkg/latest`` package will not appear in the dependency graph at all.

This is also less deterministic, and puts the control on the package creator side, instead of
the consumer (version ranges are controlled by the consumer). Package creators can control
which real versions will their consumers be using. This is probably not the recommended way
for normal dependencies versions management.


Package revisions
+++++++++++++++++

TODO 

Read more about :ref:`package_revisions`


Versions conflicts and overrides
--------------------------------

TODO:
- The problem of diamonds and version conflicts
- How overrides work

How versions of dependencies affect binary compatibility
--------------------------------------------------------

TODO

Read more about :ref:`define_abi_compatibility`

