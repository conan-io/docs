conan.tools.files patches
=========================

.. _conan_tools_files_patch:

conan.tools.files.patch()
-------------------------

.. currentmodule:: conan.tools.files.patches

.. autofunction:: patch


Usage:

.. code-block:: python

    from conan.tools.files import patch

    def build(self):
        for it in self.conan_data.get("patches", {}).get(self.version, []):
            patch(self, **it)


.. _conan_tools_files_apply_conandata_patches:

conan.tools.files.apply_conandata_patches()
-------------------------------------------

.. currentmodule:: conan.tools.files.patches

.. autofunction:: apply_conandata_patches

Usage:

.. code-block:: python

    from conan.tools.files import apply_conandata_patches

    def build(self):
        apply_conandata_patches(self)


Examples of ``conandata.yml``:

.. code-block:: yaml

    patches:
    - patch_file: "patches/0001-buildflatbuffers-cmake.patch"
    - patch_file: "patches/0002-implicit-copy-constructor.patch"
      base_path: "subfolder"
      patch_type: backport
      patch_source: https://github.com/google/flatbuffers/pull/5650
      patch_description: Needed to build with modern clang compilers.

With different patches for different versions:

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


For each patch, a ``patch_file``, a ``patch_string`` or a ``patch_user`` field must be provided. The first two are automatically applied by ``apply_conandata_patches()``, while ``patch_user`` are ignored, and must be handled by the user directly in the ``conanfile.py`` recipe.


conan.tools.files.export_conandata_patches()
--------------------------------------------

.. currentmodule:: conan.tools.files.patches

.. autofunction:: export_conandata_patches

Example of ``conandata.yml`` without versions defined:

.. code-block:: python

    from conan.tools.files import export_conandata_patches
    def export_sources(self):
        export_conandata_patches(self)