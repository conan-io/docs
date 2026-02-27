.. _versioning_lockfiles_introduction:

Introduction
============

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


Let's introduce lockfiles by example, with 2 packages, package ``pkgb`` that depends on  package ``pkga``.

.. note::

    The code used in this section, including a *build.py* script to reproduce it, is in the
    examples repository: https://github.com/conan-io/examples. You can go step by step
    reproducing this example while reading the below documentation.

    .. code:: bash

        $ git clone https://github.com/conan-io/examples.git
        $ cd features/lockfiles/intro
        # $ python build.py only to run the full example, but better go step by step

Locking dependencies
--------------------

This example uses ``full_version_mode``, that is, if a package changes any part of its version, its consumers will
need to build a new binary because a new ``package_id`` will be computed. This example will use version ranges, and
it is not necessary to have revisions enabled. It also do not require a server, everything can be reproduced locally.


.. code-block:: bash

    $ conan config set general.default_package_id_mode=full_version_mode


Let's start by creating from the recipe and source in the ``pkga`` folder, a first ``pkg/0.1@user/testing``
package in our local cache:

.. code-block:: bash

    $ conan create pkga pkga/0.1@user/testing


Now we want to start developing and testing the code for ``pkgb``, but we want to create a "snapshot" of the
dependency graph, to isolate our development from possible changes (note that the recipe in *pkgb/conanfile.py*
contains a require like ``requires = "pkga/[>0.0]@user/testing"``).


.. code-block:: bash

    $ cd pkgb
    $ conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_deps.lock


This will create a *pkgb_deps.lock* file in the *locks* folder. Note that we have passed the user and channel of the future
package that we will create as ``--user=user --channel=testing``.

Let's have a look at the lockfile:

.. code-block:: json

    {
        "graph_lock": {
            "nodes": {
                "0": {
                    "ref": "pkgb/0.1@user/testing",
                    "options": "shared=False",
                    "requires": ["1"],
                    "path": "..\\conanfile.py",
                    "context": "host"
                },
                "1": {
                    "ref": "pkga/0.1@user/testing",
                    "options": "",
                    "package_id": "4024617540c4f240a6a5e8911b0de9ef38a11a72",
                    "prev": "0",
                    "context": "host"
                }
            },
            "revisions_enabled": false
        },
        "version": "0.4",
        "profile_host": "[settings]\narch=x86_64\narch_build=x86_64\nbuild_type=Release\ncompiler=Visual Studio\ncompiler.runtime=MD\ncompiler.version=15\nos=Windows\nos_build=Windows\n[options]\n[build_requires]\n[env]\n"
    }


We can see the ``pkga/0.1@user/testing`` dependency in the lockfile, together with its ``package_id``. This
dependency is fully locked. The ``pkgb/0.1@user/testing`` doesn't have a ``package_id`` yet, because so far it
is just a local *conanfile.py* as a consumer, not a package. But the ``user/testing`` user and channel are already defined.

It is important to note that the *pkgb_deps.lock* lockfile contains the current ``profile`` for the current configuration.

At this moment we have captured the dependency graph for ``pkgb``. Now, it would be possible that a new version
of ``pkga`` is created:


.. code-block:: bash

    $ cd ..
    # The recipe generates different package code depending on the version, automatically
    $ conan create pkga pkga/0.2@user/testing

If now we install and build our code in ``pkgb`` we would get:

.. code-block:: bash

    $ mkdir pkgb/build
    $ cd pkgb/build
    $ conan install ..
    > ... pkga/0.2@user/testing from local cache - Cache
    # Example for VS, use your compiler here
    $ cmake ../src -G "Visual Studio 15 Win64"
    $ cmake --build . --config Release
    $ ./bin/greet
    HelloA 0.2 Release
    HelloB Release!
    Greetings Release!

But as explained above, the purpose of the lockfile is to capture the dependencies and use them later.
Let's pass the lockfile as an argument to guarantee the usage of the locked ``pkga/0.1@user/testing`` dependency:

.. code-block:: bash

    $ conan install .. --lockfile=../locks/pkgb_deps.lock
    > ... pkga/0.1@user/testing from local cache - Cache
    $ cmake ../src -G "Visual Studio 15 Win64"
    $ cmake --build . --config Release
    $ ./bin/greet
    HelloA 0.1 Release
    HelloB Release!
    Greetings Release!

That's it. We managed to depend on ``pkga/0.1@user/testing`` instead of the ``pkga/0.2@user/testing`` although the later
satisfies the version range and is available in the cache. Using the same dependency was possible because we used the information stored in the lockfile.


Immutability
------------

A core concept of lockfiles is their immutability and the integrity of its data:

