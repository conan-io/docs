Products pipeline
==================



There are some important points to understand about the products pipeline:

- What are the **products**? The "products" are the main software artifact that my organization is delivering as final result and provide some
  value for users of those artifacts. In this example we will consider ``game/1.0`` and ``mapviewer/1.0`` the "products". Note that it is 
  possible to define different versions of the same package as products, for example, if we had to maintain different versions of the ``game`` for
  different customers, we could have ``game/1.0`` and ``game/2.3`` as well as different versions of ``mapviewer`` as products.
- Why not defining in CI the "users" or "consumers" of every package? It might be tempting to model the relationships between packages, in this
  case, that the package ``ai`` is used by the ``engine`` package, and then try to configure the CI so a build of ``engine`` is triggered after
  a build of ``ai``. But this approach does not scale at all and have very important limitations:
  
  - The example above is relatively simple, but in practice dependency graphs can have many more packages, even hundrends, making it very tedious and error prone to define all dependencies among packages in the CI
  - Dependencies evolve over time, and new versions are used, some dependencies are removed and newer dependencies are added. The simple relationship between repositories modeled at the CI level can result in a very inefficient, slow and time consuming CI, if not a fragile one that continuously breaks because some dependencies change.
  - The combinatorial nature that happens downstream a dependency graph, where a relatively stable top dependency, lets say ``mathlib/1.0`` might be used by multiple consumers such as ``ai/1.0``, ``ai/1.1``, ``ai/1.2`` which in turn each one might be used by multiple ``engine`` different versions and so on. Building only the latest version of the consumers would be insufficient in many cases and building all of  them would be extremely costly.
- In C and C++ projects the "products" pipeline becomes more necessary and critical than in other languages due to the compilation model with
  headrs textual inclusions becoming part of the consumers' binary artifacts and due to the native artifacts
  linkage models. This means that in many scenarios it will be necessary to build new binaries that depend on some modified packages, even
  if the source of the package itself didn't change at all. Conan's ``package_id`` computation together with some versioning conventions
  can greatly help to efficiently define which packages needs to rebuild and which ones don't.



.. toctree::
   :maxdepth: 1

   products_pipeline/single_configuration

