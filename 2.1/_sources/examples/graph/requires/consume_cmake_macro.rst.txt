.. _consume_cmake_macro:
    
Use a CMake macro packaged in a dependency
------------------------------------------

When a package recipe wants to provide a CMake functionality via a macro, it can be done as follows.
Let's say that we have a ``pkg`` recipe, that will "export" and "package" a ``Macros.cmake`` file
that contains a ``pkg_macro()`` CMake macro:


.. code-block:: python
    :caption: pkg/conanfile.py

    from conan import ConanFile
    from conan.tools.files import copy

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"
        package_type = "static-library"
        # Exporting, as part of the sources
        exports_sources = "*.cmake"

        def package(self):
            # Make sure the Macros.cmake is packaged
            copy(self, "*.cmake", src=self.source_folder, dst=self.package_folder)
    
        def package_info(self):
            # We need to define that there are "build-directories", in this case
            # the current package root folder, containing build files and scripts
            self.cpp_info.builddirs = ["."]

.. code-block:: cmake
    :caption: pkg/Macros.cmake

    function(pkg_macro)
        message(STATUS "PKG MACRO WORKING!!!")
    endfunction()

When this package is created (``cd pkg && conan create .``), it can be consumed by other package
recipes, for example this application:

.. code-block:: python
    :caption: app/conanfile.py

    from conan import ConanFile
    from conan.tools.cmake import CMake
    
    class App(ConanFile):
        package_type = "application"
        generators = "CMakeToolchain"
        settings = "os", "compiler", "arch", "build_type"
        requires = "pkg/0.1"

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

That has this ``CMakeLists.txt``:

.. code-block:: cmake
    :caption: app/CMakeLists.txt

    cmake_minimum_required(VERSION 3.15)
    project(App LANGUAGES NONE)

    include(Macros)  # include the file with the macro (note no .cmake extension)
    pkg_macro()  # call the macro


So when we run a local build, we will see how the file is included and the macro called:


.. code-block:: bash

    $ cd app
    $ conan build .
    PKG MACRO WORKING!!!
