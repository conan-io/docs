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


conan.tools.files.update_conandata()
------------------------------------

.. code-block:: python

    def update_conandata(conanfile, data)

Parameters:

- **conanfile**: Conanfile object.
- **data** (Required): A dictionary (can be nested), of values to update


This function reads the ``conandata.yml`` inside the exported folder in the conan cache, if it exists.
If the ``conandata.yml`` does not exist, it will create it.
Then, it updates the conandata dictionary with the provided ``data`` one, which is updated recursively,
prioritizing the ``data`` values, but keeping other existing ones. Finally the ``conandata.yml`` is saved
in the same place.

This helper can only be used within the ``export()`` method, it can raise otherwise. One application is
to capture in the ``conandata.yml`` the scm coordinates (like Git remote url and commit), to be able to
recover it later in the ``source()`` method and have reproducible recipes that can build from sources
without actually storing the sources in the recipe.

Example:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import update_conandata

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"

        def export(self):
            # This is an example, doesn't make sense to have static data, instead you
            # could put the data directly in a conandata.yml file.
            # This would be useful for storing dynamic data, obtained at export() time from elsewhere
            update_conandata(self, {"mydata": {"value": {"nested1": 123, "nested2": "some-string"}}})
    
        def source(self):
            data = self.conan_data["sources"]["mydata"]
