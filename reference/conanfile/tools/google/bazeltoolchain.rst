.. _conan_tools_google_bazeltoolchain:

BazelToolchain
==============

.. important::

    Some of the features used in this section are still **under development**, while they are
    recommended and usable and we will try not to break them in future releases, some breaking
    changes might still happen if necessary to prepare for the *Conan 2.0 release*.

Available since: `1.37.0 <https://github.com/conan-io/conan/releases/tag/1.37.0>`_

BazelToolchain
--------------

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


The toolchain supports the following methods and attributes:

constructor
+++++++++++

.. code-block:: python

    def __init__(self, conanfile, namespace=None):


- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: Deprecated since Conan 1.62. It only keeps backward compatibility.


Attributes
++++++++++

You can change some attributes before calling the ``generate()`` method if you want to change some of the precalculated
values:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.google import BazelToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = BazelToolchain(self)
            tc.cxxopt.append("--my_flag")
            tc.generate()

These attributes are processed and passed as part of ``build:conan-config``:

* **force_pic** (defaulted to ``fpic`` if ``options.shared == False`` and ``options.fpic == True`` else ``None``):
  Injected to the ``--force_pic`` parameter.
* **dynamic_mode** (defaulted to ``fully`` if shared, else ``off``): Injected to the ``--dynamic_mode`` parameter.
* **cppstd** (defaulted to ``None`` if your settings does not have ``settings.compiler.cppstd``
* **copt** (defaulted to ``[]``): They will be part of the ``--copt`` parameter.
* **conlyopt** (defaulted to ``[]``): They will be part of the ``--conlyopt`` parameter.
* **cxxopt** (defaulted to ``[]``): They will be part of the ``--cxxopt`` parameter.
* **linkopt** (defaulted to ``[]``): They will be part of the ``--linkopt`` parameter.
* **compilation_mode** (defaulted to ``opt`` if ``settings.build_type == "Release"``, otherwise,
  if ``settings.build_type == "Debug"``, it'll be ``dbg``): Injected to the ``--compilation_mode`` parameter.
* **compiler** (defaulted to ``None``): Injected to the ``--compiler`` parameter.
* **cpu** (defaulted to ``None``): Injected to the ``--cpu`` parameter.
* **crosstool_top** (defaulted to ``None``): Injected to the ``--crosstool_top`` parameter.


conf
+++++

``BazelToolchain`` is affected by these :ref:`[conf]<global_conf>` variables:

- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``cxxopt``.
- ``tools.build:cflags`` list of extra of pure C flags that will be used by ``conlyopt``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``linkopt``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by ``linkopt``.
- ``tools.build:linker_scripts`` list of linker scripts, each of which will be prefixed with ``-T`` and added to ``linkopt``.
