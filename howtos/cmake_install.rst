.. _reuse_cmake_install:

How to reuse cmake install for package() method
===============================================

It is possible that your project's *CMakeLists.txt* has already defined some
functionality that extracts the artifacts (headers, libraries, binaries) from
the build and source folder to a predetermined place and does the post-processing (*e.g.*, strips rpaths). For example,
one common practice is to use CMake `install <https://cmake.org/cmake/help/latest/command/install.html>`_ directive
to that end.

When using conan, the install phase of CMake is wrapped in the conan ``package()`` method.

The ``package_info()`` method specifies the list of the necessary libraries, defines and flags for different
build configurations for the consumers of the package. This is necessary as there is no possible way to extract this
information from the CMake install automatically.

``no_copy_source``
------------------
When ``no_copy_source = False``, the building and packaging follows what we expect from the usual CMake pipeline.
However, when ``no_copy_source = True``, conan workflow might be surprising to users familiar with CMake, but still
unfamiliar with intricacies of conan.

Let us recap briefly the building and packaging process of conan and see then how a special case, when
``no_copy_source = True`` is set, affects the usage of conan with CMake.

Conan retrieves the sources and put them in a source folder. Before compiling, conan creates a copy of the source folder
into the build folder and starts the build. Once the build is done, conan creates the package by collecting the
artifacts from the build folder using ``package()`` method. When ``no_copy_source = False``, there is nothing unexpected
in the workflow.

If you set ``no_copy_source = True``, conan still retrieves the sources, but does not copy them to the
build folder. The build starts and once the artefacts are built, ``package()`` method needs to be called *twice*.
First, source files are copied from the source folder into the package folder (which involves calling ``package()``
once) and second, artifacts are copied from the build folder into the package folder (which again calls ``package()``
for the second time).

Please mind that CMake usually uses ``install`` directive to package both the artifacts and source code (*i.e.* header
files) into the package folder. Hence calling ``package()`` twice, while having no side effects, is wasting a couple of
cycles, since source code is already copied in the first invokation of ``package()`` and the install step will be done
twice. Files will be simply overwritten, but install steps are sometimes time-expensive and this doubles the "packaging"
time.

This might be unintuitive if you only use CMake, but mind that conan needs to cater to many different build systems and
scenarios (*e.g.* where you don't control the CMake configuration directly) and hence this workflow, though potentially
unintuitive, is indispensable.

Example
-------
The following excerpt shows how to build and package with CMake within conan. Mind that you need to configure CMake
both in ``build()`` and in ``package()`` since these methods are called independently.

.. code-block:: python

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.definitions["SOME_DEFINITION"] = "On"

        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.bindirs = ['bin']
