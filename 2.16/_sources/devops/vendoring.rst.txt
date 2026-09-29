.. _devops_vendoring:

Vendoring dependencies in Conan packages
========================================

.. include:: ../common/experimental_warning.inc

From Conan 2.4 it is possible to create and use Conan packages that completely vendor their dependencies,
that is, they completely hide and isolate their dependencies from their consumers. This can be useful
in some different cases:

- When sharing Conan packages with other organizations which vendor (copy, embed or link) the dependencies,
  so it is not necessary for the consumers of their packages to have access to those dependencies and the
  intention is that they always use the shared precompiled binaries.
- To introduce a hard decoupling between parts of a project.

To make a package vendor its dependencies, define in its recipe the following attribute:

.. code-block:: bash


   class MyPkg(ConanFile):
      name = "mypkg"
      version = "0.1"

      vendor = True

      requires = "somedep/1.2"


When we have this recipe, we can create its binaries with a normal ``conan create .``.
But when we use this package as a requirement for other packages, its dependencies will be fully invisible.
The graph will not even expand the ``somedep/1.2`` requirement. This dependency doesn't even need to be available
in the remotes for the consumers, it will not be checked.

Some important notes:

- A package that vendors its dependencies is intended to be consumed always in binary form.
- The dependencies of a vendoring package always form a fully private and isolated dependency graph, decoupled from
  the rest of the dependency graph that uses this package.
- It is the responsibility of the vendoring package and its users to guarantee that vendored dependencies do not
  collide. If a vendoring package vendors for example ``libssl.a`` as a static library doing a regular copy of
  it in its package, and there is another package in the graph that also provides ``libssl``, there will be a
  conflict that Conan cannot detect as ``libssl.a`` is vendored as an internal implementation detail of the package,
  but not explicitly modeled. Mechanisms like ``provides`` can be used for this purpose, but it is the responsibility
  of the recipe authors to take it into account.
- The ``package_id`` of a package that defines ``vendor=True`` is fully independent of its dependencies. The
  dependencies versions will never affect the ``package_id`` of the vendoring package, so it is important
  to note that the version of the vendoring package represents a full private dependency graph.
- The regular ``default_options`` or options values definitions from consumer ``conanfile.py`` recipes do not
  propagate over vendoring packages, as they don't even expand their dependencies.
- If a vendoring package binary is missing and/or the user request to build such a package from sources, Conan
  will fail, raising an error that it is not possible to build it.
- To allow the expansion of the private dependency the ``tools.graph:vendor=build`` configuration can be activated.
  If that is the case, the private dependency graph of the package will be computed and expanded and the package
  will be allowed to build.
