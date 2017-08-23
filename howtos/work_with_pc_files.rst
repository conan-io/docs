.. _pc_files:

Work with pkg-config and pc files
=================================

If you are creating a Conan package for a library (A) and the build system uses ``.pc`` files to locate
its dependencies (B and C), Conan packages too, you can follow different approaches.

The main issue to solve is the absolute paths. When an user installs a package in the local cache,
the directory will probably be different from the directory where the package was created,
because of the different computer, conan home directory or even different user or channel:

In the machine where the packages were created:

.. code-block:: text

    /home/user/lasote/.data/storage/zlib/1.2.11/conan/stable

In the machine where some user are reusing the library:

.. code-block:: text

    /custom/dir/.data/storage/zlib/1.2.11/conan/testing

So the ``.pc``  files containing absolute paths won't work to locate the dependencies.


Example of a ``.pc`` file with an absolute path:


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


Approach 1: Import and patch the prefix in the `pc` files
---------------------------------------------------------

Following this approach your library `A` will import to a local directory the ``.pc`` files from `B` and `C`, then,
as they will contain absolute paths, the recipe for `A` will patch the paths to match the current installation
directory.

You will need to package the `pc` files from your dependencies.
You can adjust the `PKG_CONFIG_PATH` to let ``pkg-config`` tool locate your ``.pc`` files.

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
            from conans.client.file_copier import FileCopier
            lib_b_path = self.deps_cpp_info["libB"].rootpath
            file_copier = FileCopier(lib_b_path, ".")
            pcs = file_copier("*.pc")
            for pcfile in pcs:
                tools.replace_prefix_in_pc_file(pcfile, lib_b_path)

            with tools.environment_append({"PKG_CONFIG_PATH": os.getcwd()}):
               # CALL YOUR BUILD SYSTEM (configure, make etc)
               # E.j: self.run('g++ main.cpp $(pkg-config libB --libs --cflags) -o main')


Approach 2: Prepare and package `pc` files before package them
--------------------------------------------------------------

With this approach you will patch the ``pc`` files from B and C before package them.
The goal is to replace the absolute path (the variable part of the path) with a variable placeholder.
Then in the consumer package A, declare the variable using ``--define-variable`` when calling the
`pkg-config` command.

This approach is cleaner than approach 1, because the packaged files are already prepared to be
reused with or without conan, just declaring the needed variable. And it's not needed to import the ``pc``
files to the consumer package. However, you need B and C libraries to package the ``pc`` files correctly.


Library B recipe (preparing the ``pc`` file):


.. code-block:: python

    from conans import tools

    class LibraryBrecipe(ConanFile):
        ....

        def build(self):
            ...
            tools.replace_prefix_in_pc_file("mypcfile.pc", "${package_root_path_lib_b}")

        def package(self):
            self.copy(pattern="*.pc", dst="", keep_path=False)


Library A recipe (importing and consuming ``pc`` file):


.. code-block:: python

    class LibraryArecipe(ConanFile):
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



Approach 3: Use `--define-prefix`
---------------------------------

If you have available ``pkg-config`` >= 0.29 and you have only one dependency, you can use directly
the ``--define-prefix`` option to declare a custom ``prefix`` variable. With this approach you won't
need to patch anything, just declare the correct variable.

Approach 3: Use `PKG_CONFIG_$PACKAGE_$VARIABLE`
-----------------------------------------------

If you have available ``pkg-config`` >= 0.29.1 you can manage multiple dependencies declaring N variables
with the prefixes:

.. code-block:: python

    class LibraryArecipe(ConanFile):
        ....

        requires = "libB/1.0@conan/stable, libC/1.0@conan/stable"

        def build(self):

            vars = {'PKG_CONFIG_libB_PREFIX': self.deps_cpp_info["libB"].rootpath,
                    'PKG_CONFIG_libC_PREFIX': self.deps_cpp_info["libC"].rootpath,
                    'PKG_CONFIG_PATH': "%s:%s" % (self.deps_cpp_info["libB"].rootpath,
                                                  self.deps_cpp_info["libC"].rootpath)}

            with tools.environment_append(vars):
                # Call the build system
