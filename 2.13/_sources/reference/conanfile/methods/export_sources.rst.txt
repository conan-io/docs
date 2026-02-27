.. _reference_conanfile_methods_export_sources:

export_sources()
================

Equivalent to the ``exports_sources`` attribute, but in method form. This method will be called at ``export`` time,
which happens in ``conan export`` and ``conan create`` commands, and it is intended to allow copying files from the
user folder to the Conan cache folders, those files becoming part of the recipe sources. These sources will
be uploaded to the servers together with the recipe, but are typically not downloaded unless the package is 
being built from source.

The current working directory will be ``self.recipe_folder``, and it can use the ``self.export_sources_folder``
as the destination folder for using ``copy()`` or your custom copy.

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import copy

    class Pkg(ConanFile):
        def export_sources(self):
            # This LICENSE.md is a source file intended to be part of the final package
            # it is not the license of the current recipe
            copy(self, "LICENSE.md", self.recipe_folder, self.export_sources_folder)


The method might be able to read files in the recipe folder and do something with it:

.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.files import load, save

    class Pkg(ConanFile):

        def export_sources(self):
            content = load(self, os.path.join(self.recipe_folder, "data.txt"))
            save(self, os.path.join(self.export_sources_folder, "myfile.txt"), content)


The ``export_conandata_patches()`` is a high-level helper function that does the export of the patches defined
in the ``conandata.yml`` file, which could be later applied with ``apply_conandata_patches()`` in the ``source()`` method.

.. code-block:: python

    from conan.tools.files import export_conandata_patches

    class Pkg(ConanFile):

        def export_sources(self):
            export_conandata_patches(self)


.. note::

    **Best practices**

    - The recipe sources must be configuration independent. Those sources are common for all configurations, thus it is not possible to do conditional ``export_sources()`` to different settings, options, or platforms. Do not try to do any kind of conditional export. If necessary export all the files necessary for all configurations at once.
    - The ``export_sources()`` method does not receive any information from profiles, not even ``conf``. Only the ``global.conf`` will be available, and in any case it is not possible to use that ``conf`` to define conditionals.
    - Keep the ``export_source()`` method simple. Its intention is to copy files from the user folder to the cache to store those files together with the recipe.
