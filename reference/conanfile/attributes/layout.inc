Layout
++++++

.. _conan_conanfile_attributes_folders:

folders
-------

The ``folders`` attribute has to be set only in the ``layout()`` method. Please check the
:ref:`layout() method documentation<layout_folders_reference>` to learn more about this
attribute.



.. _conan_conanfile_attributes_cpp:

cpp
---

Object storing all the information needed by the consumers
of a package: include directories, library names, library paths... Both for editable
and regular packages in the cache. It is only available at the ``layout()`` method.

- ``self.cpp.package``: For a regular package being used from the Conan cache. Same as
  declaring ``self.cpp_info`` at the ``package_info()`` method.
- ``self.cpp.source``: For "editable" packages, to describe the artifacts under
  ``self.source_folder``
- ``self.cpp.build``: For "editable" packages, to describe the artifacts under
  ``self.build_folder``.


The ``cpp`` attribute has to be set only in the ``layout()`` method. Please check the
:ref:`layout() method documentation<layout_cpp_reference>` to learn more about this
attribute.
