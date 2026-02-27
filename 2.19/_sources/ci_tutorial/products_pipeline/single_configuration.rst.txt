Products pipeline: single configuration
=======================================

In this section we will implement a very basic products pipeline, without distributing the build, without using lockfiles or building multiple configurations.

The main idea is to illustrate the need to rebuild some packages because there is a new ``ai/1.1.0`` version that can be integrated by our main products. This new ``ai`` version is in the ``products`` repository, as it was already succesfully built by the "packages pipeline".
Let's start by making sure we have a clean environment with the right repositories defined:

.. code-block:: bash

    # First clean the local "build" folder
    $ pwd  # should be <path>/examples2/ci/game
    $ rm -rf build  # clean the temporary build folder 
    $ mkdir build && cd build # To put temporary files

    # Now clean packages and define remotes
    $ conan remove "*" -c  # Make sure no packages from last run
    # NOTE: The products repo is first, it will have higher priority.
    $ conan remote enable products


Recall that the ``products`` repo has higher priority than the ``develop`` repo. It means Conan will resolve first in the ``products`` repo, if it finds a valid version for the defined version ranges, it will stop there and return that version, without
checking the ``develop`` repo (checking all repositories can be done with ``--update``, but that would be slower and with the right repository ordering, it is not necessary).

As we have already defined, our main products are ``game/1.0`` and ``mapviewer/1.0``, let's start by trying to install and use ``mapviewer/1.0``:


.. code-block:: bash

  $ conan install --requires=mapviewer/1.0
  ...
  Requirements
      graphics/1.0#24b395ba17da96288766cc83accc98f5 - Downloaded (develop)
      mapviewer/1.0#c4660fde083a1d581ac554e8a026d4ea - Downloaded (develop)
      mathlib/1.0#f2b05681ed843bf50d8b7b7bdb5163ea - Downloaded (develop)
  ...
  Install finished successfully

  # Activate the environment and run the executable 
  # Use "conanbuild.bat && mapviewer" in Windows
  $ source conanrun.sh && mapviewer
  ...
  graphics/1.0: Checking if things collide (Release)!
  mapviewer/1.0:serving the game (Release)!


As we can see, ``mapviewer/1.0`` doesn't really depend on ``ai`` package at all, not any version.
So if we install it, we would already have a pre-compiled binary for it and everything works.

But if we now try the same with ``game/1.0``:

.. code-block:: bash

  $ conan install --requires=game/1.0
  ...
  ======== Computing necessary packages ========
  ...
  ERROR: Missing binary: game/1.0:bac7cd2fe1592075ddc715563984bbe000059d4c

  game/1.0: WARN: Cant find a game/1.0 package binary bac7cd2fe1592075ddc715563984bbe000059d4c for the configuration:
  ...
  [requires]
  ai/1.1.0#01a885b003190704f7617f8c13baa630

It will fail, because it will get ``ai/1.1.0`` from the ``products`` repo, and there will be no pre-compiled binary for ``game/1.0`` against this new version of ``ai``. This is correct, ``ai`` is a static library, so we need to re-build ``game/1.0`` against it, let's do it using the ``--build=missing`` argument:

.. code-block:: bash

  $ conan install --requires=game/1.0 --build=missing
  ...
  ======== Computing necessary packages ========
  Requirements
      ai/1.1.0:8b108997a4947ec6a0487a0b6bcbc0d1072e95f3 - Download (products)
      engine/1.0:de738ff5d09f0359b81da17c58256c619814a765 - Build
      game/1.0:bac7cd2fe1592075ddc715563984bbe000059d4c - Build
      graphics/1.0:8b108997a4947ec6a0487a0b6bcbc0d1072e95f3 - Download (develop)
      mathlib/1.0:4d8ab52ebb49f51e63d5193ed580b5a7672e23d5 - Download (develop)

  -------- Installing package engine/1.0 (4 of 5) --------
  engine/1.0: Building from source
  ...
  engine/1.0: Package de738ff5d09f0359b81da17c58256c619814a765 created
  -------- Installing package game/1.0 (5 of 5) --------
  game/1.0: Building from source
  ...
  game/1.0: Package bac7cd2fe1592075ddc715563984bbe000059d4c created
  Install finished successfully

Note the ``--build=missing`` knows that ``engine/1.0`` also needs a new binary as a result of its dependency to the new ``ai/1.1.0`` version. Then, Conan proceeds to build the packages in the right order, first ``engine/1.0`` has to be built, because ``game/1.0`` depends on it. After the build we can list the new built binaries and see how they depend on the new versions:

.. code-block:: bash

  $ conan list engine:*
  Local Cache
    engine
      engine/1.0
        revisions
          fba6659c9dd04a4bbdc7a375f22143cb (2024-09-30 12:19:54 UTC)
            packages
              de738ff5d09f0359b81da17c58256c619814a765
                info
                  ...
                  requires
                    ai/1.1.Z
                    graphics/1.0.Z
                    mathlib/1.0.Z

  $ conan list game:*
  Local Cache
    game
      game/1.0
        revisions
          1715574045610faa2705017c71d0000e (2024-09-30 12:19:55 UTC)
            packages
              bac7cd2fe1592075ddc715563984bbe000059d4c
                info
                  ...
                  requires
                    ai/1.1.0#01a885b003190704f7617f8c13baa630:8b108997a4947ec6a0487a0b6bcbc0d1072e95f3
                    engine/1.0#fba6659c9dd04a4bbdc7a375f22143cb:de738ff5d09f0359b81da17c58256c619814a765
                    graphics/1.0#24b395ba17da96288766cc83accc98f5:8b108997a4947ec6a0487a0b6bcbc0d1072e95f3
                    mathlib/1.0#f2b05681ed843bf50d8b7b7bdb5163ea:4d8ab52ebb49f51e63d5193ed580b5a7672e23d5                     

The new ``engine/1.0:de738ff5d09f0359b81da17c58256c619814a765`` binary depends on ``ai/1.1.Z``, because as it is a static library it will only require re-builds for changes in the minor version, but not patches. While the ``game/1.0`` new binary will depend on the full exact ``ai/1.1.0#revision:package_id``, and also on the new ``engine/1.0:de738ff5d09f0359b81da17c58256c619814a765`` new binary that depends on ``ai/1.1.Z``.

Now the game can be executed:

.. code-block:: bash

  # Activate the environment and run the executable 
  # Use "conanbuild.bat && game" in Windows
  $ source conanrun.sh && game
  mathlib/1.0: mathlib maths (Release)!
  ai/1.1.0: SUPER BETTER Artificial Intelligence for aliens (Release)!
  ai/1.1.0: Intelligence level=50
  graphics/1.0: Checking if things collide (Release)!
  engine/1.0: Computing some game things (Release)!
  game/1.0:fun game (Release)!

We can see that the new ``game/1.0`` binary incorporates the improvements in ``ai/1.1.0``, and links correctly with the new binary for ``engine/1.0``.

And this is a basic "products pipeline", we manage to build and test our main products when necessary (recall that ``mapviewer`` wasn't really affected, so no rebuilds were necessary at all).
In general, a production "products pipeline" will finish uploading the built packages to the repository and running a new promotion to the ``develop`` repo. But as this was a very basic and simple pipeline, let's wait a bit for that, and let's continue with more advanced scenarios.
