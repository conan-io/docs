Products pipeline
==================

The **products pipeline** responds to a more challenging question: do my "products" build correctly with the new versions of the packages?
to the packages and their dependencies? This is the real "Continuous Integration" part, in which changes in different packages are really tested against the organization
important products to check if things integrate cleanly or break. 

Let's continue with the example above, if we now have a new ``ai/1.1.0`` package,
is it going to break the existing ``game/1.0`` and/or ``mapviewer/1.0`` applications? Is it necessary to re-build from source some of the existing
packages that depend directly or indirectly on ``ai`` package? In this tutorial we use ``game/1.0`` and ``mapviewer/1.0`` as our "products",
but this concept will be further explained later, and specially why it is important to think in terms of "products" instead of trying to explicitly
model the dependencies top-bottom in the CI.

The essence of this **products pipeline** in our example is that the new ``ai/1.1.0`` version that was uploaded to the ``products`` repository
automatically falls into the valid version ranges, and our versioning approach means that such a minor version increase will require building from
source its consumers, in this case ``engine/1.0`` and ``game/1.0`` and in that specific sequential order, while all the other packages will remain the same. 
Knowing which packages need to be built from source and in which order, and executing that build to check if the main organization products keep 
working correctly with the new dependencies versions is the responsibility of the products pipeline.


What are the **products**
-------------------------

The **products** are the main software artifact that a organization (a company, a team, a project) is delivering as final result and provide some
value for users of those artifacts. In this example we will consider ``game/1.0`` and ``mapviewer/1.0`` the "products". Note that it is 
possible to define different versions of the same package as products, for example, if we had to maintain different versions of the ``game`` for
different customers, we could have ``game/1.0`` and ``game/2.3`` as well as different versions of ``mapviewer`` as products.

The "products" approach, besides the advantage of focusing on the business value, has another very important advantage: it avoids having to model
the dependency graph at the CI layer. It is a frequent attempt trying to model the inverse dependency model, that is, representing at the CI level
the dependants or consumers of a given package. In our example, if we had configured a job for building the ``ai`` package, we could have another
job for the ``engine`` package, that is triggered after the ``ai`` one, configuring such topology somehow in the CI system.

But this approach does not scale at all and have very important limitations:
  
- The example above is relatively simple, but in practice dependency graphs can have many more packages, even several hundreds, making it very tedious and error prone to define all dependencies among packages in the CI
- Dependencies evolve over time, and new versions are used, some dependencies are removed and newer dependencies are added. The simple relationship between repositories modeled at the CI level can result in a very inefficient, slow and time consuming CI, if not a fragile one that continuously breaks because some dependencies change.
- The combinatorial nature that happens downstream a dependency graph, where a relatively stable top dependency, lets say ``mathlib/1.0`` might be used by multiple consumers such as ``ai/1.0``, ``ai/1.1``, ``ai/1.2`` which in turn each one might be used by multiple ``engine`` different versions and so on. Building only the latest version of the consumers would be insufficient in many cases and building all of  them would be extremely costly.
- The "inverse" dependency model, that is, asking what are the "dependants" of a given package is extremely challeging in practice, specially in a decentralized
  approach like Conan in which packages can be stored in different repositories, including different servers, and there isn't a central database of all packages and their relations.
  Also, the "inverse" dependency model is, similar to the direct one, conditional. As a dependency can be conditional on any configuration (settings, options), the inverse is
  also conditioned to the same logic, and such logic also evolves and changes with every new revision and version.

In C and C++ projects the "products" pipeline becomes more necessary and critical than in other languages due to the compilation model with headers textual inclusions becoming part of the consumers' binary artifacts and due to the native artifacts linkage models. 


Building intermediate packages new binaries
-------------------------------------------

A frequently asked question is what would be the version of a consumer package when it builds against a new dependency version.
Put it explicitly for our example, where we have defined that we need to build again the ``engine/1.0`` package because now it is
depending on ``ai/1.1.0`` new version:

- Should we create a new ``engine/1.1`` version to build against the new ``ai/1.1.0``?
- Or should we keep the ``engine/1.0`` version?

The answer lies in the  :ref:`binary model and how dependencies affect the package_id<reference_binary_model_dependencies>`.
Conan has a binary model that takes into account both the versions, revisions and ``package_id`` of the dependencies, as well
as the different package types (``package_type`` attribute).

The recommendation is to keep the package versions aligned with the source code. If ``engine/1.0`` is building from a specific
commit/tag of its source repository, and the source of that repository doesn't change at all, then it becomes very confusing to
have a changing package version that deviate from the source version. With the Conan binary model what we will have is 2
different binaries for ``engine/1.0``, with 2 different ``package_id``. One binary will be built against the ``ai/1.0`` version
and the other binary will be built against the ``ai/1.1.0``, something like:

.. code-block::
  :emphasize-lines: 6, 12, 14, 20

  $ conan list engine:* -r=develop
  engine/1.0
      revisions
        fba6659c9dd04a4bbdc7a375f22143cb (2024-08-22 09:46:24 UTC)
          packages
            2c5842e5aa3ed21b74ed7d8a0a637eb89068916e
              info
                settings
                  ...
                requires
                  ai/1.0.Z
                  graphics/1.0.Z
                  mathlib/1.0.Z
            de738ff5d09f0359b81da17c58256c619814a765
              info
                settings
                  ...
                requires
                  ai/1.1.Z
                  graphics/1.0.Z
                  mathlib/1.0.Z


Let's see how a product pipeline can build such ``engine/1.0`` and ``game/1.0`` new binaries using the new dependencies versions.
In the following sections we will present a products pipeline in an incremental way, the same as the packages pipeline.


.. toctree::
   :maxdepth: 1

   products_pipeline/single_configuration
   products_pipeline/build_order
   products_pipeline/multi_product
   products_pipeline/full_pipeline
