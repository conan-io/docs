conan.tools.files patches
=========================

.. _conan_tools_files_patch:

conan.tools.files.patch()
-------------------------

.. code-block:: python

    def patch(conanfile, base_path=None, patch_file=None, patch_string=None, strip=0, fuzz=False, **kwargs):

Applies a diff from file (*patch_file*) or string (*patch_string*) in the ``conanfile.source_folder`` directory.
The folder containing the sources can be customized with the ``self.folders`` attribute in the :ref:`layout(self)
method<layout_folders_reference>`.

Parameters:

- **patch_file**: Patch file that should be applied. The path is relative to the **conanfile.source_folder** unless
  an absolute path is provided.
- **base_path**: The path is a relative path to **conanfile.source_folder** unless an absolute path is provided.
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
