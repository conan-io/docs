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


layouts
-------

The ``layouts`` attribute has to be set only in the ``layout()`` method. Please check the
:ref:`layout() method documentation<layout_cpp_reference>` to learn more about this
attribute.

The ``layouts`` attribute contains information about environment variables and ``conf`` that
would be path-dependent, and as a result it would contain a different value when the package
is in editable mode, or when the package is in the cache. The ``layouts`` sub-attributes are:

- ``self.layouts.build``: information related to the relative ``self.folders.build``
- ``self.layouts.source``: information related to the relative ``self.folders.source``
- ``self.layouts.package``: information related to the final ``package_folder``

Each one of those will contain:

- ``buildenv_info``: environment variables build information for consumers (equivalent to ``self.buildenv_info`` in ``package_info()``)
- ``runenv_info``: environment variables run information for consumers (equivalent to ``self.runenv_info`` in ``package_info()``)
- ``conf_info``: configuration information for consumers (equivalent to ``self.conf_info`` in ``package_info()``). Note this is
  only automatically propagated to ``self.conf`` of consumers when this package is a direct ``tool_require``.

For example, if we had an ``androidndk`` recipe that contais the AndroidNDK, and we want to have that recipe in "editable" mode,
it is necessary where the androidndk will be locally, before being in the created package:

.. code-block:: python

  import os
  from conan import ConanFile
  from conan.tools.files import copy

  class AndroidNDK(ConanFile):

      def layout(self):
          # When developing in user space it is in a "mybuild" folder (relative to current dir)
          self.layouts.build.conf_info.define_path("tools.android:ndk_path", "mybuild")
          # but when packaged it will be in a "mypkg" folder (inside the cache package folder)
          self.layouts.package.conf_info.define_path("tools.android:ndk_path", "mypkg")

      def package(self):
          copy(self, "*", src=os.path.join(self.build_folder, "mybuild"),
               dst=os.path.join(self.package_folder, "mypkg"))
