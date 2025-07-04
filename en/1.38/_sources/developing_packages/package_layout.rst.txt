.. _package_layout:

Package layout
==============

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

Available since: `1.37.0 <https://github.com/conan-io/conan/releases>`_

You can declare a ``layout()`` method in the recipe to describe the package contents,
not only the final package in the cache but also the package while developing.
As the package will have the same structure in the cache and in our local directory, the recipe development becomes easier.

In the ``layout()`` method you can adjust 3 different things:

    - ``self.folders``: Specify the location of several things, like the sources, the build folder or even the folder where
      the generators files (e.g the `xx-config.cmake` files from the ``CMakeDeps``) will be created.

    - ``self.patterns``: Describe the file patterns of your **source** and **build** folders. It will ease the process of
      packaging the files in the ``package()`` method.

    - ``self.cpp``: The same you could adjust the ``self.cpp_info`` in the :ref:`package_info()<method_package_info>` for the
      package in the cache, you can do the same for the `source` and `build` folders while developing the package. This feature
      enables an easier way to use :ref:`editable packages<editable_packages>`.


self.folders
++++++++++++

- **self.folders.source**: To specify a folder where your sources are.
- **self.folders.build**: To specify a subfolder where the files from the build are (or will be).
- **self.folders.generators**: To specify a subfolder where to write the files from the generators and the toolchains.
- **self.folders.imports**: To specify a subfolder where to write the files copied when using the ``imports(self)``
  method in a ``conanfile.py``.
- **self.folders.package**: To specify a subfolder where to write the package files when running the :command:`conan package`
  command.

Check the :ref:`complete reference<layout_folders_reference>` of the folders attribute.

In the following example we are declaring a layout that follows the standard CLion one, where the build directory is ``cmake-build-release``
or ``cmake-build-debug`` depending on the declared ``build_type`` setting. The sources of the project are in the ``src`` folder.
Also the generators folders inside the build folder is quite convenient to include the :ref:`conan_toolchain.cmake<conan-cmake-toolchain>`
file when using the :ref:`CMakeDeps<conan_tools_cmake>` generator because it will be always in the same relative path to the build folder.


.. code-block:: text

    <my_project_folder>
      | - conanfile.py
      | - src
          | - CMakeLists.txt
          | - hello.cpp
          | - hello.h


.. code:: python

    import os
    from conans import ConanFile, CMake

    class Pkg(ConanFile):

        settings = "os", "build_type", "arch"
        requires = "zlib/1.2.11"
        generators = "CMakeDeps", "CMakeToolchain"
        exports_sources = "src*"

        def layout(self):
            self.folders.build = "cmake-build-{}".format(str(self.settings.build_type).lower())
            self.folders.generators = os.path.join(self.folders.build, "generators")
            self.folders.imports = self.folders.build
            self.folders.source = "src"

        def source(self):
            # In the source method, the current directory == self.source_folder
            assert self.source_folder == os.getcwd()

        def build(self):
            # We are at a folder like "myproject/cmake-build-debug"
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

Given the previous example we can run the conan local methods without taking much care of the directories where the
files are or the build files should be:

.. code:: bash

    # This will write the toolchains and generator files from the dependencies to the ``cmake-build-debug/generators``
    $ conan install . -if=my_install -s build_type=Debug

    # In case we needed it, this will fetch the sources to the ./src folder.
    $ conan source . -if=my_install

    # This will build the project using the declared source folder and ``cmake-build-debug`` as the build folder
    $ conan build . -if=my_install

    # This will import, if declared imports(self) method, the files to the ``cmake-build-debug`` folder
    $ conan imports . -if=my_install

Of course we could open the **Clion IDE** and build from there and the artifacts will be created at the same  ``cmake-build-debug``
folder.


.. note::

    Maybe you are wondering why the **install folder** is not parametrized and has to be specified with the ``-if``
    argument.
    Currently, Conan generates several files like the ``graph_info.json`` and the ``conanbuildinfo.txt`` that
    are read to restore the configuration saved (settings, options, etc) to be applied in the local commands.
    That configuration is needed before running the ``layout()`` method because the folders might depend on the settings
    like in the previous example. It is a kind of a chicken-egg issue. In Conan 2.0, likely, the
    configuration won't be stored, and the local methods like :command:`conan build .` will compute the graph
    from arguments (--profile, -s, -o...) and won't need the ``--if`` argument anymore, being always trivial to run.




.. _package_layout_cpp:

self.cpp
++++++++

The ``layout()`` method allows to declare ``cpp_info`` objects not only for the final package (like the classic approach with
the ``self.cpp_info`` in the ``package_info(self)`` method) but for the ``self.source_folder`` and ``self.build_folder``.
This is useful when a package is in :ref:`editable mode<editable_packages>` to automatically propagate to the consumers
all the needed information (library names, include directories...) but pointing to the local project directories while developing,
whether you are calling directly your build-system, using an IDE or executing the :command:`conan build` command to build
your code.


Example:

.. code:: python

        from conans import ConanFile

        class Pkg(ConanFile):

            def layout(self):

                self.cpp.source.includedirs = ["include"]

                self.cpp.build.libdirs = ["."]
                self.cpp.build.libs = ["mylib"]
                self.cpp.build.includedirs = ["gen_include"]

                self.cpp.package.libs = ["mylib"]


The fields of the cpp_info objects at ``self.info.build`` and ``self.info.source`` are the same described :ref:`here<cpp_info_attributes_reference>`.
Components are also supported.

