.. _conan_tools_google:

conan.tools.google
==================

.. warning::

    These tools are **experimental** and subject to breaking changes.


BazelDeps
---------

Available since: `1.37.0 <https://github.com/conan-io/conan/releases>`_

The ``BazelDeps`` helper will generate one **conandeps/xxxx/BUILD** file per dependency. This dependencies will be
automatically added to the project if you add the following lines to the project's **WORKSPACE** file:


.. code-block:: text

    load("@//conandeps:dependencies.bzl", "load_conan_dependencies")
    load_conan_dependencies()


The dependencies should be added to the **conanfile.py** file as usual:

.. code-block:: python

    class BazelExampleConan(ConanFile):
        name = "bazel-example"
        ...
        generators = "BazelDeps", "BazelToolchain"
        requires = "boost/1.76.0"


BazelToolchain
--------------

The ``BazelToolchain`` is the toolchain generator for Bazel. It will generate a file called
``conanbuild.conf`` containing two keys:

- **bazelrc_path**: defining Bazel rc-path. Can be set using the conf ``tools.google.bazel:bazelrc_path``.
- **bazel_configs**: defining the configs to be activated in the ``bazelrc_path``.
  Can be set with the conf ``tools.google.bazel:configs``.

.. code-block:: text
   :caption: **Example of a custom bazelrc file at '/path/to/mybazelrc':**

   build:Release -c opt
   build:RelWithDebInfo -c opt --copt=-O3 --copt=-DNDEBUG
   build:MinSizeRel  -c opt --copt=-Os --copt=-DNDEBUG
   build --color=yes
   build:withTimeStamps --show_timestamps

.. code-block:: ini
   :caption: **Example of a Release profile:**

   [settings]
   ...
   build_type=Release

   [conf]
   tools.google.bazel:bazelrc_path=/path/to/mybazelrc
   tools.google.bazel:configs=["Release"]


The Bazel build helper will use that ``conanbuild.conf`` file to seamlessly call
the configure and make script using these precalculated arguments. Note that the file can have a
different name if you set the namespace argument in the constructor as explained bellow.

It supports the following methods and attributes:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, namespace=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: this argument avoids collisions when you have multiple toolchain calls in the same
  recipe. By setting this argument, the *conanbuild.conf* file used to pass information to the
  build helper will be named as: *<namespace>_conanbuild.conf*. The default value is ``None`` meaning that
  the name of the generated file is *conanbuild.conf*. This namespace must be also set with the same
  value in the constructor of the ``Bazel`` build helper so that it reads the information from the proper
  file.


Bazel
-----
The ``Bazel`` build helper is a wrapper around the command line invocation of bazel. It will abstract the
calls like ``bazel build //main:hello-world`` into Python method calls.

The helper is intended to be used in the ``build()`` method, to call Bazel commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conan import ConanFile
    from conan.tools.google import Bazel

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            bazel = Bazel(self)
            bazel.configure()
            bazel.build(label="//main:hello-world")

It supports the following methods:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, namespace=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: this argument avoids collisions when you have multiple toolchain calls in the same
  recipe. By setting this argument, the *conanbuild.conf* file used to pass information to the
  toolchain will be named as: *<namespace>_conanbuild.conf*. The default value is ``None`` meaning that
  the name of the generated file is *conanbuild.conf*. This namespace must be also set with the same
  value in the constructor of ``BazelToolchain`` so that it reads the information from the proper file.


build()
+++++++

.. code:: python

    def build(self, args=None, label=None):


Calls the build system. Equivalent to :command:`bazel build {label}` in the build folder.
