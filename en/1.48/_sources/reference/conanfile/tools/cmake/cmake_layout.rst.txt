.. _cmake_layout:

cmake_layout
------------

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.


For example, this would implement the standard CMake project layout:

.. code:: python

    from conan.tools.cmake import cmake_layout

    def layout(self):
        cmake_layout(self)


If you want to try it, use the ``conan new hello/0.1 --template=cmake_lib`` template.

It is very important to note that this ``cmake_layout()`` is just calling the ``folders`` and ``cpp``
attributes described in the (:ref:`layout reference <layout_folders_reference>`).

This is the implementation of ``cmake_layout()``:


.. code:: python

    def cmake_layout(conanfile, generator=None, src_folder="."):
        gen = conanfile.conf.get("tools.cmake.cmaketoolchain:generator", default=generator)
        if gen:
            multi = "Visual" in gen or "Xcode" in gen or "Multi-Config" in gen
        else:
            compiler = conanfile.settings.get_safe("compiler")
            if compiler in ("Visual Studio", "msvc"):
                multi = True
            else:
                multi = False

        conanfile.folders.source = src_folder
        try:
            build_type = str(conanfile.settings.build_type)
        except ConanException:
            raise ConanException("'build_type' setting not defined, it is necessary for cmake_layout()")
        if multi:
            conanfile.folders.build = "build"
        else:
            build_type = build_type.lower()
            conanfile.folders.build = "cmake-build-{}".format(build_type)

        conanfile.folders.generators = "build/generators"
        conanfile.cpp.source.includedirs = ["include"]

        if multi:
            conanfile.cpp.build.libdirs = ["{}".format(build_type)]
            conanfile.cpp.build.bindirs = ["{}".format(build_type)]
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

Nevertheless, the ``conanfile.folders.generators`` folder containing
the saved files from the generators (CMakeDeps, CMakeToolchain...) is always at ``build/generators`` because they
support multi-configuration. That is, you can run :command:`conan install . -s build_type=Debug` and
:command:`conan install . -s build_type=Release` and the generated files will coexist at the ``build/generators`` without any issue.

Finally, the location where the libraries are created also depends. For multi-config, the respective libraries
will be located in a dedicated folder inside the build folder, while for single-config, the libraries will
be located directly in the build folder.

This helper defines a few things, for example that the source folder is called ``"."`` by default, meaning that
Conan will expect the sources in the same directory were the conanfile is (most likely the project root). If you have
a different folder where the ``CMakeLists.txt`` is located, for example, when creating a package for an external library,
you can use the ``src_folder`` argument:


.. code:: python

    def layout(self):
        cmake_layout(self, src_folder="subfolder")

