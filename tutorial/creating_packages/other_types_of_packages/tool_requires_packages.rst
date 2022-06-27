Tool requires packages
======================

In the ":ref:`Using build tools as Conan packages <consuming_packages_tool_requires>`" section we learned how to use
a tool require to build (or help building) our project or Conan package.
In this section we are going to learn how to create a recipe for a tool require.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/other_packages/tool_requires/tool


A simple tool require recipe
----------------------------

This is a recipe for a (fake) application that receiving a path returns 0 if the path is secure.
We can check how the following simple recipe covers most of the ``tool-require`` use-cases:

.. code-block:: python
    :caption: conanfile.py

    import os
    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
    from conan.tools.files import copy


    class secure_scannerRecipe(ConanFile):
        name = "secure_scanner"
        version = "1.0"
        package_type = "application"
        settings = "os", "compiler", "build_type", "arch"
        exports_sources = "CMakeLists.txt", "src/*"

        def layout(self):
            cmake_layout(self)

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            copy(self, "secure_scanner*", self.build_folder, os.path.join(self.package_folder, "bin"), keep_path=False)

        def package_info(self):
            self.buildenv_info.define("MY_VAR", "23")


There are few relevant things in this recipe:

1. It declares ``package_type = "application"``, this is optional but convenient, it will indicate conan that the current
   package doesn't contain headers or libraries to be linked. The consumers will know that this package is an application.

2. The ``package()`` method is packaging the executable into the ``bin/`` folder, that is declared by default as a bindir:
   ``self.cpp_info.bindirs = ["bin"]``.

3. In the ``package_info()`` method, we are using ``self.buildenv_info`` to define a environment variable ``MY_VAR``
   that will also be available in the consumer.


Let's create a binary package for the tool_require:

.. code-block:: bash

    $ conan create .
    ...
    secure_scanner/1.0: Calling package()
    secure_scanner/1.0: Copied 1 file: secure_scanner
    secure_scanner/1.0 package(): Packaged 1 file: secure_scanner
    ...
    Security Scanner: The path 'mypath' is secure!


We can create a consumer recipe to test if we can run the ``secure_scanner`` application of the ``tool_require`` and
read the environment variable. Go to the `examples2/tutorial/creating_packages/other_packages/tool_requires/consumer`
folder:


.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile

    class MyConsumer(ConanFile):
        name = "my_consumer"
        version = "1.0"
        settings = "os", "arch", "compiler", "build_type"
        tool_requires = "secure_scanner/1.0"

        def build(self):
            extension = ".exe" if self.settings_build.os == "Windows" else ""
            self.run("secure_scanner{} {}".format(extension, self.build_folder))
            if self.settings_build.os != "Windows":
                self.run("echo MY_VAR=$MY_VAR")
            else:
                self.run("set MY_VAR")


In this simple recipe we are declaring a ``tool_require`` to ``secure_scanner/1.0`` and we are calling directly the packaged
application ``secure_scanner`` in the ``build()`` method, also printing the value of the ``MY_VAR`` env variable.

If we build the consumer:


.. code-block:: bash


    $ conan build .

    -------- Installing (downloading, building) binaries... --------
    secure_scanner/1.0: Already installed!

    -------- Finalizing install (deploy, generators) --------
    ...
    conanfile.py (my_consumer/1.0): RUN: secure_scanner /Users/luism/workspace/examples2/tutorial/creating_packages/other_packages/tool_requires/consumer
    ...
    Security Scanner: The path '/Users/luism/workspace/examples2/tutorial/creating_packages/other_packages/tool_requires/consumer' is secure!
    ...
    MY_VAR=23


We can see that the executable returned 0 (because our folder is secure) and it printed ``Security Scanner: The path is secure!`` message.
It also printed the "23" value assigned to ``MY_VAR`` but, why are these automatically available?

- The generators ``VirtualBuildEnv`` and ``VirtualRunEnv`` are automatically used.
- The ``VirtualRunEnv`` is reading the ``tool-requires`` and is creating a launcher like ``conanbuildenv-release-x86_64.sh`` appending
  all ``cpp_info.bindirs`` to the ``PATH``, all the ``cpp_info.libdirs`` to the ``LD_LIBRARY_PATH`` environment variable and
  declaring each variable of ``self.buildenv_info``.
- Every time conan executes the ``self.run``, by default, activates the ``conanbuild.sh`` file before calling any command.
  The ``conanbuild.sh`` is including the ``conanbuildenv-release-x86_64.sh``, so the application is in the PATH
  and the enviornment variable "MYVAR" has the value declared in the tool-require.


More complex recipes
--------------------

- Toolchains (compilers) ?
- Usage of `self.rundenv_info` ?
- settings_target ?
