Folders and layout
++++++++++++++++++

.. _conan_conanfile_properties_folders:

.. _conan_conanfile_properties_source_folder:

source_folder
-------------

The folder in which the source code lives. The path is built joining the base directory
(a cache directory when running in the cache or the ``output folder`` when running locally)
with the value of ``folders.source`` if declared in the ``layout()`` method.

Note that the base directory for the ``source_folder`` when running in the cache will point to the base folder of the
build unless :ref:`no_copy_source<conan_conanfile_properties_no_copy_source>` is set to ``True``. But anyway it will
always point to the correct folder where the source code is.


export_sources_folder
---------------------

The value depends on the method you access it:

- At ``source(self)``: Points to the base source folder (that means self.source_folder but
  without taking into account the ``folders.source`` declared in the ``layout()`` method).
  The declared `exports_sources` are copied to that base source folder always.
- At ``exports_sources(self)``: Points to the folder in the cache where the export sources
  have to be copied.

.. seealso::

    - :ref:`Read about the export_sources() method<reference_conanfile_methods_export_sources>`.
    - :ref:`Read about the source() method<reference_conanfile_methods_source>`.

.. _attribute_build_folder:

build_folder
------------

The folder used to build the source code. The path is built joining the base directory (a cache
directory when running in the cache or the ``output folder`` when running locally) with
the value of ``folders.build`` if declared in the ``layout()`` method.


.. _attribute_generators_folder:

generators_folder
-----------------

The folder where the files in the ``generate()`` method should be generated. The path is built
from the layout's ``self.folders.generators`` attribute.

.. _conan_conanfile_properties_package_folder:

package_folder
--------------

The folder to copy the final artifacts for the binary package. In the local cache a package
folder is created for every different package ID.

The most common usage of ``self.package_folder`` is to ``copy`` the files
at the :ref:`package() method<reference_conanfile_methods_package>`:

.. code-block:: python

   import os
   from conan import ConanFile
   from conan.tools.files import copy

   class MyRecipe(ConanFile):
       ...

       def package(self):
           copy(self, "*.so", self.build_folder, os.path.join(self.package_folder, "lib"))
           ...


recipe_folder
-------------

The folder where the recipe *conanfile.py* is stored, either in the local folder or in
the cache. This is useful in order to access files that are exported along with the recipe,
or the origin folder when exporting files in ``export(self)`` and ``export_sources(self)``
methods.

The most common usage of ``self.recipe_folder`` is in the ``export(self)`` and ``export_sources(self)`` methods,
as the folder from where we copy the files:

.. code-block:: python

   from conan import ConanFile
   from conan.tools.files import copy

   class MethodConan(ConanFile):
       exports = "file.txt"
       def export(self):
           copy(self, "LICENSE.md", self.recipe_folder, self.export_folder)


recipe_metadata_folder
----------------------

The ``self.recipe_metadata_folder`` (**experimental**) can be used in the ``export()`` and ``export_sources()`` and ``source()`` methods
to save or copy **recipe** metadata files. See :ref:`metadata section<devops_metadata>` for more information.


package_metadata_folder
-----------------------

The ``self.package_metadata_folder`` (**experimental**)  can be used in the ``generate()``, ``build()`` and ``package()`` methods
to save or copy **package** metadata files. See :ref:`metadata section<devops_metadata>` for more information.



.. _conan_conanfile_properties_no_copy_source:

no_copy_source
--------------

The attribute ``no_copy_source`` tells the recipe that the source code will not be copied from
the ``source_folder`` to the ``build_folder``. This is mostly an optimization for packages
with large source codebases or header-only, to avoid extra copies.


If you activate ``no_copy_source=True``, it is **mandatory** that the source code must not be modified at all by
the configure or build scripts, as the source code will be shared among all builds.

The recipes should always use ``self.source_folder`` attribute, which will point to the ``build``
folder when ``no_copy_source=False`` and will point to the ``source`` folder when ``no_copy_source=True``.

.. seealso::

    Read  :ref:`header-only packages section <creating_packages_other_header_only>` for an
    example using ``no_copy_source`` attribute.


.. _conan_conanfile_attributes_test_package_folder:

test_package_folder
-------------------

The ``test_package_folder`` class attribute allows defining in recipe a different default
``test_package`` folder for ``conan create`` commands.
When a ``conan create`` runs, after the package is created in the cache, it will look for
a ``test_package`` folder, or for the folder specified in the ``--test-folder=xxx`` argument,
and launch the package test.

This attribute allows to change that default name:

.. code-block:: python

  import os
  from conan import ConanFile

  class Pkg(ConanFile):
      test_package_folder = "my/test/folder"


It allows to define any folder, always relative to the location of the ``conanfile.py``.
