.. _package_repo:

Recipe and sources in the same repo
===================================

Sometimes it is more convenient to have the recipe and source code together in the same repository.
This is true especially if you are developing and packaging your own library, and not one from a third-party.

There are two different approaches:

1. Using the :ref:`exports sources attribute <exports_sources_attribute>` of the conanfile to
   export the source code together with the recipe. This way the recipe is self-contained and will
   not need to fetch the code from external origins when building from sources. It can be considered
   a "snapshot" of the source code.
2. Using the :ref:`scm attribute <scm_attribute>` of the conanfile to capture the remote and
   commit of your repository automatically.


Exporting the sources with the recipe: ``exports_sources``
----------------------------------------------------------

This could be an appropriate approach if we want the package recipe to live in the same repository
as the source code it is packaging.

First, let's get the initial source code and create the basic package recipe:

.. code-block:: bash

    $ conan new Hello/0.1 -t -s

A *src* folder will be created with the same "hello" source code as in the previous example. You
can have a look at it, the code is straightforward.

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
- Removed the ``source()`` method, since it is no longer necessary to retrieve external sources.

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



Capturing the remote and commit from git: ``scm`` [EXPERIMENTAL]
----------------------------------------------------------------

You can use the :ref:`scm attribute <scm_attribute>` with the ``url`` and ``revision`` field set to ``auto``.
When you export the recipe (or when ``conan create`` is called) the exported recipe will capture the
remote and commit of the local repository:

.. code-block:: python
   :emphasize-lines: 7, 8

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
         scm = {
            "type": "git",
            "subfolder": "hello",
            "url": "auto",
            "revision": "auto"
         }
        ...


The ``conanfile.py`` can be commited and pushed to your origin repository, and will keep always the "auto"
values. But when the file is exported to the conan local cache, the copied recipe in the local cache,
will point to the captured remote and commit:

.. code-block:: python
   :emphasize-lines: 7, 8

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
         scm = {
            "type": "git",
            "subfolder": "hello",
            "url": "https://github.com/memsharded/hello.git",
            "revision": "437676e15da7090a1368255097f51b1a470905a0"
         }
        ...


So when you :ref:`upload the recipe <uploading_packages>` to a conan remote, the recipe will contain
the "absolute" url and commit.

When you are requiring your ``HelloConan`` the ``conan install`` will retrieve the recipe from the
remote and if you build the package, the source code will be fetched from the captured url/commit.


.. tip::

    While you are in the same computer (same conan cache), even when you have exported the recipe and
    conan has captured the absolute url and commit, conan will store the local folder where your source code lives.
    If you build your package locally it will use the local repository (in the local folder) instead of the remote URL,
    even if the local directory contains uncommited changes.
    It allows to speed up the development of your packages cloning from a local repository.