.. important::

    The information stored in a lockfile cannot be changed. Any attempt to modify locked data will result in
    an error.

For example, if now we try to do a :command:`conan install` that also builds ``pkga`` from source:

.. code-block:: bash

    $ conan install .. --lockfile=../locks/pkgb_deps.lock --build=pkga
    ERROR: Cannot build 'pkga/0.1@user/testing' because it is already locked in the input lockfile

It is an error, because the ``pkga/0.1@user/testing`` dependency was fully locked. When the lockfile was created, the
``pkga/0.1@user/testing`` was found, including a binary, and that information was stored. Everytime this lockfile is
used, it assumes this package and binary exist and it will try to get them, but it will never allow to re-build, because
that can violate the integrity of the lockfile. For example, if we were using ``package_revision_mode``, a new binary
of ``pkga`` would produce new package-ids of all its consumers, that will not match the package-ids stored in the lockfile.

It is possible though to control what is being locked with the ``--build`` argument provided to the :command:`conan lock create`
command.

The same principle applies if we try to create a package for ``pkgb` and it tries to alter the user and channel ``user/testing``
that were provided at the time of the :command:`conan lock create` command used above.

.. code-block:: bash

    $ cd ..
    $ conan create . user/stable --lockfile=locks/pkgb_deps.locked
    ERROR: Attempt to modify locked pkgb/0.1@user/testing to pkgb/0.1@user/stable

Again, it is important to keep the integrity. Package recipes can have conditional or parameterized dependencies, based on
user and channel for example. If we try to create the ``pkgb`` package with different user and channel, it could result in
a different dependency graph, totally incompatible with the one captured in the lockfile. If ``pkgb/0.1@user/testing`` was stored in
the lockfile, any command using this lockfile must respect and keep it without changes.

.. note::

    A package in a lockfile is fully locked if it contains a ``prev`` (package revision) field defined.
    Fully locked packages cannot be built from sources. Partially locked packages do not contain a ``prev``
    defined. They lock the reference and the package-id, and they can be built from sources.


Reproducibility
---------------

That doesn't mean that a lockfile cannot evolve at all. Using the :command:`--lockfile` argument, we are able to create
``pkgb/0.1@user/testing`` guaranteeing it is being created depending on ``pkga/0.1@user/testing``. Additionally, if we use the
:command:`--lockfile-out` argument, we can obtain an updated version of the lockfile:

.. code-block:: bash

    $ conan create . user/testing --lockfile=locks/pkgb_deps.lock --lockfile-out=locks/pkgb.lock


And if we inspect the new *locks/pkgb.lock* file:

.. code-block:: text

    {
        ...
        "0": {
            "ref": "pkgb/0.1@user/testing",
            "options": "shared=False",
            "package_id": "2418b211603ca0a3858d9dd1fc1108d54a4cab99",
            "prev": "0",
            "modified": true,
            "requires": ["1"],
            "context": "host"
        }
        ...
    }

It can be appreciated in *locks/pkgb.lock* that now ``pkgb/0.1@user/testing`` is fully locked, as a package (not a local *conanfile.py*),
and contains a ``package_id``. So if we try to use this new file for creating the package again, it will error,
as a package that is fully locked cannot be rebuilt:


.. code-block:: bash

    $ conan create . user/testing --lockfile=locks/pkgb.lock
    ERROR: Attempt to modify locked pkgb/0.1@user/testing to pkgb/0.1@user/testing


But we can reproduce the same set of dependencies and the creation of ``pkgb``, using the *pkgb_deps.lock* lockfile:

.. code-block:: bash

    $ conan create . user/testing --lockfile=locks/pkgb_deps.lock # OK


The *pkgb.lock* can be used later in time to install the ``pkgb`` application (the ``pkgb`` *conanfile.py* contains a ``deploy()``
method for convenience for this example), and get the same package and dependencies:

.. code-block:: bash

    $ cd ..
    $ mkdir consume
    $ cd consume
    $ conan install pkgb/0.1@user/testing --lockfile=../pkgb/locks/pkgb.lock
    $ ./bin/greet
    HelloA 0.1 Release
    HelloB Release!
    Greetings Release!

As long as we have the *pkgb.lock* lockfile, we will be able to robustly reproduce this install, even if the packages were
uploaded to a server, if there are new versions that satisfy the version ranges, etc.


.. important::

    All the examples and documentation of this section is done with version ranges and revisions disabled.
    Lockfiles also work and can lock both recipe and package revisions, with the same behavior as
    version-ranges. All is necessary is to enable revisions. The only current limitation is that the local
    cache cannot store more than one revision at a time, but that is a limitation of the cache and unrelated
    to lockfiles.
