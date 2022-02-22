conan.tools.files basic operations
==================================


.. warning::

    These tools are **experimental** and subject to breaking changes.


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
