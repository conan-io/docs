.. _conan_tools_files:

conan.tools.files
=================

.. _conan_tools_files_patch:

conan.tools.files.patch()
-------------------------

.. code-block:: python

    def patch(conanfile, base_path=None, patch_file=None, patch_string=None,
              strip=0, fuzz=False, **kwargs):

Applies a diff from file (*patch_file*) or string (*patch_string*) in the ``conanfile.source_folder`` directory.
The folder containing the sources can be customized with the ``self.folders`` attribute in the :ref:`layout(self)
method<layout_folders_reference>`.

Parameters:
    - **patch_file**: Patch file that should be applied.
    - **base_path**: Relative path from **conanfile.source_folder**.
    - **patch_string**: Patch string that should be applied.
    - **strip**: Number of folders to be stripped from the path.
    - **output**: Stream object.
    - **fuzz**: Should accept fuzzy patches.
    - **kwargs**: Extra parameters that can be added and will contribute to output information.


.. code-block:: python

    from conan.tools.files import patch

    def build(self):
        for it in self.conan_data.get("patches", {}).get(self.version, []):
            patch(self, **it)

.. _conan_tools_files_apply_conandata_patches:

conan.tools.files.apply_conandata_patches()
-------------------------------------------

.. code-block:: python

    def apply_conandata_patches(conanfile):

Applies patches stored in ``conanfile.conan_data`` (read from ``conandata.yml`` file). It will apply
all the patches under ``patches`` entry that matches the given ``conanfile.version``. If versions are
not defined in ``conandata.yml`` it will apply all the patches directly under ``patches`` keyword.

The key entries will be passed as kwargs to the :ref:`patch<conan_tools_files_patch>` function.

Example of ``conandata.yml`` without versions defined:

.. code-block:: python

    from conan.tools.files import apply_conandata_patches

    def build(self):
        apply_conandata_patches(self)

.. code-block:: yaml

    patches:
    - patch_file: "patches/0001-buildflatbuffers-cmake.patch"
    - patch_file: "patches/0002-implicit-copy-constructor.patch"
      base_path: "subfolder"
      patch_type: backport
      patch_source: https://github.com/google/flatbuffers/pull/5650
      patch_description: Needed to build with modern clang compilers.

Example of ``conandata.yml`` with different patches for different versions:

.. code-block:: yaml

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

conan.tools.files.rename()
--------------------------

.. code-block:: python

    def rename(conanfile, src, dst)

Utility functions to rename a file or folder *src* to *dst*. On Windows, it is very common that ``os.rename()`` raises an "Access is denied" exception, so this tool uses:command:`robocopy` if available. If that is not the case, or the rename is done in a non-Windows machine, it falls back to the ``os.rename()`` implementation.

.. code-block:: python

    from conan.tools.files import rename

    def source(self):
        rename(self, "lib-sources-abe2h9fe", "sources")  # renaming a folder

Parameters:
  - **conanfile**: Conanfile object.
  - **src** (Required): Path to be renamed.
  - **dst** (Required): Path to be renamed to.
