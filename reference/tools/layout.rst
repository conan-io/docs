.. _conan_tools_layout:

conan.tools.layout
==================

.. _conan_tools_layout_predefined_layouts:

Predefined layouts
------------------

There are some pre-defined common :ref:`layouts<reference_conanfile_methods_layout>`, ready to be simply used in recipes:

- ``cmake_layout()``: :ref:`a layout for a typical CMake project <cmake_layout>`
- ``vs_layout()``: a layout for a typical Visual Studio project
- ``basic_layout()``: :ref:`a very basic layout for a generic project <conan_tools_basic_layout>`

The pre-defined layouts define the Conanfile ``.folders`` and ``.cpp`` attributes with
typical values. To check which values are set by these pre-defined layouts please
check the reference for the :ref:`layout()<reference_conanfile_methods_layout>` method. For example in the
``cmake_layout()`` the source folder is set to ``"."``, meaning that Conan will expect
the sources in the same directory where the conanfile is (most likely the project root,
where a ``CMakeLists.txt`` file will be typically found). If you have a different folder
where the ``CMakeLists.txt`` is located, you can use the ``src_folder`` argument:

.. code:: python
    
    from conan.tools.cmake import cmake_layout

    def layout(self):
        cmake_layout(self, src_folder="mysrcfolder")


Even if this pre-defined layout doesn't suit your specific projects layout, checking how
they implement their logic shows how you could implement your own logic (and probably put
it in a common ``python_require`` if you are going to use it in multiple packages).


To learn more about the layouts and how to use them while developing packages, please
check the Conan package layout :ref:`tutorial <developing_packages_layout>`.

.. _conan_tools_basic_layout:

basic_layout
------------

Usage:

.. code:: python

    from conan.tools.layout import basic_layout

    def layout(self):
        basic_layout(self)


The current layout implementation is very simple, basically sets a different build folder for different build_types
and sets the generators output folder inside the build folder. This way we avoid to clutter our project
while working locally. If you prefer, you can define the `build_folder` to take control over the destination folder,
so the temporary build files do not pollute the source tree.


.. code:: python

    def basic_layout(conanfile, src_folder=".", build_folder=None):
        subproject = conanfile.folders.subproject

        conanfile.folders.source = src_folder if not subproject else os.path.join(subproject, src_folder)
        if build_folder:
            conanfile.folders.build = build_folder if not subproject else os.path.join(subproject, build_folder)
        else:
            conanfile.folders.build = "build" if not subproject else os.path.join(subproject, "build")
            if conanfile.settings.get_safe("build_type"):
                conanfile.folders.build += "-{}".format(str(conanfile.settings.build_type).lower())
        conanfile.folders.generators = os.path.join(conanfile.folders.build, "conan")
        conanfile.cpp.build.bindirs = ["."]
        conanfile.cpp.build.libdirs = ["."]
