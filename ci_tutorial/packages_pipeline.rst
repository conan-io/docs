Packages pipeline
==================


The **packages pipeline** will build, create and upload the package binaries for the different configurations and platforms, when some
developer is submitting some changes to one of the organization repositories source code. For example if a developer is doing some changes
to the ``ai`` package, improving some of the library functionality, and bumping the version to ``ai/1.1.0``. If the organization needs to
support both Windows and Linux platforms, then the package pipeline will build the new ``ai/1.1.0`` both for Windows and Linux, before
considering the changes are valid. If some of the configurations fail to build under a specific platform, it is common to consider the
changes invalid and stop the processing of those changes, until the code is fixed.


For the ``package pipeline`` we will start with a simple source code change in the ``ai`` recipe, simulating some improvements
in the ``ai`` package, providing some better algorithms for our game.

**Let's do the following changes in the ai package**:

- Let's change the implementation of the ``ai/src/ai.cpp`` function and change the message from ``Some Artificial`` to ``SUPER BETTER Artificial``
- Let's change the default ``intelligence=0`` value in ``ai/include/ai.h`` to a new ``intelligence=50`` default.
- Finally, let's bump the version. As we did some changes to the package public headers, it would be adviced to bump the ``minor`` version,
  so let`s edit the ``ai/conanfile.py`` file and define ``version = "1.1.0"`` there (instead of the previous ``1.0``). Note that if we
  did some breaking changes to the ``ai`` public API, the recommendation would be to change the major instead and create a new ``2.0`` version.


The **packages pipeline** will take care of building the different packages binaries for the new ``ai/1.1.0`` and upload them to the ``packages``
binary repository to avoid disrupting or causing potential issues to other developers and CI jobs. 
If the pipeline succeed it will promote (copy) them to the ``products`` binary repository, and stop otherwise.

There are different aspects that need to be taken into account when building these binary packages for ``ai/1.1.0``. The following tutorial sections do the same
job, but under different hypothesis. They are explained in increasing complexity.

Note all of the commands can be found in the repository ``run_example.py`` file. This file is mostly intended for maintainers and testing,
but it might be useful as a reference in case of issues.


.. toctree::
   :maxdepth: 1

   packages_pipeline/single_configuration
   packages_pipeline/multi_configuration
   packages_pipeline/multi_configuration_lockfile
