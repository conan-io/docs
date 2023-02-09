.. _examples_conanfile_layout_third_party_libraries:

Declaring the layout when creating packages for third-party libraries
---------------------------------------------------------------------

Please, first of all, clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/conanfile/layout/third_party_libraries


If we have this project, intended to create a package for a third-party library which code
is located externally:

..  code-block:: text

    .
    ├── conanfile.py
    └── patches
        └── mypatch

The ``conanfile.py`` would look like this:

..  code-block:: python

    ...
    
    class Pkg(ConanFile):
        name = "hello"
        version = "1.0"
        exports_sources = "patches*"

        ...

        def layout(self):
            cmake_layout(self, src_folder="src")
            # if you are declaring your own layout, just declare:
            # self.folders.source = "src"
        
        def source(self):
            # we are inside a "src" subfolder, as defined by layout
            # the downloaded soures will be inside the "src" subfolder
            get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", 
                strip_root=True)

            # patching, replacing, happens here
            patch(self, patch_file=os.path.join(self.export_sources_folder, "patches/mypatch"))

        def build(self):
            # If necessary, the build() method also has access to the export_sources_folder
            # for example if patching happens in build() instead of source()
            #patch(self, patch_file=os.path.join(self.export_sources_folder, "patches/mypatch"))
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            ...


We can see that the ``ConanFile.export_sources_folder`` can provide access to the root
folder of the sources:

- Locally it will be the folder where the ``conanfile.py`` lives
- In the cache it will be the "source" folder, that will contain a copy of
  ``CMakeLists.txt`` and ``patches``, while the "source/src" folder will contain the
  actual downloaded sources.

.. seealso::

    - Read more about the :ref:`layout method<conanfile_methods_layout>` and :ref:`how the
      package layout works<tutorial_package_layout>`.
