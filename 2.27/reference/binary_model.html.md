<a id="reference-binary-model"></a>

# Binary model

This section introduces first how the `package_id`, the package binaries identifier is computed, hashing the configuration (settings + options + dependencies versions). While the effect of `settings` and `options` is more straightforward, understanding the effects of the dependencies requires more explanations, so that will be done in its own section.

Conan binary model is extensible, and users can define their custom settings, options and configuration to model their own binaries characteristics.

Finally, the default binary compatibility model will be described, and how it can be customized to adapt to different needs.

* [How the `package_id` is computed](https://docs.conan.io/2//reference/binary_model/package_id.html.md)
* [How settings and options of a recipe influence its package ID](https://docs.conan.io/2//reference/binary_model/settings_and_options.html.md)
* [The effect of dependencies on `package_id`](https://docs.conan.io/2//reference/binary_model/dependencies.html.md)
* [Extending the binary model](https://docs.conan.io/2//reference/binary_model/extending.html.md)
* [Customizing the binary compatibility](https://docs.conan.io/2//reference/binary_model/custom_compatibility.html.md)
