.. _examples_conanfile_layout_components_editables:

Using components and editable packages
--------------------------------------

It is possible to define components in the ``layout()`` method, to support the case of ``editable`` packages.
That is, if we want to put a package in ``editable`` mode, and that package defines ``components``, it is 
necessary to define the components layout correctly in the ``layout()`` method.  
Let's see it in a real example.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/conanfile/layout/editable_components

There we find a ``greetings`` subfolder and package, that contains 2 libraries, the ``hello`` library and the
``bye`` library. Each one is modeled as a ``component`` inside the package recipe:

.. code-block:: python
    :caption: greetings/conanfile.py

    class GreetingsConan(ConanFile):
        name = "greetings"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeDeps", "CMakeToolchain"
        exports_sources = "src/*"

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def layout(self):
            cmake_layout(self, src_folder="src")
            # This "includedirs" starts in the source folder, which is "src"
            # So the components include dirs is the "src" folder (includes are
            # intended to be included as ``#include "hello/hello.h"``)
            self.cpp.source.components["hello"].includedirs = ["."]
            self.cpp.source.components["bye"].includedirs = ["."]
            # compiled libraries "libdirs" will be inside the "build" folder, depending
            # on the platform they will be in "build/Release" or directly in "build" folder
            bt = "." if self.settings.os != "Windows" else str(self.settings.build_type)
            self.cpp.build.components["hello"].libdirs = [bt]
            self.cpp.build.components["bye"].libdirs = [bt]

        def package(self):
            copy(self, "*.h", src=self.source_folder, 
                 dst=join(self.package_folder, "include"))
            copy(self, "*.lib", src=self.build_folder,
                 dst=join(self.package_folder, "lib"), keep_path=False)
            copy(self, "*.a", src=self.build_folder,
                 dst=join(self.package_folder, "lib"), keep_path=False)

        def package_info(self):
            self.cpp_info.components["hello"].libs = ["hello"]
            self.cpp_info.components["bye"].libs = ["bye"]

            self.cpp_info.set_property("cmake_file_name", "MYG")
            self.cpp_info.set_property("cmake_target_name", "MyGreetings::MyGreetings")
            self.cpp_info.components["hello"].set_property("cmake_target_name", "MyGreetings::MyHello")
            self.cpp_info.components["bye"].set_property("cmake_target_name", "MyGreetings::MyBye")

While the location of the ``hello`` and ``bye`` libraries in the final package is in the final ``lib`` folder,
then nothing special is needed in the ``package_info()`` method, beyond the definition of the components. In
this case, the customization of the CMake generated filenames and targets is also included, but it is not 
necessary for this example.

The important part is the ``layout()`` definition. Besides the common ``cmake_layout``, it is necessary to
define the location of the components headers (``self.cpp.source`` as they are source code) and the location
of the locally built libraries. As the location of the libraries depends on the platform, the final
``self.cpp.build.components["component"].libdirs`` depends on the platform.

With this recipe we can put the package in editable mode and locally build it with:

.. code-block:: bash

    $ conan editable add greetings
    $ conan build greetings
    # we might want to also build the debug config


In the ``app`` folder we have a package recipe to build 2 executables, that link with the ``greeting`` package
components. The ``app/conanfile.py`` recipe there is simple, the ``build()`` method builds and runs both ``example``
and ``example2`` executables that are built with ``CMakeLists.txt``:


.. code-block:: cmake

    # Note the MYG file name, not matching the package name, 
    # because the recipe defined "cmake_file_name"
    find_package(MYG)

    add_executable(example example.cpp)
    # Note the MyGreetings::MyGreetings target name, not matching the package name, 
    # because the recipe defined "cmake_target_name"
    # "example" is linking with the whole package, both "hello" and "bye" components
    target_link_libraries(example MyGreetings::MyGreetings)

    add_executable(example2 example2.cpp)
    # "example2" is only using and linking "hello" component, but not "bye"
    target_link_libraries(example2 MyGreetings::MyHello)


.. code-block:: bash

    $ conan build app
    hello: Release!
    bye: Release!


If you now go to the ``bye.cpp`` source file and modify the output message, then build ``greetings`` and
``app`` locally, the final output message for the "bye" component library should change:

.. code-block:: bash

    $ conan build greetings
    $ conan build app
    hello: Release!
    adios: Release!
