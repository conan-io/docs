.. _MesonDeps:

MesonDeps
=========

.. important::

    This feature is still **under development**, while it is recommended and usable and we will try not to break them in future releases,
    some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.

Available since: `1.51.0 <https://github.com/conan-io/conan/releases/tag/1.51.0>`_

:ref:`MesonToolchain<conan-meson-toolchain>` normally works together with :ref:`PkgConfigDeps<PkgConfigDeps>` to manage all the dependencies,
but sometimes we need to gather some flags coming from ``Autotools`` tool so that's what ``MesonDeps`` is meant for. In other words, it is typically used
when Meson cannot find a dependency using the already known `detection mechanisms <https://mesonbuild.com/Dependencies.html>`__ like: `pkg-config`, `cmake`, `config-tool`, etc.
For instance, if we'd have these lines in your `meson.build` file, you might need ``MesonDeps`` to find that dependency and inject the correct flags to the compiler:

.. code-block:: text
    :caption: **meson.build**

    project('tutorial', 'cpp')
    cxx = meson.get_compiler('cpp')
    mylib = cxx.find_library('mylib', required: true)
    executable('app', 'main.cpp', dependencies: mylib)


In a nutshell, the ``MesonDeps`` generator is the dependencies generator for Meson and GNU flags. It creates a
`conan_meson_deps_flags.ini` file with all those flags collected by each dependency.


.. important::

    At this moment, this generator must be used along with ``MesonToolchain`` one to make it work correctly.


.. important::

    This class will require very soon to define both the "host" and "build" profiles. It is very recommended to
    start defining both profiles immediately to avoid future breaking. Furthermore, some features, like trying to
    cross-compile might not work at all if the "build" profile is not provided.


The ``MesonDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "MesonDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    MesonDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.meson import MesonDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = MesonDeps(self)
            tc.generate()

The ``MesonDeps`` generates after a ``conan install`` command a `conan_meson_deps_flags.ini` file:

.. code-block:: bash

    [constants]
    deps_c_args = []
    deps_c_link_args = []
    deps_cpp_args = []
    deps_cpp_link_args = []


This generator defines a Meson constants: ``deps_c_args``, ``deps_c_link_args``, ``deps_cpp_args``, ``deps_cpp_link_args``,
that accumulate all dependencies information, including transitive dependencies, with flags like ``-I<path>``, ``-L<path>``, etc.

.. important::

    Those variables are added automatically as part of the built-in options declared by ``MesonToolchain`` generator: ``c_args``, ``c_link_args``,
    ``cpp_args``, ``cpp_link_args``.


.. note::

    For now, only the ``requires`` information is generated, the ``tool_requires`` one is not managed by this generator yet.


Attributes
++++++++++

* ``c_args``, ``c_link_args``, ``cpp_args``, ``cpp_link_args``: list of flags that accumulate all dependencies information. Each one
  is saved as ``deps_c_args``, ``deps_c_link_args``, ``deps_cpp_args``, and ``deps_cpp_link_args``, respectively in the
  `conan_meson_deps_flags.ini` file.

.. code:: python

    from conan import ConanFile
    from conan.tools.meson import MesonDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = MesonDeps(self)
            tc.c_args.append("-val1")
            tc.c_link_args.append("-val2")
            tc.cpp_args.append("-val3")
            tc.cpp_link_args.append("-val4")
            tc.generate()
