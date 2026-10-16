<a id="reference-extensions-compiler-flags-plugin"></a>

# Compiler flags mapper plugin

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `compiler_flags.py` extension plugin is a Python script that receives the list of compiler
flags provided by dependencies `cpp_info` information, and allows to process it.

This plugin must be located in the `extensions/plugins` cache folder, and can be installed
with the `conan config install` and `conan config install-pkg` commands.

A possible use case would be when packages built with a different compiler, for example `msvc`
define some `msvc` specific compiler flags for their consumers assuming it will be the same
compiler. But if the consumer is using LLVM/Clang, assuming binary compatibility, then that
clang compiler could be receiving `msvc` flags that is not expecting and that it doesn’t
understand. This plugin allows to convert, map, remove, translate or add compiler flags.

For example, a case that exists in ConanCenter recipes is some packages defining `/Zc:__cplusplus`
compiler flag for `msvc` that `clang` compiler won’t understand. In this case, it is possible
to write a pluging like:

```python
def flags_map(conanfile, item, flags, **kwargs):
    if item != "cxxflags":
        return flags
    result = []
    compiler = conanfile.settings.get_safe("compiler")
    for d in flags:
        if d.startswith("/Zc:"):
            if compiler == "msvc":
                result.append(d)
        else:
            result.append(d)
    return result
```

The `conanfile` object is passed as an argument, so it is possible to check the `compiler`
that the consumer will be using. Only for `msvc` the `/Zc` flags will be propagated, otherwise
they will be ignored.

The possible `item` values are `cflags`, `cxxflags`, `sharedlinkflags` and `exelinkflags`.

#### WARNING
Do not abuse this feature for other purposes rather than the binary compatibility among
different compilers exemplified above. If you have some other use case that could be addressed
by this plugin, please submit a ticket to [https://github.com/conan-io/conan/issues](https://github.com/conan-io/conan/issues) first to discuss.
