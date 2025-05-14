.. _reuse_cmake_install:

How to reuse cmake install for package() method
===============================================

It is possible that your project's *CMakeLists.txt* has already defined some functionality that extracts the artifacts (headers, libraries,
binaries) from the build and source folder to a predetermined place and does the post-processing (*e.g.*, strips rpaths). For example, one
common practice is to use CMake `install <https://cmake.org/cmake/help/latest/command/install.html>`_ directive to that end.

When using Conan, the install phase of CMake is wrapped in the ``package()`` method. That way the flags like
:command:`conan create --keep-build` or the commands for the :ref:`package_dev_flow` are consistent with every step of the packaging
process.

The following excerpt shows how to build and package with CMake within Conan. Mind that you need to configure CMake both in ``build()`` and
in ``package()``, since these methods are called independently.

.. code-block:: python

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["SOME_DEFINITION"] = True
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["libname"]


The ``package_info()`` method specifies the list of the necessary libraries, defines and flags for different build configurations for the
consumers of the package. This is necessary as there is no possible way to extract this information from the CMake install automatically.
