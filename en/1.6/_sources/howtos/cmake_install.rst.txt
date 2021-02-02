.. _reuse_cmake_install:

How to reuse cmake install for package() method
===============================================

It is possible that your project's *CMakeLists.txt* has already defined some functionality that extracts the artifacts (headers, libraries,
binaries) from the build and source folder to a predetermined place and does the post-processing (*e.g.*, strips rpaths). For example, one
common practice is to use CMake `install <https://cmake.org/cmake/help/latest/command/install.html>`_ directive to that end.

When using Conan, the install phase of CMake is wrapped in the ``package()`` method.

The following excerpt shows how to build and package with CMake within Conan. Mind that you need to configure CMake both in ``build()`` and
in ``package()`` since these methods are called independently.

.. code-block:: python

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["SOME_DEFINITION"] = True
        cmake.configure()

        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["libname"]


The ``package_info()`` method specifies the list of the necessary libraries, defines and flags for different build configurations for the
consumers of the package. This is necessary as there is no possible way to extract this
information from the CMake install automatically.


.. important::

    Please mind that if you use ``cmake.install()`` in ``package()``, it will be called twice if you are using
    :ref:`no_copy_source` attribute in your conanfile.

    CMake usually uses ``install`` directive to package both the artifacts and source code (*i.e.* header files) into the package folder.
    Hence calling ``package()`` twice, while having no side effects, is wasting a couple of cycles, since source code is already copied in
    the first invocation of ``package()`` and the install step will be done twice. Files will be simply overwritten, but install steps are
    sometimes time-expensive and this doubles the "packaging" time.

    This might be unintuitive if you only use CMake, but mind that Conan needs to cater to many different build systems and scenarios
    (*e.g.* where you don't control the CMake configuration directly) and hence this workflow is indispensable.
