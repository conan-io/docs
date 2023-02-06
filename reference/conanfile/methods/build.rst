.. _reference_conanfile_methods_build:

build()
=======

The ``build()`` method is used to define the build from source of the package. In practice this means calling some build system, which could be done explictly or using any of the build helpers provided by Conan:


.. code-block:: python

    from conan.tools.cmake import CMake

    clas Pkg(ConanFile):

        def build(self):
            # Either using some of the Conan built-in helpers
            cmake = CMake(self)
            cmake.configure()  # equivalent to self.run("cmake . <other args>")
            cmake.build() # equivalent to self.run("cmake --build . <other args>")
            cmake.test()  # equivalent to self.run("cmake --target=RUN_TESTS")

            # Or it could run your own build system or scripts
            self.run("mybuildsystem . --configure")
            self.run("mybuildsystem . --build")
        

For more information about the existing built-in build system integrations, visit :ref:`conan_tools`.

The ``build()`` method should be as simple as possible, just wrapping the command line invocations
that a developer would do in the simplest possible way. The ``generate()`` method is the responsible
for preparing the build, creating toolchain file, CMake presets, or whatever other files are necessary
so developers can easily call the build system by hand easily. This way the integration with IDEs and 
the developer experience is much better. The result is that the ``build()`` method should be relatively
simple in practice.

The ``build()`` method is the right place to build and run unit tests, before packaging, and raising errors if those tests fail, interrupting the process, and not even packaging the final binaries.
The built-in helpers will skip the unit tests if ``tools.build:skip_test`` configuration is defined, for custom integrations, it is expected that the method checks this ``conf`` value in order to skip building and running tests, which can be useful for some CI scenarios.

The ``build()`` method runs once per different configuration, so if there are some source operations like applying patches that are done conditionally to different configurations, they could be also applied in the
``build()`` method, before the actual build. It is important that in this case the ``no_copy_source`` attribute cannot be set to ``True``.



.. note::

    **Best practices**

    - The ``build()`` should be as simple as possible, the heavy lifting of preparing the build should happen in the ``generate()`` method, in order to achieve a good developer experience that can easily build locally with just ``conan install .``, plus directly calling the build system or opening their IDE.