.. _examples_conanfile_layout_multiple_subprojects:

Example: Multiple subprojects
-----------------------------

Lets say that we have a project that contains multiple subprojects, and some of these subprojects need
to access some information that is at their same level (sibling folders). Each subproject would be 
a Conan package.

So we have the following folders and files:

..  code-block:: text

    ├── pkg
    │    ├── conanfile.py
    │    ├── app.cpp  # contains an #include "../common/myheader.h"
    │    └── CMakeLists.txt # contains include(../common/myutils.cmake)
    ├── common
    │    ├── myutils.cmake
    │    └── myheader.h
    └── othersubproject


The ``pkg`` subproject needs to use some of the files located inside the ``common`` folder (that might be
used and shared by other subprojects too), and it references them by their relative location.
Note that ``common`` is not intended to be a Conan package. It is just some common code that will be copied
into the different subproject packages.

We can use the ``self.folders.root = ".."`` layout specifier to locate the root of the project, then
use the ``self.folders.subproject = "subprojectfolder"`` to relocate back most of the layout to the
current subproject folder, as it would be the one containing the build scripts, sources code, etc.,
so other helpers like ``cmake_layout()`` keep working.


..  code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.cmake import cmake_layout, CMake
    from conan.tools.files import load, copy, save

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeToolchain"

        def layout(self):
            self.folders.root = ".."
            self.folders.subproject = "pkg"
            cmake_layout(self)

        def export_sources(self):
            source_folder = os.path.join(self.recipe_folder, "..")
            copy(self, "*", source_folder, self.export_sources_folder)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            self.run(os.path.join(self.cpp.build.bindirs[0], "myapp"))


Note it is very important the ``export_sources()`` method, that is able to maintain the same relative layout
of the ``pkg`` and ``common`` folders, both in the local developer flow in the current folder, but also
when those sources are copied to the Conan cache, to be built there with ``conan create`` or ``conan install --build=pkg``.
This is one of the design principles of the ``layout()``, the relative location of things must be consistent in the user
folder and in the cache.
