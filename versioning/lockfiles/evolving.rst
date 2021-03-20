.. _versioning_lockfiles_evolving:

Evolving lockfiles
==================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

As described before, lockfiles are immutable, they cannot change the information they contain.
If some install or create command tries to change some data in a lockfile, it will error. This
doesn't mean that operations on lockfiles cannot be done, as it is possible to create a new
lockfile from an existing one. We have already done this, obtaining a full lockfile for a
specific configuration from an initial "base" lockfile.


There are several scenarios you might want to create a new lockfile from an existing one.


Deriving a partial lockfile
---------------------------

Lets say that we have an application ``app/1.0`` that depends on ``libc/1.0`` that depends on ``libb/1.0``
that finally depends on ``liba/1.0``. We could capture a "base" lockfile from it, and then several full
lockfiles, one per configuration:

.. code:: bash

    $ conan lock create --reference=app/1.0@ --base --lockfile-out=app_base.lock
    $ conan lock create --reference=app/1.0@ --lockfile=app_base.lock -s build_type=Release --lockfile-out=app_release.lock
    $ conan lock create --reference=app/1.0@ --lockfile=app_base.lock -s build_type=Debug --lockfile-out=app_debug.lock


Now a developer wants to start testing some changes in ``libb``, using the same dependencies versions defined
in the lockfile. As ``libb`` is locked, it will not be possible to create a new version ``libb/1.1`` or build
a new binary for it with the existing lockfiles. But we can create a new lockfile for it in different ways.
For example, we could derive directly from the *app_release.lock* and *app_debug.lock* lockfiles:

.. code:: bash

    $ git clone <libb-repo> && cd libb
    $ conan lock create conanfile.py --lockfile=app_release.lock --lockfile-out=libb_deps_release.lock
    $ conan lock create conanfile.py --lockfile=app_debug.lock --lockfile-out=libb_deps_debug.lock

This will create partial lockfiles, only for ``libb`` dependencies, i.e. locking ``liba/1.0``, that can be used
while installing, building and testing ``libb``.

But it is also possible to derive a new "base" profile from *app_base.lock* only for libb dependencies, and then
compute from it the configuration specific profiles.

These partial lockfiles will be smaller than the original app lockfiles, not containing information at all about
``app`` and ``libc``.

Unlocking packages with --build
+++++++++++++++++++++++++++++++

It is also possible to derive a partial lockfile for ``libb/1.0`` without cloning the ``libb`` repository, directly with:

.. code:: bash

    $ conan lock create --reference=libb/1.0 --lockfile=app_release.lock --lockfile-out=libb_release.lock
    $ conan lock create --reference=libb/1.0 --lockfile=app_debug.lock --lockfile-out=libb_debug.lock

These new lockfiles could be used to install the ``libb/1.0`` package, without building it, but if we tried to
build it from sources, it will fail:

.. code:: bash

    $ conan install libb/1.0@ --lockfile=libb_release.lock # Works
    $ conan install libb/1.0@ --build=libb --lockfile=libb_release.lock # Fails, libb is locked

The second scenario fails. This is because when the *app_release.lock* lockfile was captured, it completely locked all the
information (including ``libb/1.0``'s package revision). If we try to build a new binary, the lock protection will
raise. If we want to "unlock" the binary package revision, we need to tell the lockfile when we are capturing such
lockfile, that we plan to build it, with the :command:`--build` argument:

.. code:: bash

    # Note the --build=libb argument
    $ conan lock create --reference=libb/1.0 --build=libb --lockfile=app_release.lock --lockfile-out=libb_release.lock
    # This will work, building a new binary
    $ conan install libb/1.0@ --build=libb --lockfile=libb_release.lock --lockfile-out=libb_release2.lock

As usual, if you are building a new binary, it is desired to provide a :command:`--lockfile-out=libb_release2.lock` to capture such
a new binary package revision in the new lockfile.


Integrating a partial lockfile
------------------------------

This would be the opposite flow. Lets take the previous *libb_deps_release.lock* and *libb_deps_debug.lock*
lockfiles and create new ``libb/1.1`` packages with it, and obtaining new lockfiles:

.. code:: bash

    # in the libb source folder
    $ conan  create . --lockfile=libb_deps_release.lock --lockfile-out=libb_release.lock
    $ conan  create . --lockfile=libb_deps_debug.lock --lockfile-out=libb_debug.lock

These lockfiles will be containing locked information to ``liba/1.0`` and a new ``libb/1.1`` version.
Now we would like to check if ``app/1.0`` will pick this new version, and in case it is used, we would
like to rebuild whatever is necessary (that is part of the next CI section).

.. important::

    It is not possible to pick the old *app_base.lock*, *app_release.lock* or *app_debug.lock*
    lockfiles and inject the new ``libb/1.1`` version, as this would be violating the integrity of the lockfile.
    Nothing guarantees that the downstream packages will effectively use the new version, as it might fall outside
    the valid range defined in ``libc/1.0``, for example. Also, downstream consumers ``app/1.0`` and ``libc/1.0``
    could result in different package-ids as a result of having a new dependency, and this goes against the
    immutability of the lockfile data, as the package-ids for them would be already locked.

Let's create new lockfiles that will use the existing ``libb_debug.lock`` and ``libb_release.lock`` information if possible:

.. code:: bash

    $ conan lock create --reference=app/1.0@ --lockfile=libb_release.lock --lockfile-out=app_release.lock
    $ conan lock create --reference=app/1.0@ --lockfile=libb_debug.lock --lockfile-out=app_debug.lock

This will create new *app_release.lock* and *app_debug.lock* that will have both ``libb/1.1`` and ``liba/1.0``
locked. If for some reason, ``libc/1.0`` had fixed a ``requires = "libb/1.0"``, then the resulting lockfile
would resolve and lock ``libb/1.0`` instead. The ``build-order`` command (see next section) will tell us that there
is nothing to build, as it is effectively computing the same lockfile that existed before. It is also
possible, and a CI pipeline could do it, to directly check that ``libb/1.1`` is defined inside the new lockfiles.
If it is not there, it means that it didn't integrate, and nothing needs to be done downstream.
