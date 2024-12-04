.. _versioning_lockfiles_ci:

Lockfiles in Continuous Integration
===================================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


This section provides an example of application of the **lockfiles** in a Continuous Integration
case. It doesn't aim to present a complete solution or the only possible one, depending on the
project, the team, the requirements, the constraints, etc., other approaches might be recommended.

In this section we are going to use the same packages than in the previous one, defining this
 dependency graph.

.. image:: conan_lock_build_order.png
   :height: 200 px
   :width: 400 px
   :align: center


The example scenario is a developer doing some changes in ``libb``, that include bumping the
version to ``libb/0.2``. We will structure the CI in two parts:

- Building ``libb/0.2@user/testing`` to check that it is working fine.
- Building the downstream applications ``app1/0.1@user/testing`` and ``app2/0.2@user/testing``
  to check if they build correctly, or if they are broken by those changes.

.. note::

    The code used in this section, including a *build.py* script to reproduce it, is in the
    examples repository: https://github.com/conan-io/examples. You can go step by step
    reproducing this example while reading the below documentation.

    .. code:: bash

        $ git clone https://github.com/conan-io/examples.git
        $ cd features/lockfiles/ci
        # $ python build.py only to run the full example, but better go step by step


The example in this section uses ``full_version_mode``, that is, if a package changes any part of its version, its consumers will
need to build a new binary because a new ``package_id`` will be computed.

.. code:: bash

    $ conan config set general.default_package_id_mode=full_version_mode

This example will use version ranges, and it is not necessary to have revisions enabled. It also do not require
a server, everything can be reproduced locally, although the usage of different repositories will be introduced.


Repositories
------------
When a developer does some changes, the CI wants to build those changes, create packages, and check if everything
is ok. But while checking it, it is better to not pollute the main Conan remote repository with temporary packages
until we are fully sure that it is not breaking anything. So we could use 2 repositories:

- ``conan-develop``: this would be the team/project reference repository. Developers and CI will use this by default to
  retrieve Conan packages with precompiled binaries. Similarly to a git "develop" branch, it could be assumed that
  the packages in this repository work correctly, have been tested before being put there. It could also be expected
  that the repository contains pre-compiled binaries, so building from sources shouldn't be necessary.
- ``conan-build``: a repository mainly for CI purposes. When CI is creating packages in a pipeline, it can put those
  packages in this repository, so they can still be used in the CI pipelines, be fetched by some build agents to
  build other packages. These temporary packages will not disrupt the operations and usage of ``conan-develop``
  repository used by other CI jobs and developers.



Let's create the first version of the packages, for both Debug and Release configurations:

.. code:: bash

    $ conan create liba liba/0.1@user/testing -s build_type=Release
    $ conan create libb libb/0.1@user/testing -s build_type=Release
    $ conan create libc libc/0.1@user/testing -s build_type=Release
    $ conan create libd libd/0.1@user/testing -s build_type=Release
    $ conan create app1 app1/0.1@user/testing -s build_type=Release
    $ conan create app2 app2/0.1@user/testing -s build_type=Release
    $ conan create liba liba/0.1@user/testing -s build_type=Debug
    ...


Now let's say that one developer does some change to ``libb``:

.. code:: bash

    $ vim libb/conanfile.py
    # do some changes and save

These changes are local in this example, in reality they will be typically in the form of a Pull Request,
wanting to merge those changes in the main "develop" branch.


Package pipeline
----------------
The first thing the CI will do is to build ``libb/0.2@user/testing`` package, containing the developer
changes, for different configurations. As we want to make sure that all different configurations are
built with the same versions of the dependencies, the first thing is to capture a "base" lockfile of
the dependencies of ``libb``:

.. code:: bash

    $ cd libb
    $ conan lock create conanfile.py --name=libb --version=0.2 --user=user --channel=testing
      --lockfile-out=../locks/libb_deps_base.lock --base

This will capture the *libb_deps_base.lock* file with the versions of ``libb`` dependencies, in this case
``liba/0.1@user/testing``. Now that we have this file, new versions of ``liba`` could be created, but they
will not be used:

.. code:: bash

    $ cd ..
    $ conan create liba liba/0.2@user/testing

We want to test the changes for several different configurations, so the first step would be to derive a new
lockfile for each configuration/profile from the *libb_deps_base.lock*:

.. code:: bash

    $ cd libb

    # Derive one lockfile per profile/configuration
    $ conan lock create conanfile.py --name=libb --version=0.2
      --user=user --channel=testing --lockfile=../locks/libb_base.lock
      --lockfile-out=../locks/libb_deps_debug.lock -s build_type=Debug
    $ conan lock create conanfile.py --name=libb --version=0.2
      --user=user --channel=testing --lockfile=../locks/libb_base.lock
      --lockfile-out=../locks/libb_deps_release.lock

    # Create the package binaries, one with each lockfile
    $ conan create . libb/0.2@user/testing --lockfile=../locks/libb_deps_release.lock
    $ conan create . libb/0.2@user/testing --lockfile=../locks/libb_deps_debug.lock

.. note::

    It is important to note that it is not necessary to build all configurations in this build agent.
    One of the advantages of using lockfiles is that the build can be delegated to other agents,
    as long as they get the right commit of ``libb`` repo and the lockfile, they can build
    the desired package with the right dependencies.


Once everything is building ok, and ``libb/0.2@user/testing`` package is created correctly for all profiles,
we want to check if this new version can be integrated safely in its consumers. When using revisions (not
this example), it is important to capture the recipe revision, and lock it too. We can capture the recipe
revision doing an export, creating a new *libb_base.lock* lockfile:

.. code:: bash

    $ conan export . libb/0.2@user/testing --lockfile=../locks/libb_deps_base.lock
      --lockfile-out=../locks/libb_base.lock


