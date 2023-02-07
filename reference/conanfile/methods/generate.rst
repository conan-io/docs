.. _reference_conanfile_methods_generate:

generate()
==========

This method will run after the computation and installation of the dependency graph. This means that it will
run after a :command:`conan install` command, or when a package is being built in the cache, it will be run before
calling the ``build()`` method.

The purpose of ``generate()`` is to prepare the build, generating the necessary files. These files would typically be:

- Files containing information to locate the dependencies, as ``xxxx-config.cmake`` CMake config scripts, or ``xxxx.props``
  Visual Studio property files.
- Environment activation scripts, like ``conanbuild.bat`` or ``conanbuild.sh``, that define all the necessary environment
  variables necessary for the build.
- Toolchain files, like ``conan_toolchain.cmake``, that contains a mapping between the current Conan settings and options, and the
  build system specific syntax. ``CMakePresets.json`` for CMake users using modern versions.
- General purpose build information, as a ``conanbuild.conf`` file that could contain information for some toolchains like autotools to be used in the ``build()`` method.
- Specific build system files, like ``conanvcvars.bat``, that contains the necessary Visual Studio *vcvars.bat* call for certain
  build systems like Ninja when compiling with the Microsoft compiler.


The idea is that the ``generate()`` method implements all the necessary logic, making both the user manual builds after a :command:`conan install`
very straightforward, and also the ``build()`` method logic simpler. The build produced by a user in their local flow should result in
exactly the same one as the build done in the cache with a ``conan create`` without effort.

Generation of files happens in the ``generators_folder`` as defined by the current layout.

In many cases, the ``generate()`` method might not be necessary, and declaring the ``generators`` attribute could be enough:

.. code:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        generators = "CMakeDeps", "CMakeToolchain"


But the ``generate()`` method can explicitly instantiate those generators, use them conditionally (like using one build system in Windows,
and another build system integration in other platforms), customize them, or provide a complete custom
generation. 

.. code:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain

    class Pkg(ConanFile):

        def generate(self):
            tc = CMakeToolchain(self)
            # customize toolchain "tc"
            tc.generate()
            # Or provide your own custom logic


The current working directory for the ``generate()`` method will be the ``self.generators_folder`` defined in the current layout.

For custom integrations, putting code in a common ``python_require`` would be a good way to avoid repetition in
multiple recipes:

.. code:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain

    class Pkg(ConanFile):

        python_requires = "mygenerator/1.0"

        def generate(self):
            mygen = self.python_requires["mygenerator"].module.MyGenerator(self)
            # customize mygen behavior, like mygen.something= True
            mygen.generate()


In case it is necessary to collect or copy some files from the dependencies, it is also possible to do it in the ``generate()`` method, accessing ``self.dependencies``.
Listing the different include directories, lib directories from a dependency "mydep" would be possible like this:

.. code:: python

    from conan import ConanFile

    class Pkg(ConanFile):

        def generate(self):
            info = self.dependencies["mydep"].cpp_info
            self.output.info("**includedirs:{}**".format(info.includedirs))
            self.output.info("**libdirs:{}**".format(info.libdirs))
            self.output.info("**libs:{}**".format(info.libs))

And copying the shared libraries in Windows and OSX to the current build folder, could be done like:

.. code:: python

    from conan import ConanFile

    class Pkg(ConanFile):

        def generate(self):
            for dep in self.dependencies.values():
                copy(self, "*.dylib", dep.cpp_info.libdir, self.build_folder)
                copy(self, "*.dll", dep.cpp_info.libdir, self.build_folder)


.. note::

    **Best practices**

    - Accessing dependencies ``self.dependencies["mydep"].package_folder`` is possible, but it will be ``None`` when the dependency "mydep" is in "editable" mode. If you plan to use editable packages, make sure to always reference the ``cpp_info.xxxdirs`` instead.


.. seealso::

    - Follow the :ref:`tutorial about preparing build from source in recipes<creating_packages_preparing_the_build>`.
