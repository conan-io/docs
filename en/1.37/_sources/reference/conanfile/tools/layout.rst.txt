.. _conan_tools_layout:

conan.tools.layout
==================

Available since: `1.37.0 <https://github.com/conan-io/conan/releases>`_

LayoutPackager
--------------

The ``LayoutPackager`` together with the :ref:`package layouts<package_layout>` feature, allow to automatically
package the files following the declared information in the ``layout()`` method:

It will copy (being xxx => ``build`` and ``source`` (if destination is only one dir):

- Files from ``self.cpp.xxx.includedirs`` to ``self.cpp.package.includedirs`` matching ``self.patterns.xxx.include`` patterns.
- Files from ``self.cpp.xxx.libdirs`` to ``self.cpp.package.libdirs`` matching ``self.patterns.xxx.lib`` patterns.
- Files from ``self.cpp.xxx.bindirs`` to ``self.cpp.package.bindirs`` matching ``self.patterns.xxx.bin`` patterns.
- Files from ``self.cpp.xxx.srcdirs`` to ``self.cpp.package.srcdirs`` matching ``self.patterns.xxx.src`` patterns.
- Files from ``self.cpp.xxx.builddirs`` to ``self.cpp.package.builddirs`` matching ``self.patterns.xxx.build`` patterns.
- Files from ``self.cpp.xxx.resdirs`` to ``self.cpp.package.resdirs`` matching ``self.patterns.xxx.res`` patterns.
- Files from ``self.cpp.xxx.frameworkdirs`` to ``self.cpp.package.frameworkdirs`` matching ``self.patterns.xxx.framework`` patterns.


Usage:

.. code:: python

        from conans import ConanFile
        from conan.tools.layout import LayoutPackager

        class Pkg(ConanFile):

            def layout(self):
                ...

            def package(self):
                LayoutPackager(self).package()
