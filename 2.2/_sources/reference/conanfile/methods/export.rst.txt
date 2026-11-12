.. _reference_conanfile_methods_export:

export()
========

Equivalent to the ``exports`` attribute, but in method form. This method will be called at ``export`` time,
which happens in the ``conan export`` and ``conan create`` commands, and it is intended to allow copying files from the
user folder to the Conan cache folders, thus making files becoming part of the recipe. These sources will
be uploaded to the servers together with the recipe, but are typically not downloaded unless the package is 
being built from source.

The current working directory will be ``self.recipe_folder``, and it can use the ``self.export_folder``
as the destination folder for using ``copy()`` or your custom copy.

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import copy

    class Pkg(ConanFile):
        def export(self):
            # This LICENSE file is intended to be the license of the current conanfile.py recipe
            # and go with it. It is not intended to be the license of the final package (for that
            # purpose export_sources() would be recommended)
            copy(self, "LICENSE.md", self.recipe_folder, self.export_folder)


There are 2 files that are always exported to the cache, without being explicitly defined in the recipe: the ``conanfile.py`` recipe, and the ``conandata.yml`` file if it exists. The ``conandata.yml`` file is automatically loaded whenever the ``conanfile.py`` is loaded, becoming the ``self.conan_data`` attribute, so it is a intrinsic part of the recipe, so it is part of the "exported" recipe files, not of the "exported" source files.


.. note::

    **Best practices**

    - The recipe files must be configuration independent. Those files are common for all configurations, thus it is not possible to do conditional ``export()`` to different settings, options, or platforms. Do not try to do any kind of conditional export. If necessary export all the files necessary for all configurations at once.
    - The exported files must be small. Exporting big files with the recipe will make the resolution of dependencies much slower the resolution.
    - Only files that are necessary for the evaluation of the ``conanfile.py`` recipe must be exported with this method. Files necessary for building from sources should be exported with the ``exports_sources`` attribute or the :ref:`export_source()<reference_conanfile_methods_export_sources>` method.
