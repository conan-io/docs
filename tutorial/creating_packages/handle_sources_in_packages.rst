.. _creating_packages_handle_sources_in_packages:

Handle sources in packages
==========================

In the :ref:`previous tutorial
section<creating_packages_create_your_first_conan_package>`, we created a Conan package
for a "Hello World" C++ library. We used the ``exports_sources`` attribute of the
Conanfile to declare the location of the sources for the library. Using this method is the
simplest way to do declare their location when the sources are in the same folder as the
Conanfile. However, sometimes the sources are stored in a repository or a file in a remote
server and not in the same location as the Conanfile. In this section we will modify the
recipe we created previously to retrieve the same sources from other repository or a
remote server using the ``source()`` method.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/handle_sources

The structure of the project is the same as the one of the previous example but without
the library sources:

.. code-block:: text

    .
    ├── CMakeLists.txt
    ├── conanfile.py
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── src
            └── example.cpp

Let's have a look at the changes in the *conanfile.py*:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
    from conan.tools.files import get


    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def source(self):
            get(self, "https://github.com/czoido/hello/archive/refs/heads/update_source.zip", 
                      strip_root=True)

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC

        def layout(self):
            cmake_layout(self)

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            cmake = CMake(self)
            cmake.install()

        def package_info(self):
            self.cpp_info.libs = ["hello"]

As you can see, the recipe is exactly the same but instead declaring the ``exports_sources``
attribute as we did previously:

.. code-block:: python

    exports_sources = "CMakeLists.txt", "src/*", "include/*"


Now we declare a ``source()`` method with this information:

.. code-block:: python

    def source(self):
        get(self, "https://github.com/czoido/hello/archive/refs/heads/update_source.zip", 
                  strip_root=True)

As you can see we used the :ref:`conan.tools.files.get()<conan_tools_files_get>` tool that
will first **download** the url of the zip file that we pass as an argument and then
**unzip** it. Note that we are passing ``strip_root=True`` so that if all the unzipped
contents are in a single folder all the contents are moved to the parent folder (check the
:ref:`conan.tools.files.unzip()<conan_tools_files_unzip>` reference for more details).
