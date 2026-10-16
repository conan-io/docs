.. _conan_tools_google_bazeltoolchain:

BazelToolchain
==============

.. include:: ../../../common/experimental_warning.inc

The ``BazelToolchain`` is the toolchain generator for Bazel. It will generate a ``conan_bzl.rc`` file that contains
a build configuration ``conan-config`` to inject all the parameters into the :command:`bazel build` command.

The ``BazelToolchain`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "BazelToolchain"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    BazelToolchain

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.google import BazelToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = BazelToolchain(self)
            tc.generate()

Generated files
---------------

After running :command:`conan install` command, the ``BazelToolchain`` generates the *conan_bzl.rc* file
that contains Bazel build parameters (it will depend on your current Conan settings and options from your *default* profile):

.. code-block:: text
    :caption: conan_bzl.rc

    # Automatic bazelrc file created by Conan

    build:conan-config --cxxopt=-std=gnu++17

    build:conan-config --dynamic_mode=off
    build:conan-config --compilation_mode=opt

The :ref:`Bazel build helper<conan_tools_google_bazel>` will use that ``conan_bzl.rc`` file to perform a call using this
configuration. The outcoming command will look like this :command:`bazel --bazelrc=/path/to/conan_bzl.rc build --config=conan-config <target>`.


Reference
---------

.. currentmodule:: conan.tools.google

.. autoclass:: BazelToolchain
    :members:


conf
+++++

``BazelToolchain`` is affected by these :ref:`[conf]<reference_config_files_global_conf>` variables:

- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``cxxopt``.
- ``tools.build:cflags`` list of extra of pure C flags that will be used by ``conlyopt``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``linkopt``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by ``linkopt``.
- ``tools.build:linker_scripts`` list of linker scripts, each of which will be prefixed with ``-T`` and added to ``linkopt``.


.. seealso::

    - :ref:`examples_tools_bazel_toolchain_build_simple_bazel_project`
