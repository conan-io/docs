.. _meson_build_helper_reference:


Meson
=====


.. code-block:: python

   from conans import ConanFile, Meson

   class ExampleConan(ConanFile):
       ...


       def build(self):
           meson = Meson(self)
           meson.configure(cache_build_folder="build")
           meson.build()



Methods
-------

- **constructor** (conanfile, backend=None, build_type=None)

    - **conanfile**: Use ``self``.
    - **backend**: Specify a backend to be used, otherwise it will use "Ninja".
    - **build_type**: Force to use a build type, ignoring the read from the settings.

- **configure** (args=None, defs=None, source_folder=None, build_folder=None, pkg_config_paths=None)

    - **args**: A list of additional arguments to be passed to the ``configure`` script. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **defs**: A list of definitions
    - **source_folder**: Meson's source directory where ``meson.build`` is located. The default value is the ``self.source_folder``.
      Relative paths are allowed and will be relative to ``self.source_folder``.
    - **build_folder**: Meson's output directory. The default value is the ``self.build_folder`` if ``None`` is specified.
      The ``Meson`` object will store ``build_folder`` internally for subsequent calls to ``build()``.
    - **cache_build_folder**: Use the given subfolder as build folder when building the package in the local cache.
      This argument doesn't have effect when the package is being built in user folder with ``conan build`` but overrides **build_folder** when working in the local cache.
      See :ref:`self.in_local_cache<in_local_cache>`.
    - **pkg_config_paths**: A list containing paths to locate the pkg-config files (\*.pc). Default conanfile.build_folder.

- **build** (args=None, build_dir=None, targets=None)

    - **args**: A list of additional arguments to be passed to the ``make`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build_dir**: Default conanfile.build_folder
    - **targets**: A list of targets to be built.


Example
--------

A typical usage of the Meson build helper, if you want to be able to both execute ``conan create`` and also build your package for a library locally (in your user folder, not in the conan cache), could be:

.. code-block:: python

    from conans import ConanFile, Meson

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        generators = "pkg_config"
        exports_sources = "src/*"

        def build(self):
            meson = Meson(self)
            meson.configure(source_folder="%s/src" % self.source_folder, 
                            build_folder="build")
            meson.build()

        def package(self):
            self.copy("*.h", dst="include", src="src")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["hello"]


Note the **pkg_config** generator, which generates .pc files, which are understood by Meson to process dependencies informations (no need for a "meson" generator).

The layout is:

.. code-block:: text

    <folder>
      | - conanfile.py
      | - src
           | - meson.build
           | - hello.cpp
           | - hello.h

And the ``meson.build`` could be as simple as:

.. code-block:: text

    project('hello', 'cpp', version : '0.1.0',
		     default_options : ['cpp_std=c++11'])

    library('hello', ['hello.cpp'])

This allows, to create the package with ``conan create`` as well as to build the package locally:

.. code-block:: bash

    $ cd <folder>
    $ conan create user/testing
    # Now local build
    $ mkdir build && cd build
    $ conan install ..
    $ conan build ..
