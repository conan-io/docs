.. _examples_conanfile_layout_conanfile_in_subfolder:

Declaring the layout when the Conanfile is inside a subfolder
-------------------------------------------------------------

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/conanfile/layout/conanfile_in_subfolder

If we have a project intended to package the code that is in the same repo as the
``conanfile.py``, but the ``conanfile.py`` is not in the root of the project:

..  code-block:: text

    .
    ├── CMakeLists.txt
    ├── conan
    │   └── conanfile.py
    ├── include
    │   └── say.h
    └── src
        └── say.cpp

The ``conanfile.py`` would look like this:

..  code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.files import load, copy
    from conan.tools.cmake import CMake


    class PkgSay(ConanFile):
        name = "say"
        version = "1.0"
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeToolchain"

        def layout(self):
            # The root of the project is one level above
            self.folders.root = ".." 
            # The source of the project (the root CMakeLists.txt) is the source folder
            self.folders.source = "."  
            self.folders.build = "build"

        def export_sources(self):
            # The path of the CMakeLists.txt and sources we want to export are one level above
            folder = os.path.join(self.recipe_folder, "..")
            copy(self, "*.txt", folder, self.export_sources_folder)
            copy(self, "src/*.cpp", folder, self.export_sources_folder)
            copy(self, "include/*.h", folder, self.export_sources_folder)
        
        def source(self):
            # Check that we can see that the CMakeLists.txt is inside the source folder
            cmake_file = load(self, "CMakeLists.txt")

        def build(self):
            # Check that the build() method can also access the CMakeLists.txt in the source folder
            path = os.path.join(self.source_folder, "CMakeLists.txt")
            cmake_file = load(self, path)

            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            cmake = CMake(self)
            cmake.install()

You can try and create the ``say`` package:

..  code-block:: bash

    $ cd conan
    $ conan create .

.. seealso::

    - :ref:`layout method<reference_conanfile_methods_layout>`
    - :ref:`how the package layout works<tutorial_package_layout>`.
