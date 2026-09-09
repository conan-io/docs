# conan.tools.files patches

<a id="conan-tools-files-patch"></a>

## conan.tools.files.patch()

### patch(conanfile, base_path=None, patch_file=None, patch_string=None, strip=0, fuzz=False, \*\*kwargs)

Applies a diff from file (patch_file) or string (patch_string) in the conanfile.source_folder
directory. The folder containing the sources can be customized with the self.folders attribute
in the layout(self) method.

* **Parameters:**
  * **conanfile** – the current recipe, always pass ‘self’
  * **base_path** – The path is a relative path to conanfile.export_sources_folder unless an
    absolute path is provided.
  * **patch_file** – Patch file that should be applied. The path is relative to the
    conanfile.source_folder unless an absolute path is provided.
  * **patch_string** – Patch string that should be applied.
  * **strip** – Number of folders to be stripped from the path.
  * **fuzz** – Should accept fuzzy patches.
  * **kwargs** – Extra parameters that can be added and will contribute to output information

Usage:

```python
from conan.tools.files import patch

def build(self):
    for it in self.conan_data.get("patches", {}).get(self.version, []):
        patch(self, **it)
```

<a id="conan-tools-files-apply-conandata-patches"></a>

## conan.tools.files.apply_conandata_patches()

### apply_conandata_patches(conanfile)

Applies patches stored in `conanfile.conan_data` (read from `conandata.yml` file).
It will apply all the patches under `patches` entry that matches the given
`conanfile.version`. If versions are not defined in `conandata.yml` it will apply all the
patches directly under `patches` keyword.

The key entries will be passed as kwargs to the `patch` function.

Usage:

```python
from conan.tools.files import apply_conandata_patches

def source(self):
    apply_conandata_patches(self)
```

Examples of `conandata.yml`:

```yaml
patches:
- patch_file: "patches/0001-buildflatbuffers-cmake.patch"
- patch_file: "patches/0002-implicit-copy-constructor.patch"
  base_path: "subfolder"
  patch_type: backport
  patch_source: https://github.com/google/flatbuffers/pull/5650
  patch_description: Needed to build with modern clang compilers.
```

With different patches for different versions:

```yaml
patches:
  "1.11.0":
    - patch_file: "patches/0001-buildflatbuffers-cmake.patch"
    - patch_file: "patches/0002-implicit-copy-constructor.patch"
      base_path: "subfolder"
      patch_type: backport
      patch_source: https://github.com/google/flatbuffers/pull/5650
      patch_description: Needed to build with modern clang compilers.
  "1.12.0":
    - patch_file: "patches/0001-buildflatbuffers-cmake.patch"
    - patch_string: |
        --- a/tests/misc-test.c
        +++ b/tests/misc-test.c
        @@ -1232,6 +1292,8 @@ main (int argc, char **argv)
              g_test_add_func ("/misc/pause-cancel", do_pause_cancel_test);
              g_test_add_data_func ("/misc/stealing/async", GINT_TO_POINTER (FALSE), do_stealing_test);
              g_test_add_data_func ("/misc/stealing/sync", GINT_TO_POINTER (TRUE), do_stealing_test);
        +     g_test_add_func ("/misc/response/informational/content-length", do_response_informational_content_length_test);
        +

        ret = g_test_run ();
    - patch_file: "patches/0003-fix-content-length-calculation.patch"
```

For each patch, a `patch_file`, a `patch_string` or a `patch_user` field must be provided. The first two are automatically applied by `apply_conandata_patches()`, while `patch_user` are ignored, and must be handled by the user directly in the `conanfile.py` recipe.

## conan.tools.files.export_conandata_patches()

### export_conandata_patches(conanfile)

Exports patches stored in ‘conanfile.conan_data’ (read from ‘conandata.yml’ file). It will export
all the patches under ‘patches’ entry that matches the given ‘conanfile.version’. If versions are
not defined in ‘conandata.yml’ it will export all the patches directly under ‘patches’ keyword.

Example of `conandata.yml` without versions defined:

```python
from conan.tools.files import export_conandata_patches
def export_sources(self):
    export_conandata_patches(self)
```

### core.sources.patch:extra_path

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `export_conandata_patches()` tool can automatically inject patches from an external path at package creation time
using the `core.sources.patch:extra_path` core configuration.

That means that `conan create` commands in `conan-center-index` repository could inject and apply patches without
necessarily putting the patches in the same repository and without modifying the `conandata.yml` files.

The `core.sources.patch:extra_path` configuration should point to a folder containing all possible extra patches
for all possible packages, structured by package name, following the same conventions as `conan-center-index` repository:

```text
extra_folder
    pkgname1
       conandata.yml
       patches
          mypatch.path
    pkgname2
       ...
```

The `conandata.yml` should also follow the same structure:

```yaml
patches:
    "1.0":
        - patch_file: "patches/mypatch.patch"
```

#### NOTE
It is impossible to apply patches to arbitrary dependencies when installing them (`conan install --build=xxx`), as the
possible injected patches are part of the “source” identity of the package, and must be represented in their recipe revision.
Already existing packages in the cache or in the remote servers have already exported its files and computed a recipe revision,
so patches cannot be applied there without violating the identity (and as such the reproducibility and traceability) of packages.
As a conclusion, it means that `core.sources.patch:extra_path` can only work at `conan create` time.