Products pipeline
-----------------
There is an important question to be addressed: **when a package changes, what other packages
consuming it should be rebuild to account for this change?**. The problem might be harder than
it seems at first sight, or from the observation of the graph above. It shows that ``libd/0.1``
has a dependency to ``libb/0.1``, does it means that a new ``libb/0.2`` should produce a re-build
of ``libd/0.1`` to link with the new version? Not always, if ``libd`` had a pinned dependency
and not a version range, it will never resolve to the new version, and then it doesn't and it
cannot be rebuil unless some developer do some changes to ``libd`` and bump the requirement.

In this example, ``libd`` contains a version range, and if we evaluate it, we will see that the
new ``libb/0.2`` version lies within the range, and then yes, it needs a new binary to be built,
otherwise our repository of packages will have missing binaries.

One important problem is the combinatoric explosion that happens downstream. Projects evolve and
packages will eventually have many versions and even many revisions. In our example, we could
have in our repository many ``libd/0.0.1``, ``libd/0.0.2``, ..., ``libd/0.0.34`` versions, all of
them with a requirement to ``libb``. Each one could be in turn consumed by multiple ``app1`` versions.

We could think to consider as consumer only the latest version of ``libd``. But it is also totally
possible that some developer has already uploaded a ``libd/2.0`` version, with a breaking new API,
aimed for the next major version of ``app1``.

So the only alternative to be both efficient and have a robust Continuous Integration of changes in
our core "products" is to explictly define those "products". In our case we will define that our
products are ``app1/0.1@user/testing`` and ``app2/0.1@user/testing``. This product definition could
change as we keep doing releases of our products to our customers.

The first step in the products pipeline would be to capture the lockfiles for the different configurations
we want to build for our products. As explained above, we can first capture a "base" lockfile of
``app1/0.1@user/testing``, using the previous *libb_base.lock*, to make sure that we are using the locked
versions for both ``libb/0.2@user/testing`` and ``liba/0.1@user/testing``, as this was the snapshot of
existing versions when the CI pipeline started, even if later a ``liba/0.2@user/testing`` was created.


.. code:: bash

    $ conan lock create --reference=app1/0.1@user/testing --lockfile=locks/libb_base.lock
      --lockfile-out=locks/app1_base.lock --base

The *app1_base.lock* lockfile will capture and lock ``libd/0.1@user/testing`` and ``libc/0.1@user/testing``.
Now, even if those packages also got new versions, they will not be used, even if they fit in the version range.
The *app1_base.lock* lockfile can be in turn used to capture complete lockfiles, one per profile/configuration:

.. code:: bash

    $ conan lock create --reference=app1/0.1@user/testing --lockfile=locks/app1_base.lock
      --lockfile-out=locks/app1_release.lock
    $ conan lock create --reference=app1/0.1@user/testing --lockfile=locks/app1_base.lock
      --lockfile-out=locks/app1_debug.lock -s build_type=Debug

The build-order can now be computed, also for each configuration:

.. code:: bash

    $ conan lock build-order locks/app1_release.lock --json=bo_release.json
    [[['libd/0.1@user/testing', 'b03c813b34cfab7a095fd903f7e8df2114e2b858', 'host', '4']],
     [['app1/0.1@user/testing', '15d2c695ed8d421c0d8932501fc654c8083e6582', 'host', '3']]]

    $ conan lock build-order locks/app1_debug.lock --json=bo_debug.json
    [[['libd/0.1@user/testing', '67a26cfbef78ad4905bec085664768c209d14fda', 'host', '4']],
     [['app1/0.1@user/testing', '680239a70c97f93d4d3dba4dec1b148d45ed087a', 'host', '3']]]


The build order tells that we need to build ``libd/0.1@user/testing`` and ``app1/0.1@user/testing``
in that order, for both Release and Debug configurations (again this can also be delegated to other build agents)

That build can be done with command:

.. code:: bash

    $ conan install libd/0.1@user/testing --build=libd/0.1@user/testing --lockfile=locks/app1_release.lock
      --lockfile-out=locks/app1_release_updated.lock

Note that we are creating a new temporary *app1_release_updated.lock* lockfile, that will contain and lock
the binary produced by the build of ``libd``. If this was implemented in CI, the *app1_release.lock* would
be sent to the build agent, and it would return a modified *app1_release_updated.lock*. The way to
integrate this information into the existing lockfile, necessary to keep building other downstream packages
is:

.. code:: bash

    $ conan lock update locks/app1_release.lock locks/app1_release_updated.lock

Now that *locks/app1_release.lock* is updated we could launch in exactly the same way the build of ``app1``:

.. code:: bash

    $ conan install app1/0.1@user/testing --build=app1/0.1@user/testing --lockfile=locks/app1_release.lock
      --lockfile-out=locks/app1_release_updated.lock

The process will be repeated (or it could also run in parallel) for the Debug configuration.

After the ``app1/0.1@user/testing`` product pipeline finishes, then the ``app2/0.2@user/testing`` one will
be started. With this setup and example, it is very important that the products pipelines are ran sequentially,
otherwise it is possible that the same binaries are unnecesarily built more than once.

When the products pipeline finishes it means that the changes proposed by the developer in their Pull Request that
would result in a new ``libb/0.2@user/testing`` package are safe to be merged and will be integrated in our
product packages without problems. When the Pull Request is merged there might be two alternatives:

- The merge is a merge commit, with a different revision and possible different source as the result of a real merge,
  than the source used in this CI job. Then it is necessary to fire again a new job that will build these packages.
- If the merge is a clean fast-forward, then the packages that were built in this job would be valid, and could be
  copied from the repository ``conan-build`` to the ``conan-develop``.