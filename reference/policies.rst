.. _reference_policies:

Policies
========

Policies are a set of rules to enforce certain behaviors from Conan.
Policies are handled by the ``core:policies`` configuration in your ``global.conf``.

Some policies are meant to be used only as a fallback mechanism for deleted deprecated behaviour,
while others are meant to be used to opt-in to bugfixes that can be considered breaking changes.

This page documents the currently available policies.

.. code-block::
   :caption: ``global.conf``

   core:policies = ["required_conan_version>=2.28", "deprecated_build_order_args"]

List of current policies
~~~~~~~~~~~~~~~~~~~~~~~~

``required_conan_version>=version``
-----------------------------------
*Introduced in Conan 2.28*

If the policy is defined, different behaviors can be enabled:
   - If ``required_conan_version>=2.28``, bugfix https://github.com/conan-io/conan/pull/19705 for transitive static libraries package_id
   - If ``required_conan_version>=2.28``, bugfix https://github.com/conan-io/conan/pull/19849 for VirtualBuildEnv bindir path propagation based on requirement run trait
   - If ``required_conan_version>=2.28``, https://github.com/conan-io/conan/pull/19286 defaults the new ``consistent`` trait to True for the host context, even when ``visible=False``

More explanation of this policy, and differences with ``core:required_conan_version``

``deprecated_build_order_args``
-------------------------------
*Introduced in Conan 2.28*

If the policy is defined, the old behaviour for ``conan graph build-order`` is kept where the
``--order-by`` argument is not required, and the output is ordered by recipe by default.
Note that when the argument is provided, the output format is different, such that the order is
returned inside the ``order`` key of the json output, instead of being the top-level list.

**Will be removed in Conan 2.32**, where the ``--order-by`` argument will be mandatory and the old behavior will be removed.

``deprecated_empty_version_range``
----------------------------------
*Introduced in Conan 2.28*

If the policy is enabled, Conan will accept empty version ranges (e.g., ``pkg/[]``) as valid,
and they will be treated as "any version" (equivalent to ``pkg/[*]``).

**Will be removed in Conan 2.32**, where empty version ranges will be considered invalid and treated as a syntax error.