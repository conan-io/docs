<a id="reference-conanfile-methods-config-options"></a>

# config_options()

The `config_options()` method is used to configure or constrain the available options in a package **before** assigning them a value.
A typical use case is to remove an option in a given platform.
For example, the `SSE2` flag doesn’t exist in architectures different than 32 bits, so it should be removed in this method like so:

```python
def config_options(self):
    if self.settings.arch != "x86_64":
        del self.options.with_sse2
```

The `config_options()` method executes:

* Before calling the `configure()` method.
* Before assigning the `options` values.
* After `settings` are already defined.

<a id="reference-conanfile-methods-config-options-implementations"></a>

## Available automatic implementations

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

When the `config_options()` method is not defined, Conan can automatically manage some
conventional options if specified in the
[implements](https://docs.conan.io/2//reference/conanfile/attributes.html.md#conan-conanfile-attributes-implements) ConanFile attribute:

### auto_shared_fpic

Options automatically managed:

- `fPIC` (True, False).

It can be added to the recipe like this:

```python
from conan import ConanFile

class Pkg(ConanFile):
    implements = ["auto_shared_fpic"]
    ...
```

Then, if no `config_options()` method is specified in the recipe, Conan will
automatically manage the fPIC setting in the `config_options` step like this:

```python
if conanfile.settings.get_safe("os") == "Windows":
    conanfile.options.rm_safe("fPIC")
```

Be aware that adding this implementation to the recipe may also affect the
[configure](https://docs.conan.io/2//reference/conanfile/methods/configure.html.md#reference-conanfile-methods-configure-implementations) step.

If you need to implement custom behaviors in your recipes but also need this logic, it
must be explicitly declared:

```python
def config_options(self):
    if conanfile.settings.get_safe("os") == "Windows":
        conanfile.options.rm_safe("fPIC")
    if self.settings.arch != "x86_64":
        del self.options.with_sse2
```

#### SEE ALSO
- Follow the [tutorial about recipe configuration methods](https://docs.conan.io/2//tutorial/creating_packages/configure_options_settings.html.md#tutorial-creating-configure).
