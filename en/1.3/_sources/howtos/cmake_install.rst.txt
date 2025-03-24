.. _reuse_cmake_install:

How to reuse cmake install for package() method
===============================================

It is possible that your project's *CMakeLists.txt* has already defined some
functionality that extracts the artifacts (headers, libraries, binaries) from
the build and source folder to a predetermined place.

The conan ``package()`` method does exactly that: it defines which files
have to be copied from the build folder to the package folder.

If you want to reuse that functionality, you can do it with cmake.

Invoke cmake with ``CMAKE_INSTALL_PREFIX`` using the ``package_folder`` variable.
If the ``cmake install`` target correctly copies all the required libraries, headers, etc. to the ``package_folder``,
then the ``package()`` method is not required.

.. code-block:: python

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
        # equivalent to
        # args += ['-DCMAKE_INSTALL_PREFIX="%s"' % self.package_folder]
        # self.run('cmake "%s/src" %s %s'
        #          % (self.source_folder, cmake.command_line, ' '.join( args ) ) )
        # self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        # nothing to do here now

The ``package_info()`` method is still necessary, as there is no possible way to
automatically extract the information of the necessary libraries, defines and flags for different
build configurations from the cmake install.
