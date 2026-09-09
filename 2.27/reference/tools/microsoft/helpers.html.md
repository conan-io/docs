<a id="conan-tools-microsoft-helpers"></a>

# check_min_vs

### check_min_vs(conanfile, version, raise_invalid=True)

This is a helper method to allow the migration of 1.X -> 2.0 and VisualStudio -> msvc settings
without breaking recipes.
The legacy “Visual Studio” with different toolset is not managed, not worth the complexity.

* **Parameters:**
  * **raise_invalid** – `bool` Whether to raise or return False if the version check fails
  * **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.
  * **version** – `str` Visual Studio or msvc version number.

Example:

```python
def validate(self):
    check_min_vs(self, "192")
```

# msvc_runtime_flag

### msvc_runtime_flag(conanfile)

Gets the MSVC runtime flag given the `compiler.runtime` value from the settings.

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.
* **Returns:**
  `str` runtime flag.

# is_msvc

### is_msvc(conanfile, build_context=False)

Validates if the current compiler is `msvc`.

* **Parameters:**
  * **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.
  * **build_context** – If True, will use the settings from the build context, not host ones
* **Returns:**
  `bool` True, if the host compiler is `msvc`, otherwise, False.

# is_msvc_static_runtime

### is_msvc_static_runtime(conanfile)

Validates when building with Visual Studio or msvc and MT on runtime.

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.
* **Returns:**
  `bool` True, if `msvc + runtime MT`. Otherwise, False.

# msvs_toolset

### msvs_toolset(conanfile)

Returns the corresponding platform toolset based on the compiler setting.
In case no toolset is configured in the profile, it will return a toolset based on the
compiler version, otherwise, it will return the toolset from the profile.
When there is no compiler version neither toolset configured, it will return None
It supports msvc, intel-cc and clang compilers. For clang, is assumes the ClangCl toolset,
as provided by the Visual Studio installer.

* **Parameters:**
  **conanfile** – Conanfile instance to access settings.compiler
* **Returns:**
  A toolset when compiler.version is valid or compiler.toolset is configured. Otherwise, None.

<a id="conan-tools-microsoft-unix-path"></a>

# unix_path

### unix_path(conanfile, path, scope='build')
