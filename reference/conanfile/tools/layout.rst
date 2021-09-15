.. _conan_tools_layout:

conan.tools.layout
==================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.
    The ``layout()`` feature will be fully functional only in the new build system integrations
    (:ref:`in the conan.tools space <conan_tools>`). If you are using other integrations, they
    might not fully support this feature.


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

.. _conan_tools_layout_predefined_layouts:

Predefined layouts
------------------

There are some pre-defined common layouts, ready to be simply used in recipes.

For example, this would implement the standard CMake project layout:

.. code:: python

    from conan.tools.layout import cmake_layout

    def layout(self):
        cmake_layout(self)

If you want to try it, use the ``conan new hello/0.1 --template=cmake_lib`` template.

It is very important to note that this ``cmake_layout()`` is just calling the ``folders`` and ``cpp``
attributes described before:


.. code:: python

    def cmake_layout(conanfile, generator=None):
        gen = conanfile.conf["tools.cmake.cmaketoolchain:generator"] or generator
        if gen:
            multi = "Visual" in gen or "Xcode" in gen or "Multi-Config" in gen
        elif conanfile.settings.compiler == "Visual Studio" or conanfile.settings.compiler == "msvc":
            multi = True
        else:
            multi = False

        conanfile.folders.source = "."
        if multi:
            conanfile.folders.build = "build"
            conanfile.folders.generators = "build/conan"
        else:
            build_type = str(conanfile.settings.build_type).lower()
            conanfile.folders.build = "cmake-build-{}".format(build_type)
            conanfile.folders.generators = os.path.join(conanfile.folders.build, "conan")

        conanfile.cpp.source.includedirs = ["src"]
        if multi:
            conanfile.cpp.build.libdirs = ["{}".format(conanfile.settings.build_type)]
            conanfile.cpp.build.bindirs = ["{}".format(conanfile.settings.build_type)]
        else:
            conanfile.cpp.build.libdirs = ["."]
            conanfile.cpp.build.bindirs = ["."]

First, it is important to notice that the layout depends on the CMake generator that will be used.
So if defined from ``[conf]``, that value will be used. If defined in recipe, then the recipe should
pass it as ``cmake_layout(self, cmake_generator)``.

The definitions of the folders is different if it is a multi-config generator (like Visual Studio or Xcode),
or a single-config generator (like Unix Makefiles). In the first case, the folder is the same irrespective
of the build type, and the build system will manage the different build types inside that folder. But
single-config generators like Unix Makefiles, must use a different folder for each different configuration
(as a different build_type Release/Debug).

Finally, the location where the libraries are created also depends. For multi-config, the respective libraries
will be located in a dedicated folder inside the build folder, while for single-config, the libraries will
be located directly in the build folder.

This helper defines a few things, for example that the source folder is called ``"."``, meaning that Conan will
search the main `CMakeLists.txt` in the same directory were the conanfile is (most likely the project root).
This could be customized without fully changing the layout:

    def layout(self):
        cmake_layout(self)
        self.folders.source = "mysrcfolder"


Even if this pre-defined layout doesn't suit your specific projects layout, it is a good example how you could
implement your own logic (and probably put it in a common ``python_require`` if you are going to use it in multiple
packages).
