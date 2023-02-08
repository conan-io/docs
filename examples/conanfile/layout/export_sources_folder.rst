.. _examples_conanfile_layout_export_sources_folder:

Example: export_sources_folder
------------------------------

If we have this project, intended to create a package for a third-party library which code is located externally:

..  code-block:: text

    ├── conanfile.py
    ├── patches
    │   └── mypatch
    └── CMakeLists.txt


The ``conanfile.py`` would look like this:

..  code-block:: python

      import os
      from conan import ConanFile


      class Pkg(ConanFile):
          name = "pkg"
          version = "0.1"
          exports_sources = "CMakeLists.txt", "patches*"

          def layout(self):
              self.folders.source = "src"
          
          def source(self):
              # we are inside a "src" subfolder, as defined by layout
              # download something, that will be inside the "src" subfolder
              # access to patches and CMakeLists, to apply them, replace files is done with:
              mypatch_path = os.path.join(self.export_sources_folder, "patches/mypatch")
              cmake_path = os.path.join(self.export_sources_folder, "CMakeLists.txt")
              # patching, replacing, happens here

          def build(self):
              # If necessary, the build() method also has access to the export_sources_folder
              # for example if patching happens in build() instead of source()
              cmake_path = os.path.join(self.export_sources_folder, "CMakeLists.txt")


We can see that the ``ConanFile.export_sources_folder`` can provide access to the root folder of the sources:

- Locally it will be the folder where the ``conanfile.py`` lives
- In the cache it will be the "source" folder, that will contain a copy of ``CMakeLists.txt`` and ``patches``,
  while the "source/src" folder will contain the actual downloaded sources.
