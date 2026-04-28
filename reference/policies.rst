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

``required_conan_version>=version``
-----------------------------------
*Introduced in Conan 2.28*

This policy is unique, as the version specified in the policy is used to enable different behaviors based on the version specified.
This allows to opt-in to bugfixes that can be considered breaking changes, without having to wait for a new Conan release to include them by default.

* If using ``required_conan_version>=2.28`` or later, the following bugfixes will be enabled:
   * Bugfix https://github.com/conan-io/conan/pull/19705 for transitive static libraries package_id
   * Bugfix https://github.com/conan-io/conan/pull/19849 for VirtualBuildEnv bindir path propagation based on requirement run trait
   * https://github.com/conan-io/conan/pull/19286 defaults the new ``consistent`` trait to True for the host context, even when ``visible=False``

The same behaviours are also enabled recipe-wise when the ``required_conan_version`` attribute is defined in the recipe.

.. note::
   This policy is independent of the ``core:required_conan_version`` conf,
   which is exclusively used to define the minimum required Conan version.

``deprecated_build_order_args``
-------------------------------
*Introduced in Conan 2.28*

If the policy is defined, the old behaviour for ``conan graph build-order`` is kept where the
``--order-by`` argument is not required, and the output is ordered by recipe by default.
Note that when the argument is provided, the output format is different, such that the order is
returned inside the ``order`` key of the json output, instead of being the top-level list.

.. warning::
   **Will be removed in Conan 2.32**, where the ``--order-by`` argument will be mandatory and the old behavior will be removed.

``deprecated_empty_version_range``
----------------------------------
*Introduced in Conan 2.28*

If the policy is enabled, Conan will accept empty version ranges (e.g., ``pkg/[]``) as valid,
and they will be treated as "any version" (equivalent to ``pkg/[*]``).

.. warning::
   **Will be removed in Conan 2.32**, where empty version ranges will be considered invalid and treated as a syntax error.
