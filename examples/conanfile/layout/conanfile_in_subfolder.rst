.. _examples_conanfile_layout_conanfile_in_subfolder:

Example: conanfile in subfolder
-------------------------------

If we have this project, intended to package the code that is in the same repo as the ``conanfile.py``, but
the ``conanfile.py`` is not in the root of the project:

..  code-block:: text

    ├── CMakeLists.txt
    └── conan
        └── conanfile.py


The ``conanfile.py`` would look like this:

..  code-block:: python

      import os
      from conan import ConanFile
      from conan.tools.files import load, copy


      class Pkg(ConanFile):
          name = "pkg"
          version = "0.1"

          def layout(self):
              # The root of the project is one level above
              self.folders.root = ".." 
              # The source of the project (the root CMakeLists.txt) is the source folder
              self.folders.source = "."  
              self.folders.build = "build"
        
          def export_sources(self):
              # The path of the CMakeLists.txt we want to export is one level above
              folder = os.path.join(self.recipe_folder, "..")
              copy(self, "*.txt", folder, self.export_sources_folder)
          
          def source(self):
              # we can see that the CMakeLists.txt is inside the source folder
              cmake = load(self, "CMakeLists.txt")

          def build(self):
              # The build() method can also access the CMakeLists.txt in the source folder
              path = os.path.join(self.source_folder, "CMakeLists.txt")
              cmake = load(self, path)
