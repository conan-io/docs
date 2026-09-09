.. _package_repo:

Recipe and sources in the same repo
===================================

In the previous package we implemented a ``source()`` method that fetched the source code from
github. An alternative approach would be embedding the source code into the package recipe, so it is
self-contained and it doesn't require to fetch code from external origins when it is necessary to
build from sources.

This could be an appropriate approach if we want the package recipe to live in the same repository
as the source code it is packaging. It could be considered as a "snapshot" of the source code too.

First, let's get the initial source code and create the basic package recipe:

.. code-block:: bash

    $ conan new Hello/0.1 -t -s

A *src* folder will be created with the same "hello" source code than in the previous example. You
can have a look at it, is straightforward code.

Now lets have a look to the *conanfile.py*:

.. code-block:: python

    from conans import ConanFile, CMake

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        license = "<Put the package license here>"
        url = "<Package recipe repository url here, for issues about the package>"
        description = "<Description of Hello here>"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"
        generators = "cmake"
        exports_sources = "src/*"

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_folder="src")
            cmake.build()

            # Explicit way:
            # self.run('cmake "%s/src" %s' % (self.source_folder, cmake.command_line))
            # self.run("cmake --build . %s" % cmake.build_config)

        def package(self):
            self.copy("*.h", dst="include", src="src")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["hello"]

There are two important changes:

- Added the ``exports_sources`` field, to tell conan to copy all the files from the local *src*
  folder into the package recipe.
- Removed the ``source()`` method, it is not necessary anymore to retrieve external sources.

Also, you can notice the two CMake lines:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

They are not added in the package recipe, as they can be directly put in the ``src/CMakeLists.txt``
file.

And simply create the package for user and channel **demo/testing** as previously:

.. code-block:: bash

    $ conan create . demo/testing
    ...
    Hello/0.1@demo/testing test package: Running test()
    Hello world!
