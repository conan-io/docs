.. _pc_files:

:command:`pkg-config` and *.pc* files
=====================================

If you are creating a Conan package for a library (A) and the build system uses *.pc* files to locate
its dependencies (B and C) that are Conan packages too, you can follow different approaches.

The main issue to solve is the absolute paths. When a user installs a package in the local cache,
the directory will probably be different from the directory where the package was created. This could be
because of the different computer, the change in Conan home directory or even a different user or channel:

For example, in the machine where the packages were created:

.. code-block:: text

    /home/user/lasote/.data/storage/zlib/1.2.11/conan/stable

In the machine where the library is being reused:

.. code-block:: text

    /custom/dir/.data/storage/zlib/1.2.11/conan/testing

You can see that *.pc* files containing absolute paths won't work to locate the dependencies.

Example of a *.pc* file with an absolute path:

.. code-block:: text

    prefix=/Users/lasote/.conan/data/zlib/1.2.11/lasote/stable/package/b5d68b3533204ad67e01fa587ad28fb8ce010527
    exec_prefix=${prefix}
    libdir=${exec_prefix}/lib
    sharedlibdir=${libdir}
    includedir=${prefix}/include

    Name: zlib
    Description: zlib compression library
    Version: 1.2.11

    Requires:
    Libs: -L${libdir} -L${sharedlibdir} -lz
    Cflags: -I${includedir}

To solve this problem there are different approaches that can be followed.

Approach 1: Import and patch the prefix in the *.pc* files
----------------------------------------------------------

In this approach your **library A** will import to a local directory the *.pc* files from **B** and **C**, then,
as they will contain absolute paths, the recipe for **A** will patch the paths to match the current installation
directory.

You will need to package the *.pc* files from your dependencies. You can adjust the ``PKG_CONFIG_PATH`` to let :command:`pkg-config` tool
locate them.

.. code-block:: python

    import os
    from conans import ConanFile, tools

    class LibAConan(ConanFile):
        name = "libA"
        version = "1.0"
        settings = "os", "compiler", "build_type", "arch"
        exports_sources = "*.cpp"
        requires = "libB/1.0@conan/stable"

        def build(self):
            lib_b_path = self.deps_cpp_info["libB"].rootpath
            copyfile(os.path.join(lib_b_path, "libB.pc"), "libB.pc")
            # Patch copied file with the libB path
            tools.replace_prefix_in_pc_file("libB.pc", lib_b_path)

            with tools.environment_append({"PKG_CONFIG_PATH": os.getcwd()}):
               # CALL YOUR BUILD SYSTEM (configure, make etc)
               # E.g., self.run('g++ main.cpp $(pkg-config libB --libs --cflags) -o main')

Approach 2: Prepare and package *.pc* files before package them
---------------------------------------------------------------

With this approach you will patch the *.pc* files from B and C before packaging them.
The goal is to replace the absolute path (the variable part of the path) with a variable placeholder.
Then in the consumer package A, declare the variable using ``--define-variable`` when calling the
:command:`pkg-config` command.

This approach is cleaner than approach 1, because the packaged files are already prepared to be
reused with or without Conan by declaring the needed variable. And it's not needed to import the *.pc*
files to the consumer package. However, you need B and C libraries to package the *.pc* files correctly.

Library B recipe (preparing the *.pc* file):

.. code-block:: python

    from conans import ConanFile, tools

    class LibBConan(ConanFile):
        ....

        def build(self):
            ...
            tools.replace_prefix_in_pc_file("mypcfile.pc", "${package_root_path_lib_b}")

        def package(self):
            self.copy(pattern="*.pc", dst="", keep_path=False)

Library A recipe (importing and consuming *.pc* file):

.. code-block:: python

    class LibAConan(ConanFile):
        ....

        requires = "libB/1.0@conan/stable, libC/1.0@conan/stable"

        def build(self):

            args = '--define-variable package_root_path_lib_b=%s' % self.deps_cpp_info["libB"].rootpath
            args += ' --define-variable package_root_path_lib_c=%s' % self.deps_cpp_info["libC"].rootpath
            pkgconfig_exec = 'pkg-config ' + args

            vars = {'PKG_CONFIG': pkgconfig_exec, # Used by autotools
                    'PKG_CONFIG_PATH': "%s:%s" % (self.deps_cpp_info["libB"].rootpath,
                                                  self.deps_cpp_info["libC"].rootpath)}

            with tools.environment_append(vars):
                # Call autotools (./configure ./make, will read PKG_CONFIG)
                # Or directly declare the variables:
                self.run('g++ main.cpp $(pkg-config %s libB --libs --cflags) -o main' % args)

Approach 3: Use :command:`--define-prefix`
------------------------------------------

If you have available :command:`pkg-config` >= 0.29 and you have only one dependency, you can use directly
the :command:`--define-prefix` option to declare a custom ``prefix`` variable. With this approach you won't
need to patch anything, just declare the correct variable.

Approach 4: Use ``PKG_CONFIG_$PACKAGE_$VARIABLE``
-------------------------------------------------

If you have :command:`pkg-config` >= 0.29.1 available, you can manage multiple dependencies declaring **N** variables
with the prefixes:

.. code-block:: python

    class LibAConan(ConanFile):
        ....

        requires = "libB/1.0@conan/stable, libC/1.0@conan/stable"

        def build(self):

            vars = {'PKG_CONFIG_libB_PREFIX': self.deps_cpp_info["libB"].rootpath,
                    'PKG_CONFIG_libC_PREFIX': self.deps_cpp_info["libC"].rootpath,
                    'PKG_CONFIG_PATH': "%s:%s" % (self.deps_cpp_info["libB"].rootpath,
                                                  self.deps_cpp_info["libC"].rootpath)}

            with tools.environment_append(vars):
                # Call the build system

.. _pkg_config_generator_example:

Approach 5: Use the ``pkg_config`` generator
--------------------------------------------

If you use ``package_info()`` in library B and library C, and specify all the library names and any other needed flag,
you can use the ``pkg_config`` generator for **library bA**. Those files doesn't need to be patched, because
are dynamically generated with the correct path.

So it can be a good solution in case you are building **library A** with a build system that manages *.pc* files like
:ref:`Meson Build<meson_build_tool>` or :ref:`AutoTools<autotools_build_tool>`:

**Meson Build**

.. code-block:: python
   :emphasize-lines: 5, 10, 11, 12

    from conans import ConanFile, tools, Meson
    import os

    class ConanFileToolsTest(ConanFile):
        generators = "pkg_config"
        requires = "LIB_A/0.1@conan/stable"
        settings = "os", "compiler", "build_type"

        def build(self):
            meson = Meson(self)
            meson.configure()
            meson.build()

**Autotools**

.. code-block:: python
   :emphasize-lines: 5, 10, 11, 12, 13

    from conans import ConanFile, tools, AutoToolsBuildEnvironment
    import os

    class ConanFileToolsTest(ConanFile):
        generators = "pkg_config"
        requires = "LIB_A/0.1@conan/stable"
        settings = "os", "compiler", "build_type"

        def build(self):
            autotools = AutoToolsBuildEnvironment(self)
            # When using the pkg_config generator, self.build_folder will be added to PKG_CONFIG_PATH
            # so pkg_config will be able to locate the generated pc files from the requires (LIB_A)
            autotools.configure()
            autotools.make()

.. seealso::

    Check the :ref:`pkgconfigtool`, a wrapper of the :command:`pkg-config` tool that allows to extract flags,
    library paths, etc. for any *.pc* file.
