.. _conan_tools_files:

conan.tools.files
=================

.. _conan_tools_files_patch:

conan.tools.files.patch()
-------------------------

.. code-block:: python

    def patch(conanfile, base_path=None, patch_file=None, patch_string=None,
            strip=0, fuzz=False, **kwargs):

Applies a diff from file (*patch_file*)  or string (*patch_string*) in *base_path* directory. If
*base_path* is not passed it is applied in the current directory.

Parameters:
    - **base_path**: Base path where the patch should be applied.
    - **patch_file**: Patch file that should be applied.
    - **patch_string**: Patch string that should be applied.
    - **strip**: Number of folders to be stripped from the path.
    - **output**: Stream object.
    - **fuzz**: Should accept fuzzy patches.
    - **kwargs**: Extra parameters that can be added and will contribute to output information.

.. _conan_tools_files_apply_conandata_patches:

conan.tools.files.apply_conandata_patches()
-------------------------------------------

.. code-block:: python

    def apply_conandata_patches(conanfile):

Applies patches stored in ``conanfile.conan_data`` (read from ``conandata.yml`` file). It will apply
all the patches under ``patches`` entry that matches the given ``conanfile.version``. If versions are
not defined in ``conandata.yml`` it will apply all the patches directly under ``patches`` keyword.

Example of ``conandata.yml`` without versions defined:

.. code-block:: yaml

    patches:
    - patch_file: "patches/0001-buildflatbuffers-cmake.patch"
      base_path: "source_subfolder"
    - patch_file: "patches/0002-implicit-copy-constructor.patch"
      base_path: "source_subfolder"
      patch_type: backport
      patch_source: https://github.com/google/flatbuffers/pull/5650
      patch_description: Needed to build with modern clang compilers.

Example of ``conandata.yml`` with different patches for different versions:

.. code-block:: yaml

    patches:
      "1.11.0":
        - patch_file: "patches/0001-buildflatbuffers-cmake.patch"
          base_path: "source_subfolder"
        - patch_file: "patches/0002-implicit-copy-constructor.patch"
          base_path: "source_subfolder"
          patch_type: backport
          patch_source: https://github.com/google/flatbuffers/pull/5650
          patch_description: Needed to build with modern clang compilers.
      "1.12.0":
        - patch_file: "patches/0001-buildflatbuffers-cmake.patch"
          base_path: "source_subfolder"
