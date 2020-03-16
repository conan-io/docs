.. _meson_build_reference:

Meson
=====

If you are using **Meson Build** as your build system, you can use the **Meson** build helper.
Specially useful with the :ref:`pkg_config_generator` that will generate the *.pc*
files of our requirements, then ``Meson()`` build helper will locate them automatically.

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
            meson.configure(build_folder="build")
            meson.build()

Constructor
-----------

.. code-block:: python

    class Meson(object):

        def __init__(self, conanfile, backend=None, build_type=None)

Parameters:
    - **conanfile** (Required): Use ``self`` inside a ``conanfile.py``.
    - **backend** (Optional, Defaulted to ``None``): Specify a backend to be used, otherwise it will use ``"Ninja"``.
    - **build_type** (Optional, Defaulted to ``None``): Force to use a build type, ignoring the value from the settings.

Methods
-------

configure()
+++++++++++

.. code-block:: python

    def configure(self, args=None, defs=None, source_folder=None, build_folder=None,
                  pkg_config_paths=None, cache_build_folder=None, append_vcvars=False)

Configures Meson project with the given parameters.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``configure`` script. Each argument will
      be escaped according to the current shell. No extra arguments will be added if ``args=None``.
    - **defs** (Optional, Defaulted to ``None``): A list of definitions.
    - **source_folder** (Optional, Defaulted to ``None``): Meson's source directory where ``meson.build`` is located. The default value is the ``self.source_folder``.
      Relative paths are allowed and will be relative to ``self.source_folder``.
    - **build_folder** (Optional, Defaulted to ``None``): Meson's output directory. The default value is the ``self.build_folder`` if ``None`` is specified.
      The ``Meson`` object will store ``build_folder`` internally for subsequent calls to ``build()``.
    - **pkg_config_paths** (Optional, Defaulted to ``None``): A list containing paths to locate the pkg-config files (*\*.pc*). If ``None``, it will be set to ``conanfile.build_folder``.
    - **cache_build_folder** (Optional, Defaulted to ``None``): Subfolder to be used as build folder when building the package in the local cache.
      This argument doesn't have effect when the package is being built in user folder with :command:`conan build` but overrides **build_folder** when working in the local cache.
      See :ref:`self.in_local_cache<in_local_cache>`.
    - **append_vcvars** (Optional, Defaulted to ``False``): When a Visual Studio environment is activated by the build helper, append it to respect existing environment. ``Meson`` helper uses the Ninja generator and needs to call ``vcvars`` to set the VS environment. By default the ``vcvars`` is pre-pended to the environment, taking precedence. With ``append_vcvars=True``, the ``vcvars`` will append to the end of the environment (for "list" environment variables, like ``PATH``), instead of pre-pending, so the existing environment takes precedence.


build()
+++++++

.. code-block:: python

    def build(self, args=None, build_dir=None, targets=None)

Builds Meson project with the given parameters.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``ninja`` command. Each argument will be escaped
      according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): Build folder. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.
      If ``build_folder`` from ``configure()`` is ``None``, it will be set to ``conanfile.build_folder``.
    - **targets** (Optional, Defaulted to ``None``): Specifies the targets to build. The default *all* target will be built if ``None`` is specified.


test()
++++++

.. code-block:: python

    def test(args=None, build_dir=None, target=None)

Executes ninja test target, which usually means building and running unit tests.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``ninja`` command. Each argument will be escaped
      according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): Build folder. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.
      If ``build_folder`` from ``configure()`` is ``None``, it will be set to ``conanfile.build_folder``.
    - **targets** (Optional, Defaulted to ``None``): Specifies the targets to be executed. The *test* target will be executed if ``None`` is specified.


install()
+++++++++

.. code-block:: python

    def install(args=None, build_dir=None)

Executes ninja install target.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``ninja`` command. Each argument will be escaped
      according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): Build folder. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.
      If ``build_folder`` from ``configure()`` is ``None``, it will be set to ``conanfile.build_folder``.


meson_test()
++++++++++++

.. code-block:: python

    def meson_test(args=None, build_dir=None)

Executes ``meson test`` command.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``meson test`` command. Each argument will be escaped
      according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): Build folder. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.
      If ``build_folder`` from ``configure()`` is ``None``, it will be set to ``conanfile.build_folder``.


meson_install()
+++++++++++++++

.. code-block:: python

    def meson_install(args=None, build_dir=None)

Executes ``meson install`` command.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``meson install`` command. Each argument will be escaped
      according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): Build folder. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.
      If ``build_folder`` from ``configure()`` is ``None``, it will be set to ``conanfile.build_folder``.

Example
-------

A typical usage of the Meson build helper, if you want to be able to both execute :command:`conan create` and also build your package for a
library locally (in your user folder, not in the local cache), could be:

.. code-block:: python

    from conans import ConanFile, Meson

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        generators = "pkg_config"
        exports_sources = "src/*"
        requires = "zlib/1.2.11"

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

Note the ``pkg_config`` generator, which generates *.pc* files (*zlib.pc* from the example above ), which are understood by Meson to process
dependencies information (no need for a ``meson`` generator).

The layout is:

.. code-block:: text

    <folder>
      | - conanfile.py
      | - src
          | - meson.build
          | - hello.cpp
          | - hello.h

And the *meson.build* could be as simple as:

.. code-block:: text

    project('hello',
            'cpp',
            version : '0.1.0'
            default_options : ['cpp_std=c++11']
            )

    library('hello',
            ['hello.cpp'],
            dependencies: [dependency('zlib')]
            )

This allows, to create the package with :command:`conan create` as well as to build the package locally:

.. code-block:: bash

    $ cd <folder>
    $ conan create . user/testing
    # Now local build
    $ mkdir build && cd build
    $ conan install ..
    $ conan build ..
