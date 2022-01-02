.. _conan_tools_layout:

conan.tools.layout
==================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.
    The ``layout()`` feature will be fully functional only in the new build system integrations
    (:ref:`in the conan.tools space <conan_tools>`). If you are using other integrations, they
    might not fully support this feature.

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

        conanfile.cpp.local.includedirs = ["src"]
        if multi:
            _dir = os.path.join(conanfile.folders.build, str(conanfile.settings.build_type))
            conanfile.cpp.local.libdirs = [_dir]
            conanfile.cpp.local.bindirs = [_dir]
        else:
            conanfile.cpp.local.libdirs = [conanfile.folders.build]
            conanfile.cpp.local.bindirs = [conanfile.folders.build]

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
expect the sources in the same directory were the conanfile is (most likely the project root).
This could be customized without fully changing the layout:


.. code:: python

    def layout(self):
        cmake_layout(self)
        self.folders.source = "mysrcfolder"


Even if this pre-defined layout doesn't suit your specific projects layout, it is a good example how you could
implement your own logic (and probably put it in a common ``python_require`` if you are going to use it in multiple
packages).
