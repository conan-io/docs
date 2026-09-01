.. _reference_conanfile_methods_finalize:

finalize()
==========

.. include:: ../../../common/experimental_warning.inc

Package immutability is an important concept in Conan. It ensures that the package is not modified after it has been built and packaged,
so that the package id is consistent and the package can be reused in different machines.

This method is intended for customization of the package in the running machine, allowing modifications to the package
that will be used by the consumers of the package, but not modifying the original package inside the Conan cache.
This method is called after the package has been installed in the local cache and
the modifications are not uploaded to any remote server, they are only local.


The main use-cases of this method include:

- Having different packages that get modified when they are run (Like python tools that generate pycache files as part
  of their execution)
- Modifying the package to be used in the local machine (Like creating a ``conf`` file with the necessary
  environment variables for the package to be used in the local machine)

These changes are transparent to the consumers of the package, they will use the customized package as if they were dealing with the original package,
so changes made in this method should work.


finalize() example usage
------------------------

The most common use-case of this method is to avoid corrupting the immutability of the package.

For example, if a package generates some files during its execution, like a python package that generates pycache files,
you can use this method to generate those files in the local machine, without affecting the original package.
This is the case for tools like Meson.


.. code-block:: python

   from conan import ConanFile, conan_version
   from conan.tools.files import copy


   class MesonPackage(ConanFile):
       ...

       def package(self):
           copy(self, "*", src=self.source_folder, dst=os.path.join(self.package_folder, "bin"))
           ...

       def finalize(self):
           copy(self, "*", src=self.immutable_package_folder, dst=self.package_folder)


Here we are copying the files from the immutable package folder to the finalized package folder,
which inside the finalize method (and everywhere after that point) will be the new package folder,
so that any modifications done by the package are done in the local finalized folder, without affecting the original package.

For cases where it's necessary to access the original package, the ``immutable_package_folder`` attribute is available
both in the same recipe's ``self.immutable_package_folder`` and
thru the ``self.dependencies[<package_name>].immutable_package_folder`` attribute in the dependants' recipe.
This info is also serialized as part of the graph information in :command:`conan graph info` etc.

As this method must have a 1 to 1 correspondence to the generated package id,
access to ``self.settings``, ``self.options`` and ``self.cpp_info`` is forbidden inside the ``finalize()`` method, 
and **must** be done thru the ``self.info`` attribute.

.. note::

  Without using this approach, the package would generate the pycache files in the package folder,
  and thus there would be a need to set ``PYTHONDONTWRITEBYTECODE`` to avoid mutating the package, but this would affect performance,
  and performing cache integrity checks either thru :command:`conan cache check-integrity` or as part of the upload processes
  in :command:`conan upload ... --check` would raise errors if the modified package was ever checked.


.. warning::

  This is not a replacement for the :ref:`post_package <reference_extensions_hooks>` hook.
  The hook runs after the creation of the package for a chance to modify it before the package_id is computed,
  but it is not intended for modifications of the package for a particular running machine.
