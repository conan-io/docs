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

There are some pre-defined common layouts, ready to be simply used in recipes:

- ``cmake_layout()``: :ref:`a layout for a typical CMake project <cmake_layout>`
- ``meson_layout()``: :ref:`a layout for a typical Meson project <meson_layout>`
- ``vs_layout()``: a layout for a typical Visual Studio project


The predefined layouts define a few things, for example in the ``cmake_layout()`` the source folder is  called ``"."``, meaning that Conan will
expect the sources in the same directory where the conanfile is (most likely the project root, where a ``CMakeLists.txt`` file will be typically found).
This could be customized without fully changing the layout:

.. code:: python

    def layout(self):
        cmake_layout(self)
        self.folders.source = "mysrcfolder"


Even if this pre-defined layout doesn't suit your specific projects layout, checking how they implement their logic
shows how you could implement your own logic (and probably put it in a common ``python_require`` if you are going to use it in multiple
packages).
