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

Reusing cmake install for package developers
--------------------------------------------

Using the local development workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using the :ref:`local development workflow<package_dev_flow>`, the :command:`conan package` 
command can obviously be skipped, since it has nothing to do. But when using the 
:command:`conan export-pkg` command, you will need to specify the package-folder parameter:

.. code-block:: bash

    $ conan export-pkg . user/testing --package-folder=tmp/package

Using the ``conan create`` workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to support the :command:`conan create` command (and the excellent 
`Conan Package Tools <https://github.com/conan-io/conan-package-tools>`_), the ``package()`` 
method must actually be the one to call ``cmake.install()``.

The ``cmake.configure()`` method must also be called again in order to define the 
``CMAKE_INSTALL_PREFIX`` correctly. The extra cmake.configure() is very fast, since it is not 
doing a clean cmake configuration, so performance is not an issue.

.. code-block:: python

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

In case you need significant customization of the cmake configuration, you may define your own 
helper method to keep that in once place:

.. code-block:: python

    def custom_cmake_config(self):
        cmake = CMake(self, set_cmake_flags=True)
        if os.environ.get('VERBOSE') == '1':
            cmake.verbose = True
        cmake.definitions["FOO"] = "BAR
        cmake.configure(defs=self.options, build_folder="./build", ...)
        return cmake
    def build(self):
        self.custom_cmake_config().build()
    def package(self):
        self.custom_cmake_config().install()
        
