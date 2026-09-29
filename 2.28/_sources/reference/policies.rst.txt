.. _reference_policies:

Policies
========
Policies are a set of rules to enforce certain behaviors from Conan.
Policies are handled by the ``core:policies`` configuration in your ``global.conf``,
which is a list of strings, where each string is the name of a policy to be enabled.


.. code-block::
   :caption: ``global.conf``

   core:policies = ["required_conan_version>=2.28", "deprecated_build_order_args"]

List of current policies
~~~~~~~~~~~~~~~~~~~~~~~~

required_conan_version>=version
-------------------------------
*Introduced in Conan 2.28*

This policy is unique, as the version specified in the policy is used to enable different behaviors based on the version.
This allows to opt-in to bugfixes that can be considered breaking changes, without having to wait for a new Conan release to include them by default.

The same behaviours are also enabled recipe-wise when the ``required_conan_version`` attribute is defined in the recipe,
such that the policy can be enabled for specific recipes, without having to enable it globally.
If both the policy and the recipe attribute are defined, the behavior will be enabled if either of them matches the required version range.

* If using ``required_conan_version>=2.28`` or later, the following bugfixes will be enabled:
   * Bugfix https://github.com/conan-io/conan/pull/19705:
      * The computation of ``package_id`` for static libraries and non-embed mode was taking into account transitive (non-direct) dependencies,
        even if they were not being embedded and not contributing headers at all.
        See the docs for the :ref:`effect of dependencies in the package_id<reference_binary_model_dependencies>`.
   * Bugfix https://github.com/conan-io/conan/pull/19849:
      * The ``VirtualBuildEnv`` generator used to include the ``bindir`` paths of tool requires
        regardless of their ``run`` trait in the generated environment. With the bugfix enabled,
        only tool requires with the ``run`` trait set to ``True`` will have their ``bindir`` paths
        propagated.
   * Behaviour change https://github.com/conan-io/conan/pull/19286:
      * For the new ``consistent`` trait, its default value currently keeps the old graph expansion behaviour,
        which had some inconsistencies regarding the handling of private dependencies.
        With the new behaviour enabled, the graph expansion is more consistent and private dependencies are handled in a more intuitive way,
        but some graphs can be expanded differently. For a detailed explanation of the changes,
        see :ref:`the trait documentation section<reference_conanfile_methods_requirements_consistent>`.

.. note::
   This policy is independent of the ``core:required_conan_version`` conf,
   which is exclusively used to define the minimum required Conan version.

deprecated_build_order_args
---------------------------
*Introduced in Conan 2.28*

If the policy is defined, the old behaviour for ``conan graph build-order`` is kept where the
``--order-by`` argument is not required, and the output is ordered by recipe by default.
Note that when the argument is provided, the output format is different, such that the order is
returned inside the ``order`` key of the json output, instead of being the top-level list.

With ``core:policies=["deprecated_build_order_args"]``, the following command will work without the ``--order-by`` argument:

.. code-block:: shell

   $ conan graph build-order ... -f=json

   [
       [{...}, {...}],
       [{...}]
   ]

Without the policy, the ``--order-by`` argument is mandatory, and the output will be:

.. code-block:: shell

   $ conan graph build-order ... -f=json --order-by=recipe

   {
       "order": [
           [{...}, {...}],
           [{...}]
       ],
       "order_by": "recipe",
       ...
   }



.. warning::
   **Will be removed in Conan 2.32**, where the ``--order-by`` argument will be mandatory and the old behavior will be removed.

deprecated_empty_version_range
------------------------------
*Introduced in Conan 2.28*

If the policy is enabled, Conan will accept empty version ranges (e.g., ``pkg/[]``) as valid,
and they will be treated as "any version" (equivalent to ``pkg/[*]``).

.. warning::
   **Will be removed in Conan 2.32**, where empty version ranges will be considered invalid and treated as a syntax error.
