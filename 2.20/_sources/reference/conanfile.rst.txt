.. _conanfile_reference:

conanfile.py
============


The ``conanfile.py`` is the recipe file of a package, responsible for defining how to build it and consume it.

   .. code-block:: python

       from conan import ConanFile

       class HelloConan(ConanFile):
           ...


.. important::

    *conanfile.py* recipes use a variety of attributes and methods to operate. In order to avoid
    collisions and conflicts, follow these rules:

    - Public attributes and methods, like ``build()``, ``self.package_folder``, are reserved for Conan.
      Don't use public members for custom fields or methods in the recipes.
    - Use "protected" access for your own members, like ``self._my_data`` or ``def _my_helper(self):``.
      Conan only reserves "protected" members starting with ``_conan``.



Contents:

.. toctree::
   :maxdepth: 2

   conanfile/attributes
   conanfile/methods
   conanfile/running_and_output