.. note::

        You can still use the ``package_info(self)`` method. The received `self.cpp_info` object will be populated with the information explicitly declared
        in the ``self.cpp.package`` object, so you can complete it or modify it later.


Once you have your ``self.cpp.source`` and ``self.cpp.build`` objects declared you can put the package in
:ref:`editable mode<editable_packages>` and keep working on the code development with your IDE. Other packages
depending on this one, will locate the libraries being developed instead of the Conan package in the cache.

.. code:: bash

    $ conan editable add .  hello/1.0



self.patterns
+++++++++++++

You can fill the ``self.patterns.source`` and ``self.patterns.build`` objects describing the patterns of the files that are at the ``self.folders.source`` and ``self.folders.build``
to automate the ``package(self)`` method with the **LayoutPackager()** tool (see the :ref:`example below<layout_example>`).

The defaults are the following but you can customize anything based on the configuration (``self.settings``, ``self.options``...):

.. code:: python

        self.patterns.source.include = ["*.h", "*.hpp", "*.hxx"]
        self.patterns.source.lib = []
        self.patterns.source.bin = []

        self.patterns.build.include = ["*.h", "*.hpp", "*.hxx"]
        self.patterns.build.lib = ["*.so", "*.so.*", "*.a", "*.lib", "*.dylib"]
        self.patterns.build.bin = ["*.exe", "*.dll"]


These are all the fields that can be adjusted, both in ``self.patterns.source`` and ``self.patterns.build``:

+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| NAME                                 | DESCRIPTION (xxx can be either ``build`` or ``source``)                                                 |
+======================================+=========================================================================================================+
| include                              | Patterns of the files from the folders: ``self.cpp.xxx.includedirs``                                    |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| lib                                  | Patterns of the files from the folders: ``self.cpp.xxx.libdirs``                                        |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| bin                                  | Patterns of the files from the folders: ``self.cpp.xxx.bindirs``                                        |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| src                                  | Patterns of the files from the folders: ``self.cpp.xxx.srcdirs``                                        |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| build                                | Patterns of the files from the folders: ``self.cpp.xxx.builddirs``                                      |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| res                                  | Patterns of the files from the folders: ``self.cpp.xxx.resdirs``                                        |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+
| framework                            | Patterns of the files from the folders: ``self.cpp.xxx.frameworkdirs``                                  |
+--------------------------------------+---------------------------------------------------------------------------------------------------------+


.. _layout_example:

Example: Everything together
++++++++++++++++++++++++++++

Let's see how we can use the ``layout()`` method to both write simpler recipes, improve the local methods and the integration
with the IDE and develop the package as an :ref:`editable package<editable_packages>`.

This is the project structure:

.. code-block:: text

    <project_folder>
      | - CMakeLists.txt
      | - hello.cpp
      | - include
          | - hello.h
      | - res
          | - myasset.jpg

We want to use CLion to build the project so we open the project (using both **Release** and **Debug** configurations).
After building the project we have this layout:

.. code-block:: text

    <project_folder>
      | - cmake-build-debug
          | - CMakeFiles
          | - ... other CMake stuff...
          | - libhello.a
          | - gen.h
      | - cmake-build-release
          | - CMakeFiles
          | - ... other CMake stuff...
          | - libhello.a
          | - gen.h
      | - CMakeLists.txt
      | - hello.cpp
      | - include
          | - hello.h
      | - res
          | - myasset.jpeg


We can write a ``layout()`` method describing it:

.. code:: python

        from conans import ConanFile
        from conan.tools.layout import LayoutPackager

        class Pkg(ConanFile):

            def layout(self):
                # ###### FOLDERS
                # The sources can be found in the root dir
                self.folders.source = "."

                # The build folder is created with the CLion way
                self.folders.build = "cmake-build-{}".format(str(self.settings.build_type).lower())

                # We want to have the toolchains in the build folder so we can always pass
                # `-DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake` to CMake
                self.folders.generators = os.path.join(self.folders.build, "generators")

                # In case we use "conan package" we declare an output directory
                self.folders.package = "package-{}".format(str(self.settings.build_type).lower())

                # ###### INFOS
                self.cpp.source.includedirs = ["include"] # Relative to ["."] (self.folders.source)
                self.cpp.build.libdirs = ["."]  # Relative to (self.folders.build)
                self.cpp.build.libs = ["hello"]
                self.cpp.build.includedirs = ["."] # Relative to (self.folders.build)
                self.cpp.package.libs = ["hello"]

                # ###### PATTERNS
                self.patterns.source.res = ["*.jpeg"] # To package automatically the myasset.jpeg

            def package(self):
                LayoutPackager(self).package()


- There is no need to declare the ``package_info(self)`` method, we declared the needed information at ``self.cpp.package``.
- The ``package(self)`` method is quite simple using the ``LayoutPackager(self).package()``
- We can easily put the package in editable mode and keep using the CLion IDE to build the libraries:

    .. code:: bash

        $ conan editable add . hello/1.0

    The packages requiring "hello/1.0" will find the headers and libraries in the right CLion output directories automatically.

- If we want to verify the that the Conan recipe is totally correct we can use the Conan local methods always with the same syntax:

    .. code:: bash

        $ conan install . -if=my_install
        $ conan imports . -if=my_install
        $ conan build . -if=my_install
        $ conan package . -if=my_install

    The conan commands will follow the same directory layout while building, and the ``conan package`` command will
    create an additional ``package-release`` folder with the packaged artifacts.
