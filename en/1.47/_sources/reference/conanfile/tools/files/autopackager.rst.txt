.. _conan_tools_files_autopackager:

conan.tools.files.AutoPackager
------------------------------

The ``AutoPackager`` together with the :ref:`package layouts<package_layout>` feature, allow to automatically
package the files following the declared information in the ``layout()`` method:

It will copy:

- Files from ``self.cpp.local.includedirs`` to ``self.cpp.package.includedirs``
- Files from ``self.cpp.local.libdirs`` to ``self.cpp.package.libdirs``
- Files from ``self.cpp.local.bindirs`` to ``self.cpp.package.bindirs``
- Files from ``self.cpp.local.srcdirs`` to ``self.cpp.package.srcdirs``
- Files from ``self.cpp.local.builddirs`` to ``self.cpp.package.builddirs``
- Files from ``self.cpp.local.resdirs`` to ``self.cpp.package.resdirs``
- Files from ``self.cpp.local.frameworkdirs`` to ``self.cpp.package.frameworkdirs``

The patterns of the files to be copied can be defined with the `.patterns` property of the ``AutoPackager`` instance.
The default patterns are:

.. code:: python

        packager = AutoPackager(self)
        packager.patterns.include == ["*.h", "*.hpp", "*.hxx"]
        packager.patterns.lib == ["*.so", "*.so.*", "*.a", "*.lib", "*.dylib"]
        packager.patterns.bin == ["*.exe", "*.dll"]
        packager.patterns.src == []
        packager.patterns.build == []
        packager.patterns.res == []
        packager.patterns.framework == []

Usage:

.. code:: python

        from conans import ConanFile
        from conan.tools.files import AutoPackager

        class Pkg(ConanFile):

            def layout(self):
                ...

            def package(self):
                packager = AutoPackager(self)
                packager.patterns.include = ["*.hpp", "*.h", "include3.h"]
                packager.patterns.lib = ["*.a"]
                packager.patterns.bin = ["*.exe"]
                packager.patterns.src = ["*.cpp"]
                packager.patterns.framework = ["sframe*", "bframe*"]
                packager.run()
