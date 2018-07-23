.. _reuse_cmake_install:

How to reuse cmake install for package() method
===============================================

It is possible that your project's *CMakeLists.txt* has already defined some
functionality that extracts the artifacts (headers, libraries, binaries) from
the build and source folder to a predetermined place and does the post-processing (*e.g.*, strips rpaths). For example,
one common practice is to use CMake `install <https://cmake.org/cmake/help/latest/command/install.html>`_ directive
to that end.

When using conan, you need to wrap that functionality in the conan ``package()`` method.

The following excerpt shows how to build and package with CMake within conan:

.. code-block:: python

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

If you want to specify a different ``CMAKE_INSTALL_PREFIX`` for your package, you need to specify it as
``package_folder`` argument both in a call to conan ``build()`` and ``package()``, respectively.
(Maybe a bit unexpectedly, you can not specify ``package_folder`` only in the call to ``package()`` since CMake needs
to know the install prefix already at the building stage.)

The following excerpt from a custom script (meant to install conan, build and package the code) shows you how to set
``package_folder`` properly:

.. code-block:: python

    import conans

    def conan_build_and_install_my_codebase():
        conan, _, _ = conans.client.conan_api.ConanAPIV1.factory()

        source_folder = "/some/path/to/the/sources"
        build_folder = "/some/path/to/the/build/folder"
        package_folder = "/some/path/to/the/install/prefix"

        conan.install(cwd=build_folder, path=source_folder, build=["missing"])

        # We already need to specify the package_folder in the build() since CMake already needs
        # the install prefix at this stage.
        conan.build(cwd=build_folder, conanfile_path=source_folder, package_folder=package_folder)

        conan.package(build_folder=build_folder, path=source_folder, package_folder=package_folder)
