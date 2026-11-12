<a id="reference-policies"></a>

# Policies

Policies are a set of rules to enforce certain behaviors from Conan.
Policies are handled by the `core:policies` configuration in your `global.conf`,
which is a list of strings, where each string is the name of a policy to be enabled.

```default
core:policies = ["required_conan_version>=2.28"]
```

## List of current policies

### required_conan_version>=version

*Introduced in Conan 2.28*

This policy is unique, as the version specified in the policy is used to enable different behaviors based on the version.
This allows to opt-in to bugfixes that can be considered breaking changes, without having to wait for a new Conan release to include them by default.

The same behaviours are also enabled recipe-wise when the `required_conan_version` attribute is defined in the recipe,
such that the policy can be enabled for specific recipes, without having to enable it globally.
If both the policy and the recipe attribute are defined, the behavior will be enabled if either of them matches the required version range.

* If using `required_conan_version>=2.28` or later, the following bugfixes will be enabled:
  : * Bugfix [https://github.com/conan-io/conan/pull/19705](https://github.com/conan-io/conan/pull/19705):
      : * The computation of `package_id` for static libraries and non-embed mode was taking into account transitive (non-direct) dependencies,
          even if they were not being embedded and not contributing headers at all.
          See the docs for the [effect of dependencies in the package_id](https://docs.conan.io/2//reference/binary_model/dependencies.html.md#reference-binary-model-dependencies).
    * Bugfix [https://github.com/conan-io/conan/pull/19849](https://github.com/conan-io/conan/pull/19849):
      : * The `VirtualBuildEnv` generator used to include the `bindir` paths of tool requires
          regardless of their `run` trait in the generated environment. With the bugfix enabled,
          only tool requires with the `run` trait set to `True` will have their `bindir` paths
          propagated.
    * Behaviour change [https://github.com/conan-io/conan/pull/19286](https://github.com/conan-io/conan/pull/19286):
      : * For the new `consistent` trait, its default value currently keeps the old graph expansion behaviour,
          which had some inconsistencies regarding the handling of private dependencies.
          With the new behaviour enabled, the graph expansion is more consistent and private dependencies are handled in a more intuitive way,
          but some graphs can be expanded differently. For a detailed explanation of the changes,
          see [the trait documentation section](https://docs.conan.io/2//reference/conanfile/methods/requirements.html.md#reference-conanfile-methods-requirements-consistent).
* If using `required_conan_version>=2.30` or later, the following bugfixes will be enabled:
  : * Bugfix [https://github.com/conan-io/conan/pull/20073](https://github.com/conan-io/conan/pull/20073):
      : * The `transitive_headers` trait propagation of some diamond structures was not working correctly
          and unexpected headers were being propagated to consumers.
          With the bugfix enabled, the propagation of transitive headers is fixed and works as expected in all
          cases, but the consumer package_id can change if it was previously affected by this bug.

#### NOTE
This policy is independent of the `core:required_conan_version` conf,
which is exclusively used to define the minimum required Conan version.
