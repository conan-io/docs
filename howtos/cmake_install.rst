.. _reuse_cmake_install:

Reuse cmake install for package() method
============================================

It is possible that your project ``CMakeLists.txt`` already has defined some
functionality that extracts the artifacts (headers, libraries, binaries) from
the build and source folder to a predetermined place.

The conan ``package()`` method does exactly that, it defines which files
have to be copied from the build folder to the package folder.

If you want to reuse that functionality, you can do it with cmake.

First, define the ``CMAKE_INSTALL_PREFIX`` in your build to point to the
package folder, defined by the conanfile variable ``package_folder``
and use it in your cmake invocation flags.

Then, you will typically build the cmake install target, which previously also
builds the source code. We probably can do it in the ``package()`` method instead
of in the ``build()`` one, but as the largest part of the time is used
for build I prefer to have it in the ``build()`` method. Note that if you run
it in both places you might end building the code twice which will make package
creation unnecessary slower


.. code-block:: python

    def build(self):
        cmake = CMake(self.settings)
        args = ["-DBUILD_SHARED_LIBS=ON"  if self.options.shared else "-DBUILD_SHARED_LIBS=OFF"]
        args += ['-DCMAKE_INSTALL_PREFIX="%s"' % self.package_folder]

        self.run('cmake %s/SRC %s %s'
                  % (self.conanfile_directory, cmake.command_line, ' '.join( args ) ) )
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        # nothing to do here now


The ``package_info()`` method is still necessary, as there is no possible way to
automatically extract the information of the necessary libraries, defines and flags for different
build configurations from the cmake install.