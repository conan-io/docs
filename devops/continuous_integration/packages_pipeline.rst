Packages pipeline
==================

For the ``package pipeline`` we will start with a simple source code change in the ``ai`` recipe, simulating some improvements
in the ``ai`` package, providing some better algorithms for our game.

Let's do the following changes:

- Let's change the implementation of the ``ai/src/ai.cpp`` function and change the message from ``Some Artificial`` to ``SUPER BETTER Artificial``
- Let's change the default ``intelligence=0`` value in ``ai/include/ai.h`` to a new ``intelligence=50`` default.
- Finally, let's bump the version. As we did some changes to the package public headers, it would be adviced to bump the ``minor`` version,
  so let`s edit the ``ai/conanfile.py`` file and define ``version = "1.1.0"`` there (instead of the previous ``1.0``). Note that if we
  did some breaking changes to the ``ai`` public API, the recommendation would be to change the major instead and create a new ``2.0`` version.


The ``packages pipeline`` will take care of building the different packages binaries for the new ``ai/1.1.0`` and upload them to the ``packages``
binary repository. If the pipeline succeed it will copy them to the ``products`` binary repository, and stop otherwise.

There are different aspects that need to be taken into account when building these packages. The following tutorial sections do the same
job, but under different hypothesis. They are explained in increasing complexity.


.. toctree::
   :maxdepth: 1

   packages_pipeline/single_configuration
   packages_pipeline/multi_configuration
   packages_pipeline/multi_configuration_lockfile
